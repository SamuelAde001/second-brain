r"""resolve_guard.py - look before you touch Resolve: memory, who owns it, stray helper Chromes (Editor, 2026-10-30).
External Python 3, stdlib only (psutil is not installed). Read-only except `clean-chromes` (without --dry-run).
Built 2026-10-30 after video 4's crashes: a whole fix round voided when Resolve crashed from 07:55, a trial install
that crashed Resolve while the render queue was also running, 18 leftover headless helper Chromes that ate the RAM,
and a review render stopped at 14 % for memory.

  python resolve_guard.py status      --kits <kits dir> [--job <dir>]
  python resolve_guard.py preflight   --kits <kits dir> --for install|render|build [--min-free-gb 8]
                                      [--max-resolve-gb 16] [--owner <name>] [--job <dir>]
  python resolve_guard.py clean-chromes [--dry-run] [--kits <kits dir>] [--job <dir>] [--min-age-min N]

status     ONE json line: free_ram_gb (available physical RAM), free_commit_gb (info), resolve ("running" |
           "not responding" | "not running") + resolve_gb (Resolve.exe working set, null when not running), lock
           {holder: render-queue | kit-pipe | <other owner> | none, pid, age_s, stale}, queue {running, pending,
           in_progress}, helper_chromes (instances) and helper_chrome_procs (processes).
preflight  Exit 0 = safe to go, exit 2 = blocked (reasons printed as json on stdout and as a BLOCKED line on stderr).
           install / render (a full timeline render) BLOCK when: the render queue is running (stop it, or let its
           batch finish); the lab lock is held by anyone (never two Resolve owners at once; --owner <name> ignores a
           lock held by that name, for a script that already took it); free RAM is under --min-free-gb; Resolve is
           over --max-resolve-gb or not responding (save the project, then restart_resolve.py --force /
           restart_resolve.py); Resolve's state cannot be read. build only WARNS (exit 0). A lock whose owner pid is
           dead (or an age-only lock older than 15 min) is stale: lab.py clears it, so it is a warning, not a block.
           Leftover helper Chromes are a warning (and named in the RAM reason): run clean-chromes.
clean-chromes
           Stops ONLY headless helper Chromes: chrome.exe (or chrome-headless-shell.exe) started with --headless or
           --remote-debugging-port AND an explicit --user-data-dir under %TEMP% / %TMP%, the Routerise client folder,
           a --job dir or the --kits dir; plus the child processes of those and anything else using the same profile
           dir. A Chrome without those flags or with the default profile (Samuel's own browser) is never touched.
           --dry-run lists instances, PIDs and shortened command lines and stops nothing. --min-age-min N leaves
           helpers younger than N minutes alone (a sibling helper may be mid-recording).

Exit codes: 0 ok / safe, 2 preflight blocked, 1 could not read the machine state, 64 wrong usage.
"""
import os, sys, re, json, time, glob, csv, ctypes, base64, argparse, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RESTART = os.path.join(os.path.dirname(HERE), "restart_resolve.py")
ROUTERISE = r"C:\Users\repzy\Desktop\Video edits\Routerise"
CHROME_NAMES = ("chrome.exe", "chrome-headless-shell.exe")
STALE_S = 15 * 60               # lab.py: a lock older than this, or whose pid is dead, is stale
ALIVE_S = 60                    # lab.py: queue.alive fresher than this = render_queue.py owns Resolve
GB = 1073741824.0


# ------------------------------------------------------------------------------------------------------- windows bits
class _MemStat(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


def memory():
    """(available physical GB, total physical GB, available commit GB)."""
    m = _MemStat()
    m.dwLength = ctypes.sizeof(_MemStat)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
        raise OSError("GlobalMemoryStatusEx failed")
    return m.ullAvailPhys / GB, m.ullTotalPhys / GB, m.ullAvailPageFile / GB


def pid_alive(pid):
    """Same test as lab.py: pid 0 = age-only lock (counts as alive)."""
    if not pid:
        return True
    try:
        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x1000, False, int(pid))              # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        code = ctypes.c_ulong()
        k.GetExitCodeProcess(h, ctypes.byref(code)); k.CloseHandle(h)
        return code.value == 259                                # STILL_ACTIVE
    except Exception:
        return True


