"""Rows 10-12: pricing and getting paid, growing through people, next steps and the close."""
from lib import *

P = {}


def src(k):
    return P.get(k)


def row10():
    op = opener(10, "Price yourself and", "Get paid", "Price per video from a rate card, price what the video is worth to the client, get to packages fast, and protect yourself.",
                "Stop collecting single projects.")
    f1 = frame("10.1", "Pricing · How you count", f"""
{title('A lot of us price ourselves wrongly.', 'Count per video.', 104)}
<div class="abs" style="left:110px;top:430px;width:1700px;display:flex;gap:30px">
  {rv(f'<div class="card gold" style="width:546px;height:330px">{icon("circle-check", 70, NAVY, 2)}<div class="ct" style="font-size:44px">Per video</div><div class="cb">Per project. How freelancers charge.</div></div>', 'Right or wrong?')}
  {rv(f'<div class="card line" style="width:546px;height:330px">{icon("circle-x", 70, MIST)}<div class="ct" style="font-size:44px;color:{MIST}">Per month</div><div class="cb">That\'s a salary. Companies pay wages.</div></div>', 'Right or wrong?')}
  {rv(f'<div class="card line" style="width:546px;height:330px">{icon("circle-x", 70, MIST)}<div class="ct" style="font-size:44px;color:{MIST}">Per minute</div><div class="cb">Length doesn\'t measure the work.</div></div>', 'Right or wrong?')}
</div>
<div class="abs" style="left:110px;bottom:90px;width:1700px"><div class="sub">A one-minute video can have as much work as a 20-minute video. <b>If a client offers to pay per minute, don't take that deal.</b></div></div>""")

    tiers = [("1", "Under 20 minutes", "Simple cut, talking head, a few captions"), ("2", "Under 20 minutes", "Motion graphics, B-roll, research from me"), ("3", "Over 20 minutes", "Motion graphics")]
    f2 = frame("10.2", "Pricing · Have a rate card", f"""
{title('One card that shows', 'your price tiers.', 110)}
<div class="abs" style="left:110px;top:420px;width:860px">
  <div class="mock" style="padding:30px 36px">
    <div style="font:800 18px 'Plus Jakarta Sans';letter-spacing:.14em;color:#8A5E17">RATE CARD · MINE, AS A LONG-FORM EDITOR</div>
    {''.join(f'<div style="display:flex;align-items:center;gap:24px;border-bottom:2px solid #E3E7EF;padding:18px 0"><div style="font-family:Gloock;font-size:56px;color:#8A5E17;width:50px">{n}</div><div style="flex:1"><div style="font:800 28px \'Plus Jakarta Sans\'">{h}</div><div style="font:500 22px \'Plus Jakarta Sans\';color:#4A5670">{b}</div></div><div style="font:800 24px \'Plus Jakarta Sans\';color:#4A5670;border:2px dashed #B9C3D6;border-radius:12px;padding:8px 16px">your price</div></div>' for n, h, b in tiers)}
  </div>
  <div class="cb" style="margin-top:16px;font-size:23px">The client sees what changes the price, and you can budget around it together.</div>
</div>
<div class="abs" style="left:1050px;top:420px;width:760px;display:flex;flex-direction:column;gap:20px">
  <div class="step">{mark(16)} What sets your number: skill, confidence, the kind of client</div>
  {rv(f'<div class="card"><div class="tag line">A beginner, learning</div><div class="num" style="font-size:90px">$5–10</div><div class="cb">per short-form video, for simple work you\'re learning on</div></div>', 'Beginner?')}
  {rv(f'<div class="card gold"><div class="tag" style="background:{NAVY};color:{CH}">Good international clients</div><div class="num" style="font-size:90px;color:{NAVY}">$20–30</div><div class="cb">per short-form video, what they used to pay</div></div>', 'International?')}
</div>""")

    faders = ["Skill and confidence", "The client's business", "What the video is for", "The work inside it", "Niche and length", "Revisions", "The result you get them"]
    fy = [180, 90, 40, 120, 200, 150, 60]
    fd = "".join(
        f'<g transform="translate({60 + k*150} 0)"><rect x="-6" y="20" width="12" height="360" rx="6" fill="{SLATE}"/>'
        f'<rect x="-44" y="{fy[k]}" width="88" height="46" rx="10" fill="{CH}"/><line x1="-26" x2="26" y1="{fy[k]+23}" y2="{fy[k]+23}" stroke="{NAVY}" stroke-width="5"/></g>' for k in range(7))
    labs = "".join(f'<div class="abs" style="left:{k*150 - 15}px;top:400px;width:150px;text-align:center;font:700 21px/1.25 \'Plus Jakarta Sans\'">{t}</div>' for k, t in enumerate(faders))
    f3 = frame("10.3", "Pricing · What moves your price", f"""
{title('There is no fixed price.', 'It\'s a mixing desk.', 104)}
<div class="abs" style="left:110px;top:400px;width:1060px;height:560px">{svg(fd, 'position:absolute;left:0;top:0', 1060, 400)}{labs}</div>
<div class="abs" style="left:1200px;top:180px;width:610px;display:flex;flex-direction:column;gap:18px">
  <div class="step">{mark(16)} Take control of the price</div>
  {''.join(f'<div class="li" style="font-size:24px">{icon(i, 38)}<span>{t}</span></div>' for i, t in [('message-circle', '<b>Ask questions first:</b> &ldquo;Do you want motion graphics? What style? What do you want to achieve?&rdquo;'), ('lightbulb', '<b>When they say it\'s too much, explain why:</b> &ldquo;There\'s motion graphics in this.&rdquo;'), ('phone-call', '<b>Price on a call</b>, so you can negotiate properly.')])}
  <div class="cb" style="font-size:22px">Paid adverts and business videos are tied to money: <b>always charge more</b>. Set revisions in the deal, e.g. &ldquo;3 rounds of revisions&rdquo;.</div>
  {remember("Don't be afraid of no's. Don't be afraid of rejection. It's part of the journey.")}
</div>""")

    f4 = frame("10.4", "Pricing · Stop collecting single projects", f"""
{title("It's easier to sell a package", 'than one video.', 110)}
<div class="abs" style="left:110px;top:430px;width:1100px;display:flex;gap:26px">
  {rv(f'<div class="card gold" style="width:537px;height:330px">{icon("film", 60, NAVY, 2)}<div class="tag" style="background:{NAVY};color:{CH}">Long-form package</div><div class="num" style="font-size:110px;color:{NAVY}">$5,000</div><div class="cb">5 long-form videos a month</div></div>', 'Long-form package')}
  {rv(f'<div class="card gold" style="width:537px;height:330px">{icon("smartphone", 60, NAVY, 2)}<div class="tag" style="background:{NAVY};color:{CH}">Short-form package</div><div class="num" style="font-size:110px;color:{NAVY}">$3,000</div><div class="cb">30 short-form videos a month</div></div>', 'Short-form package')}
</div>
<div class="abs" style="left:1280px;top:430px;width:530px;display:flex;flex-direction:column;gap:18px">
  <div class="li" style="font-size:24px">{icon('user-round-check', 40)}<span><b>Mine now:</b> 3 to 6 videos a month for my client, paid at the end of the month.</span></div>
  <div class="li" style="font-size:24px">{icon('repeat', 40)}<span>Packages need a <b>retainer client</b>: someone who posts consistently and works with you long term.</span></div>
  {rv(f'<div class="card"><div class="ct" style="font-size:28px">Add-ons</div><div class="cb" style="font-size:23px">Ideation (only if you really know how), scripting or thumbnails, so the client pays <b>USD 1,000 instead of USD 500</b>.</div></div>', 'Add-ons')}
</div>""")

    f5 = frame("10.5", "Pricing · Don't get scammed", f"""
{title('The scam is simple:', 'Deliver. Never paid.', 100)}
<div class="abs" style="left:110px;top:430px;width:860px">
  {rv(f'<div class="card gold" style="flex-direction:row;align-items:center;gap:30px"><div class="num" style="font-size:150px;color:{NAVY}">30%</div><div class="ct" style="font-size:34px">upfront before you start</div></div>', 'Before you start…')}
  {''.join(f'<div class="li" style="margin-top:18px;font-size:25px">{icon(i, 38)}<span>{t}</span></div>' for i, t in [('package', '<b>On a new bundle, always.</b> 20 or 30 videos a month with a new client? Don\'t wait until all are done for the first payment.'), ('file-pen-line', '<b>Write a contract and have them sign it.</b> Not something they said or typed in a chat.'), ('handshake', 'A long-time client can pay at the end of the month. Mine does.')])}
</div>
<div class="abs" style="left:1060px;top:330px;width:750px">
  <div class="mock" style="padding:34px 40px;height:640px;display:flex;flex-direction:column">
    <div style="font:800 18px 'Plus Jakarta Sans';letter-spacing:.14em;color:#8A5E17">AGREEMENT · EXAMPLE</div>
    <div style="font:800 40px 'Plus Jakarta Sans';margin-top:16px">5 videos a month</div>
    {''.join(f'<div style="display:flex;gap:14px;align-items:center;font:600 27px \'Plus Jakarta Sans\';margin-top:22px">{icon("check", 34, BRONZE, 2.4)}{t}</div>' for t in ['30% paid upfront for the 5', 'Balance paid on delivery', '3 rounds of revisions per video'])}
    <div style="margin-top:auto;display:flex;gap:30px">{''.join(f'<div style="flex:1;border-top:3px solid #0A1F44;padding-top:10px;font:600 22px \'Plus Jakarta Sans\';color:#4A5670">{t}</div>' for t in ['Client signature', 'Editor signature'])}</div>
  </div>
</div>""")

    pays = [("Cleva", "Mine. A US dollar account; convert to naira. Small deposit fee.", True), ("Grey", "USD, GBP and EUR accounts. Good for UK and EU clients.", False),
            ("Raenest", "A USD account built for freelancers.", False), ("Payoneer", "For Fiverr, Upwork and clients who use it. Usually dearest into naira.", False),
            ("PayPal", "Not a way to get paid in Nigeria: mostly for paying, not receiving.", False)]
    f6 = frame("10.6", "Getting paid · From abroad", f"""
{title('What works depends on where you live', 'and where your client is.', 92)}
<div class="abs" style="left:110px;top:420px;width:1700px;display:flex;gap:22px">
  {''.join(f'<div class="card {"gold" if g else ("line" if n == "PayPal" else "")}" style="width:322px;height:330px">{icon("landmark" if n != "PayPal" else "ban", 54, NAVY if g else (MIST if n == "PayPal" else CH), 2)}<div class="ct" style="font-size:36px">{n}</div><div class="cb">{b}</div></div>' for n, b, g in pays)}
</div>
<div class="abs" style="left:110px;top:800px;width:1700px;display:flex;gap:30px">
  {journey('Receiving payment in Nigeria from abroad has been very difficult. I\'ve used Payoneer, then Grey, and for the past two years <b>Cleva</b>.', 'width:1000px')}
  <div class="cb" style="width:670px;font-size:23px">US clients pay differently from Canadian ones. Ask people near you who already earn online. Fees change: check inside the app. (October 2026)</div>
</div>""")
    return [op, f1, f2, f3, f4, f5, f6]


