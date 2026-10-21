"""Chapter 8 as a map: get seen. Demo stops: my Twitter, my portfolio."""
from maplib import *
from lib import rv, icon, remember, journey, doit, NAVY, CH, MIST

NAME, W = "map08-seen", 5400
P = {}


def b1():
    items = [
        L("a0", "The question my mentor asked me", '<span style="font-family:Gloock;font-size:44px;line-height:1.15;color:#FCDD9E">&ldquo;Where can people find you? When they need you, where can they see your work?&rdquo;</span>', "message-circle", "navy"),
        note(0, 0, 1700, 'I had nowhere to show it. So I opened <b>brand-new Twitter, LinkedIn and Instagram</b> accounts and did two things.'),
        row([rv(L("a1", "1 · I curated my feed", "Searched &ldquo;video editors&rdquo; and followed every major editor: about 50 on Twitter. My feed fed me editing all day.", "rss", "", "auto", "flex:1"), "Thing 1", "flex:1;display:flex"),
             rv(L("a2", "2 · I posted my work", "Recorded myself working, photographed my timeline, screenshotted my day. <b>No less than 3 times a day.</b>", "camera", "gold", "auto", "flex:1"), "Thing 2", "flex:1;display:flex")], 40),
        row([photo("a3", 0, 0, 760, 380, "Photo: your phone recording you at work / your timeline post", P.get("atwork"), -1.5),
             col([remember("Showing your work is your leverage."),
                  note(0, 0, 820, 'For your first month, <b>lock in</b>: all your social media about editing, especially your niche. A secret most people don\'t know.')], 30, 860)], 60),
    ]
    edge("a0", "a1", "gold", sa="b", sb="t")
    edge("a0", "a2", "gold", sa="b", sb="t")
    return B(1, "8.1", "Where can people find you?", "search", items, "My mentor's question", "a0")


def b2():
    pl = [("Twitter (X) &amp; LinkedIn", "Best for beginners", "Agencies and clients search here. Low effort: text and screenshots, no face needed.", "Mostly international agencies and companies.", "twitter", "gold"),
          ("Instagram", "Big if you put in the work", "Personal brand and a mini portfolio at once. Your face, your voice, editing your own videos.", "A mix of international and Nigerian.", "instagram", ""),
          ("TikTok", "Personal brand", "Your face and your story, like Instagram.", "Lots of DMs from people near me, in Nigeria.", "music-2", ""),
          ("Facebook", "Not for this", "One of the worst places to build a brand as an editor.", "Low-paying, frustrating clients.", "facebook", "dim")]
    cards = [L(f"b{k}", f'{h} · ' + rv(f'<span>{v}</span>', "Verdict?", "display:inline-block"), f"{d}<br><b>Where I got clients:</b> {w}", ic, cls, "auto", "flex:1")
             for k, (h, v, d, w, ic, cls) in enumerate(pl)]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Pick one platform.</span><br>' + big("Own it.", 120)),
        row(cards[:2], 30), row(cards[2:], 30),
        note(0, 0, 1700, '<b>Become the known person for your niche there.</b> Two platforms if you have the capacity. Who you engage shapes who finds you. I\'ve now moved from Twitter to Instagram to build my authority.'),
    ]
    return B(2, "8.2", "Pick one platform and own it", "layout-grid", items, "One platform, owned")


