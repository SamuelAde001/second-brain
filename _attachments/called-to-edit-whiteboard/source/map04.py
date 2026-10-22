"""Chapter 4 as a map: Choose your niche. Branches snake: 4.1 -> 4.2, down to 4.3 <- , 4.4, down to 4.5 -> 4.6."""
from maplib import *
from lib import rv, icon, mark, NAVY, CH, MIST

NAME, W = "map04-niche", 5400
A, B = 1450, 3500          # the two branch columns
R1, R2, R3 = 80, 1150, 2220  # the three branch rows


def zone(x, y, w, h):
    return f'<div class="zone" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>'


def ranking(b, ox, oy):
    b.append(topic("t1", ox, oy + 60, 760, "4.1", "Who pays? My ranking", "trophy"))
    tiers = [("SaaS, software and AI companies", "Those guys have money. They can pay you a lot.", "TOP", "gold"),
             ("Real estate agents, marketers, logistics companies, personal brands", "Small businesses that actually make money. It's easier to negotiate prices with them.", "VERY GOOD", ""),
             ("Educative creators", "Educative creators are good. Most of them are selling a product in one form or the other.", "GOOD", ""),
             ("Entertainment, gaming, skits, dance", "To be honest, they are mostly broke. At 1 million views they can pay, but by then they already have a good editor.", "LOWEST", "dim")]
    y = oy + 220
    for k, (h_, bd, tag, cls) in enumerate(tiers):
        col = NAVY if cls == "gold" else ("#B9C3D6" if cls == "dim" else "#fff")
        inner = (f'<div style="display:flex;gap:18px;align-items:center"><div class="tb">{k+1}</div><div style="flex:1"><div class="lh" style="color:{col}">{h_}</div>'
                 f'<div class="lb">{bd}</div></div><div class="chip {"" if cls == "gold" else "dim"}" style="position:static">{tag}</div></div>')
        b.append(node(f"r{k}", ox + k * 70, y, 1400, rv(inner, f"Tier {k+1}?"), "leaf " + cls))
        y += 178
    edge("t1", "r0", "line", sa="b", sb="t", bend=0.4)
    for k in range(3):
        edge(f"r{k}", f"r{k+1}", "mist", sa="l", sb="l", bend=0.9)
    b.append(note(ox + 1640, oy + 640, 130, '<div style="font:800 20px \'Plus Jakarta Sans\';letter-spacing:.12em;color:#B9C3D6">PAYS<br>LESS</div>'))


def trap(b, ox, oy):
    b.append(topic("t2", ox, oy + 60, 1360, "4.2", "The follower trap", "users"))
    b.append(leaf("f1", ox, oy + 230, 620, "Business creator · 10K followers", rv('<div class="lh" style="font-size:27px;color:#0A1F44">Can be making $100,000 a month from just 10,000 followers, because he\'s marketing to them.</div>', "Earns…"), "briefcase", "gold"))
    b.append(leaf("f2", ox + 740, oy + 230, 620, "Entertainer · 100K followers", rv('<div class="lh" style="font-size:27px">And still can\'t afford to pay you $500, or even $100.</div>', "Earns…"), "gamepad-2", "dim"))
    b.append(note(ox + 640, oy + 290, 90, '<div style="font-family:Gloock;font-size:60px;color:#FCDD9E;text-align:center">vs</div>'))
    b.append(note(ox, oy + 560, 1360, '<b style="font-size:36px">Don\'t look at the followers.</b><br>Ask yourself: how much does this niche generate? Can they afford a video editor?'))
    edge("t2", "f1", "line", sa="b", sb="t", bend=0.4)
    edge("t2", "f2", "line", sa="b", sb="t", bend=0.4)
    b.append(leaf("w1", ox, oy + 760, 640, "Corporate companies", "They hire you like a normal employee. Fixed pay, and you can't negotiate. I always advise against it.", "building", "dim"))
    b.append(leaf("w2", ox + 720, oy + 760, 640, "Low-ticket sellers", "They sell something cheap. It might not make them enough to pay their editor well.", "receipt", "dim"))
    b.append(note(ox, oy + 712, 600, '<div style="font:800 20px \'Plus Jakarta Sans\';letter-spacing:.14em;color:#FCDD9E">TWO MORE TO BE CAREFUL WITH</div>'))


def glance(b, ox, oy):
    b.append(topic("t3", ox, oy + 60, 1400, "4.3", "The niches at a glance", "layout-grid"))
    rows = [("SaaS, software, AI tools", "High"), ("Personal finance, investing", "High"), ("Business, marketing, coaches", "High (my niche)"),
            ("Real estate", "High"), ("Ads, in any niche", "High"), ("Education, explainers", "Good"), ("Podcasts", "Depends"),
            ("Vlogs, lifestyle, fitness, beauty", "Depends"), ("Events, weddings, church", "Varies"), ("Gaming, skits, dance", "Low")]
    for k, (n_, p_) in enumerate(rows):
        col, r = divmod(k, 5)
        gold = p_.startswith("High")
        b.append(node(f"g{k}", ox + col * 720, oy + 230 + r * 122, 680,
                      f'<div style="display:flex;justify-content:space-between;align-items:center;gap:14px"><div class="lh" style="font-size:25px;color:{"#fff" if gold else "#B9C3D6"}">{n_}</div><div class="chip {"gold" if gold else "dim"}" style="position:static;font-size:19px;padding:7px 16px">{p_}</div></div>',
                      "leaf " + ("" if gold else "dim"), "padding:16px 22px"))
    edge("t3", "g0", "line", sa="b", sb="t", bend=0.3)
    edge("t3", "g5", "line", sa="b", sb="t", bend=0.3)


