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
QL = {4: "My example", 11: "My definition of editing", 23: "Say it like this", 46: "Say it like this"}
LINE = 26  # px per answer line

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Called to Edit Workbook: Your First 60 Days</title>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Plus+Jakarta+Sans:ital,wght@0,500;0,600;0,700;0,800;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="book.css"><link rel="stylesheet" href="wb.css"></head><body>
"""


def ans(lines, cls=""):
    return f'<div class="ans {cls}" style="height:{lines * LINE + 14}px"></div>'


def cb():
    return '<span class="cb"></span>'


def question(q, lines, hint):
    h = f'<div class="hint">{hint}</div>' if hint else ""
    return f'<div class="q"><div class="ql">{q}</div>{h}{ans(lines)}</div>'


def checks(items):
    return '<div class="chk">' + "".join(f'<div class="ci">{cb()}<span>{c}</span></div>' for c in items) + "</div>"


def day(d):
    n = d["n"]
    phase = next(p for p in PHASES if p["a"] <= n <= p["b"])
    o = [f'<section class="day dp1" id="d{n}"><span class="tm">MARKD{n}</span>',
         f'<div class="dh"><div class="dn"><span>Day</span>{n}</div><div class="meta"><span class="chip ph">Phase {phase["n"]}</span><span class="chip">{d["time"]}</span></div></div>',
         f'<h2>{d["t"]}</h2><div class="ref">{MKG}Book: {d["ch"]}</div>',
         f'<p class="why">{d["why"]}</p>']
    if d.get("quote"):
        o.append(f'<div class="box say"><div class="bl">{MKG}{QL.get(n, "In my words")}</div><p>&ldquo;{d["quote"]}&rdquo;</p></div>')
    if d.get("rhythm"):
        o.append(f'<div class="sec">{MK}Today&rsquo;s rhythm</div>' + checks(RHYTHM))
    else:
        o.append(f'<div class="sec">{MK}Do this</div><ol class="st">' + "".join(f"<li>{s}</li>" for s in d["steps"]) + "</ol>")
    o.append('<div class="notes"><div class="ql">Notes</div><div class="ans"></div></div>')
    if d.get("post"):
        o.append(f'<div class="box post"><div class="bl">{MKG}Post idea for today</div><p>{d["post"]}</p></div>')
    else:
        o.append('<div class="box post"><div class="bl">' + MKG + 'Post today</div><p>Two to three posts: 40% authentic, 40% authority, 20% sales.</p></div>')
    o.append("</section>")
    o.append(f'<section class="day dp2"><span class="tm">MARKA{n}</span><div class="ah"><span>Day {n}</span>{d["t"]}</div>')
    if d.get("rhythm"):
        o.append('<div class="nums">' + "".join(f'<div class="nm"><div class="ql">{k}</div>{ans(1, "sm")}</div>' for k in ["Names added", "Outreach sent", "Follow-ups sent", "Replies"]) + "</div>")
        qs = list(d.get("extra", [])) + [("The best thing that happened today, and what I&rsquo;ll fix tomorrow", 3, None)]
    else:
        if d.get("checks"):
            o.append(checks(d["checks"]))
        qs = d["qs"]
    for q, lines, hint in qs:
        h = f'<div class="hint">{hint}</div>' if hint else ""
        o.append(f'<div class="q" style="flex:{lines} 1 auto"><div class="ql">{q}</div>{h}<div class="ans" style="min-height:{lines * LINE + 14}px"></div></div>')
    o.append(f'<div class="done">{cb()}<span>Day {n} done</span><em>Share it in the Community</em></div></section>')
    return "\n".join(o)


def week(k):
    a, b = 7 * k - 6, 7 * k
    rows = "".join(f'<div class="tr"><div class="td">Day {i}</div>' + "".join(f'<div class="tc">{cb()}</div>' for _ in range(4)) + "</div>" for i in range(a, b + 1))
    nums = ["Followers now", "Posts this week"] + (["Outreach sent this week", "Replies this week"] if k >= 6 else ["Videos finished", "Editors I engaged"])
    return f"""<section class="week dp1" id="w{k}">
  <span class="kick">Week {k} check-in &middot; Days {a}&ndash;{b}</span>
  <h2>Week {k}, done. Look back before you go on.</h2>
  <div class="sec">{MK}Did you show up?</div>
  <p class="small">Tick each post and each day you commented on other people&rsquo;s posts. Two to three posts a day: 40% authentic, 40% authority, 20% sales.</p>
  <div class="trk"><div class="tr th"><div class="td"></div><div class="tc">Post 1</div><div class="tc">Post 2</div><div class="tc">Post 3</div><div class="tc">Comments</div></div>{rows}</div>
  <div class="sec">{MK}Your numbers</div>
  <div class="nums">{"".join(f'<div class="nm"><div class="ql">{x}</div>{ans(1, "sm")}</div>' for x in nums)}</div>
</section>
<section class="week dp2"><div class="ah"><span>Week {k}</span>Look back</div>
  {"".join(f'<div class="q" style="flex:{l} 1 auto"><div class="ql">{q}</div><div class="ans" style="min-height:{l * LINE + 14}px"></div></div>' for q, l in [("What did I finish this week?", 3), ("What slipped, and why?", 2), ("What worked best this week?", 2), ("One thing I&rsquo;ll do differently next week", 2)])}
  <div class="done">{cb()}<span>Week {k} check-in done</span><em>Post it in the Community</em></div>
