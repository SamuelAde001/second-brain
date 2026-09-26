"""Generate the Claude box as a Fusion .comp (Route Rise house style).

Card = RectangleMask -> Background (accent x 0.10) + Instance rectangle (Solid 0,
border) -> Background (accent) -> NeoGlow. Number badge on the left edge, Claude
tile, two-tone headline, ghost numeral, NeoLightSweepPro, slide-up Transform with
motion blur, DropShadow. One merge spine left -> right.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
MACROS = os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\Neo folder")
LOGO = r"C:\Users\repzy\Desktop\Video edits\Routerise\3. I Tried 100+ AI Tools. These 4 Are Best for Businesses\Graphics\AI tool logos\tiles\01 Claude.png"
PLATE = os.path.join(os.path.dirname(HERE), "comp2_before_2.5.1.jpg")
END = 114
OFF = 26   # Samuel's A-roll card settles at frame 33; the box enters after it

ACC = (1.0, 0.3529, 0.1216)        # #FF5A1F
ACC2 = (0.9922, 0.5804, 0.3412)    # #FD9457
FILL = (0.1059, 0.0353, 0.0118)    # accent x 0.10
WHITE = (1.0, 1.0, 1.0)

CY = 0.7315                        # card centre y (290 px from top)
CARD = dict(cx=0.5, cy=CY, w=0.46875, h=0.1852)       # 900 x 200 px
BADGE = dict(cx=0.2656, cy=CY, w=0.0677, h=0.0677)    # 130 px circle; ellipse height is in width units
LOGO_C = (0.3542, CY)                                 # 680 px
TEXT_X = 0.4010                                       # 770 px


def lua(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(round(v, 6)) if isinstance(v, float) else str(v)
    if isinstance(v, tuple):
        return "{ " + ", ".join(lua(x) for x in v) + " }"
    if isinstance(v, str) and v.startswith("FuID:"):
        return 'FuID { "%s" }' % v[5:]
    return '"%s"' % v.replace("\\", "\\\\").replace('"', '\\"')


tools = []   # (name, text)


def inp(d):
    out = []
    for k, v in d.items():
        key = k if re.fullmatch(r"[A-Za-z_]\w*", k) else '["%s"]' % k
        if isinstance(v, dict) and "src" in v:
            out.append('%s = Input { SourceOp = "%s", Source = "%s", },' % (key, v["src"], v.get("out", "Output")))
        else:
            out.append("%s = Input { Value = %s, }," % (key, lua(v)))
    return "\n\t\t\t\t".join(out)


def tool(name, kind, inputs, pos, extra=""):
    tools.append((name, '\t\t%s = %s {\n%s\t\t\tInputs = {\n\t\t\t\t%s\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { %d, %d } },\n\t\t},'
                  % (name, kind, extra, inp(inputs), pos[0], pos[1])))


def link(src, out="Output"):
    return {"src": src, "out": out}


def spline(name, keys, color=(255, 128, 0)):
    """keys: list of (frame, value). Eased: ease-out on each segment (fast in, soft landing)."""
    keys = [(t + OFF, v) for t, v in keys]
    kf = []
    for i, (t, v) in enumerate(keys):
        parts = [lua(float(v))]
        if i > 0:
            t0, v0 = keys[i - 1]
            parts.append("LH = { %s, %s }" % (lua(t - (t - t0) / 3.0), lua(float(v))))
        if i < len(keys) - 1:
            t1, v1 = keys[i + 1]
            parts.append("RH = { %s, %s }" % (lua(t + (t1 - t) / 3.0), lua(v + (v1 - v) * 0.85)))
        kf.append("\t\t\t\t[%d] = { %s }," % (t, ", ".join(parts)))
    tools.append((name, '\t\t%s = BezierSpline {\n\t\t\tSplineColor = { Red = %d, Green = %d, Blue = %d },\n\t\t\tNameSet = true,\n\t\t\tKeyFrames = {\n%s\n\t\t\t}\n\t\t},'
                  % (name, color[0], color[1], color[2], "\n".join(kf))))
    return link(name, "Value")


def xypath(name, x, y):
    """x, y: constant or link to a spline."""
    def f(v):
        return 'Input { SourceOp = "%s", Source = "Value", }' % v["src"] if isinstance(v, dict) else "Input { Value = %s, }" % lua(v)
    tools.append((name, '\t\t%s = XYPath {\n\t\t\tShowKeyPoints = false,\n\t\t\tDrawMode = "ModifyOnly",\n\t\t\tNameSet = true,\n\t\t\tInputs = {\n\t\t\t\tX = %s,\n\t\t\t\tY = %s,\n\t\t\t},\n\t\t},'
                  % (name, f(x), f(y))))
    return link(name, "Value")


FRAME = {"Width": 1920, "Height": 1080, "UseFrameFormatSettings": 1, "GlobalOut": END}
MASKF = {"Filter": "FuID:Fast Gaussian", "MaskWidth": 1920, "MaskHeight": 1080, "PixelAspect": (1, 1),
         "UseFrameFormatSettings": 1, "ClippingMode": "FuID:None"}
MB = {"MotionBlur": 1, "Quality": 4, "ShutterAngle": 180}


def background(name, rgb, mask, pos, a=1.0):
    tool(name, "Background", {**FRAME, "TopLeftRed": rgb[0], "TopLeftGreen": rgb[1], "TopLeftBlue": rgb[2],
                              "TopLeftAlpha": a, "EffectMask": link(mask, "Mask")}, pos)


def text(name, s, style, size, rgb, center, pos, left=False, spacing=1.0, opacity=1.0, mask=None):
    d = {**FRAME, "Center": center, "StyledText": s, "Font": "Geist", "Style": style, "Size": size,
         "CharacterSpacing": spacing, "VerticalJustificationNew": 3, "HorizontalJustificationNew": 3,
         "Red1": rgb[0], "Green1": rgb[1], "Blue1": rgb[2], "Opacity1": opacity}
    if left:
        d["HorizontalLeftCenterRight"] = -1
    if mask:
        d["EffectMask"] = link(mask, "Mask")
    tool(name, "TextPlus", d, pos)


def merge(name, bg, fg, pos, center=None, size=None, blend=None, mb=False, fgout="Output"):
    d = {"Background": link(bg), "Foreground": link(fg, fgout), "PerformDepthMerge": 0}
    if center is not None:
        d["Center"] = center
    if size is not None:
        d["Size"] = size
    if blend is not None:
        d["Blend"] = blend
    if mb:
        d.update(MB)
    tool(name, "Merge", d, pos)


def macro(file, old, new, pos, patch=None, sfx=""):
    s = open(os.path.join(MACROS, file), encoding="utf-8").read()
    start = s.index("\t\t%s = MacroOperator {" % old)
    end = s.index("\n\t\t}", start) + 4
    block = s[start:end].replace("\t\t%s = MacroOperator {" % old, "\t\t%s = MacroOperator {" % new, 1)
    block = re.sub(r"(\n\t\t\tViewInfo = GroupInfo \{\s*Pos = \{ )[^}]*\}", r"\g<1>%d, %d }" % pos, block)
    if patch:
        block = patch(block)
    if sfx:  # unique inner tool names, so two instances (or Samuel's own Merge1...) never collide
        inner = set(re.findall(r"\n\t\t\t\t(\w+) = (?!Instance)\w+ \{", block))
        block = re.sub(r"(\n\t\t\t\t)(\w+)( = (?!Instance)\w+ \{)",
                       lambda m: m.group(1) + m.group(2) + (sfx if m.group(2) in inner else "") + m.group(3), block)
        block = re.sub(r'SourceOp = "(\w+)"',
                       lambda m: 'SourceOp = "%s%s"' % (m.group(1), sfx if m.group(1) in inner else ""), block)
        block = re.sub(r'Expression = "[^"]*"',
                       lambda m: re.sub(r"\b(\w+)\.", lambda k: k.group(1) + (sfx if k.group(1) in inner else "") + ".", m.group(0)), block)
    tools.append((new, block + ","))


# ---------------- spine y = 0, x left -> right ----------------
Y = 0
# Card fill + border
tool("Rectangle_Card", "RectangleMask", {**MASKF, "Center": (CARD["cx"], CARD["cy"]), "Width": CARD["w"],
     "Height": CARD["h"], "CornerRadius": 0.3}, (-110, -44))
background("Background_CardFill", FILL, "Rectangle_Card", (-110, Y), a=0.94)
tools.append(("Instance_Rectangle_Card", '\t\tInstance_Rectangle_Card = RectangleMask {\n\t\t\tSourceOp = "Rectangle_Card",\n\t\t\tInputs = {\n\t\t\t\tSolid = Input { Value = 0, },\n\t\t\t\tBorderWidth = Input { Value = 0.00184, },\n\t\t\t\tEffectMask = Input { },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { 0, -132 } },\n\t\t},'))
background("Background_CardBorder", ACC, "Instance_Rectangle_Card", (0, -99))
macro("Neo Glow.setting", "NeoGlow", "NeoGlow_CardBorder", (0, -60), sfx="_CB")
merge("Merge_CardBorder", "Background_CardFill", "NeoGlow_CardBorder", (0, Y), fgout="MainOutput1")

# Ghost numeral inside the card
text("Text_Ghost01", "1", "Black", 0.23, ACC, (0.69, 0.715), (110, -44), opacity=0.10, mask="Rectangle_Card")
merge("Merge_Ghost01", "Merge_CardBorder", "Text_Ghost01", (110, Y),
      blend=spline("Merge_Ghost01Blend", [(20, 0), (38, 1)]))

# Claude tile
tool("Loader_ClaudeLogo", "Loader", {"PostMultiplyByAlpha": 1, "Loop": 1}, (220, -99),
     extra='\t\t\tClips = {\n\t\t\t\tClip {\n\t\t\t\t\tID = "Clip1",\n\t\t\t\t\tFilename = %s,\n\t\t\t\t\tFormatID = "PNGFormat",\n\t\t\t\t\tStartFrame = -1,\n\t\t\t\t\tLengthSetManually = true,\n\t\t\t\t\tTrimIn = 0,\n\t\t\t\t\tTrimOut = 0,\n\t\t\t\t\tExtendFirst = 0,\n\t\t\t\t\tExtendLast = %d,\n\t\t\t\t\tLoop = 1,\n\t\t\t\t\tAspectMode = 0,\n\t\t\t\t\tDepth = 0,\n\t\t\t\t\tTimeCode = 0,\n\t\t\t\t\tGlobalStart = 0,\n\t\t\t\t\tGlobalEnd = 0\n\t\t\t\t}\n\t\t\t},\n' % (lua(LOGO), END))
tool("DropShadow_Logo", "ofx.com.blackmagicdesign.resolvefx.DropShadow",
     {"Source": link("Loader_ClaudeLogo"), "shadowStrength": 0.45, "ShadowDistance": 0.03, "shadowBlur": 0.5}, (220, -60))
merge("Merge_Logo", "Merge_Ghost01", "DropShadow_Logo", (220, Y), size=0.125, mb=True,
      center=xypath("Merge_LogoCenter", LOGO_C[0], spline("Merge_LogoCenterY", [(12, CY - 0.03), (30, CY)])),
      blend=spline("Merge_LogoBlend", [(12, 0), (20, 1)]))

# Headline, two-tone: white word, accent line
text("Text_Claude", "CLAUDE", "Bold", 0.085, WHITE, (TEXT_X, CY + 0.022), (330, -99), left=True, spacing=1.04)
tool("Transform_TextClaudeIn", "Transform", {"Input": link("Text_Claude"), **MB,
     "Center": xypath("Transform_TextClaudeInCenter", 0.5, spline("Transform_TextClaudeInCenterY", [(15, 0.47), (33, 0.5)]))}, (330, -60))
merge("Merge_TextClaude", "Merge_Logo", "Transform_TextClaudeIn", (330, Y),
      blend=spline("Merge_TextClaudeBlend", [(15, 0), (23, 1)]))

text("Text_ByAnthropic", "BY ANTHROPIC", "SemiBold", 0.028, ACC2, (TEXT_X, CY - 0.052), (440, -99), left=True, spacing=1.35)
tool("Transform_TextAnthropicIn", "Transform", {"Input": link("Text_ByAnthropic"), **MB,
     "Center": xypath("Transform_TextAnthropicInCenter", 0.5, spline("Transform_TextAnthropicInCenterY", [(18, 0.47), (36, 0.5)]))}, (440, -60))
merge("Merge_TextAnthropic", "Merge_TextClaude", "Transform_TextAnthropicIn", (440, Y),
      blend=spline("Merge_TextAnthropicBlend", [(18, 0), (26, 1)]))


# Shine: NeoLightSweepPro, sweep centre animated inside the macro
def sweep_patch(block):
    path = ('\t\t\t\tPath_SweepCenter = XYPath {\n\t\t\t\t\tShowKeyPoints = false,\n\t\t\t\t\tDrawMode = "ModifyOnly",\n\t\t\t\t\tInputs = {\n'
            '\t\t\t\t\t\tX = Input { SourceOp = "Path_SweepCenterX", Source = "Value", },\n\t\t\t\t\t\tY = Input { Value = %s, },\n\t\t\t\t\t},\n\t\t\t\t},\n'
            '\t\t\t\tPath_SweepCenterX = BezierSpline {\n\t\t\t\t\tSplineColor = { Red = 255, Green = 128, Blue = 0 },\n\t\t\t\t\tKeyFrames = {\n'
            '\t\t\t\t\t\t[60] = { 0.2, RH = { 72, 0.4 } },\n\t\t\t\t\t\t[96] = { 0.85, LH = { 84, 0.7 } }\n\t\t\t\t\t}\n\t\t\t\t},\n') % lua(CY)
    block = block.replace("\t\t\tTools = ordered() {\n", "\t\t\tTools = ordered() {\n" + path, 1)
    return block.replace('\t\t\t\t\t\tAngle = Input { Value = -40, }\n',
                         '\t\t\t\t\t\tAngle = Input { Value = -40, },\n\t\t\t\t\t\tCenter = Input { SourceOp = "Path_SweepCenter", Source = "Value", },\n', 1)


macro("Neo Light Sweep Pro.setting", "NeoLightSweepPro", "NeoLightSweepPro_Card", (550, Y), patch=sweep_patch, sfx="_SW")

# Card entrance: slide up from below, scale 0.96 -> 1, motion blur on
tool("Transform_CardIn", "Transform", {"Input": link("NeoLightSweepPro_Card", "MainOutput1"), **MB,
     "Pivot": (CARD["cx"], CARD["cy"]),
     "Center": xypath("Transform_CardInCenter", 0.5, spline("Transform_CardInCenterY", [(4, 0.44), (26, 0.5)])),
     "Size": spline("Transform_CardInSize", [(4, 0.96), (26, 1.0)])}, (660, Y))
tool("DropShadow_Card", "ofx.com.blackmagicdesign.resolvefx.DropShadow",
     {"Source": link("Transform_CardIn"), "shadowStrength": 0.55, "ShadowDistance": 0.02, "shadowBlur": 0.7, "shadowAngle": 90}, (770, Y))

# Number badge: white circle, accent border + glow, accent "1"
tool("Ellipse_Badge", "EllipseMask", {**MASKF, "Center": (BADGE["cx"], BADGE["cy"]), "Width": BADGE["w"], "Height": BADGE["h"]}, (770, -198))
background("Background_BadgeFill", WHITE, "Ellipse_Badge", (770, -132))
tools.append(("Instance_Ellipse_Badge", '\t\tInstance_Ellipse_Badge = EllipseMask {\n\t\t\tSourceOp = "Ellipse_Badge",\n\t\t\tInputs = {\n\t\t\t\tSolid = Input { Value = 0, },\n\t\t\t\tBorderWidth = Input { Value = 0.0025, },\n\t\t\t\tEffectMask = Input { },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { 880, -264 } },\n\t\t},'))
background("Background_BadgeBorder", ACC, "Instance_Ellipse_Badge", (880, -231))
macro("Neo Glow.setting", "NeoGlow", "NeoGlow_Badge", (880, -198), sfx="_BD")
merge("Merge_BadgeBorder", "Background_BadgeFill", "NeoGlow_Badge", (880, -132), fgout="MainOutput1")
text("Text_Number1", "1", "Black", 0.085, ACC, (BADGE["cx"], BADGE["cy"]), (990, -165))
merge("Merge_Number1", "Merge_BadgeBorder", "Text_Number1", (990, -132))
tool("DropShadow_Badge", "ofx.com.blackmagicdesign.resolvefx.DropShadow",
     {"Source": link("Merge_Number1"), "shadowStrength": 0.5, "ShadowDistance": 0.015, "shadowBlur": 0.6, "shadowAngle": 90}, (990, -99))
tool("Transform_BadgeIn", "Transform", {"Input": link("DropShadow_Badge"), **MB,
     "Pivot": (BADGE["cx"], BADGE["cy"]),
     "Size": spline("Transform_BadgeInSize", [(10, 0.0), (20, 1.1), (26, 1.0)]),
     "Angle": spline("Transform_BadgeInAngle", [(10, -40.0), (26, 0.0)])}, (990, -60))
merge("Merge_Badge", "DropShadow_Card", "Transform_BadgeIn", (990, Y))

# Box over the comp below (BG rewired to Samuel's chain when pasted)
merge("Merge_BoxOverComp", "Plate_Test", "Merge_Badge", (1100, Y),
      blend=spline("Merge_BoxOverCompBlend", [(4, 0), (12, 1)]))

BOX = [n for n, _ in tools]

# Test-only plate + output for the scratch comp
tool("Plate_Test", "Loader", {"Loop": 1}, (1100, 66),
     extra='\t\t\tClips = {\n\t\t\t\tClip {\n\t\t\t\t\tID = "Clip1",\n\t\t\t\t\tFilename = %s,\n\t\t\t\t\tFormatID = "JpegFormat",\n\t\t\t\t\tStartFrame = -1,\n\t\t\t\t\tLengthSetManually = true,\n\t\t\t\t\tTrimIn = 0,\n\t\t\t\t\tTrimOut = 0,\n\t\t\t\t\tExtendFirst = 0,\n\t\t\t\t\tExtendLast = %d,\n\t\t\t\t\tLoop = 1,\n\t\t\t\t\tAspectMode = 0,\n\t\t\t\t\tDepth = 0,\n\t\t\t\t\tTimeCode = 0,\n\t\t\t\t\tGlobalStart = 0,\n\t\t\t\t\tGlobalEnd = 0\n\t\t\t\t}\n\t\t\t},\n' % (lua(PLATE), END))
tools.append(("MediaOut1", '\t\tMediaOut1 = MediaOut {\n\t\t\tInputs = {\n\t\t\t\tIndex = Input { Value = "0", },\n\t\t\t\tInput = Input { SourceOp = "Merge_BoxOverComp", Source = "Output", },\n\t\t\t},\n\t\t\tViewInfo = OperatorInfo { Pos = { 1210, 0 } },\n\t\t},'))

underlay = ('\t\tUnderlay_ClaudeBox = Underlay {\n\t\t\tNameSet = true,\n\t\t\tInputs = {\n\t\t\t\tComments = Input { Value = "CLAUDE BOX (Editor): card + border glow, ghost 01, logo, headline, sweep, slide-in, badge", },\n\t\t\t},\n'
            '\t\t\tViewInfo = UnderlayInfo {\n\t\t\t\tPos = { 440, -110 },\n\t\t\t\tSize = { 1400, 360 }\n\t\t\t},\n\t\t},')
tools.append(("Underlay_ClaudeBox", underlay))
BOX.append("Underlay_ClaudeBox")

body = "\n".join(t for _, t in tools)
comp = ('Composition {\n\tCurrentTime = 40,\n\tRenderRange = { 0, %d },\n\tGlobalRange = { 0, %d },\n\tCurrentID = 1,\n\tPrefs = {\n\t\tComp = {\n\t\t\tFrameFormat = { Width = 1920, Height = 1080, Rate = 23.976, },\n\t\t},\n\t},\n\tTools = ordered() {\n%s\n\t},\n}\n'
        % (END, END, body))
open(os.path.join(HERE, "claude_box.comp"), "w", encoding="utf-8").write(comp)
open(os.path.join(HERE, "box_tools.txt"), "w").write("\n".join(BOX))
print(len(tools), "tools;", len(BOX), "box tools;", len(comp), "bytes")

# ---- Paste version for Samuel's comp: box tools only, moved below his tree ----
DX, DY = -440, 750


def shift(txt):
    txt = re.sub(r"(\n\t\tViewInfo = \w+ \{\s*Pos = \{ )([-\d.]+), ([-\d.]+)",
                 lambda m: "%s%g, %g" % (m.group(1), float(m.group(2)) + DX, float(m.group(3)) + DY), txt)
    txt = re.sub(r"(\n\t\t\tViewInfo = \w+ \{\s*Pos = \{ )([-\d.]+), ([-\d.]+)",
                 lambda m: "%s%g, %g" % (m.group(1), float(m.group(2)) + DX, float(m.group(3)) + DY), txt)
    return txt


paste = []
for n, t in tools:
    if n not in BOX:
        continue
    if n == "Merge_BoxOverComp":
        t = t.replace('Background = Input { SourceOp = "Plate_Test", Source = "Output", },', "")
        t = re.sub(r"Pos = \{ [-\d.]+, [-\d.]+ \}", "Pos = { %d, %d }" % (660 - DX, 330 - DY), t)
    if n == "Underlay_ClaudeBox":
        t = t.replace("Pos = { 440, -110 }", "Pos = { -120, -300 }").replace("Size = { 1400, 360 }", "Size = { 1500, 420 }")
    paste.append(shift(t))
setting = '{\n\tTools = ordered() {\n%s\n\t},\n\tActiveTool = "Merge_BoxOverComp"\n}\n' % "\n".join(paste)
open(os.path.join(HERE, "claude_box_paste.setting"), "w", encoding="utf-8").write(setting)
print("paste:", len(paste), "tools;", len(setting), "bytes")