def choose(b, ox, oy):
    b.append(topic("t4", ox, oy + 60, 760, "4.4", "How to choose yours", "compass"))
    qs = [("What excites you?", "Edit the niche you watch the most. I watch a lot of business videos, so I understand how they're edited."), ("How much does this niche generate?", "Can they afford a video editor?"),
          ("Do they value marketing?", "That's why business guys are always the best. They already understand marketing."), ("Can your tools handle it?", "We'll talk about tools in the next chapter.")]
    pos = [(0, 230), (720, 330), (0, 560), (720, 660)]
    for k, ((h_, bd), (x, y)) in enumerate(zip(qs, pos)):
        b.append(leaf(f"q{k}", ox + x, oy + y, 660, f'<span style="font-family:Gloock;color:#FCDD9E;font-size:42px;margin-right:12px">{k+1}</span>{h_}', bd))
    edge("t4", "q0", "line", sa="b", sb="t", bend=0.4)
    chain(["q0", "q1", "q2", "q3"], "gold")


def shortlong(b, ox, oy):
    b.append(topic("t5", ox, oy + 60, 780, "4.5", "Short form or long form?", "film"))
    b.append(leaf("s1", ox, oy + 230, 660, '<span style="font-family:Gloock;font-size:66px;color:#FCDD9E;line-height:1">$500, $1,000, $2,000</span>', "per video. In long form, that's a price you easily hear. <b>Long form naturally pays more.</b>", "", "", "flex-direction:column;gap:0"))
    b.append(leaf("s2", ox + 740, oy + 230, 660, '<span style="font-family:Gloock;font-size:66px;color:#FCDD9E;line-height:1">5–10 videos</span>', "short form a month. In short form you pitch: <b>&ldquo;I'm doing 5 videos for you in a month.&rdquo;</b>", "", "", "flex-direction:column;gap:0"))
    b.append(node("s3", ox + 740, oy + 560, 660, rv(f'<div style="display:flex;gap:18px;align-items:center">{icon("megaphone", 46, NAVY, 2)}<div><div class="lh" style="color:#0A1F44">In short form, ads pay a lot</div><div class="lb" style="color:#0A1F44">Ads are tied directly to the clients a business gets, so it\'s easy to measure how your videos perform. I know guys that edit ads, and bro, they make a lot of money.</div></div></div>', "Best short form?"), "leaf gold"))
    b.append(note(ox, oy + 600, 640, 'A short form editor can earn more than a long form editor, <b>if he knows how to package his stuff well.</b>'))
    edge("t5", "s1", "line", sa="b", sb="t", bend=0.4)
    edge("t5", "s2", "line", sa="b", sb="t", bend=0.4)
    edge("s2", "s3", "gold", sa="b", sb="t")


def offer(b, ox, oy):
    b.append(topic("t6", ox, oy + 60, 1400, "4.6", "Say it in one sentence", "target"))
    b.append(note(ox, oy + 190, 1400, '<div style="font:500 26px \'Plus Jakarta Sans\';color:#B9C3D6">Once you pick your niche, you need an offer sentence. Who do you help, what result do you get them, how, and how fast. <b style="color:#fff">There must be a promise.</b></div>'))
    parts = [("I help", False), ("who", True), ("get", False), ("what result", True), ("in", False), ("how long", True), ("through", False), ("how", True)]
    x = ox
    for k, (t, g) in enumerate(parts):
        if g:
            b.append(chip(f"o{k}", x, oy + 300, t, "gold"))
            x += 70 + len(t) * 17 + 34
        else:
            b.append(note(x, oy + 312, 220, f'<span style="font:800 32px \'Plus Jakarta Sans\';color:#fff">{t}</span>'))
            x += len(t) * 19 + 34
    b.append(node("ex", ox, oy + 450, 1400, rv('<div class="lh" style="color:#0A1F44;font-size:34px">&ldquo;I help business creators get 10,000 views in 3 months through video editing and visually engaging content.&rdquo;</div><div class="lb" style="color:#0A1F44">My own offer. Always be specific.</div>', "My example"), "leaf gold"))
    b.append(leaf("do", ox, oy + 700, 1400, "Do this", "Write out what you're offering as a service, to who, which kind of videos, and how you'll package and sell it. Then write your offer sentence.", "list-checks", "navy"))
    edge("o7", "ex", "gold", sa="b", sb="t", bend=0.3)


TOC = [("4.1", "Who pays? My ranking"), ("4.2", "The follower trap"), ("4.3", "The niches at a glance"),
       ("4.4", "How to choose yours"), ("4.5", "Short form or long form?"), ("4.6", "Say it in one sentence")]


def build():
    reset()
    brs = []
    for fn in (ranking, trap, glance, choose, shortlong, offer):
        b = []
        fn(b, 0, -60)
        brs.append("".join(b))
    body = assemble("4", "Choose your", "Niche", "Pick a niche you enjoy, that makes money, and that values marketing. Then put your offer out there.",
                    "In any niche, business guys pay more.", brs, TOC, ("NEXT · CHAPTER 5", "Your tools and the money to start"))
    return body, W, None
