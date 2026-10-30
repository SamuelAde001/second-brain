# Reads every visual event (pop, reveal, count, cut-in, click ...) of an installed timeline, in timeline frames, from the manifests and .setting files.
# Usage: python sfx_events.py --list <install list.txt> [--out sfx_events.json]
# Promoted from video 4 on 2026-10-30.
"""Visual events of a timeline in timeline frames, read offline from the installed manifests and their
Fusion .setting files (editor-builder, 2026-10-24). Re-runnable: a fix round changes beats, so run it again after
any manifest or comp change, then sound_plan.py. Touches nothing but its own output.

python sfx_events.py --list <install list.txt> [--out sfx_events.json]   (default --out: beside the list)

Parsing reuses LinkedIn's comp_events.py (job 3, Graphics/Visuals v1/sound), extended for the Frontal kit:
- NeoAnim macro: the GlobalAnim expression is progress = clamp((time - InOffset) / InLength), Expo ease-out, so the element
  starts moving at comp frame InOffset (no stored InOffset = the macro default, frame 0) and lands ~InLength later (most of
  the move is in the first third). Comp frame 0 = the clip's first frame, so timeline frame = op start + comp frame.
  Out = 1 -> exit over OutLength f ending OutOffset f before the clip's last frame (comp.RenderEnd = D - 1).
- Fuse.NeoMotionText: InOffsetF (word by word from there).
- BezierSpline-driven inputs, one event per run of changing keys (dense linear keys = one run): opacity fades
  (BrightnessContrast Alpha + Gain), lights / undims, spotlights, highlighters (Merge Multiply blend, wipes, words brighten),
  MosaicBlur Blend 1 -> 0, PolylineMask WriteLength (arrows, chart lines, rings), RectangleMask Width/Height growing from ~0
  (bars, chart grids, connectors, strikes), Text+ Counter (with the $ flag), Transform Size / XYPath moves (slides, A-roll
  slide-up, card moves, punches, scrolls), EllipseMask opens (circle transitions), GaussianBlur sharpening.
  Not events: shines / light sweeps / bevels, slow pushes and creeps, dims, grades, backdrops, down fades, fade-outs.
- V2 ops: the cut-in (from A-roll, or a montage cut from another V2 clip); move=True when the V3 adj at the same start has an
  entrance NeoAnim at comp frame 0-2. Held stills that continue the previous visual are not cuts.
- .mov page/app renders: the beat folder's NOTE.md timing table when it has one (src='note', lower confidence).
PassThrough tools are skipped. Events on the same element (op + element name) closer than 3 f are merged.
Kinds: pop reveal text highlight light focus draw count whoosh scroll cutin exit type click."""
import argparse, json, os, re, sys, collections, datetime

ap = argparse.ArgumentParser(description="Visual events of a timeline in timeline frames, read from the install list's manifests and Fusion .setting files.")
ap.add_argument("--list", required=True, help="install list: one manifest.json path per line")
ap.add_argument("--out", help="output json (default: sfx_events.json beside the list)")
_a = ap.parse_args()
LIST = _a.list
OUT = _a.out or os.path.join(os.path.dirname(os.path.abspath(LIST)), "sfx_events.json")
TOP = re.compile(r"\n\t\t(\w+) = ([\w.]+) \{")
NUM = r"-?\d+(?:\.\d+)?(?:e-?\d+)?"
PRIO = {"cutin": 9, "whoosh": 8, "reveal": 7, "count": 6, "draw": 6, "highlight": 5, "pop": 5, "click": 5, "type": 5,
        "text": 4, "light": 4, "focus": 3, "scroll": 3, "exit": 2}


def keys_of(blk):
    m = re.search(r"KeyFrames = \{", blk)
    if not m:
        return []
    return [(float(k.group(1)), float(k.group(2))) for k in re.finditer(r"\[(%s)\] = \{ (%s)" % (NUM, NUM), blk[m.end():])]


def runs(ks):
    """Runs of consecutive changing keys in one direction: [(t0, v0, t1, v1)]."""
    out, cur = [], None
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if abs(v1 - v0) < 1e-6:
            if cur:
                out.append(cur); cur = None
            continue
        d = v1 > v0
        if cur and cur[4] == d and abs(cur[2] - t0) < 1e-6:
            cur = (cur[0], cur[1], t1, v1, d)
        else:
            if cur:
                out.append(cur)
            cur = (t0, v0, t1, v1, d)
    if cur:
        out.append(cur)
    return [r[:4] for r in out]


