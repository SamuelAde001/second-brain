"""Rows 0-3: opening, Chapter 1 (story), Chapter 2 (market), Chapter 3 (service)."""
from lib import *

P = {}  # photo sources by slot key, filled in build.py


def src(k):
    return P.get(k)


def row0():
    f1 = (f'<section class="frame" data-id="0.1" style="padding:0">'
          f'<img src="kit/called-to-edit-logo-dark.svg" class="abs" style="left:110px;top:90px;width:260px">'
          f'<div class="abs" style="left:110px;top:330px;width:1150px">'
          f'<div class="tag gold">{mark(14, NAVY)} Live webinar · Fri 23 Oct 2026 · 7pm WAT</div>'
          f'<div class="tl" style="font-size:60px;margin-top:44px">How to build a career as a</div>'
          f'<div class="bw" style="font-size:200px;margin-top:6px">Video Editor</div>'
          f'<div class="tl" style="font-size:60px;margin-top:18px">and get paid.</div>'
          f'<div class="sub" style="margin-top:44px">From your first lesson to your first paying client, and every step between.</div></div>'
          f'<div class="abs" style="right:0;bottom:0;width:820px;height:1080px;background:radial-gradient(closest-side at 60% 55%, #1E3150, rgba(10,31,68,0))"></div>'
          f'<img src="kit/samuel-cutout.webp" class="abs" style="right:40px;bottom:0;height:1000px">'
          f'<div class="abs" style="left:110px;bottom:84px;font:700 28px \'Plus Jakarta Sans\'">Samuel Adebayo <span style="color:{MIST};font-weight:500">· Video editor and coach · Founder, Called to Edit</span></div>'
          f'<div class="fid">0.1</div></section>')

    f2 = frame("0.2", "Start here", f"""
<div class="abs" style="left:110px;top:170px;width:1700px">
  <div class="tl" style="font-size:64px">There are millions of video editors.</div>
  <div class="bw" style="font-size:190px;margin-top:10px">Why you?</div>
</div>
<div class="abs" style="left:110px;top:560px;width:800px">
  <div class="card" style="height:400px;justify-content:center">
    {icon('scissors', 60)}
    <div class="qt" style="font-size:46px">&ldquo;Editing is cutting out what is not needed from the raw idea and presenting it in a way the viewer can get it.&rdquo;</div>
    <div class="cb">My definition of video editing</div>
  </div>
</div>
<div class="abs" style="left:960px;top:560px;width:850px" class="col">
  <div class="card line" style="height:180px;flex-direction:row;align-items:center;gap:26px">{icon('circle-x', 64, MIST)}
    <div><div class="ct" style="color:{MIST}">Not a tutorial</div><div class="cb">The buttons are free on YouTube. I learned 80 to 90% of my editing there.</div></div></div>
  {rv(f'''<div class="card gold" style="height:196px;margin-top:24px;flex-direction:row;align-items:center;gap:26px">{icon('route', 64, NAVY, 2.2)}
    <div><div class="ct">Tonight: the career around the skill</div><div class="cb">What to learn first · how to get seen · how to get clients · how to get paid</div></div></div>''', 'What tonight IS')}
</div>""")

    stops = [("1", "My story"), ("2", "The market"), ("3", "Editing is a service"), ("4", "Choose your niche"),
             ("5", "Tools & money"), ("6", "Learn the skill"), ("7", "Practice to paid"), ("8", "Get seen"),
             ("9", "Get clients"), ("10", "Price & get paid"), ("11", "Grow through people"), ("12", "Next steps")]
    bright = {"6", "7", "8", "9", "10"}
    pts = [(230, 440), (520, 380), (810, 440), (1100, 380), (1390, 440), (1680, 380),
           (1680, 760), (1390, 820), (1100, 760), (810, 820), (520, 760), (230, 820)]
    path = "M" + " L".join(f"{x} {y}" for x, y in pts[:6]) + f" C1900 420 1900 640 {pts[6][0]} {pts[6][1]} L" + " L".join(f"{x} {y}" for x, y in pts[6:])
    dots = ""
    for (n, t), (x, y) in zip(stops, pts):
        b = n in bright
        fill = CH if b else SLATE
        tc = NAVY if b else "#fff"
        dots += f'<circle cx="{x}" cy="{y}" r="46" fill="{fill}" stroke="{NAVY}" stroke-width="8"/>'
        dots += f'<text x="{x}" y="{y+15}" text-anchor="middle" font-family="Gloock" font-size="44" fill="{tc}">{n}</text>'
    labels = "".join(
        f'<div class="abs" style="left:{x-140}px;top:{y + (64 if i % 2 == 0 else -120) if i < 6 else y + (64 if i % 2 == 1 else -120)}px;width:280px;text-align:center;font:700 25px/1.2 \'Plus Jakarta Sans\';color:{"#FCDD9E" if n in bright else "#fff"}">{t}</div>'
        for i, ((n, t), (x, y)) in enumerate(zip(stops, pts)))
    f3 = frame("0.3", "Tonight's pathway", f"""
<div class="abs" style="left:110px;top:130px"><div class="h">Each step decides the next.</div></div>
{svg(f'<path d="{path}" fill="none" stroke="{SLATE}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>' + dots)}
{labels}
<div class="abs" style="left:110px;bottom:84px;display:flex;align-items:center;gap:14px;font:600 26px 'Plus Jakarta Sans';color:{MIST}">
  <svg width="28" height="28"><circle cx="14" cy="14" r="12" fill="{CH}"/></svg> Bright stops are where most of the work is: learning, getting clients and getting paid.</div>""")
    return [f1, f2, f3]


