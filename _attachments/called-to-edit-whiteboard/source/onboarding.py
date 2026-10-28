"""Community Onboarding Session (2026-10-28) as nine maps, same style as the webinar board.
Outline: 04-Projects/called-to-edit-onboarding-whiteboard.md. onb00.py … onb08.py each pick one section from here."""
from maplib import *
from lib import rv, icon, NAVY, CH, MIST

W = 5720
WHITE_TXT = "#fff"


def lead(text, size=44):
    return f'<span style="font:600 {size}px \'Plus Jakarta Sans\';color:#fff">{text}</span>'


def check(nid, text, tag=""):
    t = f'<span class="chip dim" style="position:static;font-size:20px;padding:6px 16px">{tag}</span>' if tag else ""
    return node(nid, 0, 0, "auto", f'<div style="width:44px;height:44px;border:4px solid #FCDD9E;border-radius:10px;flex:none"></div>'
                f'<div class="lh" style="flex:1;font-size:28px">{text}</div>{t}', "leaf", "align-items:center;padding:18px 26px")


def ch(nid, name, line, ic):
    return L(nid, f"#{name}", line, ic, "", "auto", "flex:1")


def pairs(p, items, gap=24):
    """Leaves two to a row."""
    rows_ = []
    for k in range(0, len(items), 2):
        rows_.append(row([ch(f"{p}{k + j}", *it) for j, it in enumerate(items[k:k + 2])], gap))
    return rows_


# ---------------- 0 · Welcome ----------------

def s0():
    tonight = [("The plan", "", "map"), ("What we need to achieve", "", "target"), ("Setting up Discord", "", "smartphone"),
               ("A tour of every channel", "", "layout-grid"), ("Getting the most out of it", "", "zap"),
               ("Your turn on stage", "", "mic"), ("Before Sunday, and your questions", "", "flag")]
    b1 = B(1, "0.1", "Tonight", "list", [note(0, 0, 1700, lead("Here's how tonight goes.") + "<br>" + big("In this order.", 100))]
           + steps("a", tonight, "gold", num=True), "Seven stops")
    b2 = B(2, "0.2", "Before we start", "flag", [
        L("b0", "This call is recorded", "The replay goes up in <b>#announcements</b>, so nobody misses anything.", "video", "navy"),
        L("b1", "Want to talk?", "Tap <b>Request to Speak</b> at the bottom of the stage. I'll bring you up.", "mic"),
        L("b2", "Everyone gets a turn", "Later tonight, each of you comes on stage. Hold your story till then.", "users", "gold"),
    ], "Quick things", "b0")
    side = ('<img src="kit/samuel-cutout-sm.webp" style="width:700px;align-self:center">'
            '<img src="kit/called-to-edit-community-dark.svg" style="width:480px">')
    return assemble("", "Welcome to the", "Community", "Called to Edit · Onboarding Session<br><b style=\"color:#FCDD9E\">Wednesday 28 October, 8pm WAT</b>",
                    "You're not doing this alone anymore.", [b1, b2], [("0.1", "Tonight"), ("0.2", "Before we start")],
                    ("NEXT · 1", "Why we're here"), side)


# ---------------- 1 · Why we're here ----------------

