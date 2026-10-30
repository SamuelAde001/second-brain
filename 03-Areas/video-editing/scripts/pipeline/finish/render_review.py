# Render a timeline through Deliver chunk by chunk (H.264 1080p mp4), holding the kit's Resolve lock with a heartbeat; chunks are joined video-only, or one chunk is the deliverable.
# usage: python render_review.py "<timeline>" <out dir> [--job <job folder> | --kits <kits dir>] [--chunk 4020] [--from F] [--to F] [--name prefix]    (needs Resolve running)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
#   deliverable: --chunk 99999 (one pass, continuous audio); chunks are for review only (see the end of this file)
# Each chunk is an H.264 .mp4 (1080p, audio on); between chunks the lock is released for 15 s so queued lab renders get in.
# At the end the chunks are joined (ffmpeg concat, stream copy) into <prefix>.mp4. Frames: ffmpeg -ss on the joined file.
import argparse, glob, json, os, subprocess, sys, threading, time
sys.dont_write_bytecode = True                           # never leave __pycache__ in the kits dir

ap = argparse.ArgumentParser(description="Chunked Deliver render of a timeline with the kit's Resolve lock held by a heartbeat.")
ap.add_argument("timeline", help="timeline to render")
ap.add_argument("out", help="output folder (made absolute: Resolve fails a job at once on a relative TargetDir)")
ap.add_argument("--job", help="job folder (gives the default --kits)")
ap.add_argument("--kits", help="kits dir (default <job>\\Graphics\\Frontal kit (Editor)\\kits)")
ap.add_argument("--chunk", type=int, default=4020, help="frames per chunk (default 4020; 99999 = one pass)")
ap.add_argument("--from", dest="f0", type=int, default=0, help="first frame (default 0)")
ap.add_argument("--to", dest="f1", type=int, default=-1, help="end frame, exclusive (default: timeline end)")
ap.add_argument("--name", default="review", help="output name prefix (video 4 used v4_review, v3_1080, ...)")
args = ap.parse_args()
if not (args.job or args.kits):
    ap.error("give --job or --kits")
