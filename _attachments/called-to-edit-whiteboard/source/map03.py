"""Chapter 3 as a map: editing is a service."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map03-service", 5400


def b1():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">What\'s business?</span><br>' + big("Exchange of value for money. Literally.", 92)),
        row([node("x0", 0, 0, 380, f'{icon("clapperboard", 96)}<div class="lh">You</div>', "leaf", "flex-direction:column;align-items:center"),
             col([note(0, 0, 560, '<div style="text-align:center"><b>I edit your videos</b> →<br><br>← <b>you give me cash</b></div>')], 0, 560, "justify-content:center"),
             node("x1", 0, 0, 380, f'{icon("user-round-check", 96)}<div class="lh">Client</div>', "leaf", "flex-direction:column;align-items:center")], 60, "justify-content:center"),
        note(0, 0, 1700, 'That\'s where a lot of video editors get stuck. <b>They learn the skill, leave it as a skill,</b> and don\'t know how to package it as a service.'),
        row([L("x2", "A skill", '<span style="font:800 34px \'Plus Jakarta Sans\';color:#B9C3D6">&ldquo;I can edit videos.&rdquo;</span><br>Millions of people can say that. Who is it for?', "scissors", "dim", "auto", "flex:1"),
             rv(L("x3", "A service", '<span style="font:800 34px/1.25 \'Plus Jakarta Sans\'">&ldquo;I edit YouTube videos for business creators so they get more views.&rdquo;</span><br>Now a particular person knows you are for them.', "target", "gold", "auto", "flex:1"), "A service sounds like…", "flex:1;display:flex")], 90),
    ]
    edge("x0", "x1", "gold", sa="t", sb="t", bend=0.12)
    edge("x1", "x0", "gold", sa="b", sb="b", bend=0.12)
    edge("x2", "x3", "gold", sa="r", sb="l")
    return B(1, "3.1", "A skill or a service?", "scale", items, "I serve you, you pay me")


def b2():
    flags = "".join(f'<span class="chip dim" style="position:static;display:inline-block;margin:6px 6px 0 0">{c}</span>' for c in ["Japan", "China", "Nigeria", "Brazil", "…"])
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Imagine I was running a clothing business.</span><br>' + big("Not everyone is your client.", 92)),
        row([L("y0", "Sewing for everyone", f'{flags}<br><br>I can\'t sew for people in Japan and people in China at the same time. <b>The way they dress is different.</b>', "shirt", "dim", "auto", "flex:1"),
             rv(L("y1", "I can only choose one demographic", '<span style="font:800 40px \'Plus Jakarta Sans\'">&ldquo;Okay, I\'m sewing clothes for Nigerians.&rdquo;</span><br>That\'s what it means to run a service. You know who you\'re targeting.', "shirt", "gold", "auto", "flex:1"), "Pick one group", "flex:1;display:flex")], 90),
        note(0, 0, 1700, 'The people you target determine <b>how you pitch your service</b>. If you serve everyone, eventually you\'ll be like every other video editor out there.'),
        quote_(0, 0, 1700, "You need to be specialised as a video editor, not generalised.", 70),
    ]
    edge("y0", "y1", "gold", sa="r", sb="l")
    return B(2, "3.2", "Not everyone is your client", "shirt", items, "The clothing business", "y0")


def b3():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Most people start with the skill.</span><br>' + big("We need to work backwards.", 100)),
        row([col([L("z0", "The tools you have", "My phone, my computer, CapCut. What can it do?", "smartphone"), L("z1", "Who you want to serve", "YouTubers, Instagram creators, real estate agents", "users")], 40, 520),
             col([L("z2", "What you go and learn", "Those two decide it.", "graduation-cap")], 0, 480, "justify-content:center"),
             col([rv(L("z3", "Then package it as a service for that person", "", "package", "gold"), "Then…")], 0, 520, "justify-content:center")], 140),
        journey("When I started, I wanted to be a motion designer. Two things stopped me: my laptop was very bad, and I didn't have the money. The tools you have decide who you can serve."),
        remember("You learn the skill of video editing. You sell the service."),
    ]
    edge("z0", "z2", "gold", sa="r", sb="l")
    edge("z1", "z2", "gold", sa="r", sb="l")
    edge("z2", "z3", "gold", sa="r", sb="l")
    return B(3, "3.3", "Work backwards", "undo-2", items, "Your tools and your client decide what you learn")


TOC = [("3.1", "A skill or a service?"), ("3.2", "Not everyone is your client"), ("3.3", "Work backwards")]


def build():
    reset()
    body = assemble("3", "Editing is a", "Service", "You learn the skill of video editing. You sell the service. And that service is for a particular person.",
                    "If you are targeting everyone, you have no one.", [b1(), b2(), b3()], TOC,
                    ("NEXT · CHAPTER 4", "Choose your niche"))
    return body, W, None
