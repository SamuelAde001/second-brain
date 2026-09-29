"""Place music (A2) and SFX (A3-A6) on the current Resolve timeline from a JSON plan, overwrite only (no ripple).

python sound_place.py plan.json [--dry]
plan = {"timeline": name, "music": [{"path", "rec", "end", "src_s", "vol"}], "sfx": [{"path", "rec", "vol", "tr"}]}
- rec/end are timeline frames, src_s is the source in-point in seconds, vol is the clip's AudioVolume in dB.
- Adds stereo audio tracks up to the highest track the plan uses. Asserts the timeline length never changes.
- Files are imported into the media pool folder "Sound (Editor)" (reused when already there).
"""
import sys, json, os
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr

resolve = dvr.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()
mp = project.GetMediaPool()
plan = json.load(open(sys.argv[1], encoding="utf-8"))
DRY = "--dry" in sys.argv
tl = next(project.GetTimelineByIndex(i) for i in range(1, project.GetTimelineCount() + 1) if project.GetTimelineByIndex(i).GetName() == plan["timeline"])
project.SetCurrentTimeline(tl)
FPS = float(tl.GetSetting("timelineFrameRate"))
ST = tl.GetStartFrame()
END0 = tl.GetEndFrame()

root = mp.GetRootFolder()
fold = next((f for f in root.GetSubFolderList() if f.GetName() == "Sound (Editor)"), None) or mp.AddSubFolder(root, "Sound (Editor)")
mp.SetCurrentFolder(fold)
cache = {c.GetClipProperty("File Path"): c for c in fold.GetClipList()}


def mpi(path):
    if path not in cache:
        got = mp.ImportMedia([path])
        cache[path] = got[0]
    return cache[path]


need = max([2] + [s["tr"] for s in plan.get("sfx", [])])
while tl.GetTrackCount("audio") < need:
    tl.AddTrack("audio", "stereo")


def place(path, rec, end, src_frames, tr, vol):
    item = mpi(path)
    if DRY:
        return None
    got = mp.AppendToTimeline([{"mediaPoolItem": item, "startFrame": src_frames, "endFrame": src_frames + (end - rec),
                                "trackIndex": tr, "recordFrame": ST + rec, "mediaType": 2}])
    it = got[0] if got else None
    if not it or it.GetStart() is None:
        print("FAILED", os.path.basename(path), rec, tr); return None
    it.SetProperty("AudioVolume", float(vol))
    assert tl.GetEndFrame() == END0, "timeline length changed!"
    return it


out = []
for m in plan.get("music", []):
    it = place(m["path"], m["rec"], m["end"], int(round(m["src_s"] * FPS)), 2, m["vol"])
    out.append(("music", os.path.basename(m["path"]), m["rec"], it.GetStart() - ST if it else None, it.GetEnd() - ST if it else None, it.GetProperty("AudioVolume") if it else None))
for s in plan.get("sfx", []):
    n = s.get("len") or int(round(s.get("dur", 1.0) * FPS))
    it = place(s["path"], s["rec"], s["rec"] + n, 0, s["tr"], s["vol"])
    out.append(("sfx", os.path.basename(s["path"]), s["rec"], it.GetStart() - ST if it else None, s["tr"], it.GetProperty("AudioVolume") if it else None))
for o in out:
    print(o)
print("audio tracks", tl.GetTrackCount("audio"), "length same", tl.GetEndFrame() == END0)
if not DRY:
    resolve.GetProjectManager().SaveProject()
