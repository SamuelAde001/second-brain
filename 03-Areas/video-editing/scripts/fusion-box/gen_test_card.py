# Samuel's standard card, animated in, for his test Fusion comp (Timeline 6, 2026-10-02).
# Built after Gemini's test ("TEST CARD" text on a flat orange frame: card at alpha 0, no animation).
#
# The house card: BGORANGE ground; box with outline (dark fill + Instance border, orange, Neo Glow);
# P01 medallion (white disc, orange ring, real logo); two-tone Geist ExtraBold headline (white line +
# orange line); NeoLightSweep -> shine -> DropShadow -> his NeoAnim, inline on the card line.
#
# Flow layout (ways of working -> Node tree layout, the B04 v2 standard):
#   text rows (one per line, ending in its Transform) -> collector column over its own clear canvas
#   medallion line: canvas -> fill -> ring -> logo -> Transform_MedallionPop
#   card line: canvas -> fill -> border -> Merge_Medallion -> Merge_Texts -> LightSweep -> shine
#              -> DropShadow -> NeoAnim_Card
#   main line: BGORANGE -> Merge_Card -> MediaOut1 (the comp's own, wired live)
#
#   python gen_test_card.py <out_dir>   -> test_card.setting + test_card_wiring.json
import json, os, re, sys
from collections import Counter

KIT = r"C:\Users\repzy\Desktop\Video edits\Routerise\3. I Tried 100+ AI Tools. These 4 Are Best for Businesses\Graphics\Visuals v2"
sys.path.insert(0, KIT)
from pk import *             # noqa: F401,F403
import pillkit as _pk        # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
LOGO = r"C:\Users\repzy\Desktop\Video edits\Routerise\I cancelled Apollo.io and built this Claude skill instead\Graphics\Logos\fav_anthropic.com.png"
KS = 1 / 1013.0                                   # px -> Text+ Size
ORANGE = (1.0, 0.3529, 0.1216)
TINT = (1.0, 0.62, 0.42)                          # eyebrow
FILL_TOP, FILL_BOT = (0.17, 0.058, 0.022), (0.075, 0.025, 0.009)

# geometry, px (1920x1080)
PAD, MD, GAP, TW = 72, 196, 52, 706            # padding, medallion, gap, widest line (measured: 791 px at 56 px)
CW, CH, CR = PAD + MD + GAP + TW + PAD, 380, 44   # card fits its content, equal padding both sides
CCX, CCY = 960, 540
X0, Y0 = CCX - CW / 2, CCY - CH / 2
MCX, MCY = X0 + PAD + MD / 2, CCY                 # medallion
TX = MCX + MD / 2 + GAP                           # text left edge
LINES = [("Eyebrow", "THE NEW OUTBOUND STACK", "SemiBold", 26, TINT, 462),
         ("Line1", "I CANCELLED APOLLO.IO", "ExtraBold", 50, (1, 1, 1), 530),
         ("Line2", "BUILT A CLAUDE SKILL", "ExtraBold", 50, ORANGE, 594)]

# timing, comp frames (clip is 120 frames)
CARD_IN, CARD_LEN = 0, 16
POP = (7, 15, 19)                                 # medallion: start, overshoot, settle
TXT_T = [11, 14, 18]                              # line starts; 10 f each
SHINE = (34, 50)

# flow grid
STEP, UP = 110, 66
C = lambda k: int(-3000 + k * STEP)
Y_MAIN, Y_CARD, Y_MED = 1400, 1100, 760
Y_ROWS = [430, 530, 630]                           # beside the medallion line, cols 2-4


def place(cx, cy):
    return (0.5 + (cx - 960) / W, 0.5 + (540 - cy) / H)


def rect(name, cx, cy, w, h, r, pos):
    tool(name, "RectangleMask", {**MASKF, "Center": (fx(cx), fy(cy)), "Width": w / W, "Height": h / H,
                                 "CornerRadius": min(1.0, 2.0 * r / min(w, h))}, pos)


def ellipse(name, cx, cy, d, pos):
    tool(name, "EllipseMask", {**MASKF, "Center": (fx(cx), fy(cy)), "Width": d / W, "Height": d / W}, pos)


