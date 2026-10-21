"""Chapter 1 as a map: My story, a timeline of photos from soldier to editor."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map01-story", 5400
P = {}  # photo sources by slot key, filled from photos.json


def ph(nid, key, label, w=420, h=320, tilt=0):
    return photo(nid, 0, 0, w, h, label, P.get(key), tilt)


def b1():
    items = [
        row([ph("p1", "uniform", "Photo: you in uniform, 2020", 400, 340, -2),
             ph("p2", "minecraft", "Screenshot: your Minecraft YouTube channel", 400, 340, 1.5),
             L("l1", "A laptop + free software", "So I found <b>DaVinci Resolve</b>.", "laptop", "", 420),
             L("l2", "Later: editing for my church", "Still a hobby. Still a soldier.", "church", "dim", 420)], 60),
        quote_(0, 0, 1700, "If I had known CapCut then, I might have started there. I'm glad I started with Resolve.", 50),
    ]
    chain(["p1", "p2", "l1", "l2"], "gold", sa="r", sb="l", bend=0.3)
    return B(1, "1.1", "It started as a hobby", "gamepad-2", items, "2020 · COVID · still a soldier", "p1")


def b2():
    items = [
        L("m0", "&ldquo;What can I do better than just being a soldier?&rdquo;", "I offered to edit my mentor's YouTube videos. <b>For free.</b> I only knew how to cut. My laptop cost a whole month's salary: decent, but laggy. It was enough.", "handshake", "navy"),
        lab2("My first three edits for my mentor"),
        row([L("e0", "Edit 1 · Rejected", "&ldquo;I can't use this.&rdquo;", "circle-x", "dim", "auto", "flex:1"),
             rv(L("e1", "Edit 2 · Not yet", "Back to YouTube to learn more.", "refresh-cw", "", "auto", "flex:1"), "Edit 2?", "flex:1;display:flex"),
             rv(L("e2", "Edit 3 · Uploaded", "It went live on his channel.", "circle-check", "gold", "auto", "flex:1"), "Edit 3?", "flex:1;display:flex")], 70),
        row([L("m1", "NGN 25,000 a month", "for data and expenses, about 4 videos a month. <b>For two years.</b>", "wallet", "", 860),
             ph("p3", "mentor", "Photo: your mentor's channel", 380, 220, 2)], 40),
        remember("I learned from tutorials I watched to deliver a video that was going live, not to practise."),
    ]
    chain(["e0", "e1", "e2"], "gold", sa="r", sb="l", bend=0.3)
    return B(2, "1.2", "The best move I made", "sparkles", items, "A few years later", "m0")


def b3():
    items = [
        note(0, 0, 1700, '<span class="big" style="font-size:80px">&ldquo;Put your work out there.&rdquo;</span><br>My mentor, to me.'),
        row([col(steps("s", [("A brand-new Twitter account", "I posted my work and networked with editors on Twitter and LinkedIn.", "twitter"),
                             ("Their work showed me I had to step up", "", "eye"),
                             ("I locked in for six months", "Mastered Resolve and learned the business side.", "flame")]), 32, 900),
             col([ph("p4", "tweet1", "Screenshot: one of your first editing tweets", 760, 300, -1.5),
                  ph("p5", "tweet2", "Screenshot: your timeline / work-in-progress post", 760, 300, 1.5)], 40)], 60),
        rv(L("s9", "USD 60 out of my salary", "to join a community that taught the <b>business</b> of editing, not just the skill.", "users-round", "gold"), "What I paid for"),
    ]
    edge("s2", "s9", "gold", sa="b", sb="t")
    return B(3, "1.3", "Putting my work out there", "megaphone", items, "My mentor's advice", "s0")


def bar(nid, v, h, gold=False):
    return node(nid, 0, 0, 250, f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px">{big("$" + str(v), 80 if not gold else 100)}'
                f'<div style="width:190px;height:{h}px;background:{CH if gold else "#1E3150"};border-radius:18px 18px 0 0"></div>'
                f'<div class="lb" style="margin:0">per short-form video</div></div>', "", "align-self:flex-end")


def b4():
    items = [
        row([col([note(0, 0, 900, '<b style="font-size:36px">My first client came to me by DM.</b><br>He had been watching my posts.'),
                  row([bar("v0", 20, 70), bar("v1", 30, 120), bar("v2", 60, 200, True)], 40, "align-items:flex-end;height:400px"),
                  L("v9", "My first dollar payment", "<b>I didn't even know how to turn dollars into naira.</b>", "coins")], 40, 980),
             col([ph("p6", "firstdm", "Screenshot: the DM from your first client", 700, 440, 1.5),
                  L("v8", "Days in the military. Nights editing.", "", "moon", "navy")], 40)], 70),
    ]
    chain(["v0", "v1", "v2"], "gold", sa="t", sb="t", bend=0.6)
    return B(4, "1.4", "The first dollar", "coins", items, "Still a soldier", "v0")


def b5():
    items = [
        note(0, 0, 1700, '<b style="font-size:40px">Then I quit the military.</b> The riskiest thing I have done.'),
        row([L("f0", "First month", big("$600", 96), "calendar", "", "auto", "flex:1"),
             rv(L("f1", "Second month", big("~$1,000", 96), "trending-up", "", "auto", "flex:1"), "Month 2?", "flex:1;display:flex"),
             L("f2", "Three clients at once", "I nearly burnt out. <b>More clients does not mean you are better.</b>", "triangle-alert", "dim", "auto", "flex:1")], 60),
        row([L("f3", "Route Rise reached out", "They had been watching my work. A YouTube channel with <b>1 million subscribers</b>, a <b>billion-dollar company</b>.", "eye", "gold", 960),
             ph("p7", "routerise", "Photo: you at work for Route Rise", 600, 300, -1.5)], 60),
        lab2("Per video, in US dollars"),
        row([L("g0", "First client", big("$20", 64), "", "dim", "auto", "flex:1"), L("g1", "Raised", big("$30", 64), "", "dim", "auto", "flex:1"),
             L("g2", "Then", big("$60", 64), "", "", "auto", "flex:1"), L("g3", "Agency", big("$250", 84, NAVY), "", "gold", "auto", "flex:1")], 60),
        rv(remember("The jump came from better clients, not more clients."), "Why the jump?"),
    ]
    chain(["f0", "f1"], "gold", sa="r", sb="l")
    chain(["g0", "g1", "g2", "g3"], "gold", sa="r", sb="l")
    return B(5, "1.5", "Going full time", "rocket", items, "The riskiest move", "f0")


def b6():
    items = [
        note(0, 0, 1700, 'About 4 to 5 years in. Lots of mistakes, trial and error.'),
        quote_(0, 0, 1700, "I wish I had known two years earlier what I know now.", 70),
        row([L("w0", "Learning from YouTube", "", "youtube", "", "auto", "flex:1"), L("w1", "Posting my work", "", "megaphone", "", "auto", "flex:1")], 40),
        note(0, 0, 1700, 'Two things ran under everything. <b>Every jump in pay came from real work or from being seen.</b>'),
        rv(remember("The skill gets you in. How you present it is why you get hired."), "The lesson"),
        row([L("w2", "Not just a skill", "Video editing is a way of passing information and communicating.", "message-circle", "dim", "auto", "flex:1"),
             L("w3", "Effects need a purpose", "A lot of people put effects in a video <b>without understanding what purpose they serve.</b>", "sparkles", "dim", "auto", "flex:1")], 40),
    ]
    return B(6, "1.6", "What it taught me", "lightbulb", items, "4 to 5 years in")


TOC = [("1.1", "It started as a hobby"), ("1.2", "The best move I made"), ("1.3", "Putting my work out there"),
       ("1.4", "The first dollar"), ("1.5", "Going full time"), ("1.6", "What it taught me")]


def build():
    reset()
    body = assemble("1", "Soldier to", "Editor", "From a soldier with a hobby to an editor paid by clients abroad, working from Abuja.",
                    "People watch what you do. People watch what you post.", [b1(), b2(), b3(), b4(), b5(), b6()], TOC,
                    ("NEXT · CHAPTER 2", "The truth about the market"),
                    '<img src="kit/samuel-cutout-sm.webp" style="width:700px;align-self:center">')
    return body, W, None
