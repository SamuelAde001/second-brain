# Scans every NeoTextMotion node in an install list: accent (non-white) text must carry StShineEnable 0.
# Usage: python accent_scan.py --list <install list.txt>
# Promoted from video 4 on 2026-10-30.
# DECISIONS #52 scan over the install list (Editor, 2026-10-29): every NeoTextMotion node whose text is not plain white
# (a Char1 range on, or a non-white base ColorR/G/B) must carry StShineEnable 0. A missing StShineEnable counts as on.
import argparse, json, os, re, sys

ap = argparse.ArgumentParser(description="Scan the install list: every accent (non-white) NeoTextMotion node must carry StShineEnable 0 (DECISIONS #52).")
ap.add_argument("--list", required=True, help="install list: one manifest.json path per line")
LST = ap.parse_args().list


def val(b, k, d=None):
    m = re.search(r"\n\s*%s = Input \{ Value = ([^,]+)," % k, b)
    return m.group(1).strip() if m else d


n, hits = 0, []
for m in [l.strip().strip('"') for l in open(LST, encoding="utf-8") if l.strip()]:
    beat = os.path.basename(os.path.dirname(m))
    for o in json.load(open(m, encoding="utf-8")):
        s = o.get("setting")
        if not s or not os.path.exists(s):
            continue
        t = open(s, encoding="utf-8", errors="replace").read()
        for mm in re.finditer(r"\n(\t+)(\w+) = Fuse\.NeoMotionText \{", t):
            e = t.index("\n" + mm.group(1) + "},", mm.end())
            b = t[mm.start():e]; n += 1
            rgb = [float(val(b, k, 1)) for k in ("ColorR", "ColorG", "ColorB")]
            lo, hi = float(val(b, "Char1RangeLow", 0)), float(val(b, "Char1RangeHigh", 1))
            accent = (val(b, "Char1Enable", "0") == "1" and hi > lo and lo < 1.0) or any(abs(v - 1) > 1e-3 for v in rgb)
            if accent and val(b, "StShineEnable", "1") != "0":
                hits.append((beat, os.path.basename(s), mm.group(2), [round(v * 255) for v in rgb], (val(b, "StyledText", "") or "")[:30]))
print("NeoTextMotion nodes scanned:", n, "| accent nodes with the shine on:", len(hits))
for h in hits:
    print("  ", h)
