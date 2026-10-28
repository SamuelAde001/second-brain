r"""render_queue.py - one script owns Resolve; helpers drop render requests in a folder (Editor, 2026-10-28).
External Python. Replaces helpers waiting on lab.py's Resolve lock (36 of 97 helper-hours on video 2).

  python render_queue.py run    --kits <kits dir> [--project "<name start>"] [--batch 6] [--frame-budget 2010]
                                [--mem-gb 16] [--idle-exit S] [--fake]
  python render_queue.py submit --kits <kits dir> <request.json>        -> {"id", "done"}  (copies it into requests\)
  python render_queue.py clip   --kits <kits dir> --manifest <m.json> --out <dir> [--name N] [--pad 12] [--res 960x540]
  python render_queue.py status --kits <kits dir>
  python render_queue.py wait   --kits <kits dir> <id> [<id> ...] [--wait 1800]     prints each done json

Folder: <kits>\_queue\ = requests\ (helpers write <id>.json) -> running\ -> done\<id>.json (always written: ok,
files, errors, secs, tries). queue.alive is refreshed every few seconds while `run` is up; lab.py render hands its
job to the queue when queue.alive is fresh (no lock wait) unless given --direct.

Request:  {"id": "HK-02_clip_r1", "kind": "stills" | "deliver" | "both" | "clip", "owner": "<helper>", "priority": 0,
           "manifest": "<manifest.json>"   -> layers, offsets, below aroll@start and D from its ops (clip kind), or
           "layers": [["setting", "<a.setting>"], ["media", "<file@src_in>"]], "below": "none"|"aroll@F"|"<file>",
           "D": n, "frames": [0, 40], "out": "<dir>", "prefix": "...", "fonts": [], "track": 2,
           "res": [960, 540], "audio": true, "pad": 12, "name": "<file stem>"  (clip kind)}
  stills/deliver/both run lab.render() as `lab.py render` would. clip lays the beat on "zz Lab (Editor)" over the
  A-roll (V1 picture + A1 sound of the cut, pad frames either side) and renders one small H.264 mp4 from Deliver.

How it keeps Resolve alive: one batch (up to --batch requests) per worker process, holding lab's lock as
"render-queue". The worker writes a heartbeat per Resolve step with that step's budget; a step past its budget =
hang: the worker is killed, Resolve restarted (restart_resolve.py; --force when Windows still says it responds,
because a timed-out script keeps running inside Resolve), the project reopened (kits\open_job.py --name), and the
request retried once. Between batches Resolve is restarted with --force once 2010 frames have rendered since the
last restart or Resolve uses more than --mem-gb (video 2 v7: one 4K pass crashed at ~3000 f; 2010-f chunks with a
restart each rendered clean; memory climbed 6 -> 19.5 GB over a long lab session on 2026-10-25).
"""
import os, sys, json, time, glob, shutil, subprocess, re, csv, threading, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
RESTART = next((p for p in (os.path.join(os.path.dirname(HERE), "restart_resolve.py"),       # Brain copy, or a kit copy
                            r"C:\Users\repzy\Desktop\My Second brain\03-Areas\video-editing\scripts\restart_resolve.py")
                if os.path.exists(p)), "restart_resolve.py")
MAX_TRIES = 2
OWNER = "render-queue"
ALIVE_S = 60


# --------------------------------------------------------------------------------------------------------- folders
def kits_dir(argv):
    k = argv[argv.index("--kits") + 1] if "--kits" in argv else (HERE if os.path.exists(os.path.join(HERE, "lab.py"))
                                                                else None)
    assert k and os.path.exists(os.path.join(k, "lab.py")), "give --kits <folder with lab.py>"
    return os.path.abspath(k)


def qdirs(kits):
    q = os.path.join(kits, "_queue")
    d = {x: os.path.join(q, x) for x in ("requests", "running", "done", "batches")}
    for p in d.values():
        os.makedirs(p, exist_ok=True)
    d["root"] = q
    d["alive"] = os.path.join(q, "queue.alive")
    d["beat"] = os.path.join(q, "worker.beat")
    d["log"] = os.path.join(q, "queue.log")
    return d


def _wjson(path, obj):
    tmp = path + ".tmp%d" % os.getpid()
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def _rjson(path, default=None):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return default


