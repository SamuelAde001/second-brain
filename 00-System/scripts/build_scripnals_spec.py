"""Build the Scripnals AI spec PDF that goes to the devs.

Source of truth: 03-Areas/scripnals/ai-workflow.md (the Brain note).
Figures: drawn from 03-Areas/scripnals/assets/*.html, saved as PNGs in _attachments/scripnals/.

  python 00-System/scripts/build_scripnals_spec.py              # rebuild the PDF only
  python 00-System/scripts/build_scripnals_spec.py --figures    # re-draw the flow chart and screens first
  python 00-System/scripts/build_scripnals_spec.py --out <file.pdf>

What the PDF leaves out: the frontmatter, the "Status:" line and the "Brain only" footer.
A figure whose file name contains "flow" gets its own landscape page, with the heading above it.
Needs Google Chrome and internet access (marked.js loads from a CDN).
"""
import argparse, json, pathlib, re, subprocess, sys

BRAIN = pathlib.Path(__file__).resolve().parents[2]
NOTE = BRAIN / "03-Areas" / "scripnals" / "ai-workflow.md"
ASSETS = BRAIN / "03-Areas" / "scripnals" / "assets"
ATT = BRAIN / "_attachments" / "scripnals"
DEFAULT_OUT = ASSETS / "scripnals-script-buddy-ai-workflow-v1.pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def chrome(*args, capture=False):
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    return r.stdout if capture else None


def shot(html, png, width, height, query=""):
    chrome("--hide-scrollbars", "--force-device-scale-factor=2", f"--window-size={width},{height}",
           "--virtual-time-budget=3000", f"--screenshot={png}", html.as_uri() + query)
    print("drew", png.name)


def figures():
    flow = ASSETS / "script-buddy-flow.html"
    dom = chrome(f"--window-size=1400,1200", "--virtual-time-budget=3000", "--dump-dom", flow.as_uri(), capture=True) or ""
    m = re.search(r'data-h="(\d+)"', dom)
    shot(flow, ATT / "script-buddy-flow.png", 1400, int(m.group(1)) if m else 930)
    mocks = ASSETS / "script-buddy-mockups.html"
    for row in (1, 2):
        shot(mocks, ATT / f"script-buddy-mockup-row{row}.png", 1000, 700, f"?row={row}")


def build(out):
    md = NOTE.read_text(encoding="utf8")
    md = re.sub(r"^---\n.*?\n---\n", "", md, count=1, flags=re.S)
    md = re.sub(r"\n---\n\n\*Brain only.*\Z", "\n", md, flags=re.S)
    md = re.sub(r"^Status: .*\n\n?", "", md, flags=re.M)

    def fig(file, heading=None):
        uri = (ATT / file).as_uri()
        if "flow" in file:
            h = f"<h2>{heading}</h2>" if heading else ""
            return f'<div class="landscape">{h}<img class="fig" src="{uri}"></div>'
        return f'<img class="fig mock" src="{uri}">'

    md = re.sub(r"## ([^\n]+)\n+!\[\[([^\]|]*flow[^\]|]*\.png)\]\]", lambda m: fig(m.group(2), m.group(1)), md)
    md = re.sub(r"!\[\[([^\]|]+\.png)\]\]", lambda m: fig(m.group(1)), md)

    css = """
  @page { size: A4; margin: 16mm 15mm 18mm; }
  @page wide { size: A4 landscape; margin: 10mm; }
  :root { --navy:#12325a; --ink:#1d2433; --muted:#5b6475; --gold:#c9971c; --cream:#faf7f1; --line:#e4dccd; }
  body { font-family: "Segoe UI", Roboto, Arial, sans-serif; color: var(--ink); font-size: 10.5pt; line-height: 1.5; margin: 0; }
  h1 { color: var(--navy); font-size: 21pt; margin: 0 0 4px; border-bottom: 3px solid var(--gold); padding-bottom: 6px; }
  h1 + p { color: var(--muted); margin-top: 6px; }
  h2 { color: var(--navy); font-size: 13.5pt; margin: 20px 0 6px; break-after: avoid; }
  strong { color: var(--navy); }
  table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 9.5pt; break-inside: avoid; }
  th { background: var(--navy); color: #fff; text-align: left; padding: 6px 8px; }
  td { border-bottom: 1px solid var(--line); padding: 6px 8px; vertical-align: top; }
  tr:nth-child(even) td { background: var(--cream); }
  pre { background: #0f1b2d; color: #e8edf5; padding: 10px 12px; border-radius: 6px; font-size: 8.6pt; line-height: 1.45; white-space: pre-wrap; }
  code { font-family: Consolas, "Cascadia Mono", monospace; }
  p code, li code, td code { background: #f1ece2; padding: 0 4px; border-radius: 3px; font-size: 9pt; }
  ul, ol { padding-left: 20px; } li { margin: 2px 0; }
  .landscape { page: wide; }
  .landscape h2 { margin-top: 0; }
  .landscape img.fig { width: auto; max-width: 100%; max-height: 172mm; margin: 0 auto; }
  img.fig { display: block; width: 100%; break-inside: avoid; }
  img.mock { width: 92%; margin: 6px auto 10px; }
"""
    html = ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<title>Scripnals · Script buddy AI workflow</title>"
            "<script src=\"https://cdn.jsdelivr.net/npm/marked@12/marked.min.js\"></script>"
            f"<style>{css}</style></head><body><main id=\"doc\"></main>"
            f"<script>document.getElementById('doc').innerHTML = marked.parse({json.dumps(md)});</script>"
            "</body></html>")
    tmp = out.with_suffix(".html")
    tmp.write_text(html, encoding="utf8")
    chrome("--no-pdf-header-footer", "--allow-file-access-from-files", "--virtual-time-budget=15000",
           f"--print-to-pdf={out}", tmp.as_uri())
    tmp.unlink()
    pages = len(re.findall(rb"/MediaBox", out.read_bytes()))
    print(f"built {out} ({out.stat().st_size // 1024} KB, {pages} pages)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--figures", action="store_true", help="re-draw the flow chart and screen PNGs first")
    ap.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT)
    a = ap.parse_args()
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    if a.figures:
        figures()
    build(a.out.resolve())
