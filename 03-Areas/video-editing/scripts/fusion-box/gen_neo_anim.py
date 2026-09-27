"""Fresh Neo Anim macros for pasting (2026-09-27, four-tools comp, Route Rise #3).

Takes Neo Anim.setting from the Neo folder, including its outer AnimCurves modifiers, and
suffixes every tool name per instance (_NA1.._NA4) so copies don't cross-wire. Writes
na_paste.setting to the cwd; paste it via the clipboard + comp.Paste(), then set values by
script (see the Editor memory for the settings used).
"""
import re,os
NEO=os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\Neo folder\Neo Anim.setting")
s=open(NEO,encoding="utf-8").read()
def rename_all(text, names, special):
    new = lambda n: special.get(n) or (n + SFX if n in names else n)
    text = re.sub(r"(\n\t+)(\w+)( = (?!Instance)[\w.]+ \{)", lambda m: m.group(1) + new(m.group(2)) + m.group(3), text)
    text = re.sub(r'SourceOp = "(\w+)"', lambda m: 'SourceOp = "%s"' % new(m.group(1)), text)
    text = re.sub(r'Expression = "[^"]*"', lambda m: re.sub(r"\b(\w+)\.", lambda k: new(k.group(1)) + ".", m.group(0)), text)
    return text
a=s.index("Tools = ordered() {")+len("Tools = ordered() {")
# end of the top-level Tools table: find ActiveTool or last "\n\t},"
z=s.rindex("\n\t}")
body=s[a:z]
tops=set(re.findall(r"\n\t\t(\w+) = [\w.]+ \{",body))
k=body.find("\n\t\t\tTools = ordered() {")
inner=set(re.findall(r"\n\t\t\t\t(\w+) = (?!Instance|Input\b)[\w.]+ \{", body[k:]))
nested=set(re.findall(r"\n\t\t\t\t(\w+Lookup\w*) = LUTBezier \{", body))
names=(tops|inner|nested)-{"NeoAnim"}
TIMES=[35,38,42,46]
out=[]
for n,t0 in enumerate(TIMES,1):
    SFX="_NA%d"%n
    b=rename_all(body,names,{"NeoAnim":"NeoAnim_Tool%d"%n})
    b=re.sub(r"(\n\t\t\tViewInfo = GroupInfo \{\s*Pos = \{ )[^}]*\}", r"\g<1>0, %d }"%(n*66), b)
    out.append(b.rstrip().rstrip(","))
open("na_paste.setting","w",encoding="utf-8").write("{\n\tTools = ordered() {%s\n\t},\n}\n"%",".join(out))
txt=open("na_paste.setting",encoding="utf-8").read()
print(len(txt), sorted(names)[:40])
print(re.findall(r"\n\t\t(\w+) = [\w.]+ \{",txt))
# sanity: any leftover unsuffixed SourceOp
print(set(re.findall(r'SourceOp = "(\w+)"',txt)) - set(re.findall(r"\n\t+(\w+) = [\w.]+ \{",txt)))