def instance(name, src, kind, bw, pos):
    _pk.tools.append((name, '\t\t%s = %s {\n\t\t\tSourceOp = "%s",\n\t\t\tInputs = {\n\t\t\t\tSolid = Input { Value = 0, },\n\t\t\t\tBorderWidth = Input { Value = %s, },\n\t\t\t\tEffectMask = Input { },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { %d, %d } },\n\t\t},' % (name, kind, src, lua(bw), pos[0], pos[1])))


def grad(name, top_c, bot_c, y0, y1, pos, mask):
    f0, f1 = y0 / H, y1 / H
    a = [t - (b - t) / (f1 - f0) * f0 for t, b in zip(top_c, bot_c)]
    z = [t + (b - t) / (f1 - f0) * (1 - f0) for t, b in zip(top_c, bot_c)]
    tool(name, "Background", {**FRAME, "Type": "FuID:Vertical", "TopLeftRed": a[0], "TopLeftGreen": a[1], "TopLeftBlue": a[2],
                              "BottomLeftRed": z[0], "BottomLeftGreen": z[1], "BottomLeftBlue": z[2],
                              "EffectMask": link(mask, "Mask")}, pos)


def tp(name, s, style, px, rgb, x, y, pos):
    tool(name, "TextPlus", {**FRAME, "Center": (fx(x), fy(y)), "StyledText": s, "Font": "Geist", "Style": style,
                            "Size": round(px * KS, 5), "VerticalJustificationNew": 3, "HorizontalJustificationNew": 3,
                            "HorizontalLeftCenterRight": -1, "Red1": rgb[0], "Green1": rgb[1], "Blue1": rgb[2]}, pos)


def mg(name, bg, fg, pos, mask=None, blend=None):
    d = {"PerformDepthMerge": 0}
    if bg: d["Background"] = link(bg)
    if fg: d["Foreground"] = link(fg)
    if mask: d["EffectMask"] = link(mask, "Mask")
    if blend is not None: d["Blend"] = blend
    tool(name, "Merge", d, pos)
    return name


def canvas(name, pos):
    background(name, (0, 0, 0), pos, a=0.0)
    return name


def keys(name, pts):
    out = []
    for i, (t, v) in enumerate(pts):
        lh = (t - (t - pts[i - 1][0]) / 3.0, v) if i else None
        rh = (t + (pts[i + 1][0] - t) / 3.0, v) if i < len(pts) - 1 else None
        out.append((t, v, lh, rh, False))
    return spline(name, out)


reset()

# ---- text rows: Text -> Transform (slide up 26 px), one row each; collector column at k=4
rows = []
for i, (nm, s, style, px, rgb, y) in enumerate(LINES):
    ry, t0 = Y_ROWS[i], TXT_T[i]
    tp("Text_%s" % nm, s, style, px, rgb, TX, y, (C(2), ry))
    tool("Transform_%s" % nm, "Transform", {"Input": link("Text_%s" % nm),
         "Center": xypath("Transform_%sCenter" % nm, 0.5, keys("Transform_%sY" % nm, [(t0, 0.5 - 26 / H), (t0 + 10, 0.5)]))},
         (C(3), ry))
    rows.append(("Transform_%s" % nm, t0))
prev = canvas("Background_TextCanvas", (C(4), Y_ROWS[0] - 2 * UP))
for i, (o, t0) in enumerate(rows):
    prev = mg("Merge_TextRow%d" % i, prev, o, (C(4), Y_ROWS[i]), blend=keys("Merge_TextRow%dBlend" % i, [(t0, 0.0), (t0 + 7, 1.0)]))
texts_out = prev

