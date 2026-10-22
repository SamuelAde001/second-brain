---
type: knowledge
area: video-editing
status: active
updated: 2026-09-26
source: memory-export
tags: [conventions, agents, fusion]
---

# Ways of working — the rules for anyone editing with Samuel

From the Claude memory export for the video-editing project, last updated 2026-09-19. **This is the single most important note for the Phase 4 video-editing agent.** It is not theory: most of these rules exist because something was done wrong once and corrected.

> **2026-10-20: Alex's videos follow Frontal's brand kit v2.3.1** ([[03-Areas/video-editing/clients/frontal-brand-v2|Frontal brand v2.3.1]]; Samuel: *"they are a must follow"*). Every rule below that names orange, BGORANGE, Geist, two-tone white/orange, pills, capsules, rounded corners, Neo Glow on borders or rings, light sweeps, shines, bevels, drop shadows on cards, curved arrows or orange icons is superseded for Alex. Everything else stands: editable nodes, real UI, show actions, variety, placement, pacing, node layout, sound, revision rules. Mapping: [[04-Projects/frontal-rebrand-video-kit|Frontal rebrand of the video kit]].

## Node naming — strict

- **Never rename Samuel's existing Fusion nodes.**
- Every new node's name must include its node type: `Transform_D01`, `Merge_Cell_D01`, `Background_D01`.
- **Never** use abbreviations or role-only names like `XF_`, `Cell_`, `Stack_`.

## Asset generation

- Samuel pastes `.setting` file content **directly into the Fusion node graph**. Claude generates those programmatically with Python.
- **Node layout coordinates must be included** — `ViewInfo = OperatorInfo { Pos = { x, y } }` — or the flow view comes out as a stacked blob.
- **Visuals are ALWAYS built as Fusion nodes so he can edit them later.** Never an animated PNG, PNG sequence or any other raster dropped into Fusion.

## Design constraints

- Brand colour `#00ACEA`.
- **All rectangles use RectangleMask nodes** — never polygon masks for rectangles.
- Circles use **EllipseMask + Instance Ellipse** (Solid off, border on), as in his verified SIGNALS comp. (Previously: RectangleMask with `CornerRadius = 1.0`.)
- Fusion colour values in **normalised 0–1 float**.
- **Don't apply a client's brand font or colours** to things built for him — e.g. B-roll pages — unless he explicitly asks.

## Visual direction requests — the standing format

> When Samuel asks for visual ideas, the deliverable is **always a full cut sheet as an HTML page** — never a chapter-level summary in chat.

Every main sentence of VO gets its own beat with a visual assigned. Beats are detailed: the specific picture, on-screen text strings, screenshots and screen references, and motion. **He corrected this once already** — a chapter-level summary was delivered instead. Do not repeat it. See [[cut-sheets]].

## Editorial process

Phase-gated. Phases are defined upfront — **intake → cut analysis → transcript → chapter markers** — and each phase is completed fully before the next begins.

## How he collaborates

- **Pragmatic.** He wants the simplest rig that achieves the result, complexity added only when a specific problem actually appears. **He pushes back on over-engineered solutions.**
- He communicates precisely about what is missing, and expects **proactive identification of production-logistics problems**.
- For a structurally ambiguous decision — grid maths with no clean division, say — **ask one targeted clarifying question before rebuilding.** Otherwise proceed on sensible assumptions and flag them.

## Fusion build conventions — his house method

**Box with outline:** RectangleMask → Background (dark fill), plus an **Instance** of that same RectangleMask with `Solid = 0` and `BorderWidth` ~`0.00184` → a second Background in the light border colour, merged over the fill. Both Backgrounds masked by their respective rectangle. Then a **NeoLightSweep Pro** macro over the result for the shine — *"this is what gives cards the modern feel."*

**Circle with outline:** the same pattern with Ellipse + Instance Ellipse (instance has Solid off, Border on).

**Lines:** a Polygon on a Background node. Nothing more.

**Colour rule:** the accent colour varies per video. The background fill is a **darker shade of the same accent**; the border is the **lighter** one. His worked example: border `1, 0.3529, 0.1216` (`#ff5a1f`) with fill `0.1059, 0.0353, 0.0118` — accent × ~0.10. Accent for the Cold Outreach / Frontal video is **`#ff5a1f`**.

**On-screen card text** is bold white ALL CAPS. Numbered list cards use a white circle with the accent numeral to the left of the bar, plus an icon circle inside the bar.

> From now on, any visual proposed or built should use these boxes and circles.

### Node tree layout — follow this

