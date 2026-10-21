"""WhatsApp Status versions of the logo: 1080 x 1920 PNGs, the logo centred on each brand background."""
import os, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "status")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
os.makedirs(OUT, exist_ok=True)

# name: (background CSS, logo file) — the logo version always matches its background
VERSIONS = {
    "navy": ("#0A1F44", "called-to-edit-logo-dark.svg"),
    "navy-glow": ("radial-gradient(90% 60% at 50% 46%, #0A1F44 0%, #0A1F44 30%, #071226 100%)", "called-to-edit-logo-dark.svg"),
    "midnight": ("#071226", "called-to-edit-logo-dark.svg"),
    "champagne": ("#FCDD9E", "called-to-edit-logo-navy.svg"),
    "white": ("#FFFFFF", "called-to-edit-logo-light.svg"),
}

for name, (bg, logo) in VERSIONS.items():
    html = os.path.join(OUT, f"_{name}.html")
    src = "file:///" + os.path.join(HERE, "kit", logo).replace("\\", "/")
    open(html, "w", encoding="utf-8").write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;width:1080px;height:1920px;overflow:hidden}}'
        f'body{{background:{bg};display:grid;place-items:center}}img{{width:640px;display:block}}</style></head>'
        f'<body><img src="{src}"></body></html>')
    png = os.path.join(OUT, f"called-to-edit-status-{name}.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", "--window-size=1080,1920", "--virtual-time-budget=5000",
                    f"--screenshot={png}", "file:///" + html.replace("\\", "/")], capture_output=True)
    os.remove(html)
    im = Image.open(png)
    print(name, im.size)

# contact sheet for checking
ims = [Image.open(os.path.join(OUT, f"called-to-edit-status-{n}.png")).convert("RGB").resize((270, 480)) for n in VERSIONS]
sh = Image.new("RGB", (len(ims) * 278 + 8, 496), "#888")
for i, im in enumerate(ims):
    sh.paste(im, (8 + i * 278, 8))
sh.save(os.path.join(HERE, "status-check.jpg"), quality=90)
