# Route Rise #3 visual sheet: one beat per main sentence.
# Frames are timeline frames on "Visuals v1 (Editor)" (23.976 fps, 0 = timeline start),
# taken from Resolve's subtitles of the final cut (2026-09-25).
# kind: intro (ideas only, never placed) | visual (rendered + placed) | aroll | screen
# layer: full = opaque full frame | overlay = alpha over the A-roll | inset = full frame with the A-roll inside

FPS = 24000 / 1001

CHAPTERS = [
    # name, start, end, Resolve clip colour, swatch
    ("Hook and intro", 0, 723, "Yellow", "#E6C229"),
    ("Tool 1: Clay", 724, 2142, "Blue", "#3B7DD8"),
    ("Clay demo: Wedge Agent Feeder", 2143, 3217, "Green", "#3FA34D"),
    ("Tool 2: Railway", 3218, 3583, "Purple", "#8A4FBF"),
    ("Railway demo: GTM playbook lead magnet", 3584, 5142, "Brown", "#8C5A3C"),
    ("Mid-video CTA: Frontal", 5143, 5845, "Pink", "#E0529C"),
    ("Tool 3: Claude + GTM OS", 5846, 9215, "Teal", "#1FA7A0"),
    ("Tool 4: Wispr Flow", 9216, 9972, "Pink", "#E0529C"),
    ("Wispr Flow demo", 9973, 11879, "Green", "#3FA34D"),
    ("Bringing the 4 tools together", 11880, 13995, "Tan", "#C4A57A"),
    ("Outro and CTA", 13996, 14267, "Violet", "#7B6FD6"),
]

# Screen recording is on (V4 Tella + V6 PIP enabled) on these timeline frames.
SCREEN_ON = [(2143, 3219), (4064, 4475), (4544, 4697), (6383, 9216), (9973, 11879)]

B = []
def beat(id, s, e, kind, vo, **kw):
    B.append(dict(id=id, start=s, end=e, kind=kind, vo=vo, **kw))

# ---------------------------------------------------------------- INTRO (ideas only)
beat("I01", 1, 99, "intro", "I've tested a lot of AI tools inside my company and I realized something.",
     type="Full-frame 3D", picture="A wall of 100+ glossy AI app tiles in a curved 3D grid on a reflective floor. The camera drifts through it while a counter rolls 0 → 100+. On \"realized something\" most tiles fade to grey and a few stay lit.",
     onscreen=["100+"], depth="Extrude3D tiles, NeoReflection floor, NeoGlow on the lit tiles, DropShadow, Vignette", motion="Slow dolly through the grid; counter rolls on a spline")
beat("I02", 100, 278, "intro", "The tools that actually matter most are not the ones with the most impressive demo, they are the ones that solve a problem you keep running into in your business.",
     type="Full-frame split", picture="Left: a flashy demo card with sparkles and a WOW badge that dims to grey with a red ✕. Right: a plain tool card beside a looping red error icon ↻ that turns into a green ✓ and stops looping.",
     onscreen=["DEMO", "PROBLEM SOLVED"], depth="NeoLightSweep on the plain card, NeoGlow on the ✓, DropShadow", motion="The flashy card enters first and fades; the plain card slides up (NeoAnim) and wins")
beat("I03", 279, 393, "intro", "So in this video, I'm going to show you four tools, what they do and how we use them at Frontal.",
     type="Full-frame 3D", picture="The 100 tiles collapse into four: Clay, Railway, Claude and Wispr Flow, each tile showing its real UI. The Frontal wordmark stamps in underneath.",
     onscreen=["4 TOOLS"], depth="3D row, NeoReflection, NeoLightSweep across the four", motion="Tiles fly into a row and settle with an overshoot")
beat("I04", 394, 590, "intro", "We're going to look at researching accounts, building a personalized lead magnet, using Claude with our business context and giving it instruction with voice.",
     type="A-roll card + numbered pills", picture="A-roll shrinks into a bordered card at the top. Four orange gradient pills build below, each with a ghost numeral and the tool's icon. Items not yet spoken stay blurred (signposting).",
     onscreen=["RESEARCHING ACCOUNTS", "PERSONALIZED LEAD MAGNET", "CLAUDE + YOUR CONTEXT", "INSTRUCTION WITH VOICE"], depth="NeoBevel + NeoLightSweep on each pill, dashed connector, DropShadow", motion="Each pill slides up on its word; the next one unblurs")
beat("I05", 591, 703, "intro", "And at the end, I will show you how these pieces can fit together in a practical workflow.",
     type="Full-frame teaser", picture="The four tiles snap into a connected workflow line, then the whole board blurs behind a COMING UP tag.",
     onscreen=["COMING UP"], depth="GaussianBlur signposting, NeoGlow on the connectors", motion="Snap-together, then blur to tease")
beat("I06", 704, 723, "intro", "Let's get into it.", type="A-roll", picture="A-roll with a quick MagicZoom punch-in.")

# ---------------------------------------------------------------- TOOL 1: CLAY
beat("B01", 724, 790, "visual", "The first tool is Clay.", layer="full", scene="tracker1",
     type="Full-frame 3D tracker", picture="Four glossy tool cards in a 3D row, each holding its tool's real UI thumbnail. Clay's card lights up and swings to face camera. Railway, Claude and Wispr Flow stay blurred: the video's progress tracker, used again at every tool.",
     onscreen=["1", "CLAY"], depth="3D perspective row (ImagePlane3D/Renderer3D), NeoBevel edge, NeoLightSweep on Clay's card, NeoGlow rim, NeoReflection floor, DropShadow", ground="Warm near-black, radial orange glow from below, grid, vignette", motion="Camera drifts right; Clay's card lifts and rotates in; the others stay blurred", sfx="Low whoosh + UI beep on the light-up")
