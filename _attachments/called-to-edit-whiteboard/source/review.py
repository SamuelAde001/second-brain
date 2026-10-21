"""Contact sheets of built rows for review: each frame at 800 px wide, 2 per sheet row."""
import sys, os, glob, json, pymupdf
from PIL import Image
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
SC = os.environ.get("SHEETS", OUT)
pick = sys.argv[1] if len(sys.argv) > 1 else ""
for pdf in sorted(glob.glob(os.path.join(OUT, "row*.pdf"))):
    name = os.path.basename(pdf)[:-4]
    if pick not in name: continue
    info = json.load(open(pdf[:-4] + ".json"))
    p = pymupdf.open(pdf)[0]
    k = 800 / 1920 * 4 / 3
    pix = p.get_pixmap(matrix=pymupdf.Matrix(k, k))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    n = len(info["frames"]); fw = 800; gap = round(420 * 800 / 1920); fh = 450
    tiles = [im.crop((i * (fw + gap), 0, i * (fw + gap) + fw, fh)) for i in range(n)]
    for s in range(0, n, 4):
        part = tiles[s:s + 4]
        sheet = Image.new("RGB", (2 * fw + 10, ((len(part) + 1) // 2) * (fh + 10)), "#333")
        for j, t in enumerate(part):
            sheet.paste(t, ((j % 2) * (fw + 10), (j // 2) * (fh + 10)))
        sheet.save(os.path.join(SC, f"sheet-{name}-{s//4}.jpg"), quality=82)
        print(os.path.join(SC, f"sheet-{name}-{s//4}.jpg"))
