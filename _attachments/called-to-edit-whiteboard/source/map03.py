"""Chapter 3 as a map: editing is a service."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map03-service", 5400


def b1():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Business is an exchange of value for money.</span><br>' + big("Literally.", 110)),
        row([node("x0", 0, 0, 380, f'{icon("clapperboard", 96)}<div class="lh">You</div>', "leaf", "flex-direction:column;align-items:center"),
             col([note(0, 0, 560, '<div style="text-align:center"><b>I edit your videos</b> →<br><br>← <b>you give me cash</b></div>')], 0, 560, "justify-content:center"),
             node("x1", 0, 0, 380, f'{icon("user-round-check", 96)}<div class="lh">Client</div>', "leaf", "flex-direction:column;align-items:center")], 60, "justify-content:center"),
        note(0, 0, 1700, 'This is where most editors get stuck. <b>Talented editors miss this all the time</b>: they focus on the skill, not on how to serve the client.'),
        row([L("x2", "A skill", '<span style="font:800 34px \'Plus Jakarta Sans\';color:#B9C3D6">&ldquo;I can edit videos.&rdquo;</span><br>True of millions of people. Nobody knows what to buy from you.', "scissors", "dim", "auto", "flex:1"),
             rv(L("x3", "A service", '<span style="font:800 34px/1.25 \'Plus Jakarta Sans\'">&ldquo;I edit YouTube videos for business creators so they get more views.&rdquo;</span><br>A specific person knows you are for them.', "target", "gold", "auto", "flex:1"), "A service sounds like…", "flex:1;display:flex")], 90),
    ]
    edge("x0", "x1", "gold", sa="t", sb="t", bend=0.12)
    edge("x1", "x0", "gold", sa="b", sb="b", bend=0.12)
    edge("x2", "x3", "gold", sa="r", sb="l")
    return B(1, "3.1", "Skill vs service", "scale", items, "An exchange of value")


def b2():
    flags = "".join(f'<span class="chip dim" style="position:static;display:inline-block;margin:6px 6px 0 0">{c}</span>' for c in ["Japan", "China", "Nigeria", "Brazil", "…"])
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Think about a clothing business.</span><br>' + big("Not everyone is your client.", 92)),
        row([L("y0", "Trying to dress everyone", f'{flags}<br><br>Different styles, sizes, tastes. <b>Nobody feels it was made for them.</b>', "shirt", "dim", "auto", "flex:1"),
             rv(L("y1", "Picking one group", '<span style="font:800 40px \'Plus Jakarta Sans\'">&ldquo;I sew clothes for Nigerians.&rdquo;</span><br>Now every choice is easy: the fabric, the cut, the price, the advert.', "shirt", "gold", "auto", "flex:1"), "Pick one group", "flex:1;display:flex")], 90),
        note(0, 0, 1700, 'Your target audience decides <b>how you pitch</b> and <b>what you learn</b>. Serve everyone and you end up like every other editor.'),
        quote_(0, 0, 1700, "Be specialised, not generalised.", 70),
    ]
    edge("y0", "y1", "gold", sa="r", sb="l")
    return B(2, "3.2", "Not everyone is your client", "shirt", items, "The clothing business", "y0")


def b3():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Don\'t start with the skill.</span><br>' + big("Work backwards.", 110)),
        row([col([L("z0", "The tools you have", "phone, computer, CapCut", "smartphone"), L("z1", "Who you want to serve", "YouTubers, IG creators, realtors", "users")], 40, 520),
             col([L("z2", "What you go and learn", "", "graduation-cap")], 0, 480, "justify-content:center"),
             col([rv(L("z3", "Package it as a service for that person", "", "package", "gold"), "Then…")], 0, 520, "justify-content:center")], 140),
        journey("I wanted to be a motion designer. My laptop was very bad and I didn't have money for a better one. So I chose what my tools could do, and that is what got me paid."),
        remember("Video editing is not just a skill, it's a service."),
    ]
    edge("z0", "z2", "gold", sa="r", sb="l")
    edge("z1", "z2", "gold", sa="r", sb="l")
    edge("z2", "z3", "gold", sa="r", sb="l")
    return B(3, "3.3", "Work backwards", "undo-2", items, "From the client to the skill")


TOC = [("3.1", "Skill vs service"), ("3.2", "Not everyone is your client"), ("3.3", "Work backwards")]


def build():
    reset()
    body = assemble("3", "Editing is a", "Service", "You learn a skill, but you sell a service, to a specific person. Everything after this rests on that.",
                    "If you are targeting everyone, you have no one.", [b1(), b2(), b3()], TOC,
                    ("NEXT · CHAPTER 4", "Choose your niche"))
    return body, W, None