beat("B02", 790, 998, "visual", "…manually, you know how messy it can get. You've got LinkedIn open, a company website, a database, a spreadsheet, and whatever tool you're using to send your outreach.", layer="full", scene="messy1",
     type="Full-frame UI pile-up", picture="An empty desktop fills with real-looking windows on each word: a LinkedIn profile, a company website, a database table, a spreadsheet and an outreach sequencer. They stack at odd angles until the screen is a mess.",
     onscreen=[], depth="DropShadow per window, Transform with motion blur, Vignette", ground="Blurred, dimmed desktop wallpaper", motion="Each window pops in on its word with a small overshoot; the whole stack drifts slowly", sfx="Soft UI pops, one per window (no keyboard SFX)")
beat("B03", 999, 1183, "visual", "You find one piece of information here, another one over here, and then you spend most of your time moving between all the different tabs.", layer="full", scene="messy2",
     type="Full-frame UI chaos", picture="Same desktop. A cursor darts between the windows; small data chips (email, title, headcount) jump from window to window. A browser tab bar at the top keeps switching tabs faster and faster while a red timer counts up.",
     onscreen=["timer"], depth="NeoGlow on the data chips, DropShadow, Transform motion blur", ground="Same desktop, darker", motion="Cursor path on a spline; tab switching speeds up; timer rolls", sfx="Quick tick per tab switch, low volume")
beat("B04", 1184, 1245, "visual", "At Frontal, Clay is a data orchestration tool.", layer="overlay", scene="clay_label",
     type="A-roll overlay", picture="A glossy Clay tile with a floor reflection slides up in the left third beside Alex. Under it, a two-tone title builds: DATA white, ORCHESTRATION orange.",
     onscreen=["DATA", "ORCHESTRATION"], depth="NeoBevel + NeoLightSweep on the tile, NeoReflection, NeoGlow on ORCHESTRATION, DropShadow", ground="Over A-roll", motion="NeoAnim slide-up with start blur, per word", sfx="UI double beep on the tile")
beat("B05", 1247, 1399, "visual", "What that means is that we use it to bring different sources of information together and then we decide what to do with all that data.", layer="full", scene="orchestrate",
     type="Full-frame diagram", picture="Source cards on the left (LinkedIn, company website, database, spreadsheet, CRM) send glowing data streams into a central Clay hub. From the hub, one clean record comes out and branches three ways: REACH OUT (green), ENRICH MORE (orange), SKIP (grey).",
     onscreen=["REACH OUT", "ENRICH MORE", "SKIP"], depth="NeoGlow on the streams and hub, NeoBevel on the hub, DropShadow, dashed connectors (Polygon → Paint)", ground="Warm near-black, grid, orange glow behind the hub", motion="Streams flow in on \"together\"; branches draw out on \"decide\"", sfx="Cybernetic data processing, low")
beat("B06", 1401, 1480, "visual", "So one example of a use case with Clay is a waterfall enrichment.", layer="full", scene="waterfall_title",
     type="Full-frame title + diagram", picture="A cascade of light provider cards stepping down diagonally like a waterfall, with a bright droplet of light falling from card to card. Two-tone title: WATERFALL white, ENRICHMENT orange.",
     onscreen=["WATERFALL", "ENRICHMENT"], depth="Light cards with NeoBevel, NeoGlow droplet, DropShadow, NeoLightSweep on the title", ground="Light variant: soft warm white with a faint grid", motion="Cards cascade in top to bottom; droplet falls through them", sfx="Soft riser")
beat("B07", 1480, 1664, "visual", "So for example, if you want to find an email address and one provider can't find the email you need, you can have Clay check another provider based on the workflow you have configured.", layer="full", scene="waterfall_run",
     type="Full-frame UI animation", picture="An email field at the top reads ___@company.com. Provider 1 searches and returns a red ✕. The light drops to Provider 2: red ✕. Provider 3 finds it: green ✓, and the email types into the field, which glows green.",
     onscreen=["PROVIDER 1", "PROVIDER 2", "PROVIDER 3", "email"], depth="NeoGlow green on success, red on misses, DropShadow, frosted cards over a blurred Clay table", ground="Blurred real Clay workflow (from the screen recording)", motion="Each provider spins, then resolves; the drop animates between them", sfx="Error blip ×2, success beep")
beat("B08", 1665, 1739, "visual", "This will actually improve your chances of finding the information.", layer="overlay", scene="coverage",
     type="A-roll overlay", picture="A glass card in the right third, EMAILS FOUND, whose bar fills in three coloured segments, one per provider, until it is nearly full. No numbers.",
     onscreen=["EMAILS FOUND"], depth="NeoBevel on the card, NeoGlow on the fill edge, DropShadow", ground="Over A-roll", motion="Segments fill on a spline, the last with a small overshoot")
