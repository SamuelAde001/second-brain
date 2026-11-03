import re
txt = open("samuel_all.md", encoding="utf-8").read()
blocks = re.split(r"\n(?=### 20)", txt)
kw = re.compile(r"resolve|fusion|timeline|visual|edit|render|clip|node|comp\b|comps|font|colou?r|zoom|b-?roll|sfx|sound|music|transition|animation|motion|routerise|route rise|alex|frontal|gamma|marker|intro|cut|subtitle|transcript|glow|blur|highlight|pill|box|card|screen ?record|tella|graphic|text|keyframe|adjustment|editor|video|frame|creative director|ifeoma|reference|style|cache|drive", re.I)
keep = [b for b in blocks if kw.search(b)]
# drop huge pastes over 6000 chars to a separate file
big = [b for b in keep if len(b) > 6000]
small = [b for b in keep if len(b) <= 6000]
open("samuel_video.md","w",encoding="utf-8").write("\n".join(small))
open("samuel_video_big.md","w",encoding="utf-8").write("\n".join(big))
print(len(blocks), len(small), sum(map(len,small)), len(big), sum(map(len,big)))
for b in big: print(b[:120].replace("\n"," | "))