# ---- medallion line: canvas -> white disc -> orange ring (+ Neo Glow) -> logo -> pop
canvas("Background_MedCanvas", (C(-3), Y_MED))
ellipse("Ellipse_MedFill", MCX, MCY, MD, (C(-2), Y_MED - 2 * UP))
background("Background_MedFill", (1, 1, 1), (C(-2), Y_MED - UP), mask="Ellipse_MedFill")
mg("Merge_MedFill", "Background_MedCanvas", "Background_MedFill", (C(-2), Y_MED))
instance("Instance_Ellipse_MedRing", "Ellipse_MedFill", "EllipseMask", 0.0042, (C(-1), Y_MED - 3 * UP))
background("Background_MedRing", ORANGE, (C(-1), Y_MED - 2 * UP), mask="Instance_Ellipse_MedRing")
macro(NEO, "Neo Glow.setting", "NeoGlow", "NeoGlow_MedRing", (C(-1), Y_MED - UP), "_MR")
mg("Merge_MedRing", "Merge_MedFill", None, (C(-1), Y_MED))
WIRING.append(("NeoGlow_MedRing", "MainInput1", "Background_MedRing"))
WIRING.append(("Merge_MedRing", "Foreground", "NeoGlow_MedRing"))
canvas("Background_LogoCanvas", (C(0), Y_MED - 3 * UP))
loader("Loader_Logo", LOGO, (C(0), Y_MED - 4 * UP))
mg("Merge_LogoCanvas", "Background_LogoCanvas", "Loader_Logo", (C(0), Y_MED - 2 * UP))
tool("Transform_Logo", "Transform", {"Size": 104 / 256.0, "Center": place(MCX, MCY), "Input": link("Merge_LogoCanvas")}, (C(0), Y_MED - UP))
ellipse("Ellipse_LogoClip", MCX, MCY, MD - 26, (C(1), Y_MED - UP))
mg("Merge_Logo", "Merge_MedRing", "Transform_Logo", (C(0), Y_MED), mask="Ellipse_LogoClip")
tool("Transform_MedallionPop", "Transform", {"Input": link("Merge_Logo"), "Pivot": (fx(MCX), fy(MCY)),
     "Size": keys("Transform_MedallionPopSize", [(POP[0], 0.001), (POP[1], 1.08), (POP[2], 1.0)])}, (C(3), Y_MED))

# ---- card line
canvas("Background_CardCanvas", (C(0), Y_CARD))
rect("Rectangle_Card", CCX, CCY, CW, CH, CR, (C(1), Y_CARD - 2 * UP))
grad("Background_CardFill", FILL_TOP, FILL_BOT, Y0, Y0 + CH, (C(1), Y_CARD - UP), "Rectangle_Card")
mg("Merge_CardFill", "Background_CardCanvas", "Background_CardFill", (C(1), Y_CARD))
instance("Instance_Rectangle_Card", "Rectangle_Card", "RectangleMask", 0.00184, (C(2), Y_CARD - 3 * UP))
background("Background_CardBorder", ORANGE, (C(2), Y_CARD - 2 * UP), mask="Instance_Rectangle_Card")
macro(NEO, "Neo Glow.setting", "NeoGlow", "NeoGlow_CardBorder", (C(2), Y_CARD - UP), "_CB")
mg("Merge_CardBorder", "Merge_CardFill", None, (C(2), Y_CARD))
WIRING.append(("NeoGlow_CardBorder", "MainInput1", "Background_CardBorder"))
WIRING.append(("Merge_CardBorder", "Foreground", "NeoGlow_CardBorder"))
mg("Merge_Medallion", "Merge_CardBorder", "Transform_MedallionPop", (C(3), Y_CARD))
mg("Merge_Texts", "Merge_Medallion", texts_out, (C(4), Y_CARD))
copy_his("NeoLightSweepPro_1_1_3_2_1_1", "NeoLightSweep_Card", "_LSC", (C(5), Y_CARD), stop=("Displace1_1_1",))
WIRING.append(("NeoLightSweep_Card", "MainInput1", "Merge_Texts"))
tool("Rectangle_Shine", "RectangleMask", {**MASKF, "Width": 0.03, "Height": 0.5, "Angle": -18.0, "SoftEdge": 0.014,
     "Center": xypath("Rectangle_ShineCenter", ease("Rectangle_ShineX", SHINE[0], SHINE[1], fx(X0 - 80), fx(X0 + CW + 80)), 0.5)},
     (C(6), Y_CARD - UP))
