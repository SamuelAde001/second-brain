"""Cut a big map into horizontal bands so each SVG stays under Canva's 3 MB limit.
Cuts fall on near-empty rows of the full render. python split_map.py map09 [map01 …]"""
import importlib, json, os, re, sys
import pymupdf
from PIL import Image
import numpy as np
from build_map import chrome, HERE, OUT
import maplib

LIMIT = 2_700_000


def svg_of(m, body, w, h, band, tag):
    hp = os.path.join(HERE, f"{m.NAME}-{tag}.html")
    open(hp, "w", encoding="utf-8").write(maplib.page(body, w, h, m.NAME, band))
    pdf = os.path.join(OUT, f"{m.NAME}-{tag}.pdf")
    chrome(f"--print-to-pdf={pdf}", "file:///" + hp.replace("\\", "/"))
    s = pymupdf.open(pdf)[0].get_svg_image(text_as_path=True)
    return re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w}" height="{band[1]-band[0]}"', s, count=1)


def split(modname):
    m = importlib.import_module(modname)
    if hasattr(m, "P") and os.path.exists(os.path.join(HERE, "photos.json")):
        m.P.update(json.load(open(os.path.join(HERE, "photos.json"), encoding="utf-8")))
    body, w, _ = m.build()
    h = json.load(open(os.path.join(OUT, m.NAME + ".json")))["size_px"][1]
    # emptiest rows, from the full map's PDF
    p = pymupdf.open(os.path.join(OUT, m.NAME + ".pdf"))[0]
    k = 0.1 * 4 / 3
    pix = p.get_pixmap(matrix=pymupdf.Matrix(k, k), alpha=True)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 4)[:, :, 3]
    ink = (a > 20).sum(1)
    ok = [int(y / 0.1) for y in range(len(ink)) if ink[y] <= 3]
    total = os.path.getsize(os.path.join(OUT, m.NAME + ".svg"))
    n = int(total / LIMIT) + 1
    while True:
        out = try_bands(m, body, w, h, ok, n)
        if all(o["kb"] * 1024 < LIMIT for o in out):
            break
        n += 1
    json.dump(out, open(os.path.join(OUT, m.NAME + "-bands.json"), "w"), indent=1)
    print(m.NAME, out)


def try_bands(m, body, w, h, ok, n):
    bands, start = [], 0
    while True:
        target = start + (h - start) // max(1, n - len(bands))
        if n - len(bands) <= 1 or target >= h:
            bands.append((start, h)); break
        cut = min((c for c in ok if c > start + 300), key=lambda c: abs(c - target), default=h)
        bands.append((start, cut)); start = cut
    out = []
    for i, b in enumerate(bands):
        s = svg_of(m, body, w, h, b, f"b{i}")
        fn = f"{m.NAME}-b{i}.svg"
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(s)
        out.append({"file": fn, "y": b[0], "h": b[1] - b[0], "kb": len(s.encode()) // 1024})
    return out


if __name__ == "__main__":
    for a in sys.argv[1:]:
        split(a)
