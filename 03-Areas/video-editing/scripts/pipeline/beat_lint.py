r"""beat_lint.py - scripted lint of built beats against Samuel's review card, before any reviewer (Editor, 2026-10-28).
No AI, no Resolve. Reads each beat's manifest (its comp ops), the .setting files and the job's word timings.

  python beat_lint.py --words <words_cut.json> [--beats <beats.json>] [--section <sec>] [--out <report.json>]
                      <manifest.json | beat folder | comps folder> ...
  python beat_lint.py --words <w.json> --setting <comp.setting> --start <timeline f> --D <n> [--beat ID] [--over aroll]
  python beat_lint.py --why <report.json> <BEAT>          print one beat's findings (for the worker that fixes it)

Prints one line per beat (ok / FAIL per rule) and the counts; the details go to the report json. Exit 1 on any FAIL.
Frames: manifest `start` and the words' `f`/`e` are timeline frames of the cut (23.976); comp frames are 0..D-1.

Rules (review card, 03-Areas/video-editing/samuel-review-card.md; thresholds from video 4's Docs\CD rules from video 2):
  P1  every element enters on its word: readable frame (entry + 25 % of its length, Expo ease-out ~82 %) lands
      0-3 f after the word's onset (+-TOL for Whisper timing), never before it; no two elements enter on the same frame.
      Elements = NeoAnim (inner GlobalAnim InOffset/InLength), NeoMotionText (InOffsetF/InLengthF), counters
      (Text+ with a Counter spline), fades (a Blend/Gain/Alpha spline rising from 0). An element's word = the first
      word of its text heard in the beat, or a cue: manifest op "cues": {"<tool>": "<word>"}. No text, no cue = unmatched
      (counted, not failed).
  P2  a hero number (a text that is only a number: $1M, 40%, 10,000) is a counter; a counter is not inside a sentence
      (no other text on its line). Integers 1-9 with no unit are ordinals and skipped.
  P3  every NeoMotionText has PosDir 0 (Up) and word Scope (1); a static Text+ of 3+ words at headline size (>= 56 px)
      is a fail (main text goes word by word).
  P5  no strike line: a tool named strike/cancel/crossout/xout, or a thin red bar across the middle of a text.
  C3  the last element is fully landed >= 36 f (1.5 s) before the cut (comp end, or the start of an exit animator).
      Reveals (wipes, line draws) and pushes are not elements: a chart line may grow until the cut by design.
  C6  over Alex (an adj comp or a comp with no ground of its own, no other op under it, not darkened): every text is
      a lower third, centred (|x - 960| <= 120 px) and low (centre y >= 900 px).
  C7  text height on the 1080 frame (Size x 1508 / font height, x downstream Transform/Merge Size): >= 56 px over
      footage, >= 40 px on a ground or a page, >= 36 px in a UI rebuild (beat kind ui-demo).
  C9  every number on screen is a number Alex says within the beat (+-1 s), from the word timings. Axis ticks (3+
      numeric texts in one name family) and ordinals are skipped; ui-demo beats are skipped.
Assumptions to know: px from Size uses the kit's font heights (Inter 1.210, JetBrains Mono 1.320, Season 1.229);
NeoMotionText per-word delay = DelaySec x fps; position/size follow the first downstream path only.
"""
import os, sys, re, json, glob, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fusion_setting as fs

FPS = 23.976
READ_FRAC = 0.25
TOL = (-1, 5)                 # P1 pass window for (readable - word onset): the rule's 0..3 f widened by Whisper's error
HOLD = 36                     # C3
HERO_PX = 72                  # P2: a number this big or bigger, said in the beat, is a hero number
LT_Y, LT_DX = 900, 120        # C6
MIN_PX = {"footage": 56, "ground": 40, "ui": 36}
FH = (("jetbrains", 1.320), ("season", 1.229), ("inter", 1.210))
RULES = ("P1", "P2", "P3", "P5", "C3", "C6", "C7", "C9")
STOP = set("a an the to of and in on for is it its it's that this you your with at by or be are was were we i my me "
           "so but if as from they them their our us he she his her do does did not no yes".split())
SCALE = {"k": 1e3, "thousand": 1e3, "m": 1e6, "mm": 1e6, "million": 1e6, "b": 1e9, "bn": 1e9, "billion": 1e9}
SPELL = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                    "fourteen fifteen sixteen seventeen eighteen nineteen".split())}
SPELL.update({w: 10 * (i + 2) for i, w in enumerate("twenty thirty forty fifty sixty seventy eighty ninety".split())})
NUM = re.compile(r"(?<![\w:.])([$€£])?\s?(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s?(%|x|k|mm|m|bn|b|million|billion|"
                 r"thousand)?(?![\w:])", re.I)


