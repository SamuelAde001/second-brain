"""Opening map: the title, why you, and tonight's pathway through the 12 chapters. Wording from his voice notes 0.1 and 0.2."""
from maplib import *
from lib import rv, icon, remember, NAVY, CH, MIST

NAME, W = "map00-opening", 5400

STOPS = [("1", "My story"), ("2", "The market"), ("3", "Editing is a service"), ("4", "Choose your niche"),
         ("5", "Tools &amp; money"), ("6", "Learn the skill"), ("7", "Practice to paid"), ("8", "Get seen"),
         ("9", "Get clients"), ("10", "Price &amp; get paid"), ("11", "Grow through people"), ("12", "Next steps")]
BRIGHT = {"6", "7", "8", "9", "10"}


def b1():
    items = [
        note(0, 0, 1700, '<span style="font:600 50px \'Plus Jakarta Sans\';color:#fff">There are up to millions of video editors all around the globe.</span><br>' + big("Why you?", 170)),
        L("d0", "Video editing is broad", "Movie editors, podcast editors, short form editors, motion graphics animators. As long as you turn raw footage and a raw idea "
              "into a video people can easily digest, <b>that is editing.</b>", "scissors", "navy"),
        row([L("d1", "Tonight is not a tutorial", "Step-by-step tutorials, YouTube is there. I learned 80 to 90% of what I know from YouTube, and I'll show you how to learn from it properly.", "circle-x", "dim", "auto", "flex:1"),
             rv(L("d2", "I'm teaching you the pathway", "How to learn the skill and what to learn first. The tools and the money to start. Your niche. How to establish yourself. "
                  "<b>How to get clients, and how to get paid.</b>", "route", "gold", "auto", "flex:1"), "What tonight is", "flex:1;display:flex")], 70),
    ]
    edge("d1", "d2", "gold", sa="r", sb="l")
    return B(1, "0.1", "Start here", "flag", items, "What tonight is, and what it isn't", "d0")


def b2():
    def stop(k, n, t):
        gold = n in BRIGHT
        return node(f"c{k}", 0, 0, 260, f'<div class="spk" style="width:130px;height:130px;font-family:Gloock;font-size:64px;font-weight:400;'
                    f'{"" if gold else "background:#1E3150;color:#fff"}">{n}</div><div style="font:700 25px/1.2 \'Plus Jakarta Sans\';color:{CH if gold else "#fff"};text-align:center;margin-top:16px">{t}</div>',
                    "", "display:flex;flex-direction:column;align-items:center")
    r1 = row([stop(k, n, t) for k, (n, t) in enumerate(STOPS[:6])], 48, "justify-content:space-between")
    r2 = row([stop(k + 6, n, t) for k, (n, t) in reversed(list(enumerate(STOPS[6:])))], 48, "justify-content:space-between")
    for k in range(11):
        if k == 5:
            edge("c5", "c6", "gold", sa="b", sb="t")
        else:
            edge(f"c{k}", f"c{k+1}", "gold", sa="r" if k < 5 else "l", sb="l" if k < 5 else "r", bend=0.2)
    items = [
        note(0, 0, 1700, big("This is where we're going tonight.", 80)),
        r1, note(0, 0, 10, "&nbsp;"), r2,
        note(0, 0, 1700, f'<div style="display:flex;align-items:center;gap:16px"><svg width="30" height="30"><circle cx="15" cy="15" r="13" fill="{CH}"/></svg>'
                         '<div>The gold ones are where I\'ll spend the most time, because that\'s what most of you asked me: <b>how do I learn, and how do I get clients and get paid?</b></div></div>'),
    ]
    return B(2, "0.2", "The pathway", "map", items, "12 stops, one by one", "c0")


TOC = [("0.1", "Start here"), ("0.2", "The pathway")]


def build():
    reset()
    side = ('<img src="kit/samuel-cutout-sm.webp" style="width:760px;align-self:center">'
            '<div style="font:700 30px \'Plus Jakarta Sans\';color:#fff">Samuel Adebayo<br><span style="color:#B9C3D6;font-weight:500">Video editor and coach. Founder, Called to Edit</span></div>'
            '<img src="kit/called-to-edit-logo-dark.svg" style="width:420px">')
    body = assemble("", "How to build a career as a", "Video Editor", "and get paid. The pathway I wish I knew when I started. <br><b style=\"color:#FCDD9E\">Live webinar, Friday 23 October, 7pm WAT</b>",
                    "Editing is cutting out what is not needed from the raw idea, and presenting it in a way the viewer can get it.",
                    [b1(), b2()], TOC, ("START · CHAPTER 1", "My story: soldier to editor"), side)
    return body, W, None
