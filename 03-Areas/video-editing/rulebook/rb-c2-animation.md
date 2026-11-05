---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: C2
---

# C2 · Motion graphic styles and animations

> **Read when:** building or reviewing any beat that moves (every motion graphic, text, logo, card, line, transition), and on the easing pass after a revision round. **Client values:** easing curve and any brand motion rules in [[03-Areas/video-editing/rulebook/rb-k2-alex-frontal|K2 Alex / Frontal]] and [[03-Areas/video-editing/rulebook/rb-k3-gamma|K3 Gamma]]. **Status:** draft, not yet approved by Samuel.

## Rules

### Speed and smoothness (his most repeated correction)
- **C2.1** Slow and smooth beats fast. Nothing the viewer has to chase; they must follow and digest every move. 🔁 (~35 markers on four videos + 5 messages, 2026-09-27 to 2026-10-24) ✅ *"Your animations throughout this video are not smooth enough, always jittery and too fast, not proper ease in and out"* (2026-10-15)
- **C2.2** Smooth Bezier keys with a proper ease in and out on every move. Never linear starts, never jitter. 🔁 ✅ (2026-10-15)
- **C2.3** Entrances 16-22 f with a long ease-out for main elements; 8-12 f for small parts inside a group, staggered 3-6 f (Q-C2.a, 2026-11-05). Exits 10-14 f (Q-C2.b). Transitions 14 f or more, starting at least 12 f after a hard cut. ✅ ⚙️ · ✏ 2026-11-05
- **C2.4** Animate with NeoAnim (slide + blur + fade, Expo ease), not a hand-keyed Transform, wherever NeoAnim can do it. ✅ (2026-10-15)
- **C2.5** One thing moves at a time. ✅ (2026-10-24)
- **C2.6** Adjustment-clip moves over UI, pages and screen recordings are smooth and easy to follow, never janky. ✅ *"your adjustment clips over UI visuals are animated janky and hard to follow, I need it smooth"* (2026-10-03)
- **C2.7** After a revision round, run an easing pass over every comp before the render (`ease_pass.py`). ⚙️ (2026-10-16)

### One by one, on its word
- **C2.8** Every element in every motion graphic animates in on its own, one at a time, on the word that names it. Nothing lands all at once; no box sits empty waiting for its content. 🔁 (~12 markers + 2 messages) ✅ *"every element must come in one by one. So remember the corrections"* (2026-10-28)
- **C2.9** Lists, logos and companies: each item moves in smoothly, but the items follow each other fast, 3-6 f apart. ✅ *"All companies should come in one by one fast, not all at once"* (2026-10-25) 🎬
- **C2.10** Inside a card: the container lands first (NeoAnim ~16 f), then each part in sequence ~3-6 f apart (text lines rise and fade), then one shine once it has landed. Never one reveal for the whole card. 🎬 ⚙️
- **C2.11** People icons and repeated small items each get their own delay. ✅ (2026-10-15)
- **C2.12** A spoken list is shown as a list, its items appearing as they are said. ✅ (2026-10-31)
- **C2.13** A UI that fills up fills whole rows, not cell by cell (~0.3 s a row, gaps tightening 0.22 → 0.10 s), and fills every visible row by the end. ✅ *"Make it fill up row by row, not cell by cell, it feels too fast"* (2026-09-27)
- **C2.14** Start the reveal at the start of its beat: cards and graphs show from the beginning, not halfway through. 🔁 2 ✅ *"Reveal the cards from the beginning"* (2026-10-08, 2026-10-24)

### Text motion
- **C2.15** Main text animates word by word with NeoMotionText, each word rising from below (PosDir 0 = Up, Scope 1 = word). Never a whole sentence at once, never from the left unless the beat needs it. 🔁 9 ✅ *"it's always word by word with neotext motion, why are you forgetting"* (2026-10-25)
- **C2.16** Typing is character by character, never word by word. ✅ (2026-10-24)
- **C2.17** A prompt or dictation overlay writes on in sync with his speech; its box opens first (height 0 → full over ~10 f). 🎬 (AI4, Apollo)

