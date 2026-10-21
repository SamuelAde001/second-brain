"""Build the Called to Edit workbook: days.py -> workbook.html -> PDF with tappable answer boxes, plus preview sheets."""
import glob, os, re, subprocess, sys
import pymupdf
from PIL import Image
from days import DAYS, PHASES, RHYTHM

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
RAW = os.path.join(HERE, "raw.pdf")
OUT = os.path.join(HERE, "Called-to-Edit-Workbook-Your-First-60-Days.pdf")

MK = '<svg class="mk" width="14" height="16" viewBox="0 0 14 16"><path d="M0 0H14V9.6L7 16L0 9.6Z" fill="#8A5E17"/></svg>'
MKG = '<svg width="12" height="14" viewBox="0 0 14 16"><path d="M0 0H14V9.6L7 16L0 9.6Z" fill="currentColor"/></svg>'
QL = {4: "My example", 41: "Example"}
LINE = 28  # px per answer line

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Called to Edit Workbook: Your First 60 Days</title>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Plus+Jakarta+Sans:ital,wght@0,500;0,600;0,700;0,800;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="book.css"><link rel="stylesheet" href="wb.css"><link rel="stylesheet" href="lean.css"></head><body>
"""


def ans(lines, cls=""):
    return f'<div class="ans {cls}" style="height:{lines * LINE + 14}px"></div>'


def cb():
    return '<span class="cb"></span>'


def ticks(items):
    return '<div class="chk">' + "".join(f'<div class="ci">{cb()}<span>{c}</span></div>' for c in items) + "</div>"


def head(label, num, time, ch, title):
    return (f'<div class="dh"><div class="dn"><span>{label}</span>{num}</div><div class="meta"><span class="chip">{time}</span></div></div>'
            f'<h2>{title}</h2><div class="ref">{MKG}Book: {ch}</div>')


def day(d):
    n = d["n"]
    o = [f'<section class="day" id="d{n}"><span class="tm">MARKD{n}</span>', head("Day", n, d["time"], d["ch"], d["t"]),
         f'<p class="why">{d["why"]}</p>']
    if d.get("say"):
        o.append(f'<div class="box say"><div class="bl">{MKG}{QL.get(n, "Say it like this")}</div><p>&ldquo;{d["say"]}&rdquo;</p></div>')
    o.append(f'<div class="sec">{MK}Today</div><ol class="st">' + "".join(f"<li>{s}</li>" for s in d["do"]) + "</ol>")
    if d.get("ticks"):
        o.append(ticks(d["ticks"]))
    for label, lines in d.get("box", []):
        o.append(f'<div class="q"><div class="ql">{label}</div>{ans(lines)}</div>')
    o.append(f'<div class="done">{cb()}<span><b>Done when:</b> {d["done"]}</span></div></section>')
    return "\n".join(o)


def block(d):
    rows = "".join(f'<div class="br"><div class="bd">Day {n}</div><div class="bx">{x or "Your five"}</div>{cb()}</div>' for n, x in d["items"])
    marks = "".join(f'<span class="tm">MARKD{n}</span>' for n, _ in d["items"])
    return f"""<section class="day" id="d{d['a']}">{marks}{head("Days", f"{d['a']}&ndash;{d['b']}", d["time"], d["ch"], d["t"])}
  <p class="why">{d["why"]}</p>
  <div class="sec">{MK}Your five, every day</div>
  <ul class="mk five">{"".join(f"<li>{r}</li>" for r in RHYTHM)}</ul>
  <div class="sec">{MK}Tick each day when your five are done</div>
  <div class="blk">{rows}</div>
</section>"""


def week(k):
    a, b = 7 * k - 6, 7 * k
    row = "".join(f'<div class="wd"><div>{i}</div>{cb()}</div>' for i in range(a, b + 1))
    return f"""<section class="week" id="w{k}">
  <span class="kick">Week {k} check-in</span>
  <h2>Days {a}&ndash;{b}, done</h2>
  <div class="sec">{MK}Did you post every day?</div>
  <div class="wk">{row}</div>
  <div class="q"><div class="ql">What slipped this week, and what will you do about it?</div>{ans(3)}</div>
  <p class="small">Missed something? Don&rsquo;t skip it. Do it first next week.</p>
</section>"""


def opener(p):
    return f"""<section class="full op" id="p{p['n']}">
  <img class="logo" src="kit/called-to-edit-logo-dark.svg" alt="">
  <div class="num">{p['n']}</div>
  <div class="lab">{MKG}<span>Phase {p['n']} &middot; Days {p['a']}&ndash;{p['b']}</span></div>
  <h1>{p['title']}</h1>
  <div class="sub">{p['sub']}</div>
  <div class="art"><div class="qr"></div><div class="qt">&ldquo;{p['quote']}&rdquo;</div></div>
  <span class="tm">MARKP{p['n']}</span>
