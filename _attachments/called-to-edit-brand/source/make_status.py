"""Logo on each brand background, ready to post: WhatsApp Status (1080 x 1920) and square posts (1080 x 1080)."""
import os, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# name: (background CSS, logo file) — the logo version always matches its background
VERSIONS = {
    "navy": ("#0A1F44", "called-to-edit-logo-dark.svg"),
    "navy-glow": ("radial-gradient(90% 60% at 50% 46%, #0A1F44 0%, #0A1F44 30%, #071226 100%)", "called-to-edit-logo-dark.svg"),
    "midnight": ("#071226", "called-to-edit-logo-dark.svg"),
    "champagne": ("#FCDD9E", "called-to-edit-logo-navy.svg"),
    "white": ("#FFFFFF", "called-to-edit-logo-light.svg"),
}
# format: (folder, file prefix, width, height, logo width)
FORMATS = {
    "status": ("status", "called-to-edit-status", 1080, 1920, 640),
    "square": ("square", "called-to-edit-square", 1080, 1080, 600),
}

for fmt, (folder, prefix, w, h, lw) in FORMATS.items():
    out = os.path.join(HERE, folder)
    os.makedirs(out, exist_ok=True)
    glow = "radial-gradient(75% 75% at 50% 48%, #0A1F44 0%, #0A1F44 30%, #071226 100%)" if h == w else None
    for name, (bg, logo) in VERSIONS.items():
        if name == "navy-glow" and glow:
            bg = glow
        html = os.path.join(out, f"_{name}.html")
        src = "file:///" + os.path.join(HERE, "kit", logo).replace("\\", "/")
        open(html, "w", encoding="utf-8").write(
            f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden}}'
            f'body{{background:{bg};display:grid;place-items:center}}img{{width:{lw}px;display:block}}</style></head>'
            f'<body><img src="{src}"></body></html>')
        png = os.path.join(out, f"{prefix}-{name}.png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--allow-file-access-from-files", f"--window-size={w},{h}", "--virtual-time-budget=5000",
                        f"--screenshot={png}", "file:///" + html.replace("\\", "/")], capture_output=True)
        os.remove(html)
        print(fmt, name, Image.open(png).size)

    # contact sheet for checking
    tw, th = 270, round(270 * h / w)
    ims = [Image.open(os.path.join(out, f"{prefix}-{n}.png")).convert("RGB").resize((tw, th)) for n in VERSIONS]
    sh = Image.new("RGB", (len(ims) * (tw + 8) + 8, th + 16), "#888")
    for i, im in enumerate(ims):
        sh.paste(im, (8 + i * (tw + 8), 8))
    sh.save(os.path.join(HERE, f"{folder}-check.jpg"), quality=90)
