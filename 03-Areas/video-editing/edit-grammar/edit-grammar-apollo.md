---
type: knowledge
area: video-editing
status: active
updated: 2026-10-08
source: local-folder
tags: [grammar, style, samuel, constructs]
---

> Study of Samuel's finished Apollo (I cancelled Apollo.io) timeline by the Editor, 2026-10-07, read from the timeline, its comps and a word-timed transcript. Copied verbatim from the B2B job's `Docs\Grammar - Samuel's last three timelines (2026-10-07).md`. Index: [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]]. Template comps named here (e.g. `apollo_V3_001190_1`) are in `Routerise\Visual Assets\Samuel templates (Editor)\comps from Apollo, 4 AI Tools, TSB\`.

# Apollo final: how Samuel shows a talking-head video

Source: the *I cancelled Apollo.io and built this Claude skill instead* final. It runs 550.2 s at 23.976 fps. Evidence comes from `rows.json` (199 items), all 10 contact sheets and 40 parsed comps. Every comp named below is in:
`C:\Users\repzy\AppData\Local\Temp\claude\C--Users-repzy-Desktop-My-Second-brain\61efb6af-ecc0-432f-8382-cd87767eae15\scratchpad\study\comps\`

**Units.** All three were checked against the stills.
- **Rectangle mask:** Width × 1920 px and Height × 1080 px. The card 0.4375×0.6759 renders 840×730 px. The pill 0.3928×0.0796 renders 754×86 px.
- **Ellipse mask with W = H:** a circle W × 1920 px across.
- **Text+ Size:** cap height is about Size × 850 px. Size 0.0277 measured 24 px caps. Size 0.0606 measured 48 px.
- **CornerRadius:** 1.0 is a full capsule.

---

## 1. Visual types: count, share, duration

Totals:
- **Visuals cover 84.8% of the runtime** (466.5 of 550.2 s).
- **104 visual beats**, with a median of 3.5 s between beat starts. 92 of the 104 start exactly on an A-roll cut.
- **A-roll:** 178 V1 clips, median 2.79 s.

| Type | n | Total | Share | Typical hold | Evidence |
|---|---|---|---|---|---|
| Voice-prompt demo: real screen recording, a dark prompt card typing his spoken words, a waveform pill, face-cam | 1 run (8 prompts + 8 result screens) | 117.1 s | 21.3% | prompt card 5.6–17 s, result glimpse 1.6–2.3 s, final result 15 s | 345.43–462.55 |
| Full-screen UI demo (Apollo, Codex, VS Code, Gmail, n8n-style workflow), always with zoom and spotlight | 14 | 85.7 s | 15.6% | median 5.2 s (2.1–13.9) | 7.38, 26.44, 39.71, 67.90, 100.64, 109.90, 115.49, 139.43, 149.94, 170.84, 214.55, 340.13, 462.55, 523.61 |
| Motion graphic on BGORANGE (full frame) | 10 | 76.7 s | 13.9% | median 5.4 s (4.0–19.8) | 1.17, 13.93, 22.40, 31.45, 129.63, 209.83, 281.87, 291.17, 476.31, 490.78 |
| UI demo + circular face-cam (V9 duplicate A-roll) | 3 runs | 68.7 s | 12.5% | 4.5–32.4 s runs, a new clip every 3.5–12 s | 250.13–281.87, 286.66–291.17, 304.22–336.63 |
| Team B-roll from other shoots (Alex with Renat, Alex with Kenny, office, Alex at laptop) | 6 | 25.6 s | 4.7% | 2.5–7.6 s, median 3.7 | 10.89, 44.34, 125.83, 220.51, 235.74, 336.63 |
| Glass panel or cards over the A-roll | 3 | 24.6 s | 4.5% | 2.9 / 6.3 / 15.4 s | 28.57, 49.63, 199.32 |
| YouTube / stock / AI video | 5 | 18.5 s | 3.4% | 1.75–7.1 s | 113.74 (AI video, file prefixed "Flow -"), 192.19 *Life at Palantir*, 238.20, 481.69, 485.99 |
| Website or article (screenshot, site capture, highlighter montage) | 4 | 16.9 s | 3.1% | 2.8–5.8 s | 183.43 montage, 189.27 Palantir site, 241.49 Frontal site, 487.99 Lob site |
| Big two-tone caption over footage | 4 (+3 inside the montage, +1 over B-roll) | 13.8 s | 2.5% | 1.2–4.8 s | 0.00 IN THIS VIDEO, 93.72 COMMON CONTEXT, 246.83 / 545.63 LINK IN THE DESCRIPTION, 10.89 over B-roll |
| Logo tiles over the A-roll | 1 | 7.0 s | 1.3% | 7 s | 163.83 CLAUDE / CODEX |
| Logo lockup over media | 2 | (counted in Website and Team B-roll) | | 3–7.5 s | 189.27 PALANTIR, 220.51 Frontal |
| Pills beside Alex | 1 (+1 over B-roll) | 5.0 s | 0.9% | 5 s | 79.00; 44.34 over B-roll |
| Rapid montage (one source per item said, caption on each) | 3 beats | 3.8 s | 0.7% | 0.92 / 1.25 / 1.67 s | 86.50–90.34 |
| AI stills (generated images) | 1 | 3.0 s | 0.6% | 3 s | 19.35 |
| Plain A-roll ("breaths") | 14 | 83.7 s | 15.2% | median 5.4 s (2.2–13.6) | see section 3 |

Notes on the types:
- The "full-screen real UI" clips are mostly the Editor's rendered replicas of the real tools, filed as `… (Editor).mov`. They carry real logos and real layouts.
- The voice-prompt demo is Alex's own screen recording, *Building a Custom GTM Operating System*.
- Visual types he does not use in Apollo:
  - Chapter title cards. The only structural graphic is the agenda at 31.45.
  - A "Box main" caption bar. It is built inside `apollo_V7_000261_1.comp` but not wired to the output; the caption sits on dimmed footage instead.

---

## 2. Triggers: which spoken line gets which visual

**Named company, tool or site → its real UI, website, logo or own footage. Never a text pill.**
- 7.38 "Apollo can give us a list of companies" → Apollo's *Find companies* UI, full screen.
- 26.44 "we still use Apollo through the API" → Apollo's API keys page.
- 100.64 "Apollo has its own research and enrichment features… connect it to AI tools" → Apollo UI. The spotlight hops Research → Enrichment → Claude (frames 12/36/80) while the zoom goes 1.21 → 1.28 → 1.0 → 1.22.
- 189.27 "The company Palantir actually invented the term" → Palantir website dimmed to Gain 0.41, white PALANTIR logo and wordmark centred. Then 192.19 "Palantir helped pioneer…" → Palantir's own YouTube footage.
- 199.32 "companies like ElevenLabs, Anthropic, OpenAI that hire engineers" → three real job-post cards with each company's logo. Each card lands on its name (InOffset 31 / 42 / 58 f).
- 163.83 "Claude Code… I'm gonna use Codex" → two logo tiles. CLAUDE dims to Gain 0.55 / Saturation 0 at f 72–79 when Codex is named.
- 125.83 → 129.63 "Kenny has been building our GTM OS… external tools and data providers" → B-roll of Kenny and Alex, then the GTM OS ring with real Apollo, AI Ark, LeadMagic and LinkedIn logos.
- 241.49 "At Frontal, we build GTM systems" → Frontal website capture.
- 220.51 "That's where I want to take Frontal" → Frontal logo lands on the word over a down fade, then office B-roll.
- 487.99 "researched the same company again" → Lob website.

**Statistic or concrete numbers → the number shown inside real UI or a data card. Never a giant isolated number.**
- 39.71 "find 5,000 companies that match a few filters" → Apollo UI with a zoom onto the Total count (1.0 → 1.3 → 1.38).
- 49.63 "two companies with the same number of employees, same industry, same country" → two glass data cards (EMPLOYEES 101-200 / INDUSTRY SOFTWARE / COUNTRY UNITED STATES), one each side of Alex, held 15.35 s.
- 314.44 "the run rate on five signals" → the Notion Lob record showing Signals 5 / Contacts 6, with the spotlight on it.

**List said aloud → one element per item, each landing on its word.**
- 86.50 "in your calls, in your team's heads, in notes from previous campaigns" → 1-second montage: call-recording UI, team B-roll, campaign-notes doc. Each beat carries a huge two-tone caption (YOUR **CALLS**, YOUR **TEAM'S HEADS**, NOTES FROM **PREVIOUS CAMPAIGNS**).
- 31.45 "where Apollo falls short, what we've built around it, how you can build your own" → numbered agenda pills 1 / 2 / 3.
- 79.00 three questions → three stacked pills beside Alex. The pill being asked turns orange; the others dim (InOffset 1 / 33 / 69 f).
- 476.31 "what a company does, who we've spoken to, what they told us…" → numbered list 01–05. Only the current item is filled orange.
- 490.78 "sales… marketing… service delivery" → hub whose branches build one per name over 19.8 s.
- 291.17 "tools to read account signals, find contacts…" → GTM OS tree with four branch pills.
- 22.40 "decide who to contact and how to approach them" → CONTEXT card (CALLS / TEAM KNOWLEDGE / CAMPAIGN NOTES) → curved arrow → WHO TO CONTACT / HOW TO APPROACH THEM cards.

**Action being described → the action happening in the tool.**
- 250.13 "write down what a good account looks like" → Notion page typing that title, face-cam on.
- 256.34 "if you give the AI a vague definition" → Codex with a vague prompt and a poor result table.
- 262.22 "explain what you sell, who it's useful for, what makes a bad fit" → Notion page; the spotlight steps down section by section.
- 139.43 "a skill is a way to save those instructions" → VS Code SKILL.md; the spotlight steps through Information / Tools / Output.
- 345.43–462.55 spoken prompts → the prompt card types his exact words with a live waveform, then the tool's real answer.
- 462.55 "before sending it, I'm gonna review" → Gmail with three drafts and a line highlight.

**Anecdote about the team, a client or a call → people footage.**
- 10.89 "doesn't know what we have learned from working with our existing clients" → Alex-and-Renat strategy-session B-roll, dimmed with a red-multiply vignette, two-tone caption.
- 44.34 "my team still needs to figure out which one…" → same B-roll + two question pills.
- 336.63 "I want my team to be able to see what the recommendation is based on" → team B-roll.
- 481.69 "sales learning something on a call that marketing never sees" → YouTube sales-call footage. It desaturates to black and white over 15 f on "never sees" (`V3_011607`).

**Claim or opinion → a comparison graphic, a bottom caption, or plain A-roll.**
- 209.83 "two companies can buy the same software and still need very different things" → HubSpot → Anthropic (orange card) ≠ ElevenLabs (dark card), with chip lists under each.
- 281.87 "I wouldn't jump from 'you have a job opening' to 'your outbound isn't working'" → Lob job-post card → arrow → email card "Your **outbound isn't working**".
- 93.72 "learn how to generate that common context" → COMMON **CONTEXT** at the bottom over the A-roll, with a down fade.
- 510.59–523.61 and 532.07–545.63: the closing opinions get plain A-roll for 13 s each.

**Section start or call to action.**
- 0.00 "In this video…" → giant IN THIS **VIDEO** for 1.17 s. Then straight into the hub MG. The first 65 s are chained visuals with no plain A-roll.
- 235.74–250.13 mid-roll CTA → Alex B-roll → YouTube "day in the life" → Frontal site → LINK IN THE **DESCRIPTION**. Then "let's get into the build" switches the visual mode to UI with face-cam.
- 545.63 end CTA → LINK IN THE **DESCRIPTION** with an orange down-arrow.

---

## 3. Rhythm

- **Chaining.** Visuals run back to back: 1.17 → 7.38 → 10.89 → 13.93 → 19.35 → 22.40 → 26.44 → 28.57 → 31.45 → 39.71 → 44.34 → 49.63 → 64.98 is one continuous run. Every run ends on an A-roll cut. There is no plain A-roll gap under 2.17 s.
- **Beats per minute** (distinct visuals starting): 0:00 = 13, 1:00 = 10, 2:00 = 6, 3:00 = 9, 4:00 = 10, 5:00 = 15, 6:00 = 20, 7:00 = 15, 8:00 = 5, 9:00 = 1. The densest stretch is the voice-prompt demo; the sparsest is the closing opinion.
- **Holds.**
  - MGs about 5.4 s. A long build-up MG runs 13–20 s with progressive reveals and dimming.
  - UI demos 2–14 s.
  - B-roll 2.5–7.5 s.
  - Montage beats 0.9–1.7 s.
  - Captions 3–5 s, except the hook at 1.17 s.
- **Breaths.** 14 plain-A-roll gaps, median 5.4 s:
  - 64.98 (2.9), 72.95 (6.1), 84.04 (2.5), 90.34 (3.4), 98.47 (2.2), 104.73 (5.2), 120.25 (5.6), 134.68 (4.8), 177.89 (5.5), 205.66 (4.2), 228.06 (7.7), 469.09 (7.2), 510.59 (13.0), 532.07 (13.6).
  - About one every 40–60 s in the explanation sections; none during the build.
- **During plain A-roll.**
  - An empty *Adjustment Clip 2* spans exactly the gap on most of them: 64.98, 72.95, 84.04, 90.34–98.47, 104.73–113.74, 120.25, 205.66, 228.06, 469.09, 510.59. It is presumably his MagicZoom punch-in (house style section 6); the effect's parameters are not readable from the export.
  - 98.47, 134.68, 177.89 and 532.07 are bare cuts.
- **Inside UI demos the shot never sits still.**
  - Zoom from 1.0 to 1.18–1.45 over 14–24 f, starting 0–4 f in (or delayed to a word, f 30–96).
  - Spotlight fade-in over the same frames.
  - The spotlight re-targets every 30–90 f (1.3–3.8 s); each move takes 10 f.
  - With no zoom, a slow push of 1.0 → 1.04–1.09 runs across the whole clip.
- **Exits.**
  - MG elements carry NeoAnim Out (8–12 f, OutOffset about 2), or the whole comp fades out over its last 6–8 f. Examples: `V2_005031` f 103–109, `V2_011767` f 464–471, `V3_004779` f 142–150. They finish on the cut.
  - B-roll and UI media animate in only and cut out hard on the next cut.

---

## 4. Construct library (template comp → settings)

**Common building blocks:**
- **BGORANGE ground** (in every full-frame MG):
  - Background #110602.
  - ResolveFX Grid 20×12, Blend 0.0143.
  - #FF5A1F glow through two ellipses, W 1.034 (1985 px), SoftEdge 0.1008, centred at y −0.299 and y 1.254.
  - GaussianBlur H 1.0 / V 0.4, merged at 0.181.
- **NeoGlow** (identical everywhere): NGBC Gain 0.15, MasterBlur 1.5, Depth 4, Screen. It goes on orange borders and rings only, never on text.
- **NeoLightSweep Pro, static shine:**
  - Cards and pills: band Width 0.1142, Angle −40, SoftEdge 0.0551, BrightnessContrast Gain 1.18–1.72 / Intensity 0.18–0.40, Distance 0.0015 at −130°, Merge Blend 0.1.
  - Orbs, tiles and captions: Width 0.0472–0.2 with Gain 2.5 / Intensity 1.5 (caption text 2.575 / 1.575).
- **Moving shine** (one pass after landing): BrightnessContrast Gain 1.55 / Brightness 0.05, masked by a 54 px-wide soft bar (SoftEdge 0.012) whose Center travels across the element.
- **DropShadow:**
  - Pills: strength 0.5–0.55, angle 90, distance 0.008, blur 0.3.
  - Cards: 0.6, distance 0.012, blur 0.45.
  - Big cards: up to 0.62 / 0.014 / 0.5.
- **NeoBevel** (central orbs only, `V7_006981`, `V2_000028`): Displace Blend 0.15, LightPower 25, LightAngle 138.4, Spread 0.15.
- **Borders:** an Instance of the shape mask with BorderWidth.
  - Pills 0.0012–0.0016 (2.3–3.1 px).
  - Medallion and number rings 0.0021–0.0046 (4–9 px).
  - Orange #FF5A1F or #FD9457.
- **Two-tone text: NeoMotionText fuse.**
  - Preset 26, Geist.
  - Char1 range from about 0.33–0.55 to 1.0, coloured G 0.3529 / B 0.1216 (#FF5A1F).
  - Word scope, InLength 18–25 f per word, Delay 0.28 s, PosDistance 0.0464, no Out.
  - Built-in shadow: strength 0.496, distance 0.0038–0.0044, blur 3.31.
  - Built-in shine: intensity 0.335, width 0.0141, 2 shines at 0.19 and 0.38.
- **NeoAnim presets:**
  - **Media adjustment clip** (26×, e.g. `V3_000634`, `V4_000177`):
    - In only, InLength 20, Position + Blur, StartOffset 0.021 at −90° (rises 2% from below), StartBlur 5.5, no Out.
    - Plus a Vignette: black, multiply, Blend 0.835, size 1, softness 0.5.
  - **MG element:**
    - In 10–16 f (usually 12–14), Out 8–12 f (usually 9–10), Position + Blend + Blur, StartBlur 25.
    - Offset 0.02–0.04 for rows, 0.05–0.08 for cards, 0.10–0.12 for pills.
    - Direction follows the side: left elements −180°, right elements 0°, lower elements −90° (rise), arrows and ticks 90° (drop).
    - Stagger 3–4 f inside a group; word-synced InOffset for items that are spoken.
  - **Centre orb or title:** Size only, 25 f.
  - **Logo tiles:** Position, 25 f, offset 0.283 from below.
- **Active state:** dim the inactive elements to Gain 0.42–0.62 and Saturation 0–0.64 over 6–8 f. Used on pills, cards, tiles, branches and the ring.

**Constructs:**

1. **Hook title: IN THIS VIDEO** (`apollo_V2_000000_1.comp` + `V4_000000`)
   - NeoMotionText "IN THIS" Geist SemiBold 0.1606 at (0.233, 0.696) and "VIDEO" Geist Black 0.1606 at (0.224, 0.549), white, left third.
   - NeoHighlighter Pro orange box behind VIDEO, Lighten mode.
   - MagicMask (Better) on Alex.
   - The V4 adjustment clip blurs the A-roll in: GaussianBlur 0.4 → 0 over 6 f.
   - Lasts 27 f.

2. **Hub with medallion pills** (`V2_000028`, 148 f)
   - Title NeoMotionText ExtraBold 0.0696 at y 0.896, two-tone.
   - Centre orange orb 376 px with GTM OS in Geist Bold 0.0606.
   - Pills: 420×118 px capsules, grey glass fill #A59E9A at alpha 0.9, 2.3 px edge.
   - On each pill's left edge: a 140 px white medallion with a 9 px #FF5A1F ring + NeoGlow, holding the logo clipped to an 88 px circle.
   - Name in Geist Black 0.032 white; role in Geist Bold 0.024 #FD9457.
   - Curved PolylineMask connectors (BorderWidth 0.0029) draw on over 10 f, staggered 5 f.
   - Pill shadow 0.55 / 0.012 / 0.4. NeoBevel on the orb. Slow push 1.0 → 1.036.
   - Opening move: the live frame shrinks into a rounded card (W 1 → 0.34, H 1 → 0.58, CornerRadius 0 → 0.092 over 38 f).
   - MosaicBlur (PixelFrequency 200) pixelates the tool names and logos in this hook only. Logos are now allowed (Samuel, 2026-10-07), so leave it out.

3. **Rebuilt UI card + question pill** (`V2_000334`)
   - White card 840×730 px, CornerRadius 0.0986 (about 36 px radius), on BGORANGE.
   - Contents are real data: Apollo logo tile 64 px; company rows with 48 px logo tiles #EDEBE8 (CornerRadius 0.54).
   - Text sizes: name SemiBold 0.0227 #1D1D1F, domain Regular 0.0158 #8C8580, employee chip SemiBold 0.0168 in a 66×53 px #F0ECE8 chip, column headers SemiBold 0.0148 #A3998F, 3 px #EDEBE8-type dividers.
   - White curved arrow: PolylineMask 0.0016, WriteLength 0 → 1 over 11 f, head scales in over 3 f.
   - Orange pill "WHO'S A **GOOD FIT**?" NeoMotionText Bold 0.0477: pops 0.82 → 1.035 → 1.0 over 12 f, then idles with a hover (Center y + 0.0026·sin(t·0.2)).
   - White "?" badge, 74 px: 0 → 1.12 → 1.0 over 10 f.

4. **Info card → arrow → decision cards** (`V2_000537`)
   - White card 547×436 px, CornerRadius 0.18, 8 px orange border; title CONTEXT ExtraBold 0.0553 #FF5A1F.
   - Bullets Bold 0.0336 #1D1D1F in 451×70 px rows, with orange dots.
   - Right side: dark cards with WHO TO CONTACT ExtraBold 0.0474 white, avatar circles 128 / 95 px, an orange ✓ badge.
   - People dim with an opacity key (1 → 0.4 over 8 f) as the choice is made.
   - NeoAnim 12 f, offset 0.12. Sweep Gain 1.25–1.3.

5. **Glass panel over the A-roll** (`V2_000685`, his reference for the glass look)
   - Panel: Rectangle 816×568 px, CornerRadius 0.252, at (0.227, 0.601). Width opens 0 → 0.425 in 6 f.
   - Glass effect macro inside: GaussianBlur 0.4 + Displace (Offset −1, Refraction −2.62, LightPower 3, LightAngle 132.6, Spread 0.827). MagicMask on Alex.
   - Diagram is built full frame and scaled 0.658 into the panel:
     - Centre orb 340 px, #FFAA58 fill, folder icon.
     - Four capsules 276–360×92 px. Fills rotate grey #828288 / near-white #EEEEF9 / white, all with 3 px orange borders.
     - 64 px orange number circles 01–04.
     - Each capsule pops (Size 0.001 → 1 over 8 f, staggered 7 f).
   - Title "OUR OWN **PROCESS**" NeoMotionText Bold 0.0467, top-left (0.229, 0.894).

6. **Agenda strip** (`V2_000754`, 197 f)
   - Opens with the frame shrinking to a rounded card (CornerRadius 0 → 0.0858 over 7 f) that slides away.
   - Light-peach panel #FFD1B2 with NeoHalftone texture (dot 0.0048, angle 30).
   - Three orange capsules 1044×130 px, 2.7 px border.
   - Ghost numerals 1 / 2 / 3 ExtraBold 0.1629 white.
   - Text NeoMotionText Bold 0.0423, the second half orange.
   - NeoAnim 14 f, offset 0.12 from the right.

7. **Data cards each side of Alex** (`V3_001190`, 367 f)
   - Dark-glass card: #120905 at alpha 0.55, Displace refraction, 564 px wide, CornerRadius 0.125, 3 px border.
   - Name ExtraBold 0.0336.
   - Rows: label Bold 0.0197 #B8B2B0, value ExtraBold 0.0267 white, 64 px orange icon circles, 432×2 px separators.
   - Tags: orange 279–356×56 px capsules (ExtraBold 0.0217 white), or light capsules with #291208 text.
   - Rows stagger in: 10 f each, offset 0.03, about 1.1 s apart.
   - The card not being discussed dims to Gain 0.45 / Saturation 0.64 (f 172–180 and f 277–285).

8. **Question pills over B-roll / beside Alex** (`V5_001063`, `V3_001894`)
   - Capsules 754×86 px (614×76 beside Alex), stacked bottom-left.
   - Grey fill #5D5D63 / #86868C, or orange #FF5A1F when active. 1.5 px orange border + NeoGlow.
   - 72 px white medallion with a 4 px orange ring + NeoGlow; orange line icon (`circle-help__orange.png`, `message-square-text__orange.png`).
   - Text ExtraBold 0.0277 / 0.0222 white.
   - NeoAnim In 12 / Out 10, offset 0.10 from the left. Static sweep + moving shine. Shadow 0.55 / 0.008 / 0.3.

9. **Big two-tone caption over footage** (`V7_000261` over B-roll; `V4_002074` / `2096` / `2126` montage; `V5_002247` bottom)
   - Footage underneath dimmed: BrightnessContrast Gain 0.34 (0.42 in the montage).
   - Optional red-multiply vignette (`V6_000261`: Vignette colour R1 G0 B0, multiply).
   - Text NeoMotionText: Bold 0.0683 in two lines with line 2 orange; or Bold 0.1365 single words, centred, in the montage; or ExtraBold 0.085 at y 0.099 at the bottom.
   - **Down fade** for bottom captions: gradient black at alpha 0.622 → #1B0903, masked by a 2061 px-wide soft rectangle (SoftEdge 0.0583) centred at y −0.119. Fades in over 8 f, out over 7 f.

10. **UI focus + zoom adjustment clip** (`V8_002413`, `V6_003595`, `V6_003343`, `V3_012554`)
    - Built on *Fusion base 1080 transparent.mov*: MediaIn_Below → Transform_Zoom (KF 1.0 → 1.18–1.45 over 14–24 f).
    - Spotlight: BrightnessContrast Gain 0.40–0.42 / Saturation 0.5–0.55, masked by an inverted rounded rectangle (CornerRadius 0.12, SoftEdge 0.004) around the target. Blend fades 0 → 1 over 5–14 f.
    - Rectangle Width / Height / Center re-key every 1.3–3.8 s, 10 f per move.
    - Text highlights in docs: the spotlight rectangle is shrunk to a single line (H 0.03–0.12).

11. **Voice-prompt card** (`V4_008282`/`8556`/`8910`/`9097`/`9543`/`9896`/`10139`/`10784` + matching V5 text comps)
    - UI behind: GaussianBlur 0.4 + Gain 0.529.
    - Prompt card #212121, about 960×390 px measured, upper centre. Height opens 0 → 0.3664 in 10 f; CornerRadius 0.433.
    - Text Geist Bold 0.0264 white, left-aligned, typing word by word to the speech.
    - Waveform pill 669×320 px, CornerRadius 0.812, black, with a white outline (PizzaBlu Outline 0.0014).
    - 11 white 13 px capsule bars: Duplicate Copies 10, TimeOffset −1.33. A FairlightAnimator on the voice audio (Scale 0.846) drives them.
    - DropShadow 0.5 / 0.0202 / 0.55. NeoAnim Size 25 f in and 25 f out.

12. **Face-cam bubble during the build**
    - V9 duplicate of the A-roll (`C0787.MP4 2`) on 250.13–281.82, 286.66–291.12, 304.22–336.63, 345.43–462.55.
    - Circle about 400 px across, centre about (1670, 870) px, thin white ring, soft drop shadow. Alex faces into the frame.
    - Off during MG inserts, B-roll and Gmail full-screen shots.

13. **Logo tiles over the A-roll** (`V3_003928`)
    - Two 168 px grey-glass rounded squares (#8C8C91 / #717176, CornerRadius 0.476, 1.3 px border) with white marks (`claude_FFFFFF.png`, `openai_FFFFFF.png`).
    - Names NeoMotionText SemiBold 0.0476 below. Placed bottom centre, about x 672 / 1245 px.
    - Down fade. Sweep Width 0.2, Gain 2.5.
    - The tile not chosen goes grey (Saturation 0).

14. **Job or post cards row** (`V3_004779`)
    - Three white cards 580×168 px, CornerRadius 0.286, 1.3 px #D9D6D4 border, along the bottom over the A-roll with a down fade.
    - 80 px logo tile (CornerRadius 0.45, #DBD9D6 border).
    - Title Bold 0.0247 #1A1A1C; meta Medium 0.0217 #737070; orange Apply capsule 120×44 px, SemiBold 0.0207 white.
    - Shadow 0.6 / 0.012 / 0.45. NeoAnim 13 / 10 f, offset 0.06 from below. Each card lands on its spoken name.

15. **Logo lockup over media** (`V4_004538` PALANTIR; `V6_005287` Frontal)
    - Palantir: media dimmed to Gain 0.41; logo + wordmark ExtraBold 0.1364 white, centred; NeoAnim Position + Blend + Blur, offset 0.44 from below.
    - Frontal: `frontal-logo-on-dark.png` at y 0.098 with SoftGlow 0.472 over a down fade; NeoAnim offset 0.44, 25 f.

16. **Comparison MG** (`V2_005031`)
    - Top: white HubSpot pill 500×150 px with a 136 px orange-ring medallion; text ExtraBold 0.0612 #1D1D1F.
    - Two arrows draw down to two 650×250 px cards (CornerRadius 0.448): Anthropic in solid orange, ElevenLabs in dark glass. Logos in 164 px medallions; names ExtraBold 0.0513 white.
    - Orange ≠ badge, 114 px, between them.
    - Under each card: capsule chips 470×72 px, white with #1D1D1F text or outlined, ExtraBold 0.0276.
    - Whole comp fades out over its last 6 f.

17. **Card → arrow → email** (`V2_006758`)
    - Lob job card: white 660×360 px, CornerRadius 0.189. Lob logo tile 124 px; LinkedIn badge.
    - Title ExtraBold 0.0345; green meta #548C5C.
    - Orange Apply capsule 160×58 px; outlined Save capsule.
    - White arrow → Gmail "New message" card: dark header #29292B, subject ExtraBold 0.0326 with the second half orange, grey skeleton lines 330 / 560×12 px.
    - The job card dims to 0.5 / 0.35 when the email lands.

18. **Numbered list** (`V2_011420`)
    - Title NeoMotionText ExtraBold 0.058 at y 0.806.
    - Five 1000×110 px capsules. Fills: glass at alpha 0.94, or orange when current.
    - 92 px number circles 01–05, ExtraBold 0.0336 #FF5A1F on white. Labels ExtraBold 0.0415 white.
    - The orange fill fades off the previous item over 8 f as the next lands.

19. **Branch hub / tree** (`V2_011767` shared data layer; `V7_006981` GTM OS)
    - Centre ring 250 / 470 px; orange orb 420 px with NeoBevel.
    - Branch pills 680×128 px with 150 px icon medallions; ExtraBold 0.0395–0.0434.
    - Sub-chips 383–480×56 px, white with #1D1D1F text.
    - Each branch lights from Gain 0.5 / Saturation 0.35 to 1.0 when named, then settles at 0.62 while the next is explained. Everything returns to full at the end.

20. **Website-article montage** (`V5_004398` NeoHighlighter + `V4_004398`/`4441`/`4464`/`4489`/`4503`)
    - Five Fusion clips (0.6–1.8 s each) carry web screenshots on white.
    - One NeoHighlighter spans the whole run: highlight colour #FD9457 on the phrase "Forward Deployed Engineer"; the rest of the page blurred.
    - The cuts match the words "everywhere / social media / on X / LinkedIn / everyone is talking about it".

21. **AI stills reveal** (`V2_000464`)
    - Generated stills: *Two men pointing at monitor*, then *Remove people from scene*.
    - MagicMask; vignette size 0.5; push 1.0 → 1.089.
    - GTM OS orb 376 px + "GO-TO-MARKET OS" NeoMotionText Bold 0.0801 at y 0.796.

22. **CTA caption** (`V2_013082`, `V3_005918`)
    - "LINK IN THE **DESCRIPTION**" NeoMotionText ExtraBold 0.06 at (0.485, 0.065) over a down fade.
    - Orange-tinted `down-arrow.png` (Size 0.1094) at (0.768, 0.133) drops in from above: NeoAnim 10 / 8 f, angle 90, InOffset 63.

**Type scale and colour (Geist only).**

| Use | Weight | Size |
|---|---|---|
| Hook | SemiBold / Black | 0.16 |
| Montage words | Bold | 0.137 |
| Captions over footage | Bold | 0.068–0.085 |
| Section titles (top band, y 0.80–0.90) | ExtraBold | 0.058–0.070 |
| Card titles | ExtraBold | 0.043–0.055 |
| Pill labels | ExtraBold | 0.022–0.042 |
| UI-replica body | SemiBold / Medium / Regular | 0.015–0.025 |

- Smallest real text: 0.0148, about 13 px caps, used only inside the UI replicas.
- Text colours: white on dark; #1D1D1F / #1A1A1C on white cards; secondary #737070 / #8C8580; labels #A3998F / #B8B2B0.
- Accent: #FF5A1F, with tint #FD9457. Panels: #110602 ground, #212121 dark card.

---

## 5. Signature moves and taste

**What makes it premium:**
- Every MG sits on BGORANGE.
- Every card and pill gets the full chain: border Instance + NeoGlow, static NeoLightSweep, tight DropShadow, one moving shine pass, then NeoAnim with Blend + Blur.
- Real logos sit in white medallions with orange rings, or in rounded tiles.
- Two-tone NeoMotionText titles carry their own shadow and two thin shines.
- Glass (blur + refraction) is used for panels over Alex.
- **One orange focus at a time.** The element being spoken is orange or fully lit; the others drop to Gain about 0.5 and low saturation. This repeats in roughly 10 comps.

**What makes it dense:**
- 85% coverage, visuals chained to the cut, and elements landing on their exact words.
- MGs keep building for their whole hold (hub branches, list items, cards).
- UI demos keep moving: zoom plus a spotlight hopping every 1.5–3.5 s.
- The hook delivers 13 visuals in the first 60 s.

**Footage handling:**
- Every media clip gets a NeoAnim adjustment clip above it (20 f rise + blur, vignette at 0.835).
- Text on footage always sits on dimmed footage (Gain 0.34–0.42) or a down fade.
- A negative beat gets black and white or a red-multiply vignette.
- Vertical phone footage is centred with dark blurred sides.

**Replaced or never done, from the final and from 27 project comps that are not on the final timeline:**
- Icon-and-text MGs explaining actions or concepts were replaced, at the same timeline positions, with real UI, web or B-roll. Examples by start frame: 2511, 2769 and 3343 became VS Code / Codex demos; 4372 became the real-article montage; 4608 became Palantir's site + logo + YouTube footage; 5288 became B-roll + Frontal logo; 6472, 7539 and 7937 became Notion demos.
- No pills naming actions.
- No chapter cards.
- No 3D tilt or rotation.
- No out-animation on B-roll.
- No A-roll slivers or gaps under about 2 s.
- No visual under 0.9 s except montage beats.
- No moving background behind pills.
- No unblurred UI behind an overlay card.
- Overshoot is limited to tiny badge or pill pops (1.035–1.12 over 6 f); nothing bounces.

**Caveats:**
- Many Apollo comps carry the Editor's node names. This is Samuel's approved final built on those comps, not necessarily nodes he wrote.
- The "Box main" bar exists unwired in `V7_000261` and is not in Apollo's render.
- The zoom adjustment clips' parameters are not in the export.

The parsing helpers are in the study folder (`fparse.py`, `csum.py`, `dump.py`, `brief.py`, `apollo_types.py`). Parsed output of all 123 comps: `apollo_csum.jsonl`. This was file-only analysis; Resolve was not opened.

=====

Back to [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]] · [[03-Areas/video-editing/video-editing|Video editing]]
