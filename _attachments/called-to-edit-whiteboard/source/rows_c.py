"""Rows 8-9: get seen, get clients."""
from lib import *

P = {}


def src(k):
    return P.get(k)


def row8():
    op = opener(8, "Get", "Seen", "No one who learns from me succeeds without visibility. Pick one platform, show who you help, and post every day.",
                "You can't succeed in this industry if you are hidden.")
    f1 = frame("8.1", "Get seen · Where can people find you?", f"""
<div class="abs" style="left:110px;top:150px;width:1000px">
  <div class="tl" style="font-size:40px">The question my mentor asked me:</div>
  {quote('Where can people find you? When they need you, where can they see your work?', 72, 'margin-top:20px')}
  <div class="sub" style="margin-top:26px">I had nowhere to show it. So I opened <b>brand-new Twitter, LinkedIn and Instagram</b> accounts and did two things.</div>
</div>
<div class="abs" style="left:110px;top:640px;width:1000px;display:flex;gap:24px">
  {rv(f'<div class="card" style="width:488px;height:330px"><div class="num" style="font-size:80px">1</div><div class="ct">I curated my feed</div><div class="cb">Searched &ldquo;video editors&rdquo; and followed every major editor: about 50 on Twitter. My feed fed me editing all day.</div></div>', 'Thing 1')}
  {rv(f'<div class="card gold" style="width:488px;height:330px"><div class="num" style="font-size:80px;color:{NAVY}">2</div><div class="ct">I posted my work</div><div class="cb">Recorded myself working, photographed my timeline, screenshotted my day. <b style="color:{NAVY}">No less than 3 times a day.</b></div></div>', 'Thing 2')}
</div>
<div class="abs" style="left:1180px;top:150px;width:630px;display:flex;flex-direction:column;gap:22px">
  {ph('Photo: your phone recording you at work / your timeline post', 'height:500px', src('worklapse'))}
  {remember('Showing your work is your leverage.')}
  <div class="cb" style="font-size:23px">For your first month, <b>lock in</b>: all your social media about editing, especially your niche. A secret most people don't know.</div>
</div>""")

    plats = [("twitter", "Twitter (X) & LinkedIn", "Best for beginners", "Agencies and clients search here. Low effort: text and screenshots, no face needed.", "Where I got clients: mostly international agencies and companies.", True),
             ("instagram", "Instagram", "Big if you put in the work", "Personal brand and a mini portfolio at once. Your face, your voice, editing your own videos.", "Where I got clients: a mix of international and Nigerian.", False),
             ("music", "TikTok", "Personal brand", "Your face and your story, like Instagram.", "Where I got clients: lots of DMs from people near me, in Nigeria.", False),
             ("facebook", "Facebook", "Not for this", "One of the worst places to build a brand as an editor.", "Low-paying, frustrating clients.", False)]
    pc = "".join(
        f'<div class="card {"gold" if g else ""}" style="width:400px;height:520px">{icon(i, 60, NAVY if g else CH, 2)}<div class="ct">{h}</div>'
        + rv(f'<div class="tag {"" if g else "line"}" style="{"background:" + NAVY + ";color:" + CH if g else ""}">{t}</div>', 'Verdict?')
        + f'<div class="cb">{b}</div><div class="cb" style="margin-top:auto;font-size:22px"><b style="color:{NAVY if g else "#fff"}">{w}</b></div></div>'
        for i, h, t, b, w, g in plats)
    f2 = frame("8.2", "Get seen · Pick one platform and own it", f"""
{title('Pick one platform.', 'Own it.', 120)}
<div class="abs" style="left:110px;top:400px;width:1700px;display:flex;gap:33px">{pc}</div>
<div class="abs" style="left:900px;top:160px;width:910px" class="cb"><div class="cb" style="font-size:24px">Become the known person for your niche there. Two platforms if you have the capacity. <b>Who you engage shapes who finds you.</b> I've now moved from Twitter to Instagram to build my authority.</div></div>""")

    callouts = [("Your face", "People trust who they can see."), ("Name + what you do", ""), ("Bio = your offer", "Chapter 4"),
                ("Clients you've edited for", ""), ("Portfolio link, always", ""), ("Pinned post = your best edit", ""), ("A good banner", "")]
    co_html = "".join(rv('<div class="li" style="margin-top:20px;color:#fff;font-weight:700"><div class="num" style="font-size:44px;width:40px">%d</div><span>%s%s</span></div>' % (k + 1, h, (' <span style="color:#B9C3D6;font-weight:500">· ' + b + '</span>') if b else ''), 'Point %d' % (k + 1), 'width:850px') for k, (h, b) in enumerate(callouts))
    f3 = frame("8.3", "Get seen · Build your profile", f"""
<div class="abs" style="left:110px;top:150px;width:780px">
  <div class="mock" style="height:820px">
    <div style="height:220px;background:linear-gradient(135deg,#1E3150,#0A1F44);display:flex;align-items:center;justify-content:center;font:800 26px 'Plus Jakarta Sans';letter-spacing:.2em;color:#B9C3D6">BANNER</div>
    <div style="width:170px;height:170px;border-radius:50%;background:#FCDD9E;border:8px solid #fff;margin:-90px 0 0 40px;display:flex;align-items:center;justify-content:center">{icon('user', 90, NAVY, 2)}</div>
    <div style="padding:16px 40px">
      <div style="font:800 40px 'Plus Jakarta Sans'">Samuel Adebayo</div>
      <div style="font:600 26px 'Plus Jakarta Sans';color:#4A5670">Long-form video editor</div>
      <div style="font:500 26px/1.4 'Plus Jakarta Sans';margin-top:14px">I help business owners get their first 10,000 views in 3 videos.</div>
      <div style="font:500 24px 'Plus Jakarta Sans';margin-top:10px;color:#4A5670">Edited for: [your clients]</div>
      <div style="font:700 24px 'Plus Jakarta Sans';margin-top:10px;color:#8A5E17">🔗 yourportfolio.site</div>
      <div style="margin-top:20px;border:3px solid #E3E7EF;border-radius:18px;padding:18px;display:flex;gap:16px;align-items:center"><div class="tag" style="background:#0A1F44;color:#FCDD9E">Pinned</div><div style="font:700 24px 'Plus Jakarta Sans'">My best edit</div>{icon('circle-play', 40, NAVY, 2)}</div>
    </div>
  </div>
</div>
<div class="abs" style="left:960px;top:150px;width:850px">
  <div class="h">Build your profile</div>
  {co_html}
  <div class="cb" style="margin-top:26px">A lot of us hide ourselves. <b>Show your face, often.</b> Pin the edit you're proudest of so the first impression is &ldquo;this person is a professional.&rdquo;</div>
</div>""")

    types = [("monitor", "A normal day", "You working, you on a call with a client."), ("book-open", "Your story", "My soldier-to-editor story hits every single time."),
             ("mountain", "Struggles", "A client who turned you down."), ("trophy", "Wins", "A new client, a new laptop."),
             ("flag", "Challenges", "&ldquo;Day one of trying to get my first client. Day two…&rdquo;")]
    ring = (f'<circle cx="95" cy="95" r="70" fill="none" stroke="{SLATE}" stroke-width="40"/>'
            f'<circle cx="95" cy="95" r="70" fill="none" stroke="{CH}" stroke-width="40" stroke-dasharray="176 440" transform="rotate(-90 95 95)"/>'
            f'<circle cx="95" cy="95" r="70" fill="none" stroke="{MIST}" stroke-width="40" stroke-dasharray="176 440" stroke-dashoffset="-176" transform="rotate(-90 95 95)"/>')
    donut = rv('<div class="card" style="flex-direction:row;align-items:center;gap:26px">' + svg(ring, "position:relative", 190, 190)
               + '<div><div class="cb" style="font-size:25px;line-height:1.7"><b class="g">40% authentic</b> builds emotion<br><b>40% authority</b> proves you know<br><b>20% sales</b> pitches you</div></div></div>', 'The post mix')
    f4 = frame("8.4", "Get seen · Build a personal brand", f"""
{title('This is the AI age.', 'Be a real human.', 110)}
<div class="abs" style="left:110px;top:410px;width:980px">
  <div class="cb">People copy posts and generate them with AI. Clients need to know you're genuine. <b>Post your life around video editing, and nothing else for now.</b></div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px">{''.join(f'<div class="card" style="padding:22px;gap:6px">{icon(i, 40)}<div class="ct" style="font-size:26px">{h}</div><div class="cb" style="font-size:20px">{b}</div></div>' for i, h, b in types)}
    <div class="card gold" style="padding:22px;gap:4px;justify-content:center"><div class="num" style="font-size:64px;color:{NAVY}">2–3</div><div class="ct" style="font-size:24px">posts a day</div></div></div>
</div>
<div class="abs" style="left:1150px;top:170px;width:660px;display:flex;flex-direction:column;gap:20px">
  {donut}
  <div class="row" style="gap:16px">{ph('Screenshot: a post that landed you a client', 'height:300px;width:322px', src('clientpost1'), 'contain')}{ph('Screenshot: another post that landed a client', 'height:300px;width:322px', src('clientpost2'), 'contain')}</div>
  {demo('My Twitter: the posts that landed me clients', 'Open x.com, scroll my old editing posts')}
</div>
<div class="abs" style="left:110px;bottom:70px;width:980px;display:flex;align-items:center;gap:26px">
  <div class="num" style="font-size:110px">700</div><div class="cb" style="font-size:26px">followers on Twitter. That's all I had. <b>The best clients I needed came from those 700.</b> I posted 3 times a day for 60 days.</div>
</div>""")

    f5 = frame("8.5", "Get seen · Your portfolio", f"""
{title('A link in your bio.', 'Your portfolio.', 110)}
<div class="abs" style="left:110px;top:410px;width:880px;display:flex;gap:22px">
  <div class="card line" style="width:430px;height:250px">{icon('folder-open', 54, MIST)}<div class="ct" style="color:{MIST}">A shared drive folder</div><div class="cb">Click. Wait. Click. They go to another editor.</div></div>
  {rv(f'<div class="card gold" style="width:430px;height:250px">{icon("globe", 54, NAVY, 2)}<div class="ct">A simple website</div><div class="cb">They just watch. That is all a client wants.</div></div>', 'The best portfolio')}
</div>
<div class="abs" style="left:110px;top:690px;width:880px">
  <div class="step">{mark(16)} Build it with AI, in one night</div>
  {''.join(f'<div class="li" style="margin-top:12px;font-size:25px"><div class="num" style="font-size:40px;width:34px">{k+1}</div><span>{t}</span></div>' for k, t in enumerate(['Upload your edits to YouTube as <b>unlisted</b> videos.', 'Copy the links.', 'Paste into an AI: <b>&ldquo;These are the videos I edited. Use them to create a portfolio I can link in my bio.&rdquo;</b>']))}
</div>
<div class="abs" style="left:1060px;top:150px;width:750px;display:flex;flex-direction:column;gap:18px">
  {ph('Screenshot: your Framer portfolio site', 'height:360px', src('portfolio'), 'contain')}
  {demo('My portfolio site', 'Built on Framer in one night. It got me clients.')}
  <div class="row" style="gap:14px">{''.join(f'<div class="card" style="width:240px;padding:20px;gap:6px"><div class="ct" style="font-size:24px">{h}</div><div class="cb" style="font-size:19px">{b}</div></div>' for h, b in [('Framer (mine)', 'Free on a Framer address. Best looking.'), ('Canva Websites', 'Free on a Canva address. Easiest.'), ('Carrd', 'Up to 3 one-page sites free. Simplest.')])}</div>
</div>""")

    f6 = frame("8.6", "Get seen · What goes in it", f"""
<div class="abs" style="left:110px;top:150px;width:900px">
  <div class="h">What goes in it</div>
  <div class="row" style="gap:20px;margin-top:22px;align-items:center"><div class="num" style="font-size:150px">8</div><div class="cb" style="font-size:28px">videos at most: <b>your top 4 and your other 4</b>. Only have 3? Put the 3. Too many gives the client too much work.</div></div>
  {''.join(f'<div class="li" style="margin-top:12px">{icon(i, 38)}<span>{t}</span></div>' for i, t in [('repeat', '<b>Before and afters</b>'), ('message-square-text', '<b>Testimonials:</b> screenshots of what clients said'), ('trending-up', '<b>Results:</b> screenshots of what you got for clients'), ('user', '<b>About you:</b> who you are, how long you\'ve edited')])}
</div>
<div class="abs" style="left:1080px;top:150px;width:730px;display:flex;flex-direction:column;gap:22px">
  {rv(quote('Your practice work is your work.', 84), 'I repeat…')}
  <div class="cb">No clients yet? Free work and practice on real people's videos count: their footage, your edit. Recreations stay practice. Replace them with real projects as they come.</div>
  <div class="card line" style="flex-direction:row;gap:20px;align-items:center">{icon('palette', 54)}<div class="cb"><b>Look the part.</b> Pick brand colours and stick to them. Mine was green. I use Canva for banners.</div></div>
</div>
{doit('For the next month: curate your feed around your niche, fix your profile with the 7 points, build a simple portfolio site, and post 2 to 3 times a day.', 'position:absolute;left:110px;bottom:84px;width:1700px')}""")
    return [op, f1, f2, f3, f4, f5, f6]


