"""Dump the music and SFX layout of finished Routerise projects (Resolve must be running; external scripting on).

python sound_study.py list                      list projects in the current project-manager folder tree
python sound_study.py dump "<project>" <out.json> [return-to-project]

For every timeline in the project: tracks, and for every audio item its file, track, start/end, source in,
AudioVolume and clip colour; for every video item its start/end/name/track (to relate SFX hits to visuals).
Loading a project closes the current one: the current project is saved first, and reopened at the end when
a return project is given. Read-only on the studied project (nothing is changed or saved there).
"""
import sys, json
sys.path.append(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
import DaVinciResolveScript as dvr

resolve = dvr.scriptapp("Resolve")
pm = resolve.GetProjectManager()


def walk_projects(path=()):
    out = [(path, p) for p in pm.GetProjectListInCurrentFolder()]
    for f in pm.GetFolderListInCurrentFolder():
        pm.OpenFolder(f)
        out += walk_projects(path + (f,))
        pm.GotoParentFolder()
    return out


def goto(path):
    pm.GotoRootFolder()
    for f in path:
        pm.OpenFolder(f)


def find(name):
    pm.GotoRootFolder()
    for path, p in walk_projects():
        if p == name:
            return path
    return None


def props(it, keys):
    d = {}
    for k in keys:
        try:
            d[k] = it.GetProperty(k)
        except Exception:
            pass
    return d


def dump_timeline(tl):
    out = {"name": tl.GetName(), "fps": tl.GetSetting("timelineFrameRate"), "start": tl.GetStartFrame(), "end": tl.GetEndFrame(),
           "audio": [], "video": [], "atracks": {}}
    st = tl.GetStartFrame()
    for tr in range(1, tl.GetTrackCount("audio") + 1):
        out["atracks"][tr] = {"name": tl.GetTrackName("audio", tr), "enabled": tl.GetIsTrackEnabled("audio", tr)}
        for it in tl.GetItemListInTrack("audio", tr) or []:
            mpi = it.GetMediaPoolItem()
            path = mpi.GetClipProperty("File Path") if mpi else ""
            out["audio"].append({"tr": tr, "name": it.GetName(), "path": path, "s": it.GetStart() - st, "e": it.GetEnd() - st,
                                 "src": it.GetSourceStartFrame(), "enabled": it.GetClipEnabled(), "color": it.GetClipColor(),
                                 **props(it, ["AudioVolume", "AudioVolumeEnabled"])})
    for tr in range(1, tl.GetTrackCount("video") + 1):
        for it in tl.GetItemListInTrack("video", tr) or []:
            out["video"].append({"tr": tr, "name": it.GetName(), "s": it.GetStart() - st, "e": it.GetEnd() - st, "enabled": it.GetClipEnabled()})
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "list":
        cur = pm.GetCurrentProject().GetName()
        print("current:", cur)
        pm.GotoRootFolder()
        for path, p in walk_projects():
            print("/".join(path), "|", p)
    elif cmd == "dump":
        name, outp = sys.argv[2], sys.argv[3]
        back = sys.argv[4] if len(sys.argv) > 4 else None
        backpath = find(back) if back else None
        pm.SaveProject()
        path = find(name)
        goto(path)
        proj = pm.LoadProject(name)
        assert proj, "could not load " + name
        res = {"project": name, "timelines": []}
        for i in range(1, proj.GetTimelineCount() + 1):
            tl = proj.GetTimelineByIndex(i)
            res["timelines"].append(dump_timeline(tl))
        json.dump(res, open(outp, "w", encoding="utf-8"), indent=0)
        print("timelines", [(t["name"], len(t["audio"])) for t in res["timelines"]])
        if back:
            goto(backpath)
            ok = pm.LoadProject(back)
            print("reopened", back, bool(ok))