def log(Q, *a):
    line = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(line, flush=True)
    with open(Q["log"], "a", encoding="utf-8") as f:
        f.write(line + "\n")


def alive(Q):
    return os.path.exists(Q["alive"]) and time.time() - os.path.getmtime(Q["alive"]) < ALIVE_S


def submit(Q, req):
    req = dict(req)
    req.setdefault("id", "%s_%s" % (re.sub(r"\W+", "_", req.get("name") or req.get("prefix") or "req")[:40],
                                    hashlib.sha1(json.dumps(req, sort_keys=True).encode()).hexdigest()[:8]))
    req.setdefault("submitted", time.time())
    for old in (os.path.join(Q["done"], req["id"] + ".json"),):
        if os.path.exists(old):
            os.replace(old, old + ".prev")
    _wjson(os.path.join(Q["requests"], req["id"] + ".json"), req)
    return req["id"], os.path.join(Q["done"], req["id"] + ".json")


def wait_done(Q, ids, wait=1800):
    t0, out = time.time(), {}
    while time.time() - t0 < wait and len(out) < len(ids):
        for i in ids:
            if i not in out:
                d = _rjson(os.path.join(Q["done"], i + ".json"))
                if d is not None:
                    out[i] = d
        if len(out) < len(ids):
            time.sleep(3)
    return out


# ------------------------------------------------------------------------------------------------- manifest -> job
def from_manifest(mpath, pad=12):
    """manifest ops -> (layers with offsets, S, D) for a clip of the whole beat."""
    ops = [o for o in json.load(open(mpath, encoding="utf-8")) if o.get("op") in ("comp", "media")]
    assert ops, "no ops in " + mpath
    S = min(int(o["start"]) for o in ops)
    E = max(int(o["start"]) + int(o["D"]) for o in ops)
    lay = []
    for o in sorted(ops, key=lambda o: (int(o.get("track", 2)), int(o["start"]))):
        lay.append({"kind": "setting" if o["op"] == "comp" else "media",
                    "path": o["setting"] if o["op"] == "comp" else o["path"], "track": int(o.get("track", 2)),
                    "off": int(o["start"]) - S + pad, "D": int(o["D"]), "src_in": int(o.get("src_in", 0) or 0),
                    "fonts": o.get("fonts") or []})
    return lay, S, E - S


# ---------------------------------------------------------------------------------------------------------- worker
class Beat:
    """Stands in for lab.W: records each Resolve step and its budget in worker.beat for the supervisor to watch."""

    def __init__(self, path):
        self.path, self.req, self.owner, self.on, self.step = path, None, None, True, None
        self.res = {"ok": False, "errors": []}

    def __call__(self, step, budget=60):
        self.step = step
        _wjson(self.path, {"pid": os.getpid(), "req": self.req, "step": step, "t": time.time(), "budget": budget})


def _aroll_audio(lab, p, mp, t, S0, F, D, tl_name, errs):
    """A1 of the cut under the lab timeline, frames F..F+D (the beat's own sound, so its timing can be judged)."""
    src = lab._find_tl(p, tl_name)
    s0 = src.GetStartFrame()
    placed = 0
    for it in src.GetItemListInTrack("audio", 1) or []:
        a, b = it.GetStart() - s0, it.GetEnd() - s0
        lo, hi = max(a, F), min(b, F + D)
        if lo >= hi:
            continue
        mpi = it.GetMediaPoolItem()
        ss, se = it.GetSourceStartFrame(), it.GetSourceEndFrame()
        r = float(se - ss) / float(b - a) if b > a else 1.0
        si = int(round(ss + (lo - a) * r))
        ok = mp.AppendToTimeline([{"mediaPoolItem": mpi, "startFrame": si, "endFrame": si + int(round((hi - lo) * r)),
                                   "trackIndex": 1, "recordFrame": S0 + (lo - F), "mediaType": 2}])
        placed += (hi - lo) if ok else 0
    if placed < D:
        errs.append("audio covers %d of %d frames" % (placed, D))