beat("B09", 1741, 1863, "visual", "Of course, it doesn't mean that every record will be complete or that every email you find is ready to contact.", layer="full", scene="records",
     type="Full-frame UI table", picture="A light table of five contact records floats over a blurred A-roll. Some cells are empty dashes that pulse. Email statuses pop in: VERIFIED green, RISKY amber, INVALID red.",
     onscreen=["VERIFIED", "RISKY", "INVALID"], depth="White card with DropShadow, NeoGlow on the badges, GaussianBlur A-roll behind (depth of field)", ground="Blurred, dimmed A-roll still", motion="Rows slide up staggered; badges pop on \"complete\" and \"ready to contact\"")
beat("B10", 1863, 2013, "visual", "But where Clay gets really useful for us is when we go beyond finding someone's email and start researching the account itself.", layer="full", scene="account",
     type="Full-frame 3D pull-back", picture="Starts tight on a single contact card (avatar + email). The camera pulls back to show it's one small part of a large company account card, surrounded by research panels: ADS, HEADCOUNT, TECH STACK, FUNDING, HIRING.",
     onscreen=["ADS", "HEADCOUNT", "TECH STACK", "FUNDING", "HIRING"], depth="3D tilt, frosted panels with NeoBevel, NeoLightSweep on the account card, DropShadow", ground="Warm near-black, grid, glow", motion="Big pull-back on \"go beyond\"; panels pop in sequence on \"researching the account\"")
beat("B11", 2013, 2072, "visual", "You can pretty much find any data points you need with Clay.", layer="overlay", scene="datapoints",
     type="A-roll overlay", picture="Dozens of small data-point chips (icon + one word) burst up around Alex from the bottom of frame and orbit him briefly.",
     onscreen=["data chips"], depth="Glass chips with NeoGlow edges, DropShadow", ground="Over A-roll", motion="Fast burst, then a slow orbit (fast pacing)", sfx="Multiple UI beeps")
beat("B12", 2072, 2143, "visual", "So let me show you an actual workflow from our workspace directly.", layer="full", scene="to_demo_clay",
     type="Full-frame transition", picture="The real Clay workflow (Wedge Agent Feeder canvas) flies in from depth as a tilted 3D window and straightens to fill the frame, handing off to the screen recording.",
     onscreen=[], depth="ImagePlane3D tilt, DropShadow, NeoLightSweep once as it lands", ground="Warm near-black", motion="3D fly-in that ends flat and full frame, so the cut to the demo is seamless")

# ---------------------------------------------------------------- TOOL 2: RAILWAY
beat("B13", 3218, 3302, "visual", "So now the second tool is Railway. Railway is a hosting platform.", layer="full", scene="tracker2",
     type="Full-frame 3D tracker", picture="The tracker again, adapted: Clay's card now carries a green ✓ and steps back. Railway's card lights violet and turns to camera, then a HOSTING PLATFORM chip with a server icon drops under it.",
     onscreen=["2", "RAILWAY", "HOSTING PLATFORM"], depth="3D row, NeoGlow violet rim, NeoLightSweep, NeoReflection", ground="Navy-violet ground (Railway's world), grid", motion="Row slides left one slot; Railway's card lifts", sfx="Whoosh + beep")
beat("B14", 3304, 3384, "aroll", "Not sure if we can actually call it a tool per se, but I'm actually including it…", type="A-roll", picture="A-roll. Casual aside; let it breathe with a slow MagicZoom push.")
beat("B15", 3384, 3541, "visual", "…because once you have built something with AI, you need a place to deploy it and let other people use it and see it.", layer="full", scene="deploy",
     type="Full-frame diagram", picture="A laptop shows an app running only on localhost. On \"deploy\", the app window lifts off the laptop into a Railway service card in the cloud (green ONLINE dot). From there, lines fan out to many user devices that light up one by one.",
     onscreen=["localhost", "ONLINE"], depth="NeoGlow on the lines and the online dot, frosted service card with NeoBevel, DropShadow", ground="Navy-violet, grid, violet glow", motion="Lift on \"deploy\"; fan-out on \"other people use it\"", sfx="Rising whoosh on the lift")
beat("B16", 3542, 3583, "aroll", "So here's an example from our business.", type="A-roll", picture="A-roll with a quick MagicZoom punch-in.")
beat("B17", 3584, 3756, "visual", "So Kenny, my business partner, built a generator that researches a company and uses Claude to produce a personalized GTM playbook.", layer="full", scene="generator",
     type="Full-frame pipeline", picture="A left-to-right pipeline of frosted nodes that light up on the words: COMPANY WEBSITE (a site card) → RESEARCH (a magnifier scanning it) → Claude (the Claude mark) → the real \"Frontal GTM Playbook\" page as a document. A name tag KENNY · BUSINESS PARTNER sits above the pipeline.",
     onscreen=["KENNY", "PLAYBOOK"], depth="NeoGlow connectors, NeoBevel nodes, NeoLightSweep on the playbook doc, DropShadow", ground="Warm near-black, grid", motion="Nodes light in sequence on researches / Claude / playbook")
beat("B18", 3758, 3892, "visual", "The idea is to give someone in our ideal customer profile something relevant to their business before asking them to book a call.", layer="overlay", scene="value_first",
     type="A-roll overlay (right third)", picture="A prospect card with an ICP ✓ badge. First a playbook slides into their hands, glowing green (1). Only then does a BOOK A CALL calendar card appear below it (2).",
     onscreen=["ICP ✓", "1", "2", "BOOK A CALL"], depth="Glass cards, NeoBevel, NeoGlow on the playbook, DropShadow", ground="Over A-roll", motion="Stagger: playbook on \"something relevant\", call card on \"book a call\"")