# ------------------------------------------------------------------------------------------------- words, numbers
def norm(w):
    return re.sub(r"[^\w$%.]", "", w.lower().replace("’", "'")).strip(".")


def screen_numbers(text):
    """'$1M a year, 40%' -> [(1000000.0, '$1M'), (40.0, '40%')]"""
    out = []
    for m in NUM.finditer(text or ""):
        cur, digits, unit = m.groups()
        v = float(digits.replace(",", ""))
        u = (unit or "").lower()
        v *= SCALE.get(u, 1)
        out.append((v, m.group(0).strip(), bool(cur), u))
    return out


def spoken_tokens(words):
    """word dicts -> [(first word, value)] for every number heard: '$1' 'million' -> 1e6, '10' ',000' -> 1e4 (Whisper
    splits thousands), 'ten thousand' -> 1e4, 'a hundred' -> 100, 'thirty-eight' -> 38, '40%' -> 40. The first word
    gets "_end" = the end frame of the number's last word."""
    toks = [(w, p) for w in words for p in w["w"].split("-")]
    out, st = [], {"cur": None, "w0": None, "wl": None}

    def flush():
        if st["cur"] is not None:
            out.append((st["w0"], st["cur"]))
            st["w0"]["_end"] = st["wl"]["e"]
        st.update(cur=None, w0=None, wl=None)

    def start(w, v):
        flush(); st.update(cur=float(v), w0=w, wl=w)

    for j, (w, raw) in enumerate(toks + [(None, "")]):
        t = norm(raw)
        nxt = norm(toks[j + 1][1]) if j + 1 < len(toks) else ""
        cur = st["cur"]
        if t in ("a", "one") and nxt in ("hundred", "thousand", "million", "billion"):
            start(w, 1.0); continue
        m3 = re.fullmatch(r",(\d{3})[.,%]?", raw.strip())
        if m3 and cur is not None:
            st.update(cur=cur * 1000 + int(m3.group(1)), wl=w); continue
        bare = t.replace("$", "").replace(",", "").rstrip("%")
        m = re.fullmatch(r"(\d+(?:\.\d+)?)(k|m|mm|b|bn|x)?", bare)
        if m:
            start(w, float(m.group(1)) * SCALE.get(m.group(2) or "", 1)); continue
        if t in SPELL:
            v = SPELL[t]
            if cur is not None and 20 <= cur < 100 and cur % 10 == 0 and v < 10:
                st.update(cur=cur + v, wl=w)                   # "twenty five"
            else:
                start(w, v)
            continue
        if t == "hundred" and cur is not None:
            st.update(cur=cur * 100, wl=w); continue
        if t in SCALE and cur is not None:
            out.append((st["w0"], cur)); st["w0"]["_end"] = st["wl"]["e"]     # "10" alone is heard too
            st.update(cur=cur * SCALE[t], wl=w); continue
        flush()
    return out


def spoken_numbers(words):
    return {v for w, v in spoken_tokens(words)}


def words_in(words, a, b):
    return [w for w in words if a <= w["f"] < b]


# --------------------------------------------------------------------------------------------------- comp model
def _graph(tools):
    """edges dst -> {src}, consumers src -> [(dst, input)] over top-level tools, plus the Note_Wiring links."""
    up, down = {}, {}

    def link(dst, k, s):
        if s in tools and s != dst and tools[s].type not in ("BezierSpline", "LUTBezier", "LUTLookup", "XYPath",
                                                            "PolyPath", "Note"):
            up.setdefault(dst, set()).add(s)
            down.setdefault(s, []).append((dst, k))

    for n, t in tools.items():
        for k, v in fs.inputs(t).items():
            if isinstance(v, fs.T) and v.get("SourceOp"):
                link(n, k, v["SourceOp"])
        if t.type in ("MacroOperator", "GroupOperator") and isinstance(t.get("Tools"), fs.T):
            for it in t["Tools"].values():                    # inner tools linked straight to outside tools
                for k, v in fs.inputs(it).items():
                    if isinstance(v, fs.T) and v.get("SourceOp") in tools:
                        link(n, "MainInput1", v["SourceOp"])
        if t.type == "Note":
            try:
                w = json.loads(fs.inp(t, "Comments") or "{}").get("w", [])
            except ValueError:
                w = []
            for dst, k, s in w:
                link(dst, k, s)
    return up, down


