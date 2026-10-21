"""Rows 4-7: niche, tools and money, learning, practice to paid."""
from lib import *

P = {}


def src(k):
    return P.get(k)


def row4():
    op = opener(4, "Choose your", "Niche", "Pick a niche you enjoy, one that makes money and values marketing. Then say it in one sentence.",
                "In any niche, business people pay more.")
    tiers = [("rocket", "SaaS, software and AI companies", "Those people have money. They can pay you a lot.", "Top", 1100),
             ("building", "Real estate, marketers, logistics, solar, service businesses, personal brands", "Businesses that sell a service know what a good video brings them.", "Very good", 1280),
             ("graduation-cap", "Educative creators", "Most are business people teaching you toward a product.", "Good", 1460),
             ("gamepad-2", "Entertainment, gaming, skits, dance", "Mostly broke. By the time they hit ~1M views and can pay, they already have a good editor.", "Lowest", 1640)]
    tr = ""
    for k, (ic, h, b, p, w) in enumerate(tiers):
        gold = k == 0
        inner = (f'<div class="card {"gold" if gold else ""}" style="width:{w}px;height:136px;flex-direction:row;align-items:center;gap:24px;padding:22px 30px">'
                 f'{icon(ic, 54, NAVY if gold else CH, 2)}<div style="flex:1"><div class="ct" style="font-size:29px">{h}</div><div class="cb" style="font-size:22px">{b}</div></div>'
                 f'<div class="pay" style="color:{NAVY if gold else CH}">{p}</div></div>')
        tr += rv(inner, f"Tier {k + 1}?", f"margin:0 auto {14}px auto;width:{w}px")
    f1 = frame("4.1", "Choose your niche · Who pays: my ranking", f"""
{title('Who pays?', 'My ranking.', 110)}
<div class="abs" style="left:110px;top:390px;width:1700px">{tr}</div>""")

    f2 = frame("4.2", "Choose your niche · The follower trap", f"""
{title('Followers are not money.', 'Ask what they sell.', 110)}
<div class="abs" style="left:110px;top:440px;width:1700px;display:flex;gap:40px">
  <div class="card gold" style="width:520px;height:440px">{icon('briefcase', 64, NAVY, 2)}<div class="ct">Business creator</div><div class="num" style="font-size:130px;color:{NAVY}">10K</div><div class="cb">followers</div>
    {rv(f'<div class="ct" style="font-size:28px">Can make USD 100,000 a month, because he markets to them.</div>', 'Earns…')}</div>
  <div class="card" style="width:520px;height:440px">{icon('gamepad-2', 64)}<div class="ct">Entertainer</div><div class="num" style="font-size:130px">100K</div><div class="cb">followers</div>
    {rv(f'<div class="ct" style="font-size:28px">May not afford USD 500, or even USD 100, per video.</div>', 'Earns…')}</div>
  <div class="col" style="width:580px;gap:22px">
    <div class="step">{mark(16)} Two more to watch</div>
    <div class="card line"><div class="ct" style="font-size:28px">Corporate companies</div><div class="cb" style="font-size:21px">Fixed pay like an employee, whatever value you bring, and you can't negotiate. I advise against it. I prefer solo creators and small businesses that make money.</div></div>
    <div class="card line"><div class="ct" style="font-size:28px">Low-ticket sellers</div><div class="cb" style="font-size:21px">Selling something cheap. May not make enough to pay an editor well.</div></div>
  </div>
</div>""")

    rows = [("SaaS, software, AI tools", "High", "product explainers, demos, founder talking heads, ads"),
            ("Personal finance, investing", "High", "talking heads, explainers"),
            ("Business, marketing, coaches", "High", "talking heads, podcasts, course promos · <b class=g>my niche</b>"),
            ("Real estate", "High", "property tours, agent talking heads, ads"),
            ("Ads, in any niche", "High", "the best-paying short form"),
            ("Education, explainers", "Good", "tutorials, documentaries, AI and tech"),
            ("Podcasts", "Depends", "business podcasts pay"),
            ("Vlogs, lifestyle, fitness, beauty", "Depends", "on whether they sell something"),
            ("Events, weddings, church", "Varies", "event recaps suit phone editors"),
            ("Gaming, skits, dance", "Low", "gameplay, highlights, trends")]
    trs = "".join(f'<tr><td style="width:560px">{a}</td><td style="width:200px"><span class="pay" style="color:{CH if b == "High" else MIST}">{b}</span></td><td>{c}</td></tr>' for a, b, c in rows)
    f3 = frame("4.3", "Choose your niche · The niches at a glance", f"""
<div class="abs" style="left:110px;top:150px;width:1700px"><div class="h">The niches at a glance</div>
<table class="tbl" style="margin-top:18px">{trs}</table>
<div class="cb" style="margin-top:8px;font-size:22px">Advertisers pay the most on YouTube for finance, business and software videos, which is why those creators can afford you. (vidIQ)</div></div>""")

    f4 = frame("4.4", "Choose your niche · How to choose", f"""
{title('Four questions.', 'How to choose yours.', 104)}
<div class="abs" style="left:110px;top:430px;width:900px" class="col">
  {''.join(f'<div class="li" style="margin-bottom:22px"><div class="num" style="font-size:54px;width:50px">{n}</div><span>{t}</span></div>' for n, t in [
      (1, '<b>What excites you most, and what do you watch most?</b> I watch a lot of business videos, so I understand how they are edited.'),
      (2, '<b>How much does this niche usually make?</b> Can they afford an editor?'),
      (3, '<b>Do they value marketing?</b> That is why business people are always the best.'),
      (4, '<b>Can your tools handle it?</b> That is the next chapter.')])}
</div>
<div class="abs" style="left:1080px;top:200px;width:730px;display:flex;flex-direction:column;gap:22px">
  <div class="step">{mark(16)} Short form or long form?</div>
  <div class="card"><div class="tag line">Long form</div><div class="num" style="font-size:72px">$500–2,000</div><div class="cb">per video is a price you easily hear. It pays more per video.</div></div>
  <div class="card"><div class="tag line">Short form</div><div class="num" style="font-size:72px">5–10 videos</div><div class="cb">a month in one package. Less per video, so you sell volume.</div></div>
  {rv(remember('Ads are the best-paying short form. An ad is tied directly to the customers a business gets.', head='The best short form'), 'Best-paying short form?')}
</div>""")

    f5 = frame("4.5", "Choose your niche · Your offer", f"""
{title('Stop saying "I\'m a video editor."', 'Say it in one sentence.', 100)}
<div class="abs" style="left:110px;top:430px;width:1700px;display:flex;align-items:flex-end;gap:18px;font:800 46px 'Plus Jakarta Sans'">
  <span>I help</span><span style="border-bottom:5px solid {CH};min-width:250px;text-align:center;color:{CH}">who</span>
  <span>get</span><span style="border-bottom:5px solid {CH};min-width:300px;text-align:center;color:{CH}">what result</span>
  <span>in</span><span style="border-bottom:5px solid {CH};min-width:250px;text-align:center;color:{CH}">how long</span>
  <span>through</span><span style="border-bottom:5px solid {CH};min-width:230px;text-align:center;color:{CH}">how</span><span>.</span>
</div>
<div class="abs" style="left:110px;top:540px;width:1700px" class="cb"><div class="cb" style="font-size:24px"><b>Who:</b> the specific people you help · <b>Result:</b> more views, more sales · <b>How long:</b> a time range · <b>How:</b> video editing, motion design, storytelling. There must be a promise.</div></div>
{rv(f'<div class="card gold" style="width:1000px"><div class="step" style="color:{NAVY}">{mark(16, NAVY)} My example</div><div class="ct" style="font-size:36px">&ldquo;I help business creators get 10,000 views in 3 months through video editing and visually engaging content.&rdquo;</div></div>', 'My example', 'position:absolute;left:110px;top:660px')}
{doit('Write down what service you offer, to whom, which kind of videos, and how you will package and sell it. Then write your offer sentence.', 'position:absolute;left:1160px;top:660px;width:650px')}""")
    return [op, f1, f2, f3, f4, f5]


