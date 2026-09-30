"""Build motion-gallery.html: one self-contained page (CSS, JS, reference thumbnails and an A-roll still inlined).

Stdlib + ffmpeg. Reads the reference frames from the Route Rise folders (read-only) and caches thumbnails
in _cache/ (gitignored). The built page is gitignored too: the sources in src/ are the record.

    python build_gallery.py            build the page
    python build_gallery.py --stills   also render one still per design into _cache/stills/ (headless Chrome)
"""
import base64, glob, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
CACHE = os.path.join(HERE, "_cache")
OUT = os.path.join(HERE, "motion-gallery.html")
FF = shutil.which("ffmpeg") or os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
RR = r"C:\Users\repzy\Desktop\Video edits\Routerise"
INSPO = os.path.join(RR, "Visual Assets", "Visual Inspo")
BEST = os.path.join(RR, "3. I Tried 100+ AI Tools. These 4 Are Best for Businesses", "Docs", "Visual study", "best-editor")
FINALS = {
    "m7": os.path.join(RR, "4. $7M Founder How I Use Claude for Cold Outreach (B2B sales)", "v2.mp4"),
    "tsb": os.path.join(RR, "1. Taking a step back from Claude (and why you should too)", "v2.1.mp4"),
    "r3": os.path.join(RR, "3. I Tried 100+ AI Tools. These 4 Are Best for Businesses", "v3.mp4"),
}
AROLL = os.path.join(RR, "I cancelled Apollo.io and built this Claude skill instead", "Graphics", "Visuals v1", "stills", "B40.jpg")
# ref ids that point into a final instead of the inspo folders: id -> (final, seconds)
SPECIAL = {"M7-67": ("m7", 68.81)}
# the approved baseline strip: (final, seconds, caption)
BASELINE = [
    ("r3", 31.36, "<b>4 AI Tools</b> · the 4-tools tiles"),
    ("r3", 53.21, "<b>4 AI Tools</b> · orange list pills + logo hub"),
    ("r3", 17.63, "<b>4 AI Tools</b> · PIP ring + connector pill"),
    ("r3", 513.71, "<b>4 AI Tools</b> · top stepper + hub"),
    ("m7", 125.87, "<b>$7M Founder</b> · numbered tool pill"),
    ("m7", 117.77, "<b>$7M Founder</b> · recap pills"),
    ("m7", 42.95, "<b>$7M Founder</b> · signals card"),
    ("tsb", 119.19, "<b>Taking a Step Back</b> · orange circle + connector"),
    ("tsb", 57.21, "<b>Taking a Step Back</b> · Claude tile + department pills"),
    ("tsb", 4.29, "<b>Taking a Step Back</b> · two-tone headline"),
]
JS_ORDER = ["gallery-engine.js", "pills.js", "boxes.js", "cards.js", "circles.js", "gallery-shell.js"]


def ff(args):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y"] + args, check=True)


def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def thumb_from_image(src, name, width=480):
    out = os.path.join(CACHE, name + ".jpg")
    if not os.path.exists(out):
        ff(["-i", src, "-vf", f"scale={width}:-2", "-q:v", "5", out])
    return out


def thumb_from_video(video, sec, name, width=480):
    out = os.path.join(CACHE, name + ".jpg")
    if not os.path.exists(out):
        ff(["-ss", f"{sec:.2f}", "-i", video, "-frames:v", "1", "-vf", f"scale={width}:-2", "-q:v", "5", out])
    return out


def ref_ids():
    ids = set()
    for f in JS_ORDER:
        with open(os.path.join(SRC, f), encoding="utf-8") as h:
            ids.update(re.findall(r'ref:\s*\{\s*id:\s*"([^"]+)"', h.read()))
    return sorted(ids)


def build():
    os.makedirs(CACHE, exist_ok=True)
    inspo = sorted(glob.glob(os.path.join(INSPO, "*.png")))
    best = sorted(glob.glob(os.path.join(BEST, "*.jpg")))
    refs = {}
    for rid in ref_ids():
        try:
            if rid in SPECIAL:
                fin, sec = SPECIAL[rid]
                refs[rid] = data_uri(thumb_from_video(FINALS[fin], sec, "ref-" + rid))
            elif rid[0] == "I":
                refs[rid] = data_uri(thumb_from_image(inspo[int(rid[1:]) - 1], "ref-" + rid))
            elif rid[0] == "B":
                refs[rid] = data_uri(thumb_from_image(best[int(rid[1:]) - 1], "ref-" + rid))
        except Exception as e:  # a missing source only drops its thumbnail
            print("ref", rid, "skipped:", e)
    base = []
    for fin, sec, cap in BASELINE:
        try:
            base.append({"src": data_uri(thumb_from_video(FINALS[fin], sec, f"base-{fin}-{sec:.0f}")), "cap": cap})
        except Exception as e:
            print("baseline", fin, sec, "skipped:", e)
    aroll = os.path.join(CACHE, "aroll.jpg")
    if not os.path.exists(aroll):
        ff(["-i", AROLL, "-vf", "scale=1600:-2", "-q:v", "3", aroll])
    assets = {"aroll": data_uri(aroll), "refs": refs, "base": base}
    with open(os.path.join(SRC, "gallery-shell.html"), encoding="utf-8") as h:
        page = h.read()
    with open(os.path.join(SRC, "gallery.css"), encoding="utf-8") as h:
        css = h.read()
    js = []
    for f in JS_ORDER:
        with open(os.path.join(SRC, f), encoding="utf-8") as h:
            js.append(f"// ===== {f} =====\n" + h.read())
    page = page.replace("/*CSS*/", css).replace("/*ASSETS*/", "window.ASSETS = " + json.dumps(assets) + ";").replace("/*JS*/", "\n".join(js))
    with open(OUT, "w", encoding="utf-8") as h:
        h.write(page)
    print(f"built {OUT} ({os.path.getsize(OUT) / 1e6:.1f} MB), {len(refs)} refs, {len(base)} baseline frames")


def stills(times=(3.8,), only=None):
    """One still per design and time, via headless Chrome screenshots of ?only=CODE&t=T (4 in parallel)."""
    from concurrent.futures import ThreadPoolExecutor
    out = os.path.join(CACHE, "stills")
    os.makedirs(out, exist_ok=True)
    codes = []
    for f in JS_ORDER[1:5]:
        with open(os.path.join(SRC, f), encoding="utf-8") as h:
            codes += re.findall(r'^D\("([A-Z]\d\d)"', h.read(), re.M)
    if only:
        codes = [c for c in codes if c in only]
    url = "file:///" + OUT.replace("\\", "/").replace(" ", "%20")
    jobs = [(c, t) for c in codes for t in times]

    def shot(job, k):
        code, t = job
        png = os.path.join(out, f"{code}_{t:.1f}.png")
        ud = os.path.join(os.environ.get("TEMP", CACHE), f"mg_chrome_{k}")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu-sandbox", "--hide-scrollbars", "--window-size=1920,1080",
                        "--user-data-dir=" + ud, "--virtual-time-budget=5000", f"--screenshot={png}", f"{url}?only={code}&t={t}"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(lambda a: shot(*a), [(j, i) for i, j in enumerate(jobs)]))
    print("stills in", out, len(jobs), "shots")


if __name__ == "__main__":
    build()
    if "--stills" in sys.argv:
        ts = [float(a.split("=")[1]) for a in sys.argv if a.startswith("--t=")] or [3.8]
        only = [a.split("=")[1] for a in sys.argv if a.startswith("--only=")]
        stills(tuple(ts), set(only[0].split(",")) if only else None)
