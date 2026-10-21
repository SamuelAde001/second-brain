"""Chapter 10 as a map: price yourself and get paid."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map10-price", 5400


def b1():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">A lot of us price ourselves wrongly.</span><br>' + big("Count per video.", 110)),
        row([rv(L("a0", "Per video ✓", "Per project. How freelancers charge.", "circle-check", "gold", "auto", "flex:1"), "Right or wrong?", "flex:1;display:flex"),
             rv(L("a1", "Per month ✗", "That's a salary. Companies pay wages.", "circle-x", "dim", "auto", "flex:1"), "Right or wrong?", "flex:1;display:flex"),
             rv(L("a2", "Per minute ✗", "Length doesn't measure the work.", "circle-x", "dim", "auto", "flex:1"), "Right or wrong?", "flex:1;display:flex")], 30),
        note(0, 0, 1700, 'A one-minute video can have as much work as a 20-minute video. <b>If a client offers to pay per minute, don\'t take that deal.</b>'),
    ]
    return B(1, "10.1", "How you count", "calculator", items, "Per video", "a0")


def b2():
    tiers = [("Under 20 minutes", "Simple cut, talking head, a few captions"), ("Under 20 minutes", "Motion graphics, B-roll, research from me"), ("Over 20 minutes", "Motion graphics")]
    card = ('<div class="mock"><div class="mh">Rate card · mine, as a long-form editor</div>' + "".join(
        f'<div style="display:flex;gap:22px;align-items:center;padding:16px 0;border-top:2px solid #DDE2EC"><span style="font-family:Gloock;font-size:52px;color:#8A5E17;width:50px">{k+1}</span>'
        f'<div style="flex:1"><b style="font-size:28px">{h}</b><br>{b}</div><span style="font:800 24px \'Plus Jakarta Sans\';border:3px dashed #B9C3D6;border-radius:12px;padding:10px 18px;color:#4A5670">your price</span></div>'
        for k, (h, b) in enumerate(tiers)) + '</div>')
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">One card that shows</span><br>' + big("your price tiers.", 110)),
        node("b0", 0, 0, "auto", card, ""),
        note(0, 0, 1700, 'The client sees what changes the price, and you can budget around it together. <b>What sets your number:</b> skill, confidence, the kind of client.'),
        row([rv(L("b1", "A beginner, learning", big("$5–10", 80) + "<br>per short-form video, for simple work you're learning on", "sprout", "", "auto", "flex:1"), "Beginner?", "flex:1;display:flex"),
             rv(L("b2", "Good international clients", big("$20–30", 80, NAVY) + "<br>per short-form video, what they used to pay", "globe", "gold", "auto", "flex:1"), "International?", "flex:1;display:flex")], 90),
    ]
    edge("b1", "b2", "gold", sa="r", sb="l")
    return B(2, "10.2", "Have a rate card", "id-card", items, "Your tiers", "b0")


def b3():
    f = ["Skill and confidence", "The client's business", "What the video is for", "The work inside it", "Niche and length", "Revisions", "The result you get them"]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">There is no fixed price.</span><br>' + big("It's a mixing desk.", 110)),
        row([col([chip(f"m{k}", 0, 0, t) for k, t in enumerate(f)], 22, 620, "align-items:flex-start"),
             col([node("mp", 0, 0, 440, '<div class="spk" style="width:400px;height:400px">Your<br>price</div>', "", "display:flex;justify-content:center")], 0, 460, "justify-content:center")], 200, "justify-content:center"),
        lab2("Take control of the price"),
        row([L("m8", "Ask questions first", "&ldquo;Do you want motion graphics? What style? What do you want to achieve?&rdquo;", "circle-help", "", "auto", "flex:1"),
             L("m9", "When they say it's too much, explain why", "&ldquo;There's motion graphics in this.&rdquo;", "message-circle", "", "auto", "flex:1")], 30),
        L("m10", "Price on a call, so you can negotiate properly.", "Paid adverts and business videos are tied to money: <b>always charge more</b>. Set revisions in the deal, e.g. &ldquo;3 rounds of revisions&rdquo;.", "phone-call", "navy"),
        remember("Don't be afraid of no's. Don't be afraid of rejection. It's part of the journey."),
    ]
    for k in range(len(f)):
        edge(f"m{k}", "mp", "line", sa="r", sb="l", bend=0.4, arrow=False)
    return B(3, "10.3", "What moves your price", "sliders-horizontal", items, "A mixing desk")


def b4():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">It\'s easier to sell a package</span><br>' + big("than one video.", 110)),
        row([rv(L("p0", "Long-form package", big("$5,000", 96, NAVY) + "<br><b>5 long-form videos a month</b>", "film", "gold", "auto", "flex:1"), "Long-form package", "flex:1;display:flex"),
             rv(L("p1", "Short-form package", big("$3,000", 96, NAVY) + "<br><b>30 short-form videos a month</b>", "smartphone", "gold", "auto", "flex:1"), "Short-form package", "flex:1;display:flex")], 40),
        L("p2", "Mine now", "3 to 6 videos a month for my client, paid at the end of the month.", "user-round-check", ""),
        L("p3", "Packages need a retainer client", "Someone who posts consistently and works with you long term.", "repeat", "navy"),
        rv(L("p4", "Add-ons", "Ideation (only if you really know how), scripting or thumbnails, so the client pays <b>USD 1,000 instead of USD 500</b>.", "plus", "gold"), "Add-ons"),
    ]
    return B(4, "10.4", "Stop collecting single projects", "package", items, "Packages", "p0")


def b5():
    agr = ('<div class="mock"><div class="mh">Agreement · example</div>5 videos a month<br>30% paid upfront for the 5<br>Balance paid on delivery<br>3 rounds of revisions per video'
           '<div style="display:flex;gap:40px;margin-top:26px"><div style="flex:1;border-top:3px solid #0A1F44;padding-top:8px;font-weight:700">Client signature</div><div style="flex:1;border-top:3px solid #0A1F44;padding-top:8px;font-weight:700">Editor signature</div></div></div>')
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">The scam is simple:</span><br>' + big("Deliver. Never paid.", 110)),
        row(steps("s", [("Deliver", "", "send", "dim"), ("Never paid", "", "circle-x", "dim")], d="row", gap=90, kind="mist"), 90),
        rv(L("s5", big("30%", 120, NAVY), "<b>upfront before you start.</b> On a new bundle, always. 20 or 30 videos a month with a new client? Don't wait until all are done for the first payment.", "", "gold"), "Before you start…"),
        row([L("s6", "Write a contract and have them sign it.", "Not something they said or typed in a chat. A long-time client can pay at the end of the month. Mine does.", "file-pen-line", "", 760),
             node("s7", 0, 0, 900, agr, "")], 40),
    ]
    edge("s6", "s7", "gold", sa="r", sb="l")
    return B(5, "10.5", "Don't get scammed", "shield-alert", items, "30% upfront", "s0")


def b6():
    ways = [("Cleva", "Mine. A US dollar account; convert to naira. Small deposit fee.", "gold"), ("Grey", "USD, GBP and EUR accounts. Good for UK and EU clients.", ""),
            ("Raenest", "A USD account built for freelancers.", ""), ("Payoneer", "For Fiverr, Upwork and clients who use it. Usually dearest into naira.", ""),
            ("PayPal", "Not a way to get paid in Nigeria: mostly for paying, not receiving.", "dim")]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">What works depends on where you live</span><br>' + big("and where your client is.", 92)),
        row([L(f"w{k}", h, b, "landmark", c, "auto", "flex:1") for k, (h, b, c) in enumerate(ways[:3])], 24),
        row([L(f"w{k+3}", h, b, "landmark", c, "auto", "flex:1") for k, (h, b, c) in enumerate(ways[3:])], 24),
        journey("Receiving payment in Nigeria from abroad has been very difficult. I've used Payoneer, then Grey, and for the past two years <b>Cleva</b>."),
        note(0, 0, 1700, 'US clients pay differently from Canadian ones. Ask people near you who already earn online. <b>Fees change: check inside the app.</b> (October 2026)'),
    ]
    return B(6, "10.6", "Getting paid from abroad", "globe", items, "Where you live decides")


TOC = [("10.1", "How you count"), ("10.2", "Have a rate card"), ("10.3", "What moves your price"),
       ("10.4", "Stop collecting single projects"), ("10.5", "Don't get scammed"), ("10.6", "Getting paid from abroad")]


def build():
    reset()
    body = assemble("10", "Price yourself and", "Get paid", "Price per video from a rate card, price what the video is worth to the client, get to packages fast, and protect yourself.",
                    "Stop collecting single projects.", [b1(), b2(), b3(), b4(), b5(), b6()], TOC,
                    ("NEXT · CHAPTER 11", "Grow through people"))
    return body, W, None