def s1():
    b1 = B(1, "1.1", "What we are", "users-round", [
        note(0, 0, 1700, big("We help video editors build a real career and land clients, together.", 96)),
        L("w0", "Not a course. A community.", "People going the same way as you, at your level, pushing each other.", "users"),
    ], "In one line")
    get = [("Editors at your level", "Everyone supporting each other.", "users"), ("Honest feedback", "On your edits, your profile, your outreach.", "message-square"),
           ("Accountability", "Your own post. Your goals. Your progress, in public.", "circle-check"), ("A weekly live call with me", "Wednesdays, 8pm.", "video"),
           ("Resources and opportunities", "Tutorials, hacks, templates. Gigs and leads.", "book-open"), ("Editors Bot", "Ask it anything from my teaching, any time.", "bot")]
    b2 = B(2, "1.2", "What you get", "gift", [row([L(f"g{k + j}", *get[k + j], "", "auto", "flex:1") for j in range(2)], 24) for k in range(0, 6, 2)], "Inside")
    plus = node("pl0", 0, 0, "auto", big("+", 110), "", "align-self:center")
    plus2 = node("pl1", 0, 0, "auto", big("+", 110), "", "align-self:center")
    b3 = B(3, "1.3", "How you get clients", "target", [
        note(0, 0, 1700, lead("This is how I teach it.") + "<br>" + big("One formula.", 100)),
        row([L("f0", "A strong personal brand", "Get seen.", "star", "gold", "auto", "flex:1"), plus,
             L("f1", "Value-first outreach", "Reach out by giving first.", "send", "gold", "auto", "flex:1"), plus2,
             L("f2", "Great skills", "Do the work well.", "wand-sparkles", "gold", "auto", "flex:1")], 20),
        L("f3", "The whole server is built around these three", "Each one has its own channels. You'll see them in the tour.", "layout-grid", "navy"),
    ], "Remember this")
    return assemble("1", "Why we're", "Here", "What this community is, and why it exists.",
                    "You can't do video editing alone.", [b1, b2, b3], [("1.1", "What we are"), ("1.2", "What you get"), ("1.3", "How you get clients")],
                    ("NEXT · 2", "The plan"))


# ---------------- 2 · The plan ----------------

def s2():
    road = [("Now to Saturday 31 October", "<b>Get set up.</b> Your profile, say hi, make your accountability post, open the workbook.", "wrench", ""),
            ("Sunday 1 November", "<b>The 60-Day Challenge starts.</b> One task a day, toward your first client.", "flame", "gold"),
            ("Every Wednesday, 8pm WAT", "<b>Live call with me.</b> I guide you, answer your questions, sometimes teach.", "video", ""),
            ("Coming soon", "<b>Called to Edit Academy.</b>", "graduation-cap", "navy")]
    b1 = B(1, "2.1", "The road", "route", steps("r", road, "gold", num=True), "Where we're going", "r0")
    phases = [("1", "Set your direction", "Days 1–7"), ("2", "Learn on real videos", "Days 8–21"), ("3", "Real people, real work", "Days 22–35"), ("4", "Go get your first client", "Days 36–60")]
    tiles = [node(f"p{k}", 0, 0, "auto", big(n, 90) + f'<div class="lh" style="margin-top:10px">{t}</div><div class="lb">{d}</div>', "leaf", "flex:1;flex-direction:column;gap:4px")
             for k, (n, t, d) in enumerate(phases)]
    for k in range(3):
        edge(f"p{k}", f"p{k+1}", "gold", sa="r", sb="l", bend=0.3)
    b2 = B(2, "2.2", "The 60-Day Challenge", "flame", [
        note(0, 0, 1700, lead("Starts Sunday 1 November.") + "<br>" + big("Four phases.", 100)),
        row(tiles, 40),
        row([L("c0", "One task a day", "From the workbook, in #resources.", "notebook-pen", "", "auto", "flex:1"),
             L("c1", "Post it every day", "In your own post in #accountability.", "circle-check", "", "auto", "flex:1"),
             L("c2", "Joined late?", "You start your own day 1.", "calendar", "gold", "auto", "flex:1")], 24),
    ], "One task a day")
    week = [("Every morning, 7am", "A nugget from my teaching in #general-chat.", "sun"), ("Streaks", "Every day you post in your own accountability post counts. Type <b>/streak</b>.", "flame"),
            ("Sunday, 6pm", "The leaderboard goes up in #wins.", "trophy"), ("Always growing", "Tutorials, hacks, templates and call replays in #resources.", "book-open")]
    b3 = B(3, "2.3", "What keeps running", "repeat", [row([L(f"k{k + j}", *week[k + j], "", "auto", "flex:1") for j in range(2)], 24) for k in range(0, 4, 2)], "Every week")
    return assemble("2", "The", "Plan", "What happens from tonight, and what keeps running every week.",
                    "Go at your own pace. When you see others putting in the work, you'll want to do it too.",
                    [b1, b2, b3], [("2.1", "The road"), ("2.2", "The 60-Day Challenge"), ("2.3", "What keeps running")], ("NEXT · 3", "Our goals"))


# ---------------- 3 · Our goals ----------------