def row5():
    op = opener(5, "Your tools and the", "Money to start", "Start on what you can afford, never on cracked software, and treat every cost as capital you will earn back.",
                "Whatever you pay for a subscription is your capital.")
    f1 = frame("5.1", "Tools · Phone or laptop", f"""
{title('Your niche and your hardware', 'pick your software.', 100)}
<div class="abs" style="left:110px;top:420px;width:1700px;display:flex;gap:36px">
  <div class="card" style="width:832px;height:540px">
    <div class="row" style="align-items:center;gap:20px">{icon('smartphone', 70)}<div class="ct" style="font-size:42px">On a phone</div></div>
    <div class="row" style="gap:12px;flex-wrap:wrap">{''.join(f'<div class="tag gold" style="font-size:20px">{a}</div>' for a in ['CapCut', 'Premiere Pro mobile', 'Edits'])}</div>
    <div class="cb">Free to start, with paid tiers. Great for short form, captions and simple social videos.</div>
    <div class="row" style="gap:20px;margin-top:10px">
      <div style="flex:1"><div class="step" style="color:{MIST}">Loses on</div>{''.join(f'<div class="li" style="font-size:24px;margin-top:10px">{icon("x", 30, MIST)}<span>{t}</span></div>' for t in ['Long-form YouTube', 'Motion graphics', 'Heavy animation'])}</div>
      {rv(f'<div><div class="step">Wins on</div>' + ''.join(f'<div class="li" style="font-size:24px;margin-top:10px;color:#fff">{icon("check", 30)}<span>{t}</span></div>' for t in ['Event recaps', 'Simple short form', 'Talking heads cut into shorts', 'Captions, overlays, screenshots']) + '</div>', 'Wins on…', 'flex:1')}
    </div>
  </div>
  <div class="card" style="width:832px;height:540px">
    <div class="row" style="align-items:center;gap:20px">{icon('laptop', 70)}<div class="ct" style="font-size:42px">On a laptop</div></div>
    <div class="row" style="gap:12px;flex-wrap:wrap">{''.join(f'<div class="tag gold" style="font-size:20px">{a}</div>' for a in ['DaVinci Resolve', 'Premiere Pro + After Effects', 'CapCut Desktop', 'Final Cut (Mac)'])}</div>
    <div class="cb">Needed for long form, colour and motion.</div>
    {''.join(f'<div class="li" style="font-size:24px;margin-top:4px">{icon("chevron-right", 28)}<span>{t}</span></div>' for t in ['<b>Resolve:</b> free, a great all-rounder, especially colour grading. Needs a laptop that can run it.', '<b>Premiere + After Effects:</b> the best for heavy motion design. Paid.', '<b>CapCut:</b> the free version is enough to get paid work. Most pro tools need Pro.'])}
  </div>
</div>""")

    f2 = frame("5.2", "Tools · Invest in your software", f"""
{title('Never use', 'cracked software.', 120)}
<div class="abs" style="left:110px;top:430px;width:820px" class="col">
  {journey("I once used a cracked copy of Premiere Pro while trying to move away from Resolve. I'm not joking: <b>my computer was hacked, and it affected my client work.</b> I went straight back to Resolve.")}
  <div class="li" style="margin-top:30px">{icon('smartphone', 42)}<span><b>Phone editors: pay for CapCut Pro.</b> No money? Borrow it for the first subscription, then work hard that month to earn the next one.</span></div>
  <div class="li" style="margin-top:20px">{icon('bot', 42)}<span><b>AI tools depend on your niche.</b> I pay for Claude now. A beginner shouldn't pay for a tool they don't need.</span></div>
</div>
<div class="abs" style="left:1000px;top:430px;width:810px">
  <div class="card" style="height:500px;align-items:center;justify-content:center;text-align:center;gap:24px">{icon('shield-alert', 110)}
  {rv(quote('Whatever you pay for a subscription is your capital.', 58), 'Your subscription is…')}
  <div class="cb">Once you see it that way: &ldquo;I'm already spending capital, I need to start making profit.&rdquo; That pushes you to pitch.</div></div>
</div>""")

    f3 = frame("5.3", "Money · What editing really costs", f"""
{title('You can start for free.', "But it's not really free.", 110)}
<div class="abs" style="left:110px;top:440px;width:760px" class="col">
  <div class="row" style="gap:20px">
    <div class="card" style="width:240px;align-items:center;text-align:center">{icon('globe', 60)}<div class="ct" style="font-size:28px">Data</div></div>
    <div class="card" style="width:240px;align-items:center;text-align:center">{icon('zap', 60)}<div class="ct" style="font-size:28px">Power</div></div>
    <div class="card" style="width:240px;align-items:center;text-align:center">{icon('laptop', 60)}<div class="ct" style="font-size:28px">Device</div></div>
  </div>
  <div class="cb" style="margin-top:24px">Even a phone editor needs data to watch tutorials, download, upload and show their work, and power to keep going. <b>No fixed price to start:</b> it varies by country and by what you own.</div>
</div>
<div class="abs" style="left:960px;top:400px;width:850px;height:560px">
  {svg(f'<line x1="40" y1="300" x2="840" y2="300" stroke="{SLATE}" stroke-width="4"/>'
       f'<path d="M40 300 C180 300 200 430 300 430 C420 430 460 300 560 250 C660 200 740 130 840 80" fill="none" stroke="{CH}" stroke-width="10" stroke-linecap="round"/>'
       f'<circle cx="300" cy="430" r="14" fill="{CH}"/><circle cx="520" cy="270" r="14" fill="{CH}"/><circle cx="840" cy="80" r="14" fill="{CH}"/>',
       'position:absolute;left:0;top:0', 850, 560)}
  <div class="abs" style="left:170px;top:460px;width:260px;text-align:center"><div class="ct" style="font-size:26px">Months 1–2</div><div class="cb" style="font-size:21px">capital: an investment</div></div>
  {rv('<div class="ct" style="font-size:26px">Paid clients cover it</div><div class="cb" style="font-size:21px">then you break even</div>', 'Then…', 'position:absolute;left:400px;top:120px;width:260px;text-align:center')}
  {rv('<div class="ct" style="font-size:26px;color:#FCDD9E">Profit</div>', 'Then…', 'position:absolute;left:700px;top:0;width:150px;text-align:center')}
</div>""")

    f4 = frame("5.4", "Tools · The computer you need", f"""
{title('For DaVinci Resolve,', 'the minimum.', 120)}
<div class="abs" style="left:110px;top:430px;width:1700px;display:flex;gap:28px">
  {''.join(f'<div class="card" style="width:330px;height:250px;align-items:center;justify-content:center;text-align:center">{icon(i, 76)}<div class="ct" style="font-size:36px">{t}</div></div>' for i, t in [('memory-stick', '16 GB RAM'), ('hard-drive', 'An SSD'), ('cpu', 'A dedicated GPU')])}
  <div class="col" style="width:640px;gap:18px">
    <div class="li">{icon('wrench', 40)}<span>I upgraded RAM instead of buying new laptops. <b>Buy a laptop you can upgrade.</b></span></div>
    <div class="li">{icon('apple', 40)}<span><b>Mac (M1 and newer)</b> is the best for editing. I couldn't afford one, so I used Windows.</span></div>
  </div>
</div>
<div class="abs" style="left:110px;top:730px;width:1700px;display:flex;gap:28px;align-items:center">
  <div class="card line" style="width:1050px"><div class="ct" style="font-size:30px">Don't wait for the perfect machine.</div><div class="cb">Some wait until they earn NGN 1 million for their first laptop. That takes a while. Can only afford an <b>NGN 300,000</b> laptop (~USD 220)? Buy it and use it until you can move to an <b>NGN 600,000</b> one (~USD 450).</div></div>
  {rv(remember("Don't spend your editing money on yourself yet. Putting my earnings back into my tools was one of the fastest ways I grew.", 'width:620px'), 'Where your first money goes')}
</div>""")
    return [op, f1, f2, f3, f4]


