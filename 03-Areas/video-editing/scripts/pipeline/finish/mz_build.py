# Build and check the A-roll MagicZoom plan (mz.json, mz_notes.md) for install_v2x --mz from a zones file, the manifests, the cut's V1 items and the cut's words; exit 0 only when every check passes.
# usage: python mz_build.py --zones <zones.json> --items <cut_items.json> --words <cut_words.json> --len <timeline frames> --out <dir> [--job <job folder> | --comps <comps dir>] [--list <list.txt>] [--full IN-07,IN-08] [--v1-count 159] [--check]    (file only, no Resolve)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
r"""mz_build.py - A-roll MagicZoom plan for install_v2x --mz (editor-builder, video 4 stage 5 JOB B, 2026-10-29).
Files only: reads the manifests, the cut's V1 items and cut_words.json; writes mz.json + mz_notes.md into --out.
    python mz_build.py ...           build + check (exit 0 only when every check passes)
    python mz_build.py ... --check   check the existing <out>\mz.json against the CURRENT manifests (run after any fix round)
    add --list <list.txt> to read only the manifests the install will place (default: every <comps>\*\manifest.json)
--zones <zones.json>: the hand-written zone plan, a JSON list of [start, end (exclusive), mode, depth, stressed word, why]; modes
zoom_hold | standard | punch | mirror. (Video 4's plan lived as the Z list inside this script; its mz.json holds the same zones.)
Rules: runbook 7, DECISIONS 9-11, bible 03 (c), review card S4/S6/S2, Samuel's 6465 marker (video 2: "this doesn't smoothly").
"""
import argparse, json, glob, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True

ap = argparse.ArgumentParser(description="Build and check the A-roll MagicZoom plan (mz.json) for install_v2x --mz.")
ap.add_argument("--zones", required=True, help="zones json: [[start, end, mode, depth, word, why], ...]")
ap.add_argument("--items", required=True, help="the cut's items json (cut_v5_items_*.json): V1 cuts")
ap.add_argument("--words", required=True, help="the cut's words json (cut_words.json): {w, f, e} per word")
ap.add_argument("--len", type=int, required=True, help="timeline length in frames (video 4: 12100)")
ap.add_argument("--out", required=True, help="folder for mz.json and mz_notes.md (and the mz.json --check reads)")
ap.add_argument("--job", help="job folder (gives the default --comps)")
ap.add_argument("--comps", help="comps dir with <beat>\\manifest.json (default <job>\\Graphics\\Frontal kit (Editor)\\comps\\v1)")
ap.add_argument("--list", help="read only the manifests named in this install list file")
ap.add_argument("--check", action="store_true", help="check the existing mz.json against the current manifests; write nothing")
ap.add_argument("--full", default="", help="comma list of full-frame adj beats with their own push: no MagicZoom under them (video 4: IN-07,IN-08,T1B-08)")
ap.add_argument("--v1-count", type=int, default=None, help="expected number of V1 items in --items (video 4: 159); not checked when omitted")
ap.add_argument("--center", default="0.507,0.62", help="zone pivot x,y (default 0.507,0.62, the A-roll face position)")
args = ap.parse_args()
if not (args.job or args.comps):
    ap.error("give --job or --comps")
K = os.path.join(os.path.abspath(args.job), "Graphics", "Frontal kit (Editor)") if args.job else None
COMPS = os.path.abspath(args.comps) if args.comps else os.path.join(K, "comps", "v1")
OUTD = os.path.abspath(args.out)
ITEMS, WORDS = args.items, args.words
LEN, CENTER, RAMP = args.len, [float(x) for x in args.center.split(",")], 24      # Speed 2 -> 1 s ramp on Types 1-3 (bible 03 c)
MODES = {"zoom_hold": 0.071, "standard": 0.071, "punch": 0.111, "mirror": 0.071}   # = kits\install_v2x.py MODES
FULL = {x for x in args.full.split(",") if x}   # adj comps that are full-frame graphics with their own push: no MZ (DECISIONS 9, plan v2)
V1COUNT = args.v1_count
# start, end (exclusive), mode, depth, stressed word, why
Z = [tuple(z) for z in json.load(open(args.zones, encoding="utf-8"))]


