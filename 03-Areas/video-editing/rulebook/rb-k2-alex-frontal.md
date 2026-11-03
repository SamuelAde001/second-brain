---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: K2
---

# K2 · Alex / Frontal (client overlay)

> **Read when:** any step of an Alex job that touches fonts, colours, boxes, logos, grounds or his footage. Every builder and reviewer on an Alex beat. **Client values:** this note. 🏢 here = from the Frontal brand kit v2.3.1. **Status:** draft, not yet approved by Samuel.

## Rules
### The brand and what it changes
- **K2.1** Every Alex video follows Frontal brand kit v2.3.1 from 2026-10-20. It is a must-follow. Finals before that date stay as they are. ✅ *"they are a must follow"* (2026-10-20)
- **K2.2** The brand re-skins his style, it does not replace it. Only three things come from the kit: fonts, colours and square boxes with corner brackets (and BGFRONTAL replaces the orange ground). Everything else follows the rest of this rulebook. ✅ *"The boxes would not be rounded, it would be square, right? But does not mean that we are not going to put the shines"* (2026-10-22) 🔁 (2026-10-20, 2026-10-22, 2026-11-03)
- **K2.3** What stays as house style: pacing and one-by-one reveals, the premium chain (light sweep, glow, glass, animate in: [[03-Areas/video-editing/rulebook/rb-c7-blurs-glows-shines|C7]]), solid icons used a lot, boxes varied in colour, white bold text in NeoTextMotion with its shines ([[03-Areas/video-editing/rulebook/rb-c4-typography|C4]]), red/green for meaning, arrows with heads, variety. ✅ (2026-10-22)
- **K2.4** Brand book wins over the kit's own README on motion: ease everywhere (CSS `ease`, cubic-bezier .25, .1, .25, 1), nothing bounces. Our timing and motion stay; only the look changes. ✅ *"For the contradiction, you need to ease everywhere, use what the brand book says"* (2026-10-20)
- **K2.5** The quality bar is his LinkedIn Training video (old orange look) rebuilt in this brand: the last four videos' standard, and better. ✅ *"using their brand guide doesn't mean you should do very medicocre looking visuals"* (2026-10-21)

### Fonts
- **K2.6** Inter only, Bold or ExtraBold, white. No other font in his videos: no Season Serif, no JetBrains Mono, no Geist. 🔁 (2) ✅ *"I want you to change all text in the video to be inter, I don't like that other font"* (2026-10-24)
- **K2.7** Season Serif is licensed to Frontal AI LLC only. Never use it outside Frontal work (not HighSignals, @SamuelSignals, Called to Edit or any other client), never commit the font file to the Brain or GitHub, never send it to anyone. 🏢 (kit licence, 2026-10-20)
- **K2.8** Fusion text size: Size = px × font height ÷ 1508 (Inter font height 1.210). ⚙️ (measured 2026-10-20)

### Colours
- **K2.9** No orange anywhere: `#FF5A1F`, BGORANGE and the July logo files are gone for Alex. ✅ 🏢 (2026-10-20)
- **K2.10** Tokens (hex → Fusion 0-1): ✅ 🏢 (2026-10-20)
  - Dark `#04060C` (0.0157, 0.0235, 0.0471): every ground; fades and darkening go to Dark, never brown.
  - White `#FFFFFF`: all text on dark.
  - Blue-300 `#A5CCFD` (0.6471, 0.8000, 0.9922): **the one accent**: the highlighted word, the active item, icons.
  - Blue-200 `#CFE2FE` (0.8118, 0.8863, 0.9961): highlighter on light screens (multiply), bracket stroke.
  - Blue-600 cobalt `#3B70D2` (0.2314, 0.4392, 0.8235): CTA band; "winners" boxes.
  - Blue-700 `#2C55A3`: blue text on white (Blue-300 is never text on white). Blue-800 navy `#1E3970`: case-study band. Blue-900 `#13254A`: quiet callouts. Gray-900 `#0D0F15`: panels. Connector grey `#8C8E99`: diagram lines. Glow-ambient `#687CDF` at 40 %.
  - Secondary text white 64 %. Dividers white 12 %. A progress rail uses white 12-20 % hairlines, not connector grey (reads too loud). ⚙️
