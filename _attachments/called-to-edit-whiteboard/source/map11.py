"""Chapter 11 as a map: grow through people."""
from maplib import *
from lib import rv, icon, remember, journey, doit, NAVY, CH, MIST

NAME, W = "map11-people", 5400
P = {}


def b1():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Clients love to work with people</span><br>' + big("who have done it before.", 100)),
        row(steps("r", [("Document the result for every client", "Views, sales, whatever you got for them.", "clipboard-list"), ("Keep screenshots of those results", "", "image"),
                        ("Turn them into case studies", "I did a lot of case studies of what I did for my mentor.", "book-open"), ("Ask for a testimonial", "Written, or a video of them saying how good you are. Video is very powerful.", "message-square-quote", "gold")],
                  d="row", gap=60, reveal=["Step 1", "Step 2", "Step 3", "Step 4"], num=True), 60),
        row([col([photo("r7", 0, 0, 800, 400, "Screenshot: views on your mentor's channel", P.get("mentorviews"), -1.5),
                  note(0, 0, 800, 'I took my mentor\'s channel from about 1,000 views to about 4,000. Not that much for YouTube, but it really helped. It went into my portfolio and case studies, <b>even though I was working for free.</b>')], 24, 820),
             col([photo("r8", 0, 0, 800, 400, "Screenshot: a client testimonial", P.get("testimonial"), 1.5)], 24, 820)], 60),
        doit("Some of us have worked with people but never asked them for a testimonial. Ask one this week."),
    ]
    return B(1, "11.1", "Results and testimonials", "trophy", items, "Your most important asset", "r0")


def b2():
    eds = [chip(f"e{k}", 0, 0, icon("clapperboard", 34, CH) + '<span style="display:inline-block;margin-left:14px">Editor</span>', "") for k in range(6)]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Social media is meant</span><br>' + big("to be social.", 110)),
        row([col(eds[:3], 40, 360, "align-items:flex-end;justify-content:center"),
             node("ey", 0, 0, 340, '<div class="spk" style="width:300px;height:300px">You</div>', "", "display:flex;justify-content:center"),
             col(eds[3:], 40, 360, "justify-content:center")], 110, "justify-content:center"),
        journey('On Twitter I was engaging other editors\' posts, commenting, talking with them. I joined their challenges, like <b>&ldquo;10 days to get my first client&rdquo;</b>, and hailed them. In our DMs we looked at each other\'s edits and corrected ourselves. When they saw an opportunity, they let me know.'),
        rv(L("e8", big("2 in 3", 100, NAVY), "freelancers get their work through referrals and reputation. (Fiverr survey, 2024)", "", "gold"), "How freelancers get work"),
        row([L("e9", "Who", "Video editors at your level, or smaller than you.", "users", "", "auto", "flex:1"), L("e10", "Where", "LinkedIn and Twitter are the best. You can still do it on Instagram.", "map-pin", "", "auto", "flex:1")], 30),
        note(0, 0, 1700, 'They will recommend you. They will give you opportunities. They will criticise your work. They will boost your posts. <b>Some opportunities never come by outreach or personal branding. They come by relationships.</b>'),
        L("e11", "Join video editing communities", "Mine was VP Plus, a paid one. I met some of the biggest editors there. They challenged me, and I got one or two clients.", "users-round", "navy"),
        remember("The real people who will give you opportunities are people who know you."),
    ]
    for k in range(3):
        edge("ey", f"e{k}", "gold", sa="l", sb="r", bend=0.3)
        edge("ey", f"e{k+3}", "gold", sa="r", sb="l", bend=0.3)
    return B(2, "11.2", "Network with other editors", "users", items, "People who know you")


TOC = [("11.1", "Results and testimonials"), ("11.2", "Network with other editors")]


def build():
    reset()
    body = assemble("11", "Grow through", "People", "Results you can show, and people who know you. That's how the bigger clients come.",
                    "You can't do video editing alone.", [b1(), b2()], TOC, ("NEXT · CHAPTER 12", "Your next steps"))
    return body, W, None