beat("B19", 3893, 4005, "visual", "On our website, we have a form where you enter your email address and your company website to request that playbook.", layer="full", scene="form",
     type="Full-frame UI rebuild", picture="The real frontal.so lead-magnet block: \"See who to target. Know how to reach them.\" and the Get your free playbook form. The email field types you@company.com, the website field types yourcompany.com, and a cursor clicks Build my playbook →.",
     onscreen=["real page copy"], depth="Browser frame in slight 3D, DropShadow, NeoGlow on the focused field, NeoLightSweep on the button", ground="Blurred frontal.so page", motion="Slow push-in on the form; typing synced to the words", sfx="Soft click on the button")
beat("B20", 4006, 4064, "visual", "And here is one we generated earlier for Frontal itself.", layer="full", scene="playbook_in",
     type="Full-frame transition", picture="The Frontal GTM Playbook page swings in as a 3D document and settles flat, matching the screen recording that follows.",
     onscreen=[], depth="3D tilt, DropShadow, NeoLightSweep", ground="Warm near-black", motion="Swing-in ending flat, to hand off to the demo")
beat("B21", 4475, 4544, "visual", "So Railway has the application behind that experience.", layer="full", scene="behind",
     type="Full-frame layered reveal", picture="The playbook page swings aside like a door and reveals, behind it, the real Railway project canvas: frontal-lead-magnets, Postgres and playbook-worker, all ONLINE.",
     onscreen=["real service names"], depth="Two 3D layers, NeoGlow on the online dots, DropShadow", ground="Navy-violet", motion="Door swing on \"behind\"")
beat("B22", 4697, 4799, "visual", "We've taken a piece of expertise and turned it into something a prospect can request and use.", layer="full", scene="expertise",
     type="Full-frame transformation", picture="A glowing EXPERTISE lightbulb moves along a conveyor into a Railway box and comes out as a product card, PLAYBOOK GENERATOR, with a REQUEST button that a cursor clicks.",
     onscreen=["EXPERTISE", "REQUEST"], depth="NeoGlow bulb, NeoBevel product card, NeoLightSweep on the output, DropShadow", ground="Warm near-black, grid", motion="Conveyor left to right; the output pops with an overshoot")
beat("B23", 4804, 4926, "visual", "You could apply the same idea to a calculator, an audit, or a research report for your own market.", layer="full", scene="three_ideas",
     type="Full-frame 3D card row", picture="Three product cards rise in a perspective row, one per word, each with a different fill: CALCULATOR (numbers ticking, orange gradient), AUDIT (checklist ticking, white card), RESEARCH REPORT (doc with a rising chart, dark glass).",
     onscreen=["CALCULATOR", "AUDIT", "RESEARCH REPORT"], depth="3D row, NeoBevel, NeoLightSweep per card on arrival, NeoReflection, DropShadow", ground="Warm near-black with glow", motion="Cards rise on their words; the camera drifts across the row")
beat("B24", 4926, 5039, "visual", "Start with a question that your buyers actually care about, then build something that helps them answer it.", layer="inset", scene="question_answer",
     type="A-roll card + numbered pills", picture="A-roll shrinks into a bordered card at the top. Two orange gradient pills build below with ghost numerals: 1 THEIR QUESTION (with a ? icon), 2 YOUR ANSWER (with a ✓ icon). Pill 2 stays blurred until he says it.",
     onscreen=["1 THEIR QUESTION", "2 YOUR ANSWER"], depth="NeoBevel + NeoLightSweep on the pills, dashed connector, DropShadow on the A-roll card", ground="Warm near-black", motion="A-roll card slides down; pills slide up; blur signposting")
beat("B25", 5039, 5141, "visual", "An email capture form is actually only useful if the thing behind it is worth requesting.", layer="full", scene="form_door",
     type="Full-frame comparison", picture="Two email forms side by side. Each swings open like a door. The left one reveals an empty box and turns red ✕. The right one reveals a glowing playbook and turns green ✓.",
     onscreen=["✕", "✓"], depth="3D doors, NeoGlow green and red, NeoBevel, DropShadow", ground="Warm near-black, grid", motion="Left opens first, then right, on \"worth requesting\"")

# ---------------------------------------------------------------- MID-CTA
beat("B26", 5143, 5228, "visual", "I know that learning all of those tools can feel super overwhelming.", layer="inset", scene="overwhelm",
     type="Graded A-roll + rain", picture="The A-roll goes black and white with a red wash (your TSB move for a negative beat) while dozens of AI app tiles rain down and pile up around him.",
     onscreen=[], depth="Colour treatment on the A-roll (desaturate + red tint), DropShadow on the tiles, motion blur", ground="The A-roll itself", motion="Tiles rain faster and faster")
beat("B27", 5231, 5364, "visual", "And if you're running a business, you probably don't have time to figure out every connection and every different tool by yourself.", layer="full", scene="tangle",
     type="Full-frame diagram", picture="A lone founder node in the middle, surrounded by tool nodes whose connections tangle into red spaghetti. A clock face in the corner spins fast.",
     onscreen=[], depth="NeoGlow red on the tangled lines, DropShadow", ground="Dark with a red glow (problem)", motion="Lines draw and tangle; the clock spins")