- **K2.11** Green and red only where they carry meaning: green for money up or advice to follow, red for something not to do or a stall. Everything else in Frontal's blues and greys: winners cobalt with Blue-300 words, stuck grey with Gray-400 words. ✅ *"you used so so so much green and red in the video"* (2026-10-23)
- **K2.12** Bands (full-frame colour): sky (Blue-300 with Dark text) once per section for the key number; navy for a case study; cobalt for the CTA; tint for a quote. Never two coloured bands in a row; never Blue-300 text on sky or cobalt. 🏢 💡 (kit rule, never confirmed by him)

### Shape: square boxes and corner brackets
- **K2.13** Every box is square: CornerRadius 0, pills too. Round only for people's avatars. 🔁 (2026-09-26, 2026-10-21, 2026-10-28) ✅ *"The boxes would not be rounded, it would be square"* (2026-10-22)
- **K2.14** Every box, card, cell, panel and frame carries Frontal corner brackets: thin arms ~14-22 px, 2-3 px thick at 1080, stroke Blue-200 `#CFE2FE` (video 2 and 4 kits). 🔁 (2) ✅ *"every box used in his videos must have those border corners as the style"* (2026-10-21)
- **K2.15** Glass is square: white 6 % fill (Dark 72 % for text-heavy panels over busy footage), 20 px background blur, 1 px Blue-300 edge at 20 %, 1 px white 14 % top highlight. 🏢
- **K2.16** Ground for motion graphics is **BGFRONTAL** (in My macros beside BGORANGE): his BGORANGE structure recoloured to Dark, faint Blue-300 grid ~7-8 % faded at the edges, blue ambient light top and bottom. ✅ 🏢 (2026-10-20)

### Logos, companies, website
- **K2.17** Show company logos: Samuel settled it with Alex. Every Frontal client may be shown by logo, and made-up companies in demos are fine. ✅ *"Show the company logos. I have settled it with him."* (2026-10-07) · *"All frontal clients are cleared to show by logo"* (2026-10-20)
- **K2.18** The Frontal logo: always the full logo (pixel icon + wordmark) or the icon alone; white wordmark on dark, icon always Blue-300; clear space half its height; at least 80 px wide (icon 16 px); never on a sky band. Use only the kit's `02_Logos`: every Frontal logo file from before 2026-10-20 is the old orange one. 🏢 (2026-10-20)
- **K2.19** Put the Frontal logo only where it belongs (the brand beat, the CTA). ✅ *"don't add frntal there"* (marker, 2026-10-25)
- **K2.20** For any website or brand beat, capture frontal.so live (the new site). Never reuse an old capture. ✅ (marker, 2026-10-25)
- **K2.21** Make our own icons in the brand's style; no extra kit parts are needed. ✅ *"We don't need those extra kits"* (2026-10-20)

### Alex and his footage
- **K2.22** Footage: Sony XAVC `C07xx.MP4`, 3840×2160, 29.97 fps, camera audio dead or scratch (max −61 dB); DJI mic WAV with timecode 00:00:00:00, so no timecode sync; Tella split-layout screen recordings. He reads a teleprompter. Sync method: [[03-Areas/video-editing/rulebook/rb-a2-import-and-sync|A2]]. 🏢 (2026-09-14 to 2026-10-06)
- **K2.23** His face sits around x 880-1100, y 190-500 and his hands reach x 400-1250 low in frame (video 2): keep text and graphics clear of both. ⚙️ (2026-10-20)
- **K2.24** Build our own UIs; don't copy Alex's own demos or visuals (GTM OS, Apollo screens) unless Samuel names one. Rebuilt UIs are dark mode. ✅ *"stop copying from alex visuals except I mentioned, make it dark mode also"* (2026-10-02)
- **K2.25** Music goes on its own track so it mutes in one click, because Alex once asked for no music under the voice (2026-10-06); every later video shipped with music. ⚙️