def row9():
    op = opener(9, "Get", "Clients", "Skill, a strong personal brand, a strong portfolio, outreach and a network of editors. Done together, consistently.",
                "Getting clients is a lot of hard work. That's the truth.")
    f1 = frame("9.1", "Get clients · Two ways in", f"""
{title('The people you reach out to', 'will check your page first.', 100)}
<div class="abs" style="left:110px;top:440px;width:1700px;display:flex;gap:40px;align-items:center">
  <div class="card" style="width:760px;height:380px">{icon('magnet', 70)}<div class="tag line">Inbound</div><div class="ct" style="font-size:44px">They come to you</div>
    <div class="bub them" style="max-width:100%;margin-top:10px">Hey, I saw your work. How much do you charge?</div></div>
  <div class="num" style="font-size:90px">+</div>
  <div class="card gold" style="width:760px;height:380px">{icon('send', 70, NAVY, 2)}<div class="tag" style="background:{NAVY};color:{CH}">Outbound</div><div class="ct" style="font-size:44px">You go to them</div>
    <div class="cb" style="font-size:28px">You see someone whose videos you could edit, and you reach out.</div></div>
</div>
<div class="abs" style="left:110px;bottom:84px;width:1700px" class="sub"><div class="sub"><b>Do both.</b> Established editors get more inbound; beginners have to go looking. If your page is empty, they won't even reply.</div></div>""")

    why = [("eye", "Showing your work", "and how you came up with it"), ("user", "The person behind it", "your personality. Specific makes you unique"),
           ("clock", "Reliability", "clients are tired of flashy editors who miss deadlines. Document your day"),
           ("badge-check", "Credibility", "testimonials and the results your work brought"), ("calendar", "Consistency", "not once a week. Every day")]
    f2 = frame("9.2", "Get clients · Inbound: make them come to you", f"""
{title('What makes a client DM you', 'instead of another editor?', 96)}
<div class="abs" style="left:110px;top:420px;width:960px">
  {''.join(rv(f'<div class="card" style="flex-direction:row;align-items:center;gap:22px;padding:20px 26px;margin-bottom:14px">{icon(i, 46)}<div><div class="ct" style="font-size:28px">{h}</div><div class="cb" style="font-size:21px">{b}</div></div></div>', f'Reason {k+1}') for k, (i, h, b) in enumerate(why))}
</div>
<div class="abs" style="left:1140px;top:330px;width:670px;display:flex;flex-direction:column;gap:18px">
  {ph('Video: one of your working time-lapses', 'height:250px', src('timelapse'))}
  {journey('A client scrolled my profile, saw my day-to-day time-lapses, and said: <b>&ldquo;This guy is locked in.&rdquo;</b>')}
  {remember('There are a lot of clients looking for editors. You are invisible. That\'s why they can\'t find you.')}
  <div class="cb" style="font-size:22px">Be patient: one, two, three months of consistency.</div>
</div>""")

    f3 = frame("9.3", "Get clients · Warm outreach first", f"""
{title('Start with people who', 'already know you.', 110)}
<div class="abs" style="left:110px;top:420px;width:820px">
  <div class="row" style="gap:14px;flex-wrap:wrap">{''.join(f'<div class="tag line" style="font-size:20px;padding:12px 20px">{t}</div>' for t in ['Friends', 'Family', 'Colleagues making content', 'People in your DMs', 'Your contacts', 'Editors you know'])}</div>
  <div class="cb" style="margin-top:22px">Warm outreach converts the fastest, because they already know and trust you. <b>My first client, my mentor, was warm.</b> Even a relative who works in a bank may know someone.</div>
  {rv(remember("They want to see experience. They don't see knowledge.", 'margin-top:24px'), 'What clients want to see')}
</div>
<div class="abs" style="left:1000px;top:200px;width:810px">
  <div class="step">{mark(16)} To my mentor</div>
  <div class="chat" style="margin-top:14px"><div class="bub me">Sir, I love your videos and I see what you do. I would love to help you out with your videos.</div></div>
  <div class="step" style="margin-top:30px">{mark(16)} To anyone you know</div>
  <div class="chat" style="margin-top:14px"><div class="bub me">I'm a video editor. Do you know anyone who needs my service?</div></div>
  {doit('Do one warm outreach after tonight. Research who to reach first, then send it.', 'margin-top:34px')}
</div>""")

    signs = [("target", "In your niche", "the videos you chose to edit"), ("dollar-sign", "Makes money", "in some form, so they can afford you"), ("scissors", "Needs an editor", "weak, badly edited or unedited videos")]
    f4 = frame("9.4", "Get clients · Find cold clients", f"""
{title('Go where your client is.', 'Find cold clients.', 110)}
<div class="abs" style="left:110px;top:420px;width:1000px">
  <div class="step">{mark(16)} The three signs of a potential client</div>
  <div class="row" style="gap:20px;margin-top:16px">{''.join(rv(f'<div class="card" style="width:320px;height:250px"><div class="num" style="font-size:60px">{k+1}</div><div class="ct" style="font-size:30px">{h}</div><div class="cb" style="font-size:22px">{b}</div></div>', f'Sign {k+1}') for k, (i, h, b) in enumerate(signs))}</div>
  <div class="cb" style="margin-top:22px;font-size:24px">YouTube clients? Search YouTube for creators in your niche. Watch their videos. Scroll past the many who already have great editors. <b>Find their email</b> on the channel, then find them everywhere else and save example videos.</div>
</div>
<div class="abs" style="left:1180px;top:170px;width:630px;display:flex;flex-direction:column;gap:20px">
  {demo('Finding clients on YouTube and Instagram', 'Search my niche live, check the three signs, find the email')}
  <div class="card" style="flex-direction:row;gap:20px;align-items:center">{icon('youtube', 60)}{icon('instagram', 60)}{icon('linkedin', 60)}{icon('twitter', 60)}</div>
  <div class="card line">{icon('building-2', 46)}<div class="cb"><b>Agencies are clients too.</b> Most post on Twitter and LinkedIn that they need an editor. Good for beginners.</div></div>
</div>""")

    cells = [("Name", "Joshua"), ("Channel or handle", "@joshua_b2b"), ("Email", "from his YouTube About page"), ("Other platforms", "Instagram, LinkedIn, Twitter"),
             ("Content", "B2B SaaS explainers, long form"), ("Followers", "8,400"), ("Example videos", "3 links saved"), ("Follow-ups", "✓ 1   ✓ 2   ☐ 3   ☐ 4")]
    tools = [("YouTube itself", "A channel's About page shows a business email. Free."), ("Channel Crawler", "Search channels by niche, country, subs. Emails paid."),
             ("TubeMailer", "Chrome extension for public business emails. Free to try."), ("Modash", "Creators on IG, TikTok, YouTube by niche and size."),
             ("AI agents", "Claude Code (I pay ~NGN 33,000 / USD 25 a month), Codex, Grok.")]
    f5 = frame("9.5", "Get clients · The dream client list", f"""
{title('The most important thing for every editor:', 'The dream client list.', 96)}
<div class="abs" style="left:110px;top:420px;width:900px">
  <div class="mock" style="padding:26px 30px">
    <div style="font:800 18px 'Plus Jakarta Sans';letter-spacing:.14em;color:#8A5E17">ONE ROW OF YOUR LIST · NOTION OR A SPREADSHEET</div>
    {''.join(f'<div style="display:flex;border-bottom:2px solid #E3E7EF;padding:10px 0;font:500 23px \'Plus Jakarta Sans\'"><div style="width:300px;color:#4A5670;font-weight:600">{a}</div><div style="font-weight:700">{b}</div></div>' for a, b in cells)}
    <div style="font:500 18px 'Plus Jakarta Sans';color:#4A5670;margin-top:10px">A made-up example row.</div>
  </div>
</div>
<div class="abs" style="left:1080px;top:170px;width:730px;display:flex;flex-direction:column;gap:14px">
  <div class="row" style="gap:16px">
    {rv(f'<div class="card gold" style="width:357px;padding:22px"><div class="num" style="font-size:72px;color:{NAVY}">20–50</div><div class="cb">names to aim for</div></div>', 'How many?')}
    {rv(f'<div class="card" style="width:357px;padding:22px"><div class="num" style="font-size:72px">100</div><div class="cb">mine: my dream 100, by hand</div></div>', 'Mine?')}
  </div>
  <div class="cb" style="font-size:22px">Gathering leads, not reaching out yet. Add every day. Keep two lists: <b>potential clients</b> and <b>clients you work with</b>.</div>
  {''.join(f'<div class="li" style="font-size:21px">{icon("search", 30)}<span><b>{h}:</b> {b}</span></div>' for h, b in tools)}
</div>""")

    f6 = frame("9.6", "Get clients · Warm them up first", f"""
{title('Before you reach out,', 'warm them up.', 110)}
<div class="abs" style="left:110px;top:430px;width:1700px;display:flex;align-items:center;gap:18px">
  {''.join(rv(f'<div class="card" style="width:345px;height:300px">{icon(i, 60)}<div class="ct" style="font-size:30px">{h}</div><div class="cb" style="font-size:22px">{b}</div></div>', f'Step {k+1}') + (svg(arrow(0, 40, 50, 40, w=6), "position:relative", 60, 80) if k < 3 else "") for k, (i, h, b) in enumerate([("bell", "Turn on notifications", "for the creator"), ("message-circle", "Be the first to comment", "say something genuinely good about what they teach"), ("repeat", "Do it on 4 or 5 posts", "especially smaller creators: they notice you"), ("eye", "They check your page", "see you're an editor, and may reach out first")]))}
</div>
<div class="abs" style="left:110px;top:800px;width:1700px;display:flex;gap:30px;align-items:center">
  <div class="row" style="gap:14px">{icon('mail', 60)}{svg(arrow(0, 30, 40, 30, w=5), 'position:relative', 50, 60)}{icon('instagram', 60)}{svg(arrow(0, 30, 40, 30, w=5), 'position:relative', 50, 60)}{icon('twitter', 60)}</div>
  <div class="cb" style="width:1200px">Then reach them on <b>every platform</b>. I emailed each of my 100, then sent an Instagram DM, then a Twitter message. <b>By the third, they think: this person really means business.</b></div>
</div>""")

    f7 = frame("9.7", "Get clients · Cold DMs: talk first, pitch later", f"""
<div class="abs" style="left:110px;top:150px;width:700px">
  <div class="h">Why most cold messages fail</div>
  <div class="bub me" style="max-width:100%;margin-top:20px;opacity:.55;text-decoration:line-through">Hey, my name is Samuel, I'm a video editor, and I'd love to work for you. Here's my portfolio.</div>
  <div class="cb" style="margin-top:16px">Too cold. You just want their money, and you show no interest in what they do.</div>
  <div class="li" style="margin-top:28px">{icon('shield-check', 40)}<span>A question lowers their guard. There are a lot of scammers; <b>a curious, casual person is not one.</b></span></div>
  <div class="li" style="margin-top:18px">{icon('mic', 40)}<span>In DMs, <b>send voice notes.</b> People want to hear real humans. Send your picture and your portfolio too.</span></div>
</div>
<div class="abs" style="left:880px;top:150px;width:930px">
  <div class="row" style="align-items:center;gap:16px"><div style="width:64px;height:64px;border-radius:50%;background:{SLATE};display:flex;align-items:center;justify-content:center;font:800 28px 'Plus Jakarta Sans'">J</div><div><div class="ct" style="font-size:28px">Joshua</div><div class="cb" style="font-size:20px">B2B SaaS creator · example</div></div></div>
  <div class="chat" style="margin-top:16px">
    <div class="step">1 · Open with a question, not a pitch</div>
    <div class="bub me">Hi Joshua. I saw your video about B2B SaaS. That was a wonderful video, I learned a lot from it. How do you make these videos?</div>
    {rv('<div class="bub them" style="max-width:100%">Thanks! I record them myself and edit when I find time.</div><div class="step" style="margin-top:14px">2 · Steer to a problem</div><div class="bub me" style="max-width:100%;margin-left:auto">These videos are nice, but do they bring you clients? Some aren\'t performing, and they have high potential. Do you have an editor?</div>', 'Step 2', 'display:flex;flex-direction:column;gap:14px')}
    {rv('<div class="bub them" style="max-width:100%">Not really. Not many customers from them yet.</div><div class="step" style="margin-top:14px">3 · Pitch, with value first</div><div class="bub me" style="max-width:100%;margin-left:auto">I\'m a video editor and I can help you make videos that bring better customers. Can I edit one or two videos for you for free, so we see how they perform?</div>', 'Step 3', 'display:flex;flex-direction:column;gap:14px')}
  </div>
</div>""")

    f8 = frame("9.8", "Get clients · Cold emails", f"""
{title("An email isn't a conversation.", 'Be specific in one message.', 96)}
<div class="abs" style="left:110px;top:420px;width:1000px">
  <div class="mock" style="padding:30px 36px">
    <div style="font:600 22px 'Plus Jakarta Sans';color:#4A5670;border-bottom:2px solid #E3E7EF;padding-bottom:10px">To: Joshua</div>
    <div style="font:700 24px 'Plus Jakarta Sans';border-bottom:2px solid #E3E7EF;padding:10px 0">Subject: Your video on 5 ways to get healthy</div>
    <div style="font:500 24px/1.5 'Plus Jakarta Sans';margin-top:14px">Good day, Joshua. I just saw your YouTube video about <b style="background:#FCDD9E;padding:0 6px">5 ways to get healthy</b>, and I love it. I noticed it isn't performing well. Do you have an editor? I feel your videos can perform better in this way, that way and this way. I would love to do a free edit for you. Let me know.</div>
  </div>
</div>
<div class="abs" style="left:1180px;top:330px;width:630px;display:flex;flex-direction:column;gap:20px">
  {demo('My real outreach email', 'Open my sent mail and show one I sent')}
  {rv(remember('Name the video. Not &ldquo;I saw your videos&rdquo; but &ldquo;your last video about…&rdquo;. Better: mention something from 10 minutes in.', head='The rule'), 'The rule')}
  <div class="cb">The more research you do on the person, the better the replies.</div>
</div>""")

    f9 = frame("9.9", "Get clients · Value first", f"""
{title("Don't wait to be offered a trial.", 'Edit their video first.', 100)}
<div class="abs" style="left:110px;top:420px;width:820px">
  {''.join(f'<div class="li" style="margin-bottom:16px">{icon(i, 40)}<span>{t}</span></div>' for i, t in [('download', 'Download one of their videos, <b>re-edit it and send it</b>. They see you already put in work.'), ('timer', '<b>30 seconds at most.</b> A full minute wastes your time: this one may say no.'), ('wand-sparkles', '<b>Pick a video you can visibly improve.</b> Don\'t add things that don\'t make sense to a well-edited one.'), ('send', 'Email it: <b>&ldquo;I did a free edit for you. Check it out.&rdquo;</b> Also post it on Twitter and tag them.')])}
  <div class="cb" style="font-size:22px">Downside: it takes time, and it sells how fancy your edit is, not everything else you bring.</div>
</div>
<div class="abs" style="left:1000px;top:330px;width:810px;display:flex;flex-direction:column;gap:18px">
  <div class="row" style="gap:16px">{ph('Clip: their original video (before)', 'height:330px;width:397px', src('vf_before'))}{ph('Clip: your value-first edit (after)', 'height:330px;width:397px', src('vf_after'))}</div>
  <div class="row" style="gap:16px;align-items:center"><div class="tag line">Before</div><div style="flex:1;height:4px;background:{SLATE}"></div><div class="tag gold">After</div></div>
  {remember('You need to learn to give value. They decide whether to post the free edit.')}
</div>""")

    f10 = frame("9.10", "Get clients · Loom: pitch yourself on video", f"""
{title('Pitch yourself on camera,', 'not in text.', 110)}
<div class="abs" style="left:110px;top:420px;width:820px">
  <div class="mock">
    <div style="padding:20px 30px;font:700 23px 'Plus Jakarta Sans';border-bottom:2px solid #E3E7EF">Subject: I recorded a video to explain some things for you</div>
    <div style="height:300px;background:#071226;position:relative;display:flex;align-items:center;justify-content:center">{icon('circle-play', 110, CH, 1.5)}<div style="position:absolute;right:20px;bottom:16px;font:700 22px 'Plus Jakarta Sans';color:#fff;background:rgba(0,0,0,.5);padding:4px 12px;border-radius:8px">2:41</div></div>
  </div>
</div>
<div class="abs" style="left:1000px;top:170px;width:810px;display:flex;flex-direction:column;gap:18px">
  {demo('My Loom account', 'Show a Loom pitch I sent')}
  {''.join(f'<div class="li" style="font-size:25px">{icon(i, 40)}<span>{t}</span></div>' for i, t in [('video', 'They see a <b>real person who took the trouble</b>. Most people now use AI to automate emails.'), ('layers', '<b>Stack it:</b> a value-first edit and a Loom together, or the edit first and a Loom as the follow-up.'), ('mail', '<b>Loom is for email.</b> In Instagram and Twitter DMs, send voice notes.'), ('link', 'Link your <b>best video</b>, not only your portfolio.')])}
  {rv(remember("They may not need you today, but they'll remember you tomorrow."), 'Why it works')}
</div>""")

    f11 = frame("9.11", "Get clients · Follow up, then close on a call", f"""
<div class="abs" style="left:110px;top:150px;width:840px">
  <div class="h">Follow up</div>
  <div class="row" style="gap:0;margin-top:26px;align-items:center">{''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px;width:168px"><div style="width:70px;height:70px;border-radius:50%;background:{CH if k == 4 else SLATE};display:flex;align-items:center;justify-content:center;font-family:Gloock;font-size:30px;color:{NAVY if k == 4 else CH}">{n}</div><div class="cb" style="font-size:21px;text-align:center">{t}</div></div>' for k, (n, t) in enumerate([('✉', 'your message'), ('1', '+24 hours'), ('2', '+2 days'), ('3', '+1 week'), ('4', 'stop at 4')]))}</div>
  <div class="bub me" style="max-width:100%;margin-top:26px">Hey, just checking whether you saw my last message. I would really love to know what you think.</div>
  <div class="bub me" style="max-width:100%;margin-top:14px">I realise you must be busy. But I really love your videos, and I still feel I can be of good help.</div>
  <div class="cb" style="margin-top:16px;font-size:23px">Be kind every time. Tick each one in your list. <b>My limit is 4</b>, because I have other people to reach.</div>
</div>
<div class="abs" style="left:1010px;top:150px;width:800px">
  <div class="h">Close on a video call</div>
  <div class="cb" style="margin-top:10px">On a chat I can tell you no and not care. On a call, before I say no, I'll reconsider.</div>
  <div class="chat" style="margin-top:18px">
    <div class="bub them">How much do you charge?</div>
    {rv('<div class="bub me" style="max-width:100%">Thank you very much, I can see you\'re interested. My price varies based on several factors, so before I tell you, I\'d love to know what you\'re trying to achieve, what business you run and your goal. Let\'s have a video call.</div><div class="bub me" style="margin-left:auto;display:flex;align-items:center;gap:12px;font-weight:700">' + icon('calendar', 30, NAVY, 2) + ' Book a time that suits you →</div>', "Don't give the price in DMs", 'display:flex;flex-direction:column;gap:14px')}
  </div>
</div>""")

    weak = [("megaphone", "\"Looking for a video editor\" posts", "About 80% scams. Replies flood in within minutes."), ("users-round", "Free communities, Discord", "Full of scammers. USD 2 edits, virus links."),
            ("briefcase", "Job sites", "One editor post can get about 5,000 applicants."), ("store", "Upwork and Fiverr", "If you're not the best there, you're the cheapest.")]
    parts = ["Good skill", "A strong personal brand", "A strong portfolio", "Outreach", "A network of editors"]
    f12 = frame("9.12", "Get clients · What actually works", f"""
<div class="abs" style="left:110px;top:150px;width:760px">
  <div class="h">The weakest routes</div>
  <div class="cb" style="margin-top:8px;font-size:23px">I used these. They didn't work for me. Know them, don't rely on them.</div>
  {''.join(f'<div class="card line" style="flex-direction:row;align-items:center;gap:20px;padding:18px 24px;margin-top:14px">{icon(i, 44, MIST)}<div><div class="ct" style="font-size:26px">{h}</div><div class="cb" style="font-size:21px">{b}</div></div></div>' for i, h, b in weak)}
</div>
<div class="abs" style="left:960px;top:150px;width:850px">
  <div class="h">What gets you clients, all at once</div>
  <div style="display:flex;flex-direction:column;gap:12px;margin-top:22px">
    {''.join(rv(f'<div class="card" style="flex-direction:row;align-items:center;gap:20px;padding:16px 26px"><div class="num" style="font-size:44px;width:30px">{k+1}</div><div class="ct" style="font-size:30px">{t}</div></div>', f'Piece {k+1}') for k, t in enumerate(parts))}
    <div class="card gold" style="flex-direction:row;align-items:center;gap:20px;padding:20px 26px">{icon('trophy', 50, NAVY, 2)}<div class="ct" style="font-size:34px">= Your first clients</div></div>
  </div>
  {remember("Don't rely on one means. Do it all consistently for one, two, three months, for many clients, and there's no way you will not land one.", 'margin-top:18px')}
</div>""")
    return [op, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]


ROWS = [("row08-seen", row8), ("row09-clients", row9)]
