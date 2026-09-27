"""Four pills + Arrowlines + circle heading for Route Rise #3 (orange-circle comp, 2026-09-27).

Samuel's asks: pills stacked and well spaced; solid black Flaticon icons used as masks on an
orange Background (no tile behind them); NeoTextMotion on every text; his Arrowline macro
(line write-on + arrow-right.png head riding the path) from ONE point on the circle to each
pill; a NeoTextMotion heading inside the circle. Each pill lands on its phrase.

His own pill parts are copied from his finished four-box comp (NeoAnim, NeoTextMotion, Light
Sweep settings), so the motion and text styling are his, not re-invented. Each pill is built
at frame centre and placed by its NeoAnim's GlobalXF, the way he builds pills.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEO = os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\Neo folder")
ASSETS = r"C:\Users\repzy\Desktop\Video edits\Routerise\Visual Assets\Assets"
JOB = r"C:\Users\repzy\Desktop\Video edits\Routerise\3. I Tried 100+ AI Tools. These 4 Are Best for Businesses\Graphics\Circle pills"
SCRATCH = sys.argv[1]                                 # session scratchpad (his comps + plate)
FINAL = os.path.join(SCRATCH, "SAMUEL_final_Composition2.comp")   # his finished four-box comp
PLATE = os.path.join(SCRATCH, "circ_560_2.6.1.jpg")
OUT = os.path.join(SCRATCH, "circle_pills")
os.makedirs(OUT, exist_ok=True)

END = 196
W, H = 1920.0, 1080.0
ACC = (1.0, 0.3529, 0.1216)        # #FF5A1F
FILL = (0.1059, 0.0353, 0.0118)    # accent x 0.10
WHITE = (1.0, 1.0, 1.0)

CIRCLE = (302, 540, 242)           # his circle after its NeoAnim settles (px centre, radius)
ORIGIN = (CIRCLE[0] + CIRCLE[2] + 6, 540)      # every arrow leaves from here
PILLS = [("RESEARCHING ACCOUNTS", os.path.join(ASSETS, "search.png")),
         ("PERSONALIZED LEAD MAGNET", os.path.join(ASSETS, "target.png")),
         ("CLAUDE + BUSINESS CONTEXT", os.path.join(JOB, "claude-black.png")),
         ("INSTRUCTING WITH VOICE", os.path.join(ASSETS, "voice-recognition.png"))]
PX0, PW, PH = 840, 960, 136        # pill left edge, width, height (px)
PYS = [225, 435, 645, 855]         # pill centres (px from top)
ARROW_T0 = [8, 44, 96, 144]        # comp frames: arrow starts; each phrase starts at 0/46/98/146
HEADING = "4 TOOLS"


def fx(px): return px / W
def fy(py): return 1.0 - py / H


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
        if isinstance(v, dict) and "expr" in v:
            out.append('%s = Input { Value = %s, Expression = "%s", },' % (key, lua(v["value"]), v["expr"]))
        elif isinstance(v, dict):
            out.append('%s = Input { SourceOp = "%s", Source = "%s", },' % (key, v["src"], v["out"]))
        else:
            out.append("%s = Input { Value = %s, }," % (key, lua(v)))
    return "\n\t\t\t\t".join(out)


def tool(name, kind, inputs, pos, extra=""):
    view = "\t\t\tViewInfo = OperatorInfo { Pos = { %d, %d } },\n" % pos if pos else ""
    tools.append((name, "\t\t%s = %s {\n%s\t\t\tInputs = {\n\t\t\t\t%s\n\t\t\t},\n%s\t\t},"
                  % (name, kind, extra, inp(inputs), view)))


def spline(name, keys):
    """keys: (frame, value, lh, rh, linear) with lh/rh = (t, v) or None."""
    kf = []
    for t, v, lh, rh, lin in keys:
        parts = [lua(float(v))]
        if lh:
            parts.append("LH = { %s, %s }" % (lua(float(lh[0])), lua(float(lh[1]))))
        if rh:
            parts.append("RH = { %s, %s }" % (lua(float(rh[0])), lua(float(rh[1]))))
        if lin:
            parts.append("Flags = { Linear = true }")
        kf.append("\t\t\t\t[%d] = { %s }," % (t, ", ".join(parts)))
    tools.append((name, "\t\t%s = BezierSpline {\n\t\t\tSplineColor = { Red = 255, Green = 128, Blue = 0 },\n\t\t\tNameSet = true,\n\t\t\tKeyFrames = {\n%s\n\t\t\t}\n\t\t},"
                  % (name, "\n".join(kf))))
    return link(name, "Value")


def ease(name, t0, t1, v0, v1):
    """Leaves fast, lands soft."""
    d = t1 - t0
    return spline(name, [(t0, v0, None, (t0 + d / 3.0, v0 + (v1 - v0) * 0.85), False),
                         (t1, v1, (t1 - d / 3.0, v1), None, False)])


def xypath(name, x, y):
    def f(v):
        return 'Input { SourceOp = "%s", Source = "Value", }' % v["src"] if isinstance(v, dict) else "Input { Value = %s, }" % lua(v)
    tools.append((name, '\t\t%s = XYPath {\n\t\t\tShowKeyPoints = false,\n\t\t\tDrawMode = "ModifyOnly",\n\t\t\tNameSet = true,\n\t\t\tInputs = {\n\t\t\t\tX = %s,\n\t\t\t\tY = %s,\n\t\t\t},\n\t\t},'
                  % (name, f(x), f(y))))
    return link(name, "Value")


def rename_all(text, names, sfx, special=None):
    """Rename tools where they are defined, linked (SourceOp) or used in expressions only,
    so published control names (InstanceInput keys) are left alone."""
    special = special or {}
    new = lambda n: special.get(n, n + sfx) if n in names else n
    text = re.sub(r"(\n\t+)(\w+)( = (?!Instance)[\w.]+ \{)", lambda m: m.group(1) + new(m.group(2)) + m.group(3), text)
    text = re.sub(r'SourceOp = "(\w+)"', lambda m: 'SourceOp = "%s"' % new(m.group(1)), text)
    return re.sub(r'Expression = "[^"]*"',
                  lambda m: re.sub(r"\b(\w+)\.", lambda k: new(k.group(1)) + ".", m.group(0)), text)


def inner_tools(block):
    """Tool names inside a macro's Tools = ordered() section (none for a plain tool)."""
    k = block.find("\n\t\t\tTools = ordered() {")
    if k < 0:
        return set()
    return set(re.findall(r"\n\t\t\t\t(\w+) = (?!Instance|Input\b)[\w.]+ \{", block[k:]))


