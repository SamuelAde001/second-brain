"""Extract lip-synced A-roll frames for beats that put the A-roll inside a graphic.
map.json: beat -> [[tl_start, tl_end, leftOffset_tl_frames], ...] from V1 of Visuals v1 (Editor)."""
import os, sys, json, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beats as BT
FF = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe"))[0]
SRC = os.path.join(HERE, "..", "..", "Client raws", "C0786.MP4")
FPS = 24000 / 1001
M = json.load(open(os.path.join(HERE, "_assets", "aroll", "map.json")))
for bid in (sys.argv[1:] or M.keys()):
    b = [x for x in BT.B if x["id"] == bid][0]
    out = os.path.join(HERE, "_assets", "aroll", bid)
    os.makedirs(out, exist_ok=True)
    for st, en, lo in M[bid]:
        a, z = max(st, b["start"]), min(en, b["end"])
        if z <= a: continue
        src_sec = (lo + (a - st)) / FPS
        subprocess.run([FF, "-v", "error", "-y", "-hwaccel", "cuda", "-ss", "%.4f" % src_sec, "-i", SRC,
                        "-vf", "fps=24000/1001,scale=1280:-2", "-frames:v", str(z - a), "-q:v", "3",
                        "-start_number", str(a - b["start"]), os.path.join(out, "f%05d.jpg")], check=True)
    print(bid, len(os.listdir(out)), "frames")
