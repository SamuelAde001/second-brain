"""Build the webinar whiteboard rows: HTML -> PDF (Chrome) -> outlined SVG + preview PNG, plus reveal positions.

python build.py            all rows
python build.py row02      rows whose name contains 'row02'
"""
import json, os, re, subprocess, sys
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROF = os.path.join(os.environ.get("TEMP", HERE), "c2e-board-chrome")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)

import lib
import rows_a
ROWS = list(rows_a.ROWS)
for mod in ("rows_b", "rows_c", "rows_d"):
    if os.path.exists(os.path.join(HERE, mod + ".py")):
        ROWS += __import__(mod).ROWS

PHOTOS = json.load(open(os.path.join(HERE, "photos.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "photos.json")) else {}
for mod in ("rows_a", "rows_b", "rows_c", "rows_d"):
    if mod in sys.modules and hasattr(sys.modules[mod], "P"):
        sys.modules[mod].P.update(PHOTOS)


def chrome(*args):
    return subprocess.run([CHROME, "--headless=new", f"--user-data-dir={PROF}", "--no-pdf-header-footer",
                           "--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw", *args],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def build(name, fn):
    frames = fn()
    html = lib.page(frames, name)
    hp = os.path.join(HERE, name + ".html")
    open(hp, "w", encoding="utf-8").write(html)
    url = "file:///" + hp.replace("\\", "/")
    pdf = os.path.join(OUT, name + ".pdf")
    chrome(f"--print-to-pdf={pdf}", url)
    dom = chrome("--dump-dom", url).stdout
    m = re.search(r'<script type="application/json" id="pos">(.*?)</script>', dom, re.S)
    pos = json.loads(m.group(1)) if m else {"rv": []}
    d = pymupdf.open(pdf)
    if len(d) != 1:
        print(f"  !! {name}: {len(d)} pages")
    p = d[0]
    s = p.get_svg_image(text_as_path=True)
    # PDF points -> CSS px: scale the root so the SVG is in px at 1:1
    wpx, hpx = round(p.rect.width * 4 / 3), round(p.rect.height * 4 / 3)
    s = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{wpx}" height="{hpx}"', s, count=1)
    open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(s)
    p.get_pixmap(matrix=pymupdf.Matrix(0.25, 0.25)).save(os.path.join(OUT, name + "-preview.png"))
    pos["size_px"] = [wpx, hpx]
    pos["frames"] = [re.search(r'data-id="([^"]+)"', f).group(1) for f in frames]
    json.dump(pos, open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8"), indent=1)
    print(f"{name}: {len(frames)} frames, {wpx}x{hpx}px, svg {len(s)//1024} KB, reveals {len(pos['rv'])}")


if __name__ == "__main__":
    pick = sys.argv[1] if len(sys.argv) > 1 else ""
    for name, fn in ROWS:
        if pick in name:
            build(name, fn)