def macro(folder, file, old, new, pos, sfx):
    """Fresh Neo macro from the Macros folder; inner tool names suffixed per instance."""
    s = open(os.path.join(folder, file), encoding="utf-8").read()
    start = s.index("\t\t%s = MacroOperator {" % old)
    end = s.index("\n\t\t}", start) + 4
    block = s[start:end]
    block = re.sub(r"(\n\t\t\tViewInfo = GroupInfo \{\s*Pos = \{ )[^}]*\}", r"\g<1>%d, %d }" % pos, block)
    block = rename_all(block, inner_tools(block), sfx)
    block = block.replace("\t\t%s = MacroOperator {" % old, "\t\t%s = MacroOperator {" % new, 1)
    tools.append((new, block + ","))


# ---------------------------------------------------------------- copy parts of his comp
_FIN = open(FINAL, encoding="utf-8").read()
_TOPS = [(m.start(), m.group(1)) for m in re.finditer(r"\n\t\t(\w+) = [\w.]+ \{", _FIN)]
_TOPN = {n for _, n in _TOPS}


def _top_block(n):
    i = [k for k, (_, nm) in enumerate(_TOPS) if nm == n][0]
    b = _FIN[_TOPS[i][0]:_TOPS[i + 1][0] if i + 1 < len(_TOPS) else _FIN.index("\n\t},", _TOPS[i][0])]
    return b.rstrip()


