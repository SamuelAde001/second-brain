# Turns the plan's beats.json into BUILD LIST.json: look-anchor units (Opus), design units (Opus) and 2-4 beat spec units (workers).
# Usage: python make_build_list.py --beats beats.json --captures captures.json --anchors anchors.json --out "BUILD LIST.json"
# Promoted from video 4 on 2026-10-30.
"""make_build_list.py - plan beats.json -> BUILD LIST.json (editor-builder, 2026-10-29).

Units: one per look-anchor beat (built first by Opus, Stage 3), one per design beat (Opus), and spec units of 2-4
neighbouring spec beats inside one section (workers, Stage 4). Spec units are cut by a small DP over each section's
spec beats in timeline order: cost = 10 per extra anchor family + size cost (2: 2, 3: 0, 4: 1, 1: 30) + 3 per 1000 f
of span - 3 per beat that shares a capture with another beat in the unit. needs = capture ids (sec aliases mapped to the CAP id), take and ref names from captures_v2.json, FLOW / BLD
ids from the assets, the family's anchor beat, hero stills the beat names.
"""
import argparse, datetime, json, os, re
from collections import Counter

ap = argparse.ArgumentParser(description="Plan beats.json -> BUILD LIST.json: look-anchor units, design units and 2-4 beat spec units.")
ap.add_argument("--beats", required=True, help="merged beats.json of the plan")
ap.add_argument("--captures", required=True, help="captures json (captures, takes, refs)")
ap.add_argument("--anchors", required=True, help='json {family: [anchor beat id, why]} - the family look anchors')
ap.add_argument("--out", required=True, help="BUILD LIST.json to write")
ap.add_argument("--by", default="make_build_list.py", help="provenance string written into the list")
A = ap.parse_args()
CAPS = A.captures
ANCHOR_BEATS = json.load(open(A.anchors, encoding="utf-8"))
SIZE = {1: 30, 2: 2, 3: 0, 4: 1}


def load_caps():
    c = json.load(open(CAPS, encoding="utf-8"))
    alias = {}
    for x in c["captures"]:
        alias[x["id"]] = x["id"]
        for v in (x.get("sec_ids") or {}).values():
            alias[v] = x["id"]
    takes = {}
    for t in c["takes"]:
        for bid in re.split(r"\+", str(t.get("beat") or "")):
            bid = re.sub(r"-S\d+$", "", bid.strip())
            takes.setdefault(bid, []).append(t["name"])
    refs = {}
    for r in c["refs"]:
        refs.setdefault(r["cap"], []).append(r["name"])
    return alias, takes, refs


def beat_needs(b, alias, takes, refs):
    s = json.dumps(b.get("assets") or [], ensure_ascii=False)
    caps = sorted({alias.get(t, t) for t in re.findall(r"CAP-[A-Z0-9]+(?:-\d+)?", s)}, key=lambda x: (len(x), x))
    out = list(caps)
    out += [f"take:{n}" for n in takes.get(b["id"], []) if n.split("_")[0] in caps]   # only takes of captures the beat uses
    for c in caps:
        out += [f"ref:{n}" for n in refs.get(c, [])]
    out += sorted(set(re.findall(r"FLOW-[A-Z0-9]+-\d+", s)))
    out += sorted(set(re.findall(r"BLD-[A-Z0-9]+-\d+", s)))
    out += [f"hero:{h}" for h in re.findall(r"frames/[\w.\-]+\.(?:png|jpg)", str(b.get("hero") or ""))]
    return out


def uniq(xs):
    seen, out = set(), []
    for x in xs:
        if x not in seen:
            seen.add(x); out.append(x)
    return out


def chunk_cost(ch):
    fams = {b["anchor"] for b in ch if b.get("anchor")}
    span = ch[-1]["end"] - ch[0]["start"]
    caps = [set(b.get("_caps") or ()) for b in ch]
    shared = sum(1 for i, c in enumerate(caps) if any(c & d for j, d in enumerate(caps) if j != i))
    return 10 * max(0, len(fams) - 1) + SIZE[len(ch)] + 3 * span / 1000 - 3 * shared


def split(seq):
    n = len(seq)
    best = [(0, [])] + [(1e9, None)] * n
    for i in range(1, n + 1):
        for k in (2, 3, 4, 1):
            if k > i or (k == 1 and n > 1):
                continue
            c = best[i - k][0] + chunk_cost(seq[i - k:i])
            if c < best[i][0]:
                best[i] = (c, best[i - k][1] + [seq[i - k:i]])
    return best[n][1]


