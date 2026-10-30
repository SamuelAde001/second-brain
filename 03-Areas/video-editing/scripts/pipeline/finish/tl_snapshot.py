# Snapshot of a timeline: markers + every item per track (start, end, name, source in), read-only. Take one before Samuel edits a timeline, so his edits and markers can be told apart afterwards (tl_diff.py).
# usage: python tl_snapshot.py <out.json> --timeline "<timeline name>" [--job <job folder> | --kits <kits dir>]    (needs Resolve running)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
import argparse, json, os, sys
sys.dont_write_bytecode = True                           # never leave __pycache__ in the kits dir

ap = argparse.ArgumentParser(description="Read-only snapshot of one Resolve timeline to JSON.")
ap.add_argument("out", help="snapshot json to write")
ap.add_argument("--timeline", required=True, help="timeline name to snapshot")
ap.add_argument("--job", help="job folder (gives the default --kits)")
ap.add_argument("--kits", help="kits dir (default <job>\\Graphics\\Frontal kit (Editor)\\kits)")
args = ap.parse_args()
if not (args.job or args.kits):
    ap.error("give --job or --kits")
K = os.path.abspath(args.kits or os.path.join(args.job, "Graphics", "Frontal kit (Editor)", "kits"))
sys.path[:0] = [K, r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"]
import lab
import DaVinciResolveScript as dvr
OUT = args.out; TL = args.timeline
lab.acquire("tl-snapshot", wait=120)
try:
    r = dvr.scriptapp("Resolve"); p = r.GetProjectManager().GetCurrentProject()
    t = next(p.GetTimelineByIndex(i) for i in range(1, p.GetTimelineCount() + 1) if p.GetTimelineByIndex(i).GetName() == TL)
    S0 = t.GetStartFrame()
    snap = {"timeline": TL, "start": S0, "end": t.GetEndFrame(), "markers": {str(k): v for k, v in (t.GetMarkers() or {}).items()}, "tracks": {}}
    for kind in ("video", "audio"):
        for n in range(1, t.GetTrackCount(kind) + 1):
            snap["tracks"]["%s%d" % (kind[0].upper(), n)] = [
                {"s": it.GetStart() - S0, "e": it.GetEnd() - S0, "name": it.GetName(), "in": it.GetLeftOffset()}
                for it in (t.GetItemListInTrack(kind, n) or [])]
    json.dump(snap, open(OUT, "w", encoding="utf-8"), indent=1)
    print(TL, "markers", len(snap["markers"]), "|", {k: len(v) for k, v in snap["tracks"].items()})
finally:
    lab.release("tl-snapshot")