### Lines, arrows, graphs
- **C2.18** Line charts grow at one constant, gradual rate while he speaks, start to end; line draws are linear. 🔁 3 ✅ *"let it be a constant growth"* (2026-10-24)
- **C2.19** Arrows write on (~11 f) and the arrowhead scales in after (~3 f); curved connectors draw on over ~10 f, staggered ~5 f; a dashed line shows its first dot one frame before the draw. 🎬 ⚙️
- **C2.20** Graphics tell the story by changing state in place (FLOPS → TAKES OFF, a losing column dims), one change at a time (~18 f), not by swapping layouts. 🎬 (LinkedIn, 2026-10-16)

### Directions and devices
- **C2.21** Elements enter from where they belong: two companies from left and right, not the centre. ✅ *"let them animate in from left and right side"* (2026-10-02)
- **C2.22** Logos enter gently: NeoAnim In ~25 f, short offset, from opacity 0, never from far below. 🔁 (10 places, B2B) ✅ *"that's why they look fast"* (2026-10-10)
- **C2.23** A notification over A-roll (Dynamic Island style) rises from the bottom. A progress indicator is a bar that fills, not dots. ✅ (2026-09-30)
- **C2.24** On "In this video", Alex's frame slides into a circle or slides up, as in his past videos (20 f or more, long ease, at least 12 f after a cut). ✅ (2026-10-25) Detail: C13.
- **C2.25** A box that changes keeps its place: change its colour and swap its logo. ✅ (2026-10-25)
- **C2.26** Put the motion on the main content, not the background. Backgrounds may drift gently so the frame never feels static. ✅ *"too much of the animation on the blue background and not enough on the main screen"* (2026-10-31); ✅ *"too much statics in this video"* (2026-10-25). See Q-C2.c.
- **C2.27** Hide what hasn't been said yet with MosaicBlur and lift it on the word (Blend 1 → 0 over 8 f, that layer only). 🎬 Detail: C7.
- **C2.28** A shine never shows before its element has animated in. ✅ (2026-10-14) Detail: C7.

### Exits
- **C2.29** Elements over A-roll animate out (NeoAnim Out 10-14 f) or fade out when their point is made; they never just vanish. 🔁 2 ✅ *"Every visual that animates on screen should animate out"* (2026-10-03)
- **C2.30** Full-frame visuals, B-roll and UI media cut hard into the A-roll: no fade-out, no out-animation, and no fade-in on inserts. 🔁 (7 markers) ✅ *"it looks like a glitch"* (2026-10-10) 🎬
- **C2.31** A whole comp may instead fade over its last 6-8 f, finishing on the cut. 🎬 (Apollo)
- **C2.32** His markers decide per place: "animate out", "fade out" or "don't animate out here" overrule C2.29-C2.31. ✅ (2026-10-15, 2026-10-24)

### Transitions
- **C2.33** Transitions are gentle, slow directional pushes or slides; direction follows the meaning (moving on = right). No fast fly-off stacked on a jump cut. 🎯 *"that cut was way too agresive"* (2026-10-26)
- **C2.34** Fades of 3-12 f only on graphics, never on the A-roll. 🎬

### When he asks for static
- **C2.35** If he asks for something static, add no motion at all. ✅ *"Don't animate them in, I don't want any animation"* (2026-10-01)
- **C2.36** Animated graphics play once and hold their last frame; no loops unless the client overlay allows a slow pulse. ✅ (2026-10-20) Detail: K2.

### Under a new brand or client
- **C2.37** A rebrand changes the look, never our motion: keep the pacing, timing, staggers and one-by-one reveals. A brand kit's web timings (140-200 ms) don't apply. ✅ *"keep our current motion and change only the look"* (2026-10-20)
- **C2.38** Use the client's easing curve where its brand book sets one. ✅ *"you need to ease everywhere, use what the brand book says"* (2026-10-20) Values: K2.
- **C2.39** Make the motion beautiful and varied: never the same animation twice in a video, never a direct replica of another video's animations. 🔁 2 ✅ *"I want the motion design to be beautiful."* (2026-10-20); ✅ *"It must not be replica"* (2026-10-31) 🏢