def inp(blk, name):
    m = re.search(r"\n\t+%s = Input \{ Value = (%s)" % (re.escape(name), NUM), blk)
    return float(m.group(1)) if m else None


def styled(blk):
    m = re.search(r'\n\t+StyledText = Input \{ Value = "((?:[^"\\]|\\.)*)"', blk)
    return m.group(1) if m else ""


PREF = re.compile(r"^(NeoAnim|BrightnessContrast|Transform|Rectangle|XYPath|Merge|MosaicBlur|Text|Polyline|Ellipse|GaussianBlur|"
                  r"Dissolve|Background|Publish)_")
SUFF = re.compile(r"(HeadSize|Head|DotGate|LineGate|AreaGate|AreaWipe|Gate|Wipe|Size|Center|Multiply|Fade|Dim|Counter|Count|"
                  r"Scale|Grow|In|On|Op|Lit)$")


def elem(n):
    k = PREF.sub("", n)
    for _ in range(3):
        k2 = SUFF.sub("", k)
        if k2 == k or not k2:
            break
        k = k2
    return k


def group(n):
    return re.sub(r"\d+", "#", elem(n))


SKIP_ANY = re.compile(r"Shine|Sweep|Bevel")


def classify(tt, iname, n, v0, v1, dur, alpha, cont=False):
    """(kind, what) or None for one run of a spline-driven input."""
    if SKIP_ANY.search(n):
        return None
    up = v1 > v0
    if tt == "BrightnessContrast":
        if iname == "Blend":
            if not up:
                return None
            if "Spotlight" in n:
                return ("focus", "spotlight")
            if "WordsBr" in n:
                return ("highlight", "words brighten")
            return None                                   # StatDark, Desat, Negative, Dark L/R: grades and backdrops
        if iname != "Gain":
            return None                                   # Saturation moves with its Gain twin
        if alpha:
            if not up:
                return ("reveal", "mosaic fades off") if "Mos" in n and v1 < 0.2 else None
            if v0 > 0.05 and v1 - v0 < 0.4:
                return None
            if re.search(r"DownFade|Ground|PageBg|PageDark|Bloom|Edge|Tip|Gate|Mosaic|Treat|Dark", n):
                return None
            if re.search(r"Glow|Pulse|Ring|Accent|Lit|Lift|Clear", n):
                return ("light", "lights up")
            if re.search(r"Title|Label|Text|Num|Count|Months|Name|Word|Caption|Line|Kicker", n):
                return ("text", "text fades in")
            return ("pop", "fades in")
        if up and v1 - v0 >= 0.15 and v0 >= 0.2 and not re.search(r"Page|Ground", n):
            return ("light", "lit (undimmed)")
        return None
    if tt == "Merge" and iname == "Blend":
        if not up or re.search(r"Negative|Phrase|Gray|Grey", n):
            return None
        if re.search(r"Hi[A-Z#\d]|Highlight", n):
            return ("highlight", "highlighter")
        if re.search(r"Knob|Toggle", n):
            return ("click", "toggle switches")
        return ("pop", "fades in")
    if tt == "MosaicBlur" and iname == "Blend":
        return ("reveal", "mosaic off") if not up and v1 < 0.2 else None
    if tt == "PolylineMask" and iname == "WriteLength":
        if not up or v0 >= 0.5:
            return None
        if "Arrow" in n:
            return ("draw", "arrow draws")
        if re.search(r"Ring|Pulse", n):
            return ("highlight", "ring draws")
        return ("draw", "line draws")
    if tt == "RectangleMask" and iname in ("Width", "Height"):
        grows_on = cont and v1 - v0 >= 0.1 and re.search(r"Wipe|Fill|Grow", n)     # a wipe that resumes after a hold
        if not up or (v0 > 0.3 * v1 and not grows_on) or v1 < 0.02:
            return None
        if re.search(r"Highlight|Strike|Underline", n):
            return ("highlight", "highlighter wipe" if "Strike" not in n else "strike-through")
        if "AreaWipe" in n:
            return ("draw", "line draws")
        if re.search(r"Grid|Base", n):
            return ("draw", "chart builds")
        if re.search(r"Fill|Grow|Stretch", n):
            return ("draw", "bar grows")
        if "Conn" in n:
            return ("draw", "connector draws")
        if "LineReveal" in n:
            return ("text", "line reveals")
        if "Wipe" in n:
            return ("draw", "wipe reveals")
        return None
    if tt == "EllipseMask" and iname in ("Width", "Height"):
        return ("whoosh", "circle opens") if up and v0 < 0.3 * v1 else None
    if tt == "GaussianBlur" and iname in ("HStrength", "XBlurSize", "BlurSize"):
        return ("reveal", "sharpens") if not up and v0 > 0.02 and v1 < 0.01 else None
    if tt == "Transform" and iname == "Size":
        if re.search(r"HeadSize|Count|Num|Scale|Push|Creep|Cont", n) or v0 <= 0:
            return None
        r = v1 / v0 - 1.0
        if v0 <= 0.7 * v1 and dur <= 12:
            return ("pop", "scales in")
        if abs(r) >= 0.15 and dur <= 30:
            return ("whoosh", "moves (size %.2f->%.2f)" % (v0, v1))
        if abs(r) >= 0.06 and dur <= 20:
            return ("whoosh", "punch / quick zoom")
        return None
    if tt == "XYPath" and iname in ("X", "Y"):
        if re.search(r"Hit|Spotlight|Zoom|Hi[A-Z#\d]|Wipe|Tip|Grow|LineReveal|Strike", n):
            return None
        if abs(v1 - v0) < 0.1:
            return None
        return ("whoosh", "slides") if dur <= 30 else ("scroll", "scrolls")
    return None