beat("B28", 5364, 5398, "aroll", "And that's where we can actually help.", type="A-roll", picture="A-roll, fast MagicZoom punch-in. The turn to the offer.")
beat("B29", 5400, 5557, "visual", "At Frontal, we help B2B companies build and run the go-to-market system across GTM engineering, paid media, and content.", layer="full", scene="frontal_pillars",
     type="Full-frame brand", picture="The real frontal.so hero (\"Grow Revenue Without Adding Headcount.\") blurred behind. The Frontal wordmark lands, then three orange gradient pillar cards rise on their words: GTM ENGINEERING, PAID MEDIA, CONTENT.",
     onscreen=["GTM ENGINEERING", "PAID MEDIA", "CONTENT"], depth="NeoBevel + NeoLightSweep on the cards, ghost numerals, NeoGlow on the wordmark, DropShadow", ground="Blurred frontal.so hero", motion="Wordmark first, then the three cards staggered on their words")
beat("B30", 5558, 5700, "visual", "So if you already have a product that people buy and you have a sales team ready to sell more, where your acquisition process is broken,", layer="overlay", scene="qualify",
     type="A-roll overlay (left third)", picture="A tall glass checklist card beside Alex. Three rows tick on their words: PRODUCT PEOPLE BUY ✓, SALES TEAM READY ✓, and ACQUISITION BROKEN, which gets a red cracked-pipe icon.",
     onscreen=["PRODUCT PEOPLE BUY", "SALES TEAM READY", "ACQUISITION BROKEN"], depth="Glass card with NeoBevel, NeoGlow green/red, DropShadow", ground="Over A-roll", motion="Rows slide up on their words")
beat("B31", 5702, 5815, "visual", "…book a call using the link in the description. We can look at your current setup and where it makes sense to improve it.", layer="overlay", scene="cta_desc",
     type="A-roll overlay (bottom)", picture="A YouTube description box slides up from the bottom with the booking link highlighted. A cursor clicks it and the real \"Book Your Strategy Call\" page pops up as a card beside Alex.",
     onscreen=["LINK IN THE DESCRIPTION"], depth="DropShadow, NeoGlow on the link, NeoLightSweep on the card", ground="Over A-roll", motion="Slide-up, click, pop")
beat("B32", 5815, 5844, "aroll", "So now let's get back into it.", type="A-roll", picture="A-roll. Quick punch-out back to the wide.")

# ---------------------------------------------------------------- TOOL 3: CLAUDE
beat("B33", 5846, 5972, "visual", "The third tool is Claude. You can already use Claude to research a topic, review a document, or write a first draft.", layer="full", scene="tracker3",
     type="Full-frame tracker → UI", picture="Tracker: Clay ✓ and Railway ✓ step back, Claude's card lights terracotta. It grows into Claude's real home screen (\"Welcome\" + prompt box), where three task chips drop in on his words: RESEARCH A TOPIC, REVIEW A DOCUMENT, WRITE A FIRST DRAFT.",
     onscreen=["3", "CLAUDE", "RESEARCH A TOPIC", "REVIEW A DOCUMENT", "WRITE A FIRST DRAFT"], depth="3D card to flat UI, NeoGlow terracotta rim, DropShadow on the chips", ground="Warm near-black → Claude cream", motion="Card expands into the UI; chips drop in on their words")
beat("B34", 5972, 6117, "visual", "But the part I want to show you is how useful it becomes when you give it the context and instruction for the way your business actually works.", layer="full", scene="context_diff",
     type="Full-frame comparison", picture="Two Claude windows. Left, no context: a grey, generic answer. Right: context files (CLIENTS, ICP, PLAYBOOKS, TONE OF VOICE) fly into the prompt, and the answer fills with specific lines highlighted in orange.",
     onscreen=["CLIENTS", "ICP", "PLAYBOOKS", "TONE OF VOICE"], depth="Cream cards with DropShadow, NeoGlow on the highlighted lines, NeoLightSweep on the right window", ground="Light variant: Claude cream with a faint grid", motion="Files fly in on \"context and instruction\"; the answer writes itself")
beat("B35", 6118, 6188, "visual", "So Kenny has been building a GTM operating system for our team.", layer="full", scene="gtm_os",
     type="Full-frame real UI", picture="The real GitHub repo card frontal-gtm-os (folder list, About: Frontal's GTM Engineering workspace) tilts in. A boot bar under it fills: FRONTAL GTM OS.",
     onscreen=["FRONTAL GTM OS"], depth="3D tilt, DropShadow, NeoLightSweep, NeoGlow on the boot bar", ground="Warm near-black", motion="Tilt-in, boot bar fills")
beat("B36", 6189, 6380, "visual", "It brings together all of the working context about the clients, about the tools, about the workflows, reusable instructions, and then all the tools to actually do the work.", layer="full", scene="os_assemble",
     type="Full-frame assembly", picture="The GTM OS core in the middle. Folder cards fly in from four sides and slot into sockets on their words: CLIENTS, TOOLS, WORKFLOWS, INSTRUCTIONS. Then tool icons plug in along the bottom (\"tools to do the work\") and the whole core glows.",
     onscreen=["CLIENTS", "TOOLS", "WORKFLOWS", "INSTRUCTIONS"], depth="NeoBevel core, NeoGlow sockets, NeoLightSweep on completion, DropShadow", ground="Warm near-black, grid", motion="Each folder lands on its word; final glow pulse")