def split_cmdline(cmd):
    """Windows command line -> argv (CommandLineToArgvW), regex fallback."""
    try:
        sh = ctypes.windll.shell32
        sh.CommandLineToArgvW.restype = ctypes.POINTER(ctypes.c_wchar_p)
        sh.CommandLineToArgvW.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_int)]
        n = ctypes.c_int(0)
        p = sh.CommandLineToArgvW(cmd, ctypes.byref(n))
        if p:
            try:
                return [p[i] for i in range(n.value)]
            finally:
                ctypes.windll.kernel32.LocalFree.argtypes = [ctypes.c_void_p]
                ctypes.windll.kernel32.LocalFree(ctypes.cast(p, ctypes.c_void_p))
    except Exception:
        pass
    return [a.strip('"') for a in re.findall(r'"[^"]*"|\S+', cmd)]


def norm(p):
    """Normalised absolute path for comparisons (long form, lower case, no trailing slash)."""
    p = os.path.abspath(os.path.expandvars(p))
    try:
        buf = ctypes.create_unicode_buffer(32768)
        if ctypes.windll.kernel32.GetLongPathNameW(p, buf, 32768):
            p = buf.value
    except Exception:
        pass
    return os.path.normcase(os.path.normpath(p))


def under(path, root):
    return path == root or path.startswith(root.rstrip("\\/") + os.sep)


# ---------------------------------------------------------------------------------------------------------- resolve
def resolve_state():
    """('running' | 'not responding' | 'not running' | 'unknown', working-set GB or None). Same tasklist calls as
    render_queue.py / restart_resolve.py."""
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Resolve.exe", "/FO", "CSV", "/NH"],
                             capture_output=True, text=True, timeout=30).stdout
        rows = [r for r in csv.reader(out.splitlines()) if r and r[0].lower() == "resolve.exe"]
        if not rows:
            return "not running", None
        kb = sum(int(re.sub(r"\D", "", r[4]) or 0) for r in rows if len(r) > 4)
        nr = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Resolve.exe", "/FI", "STATUS eq NOT RESPONDING", "/FO",
                             "CSV", "/NH"], capture_output=True, text=True, timeout=30).stdout
        return ("not responding" if "resolve.exe" in nr.lower() else "running"), round(kb / 1048576.0, 1)
    except Exception:
        return "unknown", None


# ------------------------------------------------------------------------------------------------- lock and queue
def lock_state(kits):
    """The lab.py lock <kits>\\_cache\\resolve.lock: who, pid, age, stale (lab.py's rule)."""
    path = os.path.join(kits, "_cache", "resolve.lock")
    if not os.path.exists(path):
        return {"holder": "none"}
    try:
        info = json.load(open(path, encoding="utf-8"))
    except FileNotFoundError:
        return {"holder": "none"}
    except Exception:
        try:
            mt = os.path.getmtime(path)
        except OSError:
            return {"holder": "none"}
        info = {"owner": "?", "pid": 0, "time": mt}
    age = max(0, int(time.time() - float(info.get("time", 0) or 0)))
    pid = int(info.get("pid") or 0)
    alive = pid_alive(pid)
    stale = age > STALE_S or not alive
    return {"holder": str(info.get("owner") or "?"), "pid": pid, "age_s": age, "stale": stale, "pid_alive": alive}


def queue_state(kits):
    q = os.path.join(kits, "_queue")
    alive_f = os.path.join(q, "queue.alive")
    run = os.path.exists(alive_f) and time.time() - os.path.getmtime(alive_f) < ALIVE_S
    cnt = lambda sub: len(glob.glob(os.path.join(q, sub, "*.json")))
    return {"running": bool(run), "pending": cnt("requests"), "in_progress": cnt("running")}


# ----------------------------------------------------------------------------------------------------------- chromes
def _ps(script, timeout=90):
    enc = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", enc], capture_output=True,
                       timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or b"").decode("utf-8", "replace").strip()[:200] or "powershell failed")
    return (r.stdout or b"").decode("utf-8", "replace")


