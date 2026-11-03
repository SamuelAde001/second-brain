---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: F5
---

# F5 · Speed and timing of work

> **Read when:** planning a job's days, setting up a night run, answering "where are we?", any deadline. The Editor and the General Manager. **Client values:** Route Rise's 5-day cap is in [[03-Areas/video-editing/rulebook/rb-k1-route-rise|K1 Route Rise]]. **Status:** draft, not yet approved by Samuel.

## Rules
### Speed, quality, deadlines
- **F5.1** Speed and quality together. Speed is first in his order (F3.1); quality means nothing he has to fix later. Videos ran late again and again. 🔁 5 times. *"I need speed and I need quality"* (2026-10-28) · *"Why is this video not yet done?"* (2026-10-25) · *"Also, you are very slow so far"* (2026-10-31)
- **F5.2** Hit the deadline he sets (e.g. *"at most 2 hours"*, 2026-10-25; to the creative director by Thu 18:00, 2026-10-29). Leave margin: Gamma was missed on an install collision plus an audio-only render that rendered the whole video. ✅ (2026-10-25 to 2026-11-01)
- **F5.3** If the bar and the deadline clash, tell him early with the causes and give him the choice: deliver now, or polish. ✅ (2026-10-25)
- **F5.4** Don't hurry into bad work, and don't spend excess hours; don't take long on small setups. 🔁 5 times. *"anytime you are in a hurry, you end up doing a bad job"* (2026-10-15) · *"don't waste time but don't make mistakes"* (2026-09-26)
- **F5.5** The pace to aim for: 5 Route Rise videos a month with Claude doing 70-80 % of the editing. A normal video is five days, most of it visuals. ✅ *"I really want to be able to have 70 to 80% of Claude do a lot of my video editing"* (2026-09-27) · (2026-09-29)
- **F5.6** When a card is due past midnight, deliver the day before (due Sat 02:15 → deliver Fri). Flag the risk at once when the working days are too few for the length. ⚙️
- **F5.7** Track every Route Rise job; none is forgotten. Start the next one as soon as one ships. ✅ *"You forgot the AI breakdown video I am to do for Routerise"* (2026-10-20) · *"let's get the next project started now, cause my company wants me to be faster"* (2026-09-29)

### Unattended runs
- **F5.8** Claude runs a whole job start to finish while he sleeps; he only reviews. Method: [[03-Areas/video-editing/sops/unattended-run|unattended run]]. ✅ *"I want to be able to let Claude work from the beginning till the end while I go to sleep"* (2026-10-13)
- **F5.9** Before he leaves, ask for every permission and decision the run will need. Then avoid anything that needs his approval while he is away. 🔁 8 times. *"If you want anything that will make you need approval, do the approval right now."* (2026-10-28)
- **F5.10** Power cuts: every long job resumes from files on disk. Rewrite the RUN STATE `>>> NOW` block at every step, keep the job note's RESUME block current, commit after each stage, run the hourly watchdog (it disables itself after the deadline). 🔁 6 times. *"So my power went off, I want you to continue from where you stopped"* (2026-10-24, 2026-10-28, 2026-11-01)
- **F5.11** Never stop to wait on him mid-task or overnight. If you truly need him, send a push notification to his phone. When a render lands, tell him at once with the file. 🔁 5 times. *"Stop stopping I don't have time, finish the work"* (2026-09-27) · *"if you need me, send a push notification for my phone"* (2026-09-25) · *"Why didn't you tell me"* (2026-10-29)
- **F5.12** Night runs have no approval stops: build on defaults, the Editor approves looks against the review card, and every choice goes on the morning review list. ✅ *"I want it to do the both in one session, so I don't prompt again this night"* (2026-10-08) · (2026-10-28)
- **F5.13** When he says so, the night runs through: finish fixes → music and SFX → render, no review stop. Delivery stays his call. ✅ *"When you are done, go ahead and add music and sound effects ... and render it"* (2026-10-24)
- **F5.14** When he says halt, or stops the edit to correct it himself, stop every script, keeper and watchdog at once and write the restart order in RUN STATE. ✅ *"Wait, halt on this video, my creative director has sent in corrections"* (2026-10-26) · (2026-10-25)
- **F5.15** Put the PC to sleep only when the job he named is done and cached. ✅ *"If you are done and the video is fully cached and it's not yet 7am, put my computer to sleep"* (2026-10-16)

### Telling Samuel, and his own time
- **F5.16** When he asks, give % complete and an ETA; on delivery day give a time plan with an estimate. Answer status questions with links to the files he can watch. ✅ *"How many % till the whole video is done? and what is the estimated time?"* (2026-10-09) · *"Link me the videos so I can find them"* (2026-10-25)
- **F5.17** He never waits on Claude: he approves visuals as stills, Claude builds while he is away, he does his parts (zooms, tracking) in between. ✅ *"I don't want to have to always wait for Claude to finish up a particular part of the video"* (2026-09-27)
- **F5.18** Plan each day's client work the night before. Don't put client work blocks in TickTick. ✅ *"don't schedule, cause when you schedule we never follow your plans on my tiktik and it becomes noise"* (2026-10-18)
- **F5.19** When he asks for "a timer" for a video, he means the `edit-clock` pace widget (planned vs actual playhead, WAT), not a countdown. ✅ (2026-09-20) · (2026-10-02)
- **F5.20** Size slow work to the need: Deliver stills cost 2-10 s a frame on comp-heavy timelines (542 stills ≈ 1.5 h), so batch them in the background and grab only the frames the review needs. ⚙️

## Never
- **F5.21** Stop and wait for him while he is away. ❌ *"don't stop, for anything"* (2026-09-25)
- **F5.22** Schedule job steps as TickTick blocks. ❌ (2026-10-18; replaces the 2026-09-29 practice)

## Pictures
- (no picture yet: none needed; this section is about process)

## Questions for Samuel
- **Q-F5.a** Can a deadline slip for a perfect video? 2026-10-07 and 2026-10-18: *"I have no issues delaying as long as I have a perfect video"*. Since 2026-10-24: speed first, and late videos drew *"Why is this video not yet done?"*. → Options: (1) the deadline holds; if the bar is at risk, tell you early and you choose (F5.3) (2) perfection over the deadline unless you name a hard date. My pick: 1.
- **Q-F5.b** "Push notification to my phone" (2026-09-25): in Claude Code that is the push notification tool. Is that the channel for every "I need you" during a night run, or should it also go to TickTick or Telegram? → Options: (1) push notification only (2) push plus a line in RUN STATE. My pick: 2.

## Sources
Draws on [[03-Areas/video-editing/sops/unattended-run|unattended run]], [[03-Areas/video-editing/ways-of-working|ways of working]] → Time and delivery, [[03-Areas/video-editing/workflow|workflow]], [[03-Areas/video-editing/agent-plan|agent plan]], [[03-Areas/video-editing/toolchain|toolchain]].

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
