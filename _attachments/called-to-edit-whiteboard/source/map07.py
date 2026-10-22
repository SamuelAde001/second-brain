"""Chapter 7 as a map: from practice to paid."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map07-practice", 5400


def b1():
    items = [
        row([note(0, 0, 340, big("3", 300)),
             note(0, 0, 1300, '<span style="font:800 46px/1.2 \'Plus Jakarta Sans\';color:#fff">full videos in your niche, start to finish.</span><br><br>When you\'ve done that, you\'re good enough to charge. A lot of people wait too long because they\'re learning nuggets, and <b>never finish a full project.</b>')], 40, "align-items:center"),
        lab2("The ladder from practice to paid"),
        row(steps("l", [("Practice videos", "Two or three of your own, like talking heads of yourself.", "clapperboard", "dim"),
                        ("Real people's videos, for free", "Quickly move to this. As soon as possible.", "users", ""),
                        ("Ask for a token", "If they're enjoying your work, tell them you'd love to be paid a token.", "hand-coins", ""),
                        ("Charge", "Someone sees your work and asks, &ldquo;How much do you charge?&rdquo;", "badge-dollar-sign", "gold")],
                  d="row", gap=70, reveal=["Step 1", "Step 2", "Step 3", "Step 4"]), 70),
        quote_(0, 0, 1700, "At that point, don't tell the person, \"I'm not ready.\"", 70),
    ]
    return B(1, "7.1", "When are you good enough to charge?", "flag", items, "There's no real time. It's your skill level.", "l0")


def b2():
    who = [("A friend who owns a business", "&ldquo;Record a video for your business. Let me help you edit it so you can post it.&rdquo;", "store"),
           ("An event you attend", "Capture the event, edit it, and show them so they can use it.", "calendar"),
           ("Small businesses around you", "They don't have big budgets for a video editor.", "map-pin"),
           ("Small creators", "A friend creating the kind of content you want to edit.", "user")]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Real projects, real consequences,</span><br>' + big("real people.", 110)),
        row([L("j0", "Your own practice video", "There's no deadline. You can be practising on one video for one whole month.", "hourglass", "dim", "auto", "flex:1"),
             rv(L("j1", "A real person's project", "You know he's going to post it tomorrow. It will make you stay up late at night. That pressure is what makes you learn.", "flame", "gold", "auto", "flex:1"), "The difference?", "flex:1;display:flex")], 90),
        lab2("Who you can edit for, for free"),
        row([L(f"w{k}", h, b, ic, "", "auto", "flex:1") for k, (h, b, ic) in enumerate(who[:2])], 30),
        row([L(f"w{k+2}", h, b, ic, "", "auto", "flex:1") for k, (h, b, ic) in enumerate(who[2:])], 30),
    ]
    edge("j0", "j1", "gold", sa="r", sb="l", label="vs")
    return B(2, "7.2", "Work on real projects", "zap", items, "My number one way to learn")


def b3():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Offering for free is the best way to start.</span><br>' + big("But quickly move to paid.", 100)),
        row(steps("k", [("Free", "The best way to start.", "gift", ""),
                        ("Then low pay", "Even if it's 5K, 10K. Working for free, you still need data and electricity.", "coins", ""),
                        ("Then paid", "After four, five free projects for someone, you need to start moving to paid.", "badge-dollar-sign", "gold")], d="row", gap=90), 90),
        L("k8", "Don't work for free for one year", "Give a time frame or a number of videos. Then the person already knows: either you leave, or he pays you.", "ban", "dim"),
        journey("A video editor once worked for me for free for a whole month. After that month, I started paying the person."),
        rv(col([bub("k9", "Sir, please, can I edit your videos for one month for free? I'm trying to build my portfolio and I'm looking for more work. I would love to partner with you.", True, "What to say"),
                note(0, 0, 200, '<b>or</b>'),
                bub("k10", "Let me do five videos for you, for free.", True, "", "fit-content")], 20), "What to say"),
        remember("Don't tell the person you're learning. Just say you're trying to build your portfolio."),
    ]
    return B(3, "7.3", "Work for free without getting stuck", "gift", items, "Give a scope and a time range", "k0")


def b4():
    gains = [("Testimonials", "When people see the good work, they won't even know it was free.", "message-square-quote"), ("A portfolio", "Client results you can show.", "folder-open"),
             ("Experience", "People will ask you how many years of experience.", "calendar"), ("Confidence", "You know you can do it.", "badge-check"),
             ("Referrals", "The people you edit for refer you.", "users"), ("Sharper skills", "You get better on every project.", "scissors")]
    left = [rv(L(f"g{k}", h, b, ic, "", 560), "?") for k, (h, b, ic) in enumerate(gains[:3])]
    right = [rv(L(f"g{k+3}", h, b, ic, "", 560), "?") for k, (h, b, ic) in enumerate(gains[3:])]
    hubn = node("gh", 0, 0, 420, '<div class="spk" style="width:380px;height:380px">Free<br>work</div>', "", "display:flex;justify-content:center")
    for k in range(3):
        edge("gh", f"g{k}", "gold", sa="l", sb="r", bend=0.3)
        edge("gh", f"g{k+3}", "gold", sa="r", sb="l", bend=0.3)
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Free work has more benefits for you</span><br>' + big("than you think.", 110)),
        row([col(left, 40), col([hubn], 0, None, "justify-content:center"), col(right, 40)], 80, "justify-content:center"),
        journey("I used to say I have five years of experience. Three of those years, I was mostly working for free. At most I was earning &#8358;25,000. But no one knows that."),
        remember("You have to learn to humble yourself and work for free. Most people think they need to get paid. You want to get better."),
    ]
    return B(4, "7.4", "What free work gives you", "gift", items, "More than you think")


TOC = [("7.1", "When are you good enough to charge?"), ("7.2", "Work on real projects"), ("7.3", "Work for free without getting stuck"), ("7.4", "What free work gives you")]


def build():
    reset()
    body = assemble("7", "From practice to", "Paid", "Finish three full videos in your niche. Then move to real people's videos. Free at first, then a token, then paid.",
                    "When you can finish a full video from beginning to end, you're good enough to charge.", [b1(), b2(), b3(), b4()], TOC,
                    ("NEXT · CHAPTER 8", "Get seen"))
    return body, W, None
