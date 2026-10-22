"""Chapter 5 as a map: your tools and the money to start."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map05-tools", 5400


def chips(xs, cls=""):
    return "".join(f'<span class="chip {cls}" style="position:static;display:inline-block;margin:6px 8px 0 0;font-size:23px;padding:9px 20px">{x}</span>' for x in xs)


def b1():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Your niche and the hardware you have</span><br>' + big("decide your software.", 96)),
        row([col([L("p0", "On a phone", chips(["CapCut", "Premiere Pro mobile", "Edits"], "gold") + "<br><br>All of them are free to start. I use the Edits app on my phone, especially when I want Instagram music.", "smartphone", "navy"),
                  L("p1", "Where a phone struggles", "Long form YouTube, motion graphics, heavy animation. You can't do proper colour grading on a phone.", "circle-x", "dim"),
                  rv(L("p2", "Where a phone is enough", "Event recaps, simple short form, talking heads cut into shorts, captions, overlays and screenshots.", "circle-check", "gold"), "Phone is enough for…")], 30, None, "flex:1"),
             col([L("q0", "On a laptop", chips(["DaVinci Resolve", "Premiere Pro + After Effects", "CapCut Desktop", "Final Cut (Mac)"], "gold") + "<br><br>Final Cut is mostly on Mac. Your hardware decides which one you can run.", "laptop", "navy"),
                  L("q1", "DaVinci Resolve", "Free, and a great all-rounder, especially colour grading. It's what I started with. I used the free version for client work for two, three years before I paid for it. It's a ladder.", "", ""),
                  L("q2", "Premiere Pro and After Effects", "If you want to do crazy motion design stuff, they work best. They're paid.", "", ""),
                  L("q3", "CapCut", "CapCut is enough to get you paid work. But from my experience, a lot of the major tools you need are in the paid version.", "", "")], 30, None, "flex:1")], 60),
    ]
    edge("t1", "p0", "line", sa="b", sb="t")
    edge("t1", "q0", "line", sa="b", sb="t")
    return B(1, "5.1", "Phone or laptop", "smartphone", items, "Your hardware decides")


def b2():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Let me tell you the truth.</span><br>' + big("Don't use cracked software.", 100)),
        journey("I wanted to move from Resolve to Premiere Pro, so I used a cracked version. Not joking, <b>I was hacked on my computer, and it affected my work.</b> I had to go back to Resolve."),
        row([L("c0", "On your phone? Pay for CapCut Pro", "If you don't have the money, borrow for the first subscription. Then work hard that month so you can earn the next one. That's how you build things.", "smartphone", "", "auto", "flex:1"),
             L("c1", "AI tools depend on your niche", "I pay for Claude now, but as a beginner, don't pay for what you don't really need. If a tool helps your niche, like cutting long form into shorts, invest in it and quickly make a profit.", "bot", "", "auto", "flex:1")], 40),
        rv(quote_(0, 0, 1700, "Whatever you pay for a subscription is your capital.", 70), "Your subscription is…"),
        note(0, 0, 1700, 'Look at this as a business. You\'ll quickly know: <b>&ldquo;Oh boy, I\'m already spending capital. I need to start making profit.&rdquo;</b> That\'s what speeds up your pitching.'),
    ]
    return B(2, "5.2", "Invest in your software", "shield-check", items, "If you really want to do this thing")


def b3():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">You can start for free.</span><br>' + big("But it's not really free.", 100)),
        row([L("m0", "Data", "To watch tutorials, download, upload, and show your work.", "wifi", "", "auto", "flex:1"),
             L("m1", "Electricity", "I had to buy a generator and fuel it. Now solar, inverters.", "zap", "", "auto", "flex:1"),
             L("m2", "The rest", "Software, storage, headphones, a mic. All these things are expensive.", "laptop", "", "auto", "flex:1")], 40),
        note(0, 0, 1700, 'I\'m not giving a specific price, because everything varies. <b>If you already have a phone and you can afford data, then start.</b>'),
        row(steps("n", [("The first one or two months", "Everything you spend is capital. You're investing in your business.", "piggy-bank", "dim"),
                        ("Get your first paid client", "As soon as possible. Paid clients relieve you of the cost.", "scale", ""),
                        ("You break even, then profit", "", "trending-up", "gold")],
                  d="row", gap=90, reveal=[None, "Then…", "Then…"]), 90),
        journey("I invested a lot in my first laptop, &#8358;150,000 as of then. Look at it all as an investment."),
    ]
    return B(3, "5.3", "Video editing is expensive", "wallet", items, "It's all an investment", "m0")


def b4():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">To run DaVinci Resolve, you should at least have</span><br>' + big("this.", 110)),
        row([L("r0", "16 GB RAM", "", "memory-stick", "gold", "auto", "flex:1"), L("r1", "An SSD", "", "hard-drive", "gold", "auto", "flex:1"), L("r2", "A dedicated GPU", "", "cpu", "gold", "auto", "flex:1")], 40),
        row([L("r3", "Buy a laptop you can upgrade", "There was a time my laptop had 8 gigs of RAM. Instead of buying a new laptop, I upgraded the RAM.", "wrench", "", "auto", "flex:1"),
             L("r4", "The best laptops for editing are Macs", "The M1 Apple Macs and newer. I couldn't afford a MacBook, so I used a normal Windows laptop.", "apple", "dim", "auto", "flex:1")], 40),
        journey("It's a ladder. My first laptop had 4 gigs of RAM. My second had 8, which I upgraded to 16. My third came with 16 and I upgraded it to 64. Now I use a PC with a big RTX GPU."),
        lab2("Don't wait till you have all the money"),
        note(0, 0, 1700, 'Some people say, &ldquo;I\'m going to wait till I earn 1 million before I buy my first laptop.&rdquo; It will take a while.'),
        row([L("u0", "If all you can afford is", big("&#8358;300,000", 64) + "<br>Buy it. Use it…", "laptop", "", "auto", "flex:1"),
             L("u1", "…till you can upgrade to", big("&#8358;600,000", 64, NAVY), "laptop", "gold", "auto", "flex:1")], 90),
        rv(remember("Don't spend your video editing money on yourself yet. Spend it on your tools. That was one of the fastest ways I grew."), "Where your first money goes"),
    ]
    edge("u0", "u1", "gold", sa="r", sb="l")
    return B(4, "5.4", "The computer you need", "cpu", items, "A bad laptop will frustrate your editing life", "r1")


TOC = [("5.1", "Phone or laptop"), ("5.2", "Invest in your software"), ("5.3", "Video editing is expensive"), ("5.4", "The computer you need")]


def build():
    reset()
    body = assemble("5", "Your tools and the", "Money to start", "Start with what you have. Invest in your tools as you earn. Look at this as a business.",
                    "Whatever you pay for a subscription is your capital.", [b1(), b2(), b3(), b4()], TOC,
                    ("NEXT · CHAPTER 6", "Learn the skill the right way"))
    return body, W, None
