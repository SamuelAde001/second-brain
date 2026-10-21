"""Reveal stickies: one champagne SVG per hidden part, sized to cover it, label outlined in Plus Jakarta Sans ExtraBold.
Reads out/map*.json (positions from build_map.py), writes out/covers/<row>-NN.svg and out/covers.json."""
import glob, json, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
os.makedirs(os.path.join(OUT, "covers"), exist_ok=True)
font = instantiateVariableFont(TTFont(os.path.join(HERE, "kit", "fonts", "PlusJakartaSans.ttf")), {"wght": 800})
gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
UPM = font["head"].unitsPerEm
PAD = 12


def text_path(txt, size, x0, base):
    s = size / UPM
    d, x = [], 0
    for ch in txt:
        g = cmap.get(ord(ch))
        if not g:
            continue
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x0 + x * s, base)))
        d.append(pen.getCommands())
        x += hmtx[g][0]
    return " ".join(d), x * s


def width(txt, size):
    return sum(hmtx[cmap[ord(c)]][0] for c in txt if ord(c) in cmap) * size / UPM


def cover(label, w, h):
    size = max(16, min(30, h * 0.3))
    while width(label, size) > w - 90 and size > 12:
        size -= 1
    tw = width(label, size)
    mk = 22 * size / 30
    total = mk + 12 + tw
    x0 = (w - total) / 2
    base = h / 2 + size * 0.36
    d, _ = text_path(label, size, x0 + mk + 12, base)
    my = h / 2 - mk * 16 / 14 / 2
    sc = mk / 14
    marker = f'<path transform="translate({x0:.1f} {my:.1f}) scale({sc:.3f})" d="M0 0H14V9.6L7 16L0 9.6Z" fill="#0A1F44"/>'
    r = min(18, h / 4)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="{r}" fill="#E8C47E"/>'
            f'<rect x="0" y="0" width="{w}" height="{h-6}" rx="{r}" fill="#FCDD9E"/>'
            f'{marker}<path d="{d}" fill="#0A1F44"/></svg>')


manifest = {}
for js in sorted(glob.glob(os.path.join(OUT, "map*.json"))):
    name = os.path.basename(js)[:-5]
    info = json.load(open(js, encoding="utf-8"))
    items = []
    for k, r in enumerate(info["rv"]):
        w, h = r["w"] + 2 * PAD, r["h"] + 2 * PAD
        fn = f"{name}-{k:02d}.svg"
        open(os.path.join(OUT, "covers", fn), "w", encoding="utf-8").write(cover(r["label"], w, h))
        items.append({"file": fn, "x": r["x"] - PAD, "y": r["y"] - PAD, "w": w, "h": h, "label": r["label"]})
    manifest[name] = {"size": info["size_px"], "covers": items}
json.dump(manifest, open(os.path.join(OUT, "covers.json"), "w", encoding="utf-8"), indent=1)
print(sum(len(v["covers"]) for v in manifest.values()), "covers")
