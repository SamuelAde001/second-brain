# Scans every song in the music libraries for duration, loudness (p90) and breakdowns / near-silent stretches; writes music_scan.json.
# Usage: python music_scan.py --music-dir <library> [<library> ...] --out <folder>
# Promoted from video 4 on 2026-10-30.
"""Music scan (editor-builder, 2026-10-28). Lists every song in the music libraries with its duration and
scans it in 1 s windows (power average of 100 ms RMS frames, mono 8 kHz decode) for breakdowns / near-silent stretches.
Output: music_scan.json in --out. Read-only on the libraries."""
import argparse, os, json, subprocess, sys
import numpy as np
ap = argparse.ArgumentParser(description="Scan every song in the music libraries: duration, p90 level, body span, per-0.1 s level curve.")
ap.add_argument("--music-dir", nargs="+", required=True, help="one or more music library folders (searched recursively)")
ap.add_argument("--out", required=True, help="folder for music_scan.json")
_a = ap.parse_args()
ROOTS = _a.music_dir
HERE = _a.out
os.makedirs(HERE, exist_ok=True)
EXT = {'.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg', '.aif', '.aiff'}
SR = 8000
def decode(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32)
def levels(x):
    hop = SR // 10
    n = len(x) // hop
    fr = x[:n * hop].reshape(n, hop)
    pw = (fr.astype(np.float64) ** 2).mean(1) + 1e-12          # 100 ms power
    k = 10
    cs = np.concatenate([[0], np.cumsum(pw)])
    w = np.array([(cs[min(n, i + k)] - cs[i]) / max(1, min(n, i + k) - i) for i in range(n)])  # 1 s forward power avg
    return 10 * np.log10(w)    # dB per 0.1 s step, window [t, t+1 s)
files = []
for r in ROOTS:
    for dp, dn, fn in os.walk(r):
        for f in sorted(fn):
            if os.path.splitext(f)[1].lower() in EXT:
                files.append(os.path.join(dp, f).replace(os.sep, '/'))
out = {}
for p in files:
    x = decode(p)
    if len(x) < SR * 5:
        out[p] = {"dur": len(x) / SR, "err": "short/undecodable"}; continue
    L = levels(x)
    dur = len(x) / SR
    # body = from first window within 10 dB of p90 to last such window
    p90 = float(np.percentile(L, 90))
    on = np.where(L > p90 - 10)[0]
    a, b = int(on[0]), int(on[-1])
    out[p] = {"dur": round(dur, 2), "p90": round(p90, 2), "body": [round(a / 10, 1), round(b / 10 + 1, 1)],
              "L": [round(float(v), 1) for v in L]}
    print(f"{dur:7.1f}s  p90 {p90:6.1f}  {os.path.relpath(p, os.path.dirname(r)) if False else p.split('/')[-1]}", flush=True)
json.dump(out, open(os.path.join(HERE, "music_scan.json"), "w", encoding="utf-8"))
print(len(out), "files ->", os.path.join(HERE, "music_scan.json"))