def row6():
    op = opener(6, "Learn the skill", "The right way", "Start with who you serve, what they pay for and what your tools can do. Then learn one skill at a time, on a real video.",
                "You don't choose what to learn. What you learn is chosen for you.")
    filt = [("users", "Who you want to work for, and what kind of videos", 1500), ("dollar-sign", "Who can actually pay you", 1300),
            ("laptop", "Your hardware: phone or laptop, how strong", 1100), ("layers", "Your software: CapCut can't do 3D, so why learn it?", 900)]
    fl = "".join(rv(f'<div class="card" style="width:{w}px;margin:0 auto;height:96px;flex-direction:row;align-items:center;gap:22px;padding:18px 30px">{icon(i, 46)}<div class="ct" style="font-size:28px">{t}</div></div>', f'Filter {k+1}', f'margin-bottom:14px') for k, (i, t, w) in enumerate(filt))
    f1 = frame("6.1", "Learn the skill · The filters", f"""
{title('Work backwards. Cut what you don\'t need,', 'until you know what to learn.', 90)}
<div class="abs" style="left:110px;top:400px;width:1700px">{fl}
  <div class="card gold" style="width:700px;margin:6px auto 0;height:96px;flex-direction:row;align-items:center;justify-content:center;gap:22px">{icon('list-checks', 46, NAVY, 2)}<div class="ct" style="font-size:32px">Your learning list</div></div>
</div>""")

    f2 = frame("6.2", "Learn the skill · Different videos, different skills", f"""
<div class="abs" style="left:110px;top:150px;width:1700px"><div class="h">Each kind of video needs different skills</div>
<div class="row" style="margin-top:26px;gap:22px">{''.join(f'<div class="card" style="width:325px;height:236px">{icon(i, 46)}<div class="ct" style="font-size:28px">{h}</div><div class="cb" style="font-size:22px">{b}</div></div>' for i, h, b in [('house', 'Real estate', 'A lot of tracking and animation'), ('mic', 'Business talking heads', 'No tracking or animation needed'), ('book-open', 'Storytelling', 'Some need visual effects'), ('megaphone', 'Adverts', 'Their own skills, some VFX'), ('music', 'Some videos', "Don't even need sound effects")])}</div>
<div class="cb" style="margin-top:14px;font-size:23px">Platforms edit differently too: a YouTube talking head and an Instagram talking head are not the same. TikTok is different again, and so is LinkedIn.</div></div>
<div class="abs" style="left:110px;top:560px;width:1000px">
  <div class="step">{mark(16)} Worked example: a phone editor doing podcast recaps</div>
  <div class="row" style="gap:24px;margin-top:16px">
    {rv(f'<div class="card gold" style="width:480px;height:330px"><div class="ct">Learn</div>' + ''.join(f'<div class="li" style="color:{NAVY};font-weight:700">{icon("check", 34, NAVY, 2.4)}<span>{t}</span></div>' for t in ['Cutting', 'Sound design', 'Typography', 'Captions']) + '</div>', 'Learn…')}
    {rv(f'<div class="card line" style="width:480px;height:330px"><div class="ct" style="color:{MIST}">Skip, for now</div>' + ''.join(f'<div class="li">{icon("x", 34, MIST)}<span>{t}</span></div>' for t in ['Motion graphics', 'Heavy storytelling', '3D effects']) + '</div>', 'Skip…')}
  </div>
</div>
{journey("When I started I wanted to learn everything. I'd see a flip animation and want to learn it. Overwhelming, until I chose <b>YouTube long-form business talking heads</b>. I loved motion graphics, but my laptop couldn't handle it, so I dropped it.", 'position:absolute;left:1160px;top:600px;width:650px')}""")

    f3 = frame("6.3", "Learn the skill · Software, skill and AI", f"""
{title('Software and skill', 'are two different things.', 100)}
<div class="abs" style="left:110px;top:430px;width:1700px;display:flex;gap:30px;align-items:center">
  <div class="card" style="width:520px;height:300px"><div class="tag line">1 · The software</div><div class="ct" style="font-size:40px">Master it first</div><div class="cb">The one you will actually use. For CapCut, sit through the long 4-5 hour tutorials.</div></div>
  {svg(arrow(0, 40, 80, 40, w=7), 'position:relative', 90, 80)}
  {rv(f'<div class="card gold" style="width:520px;height:300px"><div class="tag" style="background:{NAVY};color:{CH}">2 · The skill</div><div class="ct" style="font-size:40px">Then learn the craft</div><div class="cb">The art of cutting, pacing and sound that makes the kind of video you chose.</div></div>', 'Then…')}
  <div class="cb" style="width:460px">The mistake: learning the software and thinking that's editing. <b>I mastered DaVinci Resolve. The software was only the start.</b></div>
</div>
<div class="abs" style="left:110px;top:780px;width:1700px;display:flex;gap:30px">
  <div class="card line" style="width:900px;flex-direction:row;gap:22px;align-items:center">{icon('bot', 64)}<div class="cb"><b>AI is part of what you learn</b>, one tool at a time. I use Claude Code to edit parts of my videos. If you use AI tools on a client's work, charge for them.</div></div>
  {rv(remember('&ldquo;I use AI to enhance your videos faster, so you can put out content faster.&rdquo;', 'width:770px', 'AI is also a pitch'), 'AI is also…')}
</div>""")

    loop = [("target", "Name your video type", "e.g. talking heads for business creators on Instagram"),
            ("bot", "Ask AI for the skill list", "cutting, pacing, captions, typography, B-roll, sound, music"),
            ("youtube", "One tutorial, one skill", "learn them one by one"),
            ("clapperboard", "Use it on one practice video", "same video, skill after skill")]
    cx, cy, r = 470, 330, 240
    import math
    nodes = ""
    for k, (i, h, b) in enumerate(loop):
        a = -math.pi / 2 + k * math.pi / 2
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        nodes += rv(f'<div class="card" style="width:330px;height:170px;padding:20px 24px;gap:6px"><div class="row" style="gap:12px;align-items:center">{icon(i, 38)}<div class="ct" style="font-size:25px">{k+1}. {h}</div></div><div class="cb" style="font-size:20px">{b}</div></div>', f'Step {k+1}', f'position:absolute;left:{x-165:.0f}px;top:{y-85:.0f}px')
    f4 = frame("6.4", "Learn the skill · Where to learn: YouTube", f"""
{title('The problem is never the source.', "It's the search.", 100)}
<div class="abs" style="left:110px;top:330px;width:940px;height:700px">
  {svg(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{SLATE}" stroke-width="12" stroke-dasharray="30 22"/>', 'position:absolute;left:0;top:0', 940, 700)}
  {nodes}
</div>
<div class="abs" style="left:1100px;top:390px;width:710px;display:flex;flex-direction:column;gap:20px">
  {remember("Don't learn without implementation.")}
  <div class="row" style="gap:18px">
    <div class="card" style="width:345px"><div class="tag line">Free · YouTube</div><div class="ct" style="font-size:30px">The skill</div><div class="cb" style="font-size:22px">Everything a skills course sells is on YouTube. I never paid for one.</div></div>
    <div class="card gold" style="width:345px"><div class="tag" style="background:{NAVY};color:{CH}">Worth paying for</div><div class="ct" style="font-size:30px">The business</div><div class="cb" style="font-size:22px">Clients, packaging, presenting yourself.</div></div>
  </div>
  <div class="li" style="font-size:24px">{icon('zap', 36)}<span><b>Learn on the go.</b> A client asks &ldquo;Can you do this?&rdquo; I say yes, then learn it on that project.</span></div>
</div>""")

    steps = ["Pick your niche, e.g. podcast videos", "Find an edit you love: a short cut from a podcast", "Find the raw podcast on YouTube and download it",
             "Copy the same edit", "Can't do something? Search YouTube for that one thing, learn it, put it in"]
    f5 = frame("6.5", "Learn the skill · Recreate videos you love", f"""
{title('One of the fastest ways to learn:', 'Recreate.', 120)}
<div class="abs" style="left:110px;top:430px;width:900px">
  {''.join(f'<div class="li" style="margin-bottom:16px"><div class="num" style="font-size:50px;width:46px">{k+1}</div><span style="color:#fff;font-weight:600">{t}</span></div>' for k, t in enumerate(steps))}
  <div class="cb" style="margin-top:6px;font-size:23px">Raw footage: YouTube is a mine of raw videos. Skip the biggest creators, their videos are already over-edited.</div>
</div>
<div class="abs" style="left:1080px;top:200px;width:730px;display:flex;flex-direction:column;gap:20px">
  {demo('How to download a YouTube video', 'Optional: only if time allows')}
  <div class="row" style="gap:16px">{ph('Clip: the original edit', 'height:240px;width:357px', src('recreate_a'))}{ph('Clip: your recreation', 'height:240px;width:357px', src('recreate_b'))}</div>
  <div class="cb" style="font-size:23px">Share it side by side with the original. <b>It's practice, not portfolio.</b> You copy what someone did professionally, so one day you become like that person.</div>
</div>""")

    f6 = frame("6.6", "Learn the skill · Edit for the goal", f"""
{title('Edit for the goal,', 'not to look edited.', 110)}
<div class="abs" style="left:110px;top:420px;width:900px;display:flex;gap:24px">
  <div class="card line" style="width:430px;height:330px">{icon('sparkles', 54, MIST)}<div class="ct">The flashy video</div><div class="num" style="font-size:40px;color:#fff">Lots of views</div><div class="num" style="font-size:40px;color:{MIST}">No sales</div></div>
  <div class="card gold" style="width:430px;height:330px">{icon('target', 54, NAVY, 2)}<div class="ct">The clear video</div><div class="num" style="font-size:40px;color:{NAVY}">Fewer views</div><div class="num" style="font-size:40px;color:{NAVY}">Lots of sales</div></div>
</div>
{rv('<div class="ct" style="font-size:30px">Which would your client rather have?</div><div class="cb">A client will choose an editor whose videos produce results over flashy edits that don\'t perform.</div>', 'Which one?', 'position:absolute;left:110px;top:780px;width:880px')}
<div class="abs" style="left:1080px;top:420px;width:730px">
  <div class="step">{mark(16)} Show, don't tell</div>
  <div class="row" style="gap:18px;margin-top:16px">
    <div class="card line" style="width:356px;height:250px;align-items:center;justify-content:center">{icon('car', 90, MIST)}<div class="cb">A car icon: the viewer reads a symbol</div></div>
    {rv(f'<div class="card gold" style="width:356px;height:250px;align-items:center;justify-content:center;text-align:center">{icon("video", 90, NAVY, 2)}<div class="cb">Real car footage: the viewer sees the real thing</div></div>', 'Stronger…')}
  </div>
  <div class="cb" style="margin-top:18px;font-size:23px">Talking about YouTube views? Show YouTube views. Some of my videos are about <b>80% showing</b> what the client says rather than their face. What viewers hear and see must match.</div>
</div>""")
    return [op, f1, f2, f3, f4, f5, f6]