- **One horizontal merge spine, left → right on a single row.** Every Merge sits on that row.
- Each element's generator stack (Rectangle/Ellipse → Background, Text+, imported PNG) sits **directly above** the Merge where it enters the spine, feeding down into it.
- The effects chain runs **inline on the spine in order** — NeoBevel, NeoLightSweep, DropShadow, NeoAnim — never hung off to the side.
- Source footage (Adjustment Clip / MediaIn) enters at the **bottom right** and merges into the final Merge before `MediaOut1`, which sits far right.
- Third-party macros in use: **NeoLightSweep Pro, NeoBevel, NeoAnim, NeoTextMotion, MosaicBlur.**
- **A set of repeated elements (pills, cards, logos)**, Samuel's arrangement, 2026-10-01 (*"Next time arrange this kind of nodes like this"*, screenshot of the Apollo hook pills): **one row per element**, rows evenly spaced down the flow. Each row is its own spine, left to right, ending in its placement Transform. **The collector Merges sit in one vertical column on the right**, each level with its row's last node, chained top to bottom, with the clear canvas Background at the top of the column. The bottom Merge of the column feeds the comp.
- **This applies to every group of similar nodes, not only hook pills** (Samuel, 2026-10-02, on the Apollo B04 comp: *"Similar nodes on the same node line connected to a BG canvas, you are connecting them all to the main line"*, *"I prioritise node arrangement as it helps me navigate"*). Table rows, pills, arrows, logos: each group is collected over its own clear canvas and joins the main line (or the card line) **once**. Never chain the members of a group straight onto the main line.
- **The approved standard, every comp from now on** (Samuel, 2026-10-02, on Apollo B04 v2: *"Better node arrangement, ALWAYS KEEP THE NODES ORGANISED LIKE THIS"*). Reference build: the Apollo job's `Graphics\Visuals v3\build_B04.py`.
  - **Main line** at the bottom, left to right: his BGORANGE nodes laid out at its start → one Merge per group (`Merge_Card`, `Merge_Arrows`, `Merge_Pills`) → `MediaOut1` far right. Nothing else merges onto it.
  - **A container (card) gets its own line** above the main line: canvas → fill → one Merge per sub-group (`Merge_Header`, `Merge_Table`) → effects inline (dim, DropShadow) → its animation Transform, which drops straight down into its main-line Merge.
  - **Loose parts of one container** (header texts, chip, divider, column heads, footer) sit on **one line over their own clear canvas**, each part's generators straight above its Merge; the line's last Merge drops into the container line.
  - **Repeated elements** (table rows, pills, arrows): **one row each**, ending in its own Transform; a **collector column** to the right with its clear canvas on top, one Merge level with each row, chained down; the bottom Merge drops straight into the line it feeds.
  - Groups sit side by side above the main line, each collector column directly above the Merge it feeds, so every link is short and straight. No two nodes share a position, no long diagonal wires.

## Never position with a Merge — Samuel, 2026-09-27

