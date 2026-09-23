r"""Watch DaVinci Resolve render-cache progress clip by clip, and stop the moment Resolve crashes.

Resolve names each clip's cache folder after the timeline item's unique ID:
    <CacheClip>\<project uid>\<folder>\<item uid>\<uid>\SourceOne\<frame>.dvcc   (one file per frame)
so progress per clip = files in its folder vs its length in frames. Get item IDs with
TimelineItem.GetUniqueId() over the Resolve MCP; the first 8 characters are enough.
Usage:
    python resolve_cache_watch.py <queue.json> <key> [max_minutes] [--once]
queue.json holds "project_uid" and, under <key>, {"<uid8>": frames, ...}.
Exits on: batch complete, a new crash_archive.txt entry or Resolve exiting, or max_minutes.
Part of [[03-Areas/video-editing/troubleshooting|Troubleshooting]] section 7.
"""
import os, sys, json, time, subprocess, datetime

q = json.load(open(sys.argv[1]))
exp = q[sys.argv[2]]
max_min = float(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else 25
once = "--once" in sys.argv
CACHE = os.path.join(q.get("cache_root", r"C:\Users\repzy\Videos\CacheClip"), q["project_uid"])
SUP = os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support")


def resolve_pid():
    return subprocess.run(["powershell", "-NoProfile", "-Command",
                           "(Get-Process Resolve -ErrorAction SilentlyContinue | Select-Object -First 1).Id"],
                          capture_output=True, text=True).stdout.strip() or None


def vram():
    r = subprocess.run([r"C:\Windows\System32\nvidia-smi.exe", "--query-gpu=memory.used",
                        "--format=csv,noheader,nounits"], capture_output=True, text=True)
    return r.stdout.strip() + " MiB"


def crash_count():
    return open(os.path.join(SUP, "crash_archive.txt"), encoding="utf-8", errors="replace").read().count("#TIME ")


def scan():
    frames, newest = {}, {}
    for root, dirs, files in os.walk(CACHE):
        rel = os.path.relpath(root, CACHE).split(os.sep)
        if len(rel) < 2 or not files:
            continue
        u = rel[1][:8]
        frames.setdefault(u, set()).update(files)
        newest[u] = max([newest.get(u, 0)] + [os.path.getmtime(os.path.join(root, f)) for f in files])
    return {u: len(s) for u, s in frames.items()}, newest


pid0, crashes0, t0 = resolve_pid(), crash_count(), time.time()
while True:
    counts, newest = scan()
    total = sum(exp.values())
    got = sum(min(counts.get(u, 0), n) for u, n in exp.items())
    todo = [f"{u}:{counts.get(u, 0)}/{n}" for u, n in exp.items() if counts.get(u, 0) < n * 0.95]
    recent = sorted(newest.items(), key=lambda kv: -kv[1])[:3]
    print(f"[{datetime.datetime.now():%H:%M:%S}] {got}/{total} frames ({100 * got / total:.0f}%), "
          f"{len(exp) - len(todo)}/{len(exp)} clips done, VRAM {vram()}, writing: {', '.join(u for u, _ in recent)}", flush=True)
    pid = resolve_pid()
    if pid != pid0 or crash_count() != crashes0:
        print(f"!!! RESOLVE CRASHED/EXITED (pid {pid0} -> {pid}). Last written: "
              + ", ".join(f"{u}@{datetime.datetime.fromtimestamp(t):%H:%M:%S}" for u, t in recent), flush=True)
        break
    if not todo:
        print("BATCH COMPLETE", flush=True)
        break
    if once or time.time() - t0 > max_min * 60:
        print("still to do: " + ", ".join(todo), flush=True)
        break
    time.sleep(20)
