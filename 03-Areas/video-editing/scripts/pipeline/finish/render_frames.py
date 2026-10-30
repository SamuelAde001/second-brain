# Frames from a final render for the Opus check: per installed beat frames at 12 %, 50 % and 88 % of its span, both sides of every chunk join, and A-roll frames every ~300 f where no beat is placed; plus labelled contact sheets.
# usage: python render_frames.py <render.mp4> <out dir> --timeline "<base timeline>" --len <timeline frames> [--job <job folder> | --kits <kits dir>] [--beats EN-04,HB-07] [--inst "<newer timeline>[,...]"] [--off 2020] [--chunk 2020]    (file only, no Resolve)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
# Per installed beat (<kit>\renders\v2\INST\<base timeline slug>\installed_<beat>.json). Writes <out>\f<frame>_<beat>.jpg (1920x1080), <out>\sheet_<section>.jpg (3 per row, labelled) and <out>\frames.json.
import argparse, glob, json, os, re, subprocess, sys
sys.dont_write_bytecode = True

ap = argparse.ArgumentParser(description="Review frames + contact sheets from a final render, per installed beat and chunk join.")
ap.add_argument("render", help="render .mp4 (or, with --off, a chunk starting at that timeline frame)")
ap.add_argument("out", help="output folder")
ap.add_argument("--job", help="job folder (gives the default --kits)")
ap.add_argument("--kits", help="kits dir (default <job>\\Graphics\\Frontal kit (Editor)\\kits)")
ap.add_argument("--timeline", required=True, help="base timeline whose install records list the beats (video 4: Visuals v1 (Editor))")
ap.add_argument("--inst", default="", help="comma list of newer timelines (or record folder names) whose records win (video 4: Visuals_v3_Editor; was env RF_INST)")
ap.add_argument("--off", type=int, default=0, help="the render is a chunk starting at this timeline frame (video 4: 2020; was env RF_OFF)")
ap.add_argument("--len", type=int, required=True, help="timeline length in frames")
ap.add_argument("--chunk", type=int, default=2020, help="render chunk size (chunk joins are checked on both sides; default 2020)")
ap.add_argument("--beats", help="only these beats (comma list); also skips the join and A-roll frames")
args = ap.parse_args()
if not (args.job or args.kits):
    ap.error("give --job or --kits")
from PIL import Image, ImageDraw   # after parse_args so --help works without Pillow
KITS = os.path.abspath(args.kits or os.path.join(args.job, "Graphics", "Frontal kit (Editor)", "kits"))
slug = lambda name: re.sub(r"[^\w]+", "_", name).strip("_")                    # = install_v2x's record folder name
INST = os.path.join(os.path.dirname(KITS), "renders", "v2", "INST", slug(args.timeline))
SRC, OUT = args.render, args.out
only = set(args.beats.split(",")) if args.beats else None
LEN, CH = args.len, args.chunk
os.makedirs(OUT, exist_ok=True)

spans = {}
INSTS = [os.path.join(os.path.dirname(INST), slug(x)) for x in args.inst.split(",") if x] + [INST]   # --inst: its records win
for f in [g for d in INSTS for g in sorted(glob.glob(os.path.join(d, "installed_*.json")))]:
    beat = os.path.basename(f)[10:-5]
    if beat in spans:
        continue
    its = [v for v in json.load(open(f, encoding="utf-8")).get("items", {}).values() if "start" in v]
    if its:
        spans[beat] = (min(v["start"] for v in its), max(v["end"] for v in its))
want = {}
for beat, (s, e) in sorted(spans.items(), key=lambda x: x[1]):
    if only and beat not in only:
        continue
    for p in (0.12, 0.5, 0.88):
        want.setdefault(min(e - 1, int(s + p * (e - s))), beat)
if not only:
    for j in range(CH, LEN, CH):
        want.setdefault(j - 1, "join"); want.setdefault(j, "join")
    covered = sorted(spans.values())
    for fr in range(150, LEN, 300):
        if not any(s <= fr < e for s, e in covered):
            want.setdefault(fr, "A-roll")
frames = sorted(want)
# ffmpeg 9 refuses one select() over ~330 eq() terms (exit -12), so: groups of 25, each an accurate seek to half a frame
# before its first frame (n = 0 is then exactly that frame), run 3 at a time
FPS = 24000 / 1001
OFF = args.off                                                  # --off 2020: SRC is a chunk starting at timeline frame 2020
groups = [frames[i:i + 25] for i in range(0, len(frames), 25)]
procs, rows = [], []
for gi, g in enumerate(groups):
    expr = "+".join("eq(n\\,%d)" % (f - g[0]) for f in g)
    cmd = ["ffmpeg", "-y", "-v", "error", "-hwaccel", "cuda", "-ss", "%.6f" % ((g[0] - OFF - 0.5) / FPS), "-i", SRC,
           "-vf", "select='%s',scale=1920:1080" % expr, "-fps_mode", "passthrough", "-q:v", "2",
           os.path.join(OUT, "_x%03d_%%05d.jpg" % gi)]
    procs.append(subprocess.Popen(cmd))
    if len(procs) >= 3:
        assert procs.pop(0).wait() == 0, "ffmpeg failed"
for p in procs:
    assert p.wait() == 0, "ffmpeg failed"
for gi, g in enumerate(groups):
    got = sorted(glob.glob(os.path.join(OUT, "_x%03d_*.jpg" % gi)))
    assert len(got) == len(g), "group %d: extracted %d of %d frames" % (gi, len(got), len(g))
    for f, j in zip(g, got):
        dst = os.path.join(OUT, "f%05d_%s.jpg" % (f, want[f]))
        os.replace(j, dst); rows.append({"frame": f, "beat": want[f], "file": os.path.basename(dst)})
json.dump(rows, open(os.path.join(OUT, "frames.json"), "w", encoding="utf-8"), indent=1)
by = {}
for r in rows:
    by.setdefault(r["beat"].split("-")[0] if "-" in r["beat"] else r["beat"], []).append(r)
for sec, rs in by.items():
    W, Hh, n = 640, 360, 3
    sheet = Image.new("RGB", (W * n, (Hh + 22) * ((len(rs) + n - 1) // n)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, r in enumerate(rs):
        x, y = (i % n) * W, (i // n) * (Hh + 22)
        sheet.paste(Image.open(os.path.join(OUT, r["file"])).resize((W, Hh)), (x, y + 22))
        d.text((x + 6, y + 4), "f%d  %s" % (r["frame"], r["beat"]), fill=(255, 255, 255))
    sheet.save(os.path.join(OUT, "sheet_%s.jpg" % sec), quality=88)
print(len(rows), "frames,", len(by), "sheets ->", OUT)
