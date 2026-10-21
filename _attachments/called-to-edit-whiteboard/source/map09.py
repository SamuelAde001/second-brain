"""Chapter 9 as a map: get clients. Demo stops: YouTube/Instagram search, my outreach email, my Loom."""
from maplib import *
from lib import rv, icon, remember, journey, doit, NAVY, CH, MIST

NAME, W = "map09-clients", 5400
P = {}


def b1():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">The people you reach out to</span><br>' + big("will check your page first.", 96)),
        row([col([L("i0", "Inbound · they come to you", "", "arrow-down-left", "gold"), bub("i1", "Hey, I saw your work. How much do you charge?", False, "A client")], 24, None, "flex:1"),
             col([L("i2", "Outbound · you go to them", "You see someone whose videos you could edit, and you reach out.", "arrow-up-right", "")], 24, None, "flex:1")], 120),
        L("i3", "Do both.", "Established editors get more inbound; beginners have to go looking. <b>If your page is empty, they won't even reply.</b>", "repeat", "navy"),
    ]
    edge("i0", "i2", "gold", sa="r", sb="l", label="+")
    return B(1, "9.1", "Two ways in", "arrow-left-right", items, "Inbound + outbound", "i0")


def b2():
    rs = [("Showing your work", "and how you came up with it", "eye"), ("The person behind it", "your personality. Specific makes you unique", "user"),
          ("Reliability", "clients are tired of flashy editors who miss deadlines. Document your day", "clock"),
          ("Credibility", "testimonials and the results your work brought", "badge-check"), ("Consistency", "not once a week. Every day", "calendar")]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">What makes a client DM you</span><br>' + big("instead of another editor?", 90)),
        row([col(steps("r", [(h, b, ic) for h, b, ic in rs], reveal=[f"Reason {k+1}" for k in range(5)], gap=40, num=True), 40, 1000),
             col([photo("r7", 0, 0, 660, 420, "Video: one of your working time-lapses", P.get("timelapse"), 1.5),
                  journey('A client scrolled my profile, saw my day-to-day time-lapses, and said: <b>&ldquo;This guy is locked in.&rdquo;</b>')], 40, 680)], 70),
        remember("There are a lot of clients looking for editors. You are invisible. That's why they can't find you."),
        note(0, 0, 1700, '<b>Be patient:</b> one, two, three months of consistency.'),
    ]
    return B(2, "9.2", "Inbound: make them come to you", "magnet", items, "Five reasons", "r0")


def b3():
    ring = ["Friends", "Family", "Colleagues making content", "People in your DMs", "Your contacts", "Editors you know"]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Start with people who</span><br>' + big("already know you.", 110)),
        row([col([chip(f"w{k}", 0, 0, t) for k, t in enumerate(ring[:3])], 30, 520, "align-items:flex-end;justify-content:center"),
             node("wy", 0, 0, 340, '<div class="spk" style="width:300px;height:300px">You</div>', "", "display:flex;justify-content:center"),
             col([chip(f"w{k+3}", 0, 0, t) for k, t in enumerate(ring[3:])], 30, 520, "justify-content:center")], 90, "justify-content:center"),
        note(0, 0, 1700, '<b>Warm outreach converts the fastest</b>, because they already know and trust you. My first client, my mentor, was warm. Even a relative who works in a bank may know someone.'),
        rv(remember("They want to see experience. They don't see knowledge."), "What clients want to see"),
        row([bub("w8", "Sir, I love your videos and I see what you do. I would love to help you out with your videos.", True, "To my mentor", "auto", "flex:1"),
             bub("w9", "I'm a video editor. Do you know anyone who needs my service?", True, "To anyone you know", "auto", "flex:1")], 40),
        doit("Do one warm outreach after tonight. Research who to reach first, then send it."),
    ]
    for k in range(3):
        edge("wy", f"w{k}", "gold", sa="l", sb="r", bend=0.3)
        edge("wy", f"w{k+3}", "gold", sa="r", sb="l", bend=0.3)
    return B(3, "9.3", "Warm outreach first", "flame", items, "People who know you")


