import os, re, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
KIT, PNG = os.path.join(HERE, "kit"), os.path.join(HERE, "png")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
os.makedirs(PNG, exist_ok=True)
tmp = os.path.join(HERE, "png_tmp.html")

for f in sorted(os.listdir(KIT)):
    if not f.endswith(".svg"):
        continue
    svg = open(os.path.join(KIT, f), encoding="utf-8").read()
    vw, vh = [float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).groups()]
    square = abs(vw - vh) < 1
    W = 1080 if square else 2400
    H = round(W * vh / vw)
    open(tmp, "w", encoding="utf-8").write(
        f'<!doctype html><html><head><style>html,body{{margin:0;background:transparent}}img{{display:block;width:{W}px;height:{H}px}}</style></head>'
        f'<body><img src="kit/{f}"></body></html>')
    out = os.path.join(PNG, f[:-4] + ".png")
    subprocess.run([CHROME, "--headless=new", f"--user-data-dir={os.path.join(HERE, 'chrome-prof')}", "--hide-scrollbars",
                    "--default-background-color=00000000", f"--window-size={W},{H}", "--virtual-time-budget=3000",
                    f"--screenshot={out}", "file:///" + tmp.replace("\\", "/")], capture_output=True)
    im = Image.open(out)
    a = im.getchannel("A") if im.mode == "RGBA" else None
    print(f, im.size, im.mode, "alpha-min", a.getextrema()[0] if a else None)

# B&W cutout of Samuel for the flyer example (soft-edged cutout from the landing page kit)
src = Image.open(r"C:\Users\repzy\Desktop\landing-page\flyer\subject.webp").convert("RGBA")
g = src.convert("LA").convert("RGBA")
g.putalpha(src.getchannel("A"))
g.thumbnail((900, 1200))
g.save(os.path.join(HERE, "photos", "samuel-cutout-bw.webp"), quality=82)
w = Image.open(os.path.join(HERE, "photos", "wall-1080x1920.jpg"))
w.save(os.path.join(HERE, "photos", "wall-1080x1920.webp"), quality=78)
print("photos ok")
