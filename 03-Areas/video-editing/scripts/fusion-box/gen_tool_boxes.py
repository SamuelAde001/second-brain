"""Four tool boxes + dashed connector lines for Route Rise #3 (Composition2).

Samuel's rules (2026-09-26): square boxes; NeoLightSweepPro is a static centre shine,
the moving shine is a BrightnessContrast masked by an inclined RectangleMask; fades use
his Opacity macro, never Merge Blend; no underlays, each box's nodes far from the rest;
icon + name only, hidden under MosaicBlur; lines from his dashed-line setup.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
NEO = os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\Neo folder")
MINE = os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\My macros")
TILES = r"C:\Users\repzy\Desktop\Video edits\Routerise\3. I Tried 100+ AI Tools. These 4 Are Best for Businesses\Graphics\AI tool logos\tiles"
PLATE = os.path.join(os.path.dirname(HERE), "comp2_before_2.5.1.jpg")
END = 114
W, H = 1920.0, 1080.0

ACC = (1.0, 0.3529, 0.1216)        # #FF5A1F
FILL = (0.1059, 0.0353, 0.0118)    # accent x 0.10
WHITE = (1.0, 1.0, 1.0)

TOOLS = [("Claude", "CLAUDE", "01 Claude.png"), ("Clay", "CLAY", "02 Clay.png"),
         ("Railway", "RAILWAY", "03 Railway.png"), ("WisprFlow", "WISPR FLOW", "04 Wispr Flow.png")]
BOX = 280                     # px, square
GAP = 100
BOX_CY = 230                  # px from top
XS = [250 + BOX / 2 + i * (BOX + GAP) for i in range(4)]    # 390, 770, 1150, 1530
STAGGER = 8                   # frames between boxes
CARD_TOP = 515                # Samuel's A-roll card after it settles (frame 33)


def fx(px): return px / W                 # px -> Fusion x
def fy(py): return 1.0 - py / H           # px (from top) -> Fusion y


def lua(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return repr(round(v, 6))
    if isinstance(v, int):
        return str(v)
    if isinstance(v, tuple):
        return "{ " + ", ".join(lua(x) for x in v) + " }"
    if isinstance(v, str) and v.startswith("FuID:"):
        return 'FuID { "%s" }' % v[5:]
    return '"%s"' % v.replace("\\", "\\\\").replace('"', '\\"')


tools = []


def link(src, out="Output"):
    return {"src": src, "out": out}


def inp(d):
    out = []
    for k, v in d.items():
        key = k if re.fullmatch(r"[A-Za-z_]\w*", k) else '["%s"]' % k
        if isinstance(v, dict):
            out.append('%s = Input { SourceOp = "%s", Source = "%s", },' % (key, v["src"], v["out"]))
        else:
            out.append("%s = Input { Value = %s, }," % (key, lua(v)))
    return "\n\t\t\t\t".join(out)


def tool(name, kind, inputs, pos, extra=""):
    view = "\t\t\tViewInfo = OperatorInfo { Pos = { %d, %d } },\n" % pos if pos else ""
    tools.append((name, "\t\t%s = %s {\n%s\t\t\tInputs = {\n\t\t\t\t%s\n\t\t\t},\n%s\t\t},"
                  % (name, kind, extra, inp(inputs), view)))


def spline(name, keys, indent=2):
    """Eased keys: each segment leaves fast and lands soft (never linear)."""
    kf = []
    for i, (t, v) in enumerate(keys):
        parts = [lua(float(v))]
        if i > 0:
            t0, v0 = keys[i - 1]
            parts.append("LH = { %s, %s }" % (lua(t - (t - t0) / 3.0), lua(float(v))))
        if i < len(keys) - 1:
            t1, v1 = keys[i + 1]
            parts.append("RH = { %s, %s }" % (lua(t + (t1 - t) / 3.0), lua(v + (v1 - v) * 0.85)))
        kf.append("[%d] = { %s }," % (t, ", ".join(parts)))
    T = "\t" * indent
    txt = ("%s%s = BezierSpline {\n%s\tSplineColor = { Red = 255, Green = 128, Blue = 0 },\n%s\tNameSet = true,\n%s\tKeyFrames = {\n%s\n%s\t}\n%s},"
           % (T, name, T, T, T, "\n".join(T + "\t\t" + k for k in kf), T, T))
    return txt


def anim(name, keys):
    tools.append((name, spline(name, keys)))
    return link(name, "Value")


def xypath(name, x, y):
    def f(v):
        return 'Input { SourceOp = "%s", Source = "Value", }' % v["src"] if isinstance(v, dict) else "Input { Value = %s, }" % lua(v)
    tools.append((name, '\t\t%s = XYPath {\n\t\t\tShowKeyPoints = false,\n\t\t\tDrawMode = "ModifyOnly",\n\t\t\tNameSet = true,\n\t\t\tInputs = {\n\t\t\t\tX = %s,\n\t\t\t\tY = %s,\n\t\t\t},\n\t\t},'
                  % (name, f(x), f(y))))
    return link(name, "Value")


def macro(folder, file, old, new, pos, sfx, patch=None):
    s = open(os.path.join(folder, file), encoding="utf-8").read()
    start = s.index("\t\t%s = MacroOperator {" % old)
    end = s.index("\n\t\t}", start) + 4
    block = s[start:end].replace("\t\t%s = MacroOperator {" % old, "\t\t%s = MacroOperator {" % new, 1)
    block = re.sub(r"(\n\t\t\tViewInfo = GroupInfo \{\s*Pos = \{ )[^}]*\}", r"\g<1>%d, %d }" % pos, block)
    if patch:
        block = patch(block)
    # unique inner tool names per instance (not the published InstanceInput controls)
    inner = set(re.findall(r"\n\t\t\t\t(\w+) = (?!Instance)\w+ \{", block))
    block = re.sub(r"(\n\t\t\t\t)(\w+)( = (?!Instance)\w+ \{)",
                   lambda m: m.group(1) + m.group(2) + (sfx if m.group(2) in inner else "") + m.group(3), block)
    block = re.sub(r'SourceOp = "(\w+)"',
                   lambda m: 'SourceOp = "%s%s"' % (m.group(1), sfx if m.group(1) in inner else ""), block)
    block = re.sub(r'Expression = "[^"]*"',
                   lambda m: re.sub(r"\b(\w+)\.", lambda k: k.group(1) + (sfx if k.group(1) in inner else "") + ".", m.group(0)), block)
    tools.append((new, block + ","))


FRAME = {"Width": 1920, "Height": 1080, "UseFrameFormatSettings": 1, "GlobalOut": END}
MASKF = {"Filter": "FuID:Fast Gaussian", "MaskWidth": 1920, "MaskHeight": 1080, "PixelAspect": (1, 1),
         "UseFrameFormatSettings": 1, "ClippingMode": "FuID:None"}
MB = {"MotionBlur": 1, "Quality": 4, "ShutterAngle": 180}


def background(name, rgb, pos, mask=None, a=1.0):
    d = {**FRAME, "TopLeftRed": rgb[0], "TopLeftGreen": rgb[1], "TopLeftBlue": rgb[2], "TopLeftAlpha": a}
    if mask:
        d["EffectMask"] = link(mask, "Mask")
    tool(name, "Background", d, pos)


def text(name, s, style, size, rgb, center, pos, spacing=1.0, opacity=1.0, mask=None):
    d = {**FRAME, "Center": center, "StyledText": s, "Font": "Geist", "Style": style, "Size": size,
         "CharacterSpacing": spacing, "VerticalJustificationNew": 3, "HorizontalJustificationNew": 3,
         "Red1": rgb[0], "Green1": rgb[1], "Blue1": rgb[2], "Opacity1": opacity}
    if mask:
        d["EffectMask"] = link(mask, "Mask")
    tool(name, "TextPlus", d, pos)


def merge(name, bg, fg, pos, center=None, size=None, mb=False):
    d = {"PerformDepthMerge": 0}
    if bg:
        d["Background"] = link(bg)
    if fg:
        d["Foreground"] = link(fg)
    if center is not None:
        d["Center"] = center
    if size is not None:
        d["Size"] = size
    if mb:
        d.update(MB)
    tool(name, "Merge", d, pos)


def loader(name, path, pos):
    tool(name, "Loader", {"PostMultiplyByAlpha": 1, "Loop": 1}, pos,
         extra='\t\t\tClips = {\n\t\t\t\tClip {\n\t\t\t\t\tID = "Clip1",\n\t\t\t\t\tFilename = %s,\n\t\t\t\t\tFormatID = "%s",\n\t\t\t\t\tStartFrame = -1,\n\t\t\t\t\tLengthSetManually = true,\n\t\t\t\t\tTrimIn = 0,\n\t\t\t\t\tTrimOut = 0,\n\t\t\t\t\tExtendFirst = 0,\n\t\t\t\t\tExtendLast = %d,\n\t\t\t\t\tLoop = 1,\n\t\t\t\t\tAspectMode = 0,\n\t\t\t\t\tDepth = 0,\n\t\t\t\t\tTimeCode = 0,\n\t\t\t\t\tGlobalStart = 0,\n\t\t\t\t\tGlobalEnd = 0\n\t\t\t\t}\n\t\t\t},\n'
         % (lua(path), "JpegFormat" if path.lower().endswith(".jpg") else "PNGFormat", END))


def opacity_patch(spname, keys):
    def p(block):
        block = block.replace("\t\t\tTools = ordered() {\n", "\t\t\tTools = ordered() {\n" + spline(spname, keys, indent=4) + "\n", 1)
        return block.replace("\t\t\t\t\t\tAlpha = Input { Value = 1, }\n",
                             '\t\t\t\t\t\tAlpha = Input { Value = 1, },\n\t\t\t\t\t\tGain = Input { SourceOp = "%s", Source = "Value", },\n' % spname, 1)
    return p


# ------------------------------------------------------------ dashed lines (his setup)
def line_points(i):
    """Right-angled path: card top -> up -> across -> up to the box's bottom edge (px)."""
    ox = [740, 880, 1040, 1180][i]
    tx = XS[i]
    ymid = 442
    return [(ox, CARD_TOP - 12), (ox, ymid), (tx, ymid), (tx, BOX_CY + BOX / 2 + 10)]


