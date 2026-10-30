# A1 Voice Isolation check: read the cut timeline and the visuals timeline; with --keep, make the visuals timeline's A1 match the cut's when a reinstall's new timeline came in without it.
# usage: python a1_voice.py --timeline "<visuals timeline>" --src-timeline "<cut timeline>" [--keep] [--job <job folder> | --kits <kits dir>]    exit 1 when --keep could not make them match (needs Resolve running)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
import argparse, os, sys
sys.dont_write_bytecode = True                           # never leave __pycache__ in the kits dir

ap = argparse.ArgumentParser(description="Compare (and with --keep, copy) A1 Voice Isolation state from the cut timeline to the visuals timeline.")
ap.add_argument("--timeline", required=True, help="target timeline whose A1 must match (video 4: env A1_TARGET)")
ap.add_argument("--src-timeline", required=True, help="cut timeline holding Samuel's own A1 voice isolation")
ap.add_argument("--keep", action="store_true", help="set the target's A1 state to the cut's when they differ")
ap.add_argument("--job", help="job folder (gives the default --kits)")
ap.add_argument("--kits", help="kits dir (default <job>\\Graphics\\Frontal kit (Editor)\\kits)")
args = ap.parse_args()
if not (args.job or args.kits):
    ap.error("give --job or --kits")
K = os.path.abspath(args.kits or os.path.join(args.job, "Graphics", "Frontal kit (Editor)", "kits"))
sys.path[:0] = [K, r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"]
import lab
import DaVinciResolveScript as dvr
TARGET, SRC = args.timeline, args.src_timeline
lab.acquire("a1-voice", wait=1800)
rc = 0
try:
    r = dvr.scriptapp("Resolve"); p = r.GetProjectManager().GetCurrentProject()
    tls = {p.GetTimelineByIndex(i).GetName(): p.GetTimelineByIndex(i) for i in range(1, p.GetTimelineCount() + 1)}
    for name in (SRC, TARGET):
        t = tls[name]
        items = t.GetItemListInTrack("audio", 1) or []
        print(name, "| A1 track state:", t.GetVoiceIsolationState(1), "| audio tracks", t.GetTrackCount("audio"),
              "| A1 items", len(items), "| first items' state", [it.GetVoiceIsolationState() for it in items[:3]])
    want, have = tls[SRC].GetVoiceIsolationState(1), tls[TARGET].GetVoiceIsolationState(1)
    if args.keep and want != have:
        ok = tls[TARGET].SetVoiceIsolationState(1, want)
        have = tls[TARGET].GetVoiceIsolationState(1)
        print("set", TARGET, "A1 ->", ok, have, "| saved", r.GetProjectManager().SaveProject())
    if args.keep and want != have:
        rc = 1
    print("A1 match:", want == have, want)
finally:
    lab.release("a1-voice")
sys.exit(rc)