def _ups(up, start, stop=()):
    seen, todo = set(), [start]
    while todo:
        x = todo.pop()
        for s in up.get(x, ()):
            if s not in seen and s not in stop:
                seen.add(s); todo.append(s)
    return seen


def _macro_inner(t, prefix):
    for k, v in (t.get("Tools") or {}).items():
        if k.startswith(prefix):
            return v
    return None


def _is_counter(tools, n, t):
    if t.type == "TextPlus":
        return bool(fs.keys(tools, t, "Counter")) or bool(fs.expr(t, "StyledText")) or bool(re.search(r"count", n, re.I))
    return t.type == "MacroOperator" and bool(re.search(r"count", n, re.I)) and not n.startswith("NeoAnim")


def _fade(keys):
    """spline keys -> (start, land) of a rise from ~0, else None."""
    for i in range(len(keys) - 1):
        f0, v0 = keys[i]
        if v0 <= 0.05:
            for f1, v1 in keys[i + 1:]:
                if v1 >= 0.6:
                    top = max(v for f, v in keys if f >= f1)
                    land = next(f for f, v in keys if f >= f1 and v >= 0.95 * top)
                    return f0, land
    return None


def elements(tools, up):
    """-> list of dicts: name, kind, start, len, land, read, words (NeoMotionText word starts)"""
    el = []
    for n, t in tools.items():
        if t.type == "MacroOperator" and n.startswith("NeoAnim"):
            ga = _macro_inner(t, "GlobalAnim")
            gi = fs.inputs(ga) if ga is not None else {}
            off = (gi.get("InOffset") or {}).get("Value", 0.0) if isinstance(gi.get("InOffset"), fs.T) else 0.0
            ln = (gi.get("InLength") or {}).get("Value", 50.0) if isinstance(gi.get("InLength"), fs.T) else 50.0
            if ln <= 1 or re.search(r"out$", n, re.I):
                el.append({"name": n, "kind": "exit", "out": float((gi.get("OutLength") or {}).get("Value", 0) if
                                                                   isinstance(gi.get("OutLength"), fs.T) else 0)})
                continue
            el.append({"name": n, "kind": "neoanim", "start": float(off), "len": float(ln)})
        elif t.type == "Fuse.NeoMotionText":
            off, ln = float(fs.inp(t, "InOffsetF", 0) or 0), float(fs.inp(t, "InLengthF", 20) or 20)
            nw = max(1, len((fs.inp(t, "StyledText") or "").split()))
            dly = float(fs.inp(t, "Delay", 2.82) or 0)              # word stagger in frames (DelaySec only mirrors it)
            el.append({"name": n, "kind": "ntext", "start": off, "len": ln, "delay": dly, "nwords": nw,
                       "land_all": off + (nw - 1) * dly + ln})
        elif t.type == "TextPlus" and fs.keys(tools, t, "Counter"):
            k = fs.keys(tools, t, "Counter")
            el.append({"name": n, "kind": "counter", "start": k[0][0], "len": max(1.0, k[-1][0] - k[0][0]),
                       "land_all": k[-1][0]})
        else:
            for inp_name in ("Blend", "Gain", "Alpha", "Opacity", "TopLeftAlpha"):
                f = _fade(fs.keys(tools, t, inp_name))
                if f and t.type in ("Merge", "BrightnessContrast", "Background", "ColorCorrector", "MacroOperator"):
                    el.append({"name": n, "kind": "fade", "start": f[0], "len": max(1.0, f[1] - f[0]), "input": inp_name})
                    break
    for e in el:
        if e["kind"] != "exit":
            e["read"] = e["start"] + READ_FRAC * e["len"]
            e.setdefault("land_all", e["start"] + e["len"])
    return el


def _content(tools, up, e, all_el):
    """texts / loaders this element brings in (not those of a nested element)."""
    n = e["name"]
    t = tools[n]
    if e["kind"] in ("ntext", "counter"):
        return [n]
    starts = [n]
    if e["kind"] == "fade" and t.type == "Merge":
        s = fs.src(t, "Foreground")
        starts = [s] if s else []
        if not s:
            return []
    nested = {x["name"] for x in all_el if x["name"] != n and x["kind"] != "exit"}
    seen = set()
    for s in starts:
        if s != n:
            seen.add(s)
        seen |= _ups(up, s, stop=nested)
    return [x for x in seen if x in tools and tools[x].type in ("TextPlus", "Fuse.NeoMotionText", "Loader")]


