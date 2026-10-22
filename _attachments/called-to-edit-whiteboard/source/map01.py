"""Chapter 1 as a map: My story, a timeline of photos from soldier to editor. Wording from his voice note 0.1."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map01-story", 5400
P = {}  # photo sources by slot key, filled from photos.json


def ph(nid, key, label, w=420, h=320, tilt=0, fit="cover"):
    return photo(nid, 0, 0, w, h, label, P.get(key), tilt, fit)


def b1():
    items = [
        row([ph("p1", "uniform", "A soldier, 2020", 340, 440, -2),
             ph("p1b", "firstlaptop-bw", "Learning to edit, Dec 2020", 340, 440, 1.5),
             ph("p2", "minecraft", "Screenshot: your Minecraft YouTube channel", 340, 440, -1),
             col([L("l0", "I had a Minecraft YouTube channel", "I wanted to edit my own videos. That's how I stumbled on video editing.", "gamepad-2"),
                  L("l1", "I wanted a free software", "I was editing on a laptop, so I found <b>DaVinci Resolve</b>. My first editing software.", "laptop"),
                  L("l2", "Later on, I edited for my church", "But it was all just personal projects.", "church", "dim")], 40, 500, "justify-content:center")], 40),
        quote_(0, 0, 1700, "If I knew CapCut then, I might have started with CapCut. But I started with DaVinci Resolve, and I'm glad I did.", 50),
    ]
    chain(["p1", "p1b", "p2", "l0"], "gold", sa="r", sb="l", bend=0.3)
    edge("l0", "l1", "gold", sa="b", sb="t")
    edge("l1", "l2", "gold", sa="b", sb="t")
    return B(1, "1.1", "It started with Minecraft", "gamepad-2", items, "2020, during COVID. I was still a soldier.", "p1")


def b2():
    items = [
        row([L("m0", "&ldquo;What can I do better than just being a soldier?&rdquo;",
               "I went through all the skills I could learn. I already knew a little editing, so I picked it. My mentor had just opened a YouTube channel, "
               "so I reached out: <b>&ldquo;Sir, I would love to be editing your videos for you, if you don't mind.&rdquo;</b> I wasn't good at all. I only knew how to cut.",
               "handshake", "navy", "auto", "flex:1"),
             ph("pa", "acer", "I spent a whole month's salary on this laptop. Decent, but laggy.", 330, 330, 2)], 50, "align-items:center"),
        lab2("The first videos I edited for him"),
        row([L("e0", "First video", "He returned it. <b>&ldquo;I can't use this.&rdquo;</b> It was very bad.", "circle-x", "dim", "auto", "flex:1"),
             rv(L("e1", "Second video", "Still not there. I kept trying my best to improve.", "refresh-cw", "", "auto", "flex:1"), "Second video?", "flex:1;display:flex"),
             rv(L("e2", "Third video", "He finally uploaded it. I wanted to impress him so badly.", "circle-check", "gold", "auto", "flex:1"), "Third video?", "flex:1;display:flex")], 70),
        row([L("m1", "&#8358;25,000 a month", "Later he gave me an allowance for data. About four videos a month, for <b>two years</b>. But my skill kept getting better.", "wallet", "", "auto", "flex:1;align-self:center"),
             ph("p3", "mentor-edit", "Editing for my mentor, late at night", 300, 330, -1.5)], 50),
        remember("I didn't learn by watching tutorials for myself. I watched tutorials to edit videos that would actually go live. That has stakes."),
    ]
    chain(["e0", "e1", "e2"], "gold", sa="r", sb="l", bend=0.3)
    return B(2, "1.2", "The best move I made", "sparkles", items, "Editing for my mentor, for free", "m0")


def b3():
    items = [
        note(0, 0, 1700, '<span class="big" style="font-size:80px">&ldquo;Put your work out there.&rdquo;</span><br>Let people see what you can do. That was my mentor\'s advice.'),
        row([col(steps("s", [("I opened a new Twitter account", "I started posting my work and networking with other editors, on Twitter and LinkedIn mostly.", "twitter"),
                             ("I saw what other editors were doing", "And I knew I needed to step up my game.", "eye"),
                             ("I locked in for six months", "I went back and mastered DaVinci Resolve. And the business side of editing.", "flame")]), 32, 900),
             col([ph("p4", "tweet1", "Screenshot: one of your first editing tweets", 760, 300, -1.5),
                  ph("p5", "timeline", "My timeline: showing my work", 760, 300, 1.5)], 40)], 60),
        rv(L("s9", "$60 from my own salary", "I paid to join a community. They taught more of the <b>business</b> of video editing than just the skill. "
             "It's the things around the career that push you to succeed.", "users-round", "gold"), "What I paid for"),
    ]
    edge("s2", "s9", "gold", sa="b", sb="t")
    return B(3, "1.3", "Putting my work out there", "megaphone", items, "My mentor's advice", "s0")


def bar(nid, v, h, gold=False):
    return node(nid, 0, 0, 250, f'<div style="display:flex;flex-direction:column;align-items:center;gap:12px">{big("$" + str(v), 80 if not gold else 100)}'
                f'<div style="width:190px;height:{h}px;background:{CH if gold else "#1E3150"};border-radius:18px 18px 0 0"></div>'
                f'<div class="lb" style="margin:0">per short-form video</div></div>', "", "align-self:flex-end")


def b4():
    items = [
        row([col([note(0, 0, 900, '<b style="font-size:36px">Then I got my first client DM.</b><br>He\'d been watching my stuff and wanted me to edit a video for him.'),
                  row([bar("v0", 20, 70), bar("v1", 30, 120), bar("v2", 60, 200, True)], 40, "align-items:flex-end;height:400px"),
                  L("v9", "My first dollar payment", "I freaked out. <b>I didn't even know how to turn dollars into naira.</b>", "coins")], 40, 980),
             col([ph("p6", "firstdm", "My first client's message", 680, 393, 1.5, "contain"),
                  row([ph("p6b", "uniform-editing", "In uniform, editing", 280, 360, -2),
                       L("v8", "Duties in the day. Editing at night.", "I was still in the military all this while.", "moon", "navy", "auto", "flex:1;align-self:center")], 40)], 40, 720)], 50),
    ]
    chain(["v0", "v1", "v2"], "gold", sa="t", sb="t", bend=0.6)
    return B(4, "1.4", "My first dollar", "coins", items, "Same client: $20, then $30, then $60")


def b5():
    items = [
        note(0, 0, 1700, '<b style="font-size:40px">Then I quit the military to do this full time.</b> One of the riskiest things I ever did. '
                         'I wasn\'t 100% sure it would work. But if I wanted to go all in, I had to go all in.'),
        row([ph("q0", "quit", "Leaving the uniform behind", 250, 300, -2), ph("q1", "empty-room", "Jan 2025: an empty room", 250, 300, 1.5),
             ph("q2", "desk-chair", "My first desk", 250, 300, -1), ph("q3", "burnout", "Three clients, long nights", 420, 300, 2),
             L("q9", "At one point I had three clients", "I almost burnt myself out. <b>More clients doesn't mean you're better.</b> So I went for better clients.", "triangle-alert", "dim", "auto", "flex:1;align-self:center")], 50),
        row([L("f0", "First month in Abuja", big("$600", 96), "calendar", "", "auto", "flex:1"),
             rv(L("f1", "Second month", big("$1,000", 96), "trending-up", "", "auto", "flex:1"), "Month 2?", "flex:1;display:flex"),
             ph("p7", "first-pc", "My first PC", 400, 225, -1.5), ph("p8", "billion", "Editing for a billion-dollar company", 220, 270, 1.5)], 50),
        L("f3", "Then Route Rise reached out", "A big company. They'd been watching what I post. Through them I've edited for a <b>1 million subscriber</b> YouTube channel and a <b>billion-dollar company</b>.", "eye", "gold"),
        lab2("What I got paid per video"),
        row([L("g0", "First client", big("$20", 64), "", "dim", "auto", "flex:1"), L("g1", "Same client", big("$30", 64), "", "dim", "auto", "flex:1"),
             L("g2", "Later", big("$60", 64), "", "", "auto", "flex:1"), L("g3", "An agency", big("$250", 84, NAVY), "", "gold", "auto", "flex:1")], 60),
        rv(remember("What changed? I stopped chasing more clients and started targeting better clients."), "What changed?"),
    ]
    chain(["f0", "f1"], "gold", sa="r", sb="l")
    chain(["q0", "q1", "q2", "q3"], "gold", sa="r", sb="l")
    edge("f1", "p7", "gold", sa="r", sb="l")
    chain(["g0", "g1", "g2", "g3"], "gold", sa="r", sb="l")
    return B(5, "1.5", "Going all in", "rocket", items, "The riskiest move I made", "f0")


def b6():
    items = [
        note(0, 0, 1700, 'It\'s been four, five years now. I made a lot of mistakes. I did things by trial and error.'),
        row([col([quote_(0, 0, 1300, "If I knew in my first three years what I know now, I'd be farther away.", 70)], 0, 1320, "justify-content:center"),
             ph("pz", "portrait", "Today", 300, 400, 2)], 40),
        note(0, 0, 1700, 'Now that I\'ve worked with the bigger boys in the industry, I know <b>not everything matters.</b> Some things matter the most. Those are what I\'m sharing tonight.'),
        row([L("w0", "There are millions of video editors", "All around the globe. So why should they hire you? Why not other people?", "users", "", "auto", "flex:1"),
             L("w1", "Your skills are very powerful", "But if they aren't presented the right way, why you? Understanding the business side is what makes you stand out.", "briefcase", "", "auto", "flex:1")], 40),
        rv(remember("All of this happened because I built my skill. But more importantly, I learned to present myself the right way."), "The lesson"),
        row([L("w2", "Video editing is not just a skill", "It's a way of passing information. You're expressing what the person wants to say to their audience.", "message-circle", "dim", "auto", "flex:1"),
             L("w3", "Why am I putting this effect here?", "A lot of people put effects in a video <b>without understanding what purpose it's doing.</b>", "sparkles", "dim", "auto", "flex:1")], 40),
    ]
    return B(6, "1.6", "What it taught me", "lightbulb", items, "Four, five years in")


TOC = [("1.1", "It started with Minecraft"), ("1.2", "The best move I made"), ("1.3", "Putting my work out there"),
       ("1.4", "My first dollar"), ("1.5", "Going all in"), ("1.6", "What it taught me")]


def build():
    reset()
    body = assemble("1", "Soldier to", "Editor", "How I went from a soldier editing Minecraft videos to editing for clients abroad, from Abuja.",
                    "People watch what you do. People watch what you post.", [b1(), b2(), b3(), b4(), b5(), b6()], TOC,
                    ("NEXT · CHAPTER 2", "The truth about the market"),
                    '<img src="kit/samuel-cutout-sm.webp" style="width:700px;align-self:center">')
    return body, W, None
