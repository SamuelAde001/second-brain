---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: D2
---

# D2 · Sound effects

> **Read when:** the sound pass of any Route Rise job (placing SFX, setting levels, mastering), and when a reviewer checks the mix. Music and voice are in [[03-Areas/video-editing/rulebook/rb-d1-music|D1]]; when the sound pass happens is D1.1-D1.3. **Client values:** none. **Status:** draft, not yet approved by Samuel.

**The latest ruling (Samuel, 2026-10-26) overrules every older SFX rule:** use the sound design of the first two or three videos, modelled on his delivered #3. *"the sound effects I used initially in the first two or three videos ... are the ones that are best."* The "a sound on every animated item" rule of 2026-10-16 is withdrawn (see Superseded).

## Rules
### Density and palette (the #3 model)
- **D2.1** Density about 12 SFX a minute: his #3 had 122 SFX in 9.9 min. Only about one in three graphic reveals gets a sound. ✅ (2026-10-26) 🎬
- **D2.2** Small palette from his own library (`Downloads\sounds\Sound effects\`, read-only, imported by reference). #3 used 9 files: ✅ *"go to my Sound library"* (2026-09-28) 🎬

| File | Use | Level (dB) | Count on #3 |
|---|---|---|---|
| UI Double Beep 03 | graphic landings, cascades | −43.1 (−46.6 minor) to −48.6 | 42 |
| Swoosh_03 | section reveals, things that move in | −22.2 to −35.5 | 24 |
| Arpeggiated UI Beep 03 | graphic landings | −38.4 to −43.6 | 18 |
| Camera_01 | photo and B-roll cuts, montage cuts | −32.5 / −33.2 | 12 |
| Mouse Click (5) | every on-screen click in a UI demo | −29.3 | 9 |
| Multiple UI Beeps 01 | real lists only | −40.3 to −48.7 | 8 |
| ES_Low Hit | the open and section reveals only | −14.9 to −19.3 | 6 |
| Cybernetic Data Processing 1 | AI-writing moments, at most 2 | −44.2 | 2 |
| cinematic riser 4 | once, into the first big reveal | −24.5 | 1 |

- **D2.3** Keep SFX low, as low as his #3, so they never distract. 🔁 ×3 ✅ (2026-09-28, 2026-10-16, 2026-10-26) 🏢
- **D2.4** Every sound must fit what is on screen. A car sound needs a car on screen. ✅ *"if he's hearing a sound effect of a car, he needs to see something related to a car"* (2026-10-19)
- **D2.5** SFX mark graphic reveals, not cuts (in his finals 35 % of reveals had a hit within a few frames, only 8 % of cuts). 🎬

### Placement (from his #3)
- **D2.6** The open: ES_Low Hit −14.9 from source frame 1, plus Swoosh_03 −22.2, both on frame 0. 🎬
- **D2.7** Section reveal: Swoosh_03 −22.2 starting 7 f before the reveal, Low Hit −15.6 starting 5 f before. 🎬
- **D2.8** Riser: cinematic riser 4 starts 35 f before the Low Hit so it ends on the hit. Once a video. 🎬
- **D2.9** Lists: a cascade of UI Double Beep 03, 3-6 f apart, at −43.1 (−46.6 for minor items), each on its own track. Only for a real list on screen. 🎬
- **D2.10** Mouse Click (5) −29.3 on the exact frame of every on-screen click in a UI demo. 🎬
- **D2.11** Camera_01 −33.2 on photo and B-roll cuts, montage cuts included. 🎬
- **D2.12** No beeps on demo starts: he disabled about 20 of the Editor's 120 hits on #3, mostly Multiple UI Beeps 01 on demo starts and a few swooshes. ✅ (2026-10-04)
- **D2.13** Time every SFX from the comp itself (`.setting` landing frames), not from notes. ⚙️
- **D2.14** When Samuel moves or disables a visual, move or remove its sounds with it. ⚙️ (video 4 miss, 2026-10-29)

### Levels and files
- **D2.15** Set levels by loudness, not by file. Risers: max momentary loudness + clip volume = −34.2 (his cinematic riser 4 at −24.5). Other files: match his reference level. ⚙️
- **D2.16** No SFX louder than the song under it. 🎯 (Route Rise CD, 2026-10-26)
- **D2.17** Some library files lie about their container ("camera shot.wav" is MP4). Convert only those to a PCM copy, and test-import every path. ⚙️

### Mix and loudness
- **D2.18** Render the whole timeline's audio in one pass (chunk joins had 20 ms dropouts). How: [[03-Areas/video-editing/rulebook/rb-e1-rendering|E1]]. ⚙️
- **D2.19** Master the final: working value −16 LUFS integrated, true peak −1 dBTP (`audio\loudness.py`, `master.py`). **Not confirmed by Samuel.** See Q-D2.a. ⚙️ 💡

### Tools
- **D2.20** Sound plan, events and mix check by script: `audio\sound_plan.py --config`, `sfx_events.py`, `sound_place.py`, `mix_check.py` (video 4 choices in `audio\examples\`). After any re-derive, diff the new plan against the last one by (frame, beat, kind). How to run: [[03-Areas/video-editing/sops/video-pipeline-tools|video pipeline tools]]; library and import quirks: [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]]. ⚙️

## Never
- **D2.21** No SFX on A-roll cuts, highlighter swipes, counter ticks, typing, scrolls or cursor glides. ❌ 🎯 (Route Rise CD, 4 notes, 2026-10-26)
- **D2.22** No foley or ambience, chings, cash registers, money counters, sub drops or "techno" data beds. ❌ 🎯 *"didnt like the techno style SFXs here maybe volume or maybe too many in a row"* (2026-10-26)
- **D2.23** No run of beeps in a row. ❌ 🎯 (2026-10-26)
- **D2.24** No clack or pop on a key word (CD note on "$0"). ❌ 🎯 *"can u remove that clack sound"* (2026-10-26)
- **D2.25** No random SFX that don't fit the moment. ❌ ✅ *"a lot of sound effects that were random and didn't make sense in the context"* (2026-10-26)
- **D2.26** No keyboard-typing SFX, no loud repetitive SFX. ❌ 🏢 See Q-D2.b.
- **D2.27** No two sounds on the same moment. ❌ 🎯
- **D2.28** Never the video 2 v6 density: 500-650 SFX from 130-166 files (about 50-60 a minute) was rejected. ❌ ✅ (2026-10-26)

## Pictures
- (no picture yet: a still of his delivered #3 timeline's SFX tracks with the levels showing, as the density reference)

## Questions for Samuel
- **Q-D2.a** Loudness target. Your finals measure −24.6 LUFS (B2B), −22.2 (10000 SaaS), −16.6 (LinkedIn 4K, which the CD passed). Cold Email / video 4 was mastered to −16 LUFS (2026-10-29), with true peak written as −1 in one note and −1.5 dBTP in another. Your 4K B2B re-render came out 3.8 dB louder than the 1080p. You never stated a number. → Options: (1) −16 LUFS / −1 dBTP on every final; (2) leave the mix at your levels, no mastering; (3) another number. My pick: (1), it is YouTube-normal and the CD passed it.
- **Q-D2.b** Typing sounds. Apollo, one of the "first videos" you called the best, had typing beds (his Mac keyboard file at −35 dB on typed lines). Your #3 had none, Route Rise's notes ban keyboard-typing SFX, and the Route Rise CD list says no SFX on typing. → Options: (1) no typing sounds ever; (2) soft typing bed only on long typed lines in a demo. My pick: (1).
- **Q-D2.c** Is "about 12 a minute" a target or a ceiling? Cold Email (2026-10-29) shipped 72 SFX and no verdict on its sound is recorded. → Options: (1) target ~12 a minute, hook a bit denser; (2) ceiling, fewer is fine. My pick: (2), quiet beats a wrong sound.

## Sources
Replaces and draws on [[03-Areas/video-editing/samuel-review-card|Samuel's review card]] → Sound, [[03-Areas/video-editing/routerise-house-style|Route Rise house style]] §8 (Changed back), [[03-Areas/video-editing/ways-of-working|ways of working]] 2026-10-16 and 2026-10-26, [[03-Areas/video-editing/edit-grammar/edit-grammar-shared-rules|edit grammar]] S0.12, [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] 2026-10-25, the Apollo, LinkedIn, 10000 SaaS and Cold Email job notes.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