</section>"""


def front():
    maps = ""
    for p in PHASES:
        items = ""
        for d in DAYS:
            if d.get("block") and p["a"] <= d["a"] <= p["b"]:
                items += f'<li><a href="#d{d["a"]}"><b>{d["a"]}&ndash;{d["b"]}</b><span>{d["t"]}</span></a></li>'
            elif not d.get("block") and p["a"] <= d["n"] <= p["b"]:
                items += f'<li><a href="#d{d["n"]}"><b>{d["n"]}</b><span>{d["t"]}</span></a></li>'
        maps += f'<div class="mp"><div class="mh"><span>Phase {p["n"]}</span>{p["title"]}<em>Days {p["a"]}&ndash;{p["b"]}</em></div><ul>{items}</ul></div>'
    return f"""
<section class="full cover wbc">
  <img class="logo" src="kit/called-to-edit-logo-dark.svg" alt="Called to Edit">
  <div class="tl">The workbook</div>
  <div class="big">Your first 60 days <span class="g">to your first client</span></div>
  <div class="rule"></div>
  <div class="tag">One clear task a day. Simple steps, no fluff.</div>
  <img class="photo" src="photos/samuel-cutout.webp" alt="">
  <div class="fade"></div>
  <div class="by"><div class="n">Samuel Adebayo</div><div class="r">Video editor and coach</div></div>
</section>

<section style="break-after:page">
  <span class="kick">Start here</span>
  <h2>How this works</h2>
  <ol class="st">
    <li><b>One day at a time.</b> Each day has one or two tasks and a clear finish line: <b>Done when</b>.</li>
    <li><b>Missed a day?</b> Pick up where you stopped. It&rsquo;s 60 steps, not 60 dates.</li>
    <li><b>Every day, post about your journey.</b> Two to three posts. Ideas on the next page.</li>
    <li><b>Stuck?</b> Each day names the book chapter it comes from.</li>
  </ol>
  <div class="box story"><div class="bl">{MKG}Typing in this workbook</div>
    <p>Tap a box to type or tick. Open the file in <b>Adobe Acrobat Reader</b> (free on Android and iPhone), Xodo or Google Drive. If you can&rsquo;t tap a box, open it in Acrobat Reader.</p></div>
  <div class="box remember"><div class="bl">{MKG}In the Community</div>
    <p>Share each day&rsquo;s work in the Called to Edit Community. I&rsquo;ll give you feedback and guide you as you go.</p></div>
</section>

<section style="break-after:page">
  <span class="kick">Every day</span>
  <h2>What to post</h2>
  <p>Post your journey, not just finished work. Mix it like this:</p>
  <div class="pi"><div class="pt"><b>40%</b> Authentic</div><p>Your day, your story, your wins and failures. &ldquo;Day 12 of 60: learning captions.&rdquo; A photo of your timeline. A client who said no.</p></div>
  <div class="pi"><div class="pt"><b>40%</b> Authority</div><p>Teach what you&rsquo;re learning. &ldquo;3 mistakes in business videos.&rdquo; A before and after. Your recreation next to the original.</p></div>
  <div class="pi gold"><div class="pt"><b>20%</b> Sales</div><p>Say what you do. &ldquo;I edit ___ for ___. I&rsquo;m taking on new clients.&rdquo;</p></div>
</section>

<section class="map" style="break-after:page">
  <span class="kick">The plan</span>
  <h2>Your 60 days</h2>
  <p class="small">Tap a day to jump to it.</p>
  {maps}
</section>
"""


def assemble():
    body = [front()]
    weeks_done = set()
    for d in DAYS:
        first = d["a"] if d.get("block") else d["n"]
        last = d["b"] if d.get("block") else d["n"]
        p = next((p for p in PHASES if p["a"] == first), None)
        if p:
            body.append(opener(p))
        body.append(block(d) if d.get("block") else day(d))
        for k in range(1, 9):
            if first <= 7 * k <= last and k not in weeks_done:
                weeks_done.add(k)
                body.append(week(k))
    body.append(back())
    html = HEAD + "\n".join(body) + "\n</body></html>"
    path = os.path.join(HERE, "workbook.html")
    open(path, "w", encoding="utf-8").write(html)
    return path


def back():
    return f"""