</section>"""


def opener(p):
    items = "".join(f'<li><a href="#d{d["n"]}"><b>{d["n"]}</b>{d["t"]}</a></li>' for d in DAYS if p["a"] <= d["n"] <= p["b"])
    return f"""<section class="full op ph{p['n']}" id="p{p['n']}">
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
        items = "".join(f'<li><a href="#d{d["n"]}"><b>{d["n"]}</b><span>{d["t"]}</span></a></li>' for d in DAYS if p["a"] <= d["n"] <= p["b"])
        maps += f'<div class="mp"><div class="mh"><span>Phase {p["n"]}</span>{p["title"]}<em>Days {p["a"]}&ndash;{p["b"]}</em></div><ul>{items}</ul></div>'
    return f"""
<section class="full cover wbc">
  <img class="logo" src="kit/called-to-edit-logo-dark.svg" alt="Called to Edit">
  <div class="tl">The workbook</div>
  <div class="big">Your first 60 days <span class="g">to your first client</span></div>
  <div class="rule"></div>
  <div class="tag">One or two tasks a day, with questions you answer as you go.</div>
  <img class="photo" src="photos/samuel-cutout.webp" alt="">
  <div class="fade"></div>
  <div class="by"><div class="n">Samuel Adebayo</div><div class="r">Video editor and coach</div></div>
</section>

<section style="break-after:page">
  <span class="kick">Start here</span>
  <h2>How this workbook works</h2>
  <p class="lead">The book shows you the pathway. This workbook walks you down it, one day at a time, from choosing your niche to reaching out to the clients you want.</p>
  <ul class="mk">
    <li><b>One day at a time, in order.</b> Each day has one or two tasks and says how long they take.</li>
    <li><b>Missed a day? Don&rsquo;t skip it.</b> Pick up where you stopped. It&rsquo;s sixty steps, not sixty dates.</li>
    <li><b>Every day points to the book</b> chapter it comes from. Read it first if you haven&rsquo;t.</li>
    <li><b>Post every day.</b> Each day ends with a post idea. Showing your work is your leverage.</li>
    <li><b>Every seven days, a check-in.</b> Your posts, your numbers, what slipped.</li>
  </ul>
  <div class="box story"><div class="bl">{MKG}Typing your answers</div>
    <p>Tap any box and type. Open this file in <b>Adobe Acrobat Reader</b> (free on Android and iPhone), Xodo, or Google Drive on Android. Save after each day. If a box won&rsquo;t let you type, your app is only showing the file: open it in Acrobat Reader instead.</p></div>
  <div class="box remember"><div class="bl">{MKG}In the Community</div>
    <p>If you&rsquo;re in the Called to Edit Community, share each day&rsquo;s work there. I&rsquo;ll give you feedback, correct you and guide you as you go.</p></div>
  <div class="sec">{MK}What you&rsquo;ll need</div>
  <ul class="mk sm">
    <li><b>The book</b>, <i>Called to Edit: How to Build a Career as a Video Editor and Get Paid</i>. Every day points to a chapter.</li>
    <li><b>Your editing tool</b>: phone or laptop, and the software you already use.</li>
    <li><b>One social platform</b> you&rsquo;ll post on every day.</li>
    <li><b>Notion or a spreadsheet</b> for your dream client list (Day 36).</li>
    <li><b>Free accounts</b> on Canva, Loom and a booking-link tool such as Calendly or Cal.com (Days 32, 45 and 47).</li>
  </ul>
</section>

<section style="break-after:page">
  <span class="kick">Before Day 1</span>
  <h2>Your commitment</h2>
  <p class="small">Fill this in before Day 1. Come back to it on the days you don&rsquo;t feel like it.</p>
  {question("My name", 1, None)}
  <div class="nums">
    <div class="nm"><div class="ql">Day 1 is</div>{ans(1, "sm")}</div>
    <div class="nm"><div class="ql">Day 60 is</div>{ans(1, "sm")}</div>
  </div>
  {question("The hours I&rsquo;ll give this every day, and when", 1, None)}
  {question("Why I&rsquo;m doing this, in one line", 2, None)}
  {question("Who will hold me to it", 1, None)}
  {checks(["I&rsquo;ll do one day at a time, in order", "I&rsquo;ll post my work every day", "When I miss a day, I&rsquo;ll pick up where I stopped, not quit"])}
  <div class="nums">
    <div class="nm"><div class="ql">Signed (type your name)</div>{ans(1, "sm")}</div>
    <div class="nm"><div class="ql">Date</div>{ans(1, "sm")}</div>
  </div>
</section>

<section class="map" style="break-after:page">
  <span class="kick">The plan</span>
  <h2>Your 60 days at a glance</h2>
  <p class="small">Tap any day to go straight to it.</p>
  {maps}
</section>
"""


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


def assemble():
    body = [front()]
    for d in DAYS:
        p = next((p for p in PHASES if p["a"] == d["n"]), None)
        if p:
            body.append(opener(p))
        body.append(day(d))
        if d["n"] % 7 == 0 and d["n"] <= 56:
            body.append(week(d["n"] // 7))
    body.append(back())
    html = HEAD + "\n".join(body) + "\n</body></html>"
    path = os.path.join(HERE, "workbook.html")
    open(path, "w", encoding="utf-8").write(html)
    return path


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
