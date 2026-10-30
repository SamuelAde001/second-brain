# Install changed beats onto a copy of Samuel's edited timeline (his is never touched): install_v2x duplicates it to "zz <new> work (Editor)", replaces only the listed beats' clips there, and imports the result as the new timeline; "seed" first copies the base install records so install_v1 removes exactly the old clips.
# usage: python install_changed.py seed|build --beats A,B,C --job <job folder> --timeline "<new timeline>" --src-timeline "<base timeline>" --snapshot <base tl_snapshot.json> [--ver v3] [--tries 3] [--replace] [--kits <kits dir>] [--out <log dir>]
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
# seed: before the build, read-only on Resolve (uses the --snapshot of the base timeline as Samuel left it). build: install_v2x with crash retries (restart Resolve, reopen project); --replace rebuilds my own new timeline (old one renamed zz ... old), never his.
import argparse, json, os, re, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
RESTART = os.path.normpath(os.path.join(HERE, "..", "..", "restart_resolve.py"))   # scripts\restart_resolve.py

ap = argparse.ArgumentParser(description="Seed records and build changed beats onto a copy of the base timeline.")
ap.add_argument("cmd", choices=["seed", "build"])
ap.add_argument("--beats", required=True, help="comma list of changed beat folders (video 4: IN-07,WN-08,...)")
ap.add_argument("--job", help="job folder (gives the default --kits and --out)")
ap.add_argument("--kits", help="kits dir (default <job>\\Graphics\\Frontal kit (Editor)\\kits)")
ap.add_argument("--timeline", required=True, help="new timeline to build (video 4: Visuals v3 (Editor))")
ap.add_argument("--src-timeline", required=True, help="base timeline Samuel edited (video 4: Visuals v1 (Editor))")
ap.add_argument("--snapshot", help="tl_snapshot.json of the base timeline after Samuel's edits (needed for seed)")
ap.add_argument("--comps", help="comps dir holding <beat>\\manifest.json (default <kit>\\comps\\v1)")
ap.add_argument("--ver", default="changed", help="tag for the log and list file names: install_<ver>.log, list_<ver>.txt")
ap.add_argument("--project", help="project name start for open_job.py --name after a restart (default: the kit's own default)")
ap.add_argument("--tries", type=int, default=3)
ap.add_argument("--replace", action="store_true", help="the new timeline exists: rebuild it (the old one is renamed zz ... old)")
ap.add_argument("--out", help="folder for the log and list file (default <job>\\Docs\\finish)")
args = ap.parse_args()
if not (args.job or args.kits):
    ap.error("give --job or --kits")
if not (args.job or args.out):
    ap.error("give --job or --out")
if args.cmd == "seed" and not args.snapshot:
    ap.error("seed needs --snapshot")
K = os.path.abspath(args.kits or os.path.join(args.job, "Graphics", "Frontal kit (Editor)", "kits"))   # the kits dir
KIT = os.path.dirname(K)                                                                                # the kit root
OUTD = os.path.abspath(args.out or os.path.join(args.job, "Docs", "finish"))
os.makedirs(OUTD, exist_ok=True)
slug = lambda name: re.sub(r"[^\w]+", "_", name).strip("_")                    # = install_v2x's record folder name
INST = os.path.join(KIT, "renders", "v2", "INST")
OLD = os.path.join(INST, slug(args.src_timeline))
NEW = os.path.join(INST, slug(args.timeline))
COMPS = os.path.abspath(args.comps or os.path.join(KIT, "comps", "v1"))
LOG = os.path.join(OUTD, "install_%s.log" % args.ver)
say = lambda *a: (print(time.strftime("%H:%M:%S"), *a, flush=True),
                  open(LOG, "a", encoding="utf-8").write(time.strftime("%H:%M:%S ") + " ".join(map(str, a)) + "\n"))
cmd, beats = args.cmd, args.beats.split(",")
os.makedirs(NEW, exist_ok=True)
if cmd == "seed":
    snap = json.load(open(args.snapshot, encoding="utf-8"))
    for b in beats:
        rec = json.load(open(os.path.join(OLD, "installed_%s.json" % b), encoding="utf-8"))
        out = {"manifest": rec["manifest"], "items": {}}
        for k, it in rec["items"].items():
            hit = [x for x in snap["tracks"].get("V%d" % it["track"], []) if x["s"] == it["start"] and x["e"] == it["end"]]
            if not hit:
                say("seed", b, k, "V%d %d-%d not on Samuel's timeline: left out (he changed it)" % (it["track"], it["start"], it["end"]))
                continue
            out["items"][k] = dict(it, name=hit[0]["name"])
        json.dump(out, open(os.path.join(NEW, "installed_%s.json" % b), "w", encoding="utf-8"), indent=1)
        say("seed", b, len(out["items"]), "of", len(rec["items"]), "items", sorted({v["name"][:24] for v in out["items"].values()}))
    sys.exit(0)
lst = os.path.join(OUTD, "list_%s.txt" % args.ver)
open(lst, "w", encoding="utf-8").write("".join(os.path.join(COMPS, b, "manifest.json") + "\n" for b in beats))
TRIES = args.tries
run = [sys.executable, "-X", "utf8", os.path.join(K, "install_v2x.py"), "build", args.timeline, lst,
       "--from", args.src_timeline] + (["--replace"] if args.replace else [])   # --replace: rebuild my own new timeline, never his
OPEN = [sys.executable, "-X", "utf8", os.path.join(K, "open_job.py"), "--wait", "380"] + (["--name", args.project] if args.project else [])
V = args.ver.upper()
for n in range(1, TRIES + 1):
    say("try", n, "install_v2x build %s:" % args.ver, ",".join(beats))
    with open(LOG, "a", encoding="utf-8") as fh:
        rc = subprocess.run(run, cwd=KIT, stdout=fh, stderr=subprocess.STDOUT).returncode
    say("try", n, "exit", rc)
    if rc == 0:
        say("INSTALL %s OK" % V); sys.exit(0)
    if rc == 2:
        say("verify failed (exit 2): stop for the Editor"); sys.exit(2)
    say("restarting Resolve")
    subprocess.run([sys.executable, "-X", "utf8", RESTART, "--force"], cwd=KIT)
    r = subprocess.run(OPEN, cwd=KIT, capture_output=True, text=True)
    say("open_job:", (r.stdout or r.stderr).strip()[-200:])
say("INSTALL %s FAILED after" % V, TRIES, "tries"); sys.exit(1)