def main():
    beats = json.load(open(A.beats, encoding="utf-8"))
    alias, takes, refs = load_caps()
    vis = [b for b in beats if b["kind"] != "none"]
    byid = {b["id"]: b for b in beats}
    anchor_ids = {v[0] for v in ANCHOR_BEATS.values()}
    for b in vis:   # canonical capture ids, for the shared-capture bonus (same engine/take in one unit)
        b["_caps"] = {x for x in beat_needs(b, alias, takes, refs) if x.startswith("CAP-")}
    for a, (bid, _) in ANCHOR_BEATS.items():
        assert byid[bid]["anchor"] == a, (a, bid, byid[bid]["anchor"])
    units = []

    def unit(kind, sec, ch, n):
        fams = Counter(b["anchor"] for b in ch if b.get("anchor"))
        anchor = fams.most_common(1)[0][0] if fams else None
        needs = []
        for b in ch:
            needs += beat_needs(b, alias, takes, refs)
        for f in fams:
            ab = ANCHOR_BEATS[f][0]
            if ab not in [x["id"] for x in ch]:
                needs.append(f"anchor:{ab} ({f})")
        u = {"unit": f"{sec}-{kind}{n:02d}", "owner": "spec" if kind == "s" else "design",
             "beats": [b["id"] for b in ch], "anchor": anchor, "base": " ; ".join(uniq(str(b.get("base") or "") for b in ch)),
             "needs": uniq(needs), "sec": sec, "frames": [ch[0]["start"], ch[-1]["end"]]}
        if len(fams) > 1:
            u["anchors_mixed"] = sorted(fams)
        if kind == "a":
            u["look_anchor"] = True
            u["note"] = "built first by Opus (Stage 3) as the family's look anchor; beat owner in the plan: " + ch[0]["owner"]
        return u

    secs = uniq(b["sec"] for b in beats)
    for sec in secs:
        sv = [b for b in vis if b["sec"] == sec]
        n = {"a": 0, "d": 0, "s": 0}
        spec = [b for b in sv if b["owner"] == "spec" and b["id"] not in anchor_ids]
        chunks = split(spec) if spec else []
        start_of = {ch[0]["id"]: ch for ch in chunks}
        for b in sv:
            if b["id"] in anchor_ids:
                n["a"] += 1; units.append(unit("a", sec, [b], n["a"]))
            elif b["owner"] == "design":
                n["d"] += 1; units.append(unit("d", sec, [b], n["d"]))
            elif b["id"] in start_of:
                n["s"] += 1; units.append(unit("s", sec, start_of[b["id"]], n["s"]))
    covered = [i for u in units for i in u["beats"]]
    assert sorted(covered) == sorted(b["id"] for b in vis), "unit coverage"
    assert len(covered) == len(set(covered))
    out = {
        "made": datetime.date.today().isoformat(), "by": A.by,
        "source": "%s (%d beats), %s" % (os.path.basename(A.beats), len(beats), os.path.basename(A.captures)),
        "rules": "look anchors (look_anchor: true) are built first by Opus; design units are one beat each (Opus); spec units are "
                 "2-4 neighbouring spec beats in one section (Sonnet workers) and copy the anchor beat of their family "
                 "(needs: anchor:<beat>). Plain A-roll beats (kind none) are not units: the A-roll pass is main-session work.",
        "anchor_beats": {a: {"beat": bid, "why": why} for a, (bid, why) in ANCHOR_BEATS.items()},
        "units": units,
    }
    os.makedirs(os.path.dirname(os.path.abspath(A.out)), exist_ok=True)
    json.dump(out, open(A.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sp = [u for u in units if u["owner"] == "spec"]
    print("units", len(units), "| anchors", sum(1 for u in units if u.get("look_anchor")),
          "| design", sum(1 for u in units if u["owner"] == "design" and not u.get("look_anchor")),
          "| spec", len(sp), "sizes", dict(Counter(len(u["beats"]) for u in sp)),
          "| mixed", [(u["unit"], u["beats"], u["anchors_mixed"]) for u in sp if u.get("anchors_mixed")])
    for u in sp:
        print(" ", u["unit"], u["frames"], u["anchor"], " ".join(u["beats"]))


if __name__ == "__main__":
    main()
