"""Build a job's visual review page: every sentence of the cut in order, each visual animated in sync with the words.

Stdlib + ffmpeg (+ headless Chrome for QA stills). Engine, parts and page shell come from src/ here; the job supplies
a spec folder with review.json (paths, sections, logos, A-roll frames, scene files) and its scenes-*.js (RV(...) visuals).

    python build_review.py "<job folder>" "<spec folder inside the job>"
    python build_review.py "<job folder>" "<spec>" --stills [--t=3.0] [--only=V03,V04]   one still per visual into <spec>/_qa
"""
import base64, importlib.util, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
FF = shutil.which("ffmpeg") or os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
RV_ANIMATED = re.compile(r'^RV\("([A-Z0-9]+)",\s*\{[^\n]*\},\s*\(S', re.M)
RV_STILL = re.compile(r'RV\("([A-Z0-9]+)",\s*\{[^\n]*?still: "([^"]+)"')


def ff(args):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y"] + args, check=True)


def uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {".svg": "image/svg+xml", ".png": "image/png"}.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def jpg(src, out, width, q=4):
    if not os.path.exists(out):
        ff(["-i", src, "-vf", f"scale={width}:-2", "-q:v", str(q), out])
    return out


def read(p):
    with open(p, encoding="utf-8") as h:
        return h.read()


def spec(job, spec_dir):
    S = os.path.join(job, spec_dir)
    return S, json.loads(read(os.path.join(S, "review.json")))


def build(job, spec_dir):
    S, R = spec(job, spec_dir)
    cache = os.path.join(S, "_cache")
    os.makedirs(cache, exist_ok=True)
    J = lambda p: os.path.join(job, p)
    sentences = json.loads(read(J(R["sentences"])))
    cues = json.loads(read(J(R["cues"])))
    scene_files = R.get("scenes", ["scenes.js"])
    scenes_js = "\n".join(read(os.path.join(S, f)) for f in scene_files)
    # A-roll frames for visuals over the A-roll: a beat id (its start + 18 frames) or a timeline frame -> camera frame via tlmap
    frames = {}
    if R.get("frames"):
        spec_tl = importlib.util.spec_from_file_location("tlmap", J(R["tlmap"]))
        tl = importlib.util.module_from_spec(spec_tl)
        spec_tl.loader.exec_module(tl)
        fdir = os.path.join(S, "frames")
        os.makedirs(fdir, exist_ok=True)
        start = {x["id"]: x["start"] for x in sentences}
        for code, f in R["frames"].items():
            f = start[f] + 18 if isinstance(f, str) else f
            out = os.path.join(fdir, f"{code}_{f}.jpg")
            if not os.path.exists(out):
                ff(["-ss", f"{tl.cam(f):.3f}", "-i", tl.CAM, "-frames:v", "1", "-vf", "scale=1600:-2", "-q:v", "3", out])
            frames["f_" + code] = uri(out)
    logos = {k: uri(J(os.path.join(R["logos_dir"], v))) for k, v in R.get("logos", {}).items()}
    stills = {}
    for code, still in RV_STILL.findall(scenes_js):
        src = J(os.path.join(R["stills"], still + ".jpg"))
        if os.path.exists(src):
            stills[still] = uri(jpg(src, os.path.join(cache, f"still_{still}.jpg"), 960, 5))
    thumbs = {}
    for s in sentences:
        src = J(os.path.join(R["thumbs"], s["id"] + ".jpg"))
        if os.path.exists(src):
            thumbs[s["id"]] = uri(jpg(src, os.path.join(cache, f"thumb_{s['id']}.jpg"), 400, 6))
    assets = dict(frames)
    assets.update({"logos": logos, "stills": stills, "thumbs": thumbs, "aroll": next(iter(frames.values()), "")})
    job_data = {"title": R["title"], "slug": R["slug"], "version": R["version"], "date": R["date"], "fps": 24000 / 1001,
                "sentences": sentences, "cues": cues, "sections": [{"name": n, "start": f, "color": c} for n, f, c in R["sections"]]}
    page = read(os.path.join(SRC, "review-shell.html"))
    css = read(os.path.join(SRC, "gallery.css")) + "\n" + read(os.path.join(SRC, "review.css"))
    parts = [("gallery-engine.js", os.path.join(SRC, "gallery-engine.js")), ("parts.js", os.path.join(SRC, "parts.js"))]
    parts += [(f, os.path.join(S, f)) for f in scene_files]
    parts += [("review-shell.js", os.path.join(SRC, "review-shell.js"))]
    js = "\n".join(f"// ===== {n} =====\n" + read(p) for n, p in parts)
    data = "window.JOB = " + json.dumps(job_data) + ";\nwindow.ASSETS = " + json.dumps(assets) + ";"
    title = f'{R["short"]} · visual review {R["version"]}'
    page = (page.replace("/*TITLE*/", title).replace("/*H1*/", title).replace("/*SUB*/", f'{R["client"]} · {R["date"]}')
                .replace("/*INTRO*/", R.get("intro", "")).replace("/*CSS*/", css).replace("/*DATA*/", data).replace("/*JS*/", js))
    out = J(R["out"])
    with open(out, "w", encoding="utf-8") as h:
        h.write(page)
    print(f"built {out} ({os.path.getsize(out) / 1e6:.1f} MB): {len(RV_ANIMATED.findall(scenes_js))} animated, {len(stills)} stills, {len(frames)} A-roll frames, {len(logos)} logos")
    return out


def qa(job, spec_dir, out, times, only):
    from concurrent.futures import ThreadPoolExecutor
    S, R = spec(job, spec_dir)
    codes = RV_ANIMATED.findall("\n".join(read(os.path.join(S, f)) for f in R.get("scenes", ["scenes.js"])))
    if only:
        codes = [c for c in codes if c in only]
    qd = os.path.join(S, "_qa")
    os.makedirs(qd, exist_ok=True)
    url = "file:///" + out.replace("\\", "/").replace(" ", "%20").replace("$", "%24")
    jobs = [(c, t, k) for k, (c, t) in enumerate((c, t) for c in codes for t in times)]

    def shot(job_):
        code, t, k = job_
        ud = os.path.join(os.environ.get("TEMP", qd), f"rv_chrome_{k}")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu-sandbox", "--hide-scrollbars", "--window-size=1920,1080",
                        "--user-data-dir=" + ud, "--virtual-time-budget=6000", f"--screenshot={os.path.join(qd, f'{code}_{t}.png')}",
                        f"{url}?only={code}&t={t}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(shot, jobs))
    print("qa stills in", qd, len(jobs))


if __name__ == "__main__":
    job, spec_dir = sys.argv[1], sys.argv[2]
    out = build(job, spec_dir)
    if "--stills" in sys.argv:
        ts = [a.split("=")[1] for a in sys.argv if a.startswith("--t=")] or ["end"]
        only = [a.split("=")[1] for a in sys.argv if a.startswith("--only=")]
        qa(job, spec_dir, out, ts, set(only[0].split(",")) if only else None)