def row1():
    op = opener(1, "My story", "Soldier to editor", "From a soldier with a hobby to an editor paid by clients abroad, working from Abuja.",
                "People watch what you do. People watch what you post.")

    f1 = frame("1.1", "My story · It started as a hobby", f"""
{title('2020, COVID.', 'Still a soldier.', 100)}
<div class="abs" style="left:110px;top:430px;width:1700px;display:flex;gap:34px;align-items:flex-start">
  <div class="col" style="width:380px">{ph('Photo: you in uniform, 2020', 'height:440px', src('uniform'))}<div class="ct" style="font-size:28px">A soldier, learning to edit for myself</div></div>
  <div class="col" style="width:380px">{ph('Screenshot: your Minecraft YouTube channel', 'height:440px', src('minecraft'), 'contain')}<div class="ct" style="font-size:28px">My Minecraft YouTube channel</div></div>
  <div class="col" style="width:380px"><div class="card" style="height:440px;align-items:center;justify-content:center;text-align:center">{icon('laptop', 90)}<div class="ct">A laptop + free software</div><div class="cb">So I found <b>DaVinci Resolve</b></div></div><div class="ct" style="font-size:28px">Later: editing for my church</div></div>
  <div class="col" style="width:400px;padding-top:20px">{quote("If I had known CapCut then, I might have started there. I'm glad I started with Resolve.", 44)}</div>
</div>
{svg(arrow(498, 650, 524, 650, w=6) + arrow(912, 650, 938, 650, w=6) + arrow(1326, 650, 1352, 650, w=6))}
""")

    f2 = frame("1.2", "My story · The best move I made", f"""
{title('A few years later I asked myself:', 'What can I do better than just being a soldier?', 76)}
<div class="abs" style="left:110px;top:430px;width:560px" class="col">
  <div class="card" style="gap:18px">{icon('handshake', 60)}<div class="ct">I offered to edit my mentor's YouTube videos. For free.</div>
  <div class="cb">I only knew how to cut. My laptop cost a whole month's salary: decent, but laggy. It was enough.</div></div>
  <div class="li" style="margin-top:22px">{icon('wallet', 40)}<span>Then <b>NGN 25,000 a month</b> for data and expenses, about 4 videos a month. <b>For two years.</b></span></div>
</div>
<div class="abs" style="left:740px;top:430px;width:1070px">
  <div class="step">{mark(16)} My first three edits for my mentor</div>
  <div class="row" style="margin-top:22px">
    <div class="card" style="width:330px;height:300px">{icon('circle-x', 54, MIST)}<div class="tag line">Edit 1 · Rejected</div><div class="ct">&ldquo;I can't use this.&rdquo;</div></div>
    {rv(f'<div class="card" style="width:330px;height:300px">{icon("refresh-cw", 54)}<div class="tag line">Edit 2 · Not yet</div><div class="ct">Back to YouTube to learn more.</div></div>', 'Edit 2?')}
    {rv(f'<div class="card gold" style="width:330px;height:300px">{icon("circle-check", 54, NAVY, 2.2)}<div class="tag" style="background:{NAVY};color:{CH}">Edit 3 · Uploaded</div><div class="ct">It went live on his channel.</div></div>', 'Edit 3?')}
  </div>
  {remember('I learned from tutorials I watched to deliver a video that was going live, not to practise.', 'margin-top:26px')}
</div>""")

    f3 = frame("1.3", "My story · Putting my work out there", f"""
{title('My mentor said:', 'Put your work out there.', 100)}
<div class="abs" style="left:110px;top:440px;width:900px" class="col">
  <div class="li">{icon('twitter', 44)}<span>I opened a <b>brand-new Twitter account</b>, posted my work and networked with editors on Twitter and LinkedIn.</span></div>
  <div class="li" style="margin-top:22px">{icon('eye', 44)}<span>Seeing their work showed me I had to <b>step up</b>.</span></div>
  <div class="li" style="margin-top:22px">{icon('flame', 44)}<span>I <b>locked in for six months</b>: mastered Resolve and learned the business side.</span></div>
  {rv(f'''<div class="card gold" style="margin-top:30px;flex-direction:row;align-items:center;gap:24px">{icon("users-round", 60, NAVY, 2.2)}<div><div class="ct">USD 60 out of my salary</div><div class="cb">to join a community that taught the <b style="color:{NAVY}">business</b> of editing, not just the skill.</div></div></div>''', 'What I paid for')}
</div>
<div class="abs" style="left:1180px;top:330px;width:630px;display:flex;flex-direction:column;gap:24px">
  {ph('Screenshot: one of your first editing tweets', 'height:310px', src('tweet1'), 'contain')}
  {ph('Screenshot: your timeline / work-in-progress post', 'height:310px', src('tweet2'), 'contain')}
</div>""")

    f4 = frame("1.4", "My story · The first dollar", f"""
{title('My first client came to me by DM.', 'He had been watching my posts.', 84)}
<div class="abs" style="left:110px;top:450px;width:1000px">
  <div class="row" style="align-items:flex-end;gap:40px;height:330px">
    {''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:14px"><div class="num" style="font-size:{s}px">${v}</div><div style="width:200px;height:{h}px;background:{c};border-radius:18px 18px 0 0"></div><div class="cb" style="font-size:22px">per short-form video</div></div>' for v, s, h, c in [(20, 80, 70, SLATE), (30, 92, 110, SLATE), (60, 110, 180, CH)])}
  </div>
  <div class="li" style="margin-top:34px">{icon('coins', 40)}<span>My first dollar payment. <b>I didn't even know how to turn dollars into naira.</b></span></div>
</div>
<div class="abs" style="left:1180px;top:300px;width:630px;display:flex;flex-direction:column;gap:24px">
  {ph('Screenshot: the DM from your first client', 'height:440px', src('firstdm'), 'contain')}
  <div class="card" style="flex-direction:row;align-items:center;gap:22px">{icon('sun', 52)}{icon('moon', 52)}<div class="ct" style="font-size:30px">Days in the military. Nights editing.</div></div>
</div>""")

    bars = [("First client", 20), ("Raised", 30), ("Then", 60), ("Agency", 250)]
    bh = "".join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px;width:180px"><div class="num" style="font-size:{56 if v < 250 else 84}px">${v}</div>'
        f'<div style="width:150px;height:{v * 1.5 + 20}px;background:{CH if v == 250 else SLATE};border-radius:16px 16px 0 0"></div><div class="cb" style="font-size:22px;text-align:center">{t}</div></div>'
        for t, v in bars)
    f5 = frame("1.5", "My story · Going full time", f"""
{title('Then I quit the military.', 'The riskiest thing I have done.', 84)}
<div class="abs" style="left:110px;top:400px;width:760px" class="col">
  <div class="row" style="gap:22px">
    <div class="card" style="width:360px">{icon('calendar', 48)}<div class="cb">First month</div><div class="num" style="font-size:96px">$600</div></div>
    {rv(f'<div class="card" style="width:360px">{icon("trending-up", 48)}<div class="cb">Second month</div><div class="num" style="font-size:96px">~$1,000</div></div>', 'Month 2?')}
  </div>
  <div class="li" style="margin-top:28px">{icon('triangle-alert', 42)}<span>I took <b>three clients at once</b> and nearly burnt out. <b>More clients does not mean you are better.</b></span></div>
  <div class="li" style="margin-top:18px">{icon('eye', 42)}<span>I kept posting. <b>Route Rise reached out</b> because they had been watching my work: a YouTube channel with <b>1 million subscribers</b>, a <b>billion-dollar company</b>.</span></div>
</div>
<div class="abs" style="left:940px;top:400px;width:870px">
  <div class="step">{mark(16)} Per video, in US dollars</div>
  <div class="row" style="align-items:flex-end;gap:24px;height:470px;margin-top:10px">{bh}</div>
  {rv(f'<div class="rem" style="margin-top:20px"><div class="rt">The jump came from better clients, not more clients.</div></div>', 'Why the jump?')}
</div>""")

    f6 = frame("1.6", "My story · What it taught me", f"""
<div class="abs" style="left:110px;top:170px;width:1080px">
  <div class="tl" style="font-size:44px">About 4 to 5 years in. Lots of mistakes, trial and error.</div>
  {quote('I wish I had known two years earlier what I know now.', 76, 'margin-top:30px')}
  <div class="row" style="margin-top:56px;gap:24px">
    <div class="card" style="width:520px">{icon('youtube', 54)}<div class="ct">Learning from YouTube</div></div>
    <div class="card" style="width:520px">{icon('megaphone', 54)}<div class="ct">Posting my work</div></div>
  </div>
  <div class="cb" style="margin-top:16px">Two things ran under everything. Every jump in pay came from real work or from being seen.</div>
</div>
<div class="abs" style="left:1260px;top:170px;width:550px;display:flex;flex-direction:column;gap:24px">
  {rv(remember('The skill gets you in. How you present it is why you get hired.'), 'The lesson')}
  <div class="card line">{icon('message-circle', 46)}<div class="cb"><b>Video editing is not just a skill.</b> It is a way of passing information and communicating.</div></div>
  <div class="card line">{icon('sparkles', 46)}<div class="cb">A lot of people put effects in a video <b>without understanding what purpose they serve.</b></div></div>
</div>""")
    return [op, f1, f2, f3, f4, f5, f6]


