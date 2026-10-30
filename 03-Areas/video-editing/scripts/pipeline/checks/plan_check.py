# Checks a visual plan: coverage per part, holes and overlaps, slivers next to cuts, visual starts and edges against the words, seams, sections, schema, capture ids.
# Usage: python plan_check.py --config plan.json --sections-dir <sections> --words cut_words.json --sents sentences.json --xml cut.xml --captures captures.json [--json]
# Promoted from video 4 on 2026-10-30.
"""plan_check.py - checks a visual plan (Editor, 2026-10-26).

Section files <group>.json, words from cut_words.json, sentences from sentences.json, cuts from Samuel's cut XML.
Plain A-roll is an explicit kind "none" beat, so every frame must sit in exactly one beat. The per-video values
(group order, length, section ranges, part targets, sliver exceptions) come from the --config json
(video 4's: examples/video4_plan.json).

Reports: beats per group and section, frame coverage (holes, overlaps), visual coverage per
part (hook / intro / body targets from PLAN BRIEF section 3), plain A-roll stretches against
the part limits, slivers next to cuts, visual starts not on a word or cut, edges inside a word,
cross-group seams, section starts, duplicate ids, sents that don't touch their beat, consecutive
visuals on the same construct, capture ids missing from captures.json, schema gaps.
Prints counts and ids only (the full result with --json).
"""
import argparse, json, os, sys, bisect, xml.etree.ElementTree as ET

FPS = 24000 / 1001
# set by configure(): the per-video values
SEC = WORDS = SENTS = XML = CAPS = None
ORDER, TOTAL, SECTIONS, PARTS, SLIVER_OK, BODY_START, CFG = [], 0, [], [], {}, 0, {}


def add_args(ap):
    """The arguments plan_check.py and make_plan_docs.py share."""
    ap.add_argument("--config", required=True, help="json: order, total, sections, parts, sliver_ok (+ page wording for make_plan_docs); see examples/video4_plan.json")
    ap.add_argument("--sections-dir", required=True, help="folder with the section files <group>.json")
    ap.add_argument("--words", required=True, help="cut_words.json")
    ap.add_argument("--sents", required=True, help="sentences.json")
    ap.add_argument("--xml", required=True, help="Samuel's cut as FCP xml")
    ap.add_argument("--captures", required=True, help="captures.json")


def configure(a):
    global SEC, WORDS, SENTS, XML, CAPS, ORDER, TOTAL, SECTIONS, PARTS, SLIVER_OK, BODY_START, CFG
    CFG = json.load(open(a.config, encoding="utf-8"))
    SEC, WORDS, SENTS, XML, CAPS = a.sections_dir, a.words, a.sents, a.xml, a.captures
    ORDER, TOTAL = CFG["order"], CFG["total"]
    SECTIONS = [tuple(s) for s in CFG["sections"]]      # [code, start, end)
    PARTS = [tuple(p) for p in CFG["parts"]]            # (name, start, end, min coverage, max plain A-roll stretch)
    SLIVER_OK = CFG.get("sliver_ok", {})                # text over A-roll: the A-roll shows under it, so an edge near a cut is not a sliver
    BODY_START = next(p[1] for p in PARTS if p[0] == "body")


KINDS = {"capture", "demo", "mograph", "broll", "aroll-fx", "none"}
FIELDS = ["id", "sec", "start", "end", "sents", "alex", "kind", "family", "construct", "visual",
          "text", "motion", "layers", "track", "sfx", "assets", "risk", "reuses", "why", "hero"]


def load():
    beats, groups = [], {}
    for name in ORDER:
        fp = os.path.join(SEC, name + ".json")
        if not os.path.exists(fp):
            continue
        d = json.load(open(fp, encoding="utf-8"))
        bs = d["beats"] if isinstance(d, dict) else d
        for b in bs:
            b["_g"] = name
            beats.append(b)
        groups[name] = sorted(bs, key=lambda b: (b["start"], b["end"]))
    beats.sort(key=lambda b: (b["start"], b["end"]))
    return beats, groups


def cuts_from_xml():
    seq = ET.parse(XML).getroot().find("sequence")
    cl = seq.find("media/video").find("track").findall("clipitem")
    s = {int(c.findtext("start")) for c in cl} | {int(c.findtext("end")) for c in cl}
    return sorted(s)


