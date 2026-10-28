"""Merge the nine onboarding sections into one Canva clipboard payload, laid out in three columns.
python onb_merge.py <design id> <doc id>  ->  out/native-white/onboarding-board.json"""
import json, os, sys
from native import OUT, bbox, r2

COLS, GUT = [[0, 1, 2], [3, 4, 5], [6, 7, 8]], 1500
NAMES = ["onb00-welcome", "onb01-why", "onb02-plan", "onb03-goals", "onb04-setup", "onb05-channels", "onb06-most", "onb07-turn", "onb08-sunday"]


def shift(el, dx, dy):
    el["A"] = r2(el["A"] + dy); el["B"] = r2(el["B"] + dx)
    if el["A?"] == "U":
        for end in ("b", "c"):
            el[end]["C"]["A"] = r2(el[end]["C"]["A"] + dy); el[end]["C"]["B"] = r2(el[end]["C"]["B"] + dx)


els, x = [], 0
for col in COLS:
    y, cw = 0, 0
    for i in col:
        p = json.load(open(os.path.join(OUT, NAMES[i] + ".json"), encoding="utf-8"))
        bs = [bbox(e) for e in p["A"]]
        x0, y0 = min(b[0] for b in bs), min(b[1] for b in bs)
        w, h = max(b[2] for b in bs) - x0, max(b[3] for b in bs) - y0
        for e in p["A"]:
            shift(e, x - x0, y - y0); els.append(e)
        print(NAMES[i], "at", x, y, "size", round(w), round(h))
        y += h + GUT; cw = max(cw, w)
    x += cw + GUT
p["A"] = els; p["c"], p["i"] = sys.argv[1], sys.argv[2]
s = json.dumps(p, ensure_ascii=False, separators=(",", ":"))
open(os.path.join(OUT, "onboarding-board.json"), "w", encoding="utf-8").write(s)
print("total", len(els), "elements", len(s) // 1024, "KB")