def polyline(pts):
    # Fusion polyline space: centre-origin; x in width units, y in height units
    P = [((x - W / 2) / W, (H / 2 - y) / H) for x, y in pts]
    rows = []
    for k, (x, y) in enumerate(P):
        f = ["Linear = true", "X = %s" % lua(x), "Y = %s" % lua(y)]
        if k > 0:
            px, py = P[k - 1]
            f += ["LX = %s" % lua((px - x) / 3), "LY = %s" % lua((py - y) / 3)]
        if k < len(P) - 1:
            nx, ny = P[k + 1]
            f += ["RX = %s" % lua((nx - x) / 3), "RY = %s" % lua((ny - y) / 3)]
        rows.append("\t\t\t\t\t\t\t{ %s }," % ", ".join(f))
    return "Polyline {\n\t\t\t\t\t\tPoints = {\n%s\n\t\t\t\t\t\t}\n\t\t\t\t\t}" % "\n".join(rows)


def box_times(i):
    l0 = 30 + i * STAGGER                     # line starts drawing
    return dict(l0=l0, l1=l0 + 14, b0=l0 + 10, b1=l0 + 28, g0=l0 + 16, g1=l0 + 32, s0=l0 + 28, s1=l0 + 44)


LX, LY = -550, 1000
background("Background_Lines", (0, 0, 0), (LX, LY), a=0.0)
prev = "Background_Lines"
for i in range(4):
    n = i + 1
    t = box_times(i)
    x = LX + 110 * n
    pl = "Polygon_Line%dPolyline" % n
    tools.append((pl, '\t\t%s = BezierSpline {\n\t\t\tSplineColor = { Red = 173, Green = 255, Blue = 47 },\n\t\t\tNameSet = true,\n\t\t\tKeyFrames = {\n\t\t\t\t[0] = { 0, Flags = { Linear = true, LockedY = true }, Value = %s }\n\t\t\t}\n\t\t},'
                  % (pl, polyline(line_points(i)))))
    tool("Polygon_Line%d" % n, "PolylineMask", {**MASKF, "BorderWidth": 0.0019, "Solid": 0,
         "Polyline": link(pl, "Value")}, (x, LY - 66), extra='\t\t\tDrawMode = "ClickAppend",\n\t\t\tDrawMode2 = "InsertAndModify",\n')
    tools.append(("Shake_Line%d" % n, '\t\tShake_Line%d = Shake {\n\t\t\tFaster = true,\n\t\t\tInputs = {\n\t\t\t\tSmoothness = Input { Value = 25, },\n\t\t\t\tXMinimum = Input { Value = 1, },\n\t\t\t\tXMaximum = Input { Value = 2, }\n\t\t\t},\n\t\t},' % n))
    wo = anim("PolylineStroke_Line%dWriteOnEnd" % n, [(t["l0"], 0.0), (t["l1"], 1.0)])
    tools.append(("PolylineStroke_Line%d" % n, '\t\tPolylineStroke_Line%d = PolylineStroke {\n\t\t\tPoints = {\n\t\t\t},\n\t\t\tIsThreaded = true,\n\t\t\tBrushes = {\n\t\t\t\t"SoftBrush",\n\t\t\t\t"CircleBrush"\n\t\t\t},\n\t\t\tApplyModes = { "PaintApplyColor" },\n\t\t\tInputs = {\n\t\t\t\t%s\n\t\t\t},\n\t\t},'
                  % (n, inp({"BrushControls": 1, "BrushShape": "FuID:CircleBrush", "StrokeControls": 1,
                             "Spacing": link("Shake_Line%d" % n, "X"), "Polyline": link(pl, "Value"),
                             "CircleBrush.Size": 0.0111, "PaintApplyColor.Red": ACC[0], "PaintApplyColor.Green": ACC[1],
                             "PaintApplyColor.Blue": ACC[2], "WriteOnEnd": wo}))))
    tool("Paint_Line%d" % n, "Paint", {"Input": link(prev), "Paint": link("PolylineStroke_Line%d" % n, "Out"),
         "EffectMask": link("Polygon_Line%d" % n, "Mask")}, (x, LY))
    prev = "Paint_Line%d" % n