def copy_his(root, new, sfx, pos, stop=(), patches=()):
    """Copy one of his tools (+ every top-level tool it references) with unique names."""
    names, todo = [], [root]
    while todo:
        n = todo.pop()
        if n in names or n in stop:
            continue
        names.append(n)
        todo += [x for x in re.findall(r'SourceOp = "(\w+)"', _top_block(n)) if x in _TOPN]
    inner = set()
    for n in names:
        inner |= inner_tools(_top_block(n))
    for n in names:
        b = _top_block(n)
        for st in stop:          # links to tools left behind are wired by script
            b = re.sub(r'\n\t*\w+ = Input \{\s*SourceOp = "%s",\s*Source = "\w+",\s*\},?' % st, "", b)
        b = rename_all(b, set(names) | inner, sfx, {root: new})
        if n == root:
            b = re.sub(r"(\n\t\t\tViewInfo = (?:Group|Operator)Info \{\s*Pos = \{ )[^}]*\}", r"\g<1>%d, %d }" % pos, b)
            for pat, rep in patches:
                b, k = re.subn(pat, rep, b)
                assert k, (new, pat)
        if not b.endswith(","):
            b += ","
        tools.append((new if n == root else n + sfx, b))


FRAME = {"Width": 1920, "Height": 1080, "UseFrameFormatSettings": 1, "GlobalOut": END}
MASKF = {"Filter": "FuID:Fast Gaussian", "MaskWidth": 1920, "MaskHeight": 1080, "PixelAspect": (1, 1),
         "UseFrameFormatSettings": 1, "ClippingMode": "FuID:None"}


def background(name, rgb, pos, mask=None, a=1.0, mask_out="Mask"):
    d = {**FRAME, "TopLeftRed": rgb[0], "TopLeftGreen": rgb[1], "TopLeftBlue": rgb[2], "TopLeftAlpha": a}
    if mask:
        d["EffectMask"] = link(mask, mask_out)
    tool(name, "Background", d, pos)


def textplus(name, s, style, size, rgb, center, pos, opacity=1.0, mask=None):
    d = {**FRAME, "Center": center, "StyledText": s, "Font": "Geist", "Style": style, "Size": size,
         "VerticalJustificationNew": 3, "HorizontalJustificationNew": 3,
         "Red1": rgb[0], "Green1": rgb[1], "Blue1": rgb[2], "Opacity1": opacity}
    if mask:
        d["EffectMask"] = link(mask, "Mask")
    tool(name, "TextPlus", d, pos)


def merge(name, bg, fg, pos, center=None, size=None):
    d = {"PerformDepthMerge": 0}
    if bg:
        d["Background"] = link(bg)
    if fg:
        d["Foreground"] = link(fg)
    if center is not None:
        d["Center"] = center
    if size is not None:
        d["Size"] = size
    tool(name, "Merge", d, pos)


def loader(name, path, pos):
    tool(name, "Loader", {"PostMultiplyByAlpha": 1, "Loop": 1}, pos,
         extra='\t\t\tClips = {\n\t\t\t\tClip {\n\t\t\t\t\tID = "Clip1",\n\t\t\t\t\tFilename = %s,\n\t\t\t\t\tFormatID = "%s",\n\t\t\t\t\tStartFrame = -1,\n\t\t\t\t\tLengthSetManually = true,\n\t\t\t\t\tTrimIn = 0,\n\t\t\t\t\tTrimOut = 0,\n\t\t\t\t\tExtendFirst = 0,\n\t\t\t\t\tExtendLast = %d,\n\t\t\t\t\tLoop = 1,\n\t\t\t\t\tAspectMode = 0,\n\t\t\t\t\tDepth = 0,\n\t\t\t\t\tTimeCode = 0,\n\t\t\t\t\tGlobalStart = 0,\n\t\t\t\t\tGlobalEnd = 0\n\t\t\t\t}\n\t\t\t},\n'
         % (lua(path), "JpegFormat" if path.lower().endswith(".jpg") else "PNGFormat", END))