def _owner(el_content, tool):
    for e, c in el_content:
        if tool in c:
            return e
    return None


def _xf(tools, down, n):
    """first downstream path: scale and centre (frame units) applied to a point at the tool's own coordinates."""
    scale, ops, cur, seen = 1.0, [], n, {n}
    for _ in range(80):
        cons = [c for c in down.get(cur, []) if c[1] not in ("EffectMask", "Background") or tools[c[0]].type != "Merge"]
        cons = cons or [c for c in down.get(cur, []) if c[1] != "EffectMask"]
        if not cons:
            break
        dst, k = cons[0]
        if dst in seen:
            break
        seen.add(dst)
        t = tools[dst]
        if t.type == "Transform" or (t.type == "Merge" and k == "Foreground"):
            s = fs.inp(t, "Size", 1.0)
            c = fs.inp(t, "Center", [0.5, 0.5])
            s = s if isinstance(s, (int, float)) else 1.0
            c = c if isinstance(c, list) and len(c) == 2 else [0.5, 0.5]
            scale *= s
            ops.append((s, c))
        cur = dst
    return scale, ops


def _apply(ops, p):
    x, y = p
    for s, c in ops:
        x, y = (x - 0.5) * s + c[0], (y - 0.5) * s + c[1]
    return x, y


def _text_info(tools, down, n):
    t = tools[n]
    txt = fs.inp(t, "StyledText") or ""
    size = fs.inp(t, "Size", 0.05)
    size = size if isinstance(size, (int, float)) else 0.05
    font = (fs.inp(t, "Font") or "Inter").lower()
    fh = next((v for k, v in FH if k in font), 1.21)
    sc, ops = _xf(tools, down, n)
    c = fs.inp(t, "Center", [0.5, 0.5])
    c = c if isinstance(c, list) and len(c) == 2 else [0.5, 0.5]
    px = size * 1508 / fh * sc
    w = 0.5 * px * max(len(l) for l in (txt or " ").split("\n")) / 1920      # rough line width, frame units
    if t.type == "Fuse.NeoMotionText":
        j = fs.inp(t, "Justify", 1)                              # 0 = left edge at Center (lessons 2026-09-27)
        shift = w / 2 if j == 0 else (-w / 2 if j == 2 else 0)
    else:
        j = fs.inp(t, "HorizontalLeftCenterRight", 0)            # -1 left, 0 centre, 1 right
        shift = w / 2 if j == -1 else (-w / 2 if j == 1 else 0)
    x, y = _apply(ops, (c[0] + shift / sc if sc else c[0], c[1]))
    return {"text": txt, "px": round(px, 1), "x": round(x * 1920), "y": round((1 - y) * 1080), "font": font}


def _ground(tools):
    return any(re.search(r"^BGFRONTAL|_BG$|^BG_|Background_BG|Background_Ground", n) for n in tools)


def _darkened(tools):
    """the picture under the text is darkened (a statement layout), not a plain lower third over Alex."""
    for n, t in tools.items():
        if t.type == "BrightnessContrast" and not re.search(r"down|fade", n, re.I):
            g = fs.inp(t, "Gain", 1.0)
            if isinstance(g, (int, float)) and g <= 0.75:
                return True
        if t.type == "Background" and re.search(r"shade|centredark|dark[LR]?$|dim$", n, re.I) and \
                not re.search(r"down|fade|fill|edge", n, re.I):
            return True
        if fs.src(t, "EffectMask"):
            continue
        if t.type in ("Blur", "ofx.com.blackmagicdesign.resolvefx.GaussianBlur"):
            b = fs.inp(t, "XBlurSize", 0) or fs.inp(t, "blurSize", 0) or 0
            if isinstance(b, (int, float)) and b >= 5:
                return True
        if t.type == "Merge":
            b = fs.inp(t, "Blend", 1.0)
            fg = fs.src(t, "Foreground")
            if fg and re.search(r"dark|dim|shade|backing", fg, re.I) and isinstance(b, (int, float)) and b >= 0.6:
                return True
    return False


