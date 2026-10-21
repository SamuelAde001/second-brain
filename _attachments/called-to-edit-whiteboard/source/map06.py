"""Chapter 6 as a map: learn the skill the right way."""
from maplib import *
from lib import rv, icon, remember, journey, NAVY, CH, MIST

NAME, W = "map06-learn", 5400


def b1():
    f = [("Who you want to work for, and what kind of videos", "", "users"), ("Who can actually pay you", "", "wallet"),
         ("Your hardware: phone or laptop, how strong", "", "laptop"), ("Your software", "CapCut can't do 3D, so why learn it?", "app-window")]
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Work backwards. Cut what you don\'t need,</span><br>' + big("until you know what to learn.", 90)),
    ]
    fl = []
    for k, (h, b, ic) in enumerate(f):
        w = 1700 - k * 160
        fl.append(rv(L(f"f{k}", h, b, ic, "", w), f"Filter {k+1}", f"align-self:center;width:{w}px"))
    fl.append(L("f4", "Your learning list", "", "list-checks", "gold", 900, "align-self:center"))
    chain([f"f{k}" for k in range(5)], "gold", sa="b", sb="t")
    items.append(col(fl, 50))
    return B(1, "6.1", "The filters", "filter", items, "A funnel", "f0")


def b2():
    kinds = [("Real estate", "A lot of tracking and animation", "house"), ("Business talking heads", "No tracking or animation needed", "briefcase"),
             ("Storytelling", "Some need visual effects", "book-open"), ("Adverts", "Their own skills, some VFX", "megaphone"), ("Some videos", "Don't even need sound effects", "volume-x")]
    items = [
        note(0, 0, 1700, big("Each kind of video needs different skills.", 76)),
        row([L(f"k{k}", h, b, ic, "", "auto", "flex:1") for k, (h, b, ic) in enumerate(kinds[:3])], 30),
        row([L(f"k{k+3}", h, b, ic, "", "auto", "flex:1") for k, (h, b, ic) in enumerate(kinds[3:])], 30),
        note(0, 0, 1700, 'Platforms edit differently too: a YouTube talking head and an Instagram talking head are not the same. TikTok is different again, and so is LinkedIn.'),
        lab2("Worked example: a phone editor doing podcast recaps"),
        row([rv(L("w0", "Learn", "Cutting · Sound design · Typography · Captions", "circle-check", "gold", "auto", "flex:1"), "Learn…", "flex:1;display:flex"),
             rv(L("w1", "Skip, for now", "Motion graphics · Heavy storytelling · 3D effects", "circle-x", "dim", "auto", "flex:1"), "Skip…", "flex:1;display:flex")], 40),
        journey("When I started I wanted to learn everything. I'd see a flip animation and want to learn it. Overwhelming, until I chose <b>YouTube long-form business talking heads</b>. I loved motion graphics, but my laptop couldn't handle it, so I dropped it."),
    ]
    return B(2, "6.2", "Different videos, different skills", "clapperboard", items, "Choose by video type")


def b3():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Software and skill</span><br>' + big("are two different things.", 100)),
        row(steps("s", [("1 · The software: master it first", "The one you will actually use. For CapCut, sit through the long 4-5 hour tutorials.", "app-window", ""),
                        ("2 · The skill: then learn the craft", "The art of cutting, pacing and sound that makes the kind of video you chose.", "scissors", "gold")],
                  d="row", gap=100, reveal=[None, "Then…"]), 100),
        L("s9", "The mistake: learning the software and thinking that's editing.", "I mastered DaVinci Resolve. The software was only the start.", "triangle-alert", "dim"),
        L("s8", "AI is part of what you learn, one tool at a time", "I use Claude Code to edit parts of my videos. <b>If you use AI tools on a client's work, charge for them.</b>", "bot", ""),
        rv(L("s7", "AI is also a pitch", '<span style="font:800 32px/1.3 \'Plus Jakarta Sans\'">&ldquo;I use AI to enhance your videos faster, so you can put out content faster.&rdquo;</span>', "megaphone", "gold"), "AI is also…"),
    ]
    edge("s8", "s7", "gold", sa="b", sb="t")
    return B(3, "6.3", "Software, skill and AI", "layers", items, "Two different things", "s0")


