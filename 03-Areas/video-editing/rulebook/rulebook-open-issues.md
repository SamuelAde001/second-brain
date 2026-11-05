---
type: sop
area: video-editing
status: needs-input
updated: 2026-11-05
source: manual
tags: [rulebook, review]
---

# Rulebook open issues

Every open issue in the [[03-Areas/video-editing/rulebook/rulebook|rulebook]], in one place (Samuel, 2026-11-05: *"Get me where all the issues are so I answer them and finalise this rule book"*). Made by `rb_issues.py`. **15 questions** and **2 rules that are only my inference** (💡). Gamma (K3) and the other client overlays come first.

**The other 995 waiting rules** come from your own words or your finals. Once these issues are answered, say *approve the rest* and they all get ✔ in one go; anything you correct later comes in as a revision and is written back.

**How to answer:** in chat, e.g. `Q-K3.a 1`, `C2.14 drop`, `rest yes`, or type after **Answer:** here in Obsidian.

## [[03-Areas/video-editing/rulebook/rb-d1-music|D1 · Music]]

**Questions**
- **Q-D1.b** Alex asked for "no music under the voice" (2026-10-06). Every later video shipped with music under the voice. → Options: (1) that note is dead, music as above; (2) it still holds for Alex, mute A2 under speech. My pick: (1), keeping music on A2 so it mutes in one click.
  - **Answer:** 
- **Q-D1.c** Song length: Route Rise's notes say never a song over 90 s (2026-09-25); the CD standard says about 1-2 minutes a song (2026-10-22). → Options: (1) 90 s cap; (2) 1-2 min, change at section boundaries only. My pick: (2), because changes must land on section boundaries.
  - **Answer:** 
- **Q-D1.d** Voice clean-up: the CD standard says Adobe Podcast (Enhance Speech) on every video (2026-10-22); you fixed video 2 and video 4 with Resolve's Voice Isolation on A1. → Options: (1) Voice Isolation at your value only; (2) Adobe Podcast first, then your value. My pick: (1), it is what you did yourself.
  - **Answer:** 

## [[03-Areas/video-editing/rulebook/rb-d2-sound-effects|D2 · Sound effects]]

**Questions**
- **Q-D2.a** Loudness target. Your finals measure −24.6 LUFS (B2B), −22.2 (10000 SaaS), −16.6 (LinkedIn 4K, which the CD passed). Cold Email / video 4 was mastered to −16 LUFS (2026-10-29), with true peak written as −1 in one note and −1.5 dBTP in another. Your 4K B2B re-render came out 3.8 dB louder than the 1080p. You never stated a number. → Options: (1) −16 LUFS / −1 dBTP on every final; (2) leave the mix at your levels, no mastering; (3) another number. My pick: (1), it is YouTube-normal and the CD passed it.
  - **Answer:** 
- **Q-D2.b** Typing sounds. Apollo, one of the "first videos" you called the best, had typing beds (his Mac keyboard file at −35 dB on typed lines). Your #3 had none, Route Rise's notes ban keyboard-typing SFX, and the Route Rise CD list says no SFX on typing. → Options: (1) no typing sounds ever; (2) soft typing bed only on long typed lines in a demo. My pick: (1).
  - **Answer:** 
- **Q-D2.c** Is "about 12 a minute" a target or a ceiling? Cold Email (2026-10-29) shipped 72 SFX and no verdict on its sound is recorded. → Options: (1) target ~12 a minute, hook a bit denser; (2) ceiling, fewer is fine. My pick: (2), quiet beats a wrong sound.
  - **Answer:** 

**My inferences (keep, change or drop)**
- **D2.19** Master the final: working value −16 LUFS integrated, true peak −1 dBTP (`audio\loudness.py`, `master.py`). **Not confirmed by Samuel.** See Q-D2.a. ⚙️ 💡
  - **Answer:** 

## [[03-Areas/video-editing/rulebook/rb-e1-rendering|E1 · Rendering and delivery]]