# ------------------------------------------------------------------------------------------------------- the lint
def lint_op(op, words, beat, below_media, continued=None):
    """one comp op -> {rule: [findings]}, stats. A finding = (ok: bool, message)."""
    R = {r: [] for r in RULES}
    path = op["setting"]
    tools = fs.load(path)
    up, down = _graph(tools)
    S, D = int(op["start"]), int(op["D"])
    kind = (beat or {}).get("kind", "")
    lo, hi = S - 24, S + D + 24                                  # the op's own range, +-1 s
    heard = words_in(words, lo, hi)
    cues = {k: norm(v) for k, v in (op.get("cues") or {}).items()}

    el = elements(tools, up)
    ent = [e for e in el if e["kind"] != "exit"]
    content = [(e["name"], _content(tools, up, e, el)) for e in ent]
    texts = {n: _text_info(tools, down, n) for n, t in tools.items() if t.type in ("TextPlus", "Fuse.NeoMotionText")}
    by = {e["name"]: e for e in ent}

    fam = {}
    for n, ti in texts.items():
        if screen_numbers(ti["text"]):
            fam.setdefault(re.sub(r"\d+[a-z]?$", "", n), []).append(n)
    axis = {n for ns in fam.values() if len(ns) >= 3 for n in ns}
    heard_t = spoken_tokens(heard)
    heard_n = {v for w, v in heard_t}
    all_n = spoken_numbers(words)

    # P1 ------------------------------------------------------------------------------------------------------
    unmatched = 0
    for e in ent:
        if e["read"] <= 0:                                       # already on at the cut in: the cut is its entrance
            continue
        cn = dict(content)[e["name"]]
        cand = []
        if e["name"] in cues:
            cand = [cues[e["name"]]]
        else:
            for tn in [c for c in cn if c in texts and c not in axis]:
                for tok in (norm(x) for x in texts[tn]["text"].split()):
                    if tok and tok not in STOP and tok not in cand and len(tok) >= 2 and not re.fullmatch(r"0+|\d", tok):
                        cand.append(tok)
        hit = None
        for tok in cand:
            tv = screen_numbers(tok)
            if tv:                                               # a number: the word that starts the spoken number
                occ = [w for w, v in heard_t if abs(v - tv[0][0]) <= max(0.005 * abs(v), 1e-9)]
            else:
                occ = [w for w in heard if norm(w["w"]) == tok or (len(tok) >= 5 and norm(w["w"])[:5] == tok[:5])]
            if occ:
                hit = min(occ, key=lambda w: abs(w["f"] - (S + e["read"])))
                hit = (tok, hit)
                break
        if not hit:
            unmatched += 1
            continue
        tok, w = hit
        if e["kind"] == "counter":                               # a count lands as he finishes saying the number
            d = round(S + e["land_all"] - w["f"], 1)
            ok = TOL[0] <= d <= (w.get("_end", w["e"]) - w["f"]) + 8
            what = "count ends"
            at = S + e["land_all"]
        else:
            k = 0
            if e["kind"] == "ntext":
                ws = [norm(x) for x in (fs.inp(tools[e["name"]], "StyledText") or "").split()]
                k = ws.index(tok) if tok in ws else 0
            at = S + e["read"] + k * e.get("delay", 0)
            d = round(at - w["f"], 1)
            ok = TOL[0] <= d <= TOL[1]
            what = "readable" if not k else "word %d readable" % (k + 1)
        R["P1"].append((ok, "%s %s f%d vs '%s' f%d: %+g f%s" % (
            e["name"], what, at, w["w"], w["f"], d, "" if ok else (" (before the word)" if d < 0 else " (late)"))))
    lead = {}
    nested = {e["name"]: set(_ups(up, e["name"])) for e in ent}
    for e in ent:
        if (e["kind"] == "fade" and not dict(content)[e["name"]]) or e["read"] <= 0:
            continue
        lead.setdefault(round(e["start"]), []).append(e["name"])
    for f, ns in sorted(lead.items()):
        free = [a for a in ns if not any(a in nested[b] or b in nested[a] for b in ns if b != a)]
        if len(free) >= 2:
            R["P1"].append((False, "%d elements enter together at comp f%d: %s" % (len(free), f, ", ".join(free[:5]))))

    # P2 ------------------------------------------------------------------------------------------------------
    counters = [n for n, t in tools.items() if _is_counter(tools, n, t)]
    for n, ti in texts.items():
        s = ti["text"].strip()
        nums = screen_numbers(s)
        rest = NUM.sub("", s).strip(" +-/.,")
        if nums and not re.search(r"[A-Za-z]{2,}", rest) and n not in axis:
            v, raw, cur, u = nums[0]
            if v == 0 or (not cur and not u and float(v).is_integer() and 1 <= v <= 9):
                continue
            if not any(abs(h - v) <= max(0.005 * abs(v), 1e-9) for h in heard_n) or ti["px"] < HERO_PX:
                continue                                         # not said here, or a small label: C9 judges it
            if n in counters:
                R["P2"].append((True, "%s '%s' counts up" % (n, raw)))
            else:
                R["P2"].append((False, "%s '%s' is a hero number Alex says, shown static: make it a counter" % (n, raw)))
    for n in counters:
        if n not in texts:
            continue
        a = texts[n]
        for m, b in texts.items():
            if m == n or m in counters or len(re.findall(r"[A-Za-z]{2,}", b["text"])) < 2:
                continue
            same_size = abs(a["px"] - b["px"]) <= 0.25 * max(a["px"], b["px"])
            if same_size and abs(a["y"] - b["y"]) < 0.5 * max(a["px"], b["px"]) and abs(a["x"] - b["x"]) < 900:
                R["P2"].append((False, "%s counter sits in a line with '%s' (%s): a number inside a sentence is "
                                       "plain text" % (n, b["text"][:30], m)))
                break

    # P3 ------------------------------------------------------------------------------------------------------
    for n, t in tools.items():
        if t.type == "Fuse.NeoMotionText":
            pd, sc = fs.inp(t, "PosDir", 0.0), fs.inp(t, "Scope", 1.0)
            ok = pd == 0 and sc == 1
            R["P3"].append((ok, "%s PosDir %s Scope %s%s" % (n, pd, sc, "" if ok else " (needs PosDir 0 Up, Scope 1 "
                                                                                       "word)")))
        elif t.type == "TextPlus" and n not in counters:
            ti = texts[n]
            if len(ti["text"].split()) >= 3 and ti["px"] >= MIN_PX["footage"]:
                R["P3"].append((False, "%s '%s' is a static Text+ headline: use NeoTextMotion word by word" % (
                    n, ti["text"][:40])))

    # P5 ------------------------------------------------------------------------------------------------------
    for n, t in tools.items():
        if re.search(r"strike|cancel|cross_?out|xout", n, re.I):
            R["P5"].append((False, "%s: strike/cancel line by name" % n))
    for n, t in tools.items():
        if t.type != "RectangleMask":
            continue
        w, h = fs.inp(t, "Width", 0.5), fs.inp(t, "Height", 0.5)
        if not all(isinstance(v, (int, float)) for v in (w, h)) or h <= 0 or w / h < 8:
            continue
        for dst, k in down.get(n, []):
            bg = tools[dst]
            if bg.type != "Background" or k != "EffectMask":
                continue
            r, g, b = (fs.inp(bg, c, 0) for c in ("TopLeftRed", "TopLeftGreen", "TopLeftBlue"))
            if not all(isinstance(v, (int, float)) for v in (r, g, b)) or not (r > 0.5 and g < 0.4 and b < 0.4):
                continue
            c = fs.inp(t, "Center", [0.5, 0.5])
            ly, lx = (1 - c[1]) * 1080, c[0] * 1920
            for tn, ti in texts.items():
                if abs(ly - ti["y"]) < 0.35 * ti["px"] and abs(lx - ti["x"]) < w * 1920:
                    R["P5"].append((False, "%s: red bar across '%s'" % (n, ti["text"][:30])))

    # C3 ------------------------------------------------------------------------------------------------------
    exits = [e.get("out", 0) for e in el if e["kind"] == "exit" and e.get("out")]
    cut = D - (max(exits) if exits else 0)
    if continued:
        R["C3"].append((True, "continues into %s (same beat, butted): the hold is judged at the sequence end" % continued))
    elif [e for e in ent if e["kind"] != "fade" or dict(content)[e["name"]]]:
        last = max([e for e in ent if e["kind"] != "fade" or dict(content)[e["name"]]], key=lambda e: e["land_all"])
        gap = cut - last["land_all"]
        R["C3"].append((gap >= HOLD, "last element %s lands comp f%d, cut f%d: %d f hold (need %d)" % (
            last["name"], last["land_all"], cut, gap, HOLD)))

    # C6 / C7 ---------------------------------------------------------------------------------------------------
    if _ground(tools):
        over = "ground"
    elif below_media:
        over = "page"
    else:
        over = "aroll-dark" if _darkened(tools) else "aroll"
    need = MIN_PX["ui"] if kind == "ui-demo" else (MIN_PX["footage"] if over.startswith("aroll") else MIN_PX["ground"])
    shown = {n: ti for n, ti in texts.items() if ti["text"].strip()}
    if over == "aroll" and shown:
        for n, ti in shown.items():
            ok = ti["y"] >= LT_Y
            R["C6"].append((ok, "%s '%s' over Alex at y%d%s" % (n, ti["text"][:30], ti["y"],
                                                               "" if ok else " (lower third: bottom band, y >= %d)" % LT_Y)))
        xs = [ti["x"] for ti in shown.values()]
        gx = (min(xs) + max(xs)) / 2
        R["C6"].append((abs(gx - 960) <= LT_DX, "text group centred at x%d%s" % (
            gx, "" if abs(gx - 960) <= LT_DX else " (lower thirds are centred, |x - 960| <= %d)" % LT_DX)))
    for n, ti in shown.items():
        R["C7"].append((ti["px"] >= need, "%s '%s' %g px (min %d, %s)" % (n, ti["text"][:30], ti["px"], need, over)))

    # C9 ------------------------------------------------------------------------------------------------------
    if kind != "ui-demo":
        for n, ti in texts.items():
            if n in axis:
                continue
            for v, raw, cur, u in screen_numbers(ti["text"]):
                if v == 0 or (not cur and not u and float(v).is_integer() and 1 <= v <= 9):
                    continue
                near = any(abs(h - v) <= max(0.005 * abs(v), 1e-9) for h in heard_n)
                far = near or any(abs(h - v) <= max(0.005 * abs(v), 1e-9) for h in all_n)
                R["C9"].append((far, "%s shows '%s'%s" % (n, raw, "" if near else (
                    " - said elsewhere in the video, not in this beat" if far else
                    " - never said (heard here: %s)" % (", ".join("%g" % h for h in sorted(heard_n))[:80] or "none")))))
    stats = {"tools": len(tools), "elements": len(ent), "unmatched": unmatched, "over": over,
             "kb": round(os.path.getsize(path) / 1024)}
    return R, stats


