"""Chapter 2 as a map: the truth about the market."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map02-market", 5400


def b1():
    stats = [("5.66B", "social media accounts in the world, about 7 in 10 people", "DataReportal · Oct 2025", "globe"),
             ("200B", "YouTube Shorts views every single day", "YouTube · Jun 2025", "youtube"),
             ("3B", "people use Instagram every month", "Meta · Sep 2025", "instagram"),
             ("500+", "hours of video uploaded to YouTube every minute", "YouTube · 2019", "upload"),
             ("50M", "creators. Only about 4% earn over USD 100,000 a year", "Goldman Sachs · 2023", "users")]
    tiles = [node(f"s{k}", 0, 0, "auto", f'{icon(ic, 46)}{rv(big(n, 76), "?")}<div class="lh" style="font-size:24px">{t}</div><div class="lb" style="font-size:19px">{s}</div>',
                  "leaf", "flex:1;flex-direction:column;gap:12px") for k, (n, t, s, ic) in enumerate(stats)]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Is there a demand for editors right now?</span><br>' + big("Yes. A huge demand.", 100)),
        row(tiles[:3], 30), row(tiles[3:], 30),
        L("s9", "A lot of them are busy people", "You can't run a proper business today if you don't put something out there on the internet. Every business needs content, so every business needs editors. <b>And people are willing to pay a lot for it.</b>", "scissors", "gold"),
    ]
    return B(1, "2.1", "Is there demand?", "trending-up", items, "Look at the numbers", "s0")


def b2():
    kinds = [("gamepad-2", "Entertainment", "Skits, gaming, dance", "They are plenty, and they need editors too.", "Pays least", "dim"),
             ("graduation-cap", "Educative", "Teaching and explainers", "Most of them are business people. They educate you so you can eventually buy their product.", "Pays well", ""),
             ("briefcase", "Business", "Founders, brands, companies", "They put out a lot of content and it's tedious for them. These are the ones that pay the most.", "Pays the most", "gold")]
    cols = []
    for k, (ic, h, s, b, p, cls) in enumerate(kinds):
        cols.append(col([L(f"k{k}", h, f"<b>{s}</b><br>{b}", ic, cls),
                         rv(chip(f"kp{k}", 0, 0, p, "gold" if cls == "gold" else ("dim" if cls == "dim" else "")), "Pays?", "align-self:flex-start")], 24, None, "flex:1"))
    chain(["k0", "k1", "k2"], "mist", sa="r", sb="l")
    items = [note(0, 0, 1700, big("Three kinds of creators,", 72) + '<br><span style="font:600 40px \'Plus Jakarta Sans\';color:#fff">and they don\'t pay the same.</span>'),
             row(cols, 60)]
    return B(2, "2.2", "Who needs editors", "wallet", items, "Three kinds of creators", "k0")


def b3():
    ppl = lambda ic, c, n: "".join(icon(ic, 46, c) for _ in range(n))
    items = [
        lab2("An agency is a middleman"),
        row([node("a0", 0, 0, 360, f'<div style="display:flex;flex-wrap:wrap;gap:14px;justify-content:center">{ppl("user", MIST, 6)}</div><div class="lb" style="text-align:center">20 to 30 clients</div>', "leaf dim", "flex-direction:column"),
             node("a1", 0, 0, 380, f'{icon("building-2", 70, NAVY, 2)}<div class="lh" style="font-size:36px">Agency</div><div class="lb">takes a cut</div>', "leaf gold", "flex-direction:column;align-items:center;text-align:center"),
             node("a2", 0, 0, 360, f'<div style="display:flex;flex-wrap:wrap;gap:14px;justify-content:center">{ppl("clapperboard", CH, 6)}</div><div class="lb" style="text-align:center">many editors</div>', "leaf dim", "flex-direction:column")],
            150, "align-items:center;justify-content:center"),
        row([L("a3", "Agencies are good for beginners", "They always have work, and they give you access to clients you couldn't reach yourself. Working with agencies really helped my career. <b>But</b> they take their cut, so they don't pay much, and they give a lot of revisions.", "building-2", "", "auto", "flex:1"),
             rv(L("a4", "The best is working with creators and businesses directly", "When I work with the client directly, I don't have that much problem. But you have to find them yourself. <b>That's what tonight is about.</b>", "handshake", "gold", "auto", "flex:1"), "The best clients", "flex:1;display:flex")], 40),
        note(0, 0, 1700, 'The big brands and big creators go to agencies. <b>The ones who can\'t afford big agencies are the ones you work with.</b> You work your way up the ladder.'),
    ]
    edge("a0", "a1", "gold", sa="r", sb="l")
    edge("a1", "a2", "gold", sa="r", sb="l")
    return B(3, "2.3", "Agencies", "users", items, "Very good, but also very, very bad", "a1")


def b4():
    eds = "".join(node(f"e{k}", 0, 0, 200, f'{icon("clapperboard", 80)}', "", "display:flex;justify-content:center") for k in range(5))
    for k in range(5):
        edge("c0", f"e{k}", "line", sa="b", sb="t", bend=0.4)
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Some people say the market is full.</span><br>' + big("It's not. This is a big market.", 100)),
        node("c0", 0, 0, 1700, f'{icon("user-round-check", 110)}<div class="lh" style="font-size:30px;margin-top:10px">One creator</div>', "", "display:flex;flex-direction:column;align-items:center"),
        row([eds], 0, "justify-content:space-around;margin-top:60px"),
        note(0, 0, 1700, '<div style="text-align:center"><b style="font-size:34px">can have three, four, five video editors.</b></div>'),
        note(0, 0, 1700, 'The problem is, most of us are bad editors, and <b>we don\'t know how to position ourselves</b> so these people can find us.'),
        rv(L("c9", "The mistake most beginners make", "They learn a lot of skill, but they can't position themselves. They put random things in a portfolio and apply for jobs, with no social media.", "triangle-alert", "gold"), "Biggest mistake?"),
        journey("The main mistake I made was not putting myself out there."),
    ]
    return B(4, "2.4", "\"The market is full\"", "users-round", items, "A diamond is as valuable as it is visible")


def b5():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Yes, AI can edit videos. But people don\'t even want to spend time asking AI to edit their videos.</span><br>' + big("They still need editors.", 96)),
        row([L("i0", "Your skill", "", "scissors", "", "auto", "flex:1"),
             L("i1", "AI in your workflow", "", "bot", "", "auto", "flex:1"),
             rv(L("i2", "Your leverage", "You do things for them faster, easier, without too much complexity.", "zap", "gold", "auto", "flex:1"), "= ?", "flex:1;display:flex")], 110),
        row([L("i3", "My company is demanding that we use AI", "As professional video editors, not even beginners. They need editors who are up to date. But a lot of creativity is still needed.", "building", "dim", "auto", "flex:1"),
             L("i4", "This is the AI age", "A lot of skills you learn today will become useless next tomorrow. So you need to know what to learn.", "lightbulb", "dim", "auto", "flex:1")], 40),
    ]
    edge("i0", "i1", "gold", sa="r", sb="l", label="+")
    edge("i1", "i2", "gold", sa="r", sb="l", label="=")
    return B(5, "2.5", "AI", "bot", items, "Your skill + AI", "i0")


TOC = [("2.1", "Is there demand?"), ("2.2", "Who needs editors"), ("2.3", "Agencies"), ("2.4", "\"The market is full\""), ("2.5", "AI")]


def build():
    reset()
    body = assemble("2", "The truth about the", "Market", "There's a huge demand, and a huge chance for you. You just need to position yourself well.",
                    "A diamond is as valuable as it is visible.", [b1(), b2(), b3(), b4(), b5()], TOC,
                    ("NEXT · CHAPTER 3", "Editing is a service"))
    return body, W, None