def s3():
    b1 = B(1, "3.1", "By day 60", "target", [
        note(0, 0, 1700, lead("The goal for each of you.") + "<br>" + big("Your first client, or real progress toward one.", 100)),
    ], "The goal")
    ms = [("Your offer in one sentence: who you help, what result, how, how fast", "#profile-and-portfolio"),
          ("Three full videos in your niche", "#showcase"), ("Your profile fixed, and a portfolio: 8 videos at most", "#profile-and-portfolio"),
          ("Posting 2 to 3 times a day: 40% authentic, 40% authority, 20% sales", "#personal-brand"),
          ("Your dream client list: 20 to 50 names", "#outreach"), ("Value-first outreach: a free edit of 30 seconds or less", "#outreach"),
          ("Your rate card", "#pricing-and-clients")]
    b2 = B(2, "3.2", "The milestones", "list-checks", [note(0, 0, 1700, lead("Tick them off in order.") + "<br>" + big("On the way.", 100)),
                                                       col([check(f"m{k}", t, c) for k, (t, c) in enumerate(ms)], 16)], "Step by step")
    us = [("Show up in your accountability post", "Even on slow days. Especially on slow days.", "circle-check"), ("Give feedback, not only ask for it", "Someone else's edit teaches you too.", "message-square"),
          ("Back each other's posts", "Watch, like, comment, repost in #share-your-posts.", "share-2"), ("Share every win", "Small or big. A reply counts.", "trophy"),
          ("Come on Wednesdays", "Bring your questions to the call.", "video")]
    b3 = B(3, "3.3", "What it takes from all of us", "handshake", [L(f"u{k}", *u, "gold" if k == 0 else "") for k, u in enumerate(us)], "As a community", "u0")
    return assemble("3", "Our", "Goals", "What we're going for together, and what it takes.",
                    "Don't learn without implementation.", [b1, b2, b3], [("3.1", "By day 60"), ("3.2", "The milestones"), ("3.3", "What it takes")],
                    ("NEXT · 4 · LIVE DEMO", "Setting up Discord"))


# ---------------- 4 · Setting up Discord ----------------

def s4():
    b1 = B(1, "4.1", "Live demo", "monitor-play", [demo_("d0", 0, 0, 1700, "Setting up Discord, step by step", "Share my screen and follow along on your phone").replace("switch to Chrome", "switch to Discord"),
                                                    note(0, 0, 1700, "Follow along on your own phone while I do it.")], "Do it with me")
    st = [("Get the app", "On your phone and your computer. Log in with the account you joined with.", "smartphone"),
          ("Your profile", "Your real name as your server nickname, and a clear photo of your face. Same rule as your page.", "user-round"),
          ("Notifications", "Turn them on for <b>#announcements</b> and <b>#weekly-live</b>. Set the rest to @mentions only, so you're not buried.", "bell"),
          ("Find your way", "Channels are on the left. On your phone, swipe right. Tap a category to fold it.", "compass"),
          ("Forums", "#accountability, #feedback and #resources are forums. Tap <b>New Post</b>, give it a title and a tag.", "layout-grid"),
          ("The stage", "#weekly-live is where we are now. To talk, tap <b>Request to Speak</b>.", "mic"),
          ("Editors Bot", "Type <b>/</b> to see the commands. Start with <b>/help</b>.", "bot"),
          ("Your subscription", "<b>/subscription</b> shows when your month ends. Cards renew by themselves; transfers get a reminder 3 days before.", "calendar")]
    b2 = B(2, "4.2", "Step by step", "list", steps("s", [(h, b, i, "") for h, b, i in st], "gold", num=True), "Eight things", "s0")
    rules = [("Be kind to one another", "Honest feedback, given with respect.", "heart"), ("No fights, no abuse, no insults", "Disagree with the idea, never attack the person.", "ban"),
             ("No scams", "No investment, forex or crypto offers. No asking anyone for money.", "shield-alert"), ("No selling to members", "Here or in their DMs. Jobs for others go in #opportunities.", "store"),
             ("What's shared here stays here", "Call recordings, the workbook, other people's work.", "lock"), ("English", "So everyone can follow.", "globe")]
    b3 = B(3, "4.3", "The rules", "shield-check", [row([L(f"x{k + j}", *rules[k + j], "", "auto", "flex:1") for j in range(2)], 24) for k in range(0, 6, 2)]
           + [L("x6", "The bot removes messages that break them", "Breaking them on purpose means removal.", "bot", "navy")], "Six of them")
    return assemble("4", "Set up", "Discord", "Do this once, properly, and the rest is easy.",
                    "Your face and your name. Same rule as your page.", [b1, b2, b3], [("4.1", "Live demo"), ("4.2", "Step by step"), ("4.3", "The rules")],
                    ("NEXT · 5 · LIVE DEMO", "Every channel"))


