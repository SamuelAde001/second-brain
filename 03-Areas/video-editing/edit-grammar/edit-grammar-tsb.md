---
type: knowledge
area: video-editing
status: active
updated: 2026-10-08
source: local-folder
tags: [grammar, style, samuel, constructs]
---

> Study of Samuel's finished Taking a Step Back from Claude timeline by the Editor, 2026-10-07, read from the timeline, its comps and a word-timed transcript. Copied verbatim from the B2B job's `Docs\Grammar - Samuel's last three timelines (2026-10-07).md`. Index: [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]]. Template comps named here (e.g. `apollo_V3_001190_1`) are in `Routerise\Visual Assets\Samuel templates (Editor)\comps from Apollo, 4 AI Tools, TSB\`.

# How Samuel visualises a talking-head video: catalogue from the TSB final ("Taking a Step Back from Claude", Timeline 2)

**How I built this:**
- I read all 237 enabled timeline rows and all 13 contact sheets.
- I parsed all 167 comps and Samuel's macro `.setting` files with a script.
- I decoded the MagicZoom V3 settings from the compressed comps inside `tsb.drt`.
- I re-read `tsb.xml` to find **disabled** clips. These show exactly what Samuel switched off in Claude's part.

**Who built what:** Samuel built 0:00–3:06. Claude built 3:06–10:41 and Samuel then corrected it (Editor memory, `tsb-graphics-pipeline.md`). Samuel's 0:00–3:06 and his replacements after 3:06 are the standard to copy. Claude's "carrier" comps are on the timeline only because he kept them, and his creative director called them "very mediocre… shallow". Two comps inside his section, 0:08.8 and 0:09.9, use Claude-style `_D01` or `Pill…` node names, so Claude probably built or edited them.

**Units:**
- **Text px = Fusion `Size` × 1080.** I checked this against the render: STEVE JOBS at 0.1319 ≈ 143 px, the montage pill text at 0.0447 ≈ 48 px.
- **Rectangle px = `Width` × 1920 by `Height` × 1080.** The chapter bar at 0.5423 × 0.119 measured about 1050 × 120 px.
- Frames are at 23.976 fps.

**DaVinci Resolve:** the study used exported files only, so I did not launch Resolve. Its MCP reported "not running" during the study. Per Samuel's request, the next session that needs it should relaunch it if it crashed.

---

## 1. Visual types: count, share of the 10:41 runtime, typical duration

### What fills the frame
Shares are of the whole video, then of his own 0:00–3:06 section.

| Type | Items | Share (whole / his part) | Duration | Evidence |
|---|---|---|---|---|
| A-roll on screen (all kinds) | – | 44% / 43% | – | – |
| …plain A-roll, nothing over it | – | 23% / **14%** | breaths 1.2–8.5 s, median 3.5 s | see §3 |
| …A-roll with a card, pill, caption or chapter over it | – | 21% / **29%** | – | – |
| Full-screen motion graphic on BGORANGE, his | 5 | 4% / **15%** | 4–10 s, mean 5.6 | revenue chart 0:08.8, chapter overview 0:14, Claude→departments render 0:56, hub 1:58, "big boy Render" on V1 2:17 |
| Full-screen motion graphic, Claude's carrier comps | 22 | 21% / 0% | mean 6 s, up to 16 s | 3:47, 3:54, 5:50, 8:01–10:06; this is the weak part |
| Stock and third-party footage | 9 | 7% / **20%** | cutaways 1.7–5.1 s | startup-office B-roll 0:07 and 1:51; Jobs interview 0:46; iPhone keynote 5:22 |
| …source clips played full-screen with their own audio | 2 of the 9 | – | 9–19 s | Kevin O'Leary podcast 0:23.4–0:42.7 on V1; Jobs "focus means saying no" 2:41.7–2:51 on V1 |
| AI B-roll (generated video and photoreal stills) | 21 | 8% / 10% | 1.2–5.6 s, mean 2.9; montage shots 1.5 s | 1:06, 1:31, 2:10–2:17, 3:02–3:12, 5:29–5:48 |
| Real UI, full screen | 12 | 4% / 9% | 1.0–3.8 s, mean 2.3 | Claude Code recordings 1:22–1:31 (5 cuts), Artifacts video 0:59, GPT-6 Astra 2:56, n8n 5:02 |
| Real website or article screenshot with highlight or spotlight | 10 | 6% / 2% | 2.1–8.4 s, mean 3.8 | McKinsey 3:15–3:30, Frontal case page 3:45 and 3:50, results table 4:02, research paper 4:40, YouTube results page 1:38 |
| Claude's HTML rebuilds of real pages (`TSB_*.mp4`) | 8 | 4.5% / 0 | ~4 s | nature.com 4:18, tracker 6:54, clay.com and apollo.io sites 7:57 |

### What sits on top

| Type | Items | Duration | Evidence |
|---|---|---|---|
| Cards, pills or a window beside Alex over the A-roll | 24 (9 his) | his: 2–8 s, mean 4.6 | 0:00, 0:03, 0:09.9, 0:48, 1:02, 1:11, 2:27 |
| Two-tone caption: bottom fade, glass bar, statement bar, quote, montage pill | 17 | 1.5–4.0 s, mean 2.3 | 0:07, 0:59.8, 1:19.9, 1:43.5, 2:08, 2:10.6–2:17, 2:52 |
| Chapter lower-third | 4 | 2.3–4.5 s | 0:20, 6:21, 6:48, 7:47 |
| Highlighter or spotlight layers on screenshots | 7 layers on 5 shots | follows the words | 3:15, 3:21, 3:45, 3:50, 4:02, 4:40 |
| Speech bubble over B-roll | 1, held across 5 stills | 13.7 s | 5:35–5:48 |
| MagicZoom V3 adjustment clips | 95 | median 3.5 s | on **74% of all A-roll time**, 77% of plain A-roll, 38% of non-A-roll time |
| Neo Anim + Vignette adjustment clip above every piece of media | ~45 | same as the media below | see C1 |

---

## 2. Triggers: what he says → what he shows

- **A company, tool or product is named → its real logo, UI or website, never a stand-in.**
  - "Claude" at 0:00: 3D MacBook with the Claude UI, an orange CLAUDE title and a 90% pie with the Frontal logo.
  - 0:07: Claude-symbol tile and title over office B-roll.
  - "Claude Code with your data tools… find the emails… phone numbers… generate the copy… connect it to a sequencer like Clay or Instantly" at 1:22–1:31: one new cut of the real UI per clause (2.0 / 2.6 / 1.2 / 1.0 / 2.5 s), ending on the connectors menu with Apollo, Hunter, Gmail and Instantly toggles.
  - Other examples: GPT-6 Astra YouTube video at 2:56, n8n at 5:02, the frontal.so Design Pickle page with Screen Focus Emphasis at 7:49, clay.com and apollo.io pages at 7:57.
- **A person or source is named → their real footage plus their name, set big.**
  - Podcast "sandwich": the YouTube thumbnail card top-left over A-roll at 0:21.4 → the clip full screen at 0:23.4 → a PIP of the clip top-left with a two-tone name "Kevin **O'Leary**" at 0:42.7.
  - "Steve Jobs" at 0:46 and 2:37: real Jobs footage with a 143–153 px STEVE JOBS title placed **behind** him using MagicMask.
- **A statistic:**
  - His own number becomes an animated counter or chart: 90% pie counting 0→90 over frames 22–44 at 0:01; falling revenue chart at 0:08.8.
  - A statistic from a named report shows **the report itself**. At 3:21 Samuel switched off Claude's "8 OUT OF 10 COMPANIES" stat card and put in the real McKinsey paragraph with three marker strokes landing line by line.
- **A list said aloud → items revealed one per word, stacked:**
  - Agenda at 0:14: numbered pills revealed at frames 27, 79 and 116.
  - "understand the buyer / choose the right angle / judge the message" at 1:58: hub with pills.
  - "wrong people / offer / message" at 2:27: red pills sliding in from the left at frames 17, 75 and 117.
  - "pipeline and revenue" at 1:11: two pills at frames 62 and 97.
- **A list of actions → a montage of the action being done, one clip per clause, each with its clause in a glass pill.** 2:10.6–2:17.2: "sitting down with a small list / researching the people / writing something / paying attention to what comes back" at 1.5 / 1.5 / 1.5 / 2.1 s.
- **An action or analogy → show it happening, never label it.**
  - GPS analogy at 3:02–3:12: AI B-roll of a man typing an address, then driving with a map. Samuel switched off Claude's "YOU HAVE ARRIVED · NOWHERE" card for this.
  - "build an agent for each workflow" at 6:29: real n8n multi-agent video.
- **A client story → case card, then the real case page, highlighted as he speaks.** "one of our clients at Frontal" at 3:42 gets a CLIENT CASE STUDY card with the Frontal logo. Then at 3:45: "Their pipeline had been flat…", with the matching sentence highlighted on the real page.
- **A Jobs anecdote → photoreal AI stills of the scene, one per sentence**, plus a speech bubble carrying the question (5:29–5:48). This replaced Claude's "RETREAT / EXECS / OFFSITE" icon card.
- **A claim, opinion or key line → two-tone caption with the meaning words in the accent, red for negative, green for positive.**
  - 0:07 "the way that **companies use Claude**"
  - 1:00 "**without knowing why**…" (red)
  - 2:08 "we actually **stop practicing** the work **that doesn't scale**"
  - 1:43 statement bar
  - 2:52 quote on darkened A-roll: "something great" in green, "you have to say no" in red
- **A contrast or concept pair → colour-coded cards beside him**: green SIGNALS and red NOISE with live waveforms at 0:46–0:56. They come back at 1:02, 3:30 and 4:06, and the NOISE card grows to show its definition when he defines it.
- **A section start → section slam on the A-roll plus a chapter lower-third with a ghost numeral** (0:20, 6:21, 6:48, 7:47). The agenda overview comes first, at 0:14.
- **"Everyone has access to the same tools" → a real YouTube results page scrolled fast** with motion blur (1:38).

---

## 3. Rhythm

- **Density:** 124 distinct visual starts in 10:41, or 11.6 per minute. His own 0:00–3:06 runs at **13.5 per minute** against 10.8 after. Starts per minute, by minute: 14, 15, 12, 13, 13, 16, 11, 9, 9, 7, 5.
- **Chaining:** each visual runs until the next starts, or ends on an A-roll cut (211 of 237, per house-style §11b). Elements land on words *inside* a comp through NeoAnim or NeoTextMotion `InOffset`.
- **Breathing:**
  - His section has 10 plain A-roll gaps of 1.2–4.4 s, median about 2.9 s, roughly one every 19 s. Plain A-roll is only 14% of his section.
  - The whole video has 40 gaps, median 3.5 s, max 8.5 s.
  - The longest gaps (8.3 s at 4:31, 7.8 s at 5:12, 8.5 s at 9:26) are where he deleted Claude visuals and left the A-roll alone.
- **What plays during plain A-roll:** a MagicZoom V3 Zoom&Hold on a V2 adjustment clip, one per stretch, median 3.5 s (2–8 s). It sits under 77% of plain A-roll and under the cards and captions too.
- **The A-roll itself is jump-cut** about every 2–4 s (180 V1 clips in 10:41).
- **Track pattern:**
  - V1: A-roll, plus full-screen inserts such as the podcast, the Jobs clip and the big render.
  - V2: media, full-screen graphics and the zoom layer.
  - V3: the Neo Anim/Vignette adjustment clip for V2 media, or a card over the A-roll.
  - V4: a caption over V2/V3 media.
  - V5–V8: highlighters and stacked layers.

---

## 4. Construct library

All template comps are in:
`C:\Users\repzy\AppData\Local\Temp\claude\C--Users-repzy-Desktop-My-Second-brain\61efb6af-ecc0-432f-8382-cd87767eae15\scratchpad\study\comps\`

This is a temporary scratchpad folder, so copy the comps you need. The macros are in `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\My macros\` (Box main, Down fade, shine, Glass effect, Arrowline, Moving dashed line, BGORANGE, Numbers, Blinking in, Screen Focus Emphasis) and in `…\Neo folder\` (Neo Anim, Neo Glow, Neo Bevel, Neo Light Sweep Pro, Neo Reflection, Neo Highlighter Pro).

### Shared constants

**Neo Anim** (house values):
- Graphics: InLength 25 f, Angle −90 (slides up), StartBlur 25, start distance 0.44, motion blur on, In only.
- Pills from the side: Angle −180, distance 0.236.
- Pills that leave before a cut: Out on, OutLength 25.
- Media: InLength 20, distance 0.021, StartBlur 5.5.
- Position and scale each element with Neo Anim's GlobalXF Center and Size, not a Merge.

**NeoTextMotion** (the default text engine):
- Preset 26, InLength 25 f, Delay 0.28 s, PosDistance 0.0464, Out off.
- Shadow on: strength 0.50–0.62, distance 0.006.
- Glow 0.0378, or 0.1228 on giant titles.
- Shine 0.3346, width 0.0141.
- Two-tone is done with Char1 range plus Char1Color #FF5A1F, or #FF0000 / #00FF00.
- When he uses plain Text+, two-tone is done with `StyledTextCLS` (2401–2403 RGB over a character range).

**Fonts:**
- Geist **Black**: single-word card labels such as SIGNALS, NOISE and the CLAUDE title.
- **ExtraBold**: pill labels, numbers, quotes.
- **Bold**: captions, ghost numerals.
- **SemiBold**: chapter titles, glass and montage captions, big name titles.
- The one exception: the definition text inside the NOISE card is Lexend SemiBold 0.0305 (33 px).

**Effect values:**
- DropShadow on pills: strength 0.5, angle 37.5, distance 0.008, blur 0.31. Logo tile: 0.0126 / 0.213. Big window: 0.05 / 0.55.
- Neo Light Sweep Pro: Distance 0.0015, angle −130, band 0.1142 (pills) or 0.2 (cards) at −40°, soft 0.0551.
- Neo Bevel on pills: blend 0.15, power 6.05, angle 138.4, spread 0.15. Logo tile: 0.63 / 3.78 / 0.756. Circles: 0.15 / 28.72 / 1.394.
- Neo Glow: MasterBlur 1.5, gain 0.15, quality 3.

**Box main** (node group): RectangleMask CornerRadius 0.339 → fill Background (default #1B0903) → GaussianBlur 0.4 → border Instance RectangleMask (BorderWidth 0.0018, Solid 0) filled with the accent → Neo Bevel → Light Sweep → DropShadow → Neo Anim.

**Colours:**
- Fills: #1B0903 / #63220C (chapter) / #210B04 (statement bar) / #212121 (montage pills).
- Borders: #FF5A1F, or #FD9457 light orange.
- Signal: fill #006A00, border #00FF00, tint #ABFFB1.
- Noise: fill #480000 or #370000, border #FF0000, tint #FF9E9E.

### The constructs

**C1. Media entrance adjustment clip** · `tsb_V3_000074_1`, `tsb_V3_000169_1`
- On the track above every B-roll, UI clip or screenshot, the exact length of the media.
- Neo Anim In 20 f, Angle −90, StartBlur 5.5, distance 0.021.
- Then ResolveFX Vignette: oval, size 1, softness 0.5, multiply, Blend 0.835.
- MagicZoom often stacked on the same clip.

**C2. A-roll zoom (MagicZoom V3, on an Edit-page adjustment clip)**
- Settings decoded from the DRT on 59 clips:
  - Type 1 = Zoom&Hold.
  - Depth (AnimSize Scale) 0.40 on 47 clips, 0.25 on 5, 0.41 on 1.
  - The ramp lasts NumberIn1/2 = 2 s, then holds.
  - EaseIn Back, EaseOut Cubic.
  - Pivot (0.5, 0.684), which is his face.
  - Motion blur on (shutter 500, quality 4). The camera-shake block is present but off.
- One per plain stretch or card stretch. It also runs over B-roll.
- I read 0.40 as a 1.0→1.4× push. Frames 0:20.7 and 1:37.0 look consistent with that, but check one clip's controls in Resolve before relying on it.

**C3. Section slam** · `tsb_V5_000480_1`, `tsb_V4_000000_1`
- An adjustment clip about 1.2 s long at the first frame of a section.
- Transform Size goes 1.594 → 1.0 over 20 f, and GaussianBlur 0.4 → 0 over 6 f.
- Used at 0:00, 0:20, 6:21, 6:48 and 7:47.

**C4. Chapter lower-third** · `tsb_V3_000480_1` (also `tsb_V3_009145_1`, `009781`, `011197`)
- Box main bar: 0.5423 × 0.119 (1041 × 128 px), CornerRadius 0.339, fill #63220C, border #FD9457 at 0.0018.
- Neo Anim GlobalXF at (0.5, 0.074), so it sits bottom-centre.
- Ghost numeral: Text+ Geist Bold 0.1644 (178 px), gradient shading #FF5A1F → white, centred at x 0.265 so it overlaps the bar's left end.
- Title: NeoTextMotion Geist SemiBold 0.0678 (73 px) at x 0.325, left of centre.
- Effects: Bevel, Light Sweep, DropShadow 0.008 / 0.31. Neo Anim InLength 25, −90, blur 25, distance 0.44.
- Runs over the A-roll on top of C3 and C2.

**C5. Chapter overview** · `tsb_V2_000335_1` (0:14)
- BGORANGE ground.
- The A-roll becomes a card: Size 1 → 0.756 and CornerRadius 0 → 0.2 over 27 f, PizzaBlu Outline #FF5A1F at 0.0036, sliding up until only its bottom edge shows at the top of frame.
- A Moving dashed line runs down from it to three C4-style bars at y 0.65 / 0.45 / 0.25, revealed on the words (frames 22, 78, 115). Text is NeoTextMotion SemiBold 0.0442 (48 px).
- Whole-graphic push: Transform 1 → 1.052 across the clip.

**C6. Two-tone bottom caption** · over A-roll `tsb_V3_003069_1`, `tsb_V3_007141_1`; over B-roll `tsb_V4_001434_1`
- Down fade underneath: gradient black at alpha 0.62–0.65 → #212121, masked by a soft rectangle (W 1.073, H 0.619, soft 0.0583, centre y −0.119), which darkens the bottom ~20% of frame.
- Text: NeoTextMotion Geist Bold or SemiBold 0.043–0.073 (47–79 px), centred at y 0.063–0.114.
- Shine pass: BrightnessContrast gain 2.5–3.7 through a 0.026-wide rectangle at 53.6°, crossing the text once in 19–39 f.
- Lasts 1.7–3.2 s.

**C7. Statement bar** · `tsb_V3_002481_1` (1:43)
- Box main bar 0.8368 × 0.1503 (1607 × 162 px) at y 0.091, fill #210B04, border #FF5A1F, over C6's Down fade.
- Two lines of NeoTextMotion Geist Bold 0.0509 (55 px), two-tone, plus the shine.

**C8. Glass caption bar** · `tsb_V2_001915_1` (1:19.9)
- Glass effect: the A-roll under it is blurred 0.4 and refracted with Displace (strength −2.62, light 3.0 at 132.6°, spread 0.827) inside a rectangle with CornerRadius 0.252, W 0.669 × H 0.122, at y 0.074.
- A faint warm gradient is merged in at 0.134.
- Text: NeoTextMotion SemiBold 0.0851 (92 px), with "(GTM)" in orange.

**C9. Montage caption pill** · `tsb_V4_003130_1`, `003166`, `003203`, `003239` (2:10–2:17)
- Over each 1.5 s AI-B-roll cut: Box main pill 0.4788 × 0.104 (919 × 113 px), CornerRadius 0.339, fill #212121, border #FF5A1F, blur 0.4, Light Sweep.
- Centred at (0.5, 0.5), with a Down fade under it.
- Text+ Geist SemiBold 0.0447 (48 px), white plus a #FD9457 character range.
- Neo Anim 25 f, −90, distance 0.126.
- A new pill on every cut.

**C10. Logo tile plus title over B-roll** · `tsb_V4_000169_1`
- Rectangle 0.3335 × 0.5458, CornerRadius 0.221, filled with the brand colour (#D97757 for Claude), real logo PNG at size 0.514.
- Bevel 0.63 / 3.78 / 0.756, DropShadow 0.0126 / 0.213.
- Group scaled 0.657, then GlobalXF (0.5, 0.36) at size 0.756.
- Title: NeoTextMotion Bold 0.0606 at y 0.562, two-tone.
- Over Down-faded B-roll.

**C11. Signal / Noise cards** · `tsb_V3_001154_1`, `tsb_V3_001102_1`, `tsb_V2_001491_1`
- Box main card 0.2433 × 0.2513 (467 × 271 px), CornerRadius 0.339, green or red as above.
- Inside: a green-screen waveform stock clip keyed with DeltaKeyer (Transform 0.215–0.349 at y 0.54), and a label in Geist Black 0.0626 (68 px).
- Placed left and right of Alex with GlobalXF; MagicMask keeps him in front.
- When he defines the word, the card's height animates 0.2513 → 0.5007 and a Lexend line appears (frames 108–130).

**C12. Stacked pill list**
- **Red, from the left** · `tsb_V3_003533_1`: pills 0.4409 × 0.102, fill #370000, border #FF0000. GlobalXF x 0.168 (they bleed off the left edge) at y 0.7 / 0.5 / 0.3, size 0.839. Neo Anim −180, distance 0.236, Out 25 f. Text ExtraBold 0.0306 (33 px), white plus red.
- **Orange, with icon medallions** · `tsb_V3_001701_1`: pills 0.374 × 0.102 at the bottom (y 0.081, x 0.3 and 0.7), white circle medallion 0.0578 holding a flaticon PNG, header line ExtraBold 0.0378.

**C13. Hub with arrows** · `tsb_V2_002829_1` (1:58)
- On BGORANGE. An orange circle with a person icon at GlobalXF (0.267, 0.5), size 0.665, Bevel 28.72.
- White Arrowline curves (line width 0.0032 drawn on over 11 f, arrowhead scaling 0 → 0.062 in 3 f) lead to 3 Box main pills: 0.3401 × 0.1436, fill #C64418, border #FD9457, icon at left, Text+ Bold 0.0432 two-line, at x 0.755, y 0.75 / 0.5 / 0.25.
- Whole-graphic push 1 → 1.039.

**C14. Giant name behind the subject** · `tsb_V3_003766_1`, `tsb_V3_001102_1`
- NeoTextMotion SemiBold or Bold 0.13–0.14 (143–153 px), white, Glow 0.12, at the upper left.
- MagicMask (Better) on the person so they occlude the letters.

**C15. Quote on darkened footage** · `tsb_V5_004129_1` (2:52)
- BrightnessContrast gain 0.17 on the footage.
- Two centred lines of NeoTextMotion ExtraBold 0.0583 (63 px) at y 0.533 / 0.46: "**something great**" in green, "**you have to say no**" in red. The second line starts 37 f after the first.

**C16. 3D or tracked product in the A-roll** · intro `tsb_V2_000000_1`; hologram `tsb_V2_000074_1`
- **Intro:**
  - An FBX MacBook in Renderer3D spins in (Y-rotation −62 → 18 over 43 f), with the Claude UI on its screen as an image plane.
  - CLAUDE title: Geist Black 0.0701, #FF5A1F, shine.
  - 90% pie: ring length 0 → 0.9 over 22 f, Numbers counter, Frontal logo.
  - Neo Reflection, MagicMask on Alex.
- **Hologram (0:03.1):**
  - A screenshot in DVE 3D (rotation X 20°, Y 28.2°, Z −8.3°) floats above his laptop, planar-tracked to it, with MagicMask on his hand.
  - Entry: Blinking-in flicker every 2 f for 10 f, plus Neo Glitch (amount 0.354).
  - Neo Glow, a LumaKeyer screen-light merge, and a C6 caption at y 0.114.

**C17. Real article plus highlighter or spotlight**
- **Line marker** · `tsb_V5_004830_1`, `tsb_V6_004923_1`, `tsb_V7_004928_1`: Neo Highlighter Pro generator, one per line. Colour #FD9457, multiply, edge roughened by FastNoise → Displace (0.01), drop shadow 0.1 / 0.02 / 0.4. It wipes left → right as the words are spoken (3:21.5, 3:25.3, 3:25.5).
- **Spotlight** · `tsb_V4_004686_1`: the page is darkened (BC gain 0.39) outside a soft rectangle (0.27 × 0.106, soft 0.011) that fades in over 31 f, with a marker on the key phrase.
- The screenshot below gets C1 and C2.

**C18. Speech bubble on AI B-roll** · `tsb_V5_008031_1`
- Orange ellipse (#832D10 at alpha 0.835) with Grain and a FastNoise-driven Displace for an organic edge, plus Vignette.
- Text+ Geist Bold 0.0218 (24 px), lowercase, two lines.
- The same bubble is re-placed on each of the 5 stills.

**C19. Source-clip sandwich** (0:21–0:46)
- Thumbnail JPG card top-left with a white border on V4 → the clip on V1 → PIP plus name (`tsb_V6_001023_1`: NeoTextMotion Bold 0.0601, "O'Leary" in orange).

**C20. Results-page scroll** · `tsb_V2_002363_1`
- Full-page screenshot at size 0.859, path from y −0.367 to 0.134 over the clip, motion blur on.

**C21. Data card and C22. window flow** · `tsb_V2_000210_1`, `tsb_V2_000238_1`
- C21: dark card, card fill #1B0903, border 0.0018, CornerRadius 0.129, area gradient, count-up, card flash; title with red "HURTING THEM".
- C22: Mac-window card with traffic-light dots (0.0175 at #FF0000 / #FFFF00 / #00FF00), then LEADS → CALLS → REVENUE capsules (CornerRadius 1.0, 0.1938 × 0.0667) rising 0.47 → 0.5 three frames apart.
- Both carry Claude-style node names, so copy the layout but not the naming.

---

## 5. Signature moves, taste, and what he never does

### What makes his visuals look premium and dense
- **Layers stack:** zoomed A-roll + a card beside him + a caption + a slam or vignette, or B-roll + Vignette + a slide-in + a caption + a push.
- **Every element is a real effect node:** Bevel, Light Sweep, DropShadow, Glow, Reflection, MagicMask, planar tracking, 3D. Nothing is faked.
- **Something always moves:** a whole-graphic push of 1 → 1.04–1.05, a shine crossing text once, the zoom holding at depth.
- **Big type:** names at 143–153 px, chapter numerals at 178 px, single-word labels in Geist Black. Cards are 467–1607 px wide and sit beside or around him, never parked in a corner.
- **Colour carries meaning:** orange is the brand, green means good or signal, red means bad or noise. The accent goes only on the words that carry the meaning.
- **The real thing first:** logos, real UI, real pages with highlights, real people, AI B-roll of the action. The only abstract graphics are his agenda, hub and pills, and those carry nouns or lists only.

### What he never does
These come straight from the 32 Claude items he switched off.

- **Metaphor or stat cards where a real thing exists:**
  - The GPS "YOU HAVE ARRIVED" card (3:06) became AI driving B-roll.
  - "8 OUT OF 10" (3:21) became the McKinsey article with highlights.
  - Airops HTML mock-ups 1 and 3 (3:45, 4:03) became real screenshots with highlights.
  - Retreat, offsite and whiteboard cards (5:28–5:48) became photoreal scene stills with a bubble.
  - "FUEL ON THE FIRE" (7:42) and "CHASE EVERY NEW OPPORTUNITY" (9:25) became plain A-roll.
- **Full-screen chapter cards** (6:21, 6:47, 7:47): replaced by his C4 lower-third over the A-roll.
- **Text overlays that only repeat the action on screen:**
  - "40 EMAILS… SENT BY HAND" over the typing B-roll
  - "USE AI FOR RESEARCH OR A DRAFT" over the Claude video
  - "THEN BUILD THE WORKFLOW"
  - "SALES TEAM · SIGNAL · OBVIOUS"
  - "NOISE CUT IT / SIGNAL FOCUS HERE"
  - "EVEN BIG COMPANIES SUFFERING TOO"
  - "66%"
  - All removed.
- **Generic stock that doesn't show the point:** the YC-startup cutaways at 5:33 and 8:51, the job-post mock-up and the LIVE discovery-call clip were removed.
- **Also never:**
  - transitions
  - out-animations on things that end on a cut
  - paragraphs of text
  - text under 20 px
  - a visual stopping short of the next one or of a cut

**Working files** (scratchpad): `tsb_summ.txt` (every comp's settings), `tsb_cond.txt` (condensed per visual), `tsb_mz.json` (MagicZoom per clip), `tsb_drt_clips.json`, `cover.py` (the coverage and gap maths), `fparse.py`, `summ.py`, `dumpcomp.py`.

Back to [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]] · [[03-Areas/video-editing/video-editing|Video editing]]