# ---------------------------------------------------------------------------------------------------- the beats
def _manifests(args):
    out = []
    for a in args:
        if os.path.isfile(a) and a.lower().endswith(".json"):
            out.append(a)
        elif os.path.isfile(os.path.join(a, "manifest.json")):
            out.append(os.path.join(a, "manifest.json"))
        elif os.path.isdir(a):
            out += sorted(glob.glob(os.path.join(a, "*", "manifest.json")))
    return out


def _beat_index(beats):
    idx = {}
    for b in beats:
        idx.setdefault(b["id"], b)
        for x in b.get("built") or []:
            idx.setdefault(x, b)
    return idx


def find_beat(idx, folder):
    for k in (folder, re.sub(r"[a-z]$", "", folder), re.sub(r"[_ ].*$", "", folder)):
        if k in idx:
            return idx[k]
    return None


def _stem(folder):
    return re.sub(r"[a-z]$", "", folder)


def _continued(op, folder, allops):
    """the op's visual goes on in a butted op of the same beat on the same track (an entrance part, a list step)."""
    end = op["start"] + op["D"]
    for f, o in allops:
        if o is not op and o.get("op") == "comp" and o.get("track") == op.get("track") and 0 <= o["start"] - end <= 1 \
                and _stem(f) == _stem(folder):
            return "%s @%d" % (f, o["start"])
    return None


