"""Chapter 7 as a map: from practice to paid."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map07-practice", 5400


def b1():
    items = [
        row([note(0, 0, 340, big("3", 300)),
             note(0, 0, 1300, '<span style="font:800 46px/1.2 \'Plus Jakarta Sans\';color:#fff">full videos in your niche, start to finish.</span><br><br>Then you\'re ready to charge. Most people wait too long because they <b>never finish a whole project</b>: they learn nuggets, not full videos.')], 40, "align-items:center"),
        lab2("The ladder from practice to paid"),
        row(steps("l", [("Practice videos", "Your own, like 2-3 talking heads of yourself", "clapperboard", "dim"),
                        ("Real people's videos, free", "As soon as possible", "users", ""),
                        ("Ask for a token", "If they're enjoying it", "hand-coins", ""),
                        ("Charge", "Someone sees your practice and asks &ldquo;How much do you charge?&rdquo;", "badge-dollar-sign", "gold")],
                  d="row", gap=70, reveal=["Step 1", "Step 2", "Step 3", "Step 4"]), 70),
        quote_(0, 0, 1700, "Don't say \"I'm not ready.\"", 70),
    ]
    return B(1, "7.1", "When you're ready", "flag", items, "Three full videos", "l0")


def b2():
    who = [("A friend who owns a business", "&ldquo;Record a video, let me edit it so you can post it.&rdquo;", "store"),
           ("An event you attend", "Capture it, edit it, show them.", "calendar"),
           ("Small businesses near you", "Without an editor budget.", "map-pin"),
           ("Small creators", "Making content in your style.", "user")]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Real projects, real consequences,</span><br>' + big("real people.", 110)),
        row([L("j0", "Your practice video · No deadline", "You can spend a whole month on one video. Nothing is at stake.", "hourglass", "dim", "auto", "flex:1"),
             rv(L("j1", "A real project · They post it tomorrow", "You try your best not to make mistakes. It keeps you up late.", "flame", "gold", "auto", "flex:1"), "The difference: pressure", "flex:1;display:flex")], 90),
        lab2("Who to edit for, free"),
        row([L(f"w{k}", h, b, ic, "", "auto", "flex:1") for k, (h, b, ic) in enumerate(who[:2])], 30),
        row([L(f"w{k+2}", h, b, ic, "", "auto", "flex:1") for k, (h, b, ic) in enumerate(who[2:])], 30),
    ]
    edge("j0", "j1", "gold", sa="r", sb="l", label="vs")
    return B(2, "7.2", "Why real projects teach fastest", "zap", items, "Pressure teaches")


def b3():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Free first.</span><br>' + big("Don't get stuck there.", 110)),
        row(steps("k", [("Free", "The best way to start.", "gift", ""),
                        ("Low pay next", "Even NGN 5,000 or 10,000. It funds what learning costs: data and electricity.", "coins", ""),
                        ("Paid", "After 4 or 5 free projects for one person, unless you have an agreement.", "badge-dollar-sign", "gold")], d="row", gap=90), 90),
        L("k8", "Never &ldquo;free for a year&rdquo;.", "Set the scope up front.", "ban", "dim"),
        journey("An editor once worked for me free for a whole month. After that, I started paying them."),
        rv(col([bub("k9", "Sir, please, can I edit your videos for one month for free? I'm trying to build my portfolio and I'm looking for more work. I would love to partner with you.", True, "The scope ask"),
                note(0, 0, 200, '<b>or</b>'),
                bub("k10", "Let me do five videos for you, for free.", True, "", "fit-content")], 20), "What to say"),
        remember("Don't tell them you're learning. Tell them you're building your portfolio."),
    ]
    return B(3, "7.3", "Work for free without getting stuck", "gift", items, "Set the scope", "k0")


def b4():
    gains = [("Testimonials", "People won't know it was free.", "message-square-quote"), ("A portfolio", "Real work to show.", "folder-open"),
             ("Experience", "Years that count.", "calendar"), ("Confidence", "You've done it before.", "badge-check"),
             ("Referrals", "Happy people talk.", "users"), ("Sharper skills", "Pressure teaches.", "scissors")]
    left = [rv(L(f"g{k}", h, b, ic, "", 560), "?") for k, (h, b, ic) in enumerate(gains[:3])]
    right = [rv(L(f"g{k+3}", h, b, ic, "", 560), "?") for k, (h, b, ic) in enumerate(gains[3:])]
    hubn = node("gh", 0, 0, 420, '<div class="spk" style="width:380px;height:380px">Free<br>work</div>', "", "display:flex;justify-content:center")
    for k in range(3):
        edge("gh", f"g{k}", "gold", sa="l", sb="r", bend=0.3)
        edge("gh", f"g{k+3}", "gold", sa="r", sb="l", bend=0.3)
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">What free work</span><br>' + big("gives you.", 110)),
        row([col(left, 40), col([hubn], 0, None, "justify-content:center"), col(right, 40)], 80, "justify-content:center"),
        remember("You have to learn to humble yourself and work for free. Most people think they need to get paid. You want to get better."),
    ]
    return B(4, "7.4", "What free work gives you", "gift", items, "Six things money can't buy yet")


TOC = [("7.1", "When you're ready"), ("7.2", "Why real projects teach fastest"), ("7.3", "Work for free without getting stuck"), ("7.4", "What free work gives you")]


def build():
    reset()
    body = assemble("7", "From practice to", "Paid", "Finish three full videos in your niche. Then get onto real people's videos: free at first, then a token, then paid.",
                    "When you can finish a full video from beginning to end, you're good enough to charge.", [b1(), b2(), b3(), b4()], TOC,
                    ("NEXT · CHAPTER 8", "Get seen"))
    return body, W, None