def b3():
    pts = [("Your face", "People trust who they can see."), ("Name + what you do", ""), ("Bio = your offer", "Chapter 4"),
           ("Clients you've edited for", ""), ("Portfolio link, always", ""), ("Pinned post = your best edit", ""), ("A good banner", "")]
    mock = node("pm", 0, 0, 640, '<div class="mock" style="padding:0;overflow:hidden"><div style="height:150px;background:#1E3150;color:#B9C3D6;display:flex;align-items:center;justify-content:center;font:800 22px \'Plus Jakarta Sans\';letter-spacing:.14em">BANNER</div>'
                '<div style="padding:0 30px 30px"><div style="width:130px;height:130px;border-radius:50%;background:#B9C3D6;border:6px solid #F4F6FA;margin-top:-65px"></div>'
                '<div style="font:800 32px \'Plus Jakarta Sans\';margin-top:10px">Samuel Adebayo</div><div style="font:700 24px \'Plus Jakarta Sans\';color:#4A5670">Long-form video editor</div>'
                '<div style="margin-top:12px">I help business owners get their first 10,000 views in 3 videos.</div><div style="margin-top:8px;color:#4A5670">Edited for: [your clients]</div>'
                '<div style="margin-top:8px;color:#8A5E17;font-weight:700">yourportfolio.site</div>'
                '<div style="margin-top:18px;border:3px dashed #B9C3D6;border-radius:14px;padding:16px;font-weight:700">📌 Pinned · My best edit</div></div></div>', "", "")
    lst = [rv(L(f"pp{k}", f'<span style="font-family:Gloock;color:#FCDD9E;font-size:40px;margin-right:12px">{k+1}</span>{h}', b, "", ""), f"Point {k+1}") for k, (h, b) in enumerate(pts)]
    items = [
        row([mock, col(lst, 18, 1060)], 90),
        L("p9", "A lot of us hide ourselves. Show your face, often.", "Pin the edit you're proudest of so the first impression is &ldquo;this person is a professional.&rdquo;", "eye", "gold"),
    ]
    edge("pm", "pp0", "line", sa="r", sb="l", bend=0.3)
    return B(3, "8.3", "Build your profile", "user-round", items, "Seven points", "pm")


def b4():
    types = [("A normal day", "You working, you on a call with a client."), ("Your story", "My soldier-to-editor story hits every single time."),
             ("Struggles", "A client who turned you down."), ("Wins", "A new client, a new laptop."), ("Challenges", "&ldquo;Day one of trying to get my first client. Day two…&rdquo;")]
    mix = (f'<div style="display:flex;height:120px;border-radius:20px;overflow:hidden;font:800 30px \'Plus Jakarta Sans\'">'
           f'<div style="flex:40;background:#FCDD9E;color:#0A1F44;padding:18px 24px">40% authentic<div style="font:600 22px \'Plus Jakarta Sans\'">builds emotion</div></div>'
           f'<div style="flex:40;background:#B9C3D6;color:#0A1F44;padding:18px 24px">40% authority<div style="font:600 22px \'Plus Jakarta Sans\'">proves you know</div></div>'
           f'<div style="flex:20;background:#1E3150;color:#fff;padding:18px 24px">20% sales<div style="font:600 22px \'Plus Jakarta Sans\'">pitches you</div></div></div>')
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">This is the AI age.</span><br>' + big("Be a real human.", 110)),
        note(0, 0, 1700, 'People copy posts and generate them with AI. Clients need to know you\'re genuine. <b>Post your life around video editing, and nothing else for now.</b>'),
        row([L(f"c{k}", h, b, "", "", "auto", "flex:1") for k, (h, b) in enumerate(types[:3])], 24),
        row([L(f"c{k+3}", h, b, "", "", "auto", "flex:1") for k, (h, b) in enumerate(types[3:])], 24),
        row([note(0, 0, 360, big("2–3", 110) + '<br><b>posts a day</b>'), col([rv(node("c9", 0, 0, "auto", mix, ""), "The post mix")], 0, 1300, "justify-content:center")], 40, "align-items:center"),
        row([photo("c7", 0, 0, 800, 400, "Screenshot: a post that landed you a client", P.get("tweetclient1"), -1.5),
             photo("c8", 0, 0, 800, 400, "Screenshot: another post that landed a client", P.get("tweetclient2"), 1.5)], 70),
        demo_("cd", 0, 0, "auto", "My Twitter: the posts that landed me clients", "Open x.com, scroll my old editing posts"),
        row([note(0, 0, 400, big("700", 150)), note(0, 0, 1200, '<b style="font-size:34px">followers on Twitter. That\'s all I had.</b><br>The best clients I needed came from those 700. I posted 3 times a day for 60 days.')], 40, "align-items:center"),
    ]
    edge("c8", "cd", "dash", sa="b", sb="t")
    return B(4, "8.4", "Build a personal brand", "user-round-check", items, "Be a real human")