## Never
- **C2.40** Bouncing, overshoot, scale pops or settle-wobbles, on any element, for any client. 🔁 3 ✅ *"Stop using wierd animations, never use boucing animations"* (2026-10-03, again 2026-10-15 and 2026-11-01) ❌
- **C2.41** Motion blur on NeoAnim or Transform. The soft entrance blur (StartBlur) stays. ✅ *"I don't want you to use motion blur because that makes it very hard to do"* (2026-10-28) ❌ His own intro adjustment clip keeps its motion blur as he made it.
- **C2.42** 3D tilt or rotation on cards. 🔁 ✅ *"I don't like the rotation"* (2026-09-30) ❌
- **C2.43** Anything moving in the background behind a pill. ✅ *"don't use that background wave"* (2026-09-30) ❌
- **C2.44** A red cancel or strike line through anything. Turn it grey or red instead. ✅ *"NEVER EVER EVER IN ANY OF MY VIDEO, USE THIS RED CANCEL LINE"* (2026-10-25) ❌
- **C2.45** A box animated in over another box (use C2.25). ✅ (2026-10-25) ❌
- **C2.46** Light-leak transitions. 🏢 ❌
- **C2.47** A dark frame at the start of a card (use a negative NeoAnim start offset so the card is on screen at the cut), white flashes, or a black band at the top of a page entrance (fix with slide 0, not Edges = Duplicate). ⚙️ (2026-10-25) ❌

## Pictures
- ![[_attachments/rulebook/c2-state-change-one-by-one.jpg|360]] ✅ LinkedIn beats: twin cards change state in place (FLOPS → TAKES OFF), offer grid builds one part at a time (approved LinkedIn bar)
- (no picture yet: a frame strip of one entrance, showing the long ease-out against a bounce)

## Questions for Samuel
- **Q-C2.a** Entrance length. 2026-09-26 your four-box used ~8 f moves (ours at 18 f were too slow); 2026-10-15 and 2026-10-24 you said too fast, slow and smooth is better, and the house rule became 16-22 f. Your finals sit at 12-25 f. → Options: (1) 16-22 f for every entrance (2) 16-22 f for main elements, 8-12 f for small parts inside a group. My pick: (2), with the 3-6 f stagger. → Samuel: (2), 16-22 f main elements, 8-12 f small parts inside a group (2026-11-05). C2.3 updated.
- **Q-C2.b** Exits. Your Apollo final uses NeoAnim Out 8-12 f; the house rule says 10-14 f. → My pick: 10-14 f (the slower ruling is later). → Samuel: yes, 10-14 f (2026-11-05).
- **Q-C2.c** Background motion. 2026-10-25 "everything feels static" (you had animated the companies in the background before); 2026-10-31 "too much animation on the blue background". → My pick: slow drift in the background, all the real motion on the main content (C2.26). → Samuel: yes, slow drift in the background, the real motion on the main content (2026-11-05).

## Sources
Draws on and replaces the motion parts of [[03-Areas/video-editing/samuel-review-card|Samuel's review card]] (P1, P3, P6, S2, C8), [[03-Areas/video-editing/ways-of-working|Ways of working]], [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]], [[03-Areas/video-editing/sops/fusion-build|Fusion build SOP]], [[03-Areas/video-editing/motion-gallery/motion-gallery|Motion gallery]], [[03-Areas/video-editing/creative-director/creative-director-standard|Creative director standard]], [[03-Areas/video-editing/visual-vocabulary|Visual vocabulary]]. NeoAnim and macro settings: [[03-Areas/video-editing/rulebook/rb-b3-main-nodes-and-macros|B3]]. Script quirks (keys, eases, offsets): open [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] when a key or ease won't set.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