*"NEVER EVER Reposition anything with a Merge node."* Every Merge keeps Center 0.5/0.5, Size 1 and Angle 0. Position, scale and rotation go on a **Transform** (or the element's own Center: mask, Text+, Background) before it enters the merge. A logo is Loader → Transform (Size, Center) → Merge. When the foreground is smaller than the frame, its Transform Center is in the foreground's own units: offset = 0.5 + dx_px / fg_width_px.

## Two kinds of visual only — Samuel, 2026-09-27 (Route Rise #3 v2 review)

From his answers on all 63 remaining beats, checked against his finished hook (0:00–0:41).

- **Motion graphics are Fusion nodes, always.** *"When my client sends in changes, I don't want to always have to have Claude re-render everything… I can change the nodes, change the text, change the animation by myself."* Rendered video is only for **real-UI demos**.
- **UI demos:** full screen, no background, real UI (his Chrome, Google Images, or an HTML rebuild that looks like the real app), with smooth, unhurried cursor movement: *"nothing should be too fast and everything must be very smooth"*. **Never a motion graphic on a UI visual**: no timer chips, no labels, no shine. Where a line describes what a tool does ("Clay is a data orchestration tool", "research the account"), show the tool doing it as a demo, not a diagram.
- *(Superseded 2026-10-20 for Alex: the ground is BGFRONTAL, Dark with blue light. See the banner at the top.)* **Background for every motion graphic: his `BGORANGE` macro** (`My macros\BGORANGE.setting`). Stay on brand orange. Never a tool's brand colour (Railway was not to be purple) or a blue/purple ground.
- **Lines:** `Moving dashed line`. **Arrows:** his arrow macro (`Arrowline`). **Icons:** real ones from flaticon, or the tool's real logo. Never a screenshot thumbnail standing in for a logo.
- **"Premium" means the hook's look:** two-tone Geist ExtraBold titles (white + orange) with glow, glass pills with an orange border, orange numbered circles, ghost numerals, orange icons, curved white arrows, a circular A-roll with an orange ring.
- **Hub = a circle** with the tool's logo and name, not a screen.
- **Tool reveals copy his Clay reveal exactly** (V3 adjustment clip, Cut v6 0:30.16): *"The 4 tools"* cards, the named tool's card lit and zoomed in, the others desaturated, with their opacity down and MosaicBlurred. Same logos, same layout, orange for every tool.
- **Pills beside him** sit on an adjustment clip over the A-roll and come in with Neo Anim, joined by an arrow line. No extra lines.
- **Text-only beats:** NeoTextMotion over a dark gradient at the bottom (`Down fade`), in an adjustment clip. Nothing else.
- **People beats** ("business owner confused"): an AI video generated in **Flow, in his browser**. Beats about Alex himself: B-roll of Alex from earlier Route Rise projects, plus a node element (such as a thought bubble).
- **Flow model: Omni Flash** (Samuel, 2026-10-03: *"Next time, use the Omni Flash model when generating AI B-roll"*). Not Veo 3.1 Quality (100 credits a take); Omni 1.1 Flash costs about 12.
- Many sentences get **no visual** (his NONE rows): let the A-roll breathe. He handles punch-ins himself.

## Mix the designs — Samuel, 2026-09-30

After the Apollo stills: *"You tend to use the same Design every time, the same color ratio, yes we have a color we use but, mix it up, use light and dark orange and white, and sometimes grey"* and *"Same font, Same color schemes, but more creative ways of doing things"*.

- No single pill, box or card style carries a whole video. The [[03-Areas/video-editing/motion-gallery/motion-gallery|Motion gallery]] (all 36 approved, 2026-09-30) is **inspiration, not templates**. Samuel: *"this designs must not be exact like this on my edits, but this designs are impirations of what we could work with in real designs, inspirations in which can be used in the actual designs in more creative ways, so better be more creative"*. Never drop a gallery design into an edit as it is. Take its parts (the medallion, the status tag, the border beam, the ghost numeral, the hub ring, the corner badge) and combine them into the picture the sentence needs.
- **Every pill, box or card built in Fusion starts from gallery parts, never the #3 hook-pill construct as it stands.** On 2026-10-01 I built the Apollo tool pills from it (rounded rectangle, thin orange border, small square logo tile) and Samuel asked *"what kind of boxes are those"*: it reads as a generic box. Logo + name = the P01 medallion pill (full capsule, white medallion with an orange ring holding the real logo).
- A video gets its own motifs, recurring pieces that carry its story. Apollo has two: the GTM OS core and the build board.
- Rotate the fill: solid orange, white, light orange or cream, grey glass, deep orange, outline. Neighbouring visuals never share one.
- The last three finals ($7M Founder, Taking a Step Back, 4 AI Tools) are the approved baseline (*"the finished videos of the last 3 are okay, just that we need more better and different types"*). Build on them; don't repeat one of them beat after beat.
- **The ground never changes: BGORANGE or the A-roll.** He sent all 13 gallery designs on grey, cream or orange grounds back with *"The background must be BGorange"*, and *"I want a consistent background"*. The fills change; the ground doesn't.
- From his round-1 review of the gallery: no 3D tilt or rotation on cards (*"I don't like the rotation"*); side graphics like a card deck stay small; a quote goes on the footage of the person who said it; results go in one card, not a grid of tiles; a progress indicator is a bar that fills, not dots; nothing moving in the background behind a pill (*"don't use that background wave"*); a Dynamic Island notification over the A-roll rises from the bottom.

## Show actions, don't label them — Samuel, 2026-10-02

On the Apollo v3 review (marker 952–3017): *"Please learn to use real world examples, screenshots, real UI, or mockup demo's than just text in pills alone to show actions, Text in pills can show list or Nouns, but not for actions"*.

- When Alex describes something being **done** (finding companies, filtering, writing an email, recording calls, notes from a campaign), show it being done: a UI demo built from scratch, a real screenshot, or real B-roll, full screen.
- Pills and tags carry **nouns and lists** only (CALLS, TEAM KNOWLEDGE, the three questions). Never a pill that names an action in place of showing it.
- No helper text he didn't ask for: no "same on paper", no "connected" pill, no small status tags like "NOT INCLUDED".
- Elements enter from where they belong (two companies from the left and right, not out of the centre) and leave when their point is made.

## Motion, polish and checking — Samuel, 2026-10-03

On the Apollo marker-2 notes: *"Stop using wierd animations, never use boucing animations, always use Neo anim where something animates in and out, your adjustment clips over UI visuals are animated janky and hard to follow, I need it smooth"*, *"Make use of design things that make it look good, shines, bevel, glow, things that make the visuals look premium"*, *"don't be using transforms when we have neo Anim"*, *"timing is important in the visuals"*, and *"make sure that you look at what you do, and ask, would Samuel correct this ... you can crosscheck videos we have finished in the past to know what has been approved"*.

- **Every element comes in and goes out with his Neo Anim** (slide + blur + fade, Expo ease). Never a Transform pop, never an overshoot or bounce. Out animations are part of the build, not optional.
- **Zooms and focus on UI are slow and eased:** a key only where a move starts or ends, holds in between, never a per-frame cursor follow. Highlight what he's talking about with a Brightness Contrast that darkens the rest.
- **No fast zooms on UI visuals** (Samuel, 2026-10-03, second red-marker pass: *"Don't do fast zooms on UI visuals, make sure everything looks clear and premium"*). A focus move takes about 18 frames, the zoom stays at or under about 1.3, and where several parts are close together the highlight moves while the zoom holds (or there is no zoom at all). `M6 red markers\focusgen6.py` in the Apollo job has these settings.
- **Premium = real effect nodes on every card:** Neo Glow on borders and rings, static NeoLightSweep, DropShadow, a moving shine once it lands. Real logos only (Claude's own mark, not a drawn spark).
- **"Glass background" = his Glass effect** (`My macros\Glass effect.setting`): the layers below blurred 0.4, Displace refraction, inside a rounded panel whose width opens on a key, two-tone title on its top edge. His reference: the OUR OWN PROCESS beat at 685–754 of the Apollo job.
- **Time each beat to the words** from the cue times. Things land on the word they show.
- **Before reporting, render the range and look at it as he would**: size, readability, overlap with him, empty space, elements touching edges.

## Show it in the tool, reveal it as he says it — Samuel, 2026-10-03 (Apollo red markers)

His 15 red marker notes on 2635–8285 asked for one thing over and over: *"Show them Giving it Context in Codex"*, *"Show an MD file showing this context written there"*, *"Show a real skill.md file with this details, highlight them"*, *"Show the GTM OS on Codex"*, *"Write this down also in the Notion page and highlight it"*, *"SHow this on screen, on a new Notion notes Demo, Highlight what is said in the page, and reveal them as he says them"*. In his message: *"I want more real visuals, screen recordings, showing things, highlight things when necessary with brightness contrast"*.

- When Alex names where something lives or happens (Codex, a markdown file, a SKILL.md, a Notion page, a prompt), the visual is that tool on screen, full frame, rebuilt to look like the real app, with the words he says appearing in it as he says them.
- Highlight each part as he mentions it: Brightness Contrast darkening the rest, with a slow eased zoom onto it, on a base clip above the demo.
- A list or document he walks through gets written into the same page over consecutive shots (the good-account Notion page carried 6289 → 6474 → 6875), so the viewer follows one page.
- Motion graphics he called bad were small, dark, sparse and off-centre. The redesigns that replaced them fill the frame, sit centred, use real logos (companies and tools) and mixed fills, and use his straight Arrowline when he asks for a straight arrow.
- A "visual of his team" is real team B-roll from the Frontal library, not a graphic.

## UI demos and screen recordings — Samuel, 2026-09-27

- *"All Demos, screen recording, screenshot UI type of visuals must be full screen, like how it will actually look when I am browsing through the app or software."* Never a windowed UI tilted on a background.
- Accurate visuals: zoom and focus on exactly what's being said. Darken what isn't the focus and highlight the thing spoken about. **No motion graphics and no text that isn't part of the UI.** Any motion graphic needs his approval one by one.
- *"The visuals focus and all that must be on an adjustment clip not on the clip itself so I can always adjust things."* Zoom, darken and highlight go in a Fusion comp on an **adjustment clip above** the recording, never in the recording clip's own comp.
- **On his screen recordings: highlight only, no zoom** (Samuel, 2026-09-27: *"For his screen recording, don't zoom in, just highlight"*). Darken everything but the thing being spoken about; the frame stays at its normal framing.
- **HTML UI mockups follow the same rule** (Samuel, 2026-09-27, on the prospect-list mockup: *"It must be a fullscreen visual, not with any background. Stop adding Motion graphic text to screen UI mockups like this"*). A mocked app or spreadsheet fills the 1920×1080 frame edge to edge, exactly as the software looks in use: no wallpaper, no floating window, no tilt, no drop-in, no camera push, no counter chips or labels. Any focus goes on an adjustment clip afterwards.
- **Real products get their real UI, never a rebuilt look-alike** (Samuel, 2026-09-27, on the M02 tool shots: *"they don't look like the actual real UI's I need real UI's with images, and the right Icons"*). Get it from **his own Chrome** (*"always use my browser so you don't need to login to things"*): capture the live page where he's signed in or the site is public. For apps he isn't signed into, use the product's real screenshots found on **Google Images** (*"Get UI screenshots from Google"*); prefer the vendor's own help-centre or product images, and skip any with arrows, callout boxes or marketing frames. HTML rebuilds are only for things that don't exist as a real product (like a made-up prospect sheet).
- **A "UI demo" is built from scratch, never cut from the client's own screen recording** (Samuel, 2026-10-02, after I used Alex's Tella for the Apollo demo: *"I said build your own UI Demo from scratch, you are busy using Alexes Demo. Don't do that execpt I ask for that"*). Rebuild the product's real UI as a full-screen HTML page, measured off a real screenshot, with the real logos and the right icons and my own scripted cursor, then render it to the exact marker length. Zoom and focus still go on an adjustment clip above it. The client's footage is used only when he asks for it.
- **Never base a visual on Alex's visuals unless Samuel names them** (Samuel, 2026-10-02, on the Codex-layout GTM OS demo: *"Generate a UI that shows the GTM OS, not a cursur page, stop copying from alex visuals except I mentioned, make it dark mode also"*). His Tella and screens are a source of facts (what a tool returned, which tools a run used), never of layout or look. A system with no product UI of its own, like the GTM OS (a repo run through an AI harness), gets an **original app UI that shows the system itself**: its parts, the run, the tools, the output. Not a chat window or a coding harness. Dark mode unless he says otherwise. Reference build: `Graphics\Visuals v3\GTM OS demo\gtm_os.html` in the Apollo job.
- The Editor does this unasked on A-roll stretches that talk about a UI (real footage of that UI, full frame) as well as on the screen-recording stretches. Things that need creative choice stay his.

## Effects are real nodes, never faked — Samuel, 2026-09-25

On *Taking a Step Back from Claude*, Claude built its own glows and "shadow boxes" instead of using the effect nodes, and Samuel had to correct it. His words: *"I have a plugin called Neo Glow, which is well what I use for glows. It didn't use that… instead of it to use shadows, the actual drop shadow node, it was creating a shadow box."* And: *"I always use actual nodes that can help me create those visuals so light sweep glow node actual drop shadow um reflection."*

- **Glow = NeoGlow.** Never a blurred copy or a soft coloured box standing in for a glow.
- **Shadow = the DropShadow node.** Never a dark offset rectangle behind a card.
- **Shine = NeoLightSweep Pro. Bevel = NeoBevel. Reflection = a real reflection** (the Renderer3D/Opacity/GaussianBlur rig in [[fusion-node-system]] §3, or a flipped, faded copy only where that is his method).
- An HTML preview may imitate these looks, but every effect in it must map one-to-one to the node that will make it in Fusion. The cut sheet names that node.
- **Not sure which node makes a look? Ask him.** Don't invent a workaround.

## Box builds — Samuel's corrections, 2026-09-26

From his review of the first Claude box on Route Rise #3 (he liked the design; these are how he builds it):

- **NeoLightSweep Pro is a static shine**, placed so the box looks shiny at its centre. It never animates. *"I don't use lightsweep to actually sweep shine, I just add it in the box to make the box have a shiny look at the center."*
- **A moving shine = a BrightnessContrast node masked by a slightly inclined RectangleMask**, swiped across the box as it finishes animating in, on top of the static light sweep.
- **Opacity animation uses his Opacity macro** (`My macros\Opacity.setting`, a BrightnessContrast called `Op` with a Gain control). *"I don't want you to ever do any opacity animation on the merge."* Never key Merge Blend.
- **No Underlay** on generated builds. Instead, **each box's node structure sits far from every other node group** (its own area of the flow).
- **Boxes are squares** when he says "box".
- **Dashed/dotted lines use his "Moving dashed line" setup** (`My macros\Moving dashed line.setting`): transparent Background → Paint with a PolylineStroke (CircleBrush 0.0111, Spacing driven by a Shake 1–2, Smoothness 25) along a polyline, masked by the same polyline as a PolylineMask border (0.0019, Solid off). Animate it on with the stroke's `WriteOnEnd`.
- **Hiding a reveal** (logo, name, anything to be revealed later): MosaicBlur (ResolveFX) on that content's own layer only.
- Keep only the text he asks for. No invented sub-lines ("BY ANTHROPIC" was cut).

### How he finished the four-box visual (Route Rise #3, Composition2) — study, 2026-09-26

Read from his final comp (parsed from a saved copy) and frames. Build this way next time:

- **Each family of elements merges onto its own transparent Background canvas**, then that canvas joins the main line. The four boxes chain onto one canvas (Merge7 → 8 → 9 → 10), the two pills onto another, his card onto a third. This makes it easy to see which is which, and each group can be moved or shined as one.
- **The background (grid/glow) stays separate from the content.** All the content (card + lines + boxes) goes through one Transform on a PolyPath (a slow move over frames 0–33), and only then merges onto the static background. It works like a camera move.
- **One shine across the whole row:** a single BrightnessContrast + inclined RectangleMask (width 0.022, height 0.81, angle −18) on the boxes' canvas, moved by a PolyPath across the full frame over frames 36–60. Not one shine per box.
- **NeoLightSweep Pro width is narrow, about 0.07** (the default 0.2 washes the box).
- **Connector lines have two points and are curved.** They all start from one point on the top of his card and fan out to each box. They're drawn on fast (about 6.5 frames). There are no right-angle paths.
- **Timing is quick:** each box moves in about 8 frames and the boxes are about 3.75 frames apart, so the whole row is in within about 20 frames.
- **The box drop shadows were removed**, since the box glow is enough. The drop shadow on his pills is small and tight (distance 0.008, blur 0.31).
- **Pills (chips):** RectangleMask (CornerRadius 0.34) → accent Background → GaussianBlur 0.4 → Merge masked by the fill, plus an Instance border in the lighter tint #FD9457, then NeoBevel → NeoLightSweep → DropShadow → **NeoAnim** (slide + blur in). The text is **NeoTextMotion** (Geist SemiBold). The title is NeoTextMotion Geist ExtraBold, with the number in the accent colour.
- **The layout tells the story of the segment:** title ("4 TOOLS") → the two questions the section answers → the four tools → Alex at the bottom, with every line coming out of him.

## Revision rules — Samuel, 2026-10-10 (61 markers on the B2B video)

He asked for each of these once and said to repeat a correction everywhere it applies (*"if I corrected one place and you think that correction might be needed in other places, make sure you repeat that correction"*). They hold for every job.

- **The hook gets full-screen visuals and concrete ones.** His words on the old pipeline card: *"very, very bad. I need something much more concrete"*. A small card beside Alex is not a hook visual; a full-frame scene of the real thing is (a pipeline dashboard with months, values and the flat line).
- **One recurring device, one design.** A device that returns (the 7 steps) is full screen, big boxes with the text on them, his colours, the same every time it comes back (*"always keep consistency around this type of visuals"*). Make it light: no reflections or glow on every card. A heavy one crashed his cache.
- **List reveals reuse the visual.** Item two shows the visual from item one and reveals the next item, and so on (*"what every visual you came up with in the last one, reuse here and reveal the next pill"*).
- **Step and chapter pills are all one size**, with a small dark fade behind them so they stand out.
- **Logos enter gently:** Neo Anim In about 25 f, a short offset, starting from opacity 0. Never from far below (*"that's why they look fast"*). Logo tiles show the real brand colours, never grey.
- **No fade-out on full-frame visuals** into A-roll: hard cut. No fade-in on an insert either (*"it looks like a glitch"*).
- **Captions over B-roll are the words animating in, no pill behind.**
- **Real footage beats AI B-roll.** Remove AI B-roll he flags; for a real action (a cold call) find real footage on YouTube.
- **Calls are shown as calls.** Wherever a sales call is mentioned, show the video-call screen (Meet: Alex + a blurred prospect) with the transcript or messages by the side, not a call-recording page.
- **Highlights:** light the whole message when the whole message matters; move the highlight to the list as soon as it's said; zoom in far enough to read; don't move a highlight away when it should just be held.
- **One timeline.** He caches the whole video before his review. Work in place on that timeline (only touched clips re-cache) instead of duplicating it. How: [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] (2026-10-10).

## His own fixes on the B2B final — study, 2026-10-13

What Samuel changed himself after the Editor handed the B2B video over (frame diff of the three finals; write-up and stills in the B2B job's `Docs\Samuel own changes study (2026-10-13)\`). Samuel, 2026-10-13: *"Anything I corrected in the last video or in the last previous videos, I should not repeat myself."*

- **Nothing sits still.** A-roll, B-roll and screens all get a slow push from the centre, about 6–12 % over 2–4 s (472–560: 1.00 → 1.06; 625–687: 1.03 → 1.12). The hook pushed in on the whole composite, card and A-roll together, to about 1.11 in under a second, then held.
- **Web pages and screen captures fill the frame**: scaled up, browser bars cropped away, still pushing (560–621: 1.07 → 1.10).
- **No source or citation line on a stat card.** He removed "6sense · 2025 Buyer Experience Report" from the 8-out-of-10 card.
- **Never blur what is being said or highlighted.** He removed a blur that sat on the very header and rows the highlight pointed at (2901–2998).
- **Hide a person with a pixel mosaic, not a soft blur** (the prospect's webcam face, 2901–2998).
- **Twin cards share one layout.** He moved one card's header to the same inset as its twin's (7737–8000).
- His 4K delivery came out 3.8 dB louder than the 1080p one; confirm the loudness target with him before the next final.

## Real posts, full-screen UI — Samuel, 2026-10-13 (LinkedIn Training brief)

- *"Every LinkedIn post reference that he's talking about, we need the real LinkedIn post ... you should not just make up things. Go to his LinkedIn page and find the actual post."* Made-up content only where no real reference exists, and then it must look exactly like the real UI, *"every detail down to the dot ... so that it feels like I just screen recorded the LinkedIn page."*
- *"Make sure you don't show chrome tabs or the windows UI in the visuals, it must all be fullscreen of the UI visuals."* Captures are the page viewport only.
- How the real captures are made (his logged-in Chrome, PrintWindow at device pixels, stitched scrolls): [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] → LinkedIn captures, 2026-10-13.

## Samuel, 2026-10-14 (LinkedIn intro review)

After the LinkedIn Training v1 intro: *"what you did on the intro was very bad … I don't expect to repeat myself"*. Per-beat notes are in [[04-Projects/routerise-linkedin-training|the job note]]; these hold for every job.

- **The intro is the most important part of the video.** *"Don't joke with the intros."* Well paced, smooth, premium; every visual must make sense to the viewer.
- **No fast zooms.** *"If it is too fast, it doesn't allow the viewer to digest the information."*
- **UI is zoomed in from its first frame.** The viewer must be able to read what is said and highlighted the moment the shot appears; never a whole page with side rails, ads or empty margins first.
- **Zooms and punch-ins are adjustment clips, never a Fusion comp.** *"Never use fusion comp for this zoom in effect, always use Adjustment clips like we have done in last videos"*; MagicZoom V3 Zoom & Hold on A-roll. **Use adjustment clips a lot: that is how he edits.** Anything that should be an adjustment clip (zooms, darkening, text over footage, focus over UI) is one. Route: the B2B kit (`kits\drt\convert.py`, `kits\inst\round_install.py`, `kits\drt\mz_plan.py`).
- **Node trees are compact.** Groups stay separate and organised (main line, collector columns), but close enough that he never has to scroll or drag to find a group. This replaces "each box's node structure sits far from every other node group" in Box builds below.
- **Text over darkened footage** is centred and big, no pill behind it, as in his finals.
- **Sound design always comes last**, after he has approved the visuals. Before his review, cache the whole timeline so he can watch it smoothly.

## Samuel, 2026-10-15 (LinkedIn v5 review, 106 markers)

*"There are some things that I have corrected in the past that I still saw you make mistakes on ... I don't want to have to repeat myself."* He asked for each of these somewhere and said to repeat them everywhere they apply. Working copy for builders: the job's `kits\REVISION 2 RULES.md`.

- **Animation:** *"Your animations throughout this video are not smooth enough, always jittery and too fast, not proper ease in and out, correct all through the video."* Smooth Bezier keys only, entrances 16–22 f with a long ease-out, exits 10–14 f, transitions ≥ 14 f.
- **Engagement on our own cards:** *"just use one Icon that fits the theme of the video"*, *"the engagement numbers are too big, make them smaller and put them in a small pill"*. One orange icon + a small count pill. Real and made-up LinkedIn UI keeps LinkedIn's reaction row (his choice, 2026-10-15).
- **Blur:** *"always use gausian blur and not normal blur"* = the ResolveFX Gaussian Blur node (what his own comps use). **Mosaic:** *"always increase the pixel freequency to the highest"* = PixelFrequency 200, the slider maximum.
- **Text never over Alex's face:** *"NEVER EVER PUT TEXT OVER HIS FACE, if at all put it under"*. Over A-roll the text sits low with the Down fade. **No orange or brown backdrop behind text:** *"Don't darken the video with a brown color, use brightness and contrast node to darken the whole video"*, *"I hate the orange backdrop"*, and *"the screen is too dark"*: darken neutrally and moderately.
- **LinkedIn posts read as posts:** *"Zoom out all linkedin posts, so we know it is a post, not too out that has too much of linkedin UI in it, but enough for us to know it is a post."* The whole card width and its header in frame. This replaces "no #F4F2EE margins wider than ~120 px" for posts.
- **Made-up posts get a profile picture** (*"Add a profile pic to the linkedin post so it doesn't look bare"*). One face per name across the video.
- **No generic boxes:** *"You are using the same generic box designs in the whole video"*, *"The boxes should look more like pills with better rounded corners and smaller a bit"*. Capsules, his Glass effect, medallions, real icons; shine subtle (*"The shine on the boxes is much, reduce it"*). Score/stat devices sit **on screen with Alex**, in a glass panel by his side.
- **Show, don't tell:** *"show me the actual comments ... you can add numbers on the screen above the visual but show something"*. A number gets the real UI under it.
- **Reveal with mosaic until reviewed:** in a list of items Alex goes through (the six posts), the titles not yet covered are MosaicBlurred.
- **Don't change what he didn't mark:** *"I liked the visual you used in the last version of the intro in this part, I didn't tell you to change it."* A fix round touches only marked beats and the rules above.
- **Intro laptop = his TSB laptop:** the whole 3D MacBook (lid and deck) in frame at a 3/4 angle, the UI playing on its screen, then a smooth push into the screen to full frame. A lid rising from the bottom edge reads as 2D.
- **Creative director notes count as his:** Route Rise's creative director (Shawn) asked that video-call scenes use Alex's real podcast footage and real podcast guests as prospects, with "name - position" tags and the name blurred. Samuel passed it on as a correction (2026-10-15).

## Samuel, 2026-10-16 (LinkedIn v6 review: laptop, mosaic, sound design)

*"I don't want to find myself repeating myself in future videos."* Rules from this review, for every video:

- **A 3D laptop looks like a real laptop:** the screen sits inside the lid with a black bezel and a thin silver rim. Never a screen wider than the lid, never a light band between screen and lid (*"The top has a large white gap, that's not how a laptop screen looks"*). How: [[07-Agents/video-editor/memory|Editor memory]], 2026-10-16.
- **List items hidden until he says them:** *"Mosaic blur the text of each of them till he mentions it, then reveal"* (the three FOR EACH POST pills). Same as the six posts rule above: in any list Alex walks through, each item's text is MosaicBlurred (PF 200) until its word.
- **Music = the last video's music, in its order:** *"use the music I used in the last video ... in the sequence. I used them for each major segment of the video."* One cue per major segment, in the order he used them last time.
- **Every animated item gets its own sound:** *"You miss a lot of movement ... if they are listing three things, you only put a sound effect for the first thing and not ... for the second and third thing that are animated in."* Every element that animates in gets a small hit, not just the first of a group.
- **Don't repeat the same sound:** *"I noticed you are repeating the same sound all throughout the video a lot."* Go through his beep folder and vary the beeps (*"I use beeps a lot"*) so they fit what's on screen.
- **Low levels:** beeps and whooshes *"as low as I normally used to do ... so that it's not distracting"*. Whooshes only where something moves.
- **Finished means render-ready:** *"once I'm watching the video, I will just need to render it after the music."*

## The intro is Samuel's — 2026-09-25

*"Every intro is Samuel."* Visual ideas for the intro still go on the cut sheet, as inspiration for him. **Nothing is placed on the timeline before the intro ends.** Visuals start on the first sentence after it.

**Changed 2026-10-08 for the B2B Marketing video:** Samuel asked the Editor to build the intro (the hook, frames 0–2494) in its own session: *"I want you to start the intro, but not in this session, in another session with the same intensity that you gave this one"*. The default for other jobs stays as above until he says otherwise. Brief: [[04-Projects/routerise-ai-b2b-marketing-intro|B2B intro]].

## When Resolve stops responding

- **If it crashed, reopen it yourself** (Samuel, 2026-10-03: *"When resolve crashes, open it back yourself, I am not always on my PC"*): `launch_resolve`, load the project and the timeline, then report what crashed and what was lost.
- **Tell Samuel immediately** (Samuel, 2026-09-27: *"Whenever Davinci is unresponsive, tell me immediately"*). The moment a Resolve script call times out, run one quick check (`Get-Process Resolve` → `Responding`). If it's `False`, stop and tell him in that same reply, with what the last call was doing and when the project was last saved. Don't sit through minutes of monitoring first.

## Animation and tidiness

- **Always use splines to smooth keyframes.** Timing must feel smooth, never linear.
- Each segment of a node tree must be **well separated and spaced**, and **labelled with an Underlay**.
- **Always keep the nodes tidy, well organised and grouped together** (Samuel, 2026-09-27, after the circle-comp pills: *"Nice arrangement, keep always doing this"*). The layout he approved: the new merges sit on his main line in one straight row between his last merge and `MediaOut1`. Each repeated element (each arrow, each pill) is one left-to-right row, with each merge's inputs stacked above it. The rows feed a single vertical collector column that runs straight up into its merge on the main line. After pasting, read his anchor nodes' positions (FlowView) and shift the whole new group so it lines up.
- **Never leave stray or dead nodes far from the tree.** Remove them, or gather them in one group next to the tree so he can delete them in one go.

## The visual toolkit for finishing an edit — stated 2026-09-18

The kinds of visual he uses, and the rule attached to each:

| Visual | Rule |
|--------|------|
| Website screenshots | Placed where needed |
| Fusion animations | For statements that need visualising |
| YouTube B-roll | Claude can't download it — **leave a marker saying what to use** |
| Steady zoom-ins on A-roll | Via adjustment clips |
| HTML mockups | To demonstrate things on screen; screen-recorded in OBS. He records it himself if Claude can't |
| Text on screen | **Only on important statements** |
| AI B-roll | Generated in Flow — Claude supplies the prompt plus a marker |

- **Icons come from his Assets folder.** Placeholders only if that isn't possible.
- **Visuals written in cut guides are often unrealistic** — follow the style already used in the edited part of the video instead.
- **Duplicate the timeline before any agent starts editing it.**
- **Prioritise speed and credit efficiency:** reuse and copy-paste existing comps, adjustment clips and nodes rather than rebuilding.
- **Visualise with illustrations first — "show, not tell."** He expects dense, varied visuals matching the density of his own edit. *Reusing templates with swapped text was explicitly rejected as useless.*

## Time and delivery rules — confirmed 2026-09-22

From the Accountability Engine's `body.md` (2026-08-26 to 2026-09-02), checked one by one with Samuel on 2026-09-22. Only what he confirmed is here.

- **Edit in 55-minute chunks with 5-minute breaks.** His numbers — the engine's were 50 and 10.
- **Plan the day the night before.** Tomorrow is planned by 9:30pm ([[daily-routine]]).
- **Every client day has a MUST-CLOSE and a STRETCH.** MUST-CLOSE: the day fails if it does not close. STRETCH: tomorrow's first item, pulled forward if today runs ahead.
- **Route Rise's 5-day cap.** The clock starts the day he opens the project. **Route Rise counts Sunday inside the five days; Samuel does not work Sunday, so when a Sunday falls inside, he has 4 working days.**
- **Revisions become top priority.** *"Revisions happen and can't be controlled, but they become top priority."*
- **Ship day starts like any other day** — no early start. The engine's 5:00am ship-day start is dropped.

The engine's evidence behind these: the job is about 30 hours of work, and the day that closed Client #2 in about eight hours was the one built into timed chunks the night before ([[patterns|P5]]).

Related: [[fusion-node-system]] · [[fusion-recipes]] · [[routerise-house-style]] · [[cut-sheets]]. Back to [[03-Areas/video-editing/video-editing|Video editing]]

## Samuel, 2026-10-21: video 2 style frames rejected (applies to every Alex video)

His words, ~02:40 WAT, after the plan v1 style frames of [[04-Projects/routerise-claude-10000-saas|video 2]]: *"So far, I don't like the visuals used, the visuals look cheap bro, we still need to keep the standard of how we did things in previous videos, just with the new branding, and it should look better, don't put anything directly behind his back it's bad, I hate p1 03, hk 08 sy-03, at hk 06, never put text on a screen record up, I don't do that, you did that on hk 08 too, hk 01, such text should be in the center for such visual, p3 o5 text up is bad there, every box used in his videos must have those border corners as the style, add that to lp 03, lp 11, show the fuel pouring on the fire, create a stylyzed cartoonish B-roll with google flow for such B-rolls of that, I don't like small short text on a full screen background, as you did in p2 -08, from this visual samples I am already seeing that this video would have me correct you a lot for visuals, this corrections I have given apply to the whole video, does this look like the best video editors type of creative video? does this look llike something my creative director would like, does it look like a video that belongs to a 10m followers channel? so better revise your visual plan before you put it on my timeline, using their brand guide doesn't mean you should do very medicocre looking visuals, use the style and work on it, I liked the brand guide examples you gave, but you made it worse in this video examples, we would continue this video when the weekly resets, but take note of everything I said so if I say resume in another session, you won't do this rubbish again"*

1. **The bar.** Keep the standard of the last four Route Rise videos (their constructs, layering, density, polish), only re-skinned in Frontal v2.3.1, and make it better. The brand never excuses a plain or cheap visual: *"use the style and work on it."* He liked the brand-study style frames (video 2 job, `Docs/Frontal brand study (Editor)/`); the plan v1 frames were worse than them. Test every visual with his three questions: the best video editors' kind of creative work? would his creative director like it? does it belong on a 10M-follower channel?
2. **Nothing directly behind Alex's back.** No text or graphics placed behind his head or body (MagicMask / cut-out layering). P1-03 ("Proof." rising behind his head) and HK-08 (Alex cut out in front of the ledger) are rejected. This replaces his 2026-10-20 brief line *"putting text behind his back sometimes when needed"*: after seeing it he said *"don't put anything directly behind his back it's bad"*. Any behind-Alex idea needs his yes before it is planned.
3. **No text at the top of a screen recording or web capture.** Text that goes with a capture sits in the centre, big, in its own visual (centred over the blurred, darkened page, or on its own ground), never as a label strip at the top. Wrong: HK-01 (the $1M), HK-06 (labels at the top of the two captures), HK-08, P3-05 (the numbers at the top of the careers pages).
4. **Every box has the corner-bracket border.** Every card, cell, panel and frame in Alex's videos carries the Frontal corner brackets as its style. Missing on LP-03 (the loop cells) and LP-11: add them there and everywhere else.
5. **Metaphors get a stylised, cartoonish Flow B-roll.** "Fuel you pour on the fire" (LP-11) must show fuel being poured on a fire, made in Google Flow in a stylised cartoon look, not an abstract glow. Same for every B-roll of that kind.
6. **No small, short text on a full-screen background.** P2-08 (sky band: small eyebrow, "6x", one small line on a full Blue-300 frame) is the example. A full-frame colour moment carries type big enough to own the frame, or isn't used.
7. **Rejected by name:** P1-03, HK-08, HK-06, SY-03 (he said he hates them), HK-01 and P3-05 (text placement). No SY-03 frame was on the sheets; SY-02 (the 3,000-square field) was. Treat both as rejected until he says which one he meant.
8. **Revise the plan before anything goes on his timeline.** These corrections apply to the whole video, not only the 14 frames. Re-render the revised hero frames and get his yes before any Fusion build or timeline work.

Notes and the revision plan: video 2's job folder, `Docs/Visual plan v1 (Editor)/SAMUEL NOTES 2026-10-21.md`. Back to [[03-Areas/video-editing/video-editing|Video editing]]

## Samuel, 2026-10-22: video 2 first 32 visuals reviewed (applies to every Alex video)

41 markers on *Visuals v1 (Editor)* (f0-3644) and a voice brief, ~15:40 WAT. Word for word: video 2's job folder, `Docs/Visual plan v2 (Editor)/SAMUEL NOTES 2026-10-22.md`. *"It doesn't look premium. It looks like AI did it, right? Because it's flat."*

1. **The new brand changes fonts, colours and square boxes only.** *"the only thing you are changing ... is the fonts will be changed, but does not mean that we are changing any other thing about the style of the way we do typography. The boxes would not be rounded, it would be square ... But does not mean that we are not going to put the shines that we used to put before."* His premium chain stays on every box: light sweep, moving shine, glow, glass, bevel; every box animates in; variety of box colours; solid icons used a lot ([[03-Areas/video-editing/edit-grammar/edit-grammar-shared-rules|shared rules]] S0.3-S0.4, re-coloured). Text keeps his NeoTextMotion shines.
2. **Text: white, bold, big for a phone.** No corner brackets on text (brackets on boxes only), no bracketed eyebrows, no dot separators, no filler words: show numbers. Season Serif has no bold, so bold text is Inter Bold/ExtraBold.
3. **Real UI and pages: zoom out for context, then 3 points of focus.** The page reads as what it is (post, job ad, article), then the area brightens, then the exact words get highlighted.
4. **His adjustment clip on every screen recording, page and B-roll** (animation in + vignette, S0.1). *"we do this in past videos, this video shouldn't change that"*.
5. **Charts are real charts:** money on the right axis, years along the bottom, labelled lines drawn on cue, the line turns red where it stalls.
6. **Negatives get red:** red tint, red vignette and desaturation on the word. Red vs green for failure vs success.
7. **Lower thirds centred, one line, big, the method on top.** Never to the side.
8. **A visual starts on the word that names it.** **"In this video": Alex's frame slides into a circle or slides up**, as in the last videos.
9. **Mobile first:** bigger boxes, bigger text, fewer words.

## Samuel, 2026-10-22: the creative director standard applies to every video

- *"This study must be used as standard in every video we do from hence"* — said after the summary of the creative director's six top-video breakdowns.
- From 2026-10-22, every video the Editor plans, builds or reviews, for any client, follows [[03-Areas/video-editing/creative-director/creative-director-standard|the creative director standard]]: triple attack, show don't tell, real proof first, never static, one focal point, darken behind, light to steer the eye, blur teases, a title on every chart, colour carries judgement, mobile first, reuse what works. Visual frequency: every 1 s in the hook, 2 s in the intro, 5-10 s in the body, 15 s at most.
- Order of authority (Samuel, 2026-10-22, second ruling): **Samuel's own corrections and markers overrule everything.** Below them: 1. this creative director standard, 2. the older house notes, 3. the client's brand kit, more subtle but present throughout. Samuel: *"The Creative directors standard stays top, older house notes second, client brand kit third(More subtle but is there overall) The only overruling of everything is my corrections and markers"*. (Corrected the same evening: the first version put the brand kit above the standard.)
- Every visual plan and every version is checked against the standard before Samuel sees it.
