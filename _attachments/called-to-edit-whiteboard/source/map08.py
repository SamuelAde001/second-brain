"""Chapter 8 as a map: get seen. Demo stops: my Twitter, my portfolio."""
from maplib import *
from lib import rv, icon, remember, journey, doit, NAVY, CH, MIST

NAME, W = "map08-seen", 5400
P = {}


def b1():
    items = [
        L("a0", "The question my mentor asked me", '<span style="font-family:Gloock;font-size:44px;line-height:1.15;color:#FCDD9E">&ldquo;Where can people find you? When they need you, where can they see your work?&rdquo;</span>', "message-circle", "navy"),
        note(0, 0, 1700, 'And I didn\'t have a place to show it. So I opened <b>a brand new Twitter, a brand new LinkedIn, a brand new Instagram.</b> And I did two things.'),
        row([rv(L("a1", "First, I curated my feed", "I searched video editors and followed every major one I could see. Like 50 on Twitter. I wanted my feed to constantly feed me video editing.", "rss", "", "auto", "flex:1"), "Thing 1", "flex:1;display:flex"),
             rv(L("a2", "Then I started posting my work", "I'd set my phone to record me working. Pictures of my timeline, screenshots of everything I did in a day. <b>Nothing less than 3 times a day.</b>", "camera", "gold", "auto", "flex:1"), "Thing 2", "flex:1;display:flex")], 40),
        row([photo("a3", 0, 0, 760, 380, "Photo: your phone recording you at work / your timeline post", P.get("atwork"), -1.5),
             col([remember("Showing your work is your leverage."),
                  note(0, 0, 820, 'A secret most people don\'t know: if you want to build something around a niche, <b>surround yourself with that niche.</b> For the next month, lock in.')], 30, 860)], 60),
        note(0, 0, 1700, 'Video editing is a visible kind of skill. <b>Your work is your selling point. That\'s your marketing, that\'s your advert.</b> No matter how good you are, you need to announce to the world what you do.'),
    ]
    return B(1, "8.1", "Where can people find you?", "search", items, "My mentor's question", "a0")


def b2():
    pl = [("Twitter (X) &amp; LinkedIn", "Best for beginners", "Agencies and clients search for video editors here. It's easy: screenshot your edit, post it, go. You don't need to show your face.", "Mostly international clients, agencies and companies.", "twitter", "gold"),
          ("Instagram", "Huge, if you put in the work", "You build your personal brand and your portfolio at once. But you need to show your face and edit your own videos.", "A mix of international and Nigerian clients.", "instagram", ""),
          ("TikTok", "Personal brand", "Like Instagram, you need to show your face.", "A lot of Nigerian DMs.", "music-2", ""),
          ("Facebook", "Don't even", "One of the worst places to build a personal brand as a video editor.", "Low ticket clients and frustrating clients.", "facebook", "dim")]
    cards = [L(f"b{k}", f'{h} · ' + rv(f'<span>{v}</span>', "Verdict?", "display:inline-block"), f"{d}<br><b>Where I got clients:</b> {w}", ic, cls, "auto", "flex:1")
             for k, (h, v, d, w, ic, cls) in enumerate(pl)]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Pick one platform and focus on it.</span><br>' + big("Be the known person there.", 100)),
        row(cards[:2], 30), row(cards[2:], 30),
        note(0, 0, 1700, 'When I started, I focused on only Twitter. LinkedIn was my backup: everything I posted on Twitter, I reposted there. Twitter was my home. <b>If you\'re a real estate editor, be the best real estate editor that can be found on Twitter.</b> Now I\'ve moved to Instagram to build my authority.'),
    ]
    return B(2, "8.2", "Pick one platform", "layout-grid", items, "And focus on it")