def row2():
    op = opener(2, "The truth about the", "Market", "There is huge demand for editors. Most beginners never earn because nobody who pays can find them.",
                "A diamond is as valuable as it is visible.")
    stats = [("5.66B", "social media accounts in the world, about 7 in 10 people", "DataReportal · Oct 2025", "globe"),
             ("200B", "YouTube Shorts views every single day", "YouTube · Jun 2025", "youtube"),
             ("3B", "people use Instagram every month", "Meta · Sep 2025", "instagram"),
             ("500+", "hours of video uploaded to YouTube every minute", "YouTube · 2019", "upload"),
             ("50M", "creators. Only about 4% earn over USD 100,000 a year", "Goldman Sachs · 2023", "users")]
    tiles = "".join(
        f'<div class="card" style="width:316px;height:420px">{icon(ic, 50)}{rv(f"<div class=num style=font-size:96px>{n}</div>", "?")}<div class="cb" style="color:#fff;font-weight:600">{t}</div><div class="cb" style="font-size:19px;margin-top:auto">{s}</div></div>'
        for n, t, s, ic in stats)
    f1 = frame("2.1", "The market · Demand", f"""
{title('Every brand, creator and business', 'now needs video.', 110)}
<div class="abs" style="left:110px;top:440px;width:1700px" ><div class="row" style="gap:30px">{tiles}</div></div>
<div class="abs" style="left:110px;bottom:84px;width:1500px" class="sub"><div class="sub">You can't run a proper business today without putting something out there. They are busy. <b>They will pay someone to edit.</b> Someone has to cut all that video.</div></div>""")

    types = [("gamepad-2", "Entertainment", "Skits, gaming, dance", "Plenty of them. They live on views and brand deals.", "Pays least", SLATE),
             ("graduation-cap", "Educative", "Teaching and explainers", "Most are business people, teaching you toward a product.", "Pays well", SLATE),
             ("briefcase", "Business", "Founders, brands, companies", "Post a lot, find it tedious, already understand marketing.", "Pays the most", CH)]
    cols = "".join(
        f'<div class="card {"gold" if c == CH else ""}" style="width:530px;height:520px">{icon(ic, 72, NAVY if c == CH else CH, 2)}<div class="ct" style="font-size:44px">{h}</div><div class="cb"><b style="color:{NAVY if c == CH else "#fff"}">{s}</b></div><div class="cb">{b}</div>'
        + rv(f'<div class="tag {"line" if c != CH else ""}" style="{"background:" + NAVY + ";color:" + CH if c == CH else ""};font-size:24px;padding:12px 24px">{p}</div>', 'Pays?', 'margin-top:auto;align-self:flex-start') + '</div>'
        for ic, h, s, b, p, c in types)
    f2 = frame("2.2", "The market · Who pays editors", f"""
{title('There are three kinds of creators,', "and they don't pay the same.", 100)}
<div class="abs" style="left:110px;top:430px"><div class="row" style="gap:55px">{cols}</div></div>""")

    ag = ""
    for k in range(5):
        ag += f'<g transform="translate(330 {300 + k*90})">' + f'<circle r="34" fill="{SLATE}"/></g>'
    f3 = frame("2.3", "The market · Who pays you", f"""
{title('Creators, businesses', 'and agencies.', 110)}
<div class="abs" style="left:110px;top:430px;width:820px;height:520px">
  <div class="card line" style="height:520px;padding:30px">
    <div class="step">{mark(16)} An agency is a middleman</div>
    <div class="row" style="margin-top:34px;align-items:center;gap:30px">
      <div class="col" style="gap:14px;align-items:center">{''.join(icon('user', 46, MIST) for _ in range(4))}<div class="cb" style="font-size:20px">20-30 clients</div></div>
      {svg(arrow(0, 40, 90, 40, w=5), 'position:relative', 100, 80)}
      <div class="card gold" style="width:220px;align-items:center;text-align:center">{icon('building-2', 70, NAVY, 2)}<div class="ct">Agency</div><div class="cb">takes a cut</div></div>
      {svg(arrow(0, 40, 90, 40, w=5), 'position:relative', 100, 80)}
      <div class="col" style="gap:14px;align-items:center">{''.join(icon('clapperboard', 46, CH) for _ in range(4))}<div class="cb" style="font-size:20px">many editors</div></div>
    </div>
  </div>
</div>
<div class="abs" style="left:990px;top:430px;width:820px;display:flex;flex-direction:column;gap:22px">
  <div class="card"><div class="row" style="align-items:center;gap:16px">{icon('building-2', 50)}<div class="ct">Agencies</div><div class="tag line">Good for beginners</div></div>
  <div class="cb">Always have work, and clients you could never reach yourself. They really helped my career. <b>But</b> they pay less, and give the worst feedback and many revisions.</div></div>
  {rv(f'''<div class="card gold"><div class="row" style="align-items:center;gap:16px">{icon("handshake", 50, NAVY, 2)}<div class="ct">Creators &amp; businesses, directly</div><div class="tag" style="background:{NAVY};color:{CH}">The best</div></div>
  <div class="cb">The best pay and the best working relationship. You have to find them and earn their trust. That's what tonight is about.</div></div>''', 'The best clients')}
  <div class="cb" style="font-size:24px">Big brands and big creators go to agencies. <b>The ones who can't afford an agency are where you start.</b></div>
</div>""")

    eds = "".join(f'<g transform="translate({1080 + k*150} 690)"><circle r="62" fill="{SLATE}"/></g>' for k in range(5))
    f4 = frame("2.4", "The market · \"But the market is full\"", f"""
{title('"But the market is full."', 'No, it isn’t.', 130)}
<div class="abs" style="left:110px;top:450px;width:820px" class="col">
  <div class="sub">Some creators have <b>three, four, five video editors</b>. The problem is most of us are not good enough yet, and <b>we don't position ourselves</b> so the people who need us can find us.</div>
  {rv(f'<div class="card gold" style="margin-top:34px"><div class="ct">The biggest beginner mistake</div><div class="cb">Learning a lot of skill and never positioning yourself. Random things in a portfolio, applying for jobs, no social media.</div></div>', 'Biggest mistake?')}
  {journey('My own biggest mistake was not putting myself out there.', 'margin-top:24px')}
</div>
<div class="abs" style="left:1000px;top:450px;width:810px;height:500px">
  <div class="abs" style="left:300px;top:0;width:210px;display:flex;flex-direction:column;align-items:center;gap:10px">{icon('user-round-check', 120)}<div class="ct" style="font-size:28px">One creator</div></div>
  {svg(''.join(arrow(405, 200, 405 + dx, 300, w=5) for dx in (-330, -165, 0, 165, 330)), 'position:absolute;left:0;top:0', 810, 500)}
  <div class="abs" style="left:0;top:320px;width:810px;display:flex;justify-content:space-between">{''.join('<div style="width:140px;display:flex;flex-direction:column;align-items:center">' + icon('clapperboard', 76) + '</div>' for _ in range(5))}</div>
  <div class="abs" style="left:0;top:430px;width:810px;text-align:center" class="ct"><div class="ct" style="font-size:30px">several editors. <span class="g">Visibility is the gap.</span></div></div>
</div>""")

    f5 = frame("2.5", "The market · AI", f"""
{title('Yes, AI can edit.', 'AI is not taking your place.', 104)}
<div class="abs" style="left:110px;top:460px;width:1700px;display:flex;align-items:center;gap:34px">
  <div class="card" style="width:400px;height:300px;align-items:center;justify-content:center;text-align:center">{icon('scissors', 80)}<div class="ct">Your skill</div></div>
  <div class="num" style="font-size:120px">+</div>
  <div class="card" style="width:400px;height:300px;align-items:center;justify-content:center;text-align:center">{icon('bot', 80)}<div class="ct">AI in your workflow</div></div>
  <div class="num" style="font-size:120px">=</div>
  {rv(f'<div class="card gold" style="width:460px;height:300px;align-items:center;justify-content:center;text-align:center">{icon("zap", 80, NAVY, 2)}<div class="ct" style="font-size:40px">Your leverage</div><div class="cb">deliver faster and more easily</div></div>', '= ?')}
</div>
<div class="abs" style="left:110px;bottom:84px;width:1600px;display:flex;gap:40px">
  <div class="li" style="width:780px">{icon('building', 40)}<span>The company I work with <b>demands that its editors use AI</b>. Creativity is still needed.</span></div>
  <div class="li" style="width:780px">{icon('lightbulb', 40)}<span>What you learn today can be useless tomorrow. <b>Knowing what to learn matters more than ever.</b></span></div>
</div>""")
    return [op, f1, f2, f3, f4, f5]


