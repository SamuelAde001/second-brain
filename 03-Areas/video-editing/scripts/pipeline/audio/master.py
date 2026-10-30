# Masters a render to -16 LUFS / under -1 dBTP (linear gain + oversampled limiter, delay removed, video copied) and checks sync (DECISIONS #59).
# Usage: python master.py <in.mp4> <out.mp4>   (needs loudness.py beside it)
# Promoted from video 4 on 2026-10-30.
# Master a render to -16 LUFS / under -1 dBTP (Editor, 2026-10-29, DECISIONS #59): linear gain to the target, a 4x-oversampled
# limiter at -1.5 dBFS for the few transients the gain pushes over, its 24-sample delay removed, video stream copied.
#   -> prints in/out loudness and the sync check (cross-correlation at 3 points); exit 1 if the check fails
import argparse, subprocess, sys
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from loudness import measure

ap = argparse.ArgumentParser(description="Master a render to -16 LUFS / under -1 dBTP: linear gain, 4x-oversampled limiter at -1.5 dBFS, delay removed, video copied; checks sync.")
ap.add_argument("input", help="render to master (mp4)")
ap.add_argument("output", help="mastered mp4 to write")
_a = ap.parse_args()
SRC, OUT = _a.input, _a.output


def build(gain):
    af = ("aresample=192000,volume=%.2fdB,alimiter=limit=0.84:attack=0.5:release=40:asc=1:level=false,aresample=48000,"
          "atrim=start_sample=24,asetpts=PTS-STARTPTS,apad=pad_len=24" % gain)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", af,
                    "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", OUT], check=True)
    return measure(OUT)


def pcm(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vn", "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


m = measure(SRC)
print("in : %s LUFS, true peak %s dBTP" % (m["input_i"], m["input_tp"]))
gain = -16.0 - float(m["input_i"])
n = build(gain)
if abs(float(n["input_i"]) + 16.0) > 0.15:                  # the limiter takes a little loudness: correct once
    gain += -16.0 - float(n["input_i"]); n = build(gain)
print("out: %s LUFS, true peak %s dBTP, LRA %s LU (gain %+.2f dB)" % (n["input_i"], n["input_tp"], n["input_lra"], gain))
a, b = pcm(SRC), pcm(OUT)
offs = []
for t in (5, len(a) // 96000, len(a) // 48000 - 10):
    s = int(t * 48000); x = a[s:s + 48000]
    offs.append(max(range(-200, 201), key=lambda d: float(np.dot(x, b[s + d:s + d + 48000]))))
print("samples", len(a), len(b), "| sync offsets", offs)
ok = len(a) == len(b) and offs == [0, 0, 0] and float(n["input_tp"]) <= -1.0 and abs(float(n["input_i"]) + 16.0) <= 0.15
print("MASTER OK" if ok else "MASTER CHECK FAILED")
sys.exit(0 if ok else 1)
