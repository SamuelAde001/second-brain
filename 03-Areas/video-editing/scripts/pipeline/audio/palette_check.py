# Checks every SFX palette file exists and decodes; reports duration, sample peak and the loudest 100 ms; writes palette_check.json.
# Usage: python palette_check.py --palette palette.json --sfx-dir <library> --assets-sfx-dir <job SFX> --out <folder>
# Promoted from video 4 on 2026-10-30.
"""Checks the SFX palette files exist and decode (duration, peak, RMS of the loudest 100 ms), read-only. Writes palette_check.json to --out."""
import argparse, os, json, subprocess, numpy as np
ap = argparse.ArgumentParser(description="Check the SFX palette files exist and decode; report duration, peak and loudest 100 ms.")
ap.add_argument("--palette", required=True, help='json {name: "sfx:<file under --sfx-dir>" | "assets:<file under --assets-sfx-dir>" | absolute path}')
ap.add_argument("--sfx-dir", required=True, help="the SFX library folder (the 'sfx:' root)")
ap.add_argument("--assets-sfx-dir", required=True, help="the job-assets SFX folder (the 'assets:' root)")
ap.add_argument("--out", required=True, help="folder for palette_check.json")
_a = ap.parse_args()
HERE = _a.out
os.makedirs(HERE, exist_ok=True)
L = _a.sfx_dir.rstrip("/\\")
VS = _a.assets_sfx_dir.rstrip("/\\")
_roots = {"sfx:": L, "assets:": VS}


def _res(v):
    for k, r in _roots.items():
        if v.startswith(k):
            return r + "/" + v[len(k):]
    return v


P = {k: _res(v) for k, v in json.load(open(_a.palette, encoding="utf-8")).items()}
out = {}
for k, p in P.items():
    if not os.path.exists(p):
        out[k] = {"path": p, "exists": False}; print("MISSING", k, p); continue
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vn", "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                                     capture_output=True).stdout, dtype=np.float32)
    hop = 4800; n = max(1, len(x) // hop)
    db = 10 * np.log10((x[:n * hop].reshape(n, hop).astype(float) ** 2).mean(1) + 1e-12) if len(x) >= hop else [-99]
    out[k] = {"path": p, "exists": True, "dur_s": round(len(x) / 48000, 3), "peak_dBFS": round(float(20 * np.log10(np.abs(x).max() + 1e-12)), 1),
              "max100ms_dB": round(float(np.max(db)), 1)}
    print(k, out[k]["dur_s"], "s peak", out[k]["peak_dBFS"], "max100ms", out[k]["max100ms_dB"])
json.dump(out, open(os.path.join(HERE, "palette_check.json"), "w", encoding="utf-8"), indent=1)