def lint_manifest(mpath, words, idx, allops=()):
    folder = os.path.basename(os.path.dirname(mpath))
    ops = json.load(open(mpath, encoding="utf-8"))
    allops = list(allops) or [(folder, o) for o in ops]
    beat = find_beat(idx, folder)
    res = {"beat": folder, "plan_beat": beat and beat["id"], "manifest": mpath, "comps": [],
           "rules": {r: {"ok": 0, "fail": 0, "msgs": []} for r in RULES}}
    for op in ops:
        if op.get("op") != "comp":
            continue
        if not os.path.exists(op["setting"]):
            res["comps"].append({"setting": op["setting"], "error": "missing"}); continue
        below = any(o is not op and o.get("op") in ("media", "comp") and int(o.get("track", 2)) < int(op.get("track", 2))
                    and o["start"] < op["start"] + op["D"] and op["start"] < o["start"] + o["D"] for o in ops)
        same = [(f, o) for f, o in allops if f == folder and o.get("setting") == op.get("setting")]
        if same and same[0][1] is not op:                        # allops holds its own copies of this manifest's ops
            op_key = same[0][1]
        else:
            op_key = op
        try:
            R, st = lint_op(op, words, beat, below, _continued(op_key, folder, allops))
        except Exception as e:                                   # a comp the parser can't read is a FAIL to look at
            res["comps"].append({"setting": op["setting"], "error": repr(e)[:200]}); continue
        st["setting"] = op["setting"]
        res["comps"].append(st)
        for r, fl in R.items():
            for ok, msg in fl:
                res["rules"][r]["ok" if ok else "fail"] += 1
                if not ok:
                    res["rules"][r]["msgs"].append("%s: %s" % (os.path.basename(op["setting"]), msg))
    return res


