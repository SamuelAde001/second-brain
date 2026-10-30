# Speech vs bed levels (p5..p90, per-minute bed p10 / speech p80) of lav recordings and delivered mixes; writes speech_levels.json.
# Usage: python speech_levels.py --sources sources.json --out <folder>   (or --src NAME=PATH, repeatable)
# Promoted from video 4 on 2026-10-30.
"""Speech vs bed levels (editor-builder, 2026-10-28): raw lav level (speech frames) and delivered mixes of any videos
(p10 = bed in pauses, p80 = speech), 100 ms RMS frames. Writes speech_levels.json to --out."""
import argparse, subprocess, numpy as np, json, os, glob
ap = argparse.ArgumentParser(description="Speech vs bed levels of lav recordings and delivered mixes (100 ms RMS frames).")
ap.add_argument("--sources", help='json {name: wav path or glob}; a glob uses its first match, no match = skipped')
ap.add_argument("--src", action="append", default=[], metavar="NAME=PATH", help="one source (repeatable); a name starting with 'mix' also prints the per-minute list")
ap.add_argument("--out", required=True, help="folder for speech_levels.json")
_a = ap.parse_args()
_raw = json.load(open(_a.sources, encoding="utf-8")) if _a.sources else {}
_raw.update(dict(s.split("=", 1) for s in _a.src))
if not _raw:
    ap.error("give --sources or at least one --src")
SRC = {}
for k, pat in _raw.items():
    if any(c in pat for c in "*?["):
        g = sorted(glob.glob(pat))
        if g:
            SRC[k] = g[0]
    else:
        SRC[k] = pat
SR = 8000
res = {}
for k, p in SRC.items():
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True).stdout, dtype=np.float32)
    hop = SR // 10; n = len(x) // hop
    db = 10 * np.log10((x[:n * hop].reshape(n, hop).astype(np.float64) ** 2).mean(1) + 1e-12)
    q = {f"p{v}": round(float(np.percentile(db, v)), 1) for v in (5, 10, 20, 50, 80, 90)}
    # per-minute bed (p10) and speech (p80)
    per = []
    for m in range(0, n, 600):
        s = db[m:m + 600]
        if len(s) > 100: per.append((round(float(np.percentile(s, 10)), 1), round(float(np.percentile(s, 80)), 1)))
    res[k] = {"file": os.path.basename(p), "dur_s": round(len(x) / SR, 1), **q, "per_min_p10_p80": per}
    print(k, os.path.basename(p), res[k]["dur_s"], q)
    if k.startswith("mix"): print("   per min (bed p10, speech p80):", per)
os.makedirs(_a.out, exist_ok=True)
json.dump(res, open(os.path.join(_a.out, "speech_levels.json"), "w"), indent=1)
