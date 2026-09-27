"""Neo Anim copies for the five tool windows (Route Rise #3, Cut v6 marker 846-999, 2026-09-27).

python gen_window_stack.py <out.setting>
Five fresh Neo Anim macros from the Neo folder, inner tools suffixed _W1.._W5, macros named
NeoAnim_Win1..5, Out off (short comp), Angle off (the macro's own off state: NAAngle pass-through,
ToggleControls Angle 0). Timing and GlobalSize are set by script after the paste.
"""
import re, os, sys
NEO = os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\Neo folder\Neo Anim.setting")
s = open(NEO, encoding="utf-8").read()
a = s.index("Tools = ordered() {") + len("Tools = ordered() {")
z = s.rindex("\n\t}")
body = s[a:z]
tops = set(re.findall(r"\n\t\t(\w+) = [\w.]+ \{", body))
k = body.find("\n\t\t\tTools = ordered() {")
inner = set(re.findall(r"\n\t\t\t\t(\w+) = (?!Instance|Input\b)[\w.]+ \{", body[k:]))
names = (tops | inner) - {"NeoAnim"}

def rename(text, sfx, macro):
    new = lambda n: macro if n == "NeoAnim" else (n + sfx if n in names else n)
    text = re.sub(r"(\n\t+)(\w+)( = (?!Instance)[\w.]+ \{)", lambda m: m.group(1) + new(m.group(2)) + m.group(3), text)
    text = re.sub(r'SourceOp = "(\w+)"', lambda m: 'SourceOp = "%s"' % new(m.group(1)), text)
    text = re.sub(r'Expression = "[^"]*"', lambda m: re.sub(r"\b(\w+)\.", lambda q: new(q.group(1)) + ".", m.group(0)), text)
    return text

def tweak(b, sfx):
    # Out off
    b = b.replace("In = Input { Value = 1, },\n\t\t\t\t\t\tOut = Input { Value = 1, }", "In = Input { Value = 1, },\n\t\t\t\t\t\tOut = Input { Value = 0, }")
    # Angle off: NAAngle pass-through + ToggleControls Angle 0
    b = b.replace("NAAngle%s = Transform {\n" % sfx, "NAAngle%s = Transform {\n\t\t\t\t\tPassThrough = true,\n" % sfx, 1)
    i = b.index("ToggleControls%s = AlphaDivide {" % sfx)
    j = b.index("Angle = Input {", i)
    b = b[:j] + b[j:].replace("Value = 1", "Value = 0", 1)
    # PreXF input points at a Text1 that doesn't exist: strip it
    b = re.sub(r'\n\t+Input = Input \{\s*SourceOp = "Text1\w*",\s*Source = "Output",\s*\},?', "", b)
    return b

out = []
for n in range(1, 6):
    sfx = "_W%d" % n
    b = tweak(rename(body, sfx, "NeoAnim_Win%d" % n), sfx)
    b = re.sub(r"(\n\t\t\tViewInfo = GroupInfo \{\s*Pos = \{ )[^}]*\}", r"\g<1>%d, 0 }" % (n * 220), b)
    out.append(b.rstrip().rstrip(","))
txt = "{\n\tTools = ordered() {%s\n\t},\n}\n" % ",".join(out)
open(sys.argv[1], "w", encoding="utf-8").write(txt)
print(len(txt), "bytes;", "Out=1 left:", txt.count("Out = Input { Value = 1, }"),
      "; NAAngle passthrough:", len(re.findall(r"NAAngle_W\d = Transform \{\n\t+PassThrough = true", txt)),
      "; unsuffixed SourceOps:", set(re.findall(r'SourceOp = "(\w+)"', txt)) - set(re.findall(r"\n\t*(\w+) = [\w.]+ \{", txt)),
      "; Text1 refs:", txt.count("Text1"))