def load():
    ops = []
    ms = sorted(glob.glob(os.path.join(COMPS, "*", "manifest.json")))
    if args.list:                                                                    # restrict to the install list.txt
        lf = args.list; t = open(lf, encoding="utf-8").read().strip()
        ms = json.loads(t) if t.startswith("[") else [l.strip().strip('"') for l in t.splitlines() if l.strip()]
    for m in ms:
        f = os.path.basename(os.path.dirname(m))
        for o in json.load(open(m, encoding="utf-8")):
            ops.append(dict(o, folder=f, a=int(o["start"]), b=int(o["start"]) + int(o["D"]), track=int(o["track"])))
    v1 = [x for x in json.load(open(ITEMS, encoding="utf-8")) if x[0] == "video" and x[1] == 1]
    words = json.load(open(WORDS, encoding="utf-8"))
    return ops, v1, words


def plain(ops):
    blk = [o for o in ops if o["track"] == 2 or not (o["op"] == "comp" and o.get("adj")) or o["folder"] in FULL]
    mer = []
    for a, b in sorted((o["a"], o["b"]) for o in blk):
        if mer and a <= mer[-1][1]: mer[-1][1] = max(mer[-1][1], b)
        else: mer.append([a, b])
    free, t = [], 0
    for a, b in mer + [[LEN, LEN]]:
        if a > t: free.append((t, a))
        t = max(t, b)
    return free, blk


def check(plan, ops, v1, words):
    bad, warn = [], []
    cuts = {x[2] for x in v1} | {LEN}
    free, blk = plain(ops)
    starts_blk = {o["a"] for o in blk}
    adjs = {(o["track"], o["a"]) for o in ops if o["op"] == "comp" and o.get("adj")}
    if (V1COUNT is not None and len(v1) != V1COUNT) or max(x[3] for x in v1) != LEN: bad.append("V1 not %s/%d" % (V1COUNT if V1COUNT is not None else "n", LEN))
    P = sorted(plan, key=lambda z: z["start"])
    for i, z in enumerate(P):
        a, b, m = z["start"], z["end"], z["mode"]
        if m not in MODES: bad.append(("mode", a, m))
        if b - a < 24: bad.append(("short <24", a, b))
        if m == "punch" and not 25 <= b - a <= 45: bad.append(("punch length", a, b))
        if a < 28: bad.append(("in 0-28 (S6)", a))
        hit = [(o["folder"], o["track"], o["a"], o["b"]) for o in ops if o["a"] < b and o["b"] > a
               and not (o["track"] >= 3 and (o["track"], o["a"]) in adjs)]            # = install_v2x build() hit test
        if hit: bad.append(("over a visual", a, b, hit[:3]))
        full = [o["folder"] for o in ops if o["folder"] in FULL and o["a"] < b and o["b"] > a]
        if full: bad.append(("under a full-frame graphic", a, b, full))
        if i and P[i - 1]["end"] > a: bad.append(("zones overlap", P[i - 1]["start"], a))
        nxt = P[i + 1]["start"] if i + 1 < len(P) else None
        if b != LEN and b not in starts_blk:                                           # a zone end must hide or hand over on a cut
            if not (b in cuts and nxt == b) and m != "mirror": bad.append(("zoom jumps at end", a, b))
            if b in cuts and nxt != b and m != "mirror": bad.append(("ends on a cut onto unzoomed A-roll: mirror needed", a, b))
        if nxt == b and b not in cuts: bad.append(("abutting zones mid-shot", b))
        for x in (a, b):
            w = [w["w"] for w in words if w["f"] < x < w["e"]]
            if w and x not in starts_blk and not any(o["b"] == x for o in blk): bad.append(("mid-word", x, w))
            elif w: warn.append("boundary %d inside '%s' = a visual's own cut frame (fixed by the visual; the zoom starts at 1.00 there or is hidden by the full-frame cut-in)" % (x, w[0]))
        if m == "punch" and i and P[i - 1]["mode"] == "punch": bad.append(("two punches in a row", P[i - 1]["start"], a))
        sw = [w for w in words if a <= w["f"] < b and w["w"].strip(".,?!'\"").lower().startswith(z["word"].lower())]
        if not sw: bad.append(("stressed word not in zone", a, z["word"]))
        elif m in ("punch", "zoom_hold") and not any(w["f"] <= a + RAMP + 8 for w in sw): warn.append("%d '%s' lands after the ramp" % (a, z["word"]))
        z["word_f"] = sw[0]["f"] if sw else None
    vis = sorted([(o["a"], o["b"]) for o in ops if o["track"] >= 2] + [(z["start"], z["end"]) for z in P])
    e, gaps = None, []
    for a, b in vis:                                                                    # = install_v2x verify() sliver-gap test
        if e is not None and 0 < a - e < 6: gaps.append((e, a))
        e = b if e is None else max(e, b)
    if gaps: bad.append(("sliver gaps <6 f", gaps[:5]))
    pf = sum(b - a for a, b in free)
    cov = sum(max(0, min(b, z["end"]) - max(a, z["start"])) for a, b in free for z in P)
    left = [(a, b) for a, b in free if not any(z["start"] < b and z["end"] > a for z in P)]
    big_left = [x for x in left if x[1] - x[0] >= 24]
    if big_left: bad.append(("plain stretch >= 24 f with no zone (S4)", big_left))
    if pf and cov / pf < .75: bad.append(("coverage < 75 %", round(100 * cov / pf, 1)))
    np_ = sum(z["mode"] == "punch" for z in P)
    if np_ * 4 > len(P): bad.append(("punches > 1 in 4", np_, len(P)))
    from collections import Counter
    stats = dict(zones=len(P), plain_frames=pf, covered=cov, pct=round(100 * cov / pf, 1) if pf else 0,
                 styles=dict(Counter("%s %.3f" % (z["mode"], z["depth"]) for z in P)), unzoned=left, stretches=len(free))
    return bad, warn, stats