def b4():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Go where your client is.</span><br>' + big("Find cold clients.", 110)),
        lab2("The three signs of a potential client"),
        row(steps("c", [("In your niche", "the videos you chose to edit", "target"), ("Makes money", "in some form, so they can afford you", "wallet"),
                        ("Needs an editor", "weak, badly edited or unedited videos", "scissors", "gold")], d="row", gap=80,
                  reveal=["Sign 1", "Sign 2", "Sign 3"], num=True), 80),
        note(0, 0, 1700, 'YouTube clients? <b>Search YouTube for creators in your niche.</b> Watch their videos. Scroll past the many who already have great editors. <b>Find their email</b> on the channel, then find them everywhere else and save example videos.'),
        demo_("cd", 0, 0, "auto", "Finding clients on YouTube and Instagram", "Search my niche live, check the three signs, find the email"),
        L("c9", "Agencies are clients too.", "Most post on Twitter and LinkedIn that they need an editor. Good for beginners.", "building-2", "navy"),
    ]
    edge("c2", "cd", "dash", sa="b", sb="t")
    return B(4, "9.4", "Find cold clients · DEMO", "search", items, "Three signs", "c0")


def b5():
    kv = [("Name", "Joshua"), ("Channel or handle", "@joshua_b2b"), ("Email", "from his YouTube About page"), ("Other platforms", "Instagram, LinkedIn, Twitter"),
          ("Content", "B2B SaaS explainers, long form"), ("Followers", "8,400"), ("Example videos", "3 links saved"), ("Follow-ups", "✓ 1   ✓ 2   ☐ 3   ☐ 4")]
    tbl = '<div class="mock"><div class="mh">One row of your list · Notion or a spreadsheet</div><div class="kv">' + "".join(f"<div>{a}</div><div>{b}</div>" for a, b in kv) + '</div><div style="margin-top:12px;color:#4A5670;font-size:20px">A made-up example row.</div></div>'
    tools = [("YouTube itself", "A channel's About page shows a business email. Free."), ("Channel Crawler", "Search channels by niche, country, subs. Emails paid."),
             ("TubeMailer", "Chrome extension for public business emails. Free to try."), ("Modash", "Creators on IG, TikTok, YouTube by niche and size."),
             ("AI agents", "Claude Code (I pay ~NGN 33,000 / USD 25 a month), Codex, Grok.")]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">The most important thing for every editor:</span><br>' + big("The dream client list.", 100)),
        row([node("d0", 0, 0, 1000, tbl, ""),
             col([rv(L("d1", big("20–50", 90, NAVY), "names to aim for", "", "gold"), "How many?"), rv(L("d2", big("100", 90), "mine: my dream 100, by hand", "", ""), "Mine?")], 30, 660)], 50),
        note(0, 0, 1700, '<b>Gathering leads, not reaching out yet.</b> Add every day. Keep two lists: <b>potential clients</b> and <b>clients you work with</b>.'),
        row([L(f"d{k+3}", h, b, "", "", "auto", "flex:1") for k, (h, b) in enumerate(tools[:3])], 24),
        row([L(f"d{k+6}", h, b, "", "", "auto", "flex:1") for k, (h, b) in enumerate(tools[3:])], 24),
    ]
    return B(5, "9.5", "The dream client list", "list", items, "Leads first", "d0")


def b6():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Before you reach out,</span><br>' + big("warm them up.", 110)),
        col(steps("u", [("Turn on notifications", "for the creator", "bell"), ("Be the first to comment", "say something genuinely good about what they teach", "message-circle"),
                        ("Do it on 4 or 5 posts", "especially smaller creators: they notice you", "repeat"),
                        ("They check your page", "see you're an editor, and may reach out first", "eye", "gold")],
                  reveal=["Step 1", "Step 2", "Step 3", "Step 4"], num=True), 56),
        lab2("Then reach them on every platform"),
        row(steps("v", [("Email", "", "mail"), ("Instagram DM", "", "instagram"), ("Twitter message", "", "twitter", "gold")], d="row", gap=90), 90),
        note(0, 0, 1700, 'I emailed each of my 100, then sent an Instagram DM, then a Twitter message. <b>By the third, they think: this person really means business.</b>'),
    ]
    return B(6, "9.6", "Warm them up first", "thermometer", items, "Before the pitch", "u0")


