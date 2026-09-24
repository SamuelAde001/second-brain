"""Fast, resumable download of a link-shared Google Drive file (or any URL that honours Range).

One connection from Drive runs at ~2-3 MB/s here; eight in parallel reach ~9+ MB/s.
The file is split into 64 MB ranges, fetched by N threads, written in place into
<out>.part, and renamed when every range is in. Progress lives in <out>.part.json,
so re-running the same command resumes.

    python drive_download.py <file_id | url | @url-file> "<output path>" [--threads 8]

Drive: works only for files shared "anyone with the link" (no sign-in).
Tella: pass the export's signed downloadUrl (see the Routerise job setup SOP). Stock Python only.
"""
import json, os, sys, threading, time, urllib.request

CHUNK = 64 * 1024 * 1024
URL = "https://drive.usercontent.google.com/download?id={}&export=download&confirm=t"


def size_of(url):
    req = urllib.request.Request(url, headers={"Range": "bytes=0-0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        cr = r.headers.get("Content-Range")  # bytes 0-0/TOTAL
        if not cr:
            sys.exit("Server ignored Range; is the file link-shared?")
        return int(cr.split("/")[1])


def main():
    args = sys.argv[1:]
    threads = 8
    if "--threads" in args:
        i = args.index("--threads"); threads = int(args[i + 1]); del args[i:i + 2]
    src, out = args
    # a Drive file ID, a direct URL, or @file holding a long signed URL (e.g. a Tella export)
    if src.startswith("@"):
        src = open(src[1:], encoding="utf-8").read().strip()
    url = src if src.startswith("http") else URL.format(src)
    part, state_path = out + ".part", out + ".part.json"
    total = size_of(url)
    n = (total + CHUNK - 1) // CHUNK
    done = set(json.load(open(state_path))["done"]) if os.path.exists(state_path) else set()
    if not os.path.exists(part):
        with open(part, "wb") as f:
            f.truncate(total)
    todo = [i for i in range(n) if i not in done]
    lock = threading.Lock()
    got = [0]
    t0 = time.time()

    def worker():
        while True:
            with lock:
                if not todo:
                    return
                i = todo.pop(0)
            start, end = i * CHUNK, min(total, (i + 1) * CHUNK) - 1
            for attempt in range(8):
                try:
                    req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}"})
                    with urllib.request.urlopen(req, timeout=120) as r, open(part, "r+b") as f:
                        f.seek(start)
                        pos = start
                        while True:
                            b = r.read(1024 * 1024)
                            if not b:
                                break
                            f.write(b); pos += len(b)
                            with lock:
                                got[0] += len(b)
                    if pos != end + 1:
                        raise IOError(f"short range {i}: {pos - start} of {end - start + 1}")
                    break
                except Exception as e:  # retry the whole range
                    print(f"range {i} attempt {attempt + 1} failed: {e}", flush=True)
                    time.sleep(3 * (attempt + 1))
            else:
                print(f"range {i} gave up", flush=True)
                continue
            with lock:
                done.add(i)
                json.dump({"total": total, "done": sorted(done)}, open(state_path, "w"))

    ts = [threading.Thread(target=worker, daemon=True) for _ in range(threads)]
    for t in ts:
        t.start()
    while any(t.is_alive() for t in ts):
        time.sleep(15)
        with lock:
            pct = len(done) / n * 100
            rate = got[0] / 1048576 / max(1, time.time() - t0)
        print(f"{len(done)}/{n} ranges ({pct:.0f}%), {rate:.1f} MB/s", flush=True)
    if len(done) == n:
        os.replace(part, out)
        os.remove(state_path)
        print(f"DONE {out} {total} bytes", flush=True)
    else:
        sys.exit(f"INCOMPLETE: {n - len(done)} ranges missing; re-run to resume")


if __name__ == "__main__":
    main()
