# Install the visuals onto a new timeline with crash retries: install_v2x build, and after a Resolve crash restart Resolve, reopen the project and re-run (install_v2x keeps finished stages, so a re-run continues where it stopped).
# usage: python install_loop.py --job <job folder> --timeline "<new timeline>" --src-timeline "<cut timeline>" --list <list.txt> [--mz <mz.json>] [--project "<project name start>"] [--tries 4] [--kits <kits dir>] [--out <log dir>]    (run with the render queue STOPPED: one Resolve driver only)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
# Exit 0 = installed, 2 = verify failed (not a crash: stop for the Editor), 1 = failed after --tries.
import argparse, os, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
RESTART = os.path.normpath(os.path.join(HERE, "..", "..", "restart_resolve.py"))   # scripts\restart_resolve.py

ap = argparse.ArgumentParser(description="install_v2x build with Resolve-crash retries.")
ap.add_argument("--job", help="job folder (gives the default --kits and --out)")
ap.add_argument("--kits", help="kits dir (default <job>\\Graphics\\Frontal kit (Editor)\\kits)")
ap.add_argument("--timeline", required=True, help="timeline to build (video 4: Visuals v1 (Editor))")
ap.add_argument("--src-timeline", required=True, help="timeline to build from (video 4: Cut v5 (Editor) - sections)")
ap.add_argument("--list", required=True, help="manifest list file (list.txt) for install_v2x")
ap.add_argument("--mz", help="MagicZoom plan json (mz.json) for install_v2x --mz")
ap.add_argument("--project", help="project name start for open_job.py --name after a restart (default: the kit's own default)")
ap.add_argument("--tries", type=int, default=4)
ap.add_argument("--out", help="folder for install_final.log (default <job>\\Docs\\finish)")
args = ap.parse_args()
if not (args.job or args.kits):
    ap.error("give --job or --kits")
if not (args.job or args.out):
    ap.error("give --job or --out")
K = os.path.abspath(args.kits or os.path.join(args.job, "Graphics", "Frontal kit (Editor)", "kits"))   # the kits dir
KIT = os.path.dirname(K)                                                                                # the kit root (cwd of the installs)
OUT = os.path.abspath(args.out or os.path.join(args.job, "Docs", "finish"))
os.makedirs(OUT, exist_ok=True)
TRIES = args.tries
LOG = os.path.join(OUT, "install_final.log")
say = lambda *a: (print(time.strftime("%H:%M:%S"), *a, flush=True),
                  open(LOG, "a", encoding="utf-8").write(time.strftime("%H:%M:%S ") + " ".join(map(str, a)) + "\n"))
cmd = [sys.executable, "-X", "utf8", os.path.join(K, "install_v2x.py"), "build", args.timeline,
       os.path.abspath(args.list)] + (["--mz", os.path.abspath(args.mz)] if args.mz else []) + \
      ["--from", args.src_timeline, "--replace"]
OPEN = [sys.executable, "-X", "utf8", os.path.join(K, "open_job.py"), "--wait", "380"] + (["--name", args.project] if args.project else [])
for n in range(1, TRIES + 1):
    say("try", n, "install_v2x build")
    with open(LOG, "a", encoding="utf-8") as fh:
        rc = subprocess.run(cmd, cwd=KIT, stdout=fh, stderr=subprocess.STDOUT).returncode
    say("try", n, "exit", rc)
    if rc == 0:
        say("INSTALL OK"); sys.exit(0)
    if rc == 2:
        say("verify failed (exit 2): not a crash, stop for the Editor"); sys.exit(2)
    say("restarting Resolve")
    subprocess.run([sys.executable, "-X", "utf8", RESTART, "--force"], cwd=KIT)
    r = subprocess.run(OPEN, cwd=KIT, capture_output=True, text=True)
    say("open_job:", (r.stdout or r.stderr).strip()[-200:])
say("INSTALL FAILED after", TRIES, "tries"); sys.exit(1)
