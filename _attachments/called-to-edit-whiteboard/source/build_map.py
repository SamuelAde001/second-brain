"""Build chapter maps: mapNN.py -> HTML -> PDF (Chrome) -> outlined SVG + preview + reveal positions.
python build_map.py map04"""
import importlib, json, os, re, subprocess, sys
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROF = os.path.join(os.environ.get("TEMP", HERE), "c2e-board-chrome")
sys.path.insert(0, HERE)
import maplib


def chrome(*args):
    return subprocess.run([CHROME, "--headless=new", f"--user-data-dir={PROF}", "--no-pdf-header-footer",
                           "--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw", *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def build(modname, preview=0.2):
    m = importlib.import_module(modname)
    photos = json.load(open(os.path.join(HERE, "photos.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
    if hasattr(m, "P"):
        m.P.update(photos)
    body, w, h = m.build()
    html = maplib.page(body, w, h, m.NAME)
    hp = os.path.join(HERE, m.NAME + ".html")
    open(hp, "w", encoding="utf-8").write(html)
    url = "file:///" + hp.replace("\\", "/")
    pdf = os.path.join(OUT, m.NAME + ".pdf")
    chrome(f"--print-to-pdf={pdf}", url)
    dom = chrome("--dump-dom", url).stdout
    mm = re.search(r'<script type="application/json" id="pos">(.*?)</script>', dom, re.S)
    pos = json.loads(mm.group(1)) if mm else {"rv": []}
    p = pymupdf.open(pdf)[0]
    s = p.get_svg_image(text_as_path=True)
    s = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w}" height="{h}"', s, count=1)
    open(os.path.join(OUT, m.NAME + ".svg"), "w", encoding="utf-8").write(s)
    k = preview * 4 / 3
    pix = p.get_pixmap(matrix=pymupdf.Matrix(k, k), alpha=True)
    from PIL import Image
    im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    bg = Image.new("RGBA", im.size, (7, 18, 38, 255)); bg.alpha_composite(im)
    bg.convert("RGB").save(os.path.join(OUT, m.NAME + "-preview.png"))
    pos["size_px"] = [w, h]
    json.dump(pos, open(os.path.join(OUT, m.NAME + ".json"), "w", encoding="utf-8"), indent=1)
    print(f"{m.NAME}: {w}x{h}, svg {len(s)//1024} KB, reveals {len(pos['rv'])}")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        build(a, float(os.environ.get("PREVIEW", "0.2")))