def neo_text(new, sfx, pos, text, style, size, center, t_in, length, justify=None):
    p = [(r'StyledText = Input \{ Value = "[^"]*", \}', 'StyledText = Input { Value = "%s", }' % text),
         (r'Style = Input \{ Value = "SemiBold", \}', 'Style = Input { Value = "%s", }' % style),
         (r'Size = Input \{ Value = [\d.]+, \}', "Size = Input { Value = %s, }" % lua(size)),
         (r'Center = Input \{ Value = \{ [\d.]+, [\d.]+ \}, \}', "Center = Input { Value = %s, }" % lua(center)),
         (r'InOffsetF = Input \{ Value = \d+, \}', "InOffsetF = Input { Value = %d, }" % t_in),
         (r'InLengthF = Input \{ Value = \d+, \}', "InLengthF = Input { Value = %d, }" % length)]
    if justify is not None:
        p.append((r"(\n\t+)(Size = Input)", r"\1Justify = Input { Value = %d, },\1\2" % justify))
    copy_his("NeoTextMotion1_1_1_1_1_1", new, sfx, pos, patches=p)


# ---------------------------------------------------------------- heading in the circle
MAIN_Y = 150
neo_text("NeoTextMotion_Heading", "_HD", (330, MAIN_Y - 99), HEADING, "ExtraBold", 0.075,
         (fx(CIRCLE[0]), fy(CIRCLE[1])), 2, 22)
merge("Merge_HeadingOverCircle", None, "NeoTextMotion_Heading", (330, MAIN_Y))

# ---------------------------------------------------------------- arrowlines (his macro, rebuilt per arrow)
AX, AY = -1265, 500


def arrow_polyline(end):
    (sx, sy), (ex, ey) = ORIGIN, end
    X = lambda px: (px - W / 2) / W
    Y = lambda py: (H / 2 - py) / H
    dx = (ex - sx) / W
    return ("Polyline {\n\t\t\t\t\t\tPoints = {\n"
            "\t\t\t\t\t\t\t{ X = %s, Y = %s, RX = %s, RY = 0 },\n"
            "\t\t\t\t\t\t\t{ X = %s, Y = %s, LX = %s, LY = 0 }\n"
            "\t\t\t\t\t\t}\n\t\t\t\t\t}" % (lua(X(sx)), lua(Y(sy)), lua(dx * 0.55), lua(X(ex)), lua(Y(ey)), lua(-dx * 0.55)))


background("Background_ArrowsCanvas", (0, 0, 0), (AX, AY), a=0.0)
prev = "Background_ArrowsCanvas"
for i in range(4):
    n, t0 = i + 1, ARROW_T0[i]
    x = AX + 440 * i
    y = AY + 250
    end = (PX0 - 38 - 22, PYS[i])
    loader("Loader_ArrowHead%d" % n, os.path.join(ASSETS, "arrow-right.png"), (x, y - 132))
    background("Background_ArrowHead%d" % n, WHITE, (x + 110, y - 132), mask="Loader_ArrowHead%d" % n, mask_out="Output")
    size = spline("Transform_ArrowHead%dSize" % n, [(t0, 0, None, (t0 + 1, 0.0206667), True),
                                                    (t0 + 3, 0.062, (t0 + 2, 0.0413333), None, True)])
    tool("Transform_ArrowHeadSize%d" % n, "Transform", {"Size": size, "Input": link("Background_ArrowHead%d" % n)}, (x + 220, y - 132))
    tools.append(("Publish_ArrowPath%d" % n, '\t\tPublish_ArrowPath%d = PublishPolyLine {\n\t\t\tInputs = {\n\t\t\t\tValue = Input {\n\t\t\t\t\tValue = %s,\n\t\t\t\t},\n\t\t\t},\n\t\t},'
                  % (n, arrow_polyline(end))))
    wl = spline("Polyline_Arrow%dLength" % n, [(t0, 0, None, (t0 + 7.6666667, 0), False),
                                              (t0 + 11, 1, (t0 + 3.2222222, 1), None, False)])
    tool("Polyline_Arrow%d" % n, "PolylineMask", {**MASKF, "BorderWidth": 0.0032, "CapStyle": 0, "WriteLength": wl,
         "Polyline": link("Publish_ArrowPath%d" % n, "Value")}, (x + 110, y - 66),
         extra='\t\t\tDrawMode = "InsertAndModify",\n\t\t\tDrawMode2 = "InsertAndModify",\n')
    background("Background_ArrowLine%d" % n, WHITE, (x + 220, y - 66), mask="Polyline_Arrow%d" % n)
    tools.append(("Path_ArrowHead%d" % n, '\t\tPath_ArrowHead%d = PolyPath {\n\t\t\tDrawMode = "InsertAndModify",\n\t\t\tInputs = {\n\t\t\t\tDisplacement = Input { Value = 1, Expression = "Polyline_Arrow%d.WriteLength", },\n\t\t\t\tPolyLine = Input { SourceOp = "Publish_ArrowPath%d", Source = "Value", },\n\t\t\t},\n\t\t},' % (n, n, n)))
    tool("Transform_ArrowHead%d" % n, "Transform", {"Center": link("Path_ArrowHead%d" % n, "Position"),
         "Angle": link("Path_ArrowHead%d" % n, "Heading"), "Input": link("Transform_ArrowHeadSize%d" % n)}, (x + 330, y - 132))
    merge("Merge_Arrow%d" % n, "Transform_ArrowHead%d" % n, "Background_ArrowLine%d" % n, (x + 330, y - 66))
    merge("Merge_Arrow%dOnCanvas" % n, prev, "Merge_Arrow%d" % n, (AX + 110 + 440 * i, AY))
    prev = "Merge_Arrow%dOnCanvas" % n