def chrome_processes():
    """All chrome.exe / chrome-headless-shell.exe processes: [{p, pp, n, c, t (FILETIME)}]."""
    flt = " OR ".join("Name='%s'" % n for n in CHROME_NAMES)
    ps = ("$ErrorActionPreference='Stop'\n"
          "try { [Console]::OutputEncoding=[Text.Encoding]::UTF8 } catch {}\n"
          "$r=@(Get-CimInstance Win32_Process -Filter \"%s\" | ForEach-Object { [pscustomobject]@{"
          "p=[int]$_.ProcessId; pp=[int]$_.ParentProcessId; n=[string]$_.Name; c=[string]$_.CommandLine; "
          "t=$(if($_.CreationDate){[int64]$_.CreationDate.ToFileTimeUtc()}else{[int64]0})} })\n"
          "ConvertTo-Json -InputObject $r -Compress -Depth 3\n" % flt)
    out = _ps(ps).strip()
    data = json.loads(out) if out else []
    return [data] if isinstance(data, dict) else data


def allowed_roots(kits=None, jobs=()):
    roots = {norm(os.environ[k]) for k in ("TEMP", "TMP") if os.environ.get(k)}
    roots.add(norm(tempfile.gettempdir()))
    roots.add(norm(ROUTERISE))
    for j in jobs or ():
        roots.add(norm(j))
    if kits:
        roots.add(norm(kits))
    return sorted(roots)


def find_helpers(procs, roots):
    """-> {pid: {key, root}}: headless helper Chromes only.
    A seed is a process that has --headless or --remote-debugging-port AND --user-data-dir=<dir under roots>.
    Helpers = seeds + processes using the same profile dir + all descendants of those (Chrome's renderer/gpu/crashpad
    children). Anything else, notably a Chrome with the default profile or no such flags, is never in the set."""
    byid = {p["p"]: p for p in procs}
    info = {}
    for p in procs:
        flags, udd = False, None
        for a in split_cmdline(p.get("c") or ""):
            al = a.lower()
            if al == "--headless" or al.startswith("--headless=") or al.startswith("--remote-debugging-port"):
                flags = True
            elif al.startswith("--user-data-dir="):
                v = a.split("=", 1)[1].strip().strip('"')
                udd = norm(v) if v else None
        info[p["p"]] = (flags, udd)
    seeds = {pid for pid, (f, u) in info.items() if f and u and any(under(u, r) for r in roots)}
    udds = {info[pid][1] for pid in seeds}
    helpers = set(seeds) | {pid for pid, (f, u) in info.items() if u and u in udds}
    grew = True
    while grew:
        grew = False
        for p in procs:
            par = byid.get(p["pp"])
            if p["p"] not in helpers and par is not None and p["pp"] in helpers and p["t"] >= par["t"]:
                helpers.add(p["p"]); grew = True

    def top(pid):
        seen = set()
        while pid not in seen:
            seen.add(pid)
            par = byid.get(byid[pid]["pp"])
            if par is not None and par["p"] in helpers and par["t"] <= byid[pid]["t"]:
                pid = par["p"]
            else:
                break
        return pid
    out = {}
    for pid in helpers:
        r = top(pid)
        out[pid] = {"key": info[pid][1] or info[r][1] or "pid:%d" % r, "root": r}
    return out


def helper_groups(procs, helpers):
    """Instances: {key: [process dicts]}."""
    byid = {p["p"]: p for p in procs}
    g = {}
    for pid, h in helpers.items():
        g.setdefault(h["key"], []).append(byid[pid])
    return g


def chrome_count(kits=None, jobs=()):
    """(instances, processes) or (None, None) when the process list cannot be read."""
    try:
        procs = chrome_processes()
        hp = find_helpers(procs, allowed_roots(kits, jobs))
        return len({h["key"] for h in hp.values()}), len(hp)
    except Exception:
        return None, None


# ------------------------------------------------------------------------------------------------------------ status
def snapshot(kits, jobs=()):
    free, total, commit = memory()
    st, gb = resolve_state()
    inst, nproc = chrome_count(kits, jobs)
    return {"free_ram_gb": round(free, 1), "total_ram_gb": round(total, 1), "free_commit_gb": round(commit, 1),
            "resolve": st, "resolve_gb": gb, "lock": lock_state(kits), "queue": queue_state(kits),
            "helper_chromes": inst, "helper_chrome_procs": nproc}


def need_kits(a):
    k = os.path.abspath(a.kits)
    if not os.path.exists(os.path.join(k, "lab.py")):
        usage_error("--kits must be the folder holding lab.py: " + k)
    return k