def note_events(note, a, b):
    """Rows of a NOTE.md timing table inside [a, b): [(f, f2, kind, what)]."""
    if not os.path.exists(note):
        return []
    s = open(note, encoding="utf-8", errors="replace").read()
    out, on = [], False
    for line in s.splitlines():
        if line.startswith("#"):
            on = bool(re.search(r"Timing|frames", line))
            continue
        if not on:
            continue
        m = re.match(r"\| *(\d{3,5})(?: *[-–] *(\d{3,5}))?[^|]*\| *([^|]*)\|", line)
        if not m:
            continue
        f, f2, what = int(m.group(1)), int(m.group(2) or 0), m.group(3).strip()
        if not a <= f < b:
            continue
        w = what.lower()
        if re.search(r"\bcut\b|neoanim", w):
            continue
        if re.search(r"typ(ed|ing|es)", w):
            k = "type"
        elif re.search(r"highlight|\blit\b|underline|marker", w):
            k = "highlight"
        elif "spotlight" in w:
            k = "focus"
        elif re.search(r"tick", w):
            k = "pop"
        elif re.search(r"count|0 ?-> ?\d", w):
            k = "count"
        elif "click" in w:
            k = "click"
        elif re.search(r"stream|fetched|block|result|card|appears|lands|fades in|rows", w):
            k = "pop"
        else:
            continue
        out.append((f, f2 if f2 > f else 0, k, what[:60]))
    return out


# ------------------------------------------------------------------------------------------------ read the manifests
lst = [l.strip() for l in open(LIST, encoding="utf-8") if l.strip()]
ops, missing = [], []
for i, p in enumerate(lst):
    if not os.path.exists(p):
        missing.append(p); continue
    beat = os.path.basename(os.path.dirname(p))
    for j, o in enumerate(json.load(open(p, encoding="utf-8"))):
        o = dict(o)
        o["beat"], o["id"], o["manifest"] = beat, "%s#%d" % (beat, j), p
        ops.append(o)
ops.sort(key=lambda o: (o["start"], o["track"]))

events, skipped = [], collections.Counter()


def add(o, kind, cf, tool, what, **x):
    if -12 < cf < 0:          # 2026-10-25: an entrance started before its clip (negative InOffset, e.g. P3-05c) sounds on the clip's first frame
        cf = 0
    if 0 <= cf < o["D"]:
        e = dict(f=int(round(o["start"] + cf)), kind=kind, beat=o["beat"], op=o["id"], track=o["track"], tool=tool,
                 elem=elem(tool), group=group(tool), what=what, cf=round(cf, 1))
        e.update(x)
        events.append(e)


