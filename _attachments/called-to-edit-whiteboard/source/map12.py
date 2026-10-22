"""Chapter 12 as a map: your next steps, the Community, questions."""
from maplib import *
from lib import rv, icon, remember, NAVY, CH, MIST

NAME, W = "map12-close", 5400


def b1():
    hw = [("Write your offer sentence: who you help, what result, how, how fast", "4"), ("Make your learning list. Learn the first skill and implement it", "6"),
          ("Finish three full videos in your niche", "7"), ("Curate your feed around your niche. Lock in for a month", "8"),
          ("Fix your profile. Build your portfolio website", "8"), ("Post 2 to 3 times a day: 40% authentic, 40% authority, 20% sales", "8"),
          ("Do one warm outreach", "9"), ("Start your dream client list: 20 to 50 names", "9"), ("Write your rate card", "10"),
          ("Ask a past client for a testimonial", "11"), ("Start engaging editors at your level", "11")]
    rows_ = [node(f"h{k}", 0, 0, "auto", f'<div style="width:44px;height:44px;border:4px solid #FCDD9E;border-radius:10px;flex:none"></div>'
                  f'<div class="lh" style="flex:1;font-size:28px">{t}</div><span class="chip dim" style="position:static;font-size:20px;padding:6px 16px">Ch {c}</span>',
                  "leaf", "align-items:center;padding:18px 26px") for k, (t, c) in enumerate(hw)]
    items = [note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Tick them off in order.</span><br>' + big("Your homework.", 110)), col(rows_, 16)]
    return B(1, "12.1", "Your homework", "list-checks", items, "Start with these", "h0")


def b2():
    figs = [("3", "full videos in your niche before you charge"), ("4–5", "free projects for one person, then move to paid"), ("2–3", "posts a day: 40 / 40 / 20"),
            ("8", "videos at most in your portfolio"), ("20–50", "names on your dream client list"), ("1K–20K", "followers: the Instagram creators to target"),
            ("4–5", "posts you comment on before you DM"), ("30s", "the longest a value-first edit should be"), ("4", "follow-ups at most: 24 h, 2 days, 1 week"),
            ("30%", "upfront, with a signed contract"), ("1–3", "months of consistency before clients come")]
    tiles = [node(f"n{k}", 0, 0, "auto", big(n, 76) + f'<div class="lb">{t}</div>', "leaf", "flex:1;flex-direction:column;gap:6px") for k, (n, t) in enumerate(figs)]
    items = [note(0, 0, 1700, big("The numbers to remember.", 76)),
             row(tiles[0:3], 24), row(tiles[3:6], 24), row(tiles[6:9], 24),
             row(tiles[9:] + [node("n11", 0, 0, "auto", big("Be patient.", 76, NAVY), "leaf gold", "flex:1;align-items:center")], 24)]
    return B(2, "12.2", "The numbers", "hash", items, "To remember")


def b3():
    lines = ["A diamond is as valuable as it is visible.", "You learn the skill. You sell the service.", "If you are targeting everyone, you have no one.",
             "Don't learn without implementation.", "Your practice work is your work.", "They want to see experience, not knowledge."]
    items = [quote_(0, 0, 1700, t, 60) for t in lines]
    return B(3, "12.3", "Lines to keep", "quote", items, "Write them down")


def b4():
    inside = [("Feedback from me", "On your emails, your outreach and your profile.", "message-square"), ("Calls with me", "Inside the community.", "video"),
              ("The 60-day challenge", "One or two activities at a time. I'll give feedback, correct you and guide you properly.", "flame"),
              ("Editors at your level", "Everyone supporting each other.", "users")]
    items = [
        row([col([note(0, 0, 1100, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">You can\'t do video editing alone.</span><br>' + big("Join the Called to Edit Community.", 76))], 0, 1150),
             col([f'<img src="kit/called-to-edit-community-dark.svg" style="width:520px">'], 0, 560, "justify-content:center")], 40, "align-items:center"),
        note(0, 0, 1700, 'When you start putting this into practice, you\'ll have questions. You\'ll want feedback on your emails, your outreach, your profile and your niche.'),
        row([rv(L(f"c{k}", h, b, ic, "", "auto", "flex:1"), "Inside…", "flex:1;display:flex") for k, (h, b, ic) in enumerate(inside[:2])], 30),
        row([rv(L(f"c{k+2}", h, b, ic, "", "auto", "flex:1"), "Inside…", "flex:1;display:flex") for k, (h, b, ic) in enumerate(inside[2:])], 30),
        rv(L("c8", big("&#8358;5,000", 120, NAVY), "<b>a month.</b> Even if you didn't come for the webinar, you can join.", "", "gold"), "The price"),
        L("c9", "Called to Edit Academy", "<b>Coming soon.</b>", "graduation-cap", "navy"),
    ]
    return B(4, "12.4", "Called to Edit Community", "users-round", items, "Learn with me")


def b5():
    items = [note(0, 0, 1700, big("Your turn.", 140) + '<br><span style="font:800 70px \'Plus Jakarta Sans\';color:#fff">Questions</span>'),
             row([f'<img src="kit/samuel-cutout-sm.webp" style="width:520px">',
                  col([note(0, 0, 900, f'<div style="display:flex;gap:20px;align-items:center">{icon("instagram", 70)}<span style="font:800 56px \'Plus Jakarta Sans\';color:#FCDD9E">@SamuelSignals</span></div>'),
                       f'<img src="kit/called-to-edit-logo-dark.svg" style="width:460px">'], 50, 1000, "justify-content:center")], 60)]
    return B(5, "12.5", "Questions", "circle-help", items, "Over to you")


TOC = [("12.1", "Your homework"), ("12.2", "In figures"), ("12.3", "Lines to keep"), ("12.4", "Called to Edit Community"), ("12.5", "Questions")]


def build():
    reset()
    body = assemble("12", "Your next", "Steps", "Now it's time to put it into practice. This is what to do, in order.",
                    "Let us get into it.", [b1(), b2(), b3(), b4(), b5()], TOC)
    return body, W, None
