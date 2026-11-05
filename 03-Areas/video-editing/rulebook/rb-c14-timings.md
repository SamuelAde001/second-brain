---
type: sop
area: video-editing
status: approved
approved: 2026-11-05
updated: 2026-11-05
source: interview
tags: [rulebook]
section: C14
---

# C14 · Timings

> **Read when:** writing a beat spec, building or re-placing a comp, running the beat lint, reviewing motion. Builders, workers and reviewers. **Client values:** none. **Status:** approved by Samuel, 2026-11-05 (issues answered one by one, the rest approved in one go).

## Rules
### Where the timing comes from
- **C14.1** Time every graphic to the words before building it. The timeline cuts show where each visual starts and stops. 🔁 (6) ✅ *"This fusion comp is not well timed to when he was saying the words"* / *"use the cuts in the timeline as a guide for where each visual should start and stop"* (2026-09-27 to 10-03) · ✔ 2026-11-05
- **C14.2** Take word times from the real word frames of the conformed WAV, re-timed. Never from beats.json (it ran 15-69 f early) and never from comp frame 0: Fusion comp time is relative to the clip. ⚙️ → [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] for the offsets · ✔ 2026-11-05
- **C14.3** Before timing an overlay on one of his comps, read the animation already in it. ⚙️ · ✔ 2026-11-05
- **C14.4** Check every animate-in against the transcript. 🔁 (2) ✅ *"make sure that the timings are also right, the timings of the animation, the animated animation in"* (2026-10-06) · ✔ 2026-11-05

### Each element on its word
- **C14.5** Each element enters on its own word and is readable 0-3 f after the word starts, never before. The lint allows −1 to +5 f for Whisper error. 🔁 (3+) ✅ *"Animate one thing in at a time, the stick one should come when he said it"* (2026-10-25) 🎬 🎯 (review card P1) · ✔ 2026-11-05
- **C14.6** One element per word, one after another. No two separate elements enter on the same frame. Lists, logos and companies come in one by one. 🎬 (his finals set NeoAnim / NeoTextMotion InOffset to word frames) · ✔ 2026-11-05
- **C14.7** Graphics follow speech, never ahead. No label, name or number shows before it is said. 🎯 (CD06 07:10) 💡 (HK-04, 2026-10-22) · ✔ 2026-11-05
- **C14.8** A counter is judged on where the count ends against where the spoken number ends. ⚙️ → C4, C10 · ✔ 2026-11-05
- **C14.9** No effect shows before its element lands (no shine before its turn). 🔁 (2) ✅ *"Why am I seeing the shine on screen before it is animated"* (2026-10-14, 10-24) → C7 · ✔ 2026-11-05
- **C14.10** Switch between A-roll and B-roll exactly on the words he marks. 🔁 (4) ✅ *"Switch back to A-roll here"* / *"Then back to this B-roll"* (2026-10-15) · ✔ 2026-11-05
- **C14.11** In a two-line quote the second line starts 37 f after the first. 🎬 (TSB) · ✔ 2026-11-05
- **C14.12** Put cues for logos, icons and boxes in the beat manifest so the lint can check them, e.g. `"cues": {"NeoAnim_Logo": "Stripe"}`. ⚙️ · ✔ 2026-11-05