entr = {}          # op start -> entrance NeoAnim comp frame (adj comps on V3+)
for o in ops:
    if o["op"] != "comp":
        continue
    sp = o.get("setting") or ""
    if not os.path.exists(sp):
        missing.append(sp); continue
    s = open(sp, encoding="utf-8", errors="replace").read()
    tops = [(m.start(), m.group(1), m.group(2)) for m in TOP.finditer(s)]
    blocks = {n: (t, s[pp: tops[k + 1][0] if k + 1 < len(tops) else len(s)]) for k, (pp, n, t) in enumerate(tops)}
    passthru = {n for n, (t, blk) in blocks.items() if re.search(r"\n\t\t\tPassThrough = true", blk)}
    skipped["passthrough tools"] += len(passthru)
    D = o["D"]
    for n, (t, blk) in blocks.items():
        if n in passthru:
            continue
        if t == "MacroOperator" and n.startswith("NeoAnim"):
            io = inp(blk, "InOffset")
            io = 0.0 if io is None else io
            il = inp(blk, "InLength") or 20.0
            if inp(blk, "In") != 0:
                if "Entrance" in n or (o.get("adj") and n == "NeoAnim"):
                    if io <= 2:
                        entr[o["start"]] = io
                    add(o, "whoosh" if io > 2 else "cutin", io, n, "full-frame entrance %d f" % il, land=round(o["start"] + io + il),
                        move=True, entrance=True)
                else:
                    kind = "text" if re.search(r"Title|Ttl|Head|Name|Caption|Cap\d|Text|Label|Kicker|Line|Word", n) else "pop"
                    add(o, kind, io, n, "enters (NeoAnim %d f)" % il, land=round(o["start"] + io + il))
            if inp(blk, "Out") == 1 and inp(blk, "OutLength"):
                ol, oo = inp(blk, "OutLength"), inp(blk, "OutOffset") or 0.0
                xs = (D - 1 - oo) - ol
                if xs >= 0:
                    add(o, "exit", xs, n, "exits (NeoAnim out %d f)" % ol, end_cut=(oo <= 1))
        elif t == "Fuse.NeoMotionText":
            io = inp(blk, "InOffsetF")
            if io is not None:
                tx = styled(blk)
                add(o, "text", io, n, "text in: " + tx[:40].replace("\\n", " "), money="$" in tx)
        elif t == "TextPlus":
            m = re.search(r'Expression = "[^"]*\(time ?- ?(%s)\) ?/ ?(%s)' % (NUM, NUM), blk)
            if m:
                add(o, "count", float(m.group(1)), n, "counter (expression)", dur=float(m.group(2)), money="$" in blk)
    # a list item lit by contrast: two or more siblings (I2Dim, I3Dim ...) dim on the same frame, the one left out stays lit
    dims = collections.defaultdict(set)
    for n, (t, blk) in blocks.items():
        md = re.match(r"BrightnessContrast_([A-Za-z]+)(\d+)Dim$", n)
        if not md or n in passthru:
            continue
        sm = re.search(r'\n\t+Gain = Input \{\s*SourceOp = "(\w+)"', blk)
        if sm and sm.group(1) in blocks:
            for (t0, v0, t1, v1) in runs(keys_of(blocks[sm.group(1)][1])):
                if v1 < v0:
                    dims[(md.group(1), t0)].add(int(md.group(2)))
    for (pf, t0), dimmed in dims.items():
        if len(dimmed) < 2:
            continue
        idx = {int(x) for x in re.findall(r"\n\t\t\w*?_%s(\d+)(?=[A-Z_]| =)" % pf, s)}
        lit = sorted(idx - dimmed)
        if lit:
            add(o, "reveal", t0, "Lit_%s%d" % (pf, lit[0]), "list item %s%d lit (others dim)" % (pf, lit[0]))
    # spline-driven inputs
    for n, (t, blk) in blocks.items():
        if n in passthru:
            continue
        tt = t.split(".")[-1]
        alpha = bool(re.search(r"\n\t+Alpha = Input \{ Value = 1", blk))
        for m in re.finditer(r'\n\t+(\w+) = Input \{\s*SourceOp = "(\w+)",\s*Source = "Value"', blk):
            iname, sp_name = m.group(1), m.group(2)
            if sp_name not in blocks or blocks[sp_name][0] != "BezierSpline":
                continue
            for ri, (t0, v0, t1, v1) in enumerate(runs(keys_of(blocks[sp_name][1]))):
                if tt == "TextPlus" and iname == "Counter":
                    if v1 > v0:
                        tx = styled(blk)
                        add(o, "count", t0, n, "counts %g -> %g" % (v0, v1), dur=round(t1 - t0, 1),
                            money="$" in blk, to=v1)
                    continue
                c = classify(tt, iname, n, v0, v1, t1 - t0, alpha, cont=ri > 0)
                if c:
                    add(o, c[0], t0, n, c[1], dur=round(t1 - t0, 1))
                elif tt in ("BrightnessContrast", "Merge", "Transform", "XYPath", "RectangleMask"):
                    skipped["not an event: %s.%s" % (tt, iname)] += 1