# ---------------------------------------------------------------- TOOL 4: WISPR FLOW
beat("B37", 9216, 9312, "visual", "And now the fourth tool is Wispr Flow. This one is much simpler.", layer="full", scene="tracker4",
     type="Full-frame tracker", picture="Tracker complete: all four cards lit, three with ✓. Wispr Flow's card comes forward. On \"much simpler\" the others fall away and only one mic button remains, glowing.",
     onscreen=["4", "WISPR FLOW"], depth="3D row, NeoReflection, NeoGlow on the mic", ground="Warm near-black", motion="Row slides; the Wispr card comes forward; the rest drop away")
beat("B38", 9313, 9460, "visual", "It lets you dictate into the place where you would normally type. So it just allows you to go much faster with everything you should be doing.", layer="full", scene="dictate",
     type="Full-frame UI mockup", picture="A message compose box with Wispr Flow's black dictation pill at the bottom, bars moving. Text streams into the box at speaking speed. Then Wispr's real stat card from Alex's dashboard counts up: 168 WPM.",
     onscreen=["168 wpm"], depth="DropShadow, NeoGlow on the pill, glass stat card", ground="Light: Wispr cream UI", motion="Waveform animates; text streams; counter rolls")
beat("B39", 9461, 9656, "visual", "When I'm giving AI instruction, the useful context is often already in my head, but I need to explain what we are trying to achieve, what we are targeting, and what I don't want it to assume.", layer="overlay", scene="in_my_head",
     type="A-roll overlay (right third)", picture="Three cards float up from beside his head on their words: GOAL (target icon, orange), TARGETING (crosshair, teal), DON'T ASSUME (red ✕).",
     onscreen=["GOAL", "TARGETING", "DON'T ASSUME"], depth="Glass cards, NeoBevel, NeoGlow per colour, DropShadow", ground="Over A-roll", motion="Float up on each phrase, staggered")
beat("B40", 9659, 9730, "visual", "And putting all of this by writing is really time-consuming.", layer="full", scene="slow_typing",
     type="Full-frame UI", picture="The same compose box, now typed by hand: the cursor crawls one letter at a time while a red clock chip counts minutes up fast.",
     onscreen=["timer"], depth="DropShadow, NeoGlow red on the timer", ground="Wispr cream UI, dimmed", motion="Slow typing vs a fast clock (no keyboard SFX)")
beat("B41", 9733, 9971, "visual", "So for example, I can say: review the list summary for B2B outbound campaign, tell me which records still need verification, what information is missing, and what we should check before using the contacts on LinkedIn.", layer="full", scene="dictate_prompt",
     type="Full-frame UI mockup (word-synced)", picture="Claude's prompt box with Wispr Flow's dictation pill listening underneath. His words appear in the prompt as he says them, cleaned up. At the end the prompt sends.",
     onscreen=["his prompt, word-synced"], depth="DropShadow, NeoGlow on the pill, NeoLightSweep on send", ground="Claude cream", motion="Words appear on his timing; waveform follows his voice")

# ---------------------------------------------------------------- BRINGING THE 4 TOGETHER
beat("B42", 11880, 11937, "visual", "Now, how would I actually bring those four tools together?", layer="full", scene="together",
     type="Full-frame 3D", picture="The four tracker cards fly to the centre and lock together into one connected unit, with lines glowing between them.",
     onscreen=[], depth="3D, NeoGlow connectors, NeoLightSweep across the joined unit, NeoReflection", ground="Warm near-black", motion="Fly-in and lock with a small bounce", sfx="Low hit on the lock")
beat("B43", 11940, 12050, "visual", "Let's say we want to start more relevant conversations with a specific type of B2B company.", layer="full", scene="segment",
     type="Full-frame diagram", picture="A grid of grey company cards. A spotlight sweeps and a filter lights up six of them orange. Chat bubbles appear between YOU and those six.",
     onscreen=["YOU"], depth="NeoGlow on the lit companies, DropShadow", ground="Warm near-black, grid", motion="Sweep, filter, bubbles")
beat("B44", 12051, 12134, "visual", "First, I would define the audience and the problem we can help them solve.", layer="full", scene="board1",
     type="Full-frame workflow board", picture="Step 1 of the workflow board: an orange pill 1 DEFINE with two cards under it, AUDIENCE (people icon) and PROBLEM (warning icon). Dashed connectors wait for steps 2–4, blurred.",
     onscreen=["1 DEFINE", "AUDIENCE", "PROBLEM"], depth="NeoBevel + NeoLightSweep pill, glass cards, dashed connectors (Polygon → Paint), blur signposting", ground="Warm near-black, grid", motion="Pill slides up; cards on their words")
beat("B45", 12134, 12288, "visual", "So of course, I can use Wispr Flow to get all of that context into a written brief and then work through Claude Code to actually make it real.", layer="full", scene="brief_code",
     type="Full-frame UI chain", picture="Wispr Flow's pill listens; words stream into a BRIEF.md document card. The card slides into a Claude Code terminal where lines run and end in a green ✓ Built.",
     onscreen=["BRIEF.md", "Claude Code", "✓"], depth="Terminal window with DropShadow, NeoGlow on the ✓, NeoLightSweep on the doc", ground="Warm near-black", motion="Stream → slide → run")