# ---------------- 5 · Every channel ----------------

def s5():
    b1 = B(1, "5.1", "Start here", "compass", [demo_("d0", 0, 0, 1700, "Open each channel as we go", "Discord, screen shared").replace("switch to Chrome", "switch to Discord"),
                                                note(0, 0, 1700, "<b>I post here. You read.</b>")] + pairs("a", [
        ("start-here", "What this is, the rules, how to use it. Read first.", "compass"), ("announcements", "Calls, challenges, news. Notifications on.", "megaphone"),
        ("welcome", "The bot welcomes every new member here.", "user-plus")]), "Read first")
    b2 = B(2, "5.2", "Community", "message-circle", pairs("b", [
        ("general-chat", "Talk. Introduce yourself. The morning nugget lands here.", "message-circle"), ("wins", "Clients, replies, finished videos. Sunday's leaderboard.", "trophy"),
        ("showcase", "Finished edits, cuts in progress, your timeline.", "clapperboard"), ("accountability", "Your own post and your daily progress. The 60-Day Challenge lives here.", "circle-check"),
        ("ask-editors-bot", "Ask anything from my teaching. Type /ask.", "bot")]), "Every day")
    b3 = B(3, "5.3", "Grow", "sprout", pairs("c", [
        ("feedback", "Post your edit, portfolio, bio or outreach message.", "film"), ("resources", "Tutorials, hacks, templates, the webinar replay, the e-book, the workbook.", "book-open"),
        ("opportunities", "Gigs, leads, collabs. Can't take it? Pass it on.", "briefcase"), ("help", "Stuck on anything? Ask.", "circle-help")]), "Get better")
    b4 = B(4, "5.4", "Personal brand", "star", pairs("d", [
        ("personal-brand", "What to post. 40% authentic, 40% authority, 20% sales.", "star"), ("profile-and-portfolio", "Your page is where clients decide.", "id-card"),
        ("share-your-posts", "Drop your link. Back each other.", "share-2")]), "Part 1 of the formula")
    b5 = B(5, "5.5", "Outreach", "send", pairs("e", [
        ("outreach", "Value-first edits, Loom, DMs, emails, follow-ups.", "send"), ("pricing-and-clients", "What to charge, getting paid, briefs, revisions.", "circle-dollar-sign")]), "Part 2 of the formula")
    b6 = B(6, "5.6", "Skills", "wand-sparkles", pairs("f", [
        ("editing-craft", "Hooks, pacing, story, sound, colour, captions.", "wand-sparkles"), ("capcut", "Phone or computer.", "scissors"),
        ("davinci-resolve", "Edit, Fusion, Fairlight, colour.", "sliders-horizontal"), ("premiere-pro", "Premiere and After Effects.", "layers")]), "Part 3 of the formula")
    b7 = B(7, "5.7", "Live", "mic", pairs("g", [("weekly-live", "Wednesdays, 8pm WAT. Where we are right now.", "mic")]), "Every Wednesday")
    toc_ = [("5.1", "Start here"), ("5.2", "Community"), ("5.3", "Grow"), ("5.4", "Personal brand"), ("5.5", "Outreach"), ("5.6", "Skills"), ("5.7", "Live")]
    return assemble("5", "Every", "Channel", "The whole server, one category at a time.",
                    "Ask in the right room.", [b1, b2, b3, b4, b5, b6, b7], toc_, ("NEXT · 6", "Getting the most out of it"))


# ---------------- 6 · Getting the most out of it ----------------

