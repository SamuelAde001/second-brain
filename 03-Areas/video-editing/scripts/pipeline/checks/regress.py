# Regression scan between two renders: every frame of A against the same frame of B; changed spans marked expected/UNEXPECTED.
# Usage: python regress.py <a.mp4> <b.mp4> <beat,beat,...> --inst <folder with installed_*.json>
# Promoted from video 4 on 2026-10-30.
# Regression scan between two renders (Editor, 2026-10-29): every frame of A against the same frame of B at 320x180 grey.
# A frame that changed outside the beats a fix round touched is a regression.
#   -> prints changed spans, each marked "expected" (inside a changed beat) or "UNEXPECTED"
import argparse, glob, json, os, subprocess, sys
import numpy as np

ap = argparse.ArgumentParser(description="Regression scan between two renders: changed frame spans, each marked expected or UNEXPECTED.")
ap.add_argument("a", help="render A (mp4)")
ap.add_argument("b", help="render B (mp4)")
ap.add_argument("beats", help="comma list of the beats a fix round touched, e.g. HK-03d,IN-05")
ap.add_argument("--inst", required=True, help="folder holding installed_<beat>.json (the install record of the timeline both renders show)")
_a = ap.parse_args()
A, B, BEATS, INST = _a.a, _a.b, set(_a.beats.split(",")), _a.inst
W, H, TH = 320, 180, 1.5                                   # mean abs diff above 1.5 levels counts as changed


def frames(f):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-hwaccel", "cuda", "-i", f, "-vf", "scale=%d:%d" % (W, H), "-pix_fmt", "gray",
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H)
        if len(b) < W * H:
            break
        yield np.frombuffer(b, np.uint8).astype(np.int16)


spans = {}
for f in glob.glob(os.path.join(INST, "installed_*.json")):
    its = [v for v in json.load(open(f, encoding="utf-8")).get("items", {}).values() if "start" in v]
    if its:
        spans[os.path.basename(f)[10:-5]] = (min(v["start"] for v in its), max(v["end"] for v in its))
d = np.array([float(np.abs(x - y).mean()) for x, y in zip(frames(A), frames(B))])
print("frames compared", len(d), "| changed (MAD > %.1f):" % TH, int((d > TH).sum()))
ch = np.flatnonzero(d > TH)
runs = []
for i in ch:
    if runs and i - runs[-1][1] <= 2:
        runs[-1][1] = i
    else:
        runs.append([i, i])
bad = 0
for s, e in runs:
    who = sorted(b for b, (bs, be) in spans.items() if bs <= e and s < be)
    ok = any(b in BEATS for b in who)
    bad += not ok
    print("%5d-%5d  max %5.1f  %-9s %s" % (s, e, d[s:e + 1].max(), "expected" if ok else "UNEXPECTED", ",".join(who) or "A-roll"))
print("UNEXPECTED spans:", bad)