def b7():
    items = [
        lab2("Why most cold messages fail"),
        row([bub("m0", "Hey, my name is Samuel, I'm a video editor, and I'd love to work for you. Here's my portfolio.", True, "", 900, "opacity:.55"),
             note(0, 0, 700, '<b>Too cold.</b> You just want their money, and you show no interest in what they do.')], 50, "align-items:center"),
        note(0, 0, 1700, 'A question lowers their guard. There are a lot of scammers; <b>a curious, casual person is not one.</b> In DMs, <b>send voice notes.</b> People want to hear real humans. Send your picture and your portfolio too.'),
        lab2("Joshua · B2B SaaS creator · example"),
        col([bub("m1", "Hi Joshua. I saw your video about B2B SaaS. That was a wonderful video, I learned a lot from it. How do you make these videos?", True, "1 · Open with a question, not a pitch", 1300, "align-self:flex-end"),
             bub("m2", "Thanks! I record them myself and edit when I find time.", False, "Joshua", 1000),
             rv(bub("m3", "These videos are nice, but do they bring you clients? Some aren't performing, and they have high potential. Do you have an editor?", True, "2 · Steer to a problem", 1300), "Step 2", "align-self:flex-end"),
             bub("m4", "Not really. Not many customers from them yet.", False, "Joshua", 1000),
             rv(bub("m5", "I'm a video editor and I can help you make videos that bring better customers. Can I edit one or two videos for you for free, so we see how they perform?", True, "3 · Pitch, with value first", 1300), "Step 3", "align-self:flex-end")], 26),
    ]
    return B(7, "9.7", "Cold DMs: talk first, pitch later", "message-circle", items, "Question, problem, pitch")


def b8():
    mail = ('<div class="mock"><div class="mh">To: Joshua · Subject: Your video on 5 ways to get healthy</div>'
            'Good day, Joshua. I just saw your YouTube video about <b>5 ways to get healthy</b>, and I love it. I noticed it isn\'t performing well. Do you have an editor? '
            'I feel your videos can perform better in this way, that way and this way. I would love to do a free edit for you. Let me know.</div>')
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">An email isn\'t a conversation.</span><br>' + big("Be specific in one message.", 92)),
        node("e0", 0, 0, "auto", mail, ""),
        demo_("ed", 0, 0, "auto", "My real outreach email", "Open my sent mail and show one I sent"),
        rv(L("e1", "The rule: name the video.", "Not &ldquo;I saw your videos&rdquo; but &ldquo;your last video about…&rdquo;. Better: mention something from 10 minutes in.", "target", "gold"), "The rule"),
        note(0, 0, 1700, '<b>The more research you do on the person, the better the replies.</b>'),
    ]
    edge("e0", "ed", "dash", sa="b", sb="t")
    return B(8, "9.8", "Cold emails · DEMO", "mail", items, "One specific message", "e0")


def b9():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Don\'t wait to be offered a trial.</span><br>' + big("Edit their video first.", 100)),
        row(steps("f", [("Download one of their videos", "", "download"), ("Re-edit it", "30 seconds at most. A full minute wastes your time: this one may say no.", "scissors"),
                        ("Send it", "&ldquo;I did a free edit for you. Check it out.&rdquo; Also post it on Twitter and tag them.", "send", "gold")], d="row", gap=80, num=True), 80),
        L("f8", "Pick a video you can visibly improve.", "Don't add things that don't make sense to a well-edited one.", "eye", "navy"),
        row([photo("f6", 0, 0, 800, 400, "Clip: their original video (before)", P.get("before"), -1.5), photo("f7", 0, 0, 800, 400, "Clip: your value-first edit (after)", P.get("after"), 1.5)], 70),
        note(0, 0, 1700, '<b>Downside:</b> it takes time, and it sells how fancy your edit is, not everything else you bring.'),
        remember("You need to learn to give value. They decide whether to post the free edit."),
    ]
    edge("f6", "f7", "gold", sa="r", sb="l", label="before → after")
    return B(9, "9.9", "Value first", "gift", items, "Edit before you ask", "f0")


def b10():
    loom = ('<div class="mock"><div class="mh">Subject: I recorded a video to explain some things for you</div>'
            '<div style="height:300px;border-radius:14px;background:#0A1F44;display:flex;align-items:center;justify-content:center;position:relative">'
            f'{icon("circle-play", 110, CH, 1.6)}<span style="position:absolute;right:18px;bottom:14px;color:#fff;font:800 22px \'Plus Jakarta Sans\'">2:41</span></div></div>')
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Pitch yourself on camera,</span><br>' + big("not in text.", 110)),
        row([node("o0", 0, 0, 760, loom, ""),
             col([demo_("od", 0, 0, "auto", "My Loom account", "Show a Loom pitch I sent"),
                  rv(L("o1", "Why it works", "They see a <b>real person who took the trouble</b>. Most people now use AI to automate emails.", "user-round-check", "gold"), "Why it works")], 30, 880)], 60),
        L("o2", "Stack it", "A value-first edit and a Loom together, or the edit first and a Loom as the follow-up.", "layers", ""),
        L("o3", "Loom is for email.", "In Instagram and Twitter DMs, send voice notes. Link your <b>best video</b>, not only your portfolio.", "mail", "dim"),
        remember("They may not need you today, but they'll remember you tomorrow."),
    ]
    edge("o0", "od", "dash", sa="r", sb="l")
    return B(10, "9.10", "Loom: pitch yourself on video · DEMO", "video", items, "On camera", "o0")