KITS = os.path.abspath(args.kits or os.path.join(args.job, "Graphics", "Frontal kit (Editor)", "kits"))
sys.path[:0] = [KITS, r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"]
import lab                                   # noqa: E402
import DaVinciResolveScript as dvr           # noqa: E402

TL, OUT = args.timeline, os.path.abspath(args.out)      # absolute: Resolve fails a job at once on a relative TargetDir (2026-10-25)
CH, F0, F1, NAME = args.chunk, args.f0, args.f1, args.name
OWNER = "review-render"
os.makedirs(OUT, exist_ok=True)
say = lambda *x: print(time.strftime("%H:%M:%S"), *x, flush=True)


def beat(stop):
    while not stop.is_set():
        try:
            info = lab.lock_info()
            if info and info.get("owner") == OWNER:
                info["time"] = time.time()
                tmp = lab.LOCK + ".hb"
                json.dump(info, open(tmp, "w", encoding="utf-8")); os.replace(tmp, lab.LOCK)
        except Exception:
            pass
        stop.wait(60)


r = dvr.scriptapp("Resolve"); p = r.GetProjectManager().GetCurrentProject()
t = next(p.GetTimelineByIndex(i) for i in range(1, p.GetTimelineCount() + 1) if p.GetTimelineByIndex(i).GetName() == TL)
S0 = t.GetStartFrame(); LEN = t.GetEndFrame() - S0
F1 = LEN if F1 < 0 else F1
parts = [(s, min(s + CH, F1)) for s in range(F0, F1, CH)]
say("timeline", TL, "len", LEN, "chunks", parts)
done = []
for s, e in parts:
    fn = os.path.join(OUT, "%s_%05d_%05d.mp4" % (NAME, s, e))
    if os.path.exists(fn) and os.path.getsize(fn) > 1000:
        say("have", os.path.basename(fn)); done.append(fn); continue
    lab.acquire(OWNER, wait=3600)
    stop = threading.Event(); th = threading.Thread(target=beat, args=(stop,), daemon=True); th.start()
    try:
        cur0 = p.GetCurrentTimeline().GetName()
        p.SetCurrentTimeline(t); r.OpenPage("deliver"); time.sleep(1)
        p.LoadRenderPreset("YouTube - 1080p")    # resets a project left with video export off (2026-10-25: ExportVideo True alone didn't)
        assert p.SetCurrentRenderFormatAndCodec("mp4", "H264"), "no mp4/H264"
        p.SetCurrentRenderMode(1)
        p.SetRenderSettings({"SelectAllFrames": False, "MarkIn": S0 + s, "MarkOut": S0 + e - 1, "TargetDir": OUT,
                             "CustomName": os.path.splitext(os.path.basename(fn))[0], "ExportVideo": True, "ExportAudio": True,
                             "FormatWidth": 1920, "FormatHeight": 1080})
        j = p.AddRenderJob(); assert j, "job not added"
        t0 = time.time(); p.StartRendering([j], False); time.sleep(2); last = -1
        while p.IsRenderingInProgress():
            st = p.GetRenderJobStatus(j) or {}
            pc = int(st.get("CompletionPercentage", 0))
            if pc >= last + 10:
                say("chunk", s, e, "%d%%" % pc, "%.1f fps" % ((e - s) * pc / 100.0 / max(1, time.time() - t0))); last = pc
            time.sleep(3)
        st = p.GetRenderJobStatus(j) or {}
        say("chunk", s, e, st.get("JobStatus"), "%.0f s" % (time.time() - t0), "%.1f fps" % ((e - s) / max(1, time.time() - t0)))
        try:
            p.DeleteRenderJob(j)
        except Exception:
            pass
        r.OpenPage("edit")
        try:
            p.SetCurrentTimeline(next(p.GetTimelineByIndex(i) for i in range(1, p.GetTimelineCount() + 1) if p.GetTimelineByIndex(i).GetName() == cur0))
        except Exception:
            pass
    finally:
        stop.set(); lab.release(OWNER)
    got = sorted(glob.glob(os.path.join(OUT, os.path.splitext(os.path.basename(fn))[0] + "*.mp4")))
    assert got, "no output for chunk %d-%d" % (s, e)
    if got[-1] != fn:
        os.replace(got[-1], fn)
    kinds = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", fn], capture_output=True, text=True).stdout.split()
    if "video" not in kinds or "audio" not in kinds:
        os.replace(fn, fn + ".bad"); raise SystemExit("chunk %d-%d has streams %s, not video + audio" % (s, e, kinds))
    done.append(fn)
    time.sleep(15)                                   # let queued lab renders take the lock
# Chunk audio is never joined (2026-10-25): each Deliver chunk's audio fades out at its end and starts ~450 samples late, so a
# join has ~20 ms dropouts mid-word, and the scripting API cannot switch video export off for an audio-only pass (ExportVideo
# False is ignored once a preset is loaded). So: a chunked render gives review chunks plus a video-only join; the deliverable
# is a single-chunk render (--chunk larger than the timeline), whose one file is renamed to <name>.mp4.
if F0 == 0 and F1 == LEN and len(done) == 1:
    full = os.path.join(OUT, NAME + ".mp4")
    os.replace(done[0], full)
    say("single pass ->", full)
elif F0 == 0 and F1 == LEN:
    vids = []
    for f in done:                                    # video only: the concat then runs on frame-exact video timestamps
        v = os.path.splitext(f)[0] + "_v.mp4"
        if not os.path.exists(v):
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f, "-an", "-c", "copy", v], check=True)
        vids.append(v)
    lst = os.path.join(OUT, "_concat.txt")
    open(lst, "w", encoding="utf-8").write("".join("file '%s'\n" % os.path.basename(f) for f in vids))   # names only: the job path has "Here's"
    vfull = os.path.join(OUT, "_" + NAME + "_video_only.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vfull], check=True)
    say("video-only join", vfull, "(review only: render the deliverable in one pass, --chunk 99999)")
say("ALL DONE")