merge("Merge_ArrowsOverComp", "Merge_HeadingOverCircle", prev, (440, MAIN_Y))

# ---------------------------------------------------------------- the four pills (built at frame centre)
CX, CY = 960, 540
PCX = PX0 + PW / 2
background("Background_PillsCanvas", (0, 0, 0), (-1265, 1000), a=0.0)
prev = "Background_PillsCanvas"
WIRING = []
for i, (label, icon) in enumerate(PILLS):
    n, t0 = i + 1, ARROW_T0[i]
    land, txt, shine = t0 + 6, t0 + 9, t0 + 20
    GX, GY = -1265, 1300 + i * 600
    P = lambda dx, dy: (GX + dx, GY + dy)
    left = CX - PW / 2

    tool("Rectangle_Pill%d" % n, "RectangleMask", {**MASKF, "Width": PW / W, "Height": PH / H, "CornerRadius": 0.3}, P(0, -66))
    background("Background_PillFill%d" % n, FILL, P(0, 0), mask="Rectangle_Pill%d" % n, a=0.94)
    tools.append(("Instance_Rectangle_Pill%d" % n, '\t\tInstance_Rectangle_Pill%d = RectangleMask {\n\t\t\tSourceOp = "Rectangle_Pill%d",\n\t\t\tInputs = {\n\t\t\t\tSolid = Input { Value = 0, },\n\t\t\t\tBorderWidth = Input { Value = 0.00184, },\n\t\t\t\tEffectMask = Input { },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { %d, %d } },\n\t\t},' % ((n, n) + P(110, -165))))
    background("Background_PillBorder%d" % n, ACC, P(110, -132), mask="Instance_Rectangle_Pill%d" % n)
    macro(NEO, "Neo Glow.setting", "NeoGlow", "NeoGlow_PillBorder%d" % n, P(110, -66), "_PB%d" % n)
    merge("Merge_PillBorder%d" % n, "Background_PillFill%d" % n, None, P(110, 0))

    # solid black icon -> placed on a transparent canvas -> mask for an orange Background
    icx = left + 100
    background("Background_IconCanvas%d" % n, (0, 0, 0), P(220, -198), a=0.0)
    loader("Loader_Icon%d" % n, icon, P(330, -264))
    merge("Merge_IconPlace%d" % n, "Background_IconCanvas%d" % n, "Loader_Icon%d" % n, P(330, -198),
          center=(fx(icx), fy(CY)), size=74 / 512.0)
    background("Background_Icon%d" % n, ACC, P(330, -132), mask="Merge_IconPlace%d" % n, mask_out="Output")
    merge("Merge_Icon%d" % n, "Merge_PillBorder%d" % n, "Background_Icon%d" % n, P(330, 0))

    textplus("Text_Ghost%d" % n, str(n), "Black", 0.14, ACC, (fx(left + PW - 42), fy(CY + 6)), P(440, -66),
             opacity=0.16, mask="Rectangle_Pill%d" % n)
    merge("Merge_Ghost%d" % n, "Merge_Icon%d" % n, "Text_Ghost%d" % n, P(440, 0))
    neo_text("NeoTextMotion_Pill%d" % n, "_T%d" % n, P(550, -66), label, "Bold", 0.034,
             (fx(left + 160), fy(CY)), txt, 20, justify=0)
    merge("Merge_Text%d" % n, "Merge_Ghost%d" % n, "NeoTextMotion_Pill%d" % n, P(550, 0))
    copy_his("NeoLightSweepPro_1_1_3_2_1_1", "NeoLightSweep_Pill%d" % n, "_LS%d" % n, P(660, 0), stop=("Displace1_1_1",))

    # number badge on the left edge
    bx = left
    tool("Ellipse_Badge%d" % n, "EllipseMask", {**MASKF, "Center": (fx(bx), fy(CY)), "Width": 76 / W, "Height": 76 / W}, P(770, -264))
    background("Background_BadgeFill%d" % n, WHITE, P(770, -198), mask="Ellipse_Badge%d" % n)
    tools.append(("Instance_Ellipse_Badge%d" % n, '\t\tInstance_Ellipse_Badge%d = EllipseMask {\n\t\t\tSourceOp = "Ellipse_Badge%d",\n\t\t\tInputs = {\n\t\t\t\tSolid = Input { Value = 0, },\n\t\t\t\tBorderWidth = Input { Value = 0.0022, },\n\t\t\t\tEffectMask = Input { },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { %d, %d } },\n\t\t},' % ((n, n) + P(880, -330))))
    background("Background_BadgeBorder%d" % n, ACC, P(880, -297), mask="Instance_Ellipse_Badge%d" % n)
    macro(NEO, "Neo Glow.setting", "NeoGlow", "NeoGlow_Badge%d" % n, P(880, -264), "_BG%d" % n)
    merge("Merge_BadgeBorder%d" % n, "Background_BadgeFill%d" % n, None, P(880, -198))
    textplus("Text_Number%d" % n, str(n), "Black", 0.048, ACC, (fx(bx), fy(CY)), P(990, -231))
    merge("Merge_Number%d" % n, "Merge_BadgeBorder%d" % n, "Text_Number%d" % n, P(990, -198))
    merge("Merge_Badge%d" % n, None, "Merge_Number%d" % n, P(990, 0))

    # moving shine once it has landed: BrightnessContrast + inclined rectangle
    tool("Rectangle_Shine%d" % n, "RectangleMask", {**MASKF, "Width": 0.022, "Height": 0.2, "Angle": -18.0, "SoftEdge": 0.012,
         "Center": xypath("Rectangle_Shine%dCenter" % n, ease("Rectangle_Shine%dX" % n, shine, shine + 10,
                                                              fx(left - 40), fx(left + PW + 40)), 0.5)}, P(1100, -66))
    tool("BrightnessContrast_Shine%d" % n, "BrightnessContrast", {"Gain": 1.9, "Brightness": 0.06, "PreDividePostMultiply": 1,
         "EffectMask": link("Rectangle_Shine%d" % n, "Mask")}, P(1100, 0))
    tool("DropShadow_Pill%d" % n, "ofx.com.blackmagicdesign.resolvefx.DropShadow",
         {"Source": link("BrightnessContrast_Shine%d" % n), "shadowStrength": 0.5, "shadowAngle": 37.5,
          "ShadowDistance": 0.008, "shadowBlur": 0.31}, P(1210, 0))
    copy_his("NeoAnim_1_1_1", "NeoAnim_Pill%d" % n, "_NA%d" % n, P(1320, 0), stop=("DropShadow1_1_1",), patches=[
        (r"InOffset = Input \{ Value = 56, \}", "InOffset = Input { Value = %d, }" % land),
        (r"InLength = Input \{ Value = 25, \}", "InLength = Input { Value = 14, }"),
        (r"StartOffset = Input \{ Value = 0\.44, \}", "StartOffset = Input { Value = 0.12, }"),
        (r"Center = Input \{ Value = \{ 0\.3, 0\.696 \}, \}", "Center = Input { Value = %s, }" % lua((0.5 + (PCX - CX) / W, 0.5 + (CY - PYS[i]) / H)))])
    merge("Merge_Pill%dOnCanvas" % n, prev, None, (-1265 + 110 * n, 1000))
    prev = "Merge_Pill%dOnCanvas" % n

    WIRING += [("NeoGlow_PillBorder%d" % n, "MainInput1", "Background_PillBorder%d" % n),
               ("Merge_PillBorder%d" % n, "Foreground", "NeoGlow_PillBorder%d" % n),
               ("NeoLightSweep_Pill%d" % n, "MainInput1", "Merge_Text%d" % n),
               ("NeoGlow_Badge%d" % n, "MainInput1", "Background_BadgeBorder%d" % n),
               ("Merge_BadgeBorder%d" % n, "Foreground", "NeoGlow_Badge%d" % n),
               ("Merge_Badge%d" % n, "Background", "NeoLightSweep_Pill%d" % n),
               ("BrightnessContrast_Shine%d" % n, "Input", "Merge_Badge%d" % n),
               ("NeoAnim_Pill%d" % n, "MainInput1", "DropShadow_Pill%d" % n),
               ("Merge_Pill%dOnCanvas" % n, "Foreground", "NeoAnim_Pill%d" % n)]
