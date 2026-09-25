"""Build the Route Rise #3 visual sheet (HTML) from beats.py + thumbnails."""
import os, sys, base64, html, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beats as BT

FPS = BT.FPS
END = 14267
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "visual-sheet.html")

def tc(f):
    s = f / FPS
    return "%d:%04.1f" % (int(s // 60), s % 60)

def thumb(bid):
    p = os.path.join(HERE, "_thumbs", bid + ".jpg")
    if not os.path.exists(p):
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

E = html.escape
SCREEN_TXT = {
    2143: "Clay demo: the Wedge Agent Feeder workflow and its checks (LinkedIn ads, Meta ads, SDR headcount, email infrastructure, ICP and TAM).",
    4064: "Railway demo: the playbook generated for Frontal.",
    4544: "Railway demo: the project canvas, the database and the agents running in the background.",
    6383: "Claude demo: the GTM OS inside Claude, the campaign steps, the email to the CRO.",
    9973: "Wispr Flow demo: styles, Transform, Insights, and frontal.so built by voice.",
}
beats = BT.B
vis = [b for b in beats if b["kind"] == "visual"]
ar = [b for b in beats if b["kind"] == "aroll"]
intro = [b for b in beats if b["kind"] == "intro"]

# ---------- timeline strip ----------
segs = []
for b in beats:
    if b["kind"] == "intro":
        continue
    segs.append((b["start"], b["end"], b["kind"]))
for s, e in BT.SCREEN_ON:
    segs.append((s, e, "screen"))
segs.append((0, 724, "intro"))
strip = []
for s, e, k in sorted(segs):
    x = s / END * 1000
    w = max(0.6, (e - s) / END * 1000)
    strip.append(f'<rect x="{x:.2f}" y="10" width="{w:.2f}" height="34" class="k-{k}"><title>{tc(s)} {k}</title></rect>')
ticks = []
for m in range(0, 11):
    f = m * 60 * FPS
    if f > END:
        break
    x = f / END * 1000
    ticks.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="46" y2="52" class="tick"/><text x="{x:.1f}" y="66" class="tl">{m}:00</text>')
chap_marks = []
for name, s, e, col, sw in BT.CHAPTERS:
    x = s / END * 1000
    chap_marks.append(f'<rect x="{x:.2f}" y="0" width="{(e - s) / END * 1000:.2f}" height="6" fill="{sw}"><title>{E(name)}</title></rect>')

def row(b):
    k = b["kind"]
    t = thumb(b["id"]) if k == "visual" else ""
    det = []
    if b.get("onscreen"):
        det.append(("On screen", ", ".join(b["onscreen"])))
    if b.get("depth"):
        det.append(("Depth → nodes", b["depth"]))
    if b.get("ground"):
        det.append(("Ground", b["ground"]))
    if b.get("motion"):
        det.append(("Motion", b["motion"]))
    if b.get("sfx"):
        det.append(("SFX", b["sfx"]))
    if b.get("notes"):
        det.append(("Note", b["notes"]))
    dl = "".join(f"<dt>{E(a)}</dt><dd>{E(v)}</dd>" for a, v in det)
    layer = {"full": "Full frame", "overlay": "Over A-roll (alpha)", "inset": "A-roll inside"}.get(b.get("layer"), "")
    kind_lbl = {"visual": "Visual", "aroll": "A-roll", "intro": "Idea only"}[k]
    img = f'<figure class="th"><img src="{t}" alt="{E(b["id"])} still" loading="lazy" width="480" height="270"></figure>' if t else ""
    return f'''<article class="beat k-{k}" id="{b["id"]}">
  <div class="tc"><span class="mono">{tc(b["start"])}</span><span class="dur mono">{(b["end"] - b["start"]) / FPS:.1f}s</span></div>
  <div class="body">
    <div class="meta"><span class="id mono">{b["id"]}</span><span class="chip c-{k}">{kind_lbl}</span>{f'<span class="ty">{E(b.get("type", ""))}</span>' if b.get("type") else ""}{f'<span class="ly">{layer}</span>' if layer else ""}</div>
    <p class="vo">“{E(b["vo"])}”</p>
    <p class="pic">{E(b.get("picture", ""))}</p>
    {f"<dl>{dl}</dl>" if dl else ""}
  </div>
  {img}
</article>'''

def screen_row(s, e):
    return f'''<article class="beat k-screen">
  <div class="tc"><span class="mono">{tc(s)}</span><span class="dur mono">{(e - s) / FPS:.1f}s</span></div>
  <div class="body"><div class="meta"><span class="chip c-screen">Screen recording</span><span class="ty">Your Tella + PIP, left as it is</span></div>
  <p class="pic">{E(SCREEN_TXT.get(s, ""))}</p></div>
</article>'''

sections = []
for name, s, e, col, sw in BT.CHAPTERS:
    items = [(b["start"], row(b)) for b in beats if s <= b["start"] <= e and b["kind"] != "intro"]
    items += [(ss, screen_row(ss, ee)) for ss, ee in BT.SCREEN_ON if s <= ss <= e]
    lead = ""
    if name.startswith("Hook"):
        items = [(b["start"], row(b)) for b in intro]
        lead = '<p class="lead">The intro is yours. These are ideas for it, and nothing is placed on the timeline before 0:30.2.</p>'
    items.sort(key=lambda x: x[0])
    nv = sum(1 for b in vis if s <= b["start"] <= e)
    sections.append(f'''<section class="chap" id="ch-{s}">
  <header class="ch"><span class="sw" style="background:{sw}" title="Resolve clip colour: {col}"></span><h2>{E(name)}</h2><span class="mono rng">{tc(s)}–{tc(e + 1)}</span><span class="cnt">{nv} visual{'s' if nv != 1 else ''} · clip colour {col}</span></header>
  {lead}{"".join(x[1] for x in items)}
</section>''')

toc = "".join(f'<a href="#ch-{s}"><span class="sw" style="background:{sw}"></span>{E(n)}</a>' for n, s, e, c, sw in BT.CHAPTERS)
today = datetime.date(2026, 9, 25).isoformat()

page = f'''<title>Route Rise #3 Visual Sheet</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500&display=swap">
<style>
:root {{
  --bg:#F1EFEC; --paper:#FFFFFF; --ink:#1B1715; --muted:#6D655E; --rule:#E0DAD3; --acc:#D9480F; --acc-soft:#FFE5D8;
  --vis:#FF5A1F; --aroll:#A69E96; --screen:#3B7DD8; --intro:#E0B620; --tick:#B9B1A9;
  color-scheme: light;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#131110; --paper:#1C1918; --ink:#F1ECE7; --muted:#A1978E; --rule:#2F2A27; --acc:#FF7A42; --acc-soft:#3A1B0E;
  --aroll:#6F6760; --tick:#5B544E; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg:#131110; --paper:#1C1918; --ink:#F1ECE7; --muted:#A1978E; --rule:#2F2A27; --acc:#FF7A42; --acc-soft:#3A1B0E;
  --aroll:#6F6760; --tick:#5B544E; color-scheme: dark; }}
body {{ background:var(--bg); color:var(--ink); font:15px/1.55 Geist, "Segoe UI", system-ui, sans-serif; }}
.wrap {{ max-width:1240px; margin:0 auto; padding-inline:20px; padding-block:40px 80px; }}
.mono {{ font-family:"Geist Mono", ui-monospace, Consolas, monospace; font-variant-numeric:tabular-nums; }}
.eyebrow {{ font-size:12px; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); font-weight:600; }}
h1 {{ font-size:clamp(32px,5vw,52px); line-height:1.02; letter-spacing:-.02em; margin:.3em 0 .2em; font-weight:800; text-wrap:balance; }}
h1 em {{ font-style:normal; color:var(--acc); }}
.sub {{ color:var(--muted); font-size:17px; margin:0 0 26px; max-width:70ch; }}
.stats {{ display:flex; flex-wrap:wrap; gap:10px 28px; margin:0 0 28px; }}
.stats div {{ display:flex; flex-direction:column; }}
.stats b {{ font-size:28px; font-weight:800; letter-spacing:-.01em; font-variant-numeric:tabular-nums; }}
.stats span {{ font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:.1em; }}
.how {{ background:var(--paper); border:1px solid var(--rule); border-radius:14px; padding:18px 22px; margin:0 0 26px; display:grid; gap:6px; }}
.how h3 {{ margin:0 0 4px; font-size:14px; letter-spacing:.08em; text-transform:uppercase; }}
.how ol {{ margin:0; padding-left:20px; }}
.how li {{ margin:2px 0; }}
.strip {{ background:var(--paper); border:1px solid var(--rule); border-radius:14px; padding:14px 16px 8px; margin:0 0 12px; overflow-x:auto; }}
.strip svg {{ width:100%; min-width:640px; height:auto; display:block; }}
.k-visual {{ fill:var(--vis); }} .k-aroll {{ fill:var(--aroll); }} .k-screen {{ fill:var(--screen); }} .k-intro {{ fill:var(--intro); }}
rect.k-aroll {{ opacity:.55; }}
.tick {{ stroke:var(--tick); }} .tl {{ font:11px "Geist Mono", monospace; fill:var(--muted); text-anchor:middle; }}
.legend {{ display:flex; flex-wrap:wrap; gap:6px 18px; font-size:13px; color:var(--muted); margin:0 0 30px; }}
.legend i {{ display:inline-block; width:12px; height:12px; border-radius:3px; margin-right:6px; vertical-align:-1px; }}
nav.toc {{ display:flex; flex-wrap:wrap; gap:8px; margin:0 0 40px; }}
nav.toc a {{ display:inline-flex; align-items:center; gap:8px; padding:6px 12px; border:1px solid var(--rule); border-radius:999px; background:var(--paper); color:var(--ink); text-decoration:none; font-size:13px; }}
nav.toc a:hover, nav.toc a:focus-visible {{ border-color:var(--acc); outline:none; }}
.sw {{ width:12px; height:12px; border-radius:3px; display:inline-block; flex:none; }}
.chap {{ margin:0 0 44px; }}
.ch {{ display:flex; flex-wrap:wrap; align-items:center; gap:8px 14px; padding:0 0 10px; border-bottom:2px solid var(--ink); margin-bottom:6px; }}
.ch h2 {{ margin:0; font-size:22px; letter-spacing:-.01em; }}
.ch .sw {{ width:16px; height:16px; }}
.ch .rng {{ color:var(--muted); font-size:13px; }}
.ch .cnt {{ margin-left:auto; color:var(--muted); font-size:13px; }}
.lead {{ margin:10px 0 4px; padding:10px 14px; border-radius:10px; background:var(--acc-soft); font-weight:500; }}
.beat {{ display:grid; grid-template-columns:92px minmax(0,1fr) 300px; gap:18px; padding:18px 0; border-bottom:1px solid var(--rule); }}
.beat.k-screen, .beat.k-aroll {{ grid-template-columns:92px minmax(0,1fr); padding:12px 0; }}
.tc {{ display:flex; flex-direction:column; gap:2px; font-size:14px; }}
.tc .dur {{ color:var(--muted); font-size:12px; }}
.meta {{ display:flex; flex-wrap:wrap; align-items:center; gap:6px 10px; margin-bottom:6px; font-size:13px; }}
.id {{ font-weight:500; }}
.chip {{ padding:2px 9px; border-radius:999px; font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }}
.c-visual {{ background:var(--acc-soft); color:var(--acc); }}
.c-aroll {{ background:transparent; border:1px solid var(--aroll); color:var(--muted); }}
.c-screen {{ background:color-mix(in srgb, var(--screen) 16%, transparent); color:var(--screen); }}
.c-intro {{ background:color-mix(in srgb, var(--intro) 22%, transparent); color:var(--ink); }}
.ty {{ font-weight:600; }}
.ly {{ color:var(--muted); }}
.vo {{ margin:0 0 8px; font-size:16px; font-weight:500; max-width:68ch; }}
.pic {{ margin:0 0 8px; color:var(--ink); max-width:70ch; }}
.k-screen .pic, .k-aroll .pic {{ color:var(--muted); margin:0; }}
dl {{ display:grid; grid-template-columns:max-content minmax(0,1fr); gap:3px 14px; margin:8px 0 0; font-size:13px; }}
dt {{ color:var(--muted); font-weight:600; white-space:nowrap; }}
dd {{ margin:0; }}
.th {{ margin:0; }}
.th img {{ width:100%; height:auto; max-width:100%; border-radius:10px; display:block; border:1px solid var(--rule); background:#000; }}
.notes {{ background:var(--paper); border:1px solid var(--rule); border-radius:14px; padding:18px 22px; }}
.notes h2 {{ margin:0 0 8px; font-size:18px; }}
.notes ul {{ margin:0; padding-left:20px; }}
.notes li {{ margin:4px 0; max-width:80ch; }}
@media (max-width:820px) {{
  .beat, .beat.k-screen, .beat.k-aroll {{ grid-template-columns:1fr; gap:8px; }}
  .tc {{ flex-direction:row; gap:10px; }}
  .th {{ order:3; }}
  .ch .cnt {{ margin-left:0; width:100%; }}
}}
</style>
<div class="wrap">
  <div class="eyebrow">Route Rise #3 · Visuals v1 · {today}</div>
  <h1>Visual sheet: <em>I Tried 100+ AI Tools</em></h1>
  <p class="sub">A visual for every main sentence of your final cut (9:55). Each one is rendered as a video and placed on the timeline so you can judge it in context, then approve, reject, or have it rebuilt as a Fusion comp.</p>
  <div class="stats">
    <div><b>{len(vis)}</b><span>Visuals on V7</span></div>
    <div><b>{len(ar)}</b><span>A-roll beats</span></div>
    <div><b>{len(BT.SCREEN_ON)}</b><span>Screen stretches kept</span></div>
    <div><b>{len(intro)}</b><span>Intro ideas (not placed)</span></div>
  </div>
  <div class="how">
    <h3>How to review</h3>
    <ol>
      <li>Resolve project <b>3. I Tried 100+ AI Tools…</b>, timeline <b>Visuals v1 (Editor)</b>, a duplicate of your Cut v6. Cut v6 is untouched.</li>
      <li>Visuals are on <b>V7 “Claude visuals v1”</b>, Apricot clips named by beat (B01_tracker1.mp4…). Full-frame beats are H.264, beats over the A-roll are ProRes 4444 with alpha.</li>
      <li>For each beat: keep, reject, or mark it “rebuild in Fusion”. Every effect here maps to a node you use (NeoBevel, NeoLightSweep Pro, NeoGlow, DropShadow, NeoReflection), listed under “Depth → nodes”.</li>
    </ol>
  </div>
  <div class="strip" role="img" aria-label="Where visuals, A-roll and screen recording sit across the 9:55 cut">
    <svg viewBox="-24 0 1048 72" preserveAspectRatio="none">{"".join(chap_marks)}{"".join(strip)}{"".join(ticks)}</svg>
  </div>
  <div class="legend"><span><i style="background:var(--intro)"></i>Intro (yours)</span><span><i style="background:var(--vis)"></i>Visual</span><span><i style="background:var(--aroll);opacity:.55"></i>A-roll</span><span><i style="background:var(--screen)"></i>Screen recording</span><span>Top band: chapter clip colours</span></div>
  <nav class="toc" aria-label="Chapters">{toc}</nav>
  {"".join(sections)}
  <div class="notes">
    <h2>Open items</h2>
    <ul>
      <li>Tool logos: the tool cards show each tool's real UI from the Tella recording instead of a logo. Official Clay, Railway and Wispr Flow logos can be dropped in when these become Fusion comps.</li>
      <li>Example data (Northwind, Acme Corp, Sarah Lee, the email copy) is illustrative, not client data. The only real figures used are from the footage: 168 wpm (Alex's Wispr Flow insights), 5,000 and 25 (his words).</li>
      <li>B64 “Watch next” uses a placeholder thumbnail and title. The real end-screen video isn't known yet.</li>
      <li>B31 shows a rebuilt “Book Your Strategy Call” card; the Tella frame of that page was still loading.</li>
      <li>Check by ear before captions: “one provider can find” (can't?), “ICP and time estimates” (TAM?). B07 is built on “can't”.</li>
      <li>Music, SFX and MagicZoom punch-ins on the A-roll beats aren't placed. The SFX column suggests where hits could go.</li>
    </ul>
  </div>
</div>
'''
open(out, "w", encoding="utf-8").write(page)
print(out, len(page) // 1024, "KB")