macro(NEO, "Neo Glow.setting", "NeoGlow", "NeoGlow_Lines", (LX + 550, LY), "_LN")

# ------------------------------------------------------------ the four boxes
COL_Y = 600
merge("Merge_LinesOverComp", "Plate_Test", None, (-110, COL_Y))
last = "Merge_LinesOverComp"

for i, (key, label, tile) in enumerate(TOOLS):
    n = i + 1
    t = box_times(i)
    GX, GY = -550, 1550 + i * 600            # each box's nodes in their own area
    cx, cy = XS[i], BOX_CY
    left, top = cx - BOX / 2, cy - BOX / 2
    P = lambda dx, dy: (GX + dx, GY + dy)

    tool("Rectangle_Box%d" % n, "RectangleMask", {**MASKF, "Center": (fx(cx), fy(cy)), "Width": BOX / W,
         "Height": BOX / H, "CornerRadius": 0.22}, P(0, -44))
    background("Background_BoxFill%d" % n, FILL, P(0, 0), mask="Rectangle_Box%d" % n, a=0.94)
    tools.append(("Instance_Rectangle_Box%d" % n, '\t\tInstance_Rectangle_Box%d = RectangleMask {\n\t\t\tSourceOp = "Rectangle_Box%d",\n\t\t\tInputs = {\n\t\t\t\tSolid = Input { Value = 0, },\n\t\t\t\tBorderWidth = Input { Value = 0.00184, },\n\t\t\t\tEffectMask = Input { },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { %d, %d } },\n\t\t},' % ((n, n) + P(110, -132))))
    background("Background_BoxBorder%d" % n, ACC, P(110, -99), mask="Instance_Rectangle_Box%d" % n)
    macro(NEO, "Neo Glow.setting", "NeoGlow", "NeoGlow_BoxBorder%d" % n, P(110, -60), "_BB%d" % n)
    merge("Merge_BoxBorder%d" % n, "Background_BoxFill%d" % n, None, P(110, 0))


    # icon + name on their own layer, hidden under MosaicBlur
    background("Background_Content%d" % n, (0, 0, 0), P(330, -154), a=0.0)
    loader("Loader_Logo%d" % n, os.path.join(TILES, tile), P(440, -220))
    tool("DropShadow_Logo%d" % n, "ofx.com.blackmagicdesign.resolvefx.DropShadow",
         {"Source": link("Loader_Logo%d" % n), "shadowStrength": 0.45, "ShadowDistance": 0.03, "shadowBlur": 0.5}, P(440, -187))
    merge("Merge_Logo%d" % n, "Background_Content%d" % n, "DropShadow_Logo%d" % n, P(440, -154),
          center=(fx(cx), fy(cy - 28)), size=128 / 1024.0)
    text("Text_Name%d" % n, label, "Bold", 0.029, WHITE, (fx(cx), fy(cy + 88)), P(550, -187), spacing=1.04)
    merge("Merge_Name%d" % n, "Merge_Logo%d" % n, "Text_Name%d" % n, P(550, -154))
    tool("MosaicBlur_Content%d" % n, "ofx.com.blackmagicdesign.resolvefx.MosaicBlur",
         {"Source": link("Merge_Name%d" % n), "PixelFrequency": 100}, P(550, -99))
    merge("Merge_Content%d" % n, "Merge_BoxBorder%d" % n, "MosaicBlur_Content%d" % n, P(550, 0))

    # static shine at the centre, then the moving shine (BrightnessContrast + inclined rectangle)
    def sweep_centre(block, cx=cx, cy=cy):
        return block.replace("\t\t\t\t\t\tAngle = Input { Value = -40, }\n",
                             "\t\t\t\t\t\tAngle = Input { Value = -40, },\n\t\t\t\t\t\tCenter = Input { Value = { %s, %s }, },\n" % (lua(fx(cx)), lua(fy(cy))), 1)
    macro(NEO, "Neo Light Sweep Pro.setting", "NeoLightSweepPro", "NeoLightSweepPro_Box%d" % n, P(660, 0), "_SW%d" % n, patch=sweep_centre)
    tool("Rectangle_Shine%d" % n, "RectangleMask", {**MASKF, "Width": 0.022, "Height": 0.42, "Angle": -18.0, "SoftEdge": 0.012,
         "Center": xypath("Rectangle_Shine%dCenter" % n, anim("Rectangle_Shine%dCenterX" % n,
                                                                   [(t["s0"], fx(left - 40)), (t["s1"], fx(left + BOX + 40))]), fy(cy))},
         P(770, -60))
    tool("BrightnessContrast_Shine%d" % n, "BrightnessContrast", {"Gain": 1.9, "Brightness": 0.06, "PreDividePostMultiply": 1,
         "EffectMask": link("Rectangle_Shine%d" % n, "Mask")}, P(770, 0))

    # entrance: slide up + settle, motion blur; fade with his Opacity macro
    tool("Transform_BoxIn%d" % n, "Transform", {"Input": link("BrightnessContrast_Shine%d" % n), **MB,
         "Pivot": (fx(cx), fy(cy)),
         "Center": xypath("Transform_BoxIn%dCenter" % n, 0.5, anim("Transform_BoxIn%dCenterY" % n, [(t["b0"], 0.44), (t["b1"], 0.5)])),
         "Size": anim("Transform_BoxIn%dSize" % n, [(t["b0"], 0.92), (t["b1"], 1.0)])}, P(880, 0))
    macro(MINE, "Opacity.setting", "Opacity", "Opacity_Box%d" % n, P(990, 0), "_OB%d" % n,
          patch=opacity_patch("Opacity_Box%dGain" % n, [(t["b0"], 0.0), (t["b0"] + 8, 1.0)]))
    tool("DropShadow_Box%d" % n, "ofx.com.blackmagicdesign.resolvefx.DropShadow",
         {"shadowStrength": 0.55, "ShadowDistance": 0.02, "shadowBlur": 0.7, "shadowAngle": 90}, P(1100, 0))

    # number badge on the top-left corner
    bx, by, bd = left + 10, top + 10, 74
    tool("Ellipse_Badge%d" % n, "EllipseMask", {**MASKF, "Center": (fx(bx), fy(by)), "Width": bd / W, "Height": bd / W}, P(1100, -264))
    background("Background_BadgeFill%d" % n, WHITE, P(1100, -198), mask="Ellipse_Badge%d" % n)
    tools.append(("Instance_Ellipse_Badge%d" % n, '\t\tInstance_Ellipse_Badge%d = EllipseMask {\n\t\t\tSourceOp = "Ellipse_Badge%d",\n\t\t\tInputs = {\n\t\t\t\tSolid = Input { Value = 0, },\n\t\t\t\tBorderWidth = Input { Value = 0.0022, },\n\t\t\t\tEffectMask = Input { },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { %d, %d } },\n\t\t},' % ((n, n) + P(1210, -330))))
    background("Background_BadgeBorder%d" % n, ACC, P(1210, -297), mask="Instance_Ellipse_Badge%d" % n)
    macro(NEO, "Neo Glow.setting", "NeoGlow", "NeoGlow_Badge%d" % n, P(1210, -264), "_BG%d" % n)
    merge("Merge_BadgeBorder%d" % n, "Background_BadgeFill%d" % n, None, P(1210, -198))
    text("Text_Number%d" % n, str(n), "Black", 0.05, ACC, (fx(bx), fy(by)), P(1320, -231))
    merge("Merge_Number%d" % n, "Merge_BadgeBorder%d" % n, "Text_Number%d" % n, P(1320, -198))
    tool("DropShadow_Badge%d" % n, "ofx.com.blackmagicdesign.resolvefx.DropShadow",
         {"Source": link("Merge_Number%d" % n), "shadowStrength": 0.5, "ShadowDistance": 0.012, "shadowBlur": 0.6, "shadowAngle": 90}, P(1320, -154))
    tool("Transform_BadgeIn%d" % n, "Transform", {"Input": link("DropShadow_Badge%d" % n), **MB, "Pivot": (fx(bx), fy(by)),
         "Size": anim("Transform_BadgeIn%dSize" % n, [(t["g0"], 0.0), (t["g0"] + 10, 1.12), (t["g1"], 1.0)]),
         "Angle": anim("Transform_BadgeIn%dAngle" % n, [(t["g0"], -40.0), (t["g1"], 0.0)])}, P(1320, -99))
    merge("Merge_Badge%d" % n, "DropShadow_Box%d" % n, "Transform_BadgeIn%d" % n, P(1320, 0))

    merge("Merge_Box%dOverComp" % n, last, "Merge_Badge%d" % n, (110 * n - 110 + 110, COL_Y))
    last = "Merge_Box%dOverComp" % n