def b4():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">The problem is never the source.</span><br>' + big("It's the search.", 110)),
        col(steps("y", [("Name your video type", "e.g. talking heads for business creators on Instagram", "tag"),
                        ("Ask AI for the skill list", "cutting, pacing, captions, typography, B-roll, sound, music", "bot"),
                        ("One tutorial, one skill", "learn them one by one", "youtube"),
                        ("Use it on one practice video", "same video, skill after skill", "clapperboard", "gold")],
                  reveal=["Step 1", "Step 2", "Step 3", "Step 4"], num=True), 56),
        remember("Don't learn without implementation."),
        row([L("y8", "Free · YouTube: the skill", "Everything a skills course sells is on YouTube. I never paid for one.", "youtube", "", "auto", "flex:1"),
             L("y9", "Worth paying for: the business", "Clients, packaging, presenting yourself.", "briefcase", "gold", "auto", "flex:1")], 40),
        L("y7", "Learn on the go", "A client asks &ldquo;Can you do this?&rdquo; I say yes, then learn it on that project.", "rocket", "navy"),
    ]
    return B(4, "6.4", "Where to learn: YouTube", "youtube", items, "The search, not the source", "y0")


def b5():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">One of the fastest ways to learn:</span><br>' + big("Recreate.", 120)),
        col(steps("r", [("Pick your niche", "e.g. podcast videos", "target"), ("Find an edit you love", "a short cut from a podcast", "heart"),
                        ("Find the raw podcast on YouTube and download it", "", "download"), ("Copy the same edit", "", "copy"),
                        ("Can't do something?", "Search YouTube for that one thing, learn it, put it in.", "search", "gold")], num=True), 56),
        note(0, 0, 1700, '<b>Raw footage:</b> YouTube is a mine of raw videos. Skip the biggest creators, their videos are already over-edited.'),
        demo_("r9", 0, 0, "auto", "How to download a YouTube video", "Optional: only if time allows"),
        row([photo("r7", 0, 0, 800, 380, "Clip: the original edit", None, -1.5), photo("r8", 0, 0, 800, 380, "Clip: your recreation", None, 1.5)], 70),
        note(0, 0, 1700, 'Share it side by side with the original. <b>It\'s practice, not portfolio.</b> You copy what someone did professionally, so one day you become like that person.'),
    ]
    edge("r3", "r9", "dash", sa="r", sb="r", bend=0.6)
    edge("r7", "r8", "gold", sa="r", sb="l")
    return B(5, "6.5", "Recreate videos you love", "copy", items, "Copy, then learn the gaps", "r0")


def b6():
    items = [
        note(0, 0, 1700, '<span style="font:600 44px \'Plus Jakarta Sans\';color:#fff">Edit for the goal,</span><br>' + big("not to look edited.", 110)),
        row([L("g0", "The flashy video", "Lots of views · <b>No sales</b>", "sparkles", "dim", "auto", "flex:1"),
             rv(L("g1", "The clear video", "Fewer views · <b>Lots of sales</b>", "target", "gold", "auto", "flex:1"), "Which one?", "flex:1;display:flex")], 90),
        note(0, 0, 1700, '<b>Which would your client rather have?</b> A client will choose an editor whose videos produce results over flashy edits that don\'t perform.'),
        lab2("Show, don't tell"),
        row([L("g2", "A car icon", "The viewer reads a symbol.", "car", "dim", "auto", "flex:1"),
             rv(L("g3", "Real car footage", "The viewer sees the real thing.", "film", "gold", "auto", "flex:1"), "Stronger…", "flex:1;display:flex")], 90),
        note(0, 0, 1700, 'Talking about YouTube views? Show YouTube views. Some of my videos are about <b>80% showing</b> what the client says rather than their face. What viewers hear and see must match.'),
    ]
    edge("g0", "g1", "gold", sa="r", sb="l", label="vs")
    edge("g2", "g3", "gold", sa="r", sb="l", label="vs")
    return B(6, "6.6", "Edit for the goal", "target", items, "Results over flash")


TOC = [("6.1", "The filters"), ("6.2", "Different videos, different skills"), ("6.3", "Software, skill and AI"),
       ("6.4", "Where to learn: YouTube"), ("6.5", "Recreate videos you love"), ("6.6", "Edit for the goal")]


def build():
    reset()
    body = assemble("6", "Learn the skill", "The right way", "Start with who you serve, what they pay for and what your tools can do. Then learn one skill at a time, on a real video.",
                    "You don't choose what to learn. What you learn is chosen for you.", [b1(), b2(), b3(), b4(), b5(), b6()], TOC,
                    ("NEXT · CHAPTER 7", "From practice to paid"))
    return body, W, None