<section class="full community" style="display:flex;flex-direction:column;padding:44px 38px 46px">
  <img class="logo" src="kit/called-to-edit-community-dark.svg" alt="Called to Edit Community" style="width:170px">
  <div style="margin-top:auto">
    <div style="font:700 13px 'Plus Jakarta Sans';color:#FCDD9E;letter-spacing:.2em;text-transform:uppercase;margin-bottom:12px">You don&rsquo;t have to do this alone</div>
    <div style="font:400 44px/1 Gloock;letter-spacing:-.04em;color:#fff;margin-bottom:18px">Do the 60 days with editors who are doing them too</div>
    <p style="font:500 17.5px/1.5 'Plus Jakarta Sans';color:#B9C3D6">Post each day&rsquo;s work in the Called to Edit Community. I&rsquo;ll give you feedback on your edits, your outreach and your profile, and correct you as you go.</p>
    <ul class="mk" style="color:#fff;font-size:17.5px;margin-top:14px">
      <li>Feedback from me on your work, your outreach and your profile</li>
      <li>Calls with me inside the community</li>
      <li>Editors at your level, on the same 60 days</li>
    </ul>
  </div>
  <div style="margin-top:22px;background:#FCDD9E;border-radius:18px;padding:18px 22px;color:#0A1F44">
    <div style="font:400 40px/1 Gloock;letter-spacing:-.03em">NGN 5,000<span style="font:600 17px 'Plus Jakarta Sans'"> a month</span></div>
    <div style="font:600 15px/1.45 'Plus Jakarta Sans';margin-top:6px">About USD 4. Open to any editor, anywhere. Find me on Instagram: @SamuelSignals</div>
  </div>
</section>
<section class="full mid" style="display:flex;flex-direction:column;justify-content:center;padding:0 38px">
  <img src="kit/called-to-edit-logo-dark.svg" alt="Called to Edit" style="width:200px">
  <div style="font:400 30px/1.15 Gloock;letter-spacing:-.02em;color:#FCDD9E;margin-top:28px">I coach video editors to get paid.</div>
  <div style="font:600 14px/1.5 'Plus Jakarta Sans';color:#B9C3D6;margin-top:18px">&copy; 2026 Samuel Adebayo, Called to Edit. All rights reserved.</div>
</section>
"""


def render(html):
    url = "file:///" + html.replace("\\", "/")
    subprocess.run([CHROME, "--headless=new", f"--user-data-dir={os.path.join(HERE, 'chrome-prof')}",
                    "--no-pdf-header-footer", "--virtual-time-budget=20000", "--run-all-compositor-stages-before-draw",
                    f"--print-to-pdf={RAW}", url], capture_output=True)


TXT = (246, 247, 251)
CHK = (255, 253, 247)


def add_fields():
    d = pymupdf.open(RAW)
    nt = nc = 0
    for pno, page in enumerate(d):
        boxes = []
        for dr in page.get_drawings():
            f = dr.get("fill")
            if not f:
                continue
            c = tuple(round(x * 255) for x in f[:3])
            if c in (TXT, CHK):
                boxes.append((c, dr["rect"]))
        boxes.sort(key=lambda b: (round(b[1].y0), b[1].x0))
        for c, r in boxes:
            w = pymupdf.Widget()
            w.border_width = 0
            w.border_color = None
            w.fill_color = None
            if c == TXT:
                nt += 1
                w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
                w.field_name = f"answer_{nt:03d}"
                w.rect = pymupdf.Rect(r.x0 + 6, r.y0 + 4, r.x1 - 6, r.y1 - 4)
                w.text_font = "Helv"
                w.text_fontsize = 12
                w.text_color = (10 / 255, 31 / 255, 68 / 255)
                if r.height > 40:
                    w.field_flags |= pymupdf.PDF_TX_FIELD_IS_MULTILINE
            else:
                nc += 1
                w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
                w.field_name = f"tick_{nc:03d}"
                w.rect = pymupdf.Rect(r.x0 + 1, r.y0 + 1, r.x1 - 1, r.y1 - 1)
                w.text_color = (138 / 255, 94 / 255, 23 / 255)
                w.field_value = False
            page.add_widget(w)
    d.set_metadata({"title": "Called to Edit Workbook: Your First 60 Days", "author": "Samuel Adebayo", "subject": "From your first lesson to your first client"})
    d.save(OUT, garbage=3, deflate=True)
    return nt, nc, len(d)


def sheets(scale=0.42, per=8, only=None, src=None):
    d = pymupdf.open(src or OUT)
    os.makedirs(os.path.join(HERE, "sheets"), exist_ok=True)
    for f in glob.glob(os.path.join(HERE, "sheets", "*.jpg")):
        os.remove(f)
    imgs = []
    for i, p in enumerate(d):
        if only and (i + 1) not in only:
            continue
        pm = p.get_pixmap(matrix=pymupdf.Matrix(scale * 4 / 3, scale * 4 / 3))
        imgs.append((i + 1, Image.frombytes("RGB", (pm.width, pm.height), pm.samples)))
    for s in range(0, len(imgs), per):
        chunk = imgs[s:s + per]
        w, h = chunk[0][1].size
        rows = (len(chunk) + 3) // 4
        sheet = Image.new("RGB", (4 * (w + 8), rows * (h + 8)), (120, 120, 120))
        for k, (n, im) in enumerate(chunk):
            sheet.paste(im, ((k % 4) * (w + 8), (k // 4) * (h + 8)))
        sheet.save(os.path.join(HERE, "sheets", f"s{chunk[0][0]:03d}.jpg"), quality=82)


if __name__ == "__main__":
    render(assemble())
    print("fields text/ticks/pages", add_fields())
    sheets()