def cmd_status(a):
    print(json.dumps(snapshot(need_kits(a), a.job)))
    return 0


# --------------------------------------------------------------------------------------------------------- preflight
def cmd_preflight(a):
    kits = need_kits(a)
    s = snapshot(kits, a.job)
    hard, warn = [], []                          # for install/render both are blocks; for build both are warnings
    q, lk = s["queue"], s["lock"]
    if q["running"]:
        hard.append("render queue is running (%d pending, %d in progress): stop it, or wait until it is idle, "
                    "so two scripts never drive Resolve at once" % (q["pending"], q["in_progress"]))
    if lk["holder"] != "none" and lk["holder"] != a.owner:
        who = "%s (pid %s, %d s old)" % (lk["holder"], lk["pid"], lk["age_s"])
        if not lk["pid_alive"] or (lk["pid"] == 0 and lk["age_s"] > STALE_S):
            warn.append("stale Resolve lock from %s: lab.py will clear it, nothing to wait for" % who)
        elif lk["age_s"] > STALE_S:
            hard.append("Resolve lock held by %s, no heartbeat for %d min and the process is still alive: check it is "
                        "not hung before breaking it (lab.py unlock <owner> --force)" % (who, lk["age_s"] // 60))
        else:
            hard.append("Resolve lock held by %s: wait for it to finish" % who)
    ch = ""
    if s["helper_chromes"]:
        ch = " (%d leftover helper Chromes, %d processes: run resolve_guard.py clean-chromes)" % (
            s["helper_chromes"], s["helper_chrome_procs"])
    if s["free_ram_gb"] < a.min_free_gb:
        hard.append("free RAM %.1f GB is under the %g GB minimum%s" % (s["free_ram_gb"], a.min_free_gb, ch))
    elif ch:
        warn.append(ch.strip(" ()"))
    if s["resolve"] == "unknown":
        hard.append("cannot read Resolve's state (tasklist failed)")
    elif s["resolve"] == "not responding":
        hard.append("Resolve is not responding: python \"%s\" (it kills and relaunches a hung Resolve)" % RESTART)
    elif s["resolve"] == "not running":
        warn.append("Resolve is not running: start it with python \"%s\" before the job" % RESTART)
    elif s["resolve_gb"] is not None and s["resolve_gb"] > a.max_resolve_gb:
        hard.append("Resolve is using %.1f GB (over %g GB): save the project by script, then restart it with "
                    "python \"%s\" --force first" % (s["resolve_gb"], a.max_resolve_gb, RESTART))
    if s["helper_chromes"] is None:
        warn.append("could not read the Chrome process list")
    blocked = hard if a.for_ != "build" else []
    warnings = warn if a.for_ != "build" else hard + warn
    res = {"for": a.for_, "go": not blocked, "blocked": blocked, "warnings": warnings,
           "free_ram_gb": s["free_ram_gb"], "resolve": s["resolve"], "resolve_gb": s["resolve_gb"],
           "lock": lk["holder"], "queue_running": q["running"], "helper_chromes": s["helper_chromes"]}
    print(json.dumps(res))
    if blocked:
        print("BLOCKED (%s): %s" % (a.for_, " | ".join(blocked)), file=sys.stderr)
        return 2
    return 0


# --------------------------------------------------------------------------------------------------- clean-chromes
def shorten(cmd, roots, n=150):
    for r in sorted(roots, key=len, reverse=True):               # longest root first
        cmd = re.sub(re.escape(r), "<dir>", cmd, flags=re.I)
    cmd = re.sub(r"^\"?[^\"]*?(chrome(?:-headless-shell)?\.exe)\"?", r"\1", cmd, flags=re.I)
    return cmd if len(cmd) <= n else cmd[:n - 3] + "..."


def cmd_clean(a):
    kits = os.path.abspath(a.kits) if a.kits else None
    roots = allowed_roots(kits, a.job)
    procs = chrome_processes()
    helpers = find_helpers(procs, roots)
    now_ft = (time.time() + 11644473600) * 1e7
    age = lambda p: int((now_ft - p["t"]) / 1e7 / 60) if p["t"] else 0
    groups = helper_groups(procs, helpers)
    victims = set()
    lines = []
    for key, ps in sorted(groups.items(), key=lambda kv: min(p["p"] for p in kv[1])):
        oldest = max(age(p) for p in ps)
        youngest = min(age(p) for p in ps)
        if a.min_age_min and youngest < a.min_age_min:
            lines.append("  keep  %-6s %d proc, youngest %d min < --min-age-min %d  %s" % (
                min(p["p"] for p in ps), len(ps), youngest, a.min_age_min, os.path.basename(key)))
            continue
        victims.update(p["p"] for p in ps)
        top = next((p for p in ps if "--type=" not in (p.get("c") or "")), min(ps, key=lambda p: p["p"]))
        pids = sorted(p["p"] for p in ps)
        lines.append("  %s %-6s %d proc, %d min  pids %s%s\n         %s" % (
            "would stop" if a.dry_run else "stop", top["p"], len(ps), oldest,
            ",".join(map(str, pids[:12])), "..." if len(pids) > 12 else "", shorten(top.get("c") or "", roots)))
    print("%d helper Chrome instance(s), %d process(es) of %d Chrome processes in total%s" % (
        len(groups), len(helpers), len(procs), " (dry run, nothing stopped)" if a.dry_run else ""))
    for l in lines:
        print(l)
    if a.dry_run or not victims:
        print(json.dumps({"dry_run": bool(a.dry_run), "instances": len(groups), "processes": len(helpers),
                          "would_stop": len(victims) if a.dry_run else 0, "stopped": 0}))
        return 0
    todo = sorted(victims)
    for i in range(0, len(todo), 30):
        cmd = ["taskkill", "/F"]
        for pid in todo[i:i + 30]:
            cmd += ["/PID", str(pid)]
        subprocess.run(cmd, capture_output=True, timeout=120)
    time.sleep(1.5)
    left = {p["p"] for p in chrome_processes()} & victims
    print(json.dumps({"dry_run": False, "instances": len(groups), "stopped": len(victims) - len(left),
                      "remaining": len(left)}))
    return 0 if not left else 1


# -------------------------------------------------------------------------------------------------------------- main
def usage_error(msg):
    print("resolve_guard.py: " + msg, file=sys.stderr)
    sys.exit(64)


class Parser(argparse.ArgumentParser):
    def error(self, message):                    # argparse's own exit code 2 would look like "preflight blocked"
        self.print_usage(sys.stderr)
        usage_error(message)


def build_parser():
    P = Parser(prog="resolve_guard.py", description=__doc__.split("\n")[0],
               epilog="Built 2026-10-30 after video 4's crashes. Full usage: see the header of this file.")
    sub = P.add_subparsers(dest="cmd", required=True, parser_class=Parser)
    common = Parser(add_help=False)
    common.add_argument("--job", action="append", default=[], metavar="DIR",
                        help="extra folder where helper Chrome profiles may live (repeatable)")
    s = sub.add_parser("status", parents=[common], help="one json line: RAM, Resolve, lock, queue, helper Chromes")
    s.add_argument("--kits", required=True, help="the kits folder (holds lab.py)")
    s.set_defaults(fn=cmd_status)
    f = sub.add_parser("preflight", parents=[common], help="exit 0 = safe to go, 2 = blocked")
    f.add_argument("--kits", required=True, help="the kits folder (holds lab.py)")
    f.add_argument("--for", dest="for_", required=True, choices=("install", "render", "build"))
    f.add_argument("--min-free-gb", type=float, default=8.0)
    f.add_argument("--max-resolve-gb", type=float, default=16.0)
    f.add_argument("--owner", default=None, help="ignore a lock held by this owner name (you already took it)")
    f.set_defaults(fn=cmd_preflight)
    c = sub.add_parser("clean-chromes", parents=[common], help="stop headless helper Chromes only")
    c.add_argument("--dry-run", action="store_true", help="list what would be stopped, stop nothing")
    c.add_argument("--kits", default=None, help="also treat profiles under this kits folder as helper profiles")
    c.add_argument("--min-age-min", type=int, default=0, help="leave helpers younger than N minutes alone")
    c.set_defaults(fn=cmd_clean)
    return P


def main(argv):
    try:
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    except Exception:
        pass
    a = build_parser().parse_args(argv)
    try:
        return a.fn(a)
    except SystemExit:
        raise
    except Exception as e:
        print("resolve_guard.py: cannot read the machine state: %r" % (e,), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
