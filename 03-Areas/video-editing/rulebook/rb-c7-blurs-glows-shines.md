---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: C7
---

# C7 · Blurs, glows, shines

> **Read when:** finishing any box, card, list, intro tease or screen recording, and when reviewing finish and blur (Editor, editor-builder, editor-worker). Node settings are in B3. **Client values:** glass and glow colours, in the client overlays: [[03-Areas/video-editing/clients/frontal-brand-v2|Frontal brand v2]] (K2), [[03-Areas/video-editing/clients/gamma|Gamma]] (K3). **Status:** draft, not yet approved by Samuel.

## Rules

### Shines: the latest ruling (2026-10-28, restated 2026-10-31)
> **History in one line:** 2026-09-26 static sheen on boxes + one moving shine per row → 2026-10-20 Frontal reading "no shine, no glow" → 2026-10-22 "shines stay under any brand" → 2026-10-24 "stop putting shines in total" → 2026-10-28 static sheen on every box, moving shine only when necessary → 2026-10-31 moving shine only on major occasions.

- **C7.1** Every box gets a static NeoLightSweep sheen for depth. It never moves. ✅ 🔁×2 *"all the boxes must have a light sweep ... to give them that depth"* (2026-10-28). Settings: B3.29.
- **C7.2** The moving shine is rare: only on a major moment, with a reason, done well. ✅ 🔁×3 *"sometimes on only major occasions, shine should come in"* (2026-10-31); *"only when necessary and do it well"* (2026-10-28)
- **C7.3** When it is used: one pass, on that box's turn, after it lands; one shine across a whole row, not one per box; it travels fully off the box. ✅ *"this shine is okay, but they never completely leave the box"* (2026-10-24); *"I used 1 shine accross the 4 tools"* (2026-09-26)
- **C7.4** Moving-shine build: BrightnessContrast Gain 1.55-1.9 (Brightness ~0.05) through a narrow, slightly inclined RectangleMask (W 0.022, Angle −18), swiped across in ~10 f. ✅ *"I use a brightness node with a rectangle mask slightly inclined to swipe through the box"* (2026-09-26) 🎬
- **C7.5** NeoTextMotion text keeps its built-in shine on white text; off on accent words. ✅ 🔁×2 (2026-10-25, 2026-10-29). Detail: B3.16.
- **C7.6** Sheen, glow and glass are part of his look under every client brand. A brand changes colours, fonts and box shape, not the finish. ✅ 🔁×2 *"I add things like shine. I add light sweep. I add glow. I use glass effects."* (2026-10-22)

### Glows, shadows, glass
- **C7.7** Glow is NeoGlow, on borders and rings, only where it means something. ✅ 🔁×3 *"always use Neo glow next time I ask for Glow"* (2026-09-26); "glow only where it means something" (2026-10-24)
- **C7.8** A hero element may carry DreamGlow; a logo lockup a SoftGlow ~0.47. 🎬
- **C7.9** Shadows come from the DropShadow node. ✅ (2026-09-25)
- **C7.10** Boxes are opaque or properly blurred glass; nothing behind reads as a second layer. Glass where it fits (his Glass effect macro, B3.36). ✅ (2026-10-24) 🎯

### Mosaic: blur that hides
- **C7.11** His hiding blur is MosaicBlur at PixelFrequency 200, on the hidden content's own layer only. ✅ 🔁×4 *"Anytime you use mosaic blur in the whole video, always increase the pixel freequency to the highest"* (2026-10-15)
- **C7.12** Items not yet said stay mosaic-blurred and reveal on their word: list items, intro points, posts 2-6 while he talks about post 1. ✅ 🔁×3 *"we must always make sure that we blur things until they are reviewed"* (2026-10-15); *"Blur all of them to be revealed later in the video"* (2026-10-25)
- **C7.13** Tease with blur: the promised answer, chapter names, steps, the prize and the "Coming up" preview, each revealed on its word. Blur the labels, keep the shapes visible. 🎯 (2026-10-22) ✅ *"4 of them, all blurred though"* (2026-09-27)
- **C7.14** On screen recordings, unblur part by part as he reads it. 🎯 (2026-10-22)
- **C7.15** Hide a person with a pixel mosaic, never a soft blur: faces of call participants, names on call screens. 🎬 (2026-10-13)
- **C7.16** Privacy: mosaic over typed emails, API keys and tokens in recordings. 🎬 ⚙️
- **C7.17** Real third-party logos and names are mosaic-blurred only for a planned reveal or when he asks. ✅ *"use mosaic blur to blur the Logo and the name of the tools as we want to keep the curiousity"* (2026-09-26)