def row3():
    op = opener(3, "Editing is a", "Service", "You learn a skill, but you sell a service, to a specific person. Everything after this rests on that.",
                "If you are targeting everyone, you have no one.")
    f1 = frame("3.1", "Editing is a service · Skill vs service", f"""
{title('Business is an exchange of value for money.', 'Literally.', 120)}
<div class="abs" style="left:110px;top:440px;width:620px;height:480px">
  <div class="abs" style="left:0;top:40px;width:200px;display:flex;flex-direction:column;align-items:center;gap:10px">{icon('clapperboard', 96)}<div class="ct" style="font-size:28px">You</div></div>
  <div class="abs" style="left:420px;top:40px;width:200px;display:flex;flex-direction:column;align-items:center;gap:10px">{icon('user-round-check', 96)}<div class="ct" style="font-size:28px">Client</div></div>
  {svg(arrow(200, 70, 410, 70, w=6) + arrow(410, 190, 200, 190, w=6), 'position:absolute;left:0;top:0', 620, 480)}
  <div class="abs" style="left:230px;top:10px;width:160px;text-align:center" class="cb"><div class="cb" style="font-size:22px">I edit your videos</div></div>
  <div class="abs" style="left:230px;top:200px;width:160px;text-align:center"><div class="cb" style="font-size:22px">you give me cash</div></div>
  <div class="abs" style="left:0;top:330px;width:620px"><div class="cb">This is where most editors get stuck. <b>Talented editors miss this all the time</b>: they focus on the skill, not on how to serve the client.</div></div>
</div>
<div class="abs" style="left:800px;top:440px;width:1010px;display:flex;gap:28px">
  <div class="card line" style="width:490px;height:440px">{icon('scissors', 60, MIST)}<div class="tag line">A skill</div><div class="ct" style="font-size:40px">&ldquo;I can edit videos.&rdquo;</div><div class="cb">True of millions of people. Nobody knows what to buy from you.</div></div>
  {rv(f'<div class="card gold" style="width:490px;height:440px">{icon("target", 60, NAVY, 2)}<div class="tag" style="background:{NAVY};color:{CH}">A service</div><div class="ct" style="font-size:36px">&ldquo;I edit YouTube videos for business creators so they get more views.&rdquo;</div><div class="cb">A specific person knows you are for them.</div></div>', 'A service sounds like…')}
</div>""")

    flags = "".join(f'<div class="tag line" style="font-size:22px">{c}</div>' for c in ["Japan", "China", "Nigeria", "Brazil", "…"])
    f2 = frame("3.2", "Editing is a service · Not everyone is your client", f"""
{title('Think about a clothing business.', 'Not everyone is your client.', 100)}
<div class="abs" style="left:110px;top:440px;width:1700px;display:flex;gap:40px">
  <div class="card line" style="width:820px;height:400px">{icon('shirt', 70, MIST)}<div class="ct">Trying to dress everyone</div><div class="row" style="gap:12px;flex-wrap:wrap">{flags}</div>
    <div class="cb">Different styles, sizes, tastes. <b>Nobody feels it was made for them.</b></div></div>
  {rv(f'<div class="card gold" style="width:820px;height:400px">{icon("shirt", 70, NAVY, 2)}<div class="ct">Picking one group</div><div class="ct" style="font-size:44px">&ldquo;I sew clothes for Nigerians.&rdquo;</div><div class="cb">Now every choice is easy: the fabric, the cut, the price, the advert.</div></div>', 'Pick one group')}
</div>
<div class="abs" style="left:110px;bottom:80px;width:1700px;display:flex;gap:40px;align-items:center">
  <div class="sub" style="width:1100px">Your target audience decides <b>how you pitch</b> and <b>what you learn</b>. Serve everyone and you end up like every other editor.</div>
  <div class="qt" style="font-size:52px">Be specialised, not generalised.</div>
</div>""")

    f3 = frame("3.3", "Editing is a service · Work backwards", f"""
{title("Don't start with the skill.", 'Work backwards.', 120)}
<div class="abs" style="left:110px;top:430px;width:1700px;height:300px">
  <div class="card abs" style="left:0;top:0;width:430px;height:130px;flex-direction:row;align-items:center;gap:20px">{icon('smartphone', 56)}<div><div class="ct" style="font-size:30px">The tools you have</div><div class="cb" style="font-size:22px">phone, computer, CapCut</div></div></div>
  <div class="card abs" style="left:0;top:170px;width:430px;height:130px;flex-direction:row;align-items:center;gap:20px">{icon('users', 56)}<div><div class="ct" style="font-size:30px">Who you want to serve</div><div class="cb" style="font-size:22px">YouTubers, IG creators, realtors</div></div></div>
  {svg(arrow(450, 65, 600, 140, w=6) + arrow(450, 235, 600, 160, w=6) + arrow(1050, 150, 1180, 150, w=6), 'position:absolute;left:0;top:0', 1700, 300)}
  <div class="card abs" style="left:620px;top:60px;width:420px;height:180px;align-items:center;justify-content:center;text-align:center">{icon('graduation-cap', 56)}<div class="ct" style="font-size:30px">What you go and learn</div></div>
  {rv(f'<div class="card gold" style="width:500px;height:180px;align-items:center;justify-content:center;text-align:center">{icon("package", 56, NAVY, 2)}<div class="ct" style="font-size:30px">Package it as a service for that person</div></div>', 'Then…', 'position:absolute;left:1200px;top:60px')}
</div>
<div class="abs" style="left:110px;top:790px;width:1700px;display:flex;gap:34px">
  {journey("I wanted to be a motion designer. My laptop was very bad and I didn't have money for a better one. So I chose what my tools could do, and that is what got me paid.", 'width:1000px')}
  {remember("Video editing is not just a skill, it's a service.", 'width:660px')}
</div>""")
    return [op, f1, f2, f3]


ROWS = [("row00-opening", row0), ("row01-story", row1), ("row02-market", row2), ("row03-service", row3)]
