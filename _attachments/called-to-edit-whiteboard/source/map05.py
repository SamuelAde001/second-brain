"""Chapter 5 as a map: your tools and the money to start."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map05-tools", 5400


def chips(xs, cls=""):
    return "".join(f'<span class="chip {cls}" style="position:static;display:inline-block;margin:6px 8px 0 0;font-size:23px;padding:9px 20px">{x}</span>' for x in xs)


def b1():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Your niche and your hardware</span><br>' + big("pick your software.", 96)),
        row([col([L("p0", "On a phone", chips(["CapCut", "Premiere Pro mobile", "Edits"], "gold") + "<br><br>Free to start, with paid tiers. Great for short form, captions and simple social videos.", "smartphone", "navy"),
                  L("p1", "Loses on", "Long-form YouTube · Motion graphics · Heavy animation", "circle-x", "dim"),
                  rv(L("p2", "Wins on", "Event recaps · Simple short form · Talking heads cut into shorts · Captions, overlays, screenshots", "circle-check", "gold"), "Wins on…")], 30, None, "flex:1"),
             col([L("q0", "On a laptop", chips(["DaVinci Resolve", "Premiere Pro + After Effects", "CapCut Desktop", "Final Cut (Mac)"], "gold") + "<br><br>Needed for long form, colour and motion.", "laptop", "navy"),
                  L("q1", "Resolve", "Free, a great all-rounder, especially colour grading. Needs a laptop that can run it.", "", ""),
                  L("q2", "Premiere + After Effects", "The best for heavy motion design. Paid.", "", ""),
                  L("q3", "CapCut", "The free version is enough to get paid work. Most pro tools need Pro.", "", "")], 30, None, "flex:1")], 60),
    ]
    edge("t1", "p0", "line", sa="b", sb="t")
    edge("t1", "q0", "line", sa="b", sb="t")
    return B(1, "5.1", "Phone or laptop", "smartphone", items, "Your hardware decides")


def b2():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Never use</span><br>' + big("cracked software.", 110)),
        journey("I once used a cracked copy of Premiere Pro while trying to move away from Resolve. I'm not joking: <b>my computer was hacked, and it affected my client work.</b> I went straight back to Resolve."),
        row([L("c0", "Phone editors: pay for CapCut Pro", "No money? Borrow it for the first subscription, then work hard that month to earn the next one.", "smartphone", "", "auto", "flex:1"),
             L("c1", "AI tools depend on your niche", "I pay for Claude now. A beginner shouldn't pay for a tool they don't need.", "bot", "", "auto", "flex:1")], 40),
        rv(quote_(0, 0, 1700, "Whatever you pay for a subscription is your capital.", 70), "Your subscription is…"),
        note(0, 0, 1700, 'Once you see it that way: <b>&ldquo;I\'m already spending capital, I need to start making profit.&rdquo;</b> That pushes you to pitch.'),
    ]
    return B(2, "5.2", "Invest in your software", "shield-check", items, "Never cracked")


def b3():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">You can start for free.</span><br>' + big("But it's not really free.", 100)),
        row([L("m0", "Data", "", "wifi", "", "auto", "flex:1"), L("m1", "Power", "", "zap", "", "auto", "flex:1"), L("m2", "Device", "", "laptop", "", "auto", "flex:1")], 40),
        note(0, 0, 1700, 'Even a phone editor needs data to watch tutorials, download, upload and show their work, and power to keep going. <b>No fixed price to start:</b> it varies by country and by what you own.'),
        row(steps("n", [("Months 1–2", "Capital: an investment", "piggy-bank", "dim"), ("Paid clients cover it", "Then you break even", "scale", ""), ("Profit", "", "trending-up", "gold")],
                  d="row", gap=90, reveal=[None, "Then…", "Then…"]), 90),
    ]
    return B(3, "5.3", "What editing really costs", "wallet", items, "Capital, then profit", "m0")


def b4():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">For DaVinci Resolve,</span><br>' + big("the minimum.", 110)),
        row([L("r0", "16 GB RAM", "", "memory-stick", "gold", "auto", "flex:1"), L("r1", "An SSD", "", "hard-drive", "gold", "auto", "flex:1"), L("r2", "A dedicated GPU", "", "cpu", "gold", "auto", "flex:1")], 40),
        row([L("r3", "Buy a laptop you can upgrade", "I upgraded RAM instead of buying new laptops.", "wrench", "", "auto", "flex:1"),
             L("r4", "Mac (M1 and newer)", "is the best for editing. I couldn't afford one, so I used Windows.", "apple", "dim", "auto", "flex:1")], 40),
        lab2("Don't wait for the perfect machine"),
        note(0, 0, 1700, 'Some wait until they earn NGN 1 million for their first laptop. That takes a while.'),
        row([L("u0", "Can only afford", big("NGN 300,000", 64) + "<br>~USD 220. Buy it and use it…", "laptop", "", "auto", "flex:1"),
             L("u1", "…until you can move to", big("NGN 600,000", 64, NAVY) + "<br>~USD 450.", "laptop", "gold", "auto", "flex:1")], 90),
        rv(remember("Don't spend your editing money on yourself yet. Putting my earnings back into my tools was one of the fastest ways I grew."), "Where your first money goes"),
    ]
    edge("u0", "u1", "gold", sa="r", sb="l")
    return B(4, "5.4", "The computer you need", "cpu", items, "The minimum", "r1")


TOC = [("5.1", "Phone or laptop"), ("5.2", "Invest in your software"), ("5.3", "What editing really costs"), ("5.4", "The computer you need")]


def build():
    reset()
    body = assemble("5", "Your tools and the", "Money to start", "Start on what you can afford, never on cracked software, and treat every cost as capital you will earn back.",
                    "Whatever you pay for a subscription is your capital.", [b1(), b2(), b3(), b4()], TOC,
                    ("NEXT · CHAPTER 6", "Learn the skill the right way"))
    return body, W, None