def is_vis(b):
    return b.get("kind") != "none"


def check():
    beats, groups = load()
    words = json.load(open(WORDS, encoding="utf-8"))
    sents = {f"S{s['n']:03d}": s for s in json.load(open(SENTS, encoding="utf-8"))}
    cuts = cuts_from_xml()
    cutset = set(cuts)
    wstarts = sorted({w["f"] for w in words})
    R = {}

    R["beats_per_group"] = {g: len(groups.get(g, [])) for g in ORDER}
    R["beats_per_section"] = {c: sum(1 for b in beats if b.get("sec") == c) for c, _, _ in SECTIONS}
    R["missing_groups"] = [g for g in ORDER if g not in groups]
    R["beats"] = len(beats)
    R["visuals"] = sum(1 for b in beats if is_vis(b))

    # schema
    schema = []
    for b in beats:
        miss = [k for k in FIELDS if k not in b]
        if miss:
            schema.append(f"{b.get('id')}: missing {','.join(miss)}")
        if b.get("kind") not in KINDS:
            schema.append(f"{b.get('id')}: kind {b.get('kind')!r}")
        if b["end"] <= b["start"]:
            schema.append(f"{b['id']}: end<=start")
        if is_vis(b) and not b.get("assets"):
            schema.append(f"{b['id']}: visual without assets")
    R["schema"] = schema

    ids = [b["id"] for b in beats]
    R["duplicate_ids"] = sorted({i for i in ids if ids.count(i) > 1})

    # every frame in exactly one beat
    cnt = [0] * TOTAL
    vis = [0] * TOTAL
    for b in beats:
        for f in range(max(0, b["start"]), min(TOTAL, b["end"])):
            cnt[f] += 1
            if is_vis(b):
                vis[f] = 1

    def runs(pred):
        out, f = [], 0
        while f < TOTAL:
            if pred(f):
                a = f
                while f < TOTAL and pred(f):
                    f += 1
                out.append((a, f))
            else:
                f += 1
        return out
    R["holes"] = [f"{a}-{z}" for a, z in runs(lambda f: cnt[f] == 0)]
    R["double_frames"] = [f"{a}-{z}" for a, z in runs(lambda f: cnt[f] > 1)]
    R["first_frame"] = beats[0]["start"] if beats else None
    R["last_frame"] = max(b["end"] for b in beats) if beats else None
    R["overlaps"] = [f"{a['id']}({a['start']}-{a['end']}) x {b['id']}({b['start']}-{b['end']})"
                     for i, a in enumerate(beats) for b in beats[i + 1:]
                     if b["start"] < a["end"] and b["end"] > a["start"]]

    # coverage and plain A-roll per part
    R["coverage_total"] = round(100 * sum(vis) / TOTAL, 1)
    plain = runs(lambda f: not vis[f])
    parts = {}
    for name, a, z, mincov, maxplain in PARTS:
        cov = sum(vis[a:z]) / (z - a)
        long_ = []
        for p0, p1 in plain:
            s0, s1 = max(p0, a), min(p1, z)
            if s1 - s0 > maxplain and p0 >= a:   # stretch that starts in this part
                why = " ".join(str(b.get("why", "")) for b in beats if b["kind"] == "none" and b["start"] < p1 and b["end"] > p0)
                long_.append(f"{p0}-{p1} ({p1 - p0} f)")
        parts[name] = {"coverage": round(100 * cov, 1), "target": int(mincov * 100),
                       "ok": cov >= mincov - 0.005 if name != "body" else abs(cov - mincov) <= 0.08,
                       "plain_over_limit": long_, "limit": maxplain}
    R["parts"] = parts
    # body: never more than 360 f without a new element (beat level)
    R["body_plain_over_360"] = [f"{a}-{z} ({z - a} f)" for a, z in plain if z - a > 360 and z > BODY_START]
    R["visuals_over_360_check_inside"] = [f"{b['id']} ({b['end'] - b['start']} f)" for b in beats
                                          if is_vis(b) and b["end"] - b["start"] > 360]
    R["visuals_under_24f"] = [f"{b['id']} ({b['end'] - b['start']} f)" for b in beats
                              if is_vis(b) and b["end"] - b["start"] < 24]

    # slivers: a visual edge 1-12 f from a cut that leaves A-roll showing on the other side
    sliv, info = [], []
    for i, b in enumerate(beats):
        if not is_vis(b) or b["id"] in SLIVER_OK:
            continue
        prev = beats[i - 1] if i else None
        nxt = beats[i + 1] if i + 1 < len(beats) else None
        s, e = b["start"], b["end"]
        if s not in cutset and (prev is None or not is_vis(prev)):
            k = bisect.bisect_right(cuts, s) - 1
            if k >= 0 and 1 <= s - cuts[k] <= 12:
                sliv.append(f"{b['id']} starts {s}, {s - cuts[k]} f of A-roll after cut {cuts[k]}")
        if e not in cutset and (nxt is None or not is_vis(nxt)):
            k = bisect.bisect_left(cuts, e)
            if k < len(cuts) and 1 <= cuts[k] - e <= 12:
                sliv.append(f"{b['id']} ends {e}, {cuts[k] - e} f of A-roll before cut {cuts[k]}")
            k = bisect.bisect_right(cuts, e) - 1
            if k >= 0 and 1 <= e - cuts[k] <= 6:
                info.append(f"{b['id']} ends {e}, {e - cuts[k]} f past cut {cuts[k]}")
    R["slivers"] = sliv
    R["ends_just_past_cut_info"] = info
    # tiny plain A-roll between two visuals
    R["plain_slivers_between_visuals"] = [f"{b['id']} {b['start']}-{b['end']} ({b['end'] - b['start']} f)"
                                          for i, b in enumerate(beats)
                                          if not is_vis(b) and b["end"] - b["start"] <= 12]

    # starts on a word or cut
    off, near = [], []
    for b in beats:
        if not is_vis(b):
            continue
        s = b["start"]
        if s in cutset or s in wstarts or s == 0:
            continue
        k = bisect.bisect_right(wstarts, s) - 1
        prevw = wstarts[k] if k >= 0 else None
        nextw = wstarts[k + 1] if k + 1 < len(wstarts) else None
        if prevw is not None and 1 <= s - prevw <= 3:
            near.append(f"{b['id']} {s} (+{s - prevw} after word {prevw})")
        else:
            off.append(f"{b['id']} {s} (word {prevw} / {nextw}, cuts near {[c for c in cuts if abs(c - s) <= 12]})")
    R["starts_near_word_ok"] = near
    R["starts_off_word"] = off
    # edges inside a word (a beat edge splitting a word)
    inword = []
    edges = sorted({b["start"] for b in beats} | {b["end"] for b in beats})
    for e in edges:
        if e in cutset:
            continue
        for w in words:
            if w["f"] < e < w["e"] - 1:
                left = [b["id"] for b in beats if b["end"] == e]
                right = [b["id"] for b in beats if b["start"] == e]
                inword.append(f"{e} inside '{w['w']}' {w['f']}-{w['e']} ({'/'.join(left)} | {'/'.join(right)})")
                break
    R["edges_inside_a_word"] = inword

    # seams between groups
    seams = []
    for g1, g2 in zip(ORDER, ORDER[1:]):
        if g1 not in groups or g2 not in groups:
            continue
        a, b = groups[g1][-1], groups[g2][0]
        if a["end"] != b["start"]:
            seams.append(f"{g1}/{g2}: {a['id']} ends {a['end']}, {b['id']} starts {b['start']} ({b['start'] - a['end']:+d})")
    R["seams"] = seams
    R["group_edges"] = {g: [groups[g][0]["start"], groups[g][-1]["end"]] for g in groups}

    # sections
    # a beat edge within 6 f of each section start (edges may have moved to the nearest cut)
    R["section_starts_without_beat_edge"] = [
        f"{c} {a} (" + " / ".join(f"{b['id']} {b['start']}-{b['end']}" for b in beats if b["start"] < a < b["end"]) + ")"
        for c, a, _ in SECTIONS if not any(abs(e - a) <= 6 for e in edges)]
    wrongsec = []
    for b in beats:
        mid = (b["start"] + b["end"]) // 2
        code = next((c for c, a, z in SECTIONS if a <= b["start"] < z), None)
        if b.get("sec") != code:
            wrongsec.append(f"{b['id']} sec {b.get('sec')} but starts in {code}")
    R["sec_code_mismatch"] = wrongsec

    # sents touch their beat
    bad = []
    for b in beats:
        for sid in b.get("sents") or []:
            s = sents.get(str(sid).split("-")[0].strip())
            if s is None:
                bad.append(f"{b['id']}: {sid} unknown")
            elif not (s["f"] < b["end"] + 24 and s["e"] > b["start"] - 24):
                bad.append(f"{b['id']}: {sid} [{s['f']}-{s['e']}] outside {b['start']}-{b['end']}")
    R["sents_outside_beat"] = bad

    # construct twice in a row (consecutive visuals, any A-roll between them under 48 f)
    rep = []
    vb = [b for b in beats if is_vis(b)]
    for a, b in zip(vb, vb[1:]):
        gap = b["start"] - a["end"]
        ca, cb = str(a.get("construct", "")).split(">")[-1].strip(), str(b.get("construct", "")).split(">")[0].strip()
        if ca and ca == cb and ca.upper() != "NONE" and gap < 48:
            rep.append(f"{a['id']}->{b['id']} {ca}")
    R["same_construct_in_a_row"] = rep

    # assets and captures
    caps = json.load(open(CAPS, encoding="utf-8"))
    known = set()
    for c in caps.get("captures", []):
        known.add(c["id"])
        for v in (c.get("sec_ids") or {}).values():
            known.add(v)
    used, unknown, status = {}, [], {}
    for b in beats:
        for a in b.get("assets") or []:
            if not isinstance(a, dict):
                continue
            st = a.get("status")
            status[st] = status.get(st, 0) + 1
            p_ = str(a.get("path") or "")
            for tok in p_.replace(",", " ").replace(";", " ").replace("/", " ").split():
                if tok.startswith("CAP-"):
                    tok = tok.strip(".()")
                    used.setdefault(tok, []).append(b["id"])
                    if tok not in known:
                        unknown.append(f"{b['id']}: {tok}")
    R["asset_status"] = status
    R["capture_ids_used"] = len(used)
    R["capture_ids_unknown"] = unknown
    R["demos"] = sum(1 for b in beats if b.get("kind") in ("demo", "capture"))
    return R