def s6():
    day = [("Read the nugget", "7am, in #general-chat.", "sun"), ("Post what you did", "In your own post in #accountability.", "circle-check"),
           ("Give one person feedback", "In #feedback or #showcase.", "message-square"), ("Back one post", "In #share-your-posts.", "share-2")]
    b1 = B(1, "6.1", "Every day", "sun", [note(0, 0, 1700, lead("About 15 minutes.") + "<br>" + big("Every day.", 100))]
           + steps("d", [(h, b, i, "") for h, b, i in day], "gold", num=True), "Your routine")
    wk = [("Wednesday, 8pm", "The live call. Bring your questions.", "video"), ("Sunday, 6pm", "The leaderboard in #wins.", "trophy"),
          ("One piece of work a week", "In #feedback or #showcase.", "clapperboard")]
    b2 = B(2, "6.2", "Every week", "calendar", [L(f"w{k}", *w) for k, w in enumerate(wk)], "Your rhythm", "w0")
    fb = [("What it is", "A reel, your bio, a DM, your portfolio.", "file-pen-line"), ("Who it's for", "The client or the audience.", "target"),
          ("What you want checked", "The hook? The pacing? The offer?", "search")]
    b3 = B(3, "6.3", "Asking for feedback", "message-square", [note(0, 0, 1700, lead("Feedback that actually helps.") + "<br>" + big("Say three things.", 100)),
                                                               row([L(f"f{k}", *f, "", "auto", "flex:1") for k, f in enumerate(fb)], 24),
                                                               L("f3", "Post the link or the file", "Not a description of it.", "link", "gold")], "Get real help")
    cmds = [("/ask", "Any question, from my teaching"), ("/review", "Your bio, portfolio blurb or outreach message"), ("/niche", "Say what you edit in one sentence"),
            ("/nugget", "A nugget from my teaching"), ("/streak", "Your days done")]
    b4 = B(4, "6.4", "Editors Bot", "bot", [row([L(f"c{k + j}", cmds[k + j][0], cmds[k + j][1], "", "navy" if k + j == 0 else "", "auto", "flex:1")
                                                  for j in range(min(2, len(cmds) - k))], 24) for k in range(0, 5, 2)]
           + [note(0, 0, 1700, "It's an AI and it can be wrong. For big decisions, bring it to Wednesday's call.")], "Five commands")
    return assemble("6", "Get the", "Most out of it", "What the people who grow here do.",
                    "Your practice work is your work.", [b1, b2, b3, b4], [("6.1", "Every day"), ("6.2", "Every week"), ("6.3", "Asking for feedback"), ("6.4", "Editors Bot")],
                    ("NEXT · 7", "Your turn on stage"))


# ---------------- 7 · Your turn ----------------

def s7():
    how = [("Request to Speak", "", "mic", ""), ("I bring you up", "", "user-round-check", ""), ("2 to 3 minutes", "", "timer", ""), ("Your next step", "", "footprints", "gold")]
    b1 = B(1, "7.1", "How it works", "mic", [row(steps("h", how, "gold", d="row"), 50)], "One by one", "h0")
    tell = [("Your name, and where you edit from", "", "map-pin", ""), ("What you edit on", "Phone or computer. Which software.", "smartphone", ""),
            ("The videos you want to edit, and who for", "", "target", ""), ("Where you are right now", "Pick your stop on the road.", "route", "gold"),
            ("One thing you want done in the next 30 days", "", "flag", "")]
    b2 = B(2, "7.2", "Tell me", "message-circle", steps("q", tell, "gold", num=True), "Five things", "q0")
    road = [("Just starting", "You haven't edited much yet.", "Pick one tool and learn on real videos. Learn, then use it straight away.", "#capcut · #davinci-resolve · #premiere-pro"),
            ("Can edit, no direction", "You edit everything.", "Choose your niche. Write your offer in one sentence. Try /niche.", "#personal-brand"),
            ("A niche, nothing to show", "No videos in your niche yet.", "Three full videos in your niche. Practice work is real work.", "#showcase · #feedback"),
            ("Work, but nobody sees it", "You have videos. No audience.", "Fix your profile, build the portfolio, post 2 to 3 times a day.", "#profile-and-portfolio · #share-your-posts"),
            ("Posting, no clients yet", "People see you. Nobody's paying.", "Dream client list, warm up, value-first outreach, follow up up to 4 times.", "#outreach"),
            ("You have clients", "You want more, or better ones.", "Rate card, testimonials, raise your prices, ask for referrals.", "#pricing-and-clients · #wins")]
    stops = []
    for k, (h, now, nxt, chans) in enumerate(road):
        stops.append(node(f"r{k}", 0, 0, "auto",
                          f'<div class="spk" style="width:110px;height:110px;flex:none;font-family:Gloock;font-size:60px;font-weight:400">{k + 1}</div>'
                          f'<div class="lc"><div class="lh">{h}</div><div class="lb">{now}</div>'
                          f'<div class="lb" style="margin-top:12px"><b>Next:</b> {nxt}</div><div class="lb" style="margin-top:8px"><b>Live in:</b> {chans}</div></div>',
                          "leaf", "align-items:center;gap:30px"))
    for k in range(5):
        edge(f"r{k}", f"r{k+1}", "gold", sa="b", sb="t", bend=0.3)
    b3 = B(3, "7.3", "Where are you right now?", "route", [note(0, 0, 1700, lead("Find yourself on the road.") + "<br>" + big("Six stops.", 100)),
                                                           col(stops, 56)], "Pick your stop")
    slots = [node(f"n{k}", 0, 0, "auto", '<div class="lh" style="color:#B9C3D6">Name</div><div style="height:230px"></div><div class="lb">Stop · Next step</div>',
                  "leaf dim", "flex:1;flex-direction:column") for k in range(10)]
    b4 = B(4, "7.4", "My notes", "notebook-pen", [note(0, 0, 1700, "One box per person. I write their next step as they talk.")]
           + [row(slots[k:k + 2], 24) for k in range(0, 10, 2)], "Space to write")
    return assemble("7", "Your", "Turn", "Come on stage. Tell me where you are, and I'll tell you what to do next.",
                    "Tell me where you are. I'll tell you your next step.", [b1, b2, b3, b4],
                    [("7.1", "How it works"), ("7.2", "Tell me"), ("7.3", "Where are you?"), ("7.4", "My notes")], ("NEXT · 8", "Before Sunday"))


