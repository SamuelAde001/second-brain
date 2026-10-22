"""Chapter 10 as a map: price yourself and get paid."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map10-price", 5400


def b1():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">A lot of us price ourselves wrongly.</span><br>' + big("Charge per video.", 110)),
        row([rv(L("a0", "Per video ✓", "Per project. If you're working as a freelancer, charge per video.", "circle-check", "gold", "auto", "flex:1"), "Right or wrong?", "flex:1;display:flex"),
             rv(L("a1", "Per month ✗", "That's like a salary. Corporate organisations pay monthly wages.", "circle-x", "dim", "auto", "flex:1"), "Right or wrong?", "flex:1;display:flex"),
             rv(L("a2", "Per minute ✗", "I always advise against it. The timing doesn't measure the work.", "circle-x", "dim", "auto", "flex:1"), "Right or wrong?", "flex:1;display:flex")], 30),
        note(0, 0, 1700, 'A one minute video can have as much work as a 20 minute video. <b>Some people will tell you, &ldquo;I\'ll pay you per minute.&rdquo; I always advise against it.</b>'),
    ]
    return B(1, "10.1", "How to charge", "calculator", items, "Per video, not per minute", "a0")


def b2():
    tiers = [("Under 20 minutes", "Simple cut, talking head, a few captions"), ("Under 20 minutes", "Motion graphics, B-roll, research from me"), ("Over 20 minutes", "Motion graphics")]
    card = ('<div class="mock"><div class="mh">My rate card back then, as a long form editor</div>' + "".join(
        f'<div style="display:flex;gap:22px;align-items:center;padding:16px 0;border-top:2px solid #DDE2EC"><span style="font-family:Gloock;font-size:52px;color:#8A5E17;width:50px">{k+1}</span>'
        f'<div style="flex:1"><b style="font-size:28px">{h}</b><br>{b}</div><span style="font:800 24px \'Plus Jakarta Sans\';border:3px dashed #B9C3D6;border-radius:12px;padding:10px 18px;color:#4A5670">your price</span></div>'
        for k, (h, b) in enumerate(tiers)) + '</div>')
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">I had what they call a rate card.</span><br>' + big("Your price tiers, on one card.", 96)),
        node("b0", 0, 0, "auto", card, ""),
        note(0, 0, 1700, 'The rate card makes the client know your actual price, and you can budget around things together. <b>Your number depends on your expertise, how confident you are to deliver, and the type of client.</b>'),
        row([rv(L("b1", "Still a beginner", big("$5 to $10", 80) + "<br>for a short form, if you're doing simple work you're learning on", "sprout", "", "auto", "flex:1"), "Beginner?", "flex:1;display:flex"),
             rv(L("b2", "Good international clients", big("$20 to $30", 80, NAVY) + "<br>the normal rate for a short form video", "globe", "gold", "auto", "flex:1"), "International?", "flex:1;display:flex")], 90),
    ]
    edge("b1", "b2", "gold", sa="r", sb="l")
    return B(2, "10.2", "Have a rate card", "id-card", items, "Your tiers of prices", "b0")


def b3():
    f = ["Your skill and confidence", "The client's business", "How important the video is", "The work inside it", "The niche and the length", "The amount of revisions", "The result you're getting them"]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">There\'s no fixed price.</span><br>' + big("All these things add up.", 110)),
        row([col([chip(f"m{k}", 0, 0, t) for k, t in enumerate(f)], 22, 620, "align-items:flex-start"),
             col([node("mp", 0, 0, 440, '<div class="spk" style="width:400px;height:400px">Your<br>price</div>', "", "display:flex;justify-content:center")], 0, 460, "justify-content:center")], 200, "justify-content:center"),
        lab2("Try and take control of the pricing"),
        row([L("m8", "Ask questions first", "&ldquo;Do you want motion graphics in your video? What style do you want? What do you want to achieve with this?&rdquo; They'll feel you know what you're doing.", "circle-help", "", "auto", "flex:1"),
             L("m9", "When they say it's too much, explain why", "&ldquo;The reason this price is this much is because there's motion graphics added, and I'm doing more research work.&rdquo;", "message-circle", "", "auto", "flex:1")], 30),
        L("m10", "Price on a call, so you can negotiate properly", "In the DMs, they're comparing you to other editors, trying to find the lowest person. You don't want to stoop that low. If they refuse a call, give your flat price. <b>Business videos and paid adverts are tied to money, so always charge more.</b>", "phone-call", "navy"),
        remember("Don't be afraid of no's. Don't be afraid of rejection. It's part of the journey."),
    ]
    for k in range(len(f)):
        edge(f"m{k}", "mp", "line", sa="r", sb="l", bend=0.4, arrow=False)
    return B(3, "10.3", "What moves your price", "sliders-horizontal", items, "There's no fixed price")


def b4():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">It\'s easier to convince a client on a package</span><br>' + big("than one video.", 110)),
        row([rv(L("p0", "Long-form package", big("$5,000", 96, NAVY) + "<br><b>5 long-form videos a month</b>", "film", "gold", "auto", "flex:1"), "Long-form package", "flex:1;display:flex"),
             rv(L("p1", "Short-form package", big("$3,000", 96, NAVY) + "<br><b>30 short-form videos a month</b>", "smartphone", "gold", "auto", "flex:1"), "Short-form package", "flex:1;display:flex")], 40),
        L("p2", "What I do now", "Six videos at maximum, three at minimum, for my client every month. A package. They pay me at the end of the month.", "user-round-check", ""),
        L("p3", "That's why you want retainer clients", "Clients who already post consistently, and work with you over a long period. You know it's recurring.", "repeat", "navy"),
        rv(L("p4", "Upsell, after you land the client", "&ldquo;I can help you script your videos, or do your thumbnails too.&rdquo; Ideation only if you really know how. So they pay you <b>$1,000 instead of $500</b>.", "plus", "gold"), "Add-ons"),
    ]
    return B(4, "10.4", "Stop collecting single projects", "package", items, "Do packages", "p0")


def b5():
    agr = ('<div class="mock"><div class="mh">Agreement · example</div>5 videos a month<br>30% paid upfront for the 5<br>Balance paid on delivery<br>3 rounds of revisions per video'
           '<div style="display:flex;gap:40px;margin-top:26px"><div style="flex:1;border-top:3px solid #0A1F44;padding-top:8px;font-weight:700">Client signature</div><div style="flex:1;border-top:3px solid #0A1F44;padding-top:8px;font-weight:700">Editor signature</div></div></div>')
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">A lot of clients can scam you.</span><br>' + big("You deliver, and you don't get paid.", 96)),
        row(steps("s", [("Deliver", "", "send", "dim"), ("Never paid", "", "circle-x", "dim")], d="row", gap=90, kind="mist"), 90),
        rv(L("s5", big("30%", 120, NAVY), "<b>upfront, especially with people you don't trust.</b> If you've agreed on 20 or 30 videos a month with a new client, don't wait till after the 30 for your first payment.", "", "gold"), "Before you start…"),
        row([L("s6", "Learn to write contracts", "Don't just let the person say it or type it. Create a contract and send it to them to sign. You both keep a copy. My company has worked with me for a long time, so they pay at the end of the month.", "file-pen-line", "", 760),
             node("s7", 0, 0, 900, agr, "")], 40),
    ]
    edge("s6", "s7", "gold", sa="r", sb="l")
    return B(5, "10.5", "Don't get scammed", "shield-alert", items, "It happens a lot in this industry", "s0")


def b6():
    ways = [("Cleva", "What I use now. It has worked for me for the past 2 years.", "gold"), ("Grey", "I've used it. USD, GBP and EUR accounts.", ""),
            ("Raenest", "A USD account built for freelancers.", ""), ("Payoneer", "I've used it. For Fiverr, Upwork, and clients who use it.", ""),
            ("PayPal", "In Nigeria, it's mostly for paying, not receiving.", "dim")]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">What works depends on where you live</span><br>' + big("and where your client is.", 92)),
        row([L(f"w{k}", h, b, "landmark", c, "auto", "flex:1") for k, (h, b, c) in enumerate(ways[:3])], 24),
        row([L(f"w{k+3}", h, b, "landmark", c, "auto", "flex:1") for k, (h, b, c) in enumerate(ways[3:])], 24),
        journey("Receiving payment in Nigeria has been very difficult. I've used Payoneer, I've used Grey. Right now I'm using <b>Cleva</b>. But my Cleva might not work for you."),
        note(0, 0, 1700, 'Some clients are in the US, some in Canada. Their methods of payment are different. <b>Do your research. Ask people that are earning online.</b>'),
    ]
    return B(6, "10.6", "Getting paid from abroad", "globe", items, "Do your research")


TOC = [("10.1", "How to charge"), ("10.2", "Have a rate card"), ("10.3", "What moves your price"),
       ("10.4", "Stop collecting single projects"), ("10.5", "Don't get scammed"), ("10.6", "Getting paid from abroad")]


def build():
    reset()
    body = assemble("10", "Price yourself and", "Get paid", "Charge per video. Have a rate card. Get the client on a call before you price. Move to packages, and protect yourself.",
                    "Stop collecting single projects.", [b1(), b2(), b3(), b4(), b5(), b6()], TOC,
                    ("NEXT · CHAPTER 11", "Grow through people"))
    return body, W, None