tool("BrightnessContrast_Shine", "BrightnessContrast", {"Gain": 1.7, "Brightness": 0.05, "PreDividePostMultiply": 1,
     "EffectMask": link("Rectangle_Shine", "Mask")}, (C(6), Y_CARD))
WIRING.append(("BrightnessContrast_Shine", "Input", "NeoLightSweep_Card"))
tool("DropShadow_Card", "ofx.com.blackmagicdesign.resolvefx.DropShadow",
     {"shadowStrength": 0.55, "shadowAngle": 90.0, "ShadowDistance": 0.012, "shadowBlur": 0.5, "Source": link("BrightnessContrast_Shine")},
     (C(7), Y_CARD))
copy_his("NeoAnim_1_1_1", "NeoAnim_Card", "_NAC", (C(8), Y_CARD), stop=("DropShadow1_1_1",), patches=[
    (r"InOffset = Input \{ Value = 56, \}", "InOffset = Input { Value = %d, }" % CARD_IN),
    (r"InLength = Input \{ Value = 25, \}", "InLength = Input { Value = %d, }" % CARD_LEN),
    (r"StartOffset = Input \{ Value = 0\.44, \}", "StartOffset = Input { Value = 0.12, }"),
    (r"Center = Input \{ Value = \{ 0\.3, 0\.696 \}, \}", "Center = Input { Value = { 0.5, 0.5 }, }")])
WIRING.append(("NeoAnim_Card", "MainInput1", "DropShadow_Card"))

# ---- main line, BGORANGE laid out at its start
bg = bgorange("_BG")
bi = [j for j, (nm, _) in enumerate(_pk.tools) if nm == "BGORANGE_BG"][0]
BGPOS = {"Background2_1_3_2_4_2": (-3, 0), "Grid1": (-2, 0), "Merge5": (-1, 0), "GaussianBlur2": (-1, -1),
         "Background2_1_3_2_4_3": (-1, -2), "Ellipse1": (-1, -3), "Ellipse1_1": (-2, -3)}
txt = _pk.tools[bi][1]
for nm, (dk, du) in BGPOS.items():
    txt, cnt = re.subn(r"(\n\t\t%s_BG = [\w.]+ \{.*?\n\t\t\tViewInfo = OperatorInfo \{ Pos = \{ )[-\d.]+, [-\d.]+( \})" % nm,
                       lambda m: m.group(1) + "%d, %d" % (C(dk), Y_MAIN + du * UP) + m.group(2), txt, count=1, flags=re.S)
    assert cnt == 1, nm
_pk.tools[bi] = ("BGORANGE_BG", txt)
main = mg("Merge_Card", bg, None, (C(8), Y_MAIN))
WIRING.append(("Merge_Card", "Foreground", "NeoAnim_Card"))

# ---- safety: unique names, no link loops, no shared positions
names = [n for n, _ in _pk.tools]
dupn = [n for n, c in Counter(names).items() if c > 1]
assert not dupn, dupn
deps = {nm: set(re.findall(r'SourceOp = "(\w+)"', t)) for nm, t in _pk.tools}
state = {}


def _dfs(n):
    state[n] = 1
    for x in deps.get(n, ()):
        if x in deps:
            assert state.get(x) != 1, ("loop", n, x)
            if not state.get(x):
                _dfs(x)
    state[n] = 2


for n in deps:
    if not state.get(n):
        _dfs(n)
pos = {}
for nm, t in _pk.tools:
    m = re.search(r"\n\t\t\tViewInfo = (?:Operator|Group)Info \{\s*Pos = \{ ([-\d.]+), ([-\d.]+) \}", t)
    if m:
        pos.setdefault((float(m.group(1)), float(m.group(2))), []).append(nm)
over = [v for v in pos.values() if len(v) > 1]
body = "\n".join(t for _, t in _pk.tools)
open(os.path.join(OUT, "test_card.setting"), "w", encoding="utf-8").write("{\n\tTools = ordered() {\n%s\n\t},\n}\n" % body)
json.dump({"names": names, "wiring": WIRING, "last": main}, open(os.path.join(OUT, "test_card_wiring.json"), "w"), indent=1)
print(len(names), "tools; overlaps:", over)