beat("B46", 12290, 12478, "visual", "Next, I would use Clay to bring together the account research we need. That would include advertising activity, team information, and other signals relevant to our offer.", layer="full", scene="board2",
     type="Full-frame UI (callback)", picture="Step 2 lights: Clay. A light Clay-style table fills column by column with the real column names from his demo: LINKEDIN ADS and META ADS (advertising activity), SDR HEADCOUNT (team info), EMAIL INFRA and SIGNALS. Cells fill with green ticks.",
     onscreen=["2 RESEARCH", "LINKEDIN ADS", "META ADS", "SDR HEADCOUNT", "SIGNALS"], depth="White card with DropShadow, NeoGlow ticks", ground="Warm near-black", motion="Columns fill on their words")
beat("B47", 12480, 12585, "visual", "Then I can have Claude help review that research and draft a useful angle for the conversation and the messaging,", layer="full", scene="board3",
     type="Full-frame UI", picture="Step 3 lights: Claude. Research rows flow into Claude; out comes an ANGLE card with the trigger from his demo (New BDR starting → reach out to the CRO), then an email draft writes itself underneath.",
     onscreen=["3 ANGLE", "NEW BDR STARTING"], depth="Cream cards, NeoGlow on the angle, DropShadow", ground="Warm near-black → cream card", motion="Flow in, angle pops, draft writes")
beat("B48", 12585, 12722, "visual", "…using instructions and the evidence we've collected about what campaigns and what copy actually work.", layer="full", scene="evidence",
     type="Full-frame diagram", picture="A stack of past campaign cards with reply bars (no numbers). The winners glow green and slide into Claude's input with an INSTRUCTIONS doc. The losers stay grey.",
     onscreen=["INSTRUCTIONS"], depth="NeoGlow on the winners, DropShadow, 3D stack", ground="Warm near-black", motion="Sort, then slide in")
beat("B49", 12722, 12888, "visual", "And then if sending a personalized resource makes sense, I could actually build an entire application hosted on Railway,", layer="full", scene="board4",
     type="Full-frame build", picture="Step 4 lights: Railway. App UI blocks snap together (header, form, button) and drop onto a Railway canvas, where service cards connect: web, Postgres, worker, all ONLINE.",
     onscreen=["4 BUILD", "ONLINE"], depth="NeoBevel blocks, NeoGlow on the online dots, DropShadow", ground="Navy-violet", motion="Snap together, then deploy")
beat("B50", 12889, 12974, "visual", "…so I can turn that idea into something that the prospect would actually use and care about.", layer="full", scene="prospect_uses",
     type="Full-frame UI", picture="On a prospect's laptop the app opens. They click Get my playbook, it arrives, and a green heart reaction pops.",
     onscreen=[], depth="DropShadow, NeoGlow on the heart", ground="Soft blurred office", motion="Click, arrive, react")
beat("B51", 12974, 13014, "visual", "Exactly like the playbook I just showed you.", layer="overlay", scene="polaroid",
     type="A-roll overlay", picture="The real playbook page drops in beside him as a polaroid with a slight tilt (the guide's way to repeat a visual).",
     onscreen=[], depth="DropShadow, NeoLightSweep on the polaroid", ground="Over A-roll", motion="Drop with rotation and settle")
beat("B52", 13015, 13058, "visual", "Those are the roles each tool can play.", layer="full", scene="board_full",
     type="Full-frame hero", picture="The whole workflow board zooms out: DEFINE → RESEARCH (Clay) → ANGLE (Claude) → BUILD (Railway), with Wispr Flow feeding the first step. Each tile lights in turn.",
     onscreen=["DEFINE", "RESEARCH", "ANGLE", "BUILD"], depth="NeoGlow connectors, NeoLightSweep chase, NeoReflection", ground="Warm near-black, grid", motion="Zoom out; a light chase runs along the flow")
beat("B53", 13059, 13177, "visual", "Connecting the whole process still takes setup, and you need to decide where a person should review the output.", layer="full", scene="review_gate",
     type="Full-frame board (continued)", picture="Same board: some connectors turn to dashed lines with a wrench icon (setup). A HUMAN REVIEW gate (person + eye icon) drops in between ANGLE and SEND.",
     onscreen=["HUMAN REVIEW"], depth="NeoGlow on the gate, dashed lines, DropShadow", ground="Warm near-black", motion="Wrench icons pop; the gate drops in")
beat("B54", 13177, 13345, "visual", "Because again, I already mentioned it in a lot of videos, but before scaling it, I would always test things on a small scale before automating anything.", layer="overlay", scene="test_first",
     type="A-roll overlay (left third)", picture="Two numbered cards beside him: 1 TEST SMALL (green, lit) and 2 AUTOMATE (grey with a padlock). On \"before automating\" the padlock wobbles but stays shut.",
     onscreen=["1 TEST SMALL", "2 AUTOMATE"], depth="Glass cards, NeoBevel, NeoGlow green, DropShadow", ground="Over A-roll", motion="Stagger in; lock wobble")
