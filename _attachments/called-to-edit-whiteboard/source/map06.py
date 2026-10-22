"""Chapter 6 as a map: learn the skill the right way."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map06-learn", 5400


def b1():
    f = [("Who you want to work for, and what kind of videos", "Talking head, podcast, vlogs, reactions, storytelling, cinematic. Be very specific.", "users"),
         ("Who can actually pay you", "Business videos pay more than entertainment videos.", "wallet"),
         ("What you have: phone or laptop, and how strong", "I loved motion graphics, but my laptop couldn't handle it. So I had to drop it.", "laptop"),
         ("Your software", "If you're a CapCut editor, 3D motion graphics doesn't make sense. So why learn the skill?", "app-window")]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Eliminate what you don\'t need,</span><br>' + big("till you know what to learn.", 90)),
    ]
    fl = []
    for k, (h, b, ic) in enumerate(f):
        w = 1700 - k * 160
        fl.append(rv(L(f"f{k}", h, b, ic, "", w), f"Filter {k+1}", f"align-self:center;width:{w}px"))
    fl.append(L("f4", "Your learning list", "", "list-checks", "gold", 900, "align-self:center"))
    chain([f"f{k}" for k in range(5)], "gold", sa="b", sb="t")
    items.append(col(fl, 50))
    return B(1, "6.1", "What decides what you learn", "filter", items, "Start from the top", "f0")


def b2():
    kinds = [("Real estate", "They do a lot of tracking and animation.", "house"), ("Business talking heads", "I don't need tracking or animation for them.", "briefcase"),
             ("Storytelling", "Some need visual effects.", "book-open"), ("Adverts", "They need other skills. Some need visual effects.", "megaphone"), ("Some videos", "Don't even need sound effects. So why learn it now?", "volume-x")]
    items = [
        note(0, 0, 1700, big("Every type of video has its own skills.", 76)),
        row([L(f"k{k}", h, b, ic, "", "auto", "flex:1") for k, (h, b, ic) in enumerate(kinds[:3])], 30),
        row([L(f"k{k+3}", h, b, ic, "", "auto", "flex:1") for k, (h, b, ic) in enumerate(kinds[3:])], 30),
        note(0, 0, 1700, 'The platform matters too. <b>A YouTube talking head and an Instagram talking head are not the same thing.</b> TikTok is different. LinkedIn is different.'),
        lab2("Example: a mobile editor who wants to edit podcast recaps"),
        row([rv(L("w0", "All he needs to learn", "Cutting, sound design, typography, captions.", "circle-check", "gold", "auto", "flex:1"), "Learn…", "flex:1;display:flex"),
             rv(L("w1", "He doesn't need", "Motion graphics, crazy storytelling. They're not needed in his niche.", "circle-x", "dim", "auto", "flex:1"), "Skip…", "flex:1;display:flex")], 40),
        journey("I wanted to learn everything. I'd see a wonderful flip animation and want to learn it. It was overwhelming. It became easier when I decided: <b>I'm only going to do talking head business videos for YouTube.</b> That narrowed down what I needed to learn."),
    ]
    return B(2, "6.2", "Different videos, different skills", "clapperboard", items, "Be very specific")


def b3():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Some people think learning the software is learning video editing.</span><br>' + big("It's not.", 100)),
        row(steps("s", [("First, master the software", "If it's CapCut, sit down with those long four, five hour tutorials. This is the part you can't skip.", "app-window", ""),
                        ("Then learn the skill", "The art of cutting, pacing, sound. Whatever your type of video needs.", "scissors", "gold")],
                  d="row", gap=100, reveal=[None, "Then…"]), 100),
        L("s9", "I mastered DaVinci Resolve", "There's nothing you can tell me about Resolve that I don't know. But the software is just the tool that helps you edit the videos you want.", "triangle-alert", "dim"),
        L("s8", "AI is part of the tools you need to learn", "I use Claude a lot in my workflow, and it helps me edit some parts of my videos. If you use AI tools on a client's work, <b>charge them for the AI cost.</b>", "bot", ""),
        rv(L("s7", "AI can be your pitch", '<span style="font:800 32px/1.3 \'Plus Jakarta Sans\'">&ldquo;I use AI to enhance your videos faster, so you can put out content faster.&rdquo;</span><br>Some creators and business owners need speed more than fancy stuff.', "megaphone", "gold"), "AI is also…"),
    ]
    edge("s8", "s7", "gold", sa="b", sb="t")
    return B(3, "6.3", "Software, skill and AI", "layers", items, "The software, then the skill", "s0")


def b4():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">There\'s nothing you want to learn that you won\'t find on YouTube.</span><br>' + big("You just need to know what to search for.", 84)),
        col(steps("y", [("Know your type of video", "Let's say talking heads for business creators on Instagram.", "tag"),
                        ("Ask any AI tool what skills you need", "It will list them: cutting, pacing, captions, typography, B-roll, sound design, music.", "bot"),
                        ("Learn them one by one", "Watch a tutorial on cutting. Practise it.", "youtube"),
                        ("Implement it on a video", "Record yourself with your phone and edit it. Learn typography, put it in that same video. Then sound design.", "clapperboard", "gold")],
                  reveal=["Step 1", "Step 2", "Step 3", "Step 4"], num=True), 56),
        remember("Don't learn without implementation."),
        row([L("y8", "The skill is free on YouTube", "I never paid for any course. Everything you'd pay for in a skills course is on YouTube.", "youtube", "", "auto", "flex:1"),
             L("y9", "What's worth paying for: the business", "How to talk with clients, how to package yourself. I paid for a community to learn it, from marketers and sales guys, not editors.", "briefcase", "gold", "auto", "flex:1")], 40),
        L("y7", "Learn on the go", "A client asks, &ldquo;Can you do this?&rdquo; I say yes, I can do it. Meanwhile, I don't know how yet. I go and learn it on that project. <b>Let tutorials become your entertainment.</b>", "rocket", "navy"),
    ]
    return B(4, "6.4", "Where to learn: YouTube", "youtube", items, "I learned 80 to 90% there", "y0")


def b5():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">One of the fastest ways to learn:</span><br>' + big("Recreate videos.", 120)),
        col(steps("r", [("Pick your niche", "Let's say podcast videos.", "target"), ("Find an edit you love", "Someone did a short form from a podcast, and you loved it.", "heart"),
                        ("Find the raw podcast on YouTube and download it", "", "download"), ("Try and mimic the same edit", "", "copy"),
                        ("Don't know how to do something?", "Go on YouTube and search how to do that particular thing. There's a tutorial for everything, I promise you.", "search", "gold")], num=True), 56),
        note(0, 0, 1700, '<b>YouTube is a mine of raw videos.</b> Many people post their videos unedited. Don\'t look for the biggest creators, they\'ve already over-edited their videos.'),
        demo_("r9", 0, 0, "auto", "How to download a YouTube video", "Optional: only if time allows"),
        row([photo("r7", 0, 0, 800, 380, "Clip: the original edit", None, -1.5), photo("r8", 0, 0, 800, 380, "Clip: your recreation", None, 1.5)], 70),
        note(0, 0, 1700, 'Put them side by side and post it: <b>&ldquo;I just recreated this edit. Did I get it right?&rdquo;</b> It\'s mostly for practice. You can\'t really call a recreation your own. You\'re doing what someone did professionally, so that one day you can become like that person.'),
    ]
    edge("r3", "r9", "dash", sa="r", sb="r", bend=0.6)
    edge("r7", "r8", "gold", sa="r", sb="l")
    return B(5, "6.5", "Recreate videos you love", "copy", items, "One of the fastest ways I learned", "r0")


def b6():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Every video has a goal.</span><br>' + big("Edit for that goal.", 110)),
        row([L("g0", "A fancy video", "Gets a lot of views. <b>No sales.</b>", "sparkles", "dim", "auto", "flex:1"),
             rv(L("g1", "A simple, clear video", "The target audience understands it. <b>A lot of sales.</b>", "target", "gold", "auto", "flex:1"), "Which one?", "flex:1;display:flex")], 90),
        note(0, 0, 1700, '<b>Which is more beneficial for the client?</b> A client will prefer an editor whose videos produce results over an editor doing flashy stuff that isn\'t performing.'),
        lab2("Show and not tell"),
        row([L("g2", "A car icon", "If he's talking about a car, I don't put a car icon.", "car", "dim", "auto", "flex:1"),
             rv(L("g3", "A real car", "I show a real car. A real thing always beats a fake thing.", "film", "gold", "auto", "flex:1"), "Stronger…", "flex:1;display:flex")], 90),
        note(0, 0, 1700, 'If your client is talking about YouTube views, show YouTube views. Some videos I edit, <b>80% of it is me showing what the client is saying</b>, more than his face. Every cut, every effect, every caption, every B-roll should have a function.'),
    ]
    edge("g0", "g1", "gold", sa="r", sb="l", label="vs")
    edge("g2", "g3", "gold", sa="r", sb="l", label="vs")
    return B(6, "6.6", "Edit for the goal", "target", items, "What is my client trying to achieve?")


TOC = [("6.1", "What decides what you learn"), ("6.2", "Different videos, different skills"), ("6.3", "Software, skill and AI"),
       ("6.4", "Where to learn: YouTube"), ("6.5", "Recreate videos you love"), ("6.6", "Edit for the goal")]


def build():
    reset()
    body = assemble("6", "Learn the skill", "The right way", "Know who you're editing for and what your tools can do. Then learn one skill at a time, and implement it as you go.",
                    "You don't choose what to learn. What you learn is chosen for you.", [b1(), b2(), b3(), b4(), b5(), b6()], TOC,
                    ("NEXT · CHAPTER 7", "From practice to paid"))
    return body, W, None