def b5():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">A link in your bio.</span><br>' + big("Your portfolio.", 110)),
        row([L("f0", "A shared drive folder", "Click. Wait. Click. They go to another editor.", "folder-open", "dim", "auto", "flex:1"),
             rv(L("f1", "A simple website", "They just watch. That is all a client wants.", "globe", "gold", "auto", "flex:1"), "The best portfolio", "flex:1;display:flex")], 90),
        lab2("Build it with AI, in one night"),
        row(steps("g", [("Upload your edits to YouTube as unlisted videos", "", "upload"), ("Copy the links", "", "link"),
                        ("Paste into an AI", "&ldquo;These are the videos I edited. Use them to create a portfolio I can link in my bio.&rdquo;", "bot", "gold")], d="row", gap=70, num=True), 70),
        row([photo("f7", 0, 0, 820, 420, "Screenshot: your Framer portfolio site", P.get("portfolio"), -1.5),
             col([demo_("fd", 0, 0, "auto", "My portfolio site", "Built on Framer in one night. It got me clients."),
                  L("f2", "Framer (mine)", "Free on a Framer address. Best looking.", "", "gold"), L("f3", "Canva Websites", "Free on a Canva address. Easiest.", "", ""),
                  L("f4", "Carrd", "Up to 3 one-page sites free. Simplest.", "", "")], 24, 820)], 60),
    ]
    edge("f0", "f1", "gold", sa="r", sb="l", label="vs")
    return B(5, "8.5", "Your portfolio", "globe", items, "A link in your bio")


def b6():
    items = [
        row([note(0, 0, 300, big("8", 280)), note(0, 0, 1350, '<span style="font:800 44px/1.2 \'Plus Jakarta Sans\';color:#fff">videos at most:</span><br><b>your top 4 and your other 4.</b> Only have 3? Put the 3. Too many gives the client too much work.')], 40, "align-items:center"),
        row([L("h0", "Before and afters", "", "columns-2", "", "auto", "flex:1"), L("h1", "Testimonials", "Screenshots of what clients said.", "message-square-quote", "", "auto", "flex:1")], 24),
        row([L("h2", "Results", "Screenshots of what you got for clients.", "chart-column", "", "auto", "flex:1"), L("h3", "About you", "Who you are, how long you've edited.", "user", "", "auto", "flex:1")], 24),
        rv(quote_(0, 0, 1700, "Your practice work is your work.", 76), "I repeat…"),
        note(0, 0, 1700, 'No clients yet? Free work and practice on real people\'s videos count: their footage, your edit. Recreations stay practice. Replace them with real projects as they come.'),
        L("h4", "Look the part.", "Pick brand colours and stick to them. Mine was green. I use Canva for banners.", "palette", "navy"),
        doit("For the next month: curate your feed around your niche, fix your profile with the 7 points, build a simple portfolio site, and post 2 to 3 times a day."),
    ]
    return B(6, "8.6", "What goes in it", "folder-open", items, "Eight at most")


TOC = [("8.1", "Where can people find you?"), ("8.2", "Pick one platform and own it"), ("8.3", "Build your profile"),
       ("8.4", "Build a personal brand · DEMO"), ("8.5", "Your portfolio · DEMO"), ("8.6", "What goes in it")]


def build():
    reset()
    body = assemble("8", "Get", "Seen", "No one who learns from me succeeds without visibility. Pick one platform, show who you help, and post every day.",
                    "You can't succeed in this industry if you are hidden.", [b1(), b2(), b3(), b4(), b5(), b6()], TOC,
                    ("NEXT · CHAPTER 9", "Get clients"))
    return body, W, None