### Kit files
- **K2.26** Master kit: `Routerise\Visual Assets\Frontal templates (Editor)\` (27 templates: CH, LI, LT, MG, OUT, IC). Each Alex job copies it into its own `Graphics\Frontal kit (Editor)\`; fixes go back to the master; approved comps are harvested into it at each end-of-job review. Map: [[03-Areas/video-editing/clients/frontal-template-library|Frontal template library]]. ✅ (2026-10-20) ⚙️
- **K2.27** The full kit (brand book, tokens, fonts) is in `Routerise\Visual Assets\Frontal Assets\Frontal-Brand-Kit-v2.3.1\`. Read it there for anything this note doesn't cover; never copy it into the Brain. When this rulebook is silent, use the kit's five principles: dark first lit in fluo blue; square and precise; show the real thing; quiet motion. 🏢

## Never
- **K2.28** Never put anything directly behind Alex's back (no MagicMask cut-out layering) without his yes. ❌ ✅ *"don't put anything directly behind his back it's bad"* (2026-10-21)
- **K2.29** Never corner brackets on text, no bracketed eyebrows, no dots between words. Brackets go on boxes only. ❌ 🔁 (2026-10-22, 2026-10-25) ✅ *"I don't like the bracktes you are putting on text, I would never do that"* (2026-10-25)
- **K2.30** Never orange, never rounded boxes or pills, never Geist or Season Serif on screen. ❌ ✅ (2026-10-20, 2026-10-24)
- **K2.31** Never recolour, stretch, rotate, outline or type out the Frontal logo in a font. ❌ 🏢
- **K2.32** Never carry this look onto another client (Frontal mechanics such as scripts and node structures may be reused; its looks may not). ❌ ✅ (2026-10-31)

## Pictures
- ![[_attachments/rulebook/k2-brand-study-liked.jpg|360]] ✅ The Frontal brand-study frames he liked (video 2, 2026-10-20/21: *"I liked the brand guide examples"*). Fonts there are since replaced by Inter (K2.6).
- ![[_attachments/rulebook/k2-plan-v1-rejected.jpg|360]] ❌ Video 2 plan v1 frames, rejected *"the visuals look cheap bro"* (2026-10-21): text over a grey page, text at the top of captures, Alex cut out in front of the ledger, "Proof." behind his head.

## Questions for Samuel
- **Q-K2.a** Glow on the Frontal logo. The kit says no glow or effect on the logo (2026-10-20); your old approved finals put SoftGlow 0.472 on the Frontal lockup, and you said *"I add glow"* about visuals (2026-10-22). → Options: (1) no glow on the logo itself, glow on boxes and visuals as usual; (2) soft glow on the logo too. My pick: (1).
- **Q-K2.b** Kit-only rules you never confirmed: the band rules (K2.12), diagrams as 1 px grey lines ending in a 6 px diamond with no curves (you allowed arrows with heads, 2026-10-22, and used curved connectors, 2026-09-26). → Options: (1) keep the bands as soft defaults, drop the diagram rule; (2) keep both; (3) drop both. My pick: (1).
- **Q-K2.c** The Frontal template library (27 templates, 2026-10-20) was never reviewed by you. → Options: (1) one contact sheet to approve or strike; (2) keep using it as is. My pick: (1).

## Sources
Replaces the video rules in [[03-Areas/video-editing/clients/frontal-brand-v2|Frontal brand v2.3.1]] (§1-§12 stay there as the kit's full reading) and draws on [[03-Areas/video-editing/clients/alex|Alex]], [[04-Projects/frontal-rebrand-video-kit|Frontal rebrand of the video kit]], [[03-Areas/video-editing/ways-of-working|ways of working]] (2026-10-20 to 2026-10-25), [[03-Areas/video-editing/samuel-review-card|Samuel's review card]], [[03-Areas/video-editing/sops/routerise-cut-workflow|Route Rise cut workflow]].

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