def row7():
    op = opener(7, "From practice to", "Paid", "Finish three full videos in your niche. Then get onto real people's videos: free at first, then a token, then paid.",
                "When you can finish a full video from beginning to end, you're good enough to charge.")
    ladder = [("clapperboard", "Practice videos", "your own, like 2-3 talking heads of yourself"), ("handshake", "Real people's videos, free", "as soon as possible"),
              ("coins", "Ask for a token", "if they're enjoying it"), ("badge-dollar-sign", "Charge", "")]
    lad = "".join(rv(f'<div class="card {"gold" if k == 3 else ""}" style="width:380px;height:{170 + k*70}px;justify-content:flex-end">{icon(i, 52, NAVY if k == 3 else CH, 2)}<div class="ct" style="font-size:30px">{h}</div><div class="cb" style="font-size:21px">{b}</div></div>', f'Step {k+1}', 'align-self:flex-end') for k, (i, h, b) in enumerate(ladder))
    f1 = frame("7.1", "Practice to paid · When you're ready", f"""
<div class="abs" style="left:110px;top:160px;width:620px">
  <div class="num" style="font-size:420px">3</div>
  <div class="ct" style="font-size:40px;margin-top:-20px">full videos in your niche, start to finish.</div>
  <div class="cb" style="margin-top:16px">Then you're ready to charge. Most people wait too long because they <b>never finish a whole project</b>: they learn nuggets, not full videos.</div>
</div>
<div class="abs" style="left:790px;top:240px;width:1020px">
  <div class="step">{mark(16)} The ladder from practice to paid</div>
  <div class="row" style="gap:16px;align-items:flex-end;margin-top:20px;height:560px">{lad}</div>
  <div class="cb" style="margin-top:18px;font-size:23px">Someone sees your practice and asks &ldquo;How much do you charge?&rdquo; <b>Don't say &ldquo;I'm not ready.&rdquo;</b></div>
</div>""")
    # the ladder cards are 380 wide x 4 = too wide for 1020; narrower cards
    f1 = f1.replace("width:380px;height:", "width:240px;height:")

    f2 = frame("7.2", "Practice to paid · Why real projects teach fastest", f"""
{title('Real projects, real consequences,', 'real people.', 110)}
<div class="abs" style="left:110px;top:430px;width:1000px;display:flex;gap:24px">
  <div class="card line" style="width:480px;height:330px">{icon('hourglass', 60, MIST)}<div class="tag line">Your practice video</div><div class="ct" style="font-size:38px">No deadline</div><div class="cb">You can spend a whole month on one video. Nothing is at stake.</div></div>
  {rv(f'<div class="card gold" style="width:480px;height:330px">{icon("flame", 60, NAVY, 2)}<div class="tag" style="background:{NAVY};color:{CH}">A real project</div><div class="ct" style="font-size:38px">They post it tomorrow</div><div class="cb">You try your best not to make mistakes. It keeps you up late.</div></div>', 'The difference: pressure')}
</div>
<div class="abs" style="left:1170px;top:430px;width:640px">
  <div class="step">{mark(16)} Who to edit for, free</div>
  {''.join(f'<div class="li" style="margin-top:16px;font-size:25px">{icon(i, 38)}<span>{t}</span></div>' for i, t in [('store', '<b>A friend who owns a business:</b> &ldquo;Record a video, let me edit it so you can post it.&rdquo;'), ('calendar', '<b>An event you attend:</b> capture it, edit it, show them'), ('house', '<b>Small businesses near you</b> without an editor budget'), ('user', '<b>Small creators</b> making content in your style')])}
</div>""")

    f3 = frame("7.3", "Practice to paid · Work for free without getting stuck", f"""
{title('Free first.', "Don't get stuck there.", 110)}
<div class="abs" style="left:110px;top:420px;width:820px" class="col">
  {''.join(f'<div class="li" style="margin-bottom:18px">{icon(i, 40)}<span>{t}</span></div>' for i, t in [('gift', '<b>Free is the best way to start.</b>'), ('coins', '<b>Low pay next</b>, even NGN 5,000 or 10,000. It funds what learning costs: data and electricity.'), ('timer', "<b>After 4 or 5 free projects for one person</b>, move to paid, unless you have an agreement."), ('ban', '<b>Never &ldquo;free for a year&rdquo;.</b> Set the scope up front.')])}
  {journey('An editor once worked for me free for a whole month. After that, I started paying them.', 'margin-top:10px')}
</div>
<div class="abs" style="left:1000px;top:400px;width:810px">
  <div class="step">{mark(16)} The scope ask</div>
  <div class="chat" style="margin-top:18px">
    <div class="bub me">Sir, please, can I edit your videos for one month for free? I'm trying to build my portfolio and I'm looking for more work. I would love to partner with you.</div>
    <div class="cb" style="text-align:center;font-size:22px">or</div>
    <div class="bub me">Let me do five videos for you, for free.</div>
  </div>
  {rv(remember("Don't tell them you're learning. Tell them you're building your portfolio.", 'margin-top:22px'), 'What to say')}
</div>""")

    gives = [("message-square-text", "Testimonials", "People won't know it was free."), ("folder-open", "A portfolio", "Real work to show."),
             ("clock", "Experience", "Years that count."), ("shield-check", "Confidence", "You've done it before."),
             ("share-2", "Referrals", "Happy people talk."), ("scissors", "Sharper skills", "Pressure teaches.")]
    f4 = frame("7.4", "Practice to paid · What free work gives you", f"""
{title('What free work', 'gives you.', 120)}
<div class="abs" style="left:110px;top:370px;width:1700px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px">
  {''.join(rv(f'<div class="card" style="height:190px;flex-direction:row;align-items:center;gap:24px">{icon(i, 64)}<div><div class="ct">{h}</div><div class="cb">{b}</div></div></div>', '?') for i, h, b in gives)}
</div>
{remember('You have to learn to humble yourself and work for free. Most people think they need to get paid. You want to get better.', 'position:absolute;left:110px;bottom:50px;width:1500px')}""")
    return [op, f1, f2, f3, f4]


ROWS = [("row04-niche", row4), ("row05-tools", row5), ("row06-learn", row6), ("row07-practice", row7)]
