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
    tiers = [("SaaS, software and AI companies", "Those people have money. They can pay you a lot.", "TOP", "gold"),
             ("Real estate, marketers, logistics, solar, service businesses, personal brands", "Businesses that sell a service know what a good video brings them.", "VERY GOOD", ""),
             ("Educative creators", "Most are business people teaching you toward a product.", "GOOD", ""),
             ("Entertainment, gaming, skits, dance", "Mostly broke. By ~1M views, when they can pay, they already have a good editor.", "LOWEST", "dim")]
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
    b.append(leaf("f1", ox, oy + 230, 620, "Business creator · 10K followers", rv('<div class="lh" style="font-size:27px;color:#0A1F44">Can make USD 100,000 a month, because he markets to them.</div>', "Earns…"), "briefcase", "gold"))
    b.append(leaf("f2", ox + 740, oy + 230, 620, "Entertainer · 100K followers", rv('<div class="lh" style="font-size:27px">May not afford USD 500, or even USD 100, per video.</div>', "Earns…"), "gamepad-2", "dim"))
    b.append(note(ox + 640, oy + 290, 90, '<div style="font-family:Gloock;font-size:60px;color:#FCDD9E;text-align:center">vs</div>'))
    b.append(note(ox, oy + 560, 1360, '<b style="font-size:36px">Followers are not money.</b><br>Ask what a creator sells, not how many people follow them.'))
    edge("t2", "f1", "line", sa="b", sb="t", bend=0.4)
    edge("t2", "f2", "line", sa="b", sb="t", bend=0.4)
    b.append(leaf("w1", ox, oy + 760, 640, "Corporate companies", "Fixed pay, can't negotiate. I advise against it.", "building", "dim"))
    b.append(leaf("w2", ox + 720, oy + 760, 640, "Low-ticket sellers", "Sell something cheap. May not pay an editor well.", "receipt", "dim"))
    b.append(note(ox, oy + 712, 600, '<div style="font:800 20px \'Plus Jakarta Sans\';letter-spacing:.14em;color:#FCDD9E">TWO MORE TO WATCH</div>'))


def glance(b, ox, oy):
    b.append(topic("t3", ox, oy + 60, 1400, "4.3", "The niches at a glance", "layout-grid"))
    rows = [("SaaS, software, AI tools", "High"), ("Personal finance, investing", "High"), ("Business, marketing, coaches", "High · my niche"),
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
    qs = [("What excites you most?", "What do you watch most? I watch a lot of business videos."), ("How much does it make?", "Can they afford an editor?"),
          ("Do they value marketing?", "Why business people are always the best."), ("Can your tools handle it?", "That's the next chapter.")]
    pos = [(0, 230), (720, 330), (0, 560), (720, 660)]
    for k, ((h_, bd), (x, y)) in enumerate(zip(qs, pos)):
        b.append(leaf(f"q{k}", ox + x, oy + y, 660, f'<span style="font-family:Gloock;color:#FCDD9E;font-size:42px;margin-right:12px">{k+1}</span>{h_}', bd))
    edge("t4", "q0", "line", sa="b", sb="t", bend=0.4)
    chain(["q0", "q1", "q2", "q3"], "gold")


def shortlong(b, ox, oy):
    b.append(topic("t5", ox, oy + 60, 780, "4.5", "Short form or long form?", "film"))
    b.append(leaf("s1", ox, oy + 230, 660, '<span style="font-family:Gloock;font-size:66px;color:#FCDD9E;line-height:1">$500–2,000</span>', "per long-form video is a price you easily hear. <b>More per video.</b>", "", "", "flex-direction:column;gap:0"))
    b.append(leaf("s2", ox + 740, oy + 230, 660, '<span style="font-family:Gloock;font-size:66px;color:#FCDD9E;line-height:1">5–10 videos</span>', "short form a month, in one package. <b>Less per video, so you sell volume.</b>", "", "", "flex-direction:column;gap:0"))
    b.append(node("s3", ox + 740, oy + 560, 660, rv(f'<div style="display:flex;gap:18px;align-items:center">{icon("megaphone", 46, NAVY, 2)}<div><div class="lh" style="color:#0A1F44">Ads: the best-paying short form</div><div class="lb" style="color:#0A1F44">Tied directly to the customers a business gets.</div></div></div>', "Best short form?"), "leaf gold"))
    b.append(note(ox, oy + 600, 640, 'A short-form editor can earn more than a long-form one, <b>if they package their work well.</b>'))
    edge("t5", "s1", "line", sa="b", sb="t", bend=0.4)
    edge("t5", "s2", "line", sa="b", sb="t", bend=0.4)
    edge("s2", "s3", "gold", sa="b", sb="t")


def offer(b, ox, oy):
    b.append(topic("t6", ox, oy + 60, 1400, "4.6", "Say it in one sentence", "target"))
    b.append(note(ox, oy + 190, 1400, '<div style="font:500 26px \'Plus Jakarta Sans\';color:#B9C3D6">Stop saying &ldquo;I\'m a video editor.&rdquo; There are too many kinds. Turn it into an offer: there must be a promise.</div>'))
    parts = [("I help", False), ("who", True), ("get", False), ("what result", True), ("in", False), ("how long", True), ("through", False), ("how", True)]
    x = ox
    for k, (t, g) in enumerate(parts):
        if g:
            b.append(chip(f"o{k}", x, oy + 300, t, "gold"))
            x += 70 + len(t) * 17 + 34
        else:
            b.append(note(x, oy + 312, 220, f'<span style="font:800 32px \'Plus Jakarta Sans\';color:#fff">{t}</span>'))
            x += len(t) * 19 + 34
    b.append(node("ex", ox, oy + 450, 1400, rv('<div class="lh" style="color:#0A1F44;font-size:34px">&ldquo;I help business creators get 10,000 views in 3 months through video editing and visually engaging content.&rdquo;</div><div class="lb" style="color:#0A1F44">My example. Always be specific.</div>', "My example"), "leaf gold"))
    b.append(leaf("do", ox, oy + 700, 1400, "Do this", "Write what service you offer, to whom, which videos, and how you'll package and sell it. Then write your offer sentence.", "list-checks", "navy"))
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
    body = assemble("4", "Choose your", "Niche", "Pick one you enjoy, that makes money and values marketing. Then say it in one sentence.",
                    "In any niche, business people pay more.", brs, TOC, ("NEXT · CHAPTER 5", "Your tools and the money to start"))
    return body, W, None
