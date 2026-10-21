"""Sheet of chosen frames: python pick.py OUT.jpg 4.2 6.2 ..."""
import sys, os, glob, json, pymupdf
from PIL import Image
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
want = sys.argv[2:]; fw, fh = 560, 315
tiles = []
for pdf in sorted(glob.glob(os.path.join(OUT, "row*.pdf"))):
    info = json.load(open(pdf[:-4] + ".json"))
    hits = [i for i, f in enumerate(info["frames"]) if f in want]
    if not hits: continue
    p = pymupdf.open(pdf)[0]; k = fw / 1920 * 4 / 3
    pix = p.get_pixmap(matrix=pymupdf.Matrix(k, k)); im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    gap = round(420 * fw / 1920)
    for i in hits: tiles.append(im.crop((i * (fw + gap), 0, i * (fw + gap) + fw, fh)))
cols = 3; rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (fw + 8), rows * (fh + 8)), "#333")
for j, t in enumerate(tiles): sheet.paste(t, ((j % cols) * (fw + 8), (j // cols) * (fh + 8)))
sheet.save(sys.argv[1], quality=85); print(sys.argv[1], len(tiles))
