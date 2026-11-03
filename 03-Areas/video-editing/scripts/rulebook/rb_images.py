"""Copy the rulebook's reference pictures into _attachments/rulebook as small JPGs (max 960 px wide).

Reads every img_*.txt manifest in --work, one line per picture: "<full source path> -> <target name>.jpg".
Source files (job stills, style frames, contact sheets) are only read, never changed. Needs ffmpeg on PATH.

Usage: python rb_images.py --work <folder with img_*.txt>
"""
import argparse, glob, os, subprocess

DST = r"C:/Users/repzy/Desktop/My Second brain/_attachments/rulebook"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    os.makedirs(DST, exist_ok=True)
    ok = miss = 0
    for f in sorted(glob.glob(os.path.join(a.work, "img_*.txt"))):
        for line in open(f, encoding="utf-8"):
            if "->" not in line:
                continue
            src, name = [s.strip().strip('"') for s in line.rsplit("->", 1)]
            name = os.path.splitext(os.path.basename(name))[0] + ".jpg"
            if not os.path.exists(src):
                print("MISSING", src)
                miss += 1
                continue
            r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                                "-vf", "scale='min(960,iw)':-2", "-q:v", "4", os.path.join(DST, name)])
            ok += r.returncode == 0
            miss += r.returncode != 0
    print("copied", ok, "missing/failed", miss)


if __name__ == "__main__":
    main()