def row11():
    op = opener(11, "Grow through", "People", "Your biggest clients come through trust: results you can show, and people who know you.",
                "You can't do video editing alone.")
    f1 = frame("11.1", "Grow through people · Results and testimonials", f"""
{title('Clients love people', 'who have done it before.', 104)}
<div class="abs" style="left:110px;top:420px;width:860px">
  {''.join(rv(f'<div class="card" style="flex-direction:row;align-items:center;gap:22px;padding:20px 26px;margin-bottom:14px"><div class="num" style="font-size:50px;width:40px">{k+1}</div>{icon(i, 44)}<div class="ct" style="font-size:28px">{t}</div></div>', f'Step {k+1}') for k, (i, t) in enumerate([('chart-column', 'Document the result for every client'), ('camera', 'Keep screenshots of those results'), ('book-open', 'Turn them into case studies'), ('message-square-text', 'Ask for a testimonial: written, or video (very powerful)')]))}
  {doit('Ask one past client, or anyone you have edited for, for a testimonial this week.', 'margin-top:10px')}
</div>
<div class="abs" style="left:1040px;top:330px;width:770px;display:flex;flex-direction:column;gap:18px">
  {ph("Screenshot: views on your mentor's channel", 'height:330px', src('mentorviews'), 'contain')}
  <div class="cb">Not much for YouTube, but it really helped: it went into my portfolio and case studies, <b>even though the work was free.</b></div>
  {ph('Screenshot: a client testimonial', 'height:170px', src('testimonial'), 'contain')}
</div>""")

    import math
    nodes = ""
    for k in range(8):
        a = k * math.pi / 4
        x, y = 470 + 330 * math.cos(a), 330 + 240 * math.sin(a)
        nodes += f'<line x1="470" y1="330" x2="{x:.0f}" y2="{y:.0f}" stroke="{SLATE}" stroke-width="6"/>'
        nodes += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="52" fill="{SLATE}"/>'
    for k in range(8):
        a = k * math.pi / 4
        b2 = (k + 1) * math.pi / 4
        x1, y1 = 470 + 330 * math.cos(a), 330 + 240 * math.sin(a)
        x2, y2 = 470 + 330 * math.cos(b2), 330 + 240 * math.sin(b2)
        if k % 2 == 0:
            nodes += f'<path d="M{x1:.0f} {y1:.0f} Q470 330 {x2:.0f} {y2:.0f}" fill="none" stroke="{CH}" stroke-width="3" stroke-dasharray="10 10"/>'
    nodes += f'<circle cx="470" cy="330" r="86" fill="{CH}"/>'
    icons = "".join(f'<div class="abs" style="left:{470 + 330*math.cos(k*math.pi/4) - 28:.0f}px;top:{330 + 240*math.sin(k*math.pi/4) - 28:.0f}px">{icon("clapperboard", 56)}</div>' for k in range(8))
    f2 = frame("11.2", "Grow through people · Network with other editors", f"""
{title('Social media is meant', 'to be social.', 110)}
<div class="abs" style="left:110px;top:380px;width:940px;height:660px">{svg(nodes, 'position:absolute;left:0;top:0', 940, 660)}{icons}
  <div class="abs" style="left:420px;top:285px">{icon('user', 100, NAVY, 2)}</div>
  <div class="abs" style="left:350px;top:440px;width:240px;text-align:center"><div class="ct" style="font-size:26px">You</div></div>
</div>
<div class="abs" style="left:1100px;top:120px;width:710px;display:flex;flex-direction:column;gap:12px">
  {journey('On Twitter I commented, liked and talked with other editors. I joined their challenges, like <b>&ldquo;10 days to get my first client&rdquo;</b>, and cheered them on. In DMs we corrected each other\'s edits. Some became friends who sent me client projects.')}
  {rv(f'<div class="card gold" style="flex-direction:row;align-items:center;gap:24px"><div class="num" style="font-size:64px;color:{NAVY};white-space:nowrap">2 in 3</div><div class="cb">freelancers get their work through referrals and reputation. (Fiverr survey, 2024)</div></div>', 'How freelancers get work')}
  <div class="li" style="font-size:24px">{icon('users-round', 40)}<span><b>Who:</b> editors at your level or smaller. <b>Where:</b> LinkedIn and Twitter; Instagram works too.</span></div>
  <div class="li" style="font-size:24px">{icon('graduation-cap', 40)}<span><b>Join a serious community.</b> Mine was VP Plus, a paid one. I met some of the best editors there and got one or two clients.</span></div>
  {remember('The real people who will give you opportunities are people who know you.')}
</div>""")
    return [op, f1, f2]