def main(argv):
    if argv[:1] == ["--why"]:
        rep = json.load(open(argv[1], encoding="utf-8"))
        for b in rep["beats"]:
            if b["beat"] == argv[2]:
                for r in RULES:
                    for m in b["rules"][r]["msgs"]:
                        print(r, m)
                for c in b["comps"]:
                    if c.get("error"):
                        print("ERROR", c["setting"], c["error"])
        return 0
    a = {"words": None, "beats": None, "section": None, "out": None, "setting": None, "start": 0, "D": 0, "beat": None,
         "over": None, "paths": []}
    i = 0
    while i < len(argv):
        x = argv[i]
        if x.startswith("--") and x[2:] in a:
            a[x[2:]] = argv[i + 1]; i += 2; continue
        a["paths"].append(x); i += 1
    words = json.load(open(a["words"], encoding="utf-8"))
    beats = json.load(open(a["beats"], encoding="utf-8")) if a["beats"] else []
    idx = _beat_index(beats)
    t0 = time.time()
    results = []
    if a["setting"]:
        op = {"op": "comp", "setting": a["setting"], "start": int(a["start"]), "D": int(a["D"])}
        beat = idx.get(a["beat"]) if a["beat"] else None
        tmpdir = os.path.join(os.environ.get("TEMP", "."), "beat_lint")
        os.makedirs(tmpdir, exist_ok=True)
        mp = os.path.join(tmpdir, "single_manifest.json")
        json.dump([op], open(mp, "w", encoding="utf-8"))
        r = lint_manifest(mp, words, idx if beat else {})
        r["beat"] = a["beat"] or os.path.basename(a["setting"])
        results.append(r)
    mans = _manifests(a["paths"])
    allops = []
    for m in mans:
        try:
            allops += [(os.path.basename(os.path.dirname(m)), o) for o in json.load(open(m, encoding="utf-8"))]
        except ValueError:
            pass
    for m in mans:
        folder = os.path.basename(os.path.dirname(m))
        b = find_beat(idx, folder)
        if a["section"] and (not b or b.get("sec") != a["section"]):
            continue
        results.append(lint_manifest(m, words, idx, allops))
    out = a["out"] or os.path.join(os.path.dirname(a["beats"]) if a["beats"] else os.environ.get("TEMP", "."),
                                   "lint", "lint_%s_%s.json" % (a["section"] or "all", time.strftime("%Y%m%d_%H%M%S")))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"made": time.strftime("%Y-%m-%d %H:%M"), "words": a["words"], "beats": results}, open(out, "w",
              encoding="utf-8"), indent=1, ensure_ascii=False)
    print("beat_lint: %d beats%s, %.1f s -> %s" % (len(results), " (section %s)" % a["section"] if a["section"] else "",
                                                 time.time() - t0, out))
    print("%-10s %s  elements unmatched comps" % ("BEAT", " ".join("%-4s" % r for r in RULES)))
    tot = {r: [0, 0] for r in RULES}
    nfail = 0
    for r in results:
        cells = []
        for k in RULES:
            x = r["rules"][k]
            cells.append("-   " if not (x["ok"] or x["fail"]) else ("FAIL" if x["fail"] else "ok  "))
            tot[k][0] += bool(x["fail"]); tot[k][1] += x["fail"]
        err = sum(1 for c in r["comps"] if c.get("error"))
        bad = any(c == "FAIL" for c in cells) or err
        nfail += bool(bad)
        print("%-10s %s  %3d %3d %d%s" % (r["beat"][:10], " ".join(cells), sum(c.get("elements", 0) for c in r["comps"]),
                                          sum(c.get("unmatched", 0) for c in r["comps"]), len(r["comps"]),
                                          "  ERR %d" % err if err else ""))
    print("fails: " + "  ".join("%s %d beats/%d" % (k, v[0], v[1]) for k, v in tot.items() if v[0]) if nfail else
          "fails: none")
    print("%d of %d beats fail. Details: python beat_lint.py --why \"%s\" <BEAT>" % (nfail, len(results), out))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