def render_clip(lab, req):
    W = lab.W
    errs = W.res["errors"]
    t_start = time.time()
    resolve = lab._connect()
    K = lab._kit(resolve); lab.K_TC = K["tc"]
    W("project", 20)
    pm = resolve.GetProjectManager(); p = pm.GetCurrentProject(); mp = p.GetMediaPool()
    W.res["project"] = p.GetName()
    cur = p.GetCurrentTimeline(); cur_name = cur.GetName() if cur else None
    pad = int(req.get("pad", 12))
    if req.get("manifest"):
        lay, S, D = from_manifest(req["manifest"], pad)
        below = "aroll@%d" % (S - pad)
    else:
        lay = [{"kind": k, "path": v, "track": int(req.get("track", 2)) + n, "off": pad, "D": int(req["D"]),
                "src_in": 0, "fonts": req.get("fonts") or []} for n, (k, v) in enumerate(req["layers"])]
        S, D, below = None, int(req["D"]), req.get("below", "none")
    DT = D + 2 * pad
    out = req["out"]; os.makedirs(out, exist_ok=True)
    name = req.get("name") or req["id"]
    w, h = (req.get("res") or [960, 540])[:2]
    aroll_tl = req.get("aroll_tl") or lab.AROLL_TL
    fold = lab._lab_bin(mp)
    files = []
    try:
        W("lab timeline", 60)
        resolve.OpenPage("edit")
        t = lab._lab_tl(p, mp, fold)
        S0 = t.GetStartFrame()
        lab._clear(t)
        while t.GetTrackCount("video") < max([2] + [L["track"] for L in lay]):
            t.AddTrack("video")
        W("below", 120)
        if below.lower().startswith("aroll@"):
            F = int(below[6:])
            lab._aroll(K, p, mp, t, S0, F, DT, aroll_tl, errs)
            if req.get("audio", True):
                _aroll_audio(lab, p, mp, t, S0, F, DT, aroll_tl, errs)
        elif below.lower() != "none":
            lab._media_layer(K, mp, fold, t, 1, S0, below, DT, errs)
        base = None
        for L in lay:
            tr, rec, Dl = L["track"], S0 + L["off"], L["D"]
            if L["kind"] == "media":
                W("media V%d" % tr, 90)
                lab._media_layer(K, mp, fold, t, tr, rec, L["path"] + ("@%d" % L["src_in"] if L["src_in"] else ""), Dl,
                                 errs)
                continue
            if not os.path.exists(L["path"]):
                errs.append("missing " + L["path"]); continue
            W("base V%d" % tr, 60)
            base = base or K["_pool_clip"](mp, fold, K["BASE_SRC"])
            it, note = K["_place"](t, mp, base, tr, rec, Dl, 0)
            if not it or it.GetEnd() != rec + Dl:
                errs.append("base V%d not placed" % tr); continue
            W("paste V%d %s" % (tr, os.path.basename(L["path"])), 150)
            key = ("q_%d_%s" % (tr, re.sub(r"\W+", "_", os.path.splitext(os.path.basename(L["path"]))[0])))[:60]
            try:
                comp = K["_open_fusion"](t, tr, rec, Dl)
                r = K["_paste"](comp, L["path"], key, L["fonts"]) if comp else {"err": "no comp on Fusion page"}
            finally:
                resolve.OpenPage("edit")
            if r.get("err"):
                errs.append("paste V%d: %s" % (tr, r["err"])); continue
            W("reimport V%d" % tr, 90)
            rr = K["_reimport"](it, key, L["path"])
            if rr is not True:
                errs.append("reimport V%d: %s" % (tr, rr))
        W("deliver setup", 30)
        before = p.GetCurrentRenderFormatAndCodec() or {}
        if not p.SetCurrentRenderFormatAndCodec("mp4", "H264"):
            errs.append("deliver: mp4/H264 not set")
        p.SetCurrentRenderMode(1)
        d = os.path.join(lab.TMP, "clip", "%d" % int(time.time() * 1000))
        os.makedirs(d, exist_ok=True)
        p.SetRenderSettings({"SelectAllFrames": False, "MarkIn": S0, "MarkOut": S0 + DT - 1, "TargetDir": d,
                             "CustomName": name, "ExportVideo": True, "ExportAudio": bool(req.get("audio", True)),
                             "FormatWidth": int(w), "FormatHeight": int(h)})
        j = p.AddRenderJob()
        if not j:
            errs.append("deliver: job not added")
        else:
            W("deliver render %d f" % DT, 120 + 4 * DT)
            p.StartRendering([j], False)
            time.sleep(1)
            while p.IsRenderingInProgress():
                time.sleep(0.5)
            W("deliver collect", 30)
            st = p.GetRenderJobStatus(j) or {}
            got = sorted(glob.glob(os.path.join(d, "*.mp4")) + glob.glob(os.path.join(d, "*.mov")))
            if got:
                dst = os.path.join(out, name + os.path.splitext(got[-1])[1])
                shutil.copyfile(got[-1], dst)
                files.append(dst)
            else:
                errs.append("deliver: %s" % st.get("JobStatus"))
            p.DeleteRenderJob(j)
        p.SetRenderSettings({"SelectAllFrames": True})
        if before.get("format") and before.get("format") != "unknown":
            p.SetCurrentRenderFormatAndCodec(before["format"], before.get("codec", ""))
        shutil.rmtree(d, ignore_errors=True)
    finally:
        W("restore", 60)
        try:
            resolve.OpenPage("edit")
            t = lab._find_tl(p, lab.LAB)
            if t and not req.get("keep"):
                lab._clear(t)
            back = lab._find_tl(p, cur_name) if cur_name else None
            if back:
                p.SetCurrentTimeline(back)
            W("save", 60)
            W.res["saved"] = bool(pm.SaveProject())
        except Exception as e:
            errs.append("restore: " + repr(e)[:160])
    W.res.update({"files": files, "D": DT, "S": S, "pad": pad, "secs": round(time.time() - t_start, 1),
                  "frames_rendered": DT})
    W.res["ok"] = bool(files) and not [e for e in errs if not e.startswith("audio covers")]
    return W.res