def row12():
    op = opener(12, "Your next", "Steps", "Tonight changes nothing until you act on it. Here is everything to do, in order.", "Let us get into it.")
    hw = [("Write your offer: service, who, which videos, your one sentence", 4), ("Make your learning list; learn the first skill on one practice video", 6),
          ("Finish three full videos in your niche", 7), ("Curate your feed; lock in on your niche for a month", 8), ("Fix your profile (7 points); build a simple portfolio site", 8),
          ("Post 2-3 times a day: 40% authentic, 40% authority, 20% sales", 8), ("Do one warm outreach", 9), ("Start your dream client list: 20 to 50 names", 9),
          ("Write your rate card", 10), ("Ask a past client for a testimonial", 11), ("Start engaging editors at your level", 11)]
    f1 = frame("12.1", "Next steps · Your homework", f"""
<div class="abs" style="left:110px;top:150px;width:1700px">
  <div class="tl">Tick them off in order.</div><div class="bw" style="font-size:100px">Your homework.</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px 40px;margin-top:30px">
  {''.join(f'<div class="card" style="flex-direction:row;align-items:center;gap:18px;padding:16px 22px"><div style="width:38px;height:38px;border:3px solid {CH};border-radius:8px;flex:none"></div><div class="ct" style="font-size:24px;flex:1">{t}</div><div class="tag line" style="font-size:15px">Ch {c}</div></div>' for t, c in hw)}
  </div>
</div>""")

    figs = [("3", "full videos in your niche before you charge"), ("4–5", "free projects for one person, then move to paid"), ("2–3", "posts a day: 40 / 40 / 20"),
            ("8", "videos at most in your portfolio"), ("20–50", "names on your dream client list"), ("1K–20K", "followers: the Instagram creators to target"),
            ("4–5", "posts you comment on before you DM"), ("30s", "the longest a value-first edit should be"), ("4", "follow-ups at most: 24 h, 2 days, 1 week"),
            ("30%", "upfront, with a signed contract"), ("1–3", "months of consistency before clients come")]
    f2 = frame("12.2", "Next steps · Everything to remember, in figures", f"""
<div class="abs" style="left:110px;top:150px;width:1700px">
  <div class="h">Everything to remember, in figures</div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:26px">
  {''.join(f'<div class="card" style="padding:22px 24px;gap:6px;height:186px"><div class="num" style="font-size:66px">{n}</div><div class="cb" style="font-size:21px">{t}</div></div>' for n, t in figs)}
  <div class="card gold" style="padding:22px 24px;justify-content:center;height:186px"><div class="ct" style="font-size:28px">Be patient.</div></div>
  </div>
</div>""")

    lines = ["A diamond is as valuable as it is visible.", "You learn the skill. You sell the service.", "If you are targeting everyone, you have no one.",
             "Don't learn without implementation.", "Your practice work is your work.", "They want to see experience. They don't see knowledge."]
    f3 = frame("12.3", "Next steps · Lines to keep", f"""
<div class="abs" style="left:110px;top:170px;width:1700px;display:grid;grid-template-columns:1fr 1fr;gap:30px 60px">
  {''.join(f'<div style="display:flex;gap:20px;align-items:flex-start">{mark(30)}<div class="qt" style="font-size:58px">{t}</div></div>' for t in lines)}
</div>""")

    perks = [("message-square-text", "Feedback from me on your work, your outreach and your profile"), ("video", "Calls with me inside the community"),
             ("flag", "The 60-day challenge: activities that take you through all of this, with me guiding and correcting you"), ("users-round", "Editors at your level, building alongside you")]
    f4 = (f'<section class="frame" data-id="12.4" style="padding:0">'
          f'<img src="kit/called-to-edit-community-dark.svg" class="abs" style="left:110px;top:90px;width:300px">'
          f'<div class="abs" style="left:110px;top:400px;width:900px"><div class="tl" style="font-size:44px">You don\'t have to do this alone.</div>'
          f'<div class="bw" style="font-size:88px;margin-top:8px">Build it with editors who are building too.</div>'
          f'<div class="sub" style="margin-top:24px">When you start putting this into practice, you\'ll have questions. You\'ll want feedback on your emails, your outreach, your profile and your niche.</div></div>'
          f'<div class="abs" style="left:1080px;top:150px;width:730px;display:flex;flex-direction:column;gap:16px">'
          + "".join(rv(f'<div class="card" style="flex-direction:row;align-items:center;gap:20px;padding:20px 24px">{icon(i, 46)}<div class="ct" style="font-size:25px">{t}</div></div>', 'Inside…') for i, t in perks)
          + rv(f'<div class="card gold" style="flex-direction:row;align-items:center;justify-content:space-between;padding:24px 30px"><div><div class="num" style="font-size:80px;color:{NAVY}">NGN 5,000</div><div class="cb">a month · about USD 4 · any editor, anywhere</div></div>{icon("arrow-right", 70, NAVY, 2.4)}</div>', 'The price')
          + f'<div class="cb" style="font-size:22px">Called to Edit Academy, the full cohort: <b>coming soon.</b></div></div>'
          f'<div class="fid">12.4</div></section>')

    f5 = (f'<section class="frame" data-id="12.5" style="padding:0">'
          f'<img src="kit/called-to-edit-logo-dark.svg" class="abs" style="left:110px;top:90px;width:220px">'
          f'<div class="abs" style="left:110px;top:360px"><div class="tl" style="font-size:60px">Your turn.</div><div class="bw" style="font-size:260px">Questions</div></div>'
          f'<div class="abs" style="left:110px;bottom:100px;display:flex;align-items:center;gap:20px">{icon("instagram", 60)}<div class="ct" style="font-size:44px">@SamuelSignals</div></div>'
          f'<img src="kit/samuel-cutout.webp" class="abs" style="right:40px;bottom:0;height:900px">'
          f'<div class="fid">12.5</div></section>')
    return [op, f1, f2, f3, f4, f5]


ROWS = [("row10-price", row10), ("row11-people", row11), ("row12-close", row12)]