# ------------------------------------------------------------------------------------------------ cuts into V2
v2 = [o for o in ops if o["track"] == 2]
HELD = re.compile(r"held|hold|continu|last frame|same scene|no second entrance|landed state|reprise of the same", re.I)
for o in v2:
    prev = [p for p in v2 if p is not o and abs(p["start"] + p["D"] - o["start"]) <= 1]
    why = o.get("why", "")
    fake = {"start": o["start"], "D": max(o["D"], 1), "beat": o["beat"], "id": o["id"], "track": 2}
    nm = os.path.basename(o.get("path") or o.get("setting") or "")
    if prev:
        if HELD.search(why) and not re.search(r"hard cut", why, re.I):
            skipped["V2 junction held (no cut)"] += 1
            continue
        mv = o["start"] in entr
        add(fake, "cutin", 0, "Cut_" + nm[:24], "montage cut to " + nm[:30], move=mv, montage=True)
    else:
        mv = o["start"] in entr
        add(fake, "cutin", 0, "Cut_" + nm[:24], "cut in from A-roll: " + nm[:30], move=mv, montage=False,
            media=(o["op"] == "media"))

# ------------------------------------------------------------------------------------------------ inside .mov renders
for o in ops:
    if o["op"] == "media" and str(o.get("path", "")).lower().endswith(".mov"):
        for f, f2, k, what in note_events(os.path.join(os.path.dirname(o["manifest"]), "NOTE.md"), o["start"], o["start"] + o["D"]):
            fake = {"start": o["start"], "D": o["D"], "beat": o["beat"], "id": o["id"], "track": 2}
            x = {"src": "note"}
            if k in ("type", "count"):
                x["dur"] = (f2 - f) if f2 else 24
            add(fake, k, f - o["start"], "Note_%s_%d" % (k, f), what, **x)
        # the render's build record (CL-03 style: typing_end, question_hl)
        for bj in sorted(os.listdir(os.path.dirname(o["manifest"]))):
            if not (bj.startswith("build_") and bj.endswith(".json")):
                continue
            try:
                j = json.load(open(os.path.join(os.path.dirname(o["manifest"]), bj), encoding="utf-8"))
            except Exception:
                continue
            for x in (j if isinstance(j, list) else [j]):
                if not (isinstance(x, dict) and os.path.normcase(str(x.get("mov", ""))) == os.path.normcase(o["path"])):
                    continue
                fake = {"start": o["start"], "D": o["D"], "beat": o["beat"], "id": o["id"], "track": 2}
                if x.get("typing_end"):
                    add(fake, "type", 0, "Build_type", "typed on his voice (%s)" % bj, dur=int(x["typing_end"]) - o["start"], src="build")
                if isinstance(x.get("question_hl"), list) and x["question_hl"]:
                    add(fake, "highlight", int(x["question_hl"][0]) - o["start"], "Build_hl", "highlight at once (%s)" % bj, src="build")

# ------------------------------------------------------------------------------------------------ merge same element < 3 f
events.sort(key=lambda e: (e["op"], e["elem"], e["f"]))
merged = []
for e in events:
    last = merged[-1] if merged else None
    if last and last["op"] == e["op"] and last["elem"] == e["elem"] and e["f"] - last["f"] < 3:
        if PRIO.get(e["kind"], 0) > PRIO.get(last["kind"], 0):
            e2 = dict(e); e2["f"] = min(e["f"], last["f"]); merged[-1] = e2
        skipped["merged (same element < 3 f)"] += 1
        continue
    merged.append(e)
merged.sort(key=lambda e: (e["f"], -PRIO.get(e["kind"], 0)))

json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"), "list": LIST, "missing": missing,
           "ops": [{k: o.get(k) for k in ("id", "beat", "op", "track", "start", "D", "adj")} |
                   {"name": os.path.basename(o.get("setting") or o.get("path") or ""), "why": (o.get("why") or "")[:160]} for o in ops],
           "events": merged, "skipped": dict(skipped)},
          open(OUT, "w", encoding="utf-8"), indent=0, ensure_ascii=False)
pre = collections.Counter(re.match(r"[A-Z]+\d?", e["beat"]).group(0) for e in merged)
print("manifests", len(lst), "ops", len(ops), "missing", len(missing), "events", len(merged), "->", OUT)
print("kinds", dict(collections.Counter(e["kind"] for e in merged)))
print("by prefix", dict(pre))
print("skipped", dict(skipped))