### Holds: time to read
- **C14.13** The last element is fully landed at least 36 f (~1.5 s) before the cut or before an exit animation starts. Plan this in the spec, not in a fix round (74 of 142 video 2 beats missed it). 🎯 🔁 (3 CD notes) *"never did was too fast we didnt have time to read it"* (2026-10-26) · ✔ 2026-11-05
- **C14.14** A visual the viewer must read stays a few seconds. Only a one-glance visual (a red graph falling, 8 of 10 icons lit) may flash. 🎯 (2026-10-22) · ✔ 2026-11-05
- **C14.15** Hold key words long enough on screen (the CD: hold "Never did"). 🎯 (2026-10-26) · ✔ 2026-11-05
- **C14.16** No visual shorter than 0.9 s, except montage beats. 🎬 · ✔ 2026-11-05
- **C14.17** Typical holds in his finals (guides, not quotas): card reveal 2-4 s · UI render ~5.4 s (2-14 s) · motion graphic 5-8 s, a long build-up 13-20 s with reveals along the way · glass panel 6-16 s · caption 1.5-4.7 s (hook 1.17 s) · B-roll cutaway 1.7-7.5 s · montage clip 0.75-2 s. 🎬 · ✔ 2026-11-05
- **C14.18** Rapid montage: one real source per item he says, 0.75-2 s each, each with a big caption. 🎬 (Apollo, 4 AI Tools) · ✔ 2026-11-05
- **C14.19** If there's no room for the hold: (1) run the visual on into the next A-roll breath, (2) move the next visual to a later word, or (3) drop the late element. Never land an element early to make room. ⚙️ (see Q-C14.a) · ✔ 2026-11-05
- **C14.20** If a demo is too long for its stretch, render it slower to fit rather than cutting it short. ⚙️ (Apollo demo, 111 f) · ✔ 2026-11-05
- **C14.21** When a comp is moved to new words, re-time it to them and keep it at least its `min_D` long. ⚙️ · ✔ 2026-11-05

### Ends and gaps
- **C14.22** A visual ends exactly where the next one starts, or on the next cut. Never a gap before a visual's cut. ✅ *"You are leaving gaps in between each visual. Um, gaps before the cut of the visuals"* (2026-10-07) (B2B: 145 of 168 visuals ended 1-12 f early) · ✔ 2026-11-05
- **C14.23** No 1-frame gaps between adjacent visuals. The install check fails on them. ⚙️ · ✔ 2026-11-05
- **C14.24** No plain A-roll sliver under ~2 s between visuals, except cut buffers. A planned breath is longer (C15.9). 🎬 · ✔ 2026-11-05
- **C14.25** A comp never ends before its last word. ⚙️ · ✔ 2026-11-05

### Checking
- **C14.26** Review timing on filmstrips at the word times, not on single stills. Most missed faults are motion and timing, and a still hides them. ⚙️ · ✔ 2026-11-05
- **C14.27** Badly timed visuals get removed, so check them before he has to. ✅ *"I removed the visuals that you put because a lot of them were not well timed"* (2026-10-31) · ✔ 2026-11-05

## Never (strict)
- **C14.28** An element on screen before its word. ❌ (2026-10-25) · ✔ 2026-11-05
- **C14.29** Everything landing at once. ❌ *"Animate one thing in at a time"* (2026-10-25) · ✔ 2026-11-05
- **C14.30** A frame that changes before the viewer can read it. ❌ 🎯 *"this is so fast how can viewer see all the elements on this frame"* (2026-10-26) · ✔ 2026-11-05
- **C14.31** A visual ending early and leaving an A-roll sliver. ❌ (2026-10-07) · ✔ 2026-11-05

## Pictures
- (no picture yet: a filmstrip of one beat with the word frames marked, showing each element landing 0-3 f after its word and the 36 f hold)

## Questions for Samuel
- **Q-C14.a** When "on its word" and "1.5 s hold" clash (the word comes too late for a full hold), our method lets the word win and uses C14.19. → Options: (1) the word wins, extend / delay / drop (2) the hold wins, the element may land up to a few frames early. My pick: (1). → Samuel: (1), the word wins: extend, delay or drop (2026-11-05).
- **Q-C14.b** Shortest A-roll gap. Your finals show none under ~2 s except cut buffers; the Gamma brief (2026-10-31) allowed anything from 6 f. → Options: (1) ~2 s floor (2) 6 f floor. My pick: (1). → Samuel: (1), about 2 s floor (2026-11-05).

## Sources
Draws on [[03-Areas/video-editing/samuel-review-card|Samuel's review card]] (P1, C3, C4), [[03-Areas/video-editing/edit-grammar/edit-grammar|edit grammar]], [[03-Areas/video-editing/creative-director/creative-director-standard|creative director standard]] and [[03-Areas/video-editing/ways-of-working|ways of working]].

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