def b3():
    pts = [("Your face", "People trust who they can see."), ("Your name and what you do", "Samuel Adebayo, long form video editor."), ("Your bio carries your offer", "I help who, get what result, in what time, through how."),
           ("Clients you've edited for", "Simple tags of who you've worked with."), ("A link to your portfolio", "Where can they see all your work at once?"), ("Your pinned post is your best edit", "The edit you're proudest of."), ("A good banner", "On LinkedIn and Twitter.")]
    mock = node("pm", 0, 0, 640, '<div class="mock" style="padding:0;overflow:hidden"><div style="height:150px;background:#1E3150;color:#B9C3D6;display:flex;align-items:center;justify-content:center;font:800 22px \'Plus Jakarta Sans\';letter-spacing:.14em">BANNER</div>'
                '<div style="padding:0 30px 30px"><div style="width:130px;height:130px;border-radius:50%;background:#B9C3D6;border:6px solid #F4F6FA;margin-top:-65px"></div>'
                '<div style="font:800 32px \'Plus Jakarta Sans\';margin-top:10px">Samuel Adebayo</div><div style="font:700 24px \'Plus Jakarta Sans\';color:#4A5670">Long-form video editor</div>'
                '<div style="margin-top:12px">I help business owners get their first 10,000 views in 3 videos.</div><div style="margin-top:8px;color:#4A5670">Edited for: [your clients]</div>'
                '<div style="margin-top:8px;color:#8A5E17;font-weight:700">yourportfolio.site</div>'
                '<div style="margin-top:18px;border:3px dashed #B9C3D6;border-radius:14px;padding:16px;font-weight:700">Pinned · My best edit</div></div></div>', "", "")
    lst = [rv(L(f"pp{k}", f'<span style="font-family:Gloock;color:#FCDD9E;font-size:40px;margin-right:12px">{k+1}</span>{h}', b, "", ""), f"Point {k+1}") for k, (h, b) in enumerate(pts)]
    items = [
        row([mock, col(lst, 18, 1060)], 90),
        L("p9", "A lot of us hide ourselves", "If you want to succeed in this field, you need to show yourself. When people come to your profile, their first impression should be: <b>&ldquo;This guy is a professional.&rdquo;</b>", "eye", "gold"),
    ]
    edge("pm", "pp0", "line", sa="r", sb="l", bend=0.3)
    return B(3, "8.3", "Build your profile", "user-round", items, "What people see first", "pm")


def b4():
    types = [("A normal day", "A picture of you working, you talking with a client."), ("Your story", "I quit the military to focus on video editing. That story hits as a banger every single time."),
             ("Your struggles", "You tried to land a client and the client bounced you. Talk about it."), ("Your wins", "&ldquo;I just landed a new client. I bought a new laptop.&rdquo;"), ("Challenge yourself", "&ldquo;Day one of trying to get my first client. Day two…&rdquo;")]
    mix = (f'<div style="display:flex;height:120px;border-radius:20px;overflow:hidden;font:800 30px \'Plus Jakarta Sans\'">'
           f'<div style="flex:40;background:#FCDD9E;color:#0A1F44;padding:18px 24px">40% authentic<div style="font:600 22px \'Plus Jakarta Sans\'">builds emotion</div></div>'
           f'<div style="flex:40;background:#B9C3D6;color:#0A1F44;padding:18px 24px">40% authority<div style="font:600 22px \'Plus Jakarta Sans\'">proves you know</div></div>'
           f'<div style="flex:20;background:#1E3150;color:#fff;padding:18px 24px">20% sales<div style="font:600 22px \'Plus Jakarta Sans\'">pitches you</div></div></div>')
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">This is the AI age.</span><br>' + big("People need to know you're real.", 100)),
        note(0, 0, 1700, 'A lot of people are copying other people\'s posts, using ChatGPT to generate them. <b>Post your life around video editing.</b> Don\'t start posting politics or football. Not right now.'),
        row([L(f"c{k}", h, b, "", "", "auto", "flex:1") for k, (h, b) in enumerate(types[:3])], 24),
        row([L(f"c{k+3}", h, b, "", "", "auto", "flex:1") for k, (h, b) in enumerate(types[3:])], 24),
        row([note(0, 0, 360, big("2 to 3", 100) + '<br><b>posts a day</b>'), col([rv(node("c9", 0, 0, "auto", mix, ""), "The post mix")], 0, 1300, "justify-content:center")], 40, "align-items:center"),
        note(0, 0, 1700, 'Authority post: <b>&ldquo;Business owners, these are the mistakes you make in your videos.&rdquo;</b> Sales post: <b>&ldquo;Hey, I\'m a video editor and I\'m looking for a new business client.&rdquo;</b>'),
        row([photo("c7", 0, 0, 800, 400, "Screenshot: a post that landed you a client", P.get("tweetclient1"), -1.5),
             photo("c8", 0, 0, 800, 400, "Screenshot: another post that landed a client", P.get("tweetclient2"), 1.5)], 70),
        demo_("cd", 0, 0, "auto", "My Twitter: the posts that landed me clients", "Open x.com, scroll my old editing posts"),
        row([note(0, 0, 400, big("700", 150)), note(0, 0, 1200, '<b style="font-size:34px">followers on Twitter. That\'s all I had.</b><br>But those 700 followers got me the best clients I needed. You just need to show you\'re real. I posted 3 times a day for 60 days.')], 40, "align-items:center"),
    ]
    edge("c8", "cd", "dash", sa="b", sb="t")
    return B(4, "8.4", "Build a personal brand", "user-round-check", items, "Show people you're real")