**Questions**
- **Q-E1.a** How do you review now? Until 2026-10-16 you reviewed from a fully cached timeline (seven times). Since video 2 (2026-10-24) the Editor sends a 1080p review render plus phone parts, and on video 4 that was the plan. → Options: (1) cached timeline; (2) 1080p render + phone parts; (3) both. My pick: (3): the render for your phone, the cache for marking in Resolve. → Samuel (2026-11-03, A2.29): a render, imported onto its own timeline for his markers; no cache for review.
  - **Answer:** 
- **Q-E1.b** Delivery file name. No rule exists; only "v1/v2" and the job title. → Options: (1) `<video title> v<N>.mp4` in the job folder; (2) your own pattern. My pick: (1).
  - **Answer:** 
- **Q-E1.c** Upload. You wanted a system that spots a finished render, uploads it to the right Frame.io folder and posts the link on Slack for the CD (2026-09-28, *"we would work on a system for this later"*). → Options: (1) build it now; (2) keep sending by hand. My pick: (2) until you say; you watch every version first anyway.
  - **Answer:** 

## [[03-Areas/video-editing/rulebook/rb-e2-revisions-and-quality|E2 · Revisions and quality management]]

**Questions**
- **Q-E2.c** Version names for deliveries to Route Rise: only "v1/v2" as you name them. See Q-E1.b.
  - **Answer:** 

## [[03-Areas/video-editing/rulebook/rb-f2-bugs-and-crashes|F2 · Bugs, crashes, bug reports]]

**My inferences (keep, change or drop)**
- **F2.15** Tell him in one block: what broke, last call, last save time, what was lost, what you did, what's next. If he is away and you need him, ping his phone (F5.11). 💡
  - **Answer:** 

## [[03-Areas/video-editing/rulebook/rb-f3-tokens-and-scripts|F3 · Token management, cost, scripting]]

**Questions**
- **Q-F3.b** Use the week up or keep a reserve? 2026-10-13/14: *"by the reset, I should be around 99% usage"* and *"every five hours, we've used 100%"*. 2026-11-01: *"not to run out of credits as I need credits for other works"*. → Options: (1) keep a reserve; spend leftovers only on work you name (2) use it up by the reset. My pick: 1.
  - **Answer:** 

## [[03-Areas/video-editing/rulebook/rb-f4-sub-agents|F4 · Sub-agent work]]

**Questions**
- **Q-F4.a** Pool size. You said 3-5 (2026-10-15), then *"at most 7 agents"* (2026-10-22), then *"more helpers than just 8"* (2026-10-24), then *"as much agents that you think is reasonable for every 5 hours"* (2026-10-26). The 14-per-workflow cap is ours, not yours. → Options: (1) up to 14 per workflow, the stop is the job ceiling (2) a fixed number you name. My pick: 1.
  - **Answer:** 
- **Q-F4.b** Corrections under a deadline. 2026-10-25: *"every single individual correction ... should have their own individual agents working on it ... and then other agents cross check"*. The 2026-10-28 audit found that one fixer plus one checker per marker was 69 % of helper spend, and switched to one Opus fix spec per section with workers fixing 2-4 beats each. → Options: (1) batches of 2-4 beats per worker, checked independently (2) one agent per correction. My pick: 1.
  - **Answer:** 

## [[03-Areas/video-editing/rulebook/rb-f5-speed-and-timing|F5 · Speed and timing of work]]

**Questions**
- **Q-F5.a** Can a deadline slip for a perfect video? 2026-10-07 and 2026-10-18: *"I have no issues delaying as long as I have a perfect video"*. Since 2026-10-24: speed first, and late videos drew *"Why is this video not yet done?"*. → Options: (1) the deadline holds; if the bar is at risk, tell you early and you choose (F5.3) (2) perfection over the deadline unless you name a hard date. My pick: 1.
  - **Answer:** 
- **Q-F5.b** "Push notification to my phone" (2026-09-25): in Claude Code that is the push notification tool. Is that the channel for every "I need you" during a night run, or should it also go to TickTick or Telegram? → Options: (1) push notification only (2) push plus a line in RUN STATE. My pick: 2.
  - **Answer:** 

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
