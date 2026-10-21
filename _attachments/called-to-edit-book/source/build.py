"""Build the Called to Edit book: parts -> book.html -> PDF, fill contents page numbers, preview sheets."""
import glob, os, re, subprocess, sys
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = os.path.join(HERE, "Called-to-Edit-How-to-Build-a-Career-as-a-Video-Editor-and-Get-Paid.pdf")

MK = ('<svg class="mk" width="14" height="16" viewBox="0 0 14 16"><path d="M0 0H14V9.6L7 16L0 9.6Z" fill="#8A5E17"/></svg>')
MKG = ('<svg width="12" height="14" viewBox="0 0 14 16"><path d="M0 0H14V9.6L7 16L0 9.6Z" fill="currentColor"/></svg>')

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Called to Edit: How to Build a Career as a Video Editor and Get Paid</title>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Plus+Jakarta+Sans:ital,wght@0,500;0,600;0,700;0,800;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="book.css"></head><body>
"""


def opener(m):
    n, title, sub, quote = m.group(1).split("|")
    return f"""<section class="full op" id="ch{n}">
  <img class="logo" src="kit/called-to-edit-logo-dark.svg" alt="">
  <div class="num">{n}</div>
  <div class="lab">{MKG}<span>Chapter {n}</span></div>
  <h1>{title}</h1>
  <div class="sub">{sub}</div>
  <div class="art"><div class="qr"></div><div class="qt">&ldquo;{quote}&rdquo;</div></div>
  <span class="tm">MARKCH{n}</span>
</section>"""


def assemble(pages=None):
    parts = sorted(glob.glob(os.path.join(HERE, "p[0-9]*.html")), key=lambda p: int(re.findall(r"p(\d+)", os.path.basename(p))[0]))
    body = "\n".join(open(p, encoding="utf-8").read() for p in parts)
    body = re.sub(r"@@OP\|(.+?)@@", opener, body, flags=re.S)
    body = re.sub(r'data-mark="(\w+)">', lambda m: f'><span class="tm">MARK{m.group(1)}</span>', body)
    body = body.replace("{MK}", MK).replace("{MKG}", MKG)
    if pages:
        body = re.sub(r"\{\{p:(\w+)\}\}", lambda m: str(pages.get(m.group(1), "")), body)
    else:
        body = re.sub(r"\{\{p:(\w+)\}\}", "00", body)
    html = HEAD + body + "\n</body></html>"
    path = os.path.join(HERE, "book.html")
    open(path, "w", encoding="utf-8").write(html)
    return path


def render(html):
    url = "file:///" + html.replace("\\", "/")
    subprocess.run([CHROME, "--headless=new", f"--user-data-dir={os.path.join(HERE, 'chrome-prof')}",
                    "--no-pdf-header-footer", "--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw",
                    f"--print-to-pdf={OUT}", url], capture_output=True)


def marks():
    d = pymupdf.open(OUT)
    found = {}
    for i, p in enumerate(d):
        t = p.get_text()
        for k in re.findall(r"MARK(\w+)", t):
            found.setdefault(k, i + 1)
        if i >= 2:
            for k, phrase in TEXTMARKS.items():
                if phrase in t.replace("\n", " "):
                    found.setdefault(k, i + 1)
    return found, len(d)


TEXTMARKS = {"START": "There are millions of video", "RECAP": "The pathway in twelve lines", "ABOUT": "About the author"}


def sheets(scale=0.42, per=8, only=None):
    d = pymupdf.open(OUT)
    os.makedirs(os.path.join(HERE, "sheets"), exist_ok=True)
    for f in glob.glob(os.path.join(HERE, "sheets", "*.jpg")):
        os.remove(f)
    imgs = []
    for i, p in enumerate(d):
        if only and (i + 1) not in only:
            continue
        pm = p.get_pixmap(matrix=pymupdf.Matrix(scale * 4 / 3, scale * 4 / 3))
        im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
        imgs.append((i + 1, im))
    for s in range(0, len(imgs), per):
        chunk = imgs[s:s + per]
        w, h = chunk[0][1].size
        cols = 4
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (w + 8), rows * (h + 8)), (120, 120, 120))
        for k, (n, im) in enumerate(chunk):
            sheet.paste(im, ((k % cols) * (w + 8), (k // cols) * (h + 8)))
        sheet.save(os.path.join(HERE, "sheets", f"s{chunk[0][0]:03d}.jpg"), quality=82)


if __name__ == "__main__":
    render(assemble())
    found, n = marks()
    render(assemble(found))
    found2, n2 = marks()
    print("pages", n2, found2)
    sheets()