def main():
    ops, v1, words = load()
    out = os.path.join(OUTD, "mz.json")
    if args.check:
        plan = [dict(z, word=z.get("word", "")) for z in json.load(open(out, encoding="utf-8"))]
        meta = {z[0]: z for z in Z}
        for z in plan: z["word"] = meta.get(z["start"], (0, 0, 0, 0, ""))[4]
    else:
        plan = [dict(start=a, end=b, mode=m, depth=d, center=CENTER, word=w, why=y) for a, b, m, d, w, y in Z]
    bad, warn, st = check(plan, ops, v1, words)
    print("stretches", st["stretches"], "| zones", st["zones"], "| plain", st["plain_frames"], "f, covered", st["covered"], "f =", st["pct"], "%")
    print("styles", st["styles"]); print("unzoned plain", st["unzoned"])
    for w in warn: print("note:", w)
    for b in bad: print("FAIL:", b)
    if not args.check:
        os.makedirs(OUTD, exist_ok=True)
        json.dump([dict(start=z["start"], end=z["end"], mode=z["mode"], depth=z["depth"], center=z["center"]) for z in plan],
                  open(out, "w", encoding="utf-8"), indent=1)
        L = ["# mz_notes - A-roll MagicZoom plan (pipeline\\finish\\mz_build.py)", "",
             "File: `mz.json` (%d zones, end exclusive, pivot (%s, %s) on every zone, V2, MotionBlur 0 via mz_inject). Made and checked by `mz_build.py`; re-run `python mz_build.py ... --check` after the fix round, because it reads the manifests as they are now." % (len(plan), CENTER[0], CENTER[1]),
             "Coverage: %d of %d plain A-roll frames = %s %% (target >= 75 %%). Styles: %s. Not zoned: %s (each < 24 f)." % (st["covered"], st["plain_frames"], st["pct"], ", ".join("%s x%d" % kv for kv in sorted(st["styles"].items())), ", ".join("%d-%d" % x for x in st["unzoned"])),
             "Not under MagicZoom by rule: %s (full-frame adj graphics with their own push; DECISIONS 9, plan v2)." % (", ".join("%s %d-%d" % (f, min(o["a"] for o in ops if o["folder"] == f), max(o["b"] for o in ops if o["folder"] == f)) for f in sorted(FULL) if any(o["folder"] == f for o in ops)) or "none"),
             "Zone ends: every zone ends where a full-frame visual cuts in, at the timeline end, or on a V1 jump cut where the next zone starts. No zone ends on a cut onto unzoomed A-roll, so no mirror is needed (video 2's short mirrors bounced: fix_report_S4). Where an overlay is held across a jump cut or comes in on one, one zone crosses the cut so Alex never steps under the text (Samuel's 6465 marker).", "",
             "| frames | D | mode | depth | lands on | why |", "|---|---|---|---|---|---|"]
        for z in plan:
            L.append("| %d-%d | %d | %s | %.3f | '%s' %s | %s |" % (z["start"], z["end"], z["end"] - z["start"], z["mode"], z["depth"], z["word"], z.get("word_f"), z["why"]))
        L += ["", "## Open for the Editor",
              "- Run `python mz_build.py ... --check --list <list.txt>` before the install and after any fix round. A moved manifest edge fails it with a frame number.",
              "- Not proven in Resolve. install_v2x's verify is the proof (MZ placed, no overlaps/slivers/gaps, V1 count / length)."]
        open(os.path.join(OUTD, "mz_notes.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
        print("wrote", out, "and mz_notes.md")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
