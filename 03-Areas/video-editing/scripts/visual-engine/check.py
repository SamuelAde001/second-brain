"""Tile stills into a check sheet. Overlay PNGs are composited on an A-roll frame.
python check.py out.jpg B02 B03 ...   (ids)"""
import os, sys, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
FF = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe"))[0]
AROLL = os.path.join(HERE, "_assets", "aroll_ref_0330.jpg")
out, ids = sys.argv[1], sys.argv[2:]
files = []
for i in ids:
    f = sorted(glob.glob(os.path.join(HERE, "stills", i + "_*")))
    if f: files.append(f[0])
cols = 3
tw, th = 640, 360
inputs, fl = [], []
k = 0
for n, f in enumerate(files):
    if f.endswith(".png"):
        inputs += ["-i", AROLL, "-i", f]
        fl.append(f"[{k}]scale={tw}:{th}[a{n}];[{k+1}]scale={tw}:{th}[b{n}];[a{n}][b{n}]overlay[t{n}]")
        k += 2
    else:
        inputs += ["-i", f]
        fl.append(f"[{k}]scale={tw}:{th}[t{n}]")
        k += 1
    fl[-1] += f";[t{n}]drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{ids[n]}':x=8:y=8:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.6[u{n}]"
N = len(files)
rows = (N + cols - 1) // cols
while N < rows * cols:  # pad
    inputs += ["-f", "lavfi", "-i", f"color=c=black:s={tw}x{th}"]
    fl.append(f"[{k}]null[u{N}]"); k += 1; N += 1
layout = "|".join(f"{(i % cols) * tw}_{(i // cols) * th}" for i in range(N))
fl.append("".join(f"[u{i}]" for i in range(N)) + f"xstack=inputs={N}:layout={layout}")
subprocess.run([FF, "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(fl), "-frames:v", "1", "-q:v", "3", out], check=True)
print(out)