def b11():
    items = [
        lab2("Follow up"),
        row(steps("g", [("Your message", "", "send"), ("+24 hours", "", "clock"), ("+2 days", "", "clock"), ("+1 week", "", "clock"), ("Stop at 4", "", "octagon-x", "gold")], d="row", gap=50), 50),
        row([bub("g7", "Hey, just checking whether you saw my last message. I would really love to know what you think.", True, "", "auto", "flex:1"),
             bub("g8", "I realise you must be busy. But I really love your videos, and I still feel I can be of good help.", True, "", "auto", "flex:1")], 40),
        note(0, 0, 1700, 'Be kind every time. Tick each one in your list. <b>My limit is 4</b>, because I have other people to reach.'),
        lab2("Close on a video call"),
        quote_(0, 0, 1700, "On a chat I can tell you no and not care. On a call, before I say no, I'll reconsider.", 52),
        bub("g9", "How much do you charge?", False, "The client", "fit-content"),
        rv(bub("g10", "Thank you very much, I can see you're interested. My price varies based on several factors, so before I tell you, I'd love to know what you're trying to achieve, what business you run and your goal. Let's have a video call.<br><b>Book a time that suits you →</b>", True, "You", 1400, "align-self:flex-end"), "Don't give the price in DMs", "align-self:flex-end"),
    ]
    return B(11, "9.11", "Follow up, then close on a call", "phone-call", items, "Four touches, then a call", "g0")


def b12():
    weak = [("&ldquo;Looking for a video editor&rdquo; posts", "About 80% scams. Replies flood in within minutes."), ("Free communities, Discord", "Full of scammers. USD 2 edits, virus links."),
            ("Job sites", "One editor post can get about 5,000 applicants."), ("Upwork and Fiverr", "If you're not the best there, you're the cheapest.")]
    items = [
        lab2("The weakest routes · I used these. They didn't work for me."),
        row([L(f"x{k}", h, b, "circle-x", "dim", "auto", "flex:1") for k, (h, b) in enumerate(weak[:2])], 24),
        row([L(f"x{k+2}", h, b, "circle-x", "dim", "auto", "flex:1") for k, (h, b) in enumerate(weak[2:])], 24),
        lab2("What gets you clients, all at once"),
        row(steps("y", [("Good skill", "", "scissors"), ("A strong personal brand", "", "user-round-check"), ("A strong portfolio", "", "folder-open"),
                        ("Outreach", "", "send"), ("A network of editors", "", "users")], d="row", gap=40,
                  reveal=[f"Piece {k+1}" for k in range(5)], kind="mist"), 40),
        L("y9", big("= Your first clients", 80, NAVY), "", "", "gold"),
        remember("Don't rely on one means. Do it all consistently for one, two, three months, for many clients, and there's no way you will not land one."),
    ]
    for k in range(5):
        edge(f"y{k}", "y9", "gold", sa="b", sb="t", bend=0.3)
    return B(12, "9.12", "What actually works", "puzzle", items, "All of it, at once")


TOC = [("9.1", "Two ways in"), ("9.2", "Inbound: make them come to you"), ("9.3", "Warm outreach first"), ("9.4", "Find cold clients · DEMO"),
       ("9.5", "The dream client list"), ("9.6", "Warm them up first"), ("9.7", "Cold DMs: talk first, pitch later"), ("9.8", "Cold emails · DEMO"),
       ("9.9", "Value first"), ("9.10", "Loom · DEMO"), ("9.11", "Follow up, then close on a call"), ("9.12", "What actually works")]


def build():
    reset()
    body = assemble("9", "Get", "Clients", "Skill, a strong personal brand, a strong portfolio, outreach and a network of editors. Done together, consistently.",
                    "Getting clients is a lot of hard work. That's the truth.",
                    [b1(), b2(), b3(), b4(), b5(), b6(), b7(), b8(), b9(), b10(), b11(), b12()], TOC,
                    ("NEXT · CHAPTER 10", "Price yourself and get paid"))
    return body, W, None