def _lab_args(req):
    return {"layers": [tuple(x) for x in req["layers"]], "below": req.get("below", "none"), "D": int(req.get("D", 0)),
            "frames": [int(f) for f in req["frames"]], "out": req["out"], "track": int(req.get("track", 2)),
            "fonts": req.get("fonts") or [], "via": {"stills": "stills", "deliver": "deliver"}.get(req["kind"], "both"),
            "prefix": req.get("prefix"), "keep": bool(req.get("keep")), "owner": OWNER, "wait": 0,
            "aroll_tl": req.get("aroll_tl") or None}


def worker(batch_path, kits, fake=False):
    Q = qdirs(kits)
    batch = _rjson(batch_path)
    sys.path.insert(0, kits)
    lab = None
    if not fake:
        import lab as _lab
        lab = _lab
        lab.W = Beat(Q["beat"])
    for req in batch["reqs"]:
        t0 = time.time()
        if fake:
            b = Beat(Q["beat"]); b.req = req["id"]; b("fake render", 20)
            if req.get("fake_hang"):
                time.sleep(3600)
            time.sleep(1)
            os.makedirs(req["out"], exist_ok=True)
            fp = os.path.join(req["out"], (req.get("name") or req["id"]) + ".txt")
            open(fp, "w").write("fake")
            res = {"ok": True, "files": [fp], "errors": [], "frames_rendered": 10}
        else:
            lab.W.res = {"ok": False, "errors": []}
            lab.W.req = req["id"]
            try:
                if req["kind"] == "clip":
                    res = render_clip(lab, req)
                else:
                    a = _lab_args(req)
                    if not a["aroll_tl"]:
                        a["aroll_tl"] = lab.AROLL_TL
                    res = lab.render(a)
                    res["files"] = res.get("jpgs", []) + res.get("jpgs_deliver", [])
                    res["frames_rendered"] = len(a["frames"]) * (2 if a["via"] == "both" else 1)
            except Exception as e:
                res = lab.W.res
                res["errors"].append(repr(e)[:300]); res["ok"] = False
        res.update({"id": req["id"], "owner": req.get("owner"), "kind": req["kind"], "secs": round(time.time() - t0, 1),
                    "tries": req.get("tries", 0) + 1, "finished": time.strftime("%Y-%m-%d %H:%M:%S")})
        _wjson(os.path.join(Q["done"], req["id"] + ".json"), res)
        try:
            os.remove(os.path.join(Q["running"], req["id"] + ".json"))
        except OSError:
            pass
    _wjson(Q["beat"], {"pid": os.getpid(), "req": None, "step": "idle", "t": time.time(), "budget": 9999})


