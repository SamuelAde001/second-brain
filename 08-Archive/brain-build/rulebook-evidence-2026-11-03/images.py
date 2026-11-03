"""Copy the pictures the drafters picked into _attachments/rulebook as small JPGs (max 960 px wide)."""
import glob, os, subprocess
here = os.path.dirname(os.path.abspath(__file__))
dst = r"C:/Users/repzy/Desktop/My Second brain/_attachments/rulebook"
os.makedirs(dst, exist_ok=True)
ok = miss = 0
for f in sorted(glob.glob(os.path.join(here, "img_*.txt"))):
    for line in open(f, encoding="utf-8"):
        if "->" not in line:
            continue
        src, name = [s.strip().strip('"') for s in line.rsplit("->", 1)]
        name = os.path.basename(name)
        if not name.lower().endswith(".jpg"):
            name = os.path.splitext(name)[0] + ".jpg"
        out = os.path.join(dst, name)
        if not os.path.exists(src):
            print("MISSING", src); miss += 1; continue
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                            "-vf", "scale='min(960,iw)':-2", "-q:v", "4", out])
        if r.returncode == 0:
            ok += 1
        else:
            print("FAIL", src); miss += 1
print("copied", ok, "missing/failed", miss)