def b5():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">A new client can\'t start scrolling all your posts to find your work.</span><br>' + big("Put your portfolio in your bio.", 96)),
        row([L("f0", "Google Drive", "I go against it. The client has to click every video to watch it. Too much friction, and they'll go to another editor.", "folder-open", "dim", "auto", "flex:1"),
             rv(L("f1", "A website", "They easily see your videos without opening files and folders. Always try and have a website.", "globe", "gold", "auto", "flex:1"), "The best portfolio", "flex:1;display:flex")], 90),
        lab2("AI can literally build it for you"),
        row(steps("g", [("Upload your edits to YouTube as hidden videos", "", "upload"), ("Copy the links", "", "link"),
                        ("Paste into an AI", "&ldquo;These are the videos I edited. Use them to create a portfolio I can link in my bio.&rdquo;", "bot", "gold")], d="row", gap=70, num=True), 70),
        note(0, 0, 1700, 'You don\'t need a web designer. You don\'t need a perfect website that looks aesthetically clean. <b>What the client wants to see is your videos.</b>'),
        row([photo("f7", 0, 0, 820, 420, "Screenshot: your Framer portfolio site", P.get("portfolio"), -1.5),
             col([demo_("fd", 0, 0, "auto", "My portfolio site", "I sat down one night and built it on Framer. It got me clients."),
                  L("f2", "Framer", "What I used. Free on a Framer address.", "", "gold"), L("f3", "Canva Websites", "Free on a Canva address. Easiest.", "", ""),
                  L("f4", "Carrd", "Up to 3 one-page sites free. Simplest.", "", "")], 24, 820)], 60),
    ]
    edge("f0", "f1", "gold", sa="r", sb="l", label="vs")
    return B(5, "8.5", "Your portfolio", "globe", items, "A link in your bio")


def b6():
    items = [
        row([note(0, 0, 300, big("8", 280)), note(0, 0, 1350, '<span style="font:800 44px/1.2 \'Plus Jakarta Sans\';color:#fff">videos, not more.</span><br>Your best 8: <b>your top 4 and your other 4.</b> If you\'ve only done 3 videos, fine, put those 3. Don\'t give the client too much work.')], 40, "align-items:center"),
        row([L("h0", "Before and afters", "", "columns-2", "", "auto", "flex:1"), L("h1", "Testimonials", "Screenshots of what clients said.", "message-square-quote", "", "auto", "flex:1")], 24),
        row([L("h2", "Results", "Screenshots of results you've gotten for clients.", "chart-column", "", "auto", "flex:1"), L("h3", "About you", "Introduce yourself. Who you are, how long you've been working.", "user", "", "auto", "flex:1")], 24),
        rv(quote_(0, 0, 1700, "Your practice work is your work.", 76), "I repeat…"),
        note(0, 0, 1700, 'No clients yet? Put the free work you\'ve done for people. <b>The footage belongs to them, but the edit is yours.</b> Recreations are mostly practice, you can\'t really call them your own. As you start doing real projects, replace them.'),
        L("h4", "Package yourself", "Have colours you use in your brand. Back in the day, mine was green. I subscribed to Canva so I could make nice banners.", "palette", "navy"),
        doit("For the next month: curate your feed around your niche. Fix your profile. Build your portfolio website. Post 2 to 3 times a day."),
    ]
    return B(6, "8.6", "What goes in it", "folder-open", items, "Your best 8, not more")


TOC = [("8.1", "Where can people find you?"), ("8.2", "Pick one platform"), ("8.3", "Build your profile"),
       ("8.4", "Build a personal brand · DEMO"), ("8.5", "Your portfolio · DEMO"), ("8.6", "What goes in it")]


def build():
    reset()
    body = assemble("8", "Get", "Seen", "No one that learns from me will succeed if they don't do visibility. Pick one platform, show your work, and post every day.",
                    "You can't succeed in this industry if you are hidden.", [b1(), b2(), b3(), b4(), b5(), b6()], TOC,
                    ("NEXT · CHAPTER 9", "Get clients"))
    return body, W, None
