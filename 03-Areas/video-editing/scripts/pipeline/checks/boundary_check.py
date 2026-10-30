# Plan assembly check: holes, overlaps, seams between groups, plain A-roll slivers between visuals, visual starts off a word or cut, edges inside a word.
# Usage: python boundary_check.py --sections-dir <sections> --words cut_words.json --items cut_items.json --len 12100 [--order g01,g02,...] | --merged --beats beats.json
# Promoted from video 4 on 2026-10-30.
"""boundary_check.py - plan assembly check (editor-builder, 2026-10-29).

Loads the section files (or beats.json with --merged), checks against the cut words and the
V1 clip cuts (the cut items json):
  holes / overlaps (every beat butts its neighbour), seams between groups, plain A-roll pieces < 12 f
  between two visuals, visual starts not 0-3 f after a word start or on a cut, edges inside a word.
Prints counts and ids only.
"""
import argparse, json, os, sys, bisect

ap = argparse.ArgumentParser(description="Plan assembly check: holes, overlaps, seams, plain A-roll slivers, visual starts, edges inside a word.")
ap.add_argument("--sections-dir", help="folder with the section files <group>.json (g01.json ...)")
ap.add_argument("--beats", help="merged beats.json (with --merged)")
ap.add_argument("--merged", action="store_true", help="read --beats instead of the section files")
ap.add_argument("--words", required=True, help="cut_words.json")
ap.add_argument("--items", required=True, help="cut items json: [type, track, start, end, src] rows")
ap.add_argument("--len", type=int, required=True, help="timeline length in frames")
ap.add_argument("--order", help="comma list of group names in timeline order (default: the *.json names in --sections-dir, sorted)")
ARGS = ap.parse_args()
if ARGS.merged and not ARGS.beats:
    ap.error("--merged needs --beats")
if not ARGS.merged and not ARGS.sections_dir:
    ap.error("give --sections-dir (or --merged --beats)")
WORDS, ITEMS, TOTAL = ARGS.words, ARGS.items, ARGS.len
ORDER = ARGS.order.split(",") if ARGS.order else (sorted(f[:-5] for f in os.listdir(ARGS.sections_dir) if f.endswith(".json")) if ARGS.sections_dir else [])


def load(merged=False):
    if merged:
        bs = json.load(open(ARGS.beats, encoding="utf-8"))
        for b in bs:
            b["_g"] = b.get("file")
    else:
        bs = []
        for g in ORDER:
            for b in json.load(open(os.path.join(ARGS.sections_dir, g + ".json"), encoding="utf-8")):
                b["_g"] = g
                bs.append(b)
    bs.sort(key=lambda b: (b["start"], b["end"]))
    return bs


def cuts():
    it = json.load(open(ITEMS, encoding="utf-8"))
    s = set()
    for k, tr, a, z, _ in it:
        if k == "video" and tr == 1:
            s.add(a); s.add(z)
    return sorted(s)


def vis(b):
    return b.get("kind") != "none"


def main():
    bs = load(ARGS.merged)
    global ORDER
    if not ORDER:
        ORDER = sorted({b["_g"] for b in bs if b.get("_g")})
    words = json.load(open(WORDS, encoding="utf-8"))
    C = cuts(); CS = set(C)
    ws = sorted({w["f"] for w in words})
    out = {}
    # holes/overlaps between neighbours
    hol, ovl = [], []
    if bs[0]["start"] != 0:
        hol.append(f"0-{bs[0]['start']}")
    for a, b in zip(bs, bs[1:]):
        if b["start"] > a["end"]:
            hol.append(f"{a['id']}|{b['id']} {a['end']}-{b['start']}")
        elif b["start"] < a["end"]:
            ovl.append(f"{a['id']}({a['start']}-{a['end']}) x {b['id']}({b['start']}-{b['end']})")
    if max(b["end"] for b in bs) != TOTAL:
        hol.append(f"end {max(b['end'] for b in bs)} != {TOTAL}")
    out["holes"] = hol; out["overlaps"] = ovl
    # seams
    seam = []
    for g1, g2 in zip(ORDER, ORDER[1:]):
        A = [b for b in bs if b["_g"] == g1]; B = [b for b in bs if b["_g"] == g2]
        if A and B:
            a, b = A[-1], B[0]
            seam.append(f"{g1}/{g2}: {a['id']} {a['start']}-{a['end']} | {b['id']} {b['start']}-{b['end']}"
                        + ("" if a["end"] == b["start"] else f" MISMATCH {b['start'] - a['end']:+d}"))
    out["seams"] = seam
    # plain A-roll pieces < 12 f between visuals
    sl = []
    for i in range(1, len(bs) - 1):
        b = bs[i]
        if not vis(b) and b["end"] - b["start"] < 12 and vis(bs[i - 1]) and vis(bs[i + 1]):
            sl.append(f"{b['id']} {b['start']}-{b['end']} ({b['end'] - b['start']} f)")
    out["plain_under_12_between_visuals"] = sl
    # visual starts: on a cut or 0-3 f after a word start
    off = []
    for b in bs:
        if not vis(b):
            continue
        s = b["start"]
        if s == 0 or s in CS:
            continue
        k = bisect.bisect_right(ws, s) - 1
        d = s - ws[k] if k >= 0 else None
        if d is None or d > 3:
            nxt = ws[k + 1] if k + 1 < len(ws) else None
            off.append(f"{b['id']} {s} (prev word +{d}, next word {nxt}, cuts {[c for c in C if abs(c - s) <= 8]})")
    out["visual_start_off"] = off
    # edges inside a word
    inw = []
    edges = sorted({b["start"] for b in bs} | {b["end"] for b in bs})
    for e in edges:
        if e in CS:
            continue
        for w in words:
            if w["f"] < e < w["e"] - 1:
                L = [b["id"] for b in bs if b["end"] == e]; R = [b["id"] for b in bs if b["start"] == e]
                inw.append(f"{e} in '{w['w']}' {w['f']}-{w['e']} ({'/'.join(L)}|{'/'.join(R)})")
                break
    out["edges_inside_word"] = inw
    ids = [b["id"] for b in bs]
    out["dup_ids"] = sorted({i for i in ids if ids.count(i) > 1})
    print("beats", len(bs), "visuals", sum(map(vis, bs)), "cuts", len(C))
    for k, v in out.items():
        print(k.upper(), f"({len(v)})", "; ".join(v) if v else "none")


if __name__ == "__main__":
    main()