# ------------------------------------------------------------------------------------------------------ supervisor
def _resolve_state():
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Resolve.exe", "/FO", "CSV", "/NH"], capture_output=True,
                             text=True, timeout=20).stdout
        rows = [r for r in csv.reader(out.splitlines()) if r and r[0] == "Resolve.exe"]
        if not rows:
            return "not running", 0.0
        kb = int(re.sub(r"\D", "", rows[0][4]) or 0)
        nr = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Resolve.exe", "/FI", "STATUS eq NOT RESPONDING", "/FO",
                             "CSV", "/NH"], capture_output=True, text=True, timeout=20).stdout
        return ("not responding" if "Resolve.exe" in nr else "running"), kb / 1048576.0
    except Exception:
        return "unknown", 0.0


def restart(Q, kits, project, force, why):
    log(Q, "RESTART Resolve (%s)%s" % (why, " --force" if force else ""))
    subprocess.run([sys.executable, RESTART] + (["--force"] if force else []), timeout=600)
    if project:
        r = subprocess.run([sys.executable, os.path.join(kits, "open_job.py"), "--name", project, "--wait", "300"],
                           capture_output=True, text=True, timeout=420)
        log(Q, "open_job:", (r.stdout or r.stderr).strip()[-160:])


def run(argv):
    kits = kits_dir(argv)
    Q = qdirs(kits)
    opt = lambda k, d: type(d)(argv[argv.index(k) + 1]) if k in argv else d
    project, batch_n = opt("--project", ""), opt("--batch", 6)
    budget_f, mem_gb, idle_exit = opt("--frame-budget", 2010), opt("--mem-gb", 16.0), opt("--idle-exit", 0)
    fake = "--fake" in argv
    sys.path.insert(0, kits)
    import lab
    stop = threading.Event()

    def heartbeat():
        while not stop.is_set():
            _wjson(Q["alive"], {"pid": os.getpid(), "t": time.time(), "kits": kits})
            stop.wait(5)

    threading.Thread(target=heartbeat, daemon=True).start()
    log(Q, "render queue up: kits %s, batch %d, frame budget %d, mem %g GB%s" % (kits, batch_n, budget_f, mem_gb,
                                                                                 " (FAKE)" if fake else ""))
    for f in glob.glob(os.path.join(Q["running"], "*.json")):         # left by a killed queue: back in line
        os.replace(f, os.path.join(Q["requests"], os.path.basename(f)))
    frames_since, idle_since = 0, time.time()
    try:
        while True:
            reqs = []
            for f in glob.glob(os.path.join(Q["requests"], "*.json")):
                r = _rjson(f)
                if r is None:
                    continue                                       # still being written
                reqs.append((r.get("priority", 0), os.path.getmtime(f), f, r))
            if not reqs:
                if idle_exit and time.time() - idle_since > idle_exit:
                    log(Q, "idle %d s: exit" % idle_exit); break
                time.sleep(2); continue
            reqs.sort(key=lambda x: (x[0], x[1]))
            batch = [r for _, _, _, r in reqs[:batch_n]]
            for _, _, f, r in reqs[:batch_n]:
                os.replace(f, os.path.join(Q["running"], os.path.basename(f)))
            if not fake:
                st, gb = _resolve_state()
                if st != "running":
                    restart(Q, kits, project, False, "state " + st)
                try:                                               # an install run (kit-pipe) may hold Resolve
                    lab.acquire(OWNER, pid=os.getpid(), wait=3600)
                except TimeoutError as e:
                    log(Q, "lock busy, batch back in line:", e)
                    for r in batch:
                        os.replace(os.path.join(Q["running"], r["id"] + ".json"),
                                   os.path.join(Q["requests"], r["id"] + ".json"))
                    continue
            bp = os.path.join(Q["batches"], "batch_%d.json" % int(time.time() * 1000))
            _wjson(bp, {"reqs": batch})
            log(Q, "batch of %d: %s" % (len(batch), ", ".join(r["id"] for r in batch)))
            _wjson(Q["beat"], {"pid": 0, "req": None, "step": "start", "t": time.time(), "budget": 120})
            proc = subprocess.Popen([sys.executable, os.path.abspath(__file__), "--worker", bp, "--kits", kits] +
                                    (["--fake"] if fake else []))
            hung = None
            while proc.poll() is None:
                time.sleep(2)
                b = _rjson(Q["beat"], {}) or {}
                if b.get("t") and time.time() - b["t"] > float(b.get("budget", 60)) + 20:
                    hung = b; break
            if hung:
                proc.kill(); proc.wait()
                log(Q, "HANG in %s at '%s' (> %s s)" % (hung.get("req"), hung.get("step"), hung.get("budget")))
                if not fake:
                    st, gb = _resolve_state()
                    restart(Q, kits, project, st == "running", "hang at " + str(hung.get("step")))
                    frames_since = 0
            if not fake:
                try:
                    lab.release(OWNER)
                except Exception:
                    pass
            for r in batch:
                done = _rjson(os.path.join(Q["done"], r["id"] + ".json"))
                run_f = os.path.join(Q["running"], r["id"] + ".json")
                if done is not None:
                    frames_since += int(done.get("frames_rendered", 0) or 0)
                    log(Q, "done %s ok=%s %ss %s" % (r["id"], done.get("ok"), done.get("secs"),
                                                     "; ".join(done.get("errors", []))[:160]))
                    continue
                r["tries"] = r.get("tries", 0) + 1
                if r["tries"] >= MAX_TRIES:
                    _wjson(os.path.join(Q["done"], r["id"] + ".json"),
                           {"id": r["id"], "ok": False, "files": [], "tries": r["tries"], "owner": r.get("owner"),
                            "errors": ["resolve hung or crashed on this request %d times: look at the comp" %
                                       r["tries"]]})
                    log(Q, "FAILED %s after %d tries" % (r["id"], r["tries"]))
                    if os.path.exists(run_f):
                        os.remove(run_f)
                else:
                    _wjson(os.path.join(Q["requests"], r["id"] + ".json"), r)
                    if os.path.exists(run_f):
                        os.remove(run_f)
            if not fake:
                st, gb = _resolve_state()
                if frames_since >= budget_f or gb > mem_gb:
                    restart(Q, kits, project, True, "%d f since restart, %.1f GB" % (frames_since, gb))
                    frames_since = 0
            idle_since = time.time()
    finally:
        stop.set()
        try:
            os.remove(Q["alive"])
        except OSError:
            pass