def main():
    ap = argparse.ArgumentParser(description="Checks a visual plan: coverage, holes, overlaps, slivers, starts and edges against the words and cuts, schema.")
    add_args(ap)
    ap.add_argument("--json", action="store_true", help="print the full result as json")
    args = ap.parse_args()
    configure(args)
    R = check()
    if args.json:
        print(json.dumps(R, indent=1))
        return
    p = print
    p("BEATS", R["beats"], "visuals", R["visuals"], "demos", R["demos"], "| per group",
      " ".join(f"{k}={v}" for k, v in R["beats_per_group"].items()), "| missing", R["missing_groups"] or "none")
    p("PER SECTION", " ".join(f"{k}={v}" for k, v in R["beats_per_section"].items()))
    p("FRAMES", R["first_frame"], "-", R["last_frame"], "| holes", R["holes"] or "none", "| double", R["double_frames"] or "none")
    p("COVERAGE", R["coverage_total"], "% |", " ".join(f"{k} {v['coverage']}% (target {v['target']}, {'ok' if v['ok'] else 'OFF'}) plain>{v['limit']}f: {v['plain_over_limit'] or 'none'}" for k, v in R["parts"].items()))
    for k in ("body_plain_over_360", "visuals_over_360_check_inside", "visuals_under_24f", "overlaps", "seams",
              "slivers", "plain_slivers_between_visuals", "ends_just_past_cut_info", "starts_off_word",
              "starts_near_word_ok", "edges_inside_a_word", "section_starts_without_beat_edge", "sec_code_mismatch",
              "sents_outside_beat", "same_construct_in_a_row", "duplicate_ids", "schema", "capture_ids_unknown"):
        v = R[k]
        p(k.upper(), f"({len(v)})", "; ".join(v) if v else "none")
    p("ASSETS", R["asset_status"], "| capture ids used", R["capture_ids_used"])


if __name__ == "__main__":
    main()