### Gaussian: blur for depth
- **C7.18** Soft blur is the ResolveFX Gaussian Blur. ✅ *"always use gausian blur and not normal blur"* (2026-10-15)
- **C7.19** No UI reads sharp under an overlay card: dim and blur it (GaussianBlur 0.4 + Gain ~0.53). Glass panels refract and blur what's behind. 🎬
- **C7.20** Pages, recordings and B-roll enter with blur and a short slide through his media adjustment clip (B2). 🎬
- **C7.21** Keep blurs moderate. ✅ *"The blur is too mych"* (2026-10-25)

## Never
- **C7.22** Never blur what is being said or highlighted; demo and fake UI stays readable. 🎬 (2026-10-13)
- **C7.23** Never blur made-up names or companies; blur only what must stay hidden. ✅ 🔁×2 *"stop bluring things that we have made up"*, *"Stop blurring companies"* (2026-10-25)
- **C7.24** No moving shine without a reason, never two on one box, never one that stays on the box. ✅ 🔁 (≈30 shine markers on video 2) *"you put shined wrongly all throughout the video without any reason"* (2026-10-24)
- **C7.25** No shine on realistic UI, pages or screen recordings. ✅ *"Real looking UI, with the right background, no shine"* (2026-09-27); (2026-10-24)
- **C7.26** No faked glow (blurred copy, soft coloured box) and no dark offset "shadow box". ✅ *"it was creating a shadow box"* (2026-09-25)
- **C7.27** No glow for its own sake. ✅ *"shine not needed, and glow not needed"* (2026-10-24). To mark the right one, dim the rest (C6.6).
- **C7.28** No glowy graph dots: a small dot that rides the line exactly, every frame (C10). ✅ *"the circle on the graph line is too big and too glowy"* (2026-10-24)
- **C7.29** No NeoBevel (B3.43), no motion blur (C2). ✅ (2026-10-23, 2026-10-28)
- **C7.30** No Neo Reflection on white tables: it prints mirrored junk. ⚙️ (2026-10-08)

## Pictures
- ![[_attachments/rulebook/c7-linkedin-bar-boxes.jpg|360]] ✅ LinkedIn Training motion graphics (the bar for video 4): box finish to match (LinkedIn, approved final)
- (no picture yet: one good single moving shine leaving its box, next to video 2's double shine)

## Questions for Samuel
- **Q-C7.a** Which moments are "major occasions" for a moving shine? → Options: (1) the section's hero box or payoff number only, at most one per section (2) you mark them in the plan (3) never unless you ask. My pick: (1), flagged in the visual plan for your yes.
- **Q-C7.b** "Blur only what hides something" (Editor's reading of your 2026-10-25 markers) vs your Apollo final and the CD (2026-10-22), which blur the rest of a busy page or UI so the lit part stands out. → Options: (1) depth blur of the surround stays allowed; your 2026-10-25 markers were only about hiding made-up names (2) no blur except to hide. My pick: (1).

## Sources
Draws on [[03-Areas/video-editing/ways-of-working|Ways of working]], [[03-Areas/video-editing/samuel-review-card|Samuel's review card]], [[03-Areas/video-editing/creative-director/creative-director-standard|Creative director standard]], [[03-Areas/video-editing/edit-grammar/edit-grammar-shared-rules|Edit grammar shared rules]], [[04-Projects/routerise-claude-10000-saas|Video 2 job]], [[04-Projects/routerise-cold-email-goldrush|Video 4 job]], [[04-Projects/frontal-rebrand-video-kit|Frontal rebrand kit]].

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