def status(Q):
    n = {k: len(glob.glob(os.path.join(Q[k], "*.json"))) for k in ("requests", "running", "done")}
    b = _rjson(Q["beat"], {}) or {}
    st, gb = _resolve_state()
    print(json.dumps({"alive": alive(Q), "queue": n, "worker": {k: b.get(k) for k in ("req", "step")},
                      "resolve": st, "resolve_gb": round(gb, 1)}))


def main(argv):
    if "--worker" in argv:
        worker(argv[argv.index("--worker") + 1], kits_dir(argv), "--fake" in argv); return 0
    cmd = argv[0] if argv else "help"
    if cmd == "run":
        run(argv[1:]); return 0
    if cmd in ("submit", "status", "wait", "clip"):
        Q = qdirs(kits_dir(argv))
        if cmd == "status":
            status(Q); return 0
        if cmd == "submit":
            p = [x for x in argv[1:] if x.lower().endswith(".json")][0]
            i, d = submit(Q, _rjson(p))
            print(json.dumps({"id": i, "done": d, "queue_alive": alive(Q)})); return 0
        if cmd == "clip":
            g = lambda k, d=None: argv[argv.index(k) + 1] if k in argv else d
            res = [int(v) for v in g("--res", "960x540").split("x")]
            req = {"kind": "clip", "manifest": os.path.abspath(g("--manifest")), "out": os.path.abspath(g("--out")),
                   "name": g("--name") or os.path.basename(os.path.dirname(os.path.abspath(g("--manifest")))),
                   "pad": int(g("--pad", 12)), "res": res, "audio": "--no-audio" not in argv, "owner": g("--owner", "")}
            i, d = submit(Q, req)
            print(json.dumps({"id": i, "done": d, "queue_alive": alive(Q)})); return 0
        if cmd == "wait":
            w = int(argv[argv.index("--wait") + 1]) if "--wait" in argv else 1800
            ids = [x for x in argv[1:] if not x.startswith("--") and x != argv[argv.index("--kits") + 1]
                   and not (("--wait" in argv) and x == argv[argv.index("--wait") + 1])]
            got = wait_done(Q, ids, w)
            for i in ids:
                print(json.dumps(got.get(i, {"id": i, "ok": False, "errors": ["not done after %d s" % w]})))
            return 0 if all(got.get(i, {}).get("ok") for i in ids) else 1
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