# ---------------- 8 · Before Sunday ----------------

def s8():
    todo = [("Profile: your real name and your face", ""), ("Say hi in #general-chat", ""), ("Open the workbook in #resources", ""),
            ("Make your post in #accountability: “your name's 60 days”, tag 60-Day Challenge", ""),
            ("Notifications on for #announcements and #weekly-live", ""), ("Share your first post in #share-your-posts", "")]
    b1 = B(1, "8.1", "Do these before Sunday", "list-checks", [note(0, 0, 1700, lead("Before Sunday 1 November.") + "<br>" + big("Six things.", 100)),
                                                               col([check(f"m{k}", t, c) for k, (t, c) in enumerate(todo)], 16)], "Your homework")
    b2 = B(2, "8.2", "What's next", "calendar", [
        L("x0", "Sunday 1 November", "The 60-Day Challenge starts. Post your Day 1.", "flame", "gold"),
        L("x1", "Wednesday 4 November, 8pm WAT", "Our next live call, right here on the stage.", "video", "navy"),
    ], "Dates", "x0")
    edge("x0", "x1", "gold", sa="b", sb="t")
    b3 = B(3, "8.3", "Questions", "circle-help", [
        note(0, 0, 1700, big("Your turn.", 140) + '<br><span style="font:800 70px \'Plus Jakarta Sans\';color:#fff">Questions</span>'),
        row([f'<img src="kit/samuel-cutout-sm.webp" style="width:520px">',
             col([note(0, 0, 900, f'<div style="display:flex;gap:20px;align-items:center">{icon("instagram", 70)}<span style="font:800 56px \'Plus Jakarta Sans\';color:#FCDD9E">@SamuelSignals</span></div>'),
                  '<img src="kit/called-to-edit-community-dark.svg" style="width:460px">'], 50, 1000, "justify-content:center")], 60)], "Over to you")
    return assemble("8", "Before", "Sunday", "What to do this week, and what's next.",
                    "Be patient.", [b1, b2, b3], [("8.1", "Before Sunday"), ("8.2", "What's next"), ("8.3", "Questions")])


SECTIONS = [("onb00-welcome", s0), ("onb01-why", s1), ("onb02-plan", s2), ("onb03-goals", s3), ("onb04-setup", s4),
            ("onb05-channels", s5), ("onb06-most", s6), ("onb07-turn", s7), ("onb08-sunday", s8)]


def section(k):
    name, fn = SECTIONS[k]

    def build():
        reset()
        return fn(), W, None
    return name, build