merge("Merge_PillsOverComp", "Merge_ArrowsOverComp", prev, (550, MAIN_Y))
LAST = "Merge_PillsOverComp"
PASTE = [nm for nm, _ in tools]

# test-only plate + output
loader("Plate_Test", PLATE, (220, MAIN_Y))
tools.append(("MediaOut1", '\t\tMediaOut1 = MediaOut {\n\t\t\tInputs = {\n\t\t\t\tIndex = Input { Value = "0", },\n\t\t\t\tInput = Input { SourceOp = "%s", Source = "Output", },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { 770, %d } },\n\t\t},' % (LAST, MAIN_Y)))
TEST_WIRING = WIRING + [("Merge_HeadingOverCircle", "Background", "Plate_Test")]
LIVE_WIRING = WIRING + [("Merge_HeadingOverCircle", "Background", "Merge1"), ("MediaOut1", "Input", LAST)]

body = "\n".join(t for _, t in tools)
open(os.path.join(OUT, "circle_pills_test.comp"), "w", encoding="utf-8").write(
    'Composition {\n\tCurrentTime = 180,\n\tRenderRange = { 0, %d },\n\tGlobalRange = { 0, %d },\n\tPrefs = {\n\t\tComp = {\n\t\t\tFrameFormat = { Width = 1920, Height = 1080, Rate = 23.976, },\n\t\t},\n\t},\n\tTools = ordered() {\n%s\n\t},\n}\n' % (END, END, body))
open(os.path.join(OUT, "circle_pills_paste.setting"), "w", encoding="utf-8").write(
    '{\n\tTools = ordered() {\n%s\n\t},\n\tActiveTool = "%s"\n}\n' % ("\n".join(t for nm, t in tools if nm in PASTE), LAST))
open(os.path.join(OUT, "wiring_test.txt"), "w").write(repr(TEST_WIRING))
open(os.path.join(OUT, "wiring_live.txt"), "w").write(repr(LIVE_WIRING))
open(os.path.join(OUT, "names.txt"), "w").write(",".join(PASTE))
print(len(PASTE), "paste tools;", len(WIRING), "wires; last =", LAST)