beat("B55", 13346, 13404, "aroll", "This is something I tell the team and clients all the time.", type="A-roll", picture="A-roll with a MagicZoom punch-in.")
beat("B56", 13405, 13539, "visual", "Why would you start an outbound campaign to 5,000 people if you actually haven't made it work manually for 25?", layer="full", scene="5000_vs_25",
     type="Full-frame contrast", picture="Left: a huge dot field with a counter rolling to 5,000, a SEND button and a red warning. Right: a 5×5 grid of 25 people, each getting a hand-written message, lit green.",
     onscreen=["5,000", "25"], depth="NeoGlow red and green, DropShadow", ground="Warm near-black", motion="Counter rolls on \"5,000\"; the 25 appear on \"25\"")
beat("B57", 13547, 13724, "visual", "Always use those first manual conversations to find out whether the problem matters, whether your offer makes sense, and whether the resource is actually useful.", layer="full", scene="three_checks",
     type="Full-frame list (signposting)", picture="Chat bubbles on the left (the manual conversations). Three light check cards on the right tick on their words: PROBLEM MATTERS, OFFER MAKES SENSE, RESOURCE IS USEFUL. Unspoken cards stay blurred.",
     onscreen=["PROBLEM MATTERS", "OFFER MAKES SENSE", "RESOURCE IS USEFUL"], depth="White glass cards, NeoGlow green ticks, DropShadow, blur signposting", ground="Warm near-black", motion="Unblur and tick on each phrase")
beat("B58", 13724, 13813, "visual", "And then when it's working at a small scale, then you have something that's worth automating.", layer="full", scene="scale_up",
     type="Full-frame diagram", picture="The green circle of 25 duplicates outwards through a gear into many circles, and a line climbs.",
     onscreen=[], depth="NeoGlow, DropShadow", ground="Warm near-black", motion="Duplicate outwards; the line draws up")
beat("B59", 13815, 13847, "visual", "Clay coordinates the data.", layer="full", scene="recap1",
     type="Full-frame recap (1/4)", picture="The final form of the tracker: four big glossy cards in a 3D row on a reflective floor. Clay lights, with one line under it: COORDINATES THE DATA. The rest are blurred.",
     onscreen=["CLAY", "COORDINATES THE DATA"], depth="3D row, NeoReflection, NeoLightSweep on the lit card, NeoGlow", ground="Warm near-black, glow", motion="Continuous scene cut into four clips")
beat("B60", 13850, 13907, "visual", "Claude helps us research, build and review.", layer="full", scene="recap2", type="Full-frame recap (2/4)", picture="Claude lights: RESEARCH · BUILD · REVIEW.", onscreen=["CLAUDE", "RESEARCH · BUILD · REVIEW"], depth="As B59", ground="As B59", motion="Continues")
beat("B61", 13909, 13955, "visual", "Railway hosts the application,", layer="full", scene="recap3", type="Full-frame recap (3/4)", picture="Railway lights: HOSTS THE APP.", onscreen=["RAILWAY", "HOSTS THE APP"], depth="As B59", ground="As B59", motion="Continues")
beat("B62", 13955, 13995, "visual", "and Wispr Flow actually helps us move faster.", layer="full", scene="recap4", type="Full-frame recap (4/4)", picture="Wispr Flow lights: MOVE FASTER. All four glow together at the end.", onscreen=["WISPR FLOW", "MOVE FASTER"], depth="As B59", ground="As B59", motion="Continues; final light sweep across all four")

# ---------------------------------------------------------------- OUTRO
beat("B63", 13996, 14094, "visual", "Start with the workflow your business needs and choose the tools that help you make it work.", layer="full", scene="workflow_first",
     type="Full-frame diagram", picture="A workflow outline draws itself in dashed lines with empty slots. Then the four tool tiles drop into the slots.",
     onscreen=["WORKFLOW", "TOOLS"], depth="Dashed lines (Polygon → Paint), NeoGlow on each slot filling, DropShadow", ground="Warm near-black", motion="Draw on \"workflow\"; drop on \"choose the tools\"")
beat("B64", 14096, 14215, "visual", "If you want to see more of how I use Claude and Clay together for prospecting, you can watch this video next.", layer="overlay", scene="watch_next",
     type="A-roll overlay (end card)", picture="A YouTube video card slides in beside him with a placeholder thumbnail (Claude + Clay) and a WATCH NEXT tag. A cursor hovers it. Swap in the real end-screen video.",
     onscreen=["WATCH NEXT"], depth="DropShadow, NeoLightSweep on the card", ground="Over A-roll", motion="Slide in; cursor hover", notes="Which video is next isn't known; placeholder thumbnail.")
beat("B65", 14216, 14265, "aroll", "Thanks a lot for watching and I will see you in the next one.", type="A-roll", picture="A-roll to the end.")

# Close tiny gaps: a visual runs up to the next beat when that beat starts within 8 frames,
# so two full-frame visuals never flash A-roll between them.
_seq = [b for b in B if b["kind"] != "intro"]
for _a, _b in zip(_seq, _seq[1:]):
    if _a["kind"] == "visual" and 0 < _b["start"] - _a["end"] <= 8:
        _a["end"] = _b["start"]
# the recap is one continuous scene cut into four clips
for _b in B:
    if _b["id"] in ("B59", "B60", "B61", "B62"):
        _b["scene"] = "recap"
# Butt visuals against the screen-recording stretches too (no A-roll flash frames at the joins).
for _b in B:
    if _b["kind"] != "visual": continue
    for _s, _e in SCREEN_ON:
        if 0 < _s - _b["end"] <= 8: _b["end"] = _s
        if 0 < _b["start"] - _e <= 8: _b["start"] = _e