PASTE = [nm for nm, _ in tools]

# wiring that doesn't survive paste/import (links into and out of macros) -> done by script
WIRING = []
for n in range(1, 5):
    WIRING += [("NeoGlow_BoxBorder%d" % n, "MainInput1", "Background_BoxBorder%d" % n),
               ("Merge_BoxBorder%d" % n, "Foreground", "NeoGlow_BoxBorder%d" % n),
               ("NeoLightSweepPro_Box%d" % n, "MainInput1", "Merge_Content%d" % n),
               ("BrightnessContrast_Shine%d" % n, "Input", "NeoLightSweepPro_Box%d" % n),
               ("Opacity_Box%d" % n, "MainInput1", "Transform_BoxIn%d" % n),
               ("DropShadow_Box%d" % n, "Source", "Opacity_Box%d" % n),
               ("NeoGlow_Badge%d" % n, "MainInput1", "Background_BadgeBorder%d" % n),
               ("Merge_BadgeBorder%d" % n, "Foreground", "NeoGlow_Badge%d" % n)]
WIRING += [("NeoGlow_Lines", "MainInput1", "Paint_Line4"), ("Merge_LinesOverComp", "Foreground", "NeoGlow_Lines")]

# test-only plate + output
loader("Plate_Test", PLATE, (-110, COL_Y + 66))
tools.append(("MediaOut1", '\t\tMediaOut1 = MediaOut {\n\t\t\tInputs = {\n\t\t\t\tIndex = Input { Value = "0", },\n\t\t\t\tInput = Input { SourceOp = "%s", Source = "Output", },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { 660, 214 } },\n\t\t},' % last))

