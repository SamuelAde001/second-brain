"""List the visual events on a Resolve timeline, for SFX placement (external Python; Resolve running).

python sfx_events.py "<timeline>" <scratch_dir> <out.json>

Events:
- every enabled clip start on V2 and above (kind from the clip: ui / broll / comp / adjustment / generator)
- inside every Fusion comp on those clips: each Neo Anim "InOffset" and each NeoTextMotion "InOffsetF" (element lands),
  named after the tool (NeoAnim_Pill*, NeoAnim_Hub*, NeoAnim_Card*, NeoTextMotion_*), mapped to timeline frames.
Comps are exported to <scratch_dir>/sfxcomps/ to read them; nothing on the timeline is changed.
"""
import sys, os, re, json
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr

resolve = dvr.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()
name, scratch, outp = sys.argv[1], sys.argv[2], sys.argv[3]
tl = next(project.GetTimelineByIndex(i) for i in range(1, project.GetTimelineCount() + 1) if project.GetTimelineByIndex(i).GetName() == name)
ST = tl.GetStartFrame()
cdir = os.path.join(scratch, "sfxcomps")
os.makedirs(cdir, exist_ok=True)

TOP = re.compile(r"\n\t\t(\w+) = ([\w.]+) \{")


def comp_events(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    tops = [(m.start(), m.group(1), m.group(2)) for m in TOP.finditer(s)]
    ev = []
    for i, (p, n, t) in enumerate(tops):
        blk = s[p: tops[i + 1][0] if i + 1 < len(tops) else len(s)]
        if t == "MacroOperator" and "NeoAnim" in n or re.search(r"\bGlobalAnim\b", blk) and t == "MacroOperator":
            m = re.search(r"\n\t+InOffset = Input \{ Value = (-?[\d.]+)", blk)
            on = re.search(r"\n\t\t\t\tIn = Input \{ Value = 0,", blk)
            if m and not on:
                ev.append((n, "neoanim", float(m.group(1))))
        elif t in ("NeoMotionText",) or n.startswith("NeoTextMotion"):
            m = re.search(r"\n\t+InOffsetF = Input \{ Value = (-?[\d.]+)", blk)
            if m:
                ev.append((n, "text", float(m.group(1))))
    return ev


events = []
SKIP = {4, 8}   # V4 = his disabled Tella pieces, V8 = A-roll duplicate: cut-driven, never SFX
for tr in range(2, tl.GetTrackCount("video") + 1):
    if tr in SKIP or not tl.GetIsTrackEnabled("video", tr):
        continue
    for it in tl.GetItemListInTrack("video", tr) or []:
        if not it.GetClipEnabled():
            continue
        s, e = it.GetStart() - ST, it.GetEnd() - ST
        nm = it.GetName()
        events.append({"f": s, "end": e, "tr": tr, "clip": nm, "kind": "clipstart"})
        if it.GetFusionCompCount() > 0:
            p = os.path.join(cdir, "V%d_%d.comp" % (tr, s))
            if not os.path.exists(p):
                it.ExportFusionComp(p, 1)
            try:
                lo = int(round(it.GetLeftOffset(False) or 0))
            except Exception:
                lo = 0
            for tool, k, t in comp_events(p):
                f = s + int(round(t)) - lo
                if s + 1 < f < e:
                    events.append({"f": f, "end": e, "tr": tr, "clip": nm, "kind": k, "tool": tool, "clipstart": s})
events.sort(key=lambda x: x["f"])
json.dump(events, open(outp, "w", encoding="utf-8"), indent=0)
print("events", len(events))