body = "\n".join(t for _, t in tools)
open(os.path.join(HERE, "tool_boxes.comp"), "w", encoding="utf-8").write(
    'Composition {\n\tCurrentTime = 100,\n\tRenderRange = { 0, %d },\n\tGlobalRange = { 0, %d },\n\tPrefs = {\n\t\tComp = {\n\t\t\tFrameFormat = { Width = 1920, Height = 1080, Rate = 23.976, },\n\t\t},\n\t},\n\tTools = ordered() {\n%s\n\t},\n}\n' % (END, END, body))
paste = [t.replace('Background = Input { SourceOp = "Plate_Test", Source = "Output", },', "") for nm, t in tools if nm in PASTE]
open(os.path.join(HERE, "tool_boxes_paste.setting"), "w", encoding="utf-8").write(
    '{\n\tTools = ordered() {\n%s\n\t},\n\tActiveTool = "%s"\n}\n' % ("\n".join(paste), last))
open(os.path.join(HERE, "tool_boxes_wiring.txt"), "w").write(repr(WIRING))
open(os.path.join(HERE, "tool_boxes_names.txt"), "w").write(",".join(n for n in PASTE))
print(len(PASTE), "paste tools;", len(WIRING), "wires; last =", last)
for i in range(4):
    print(TOOLS[i][0], box_times(i))
