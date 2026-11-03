---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: F3
---

# F3 · Token management, cost, scripting

> **Read when:** starting a job (set the budget), before every fan-out, at each stage change, at the end-of-job review. The Editor and the General Manager. **Client values:** none. **Status:** draft, not yet approved by Samuel.

His stance moved over October: *"not bothered about token usage"* (2026-10-13) → *"efficiency is a hard rule"* (2026-10-15) → *"no weekly cap, be efficient"* (2026-10-23) → the 20x order (2026-10-24) → *"don't waste tokens, even though I'm on 20x"* (2026-10-26) → *"Make sure not to run out of credits"* (2026-11-01). The rules below are the latest. One thing never changed: quality first, waste forbidden.

## Rules
### The stance
- **F3.1** Priorities, in order: 1 speed, 2 quality (nothing he has to fix later), 3 efficiency (no waste), 4 memory of past work. ✅ *"number one, speed... Number two, quality ... number three, efficiency... I don't like wastage"* (2026-10-24)
- **F3.2** No waste, ever, even on 20x, and never trade quality for tokens. 🔁 9 times. *"No wastage of tokens, but I want you to do a good work."* (2026-10-20) · *"So don't waste tokens, even though I'm on 20x plan."* (2026-10-26)
- **F3.3** Waste is: rework from wrong builds (the correction-and-check loop was 69 % of helper spend on video 2; 80 % of a week went on a rejected Gamma style), re-teaching or re-studying what the Brain already holds, oversized sessions, agents that die before finishing, idle cache, too many agents at once. ✅ *"we are wasting tokens on repeating things that was already taught, and long sessions"* (2026-10-13)
- **F3.4** A perfect first version is the biggest saving: get the plan and the anchors right before anything is built. ✅ *"we will save more tokens ... if you do a perfect version"* (2026-10-28)

### Budget per job
- **F3.5** Set a usage ceiling for each video at job start, write it in the job note and finish under it. Never use credits he needs for other work. 🔁 3 times. *"By 90% weekly usage, we are already done with this video"* (2026-10-31) · *"Make sure not to run out of credits as I need credits for other works"* (2026-11-01)
- **F3.6** Hard stop at 95 % weekly unless he names another line. When the week runs out, pause the job and resume after the reset. ✅ *"Stop at 95% weekly usage"* (2026-10-13) · *"we would continue this video when the weekly resets"* (2026-10-21)
- **F3.7** Pace each 5-hour window: spread the helpers across it instead of burning it in a burst. At ~95 % of the window let running agents finish, start none, set `paused-5h`. ✅ *"As much agents that you think is reasonable for every 5 hours"* (2026-10-26)
- **F3.8** Read the usage card before every fan-out and write the expected cost in RUN STATE. Estimates run low (5-6 points estimated, ~9 spent): add margin. ✅ (2026-10-15) ⚙️
- **F3.9** Write the weekly % at the start and end of each stage (cut, plan, build, each review round, sound) in the job note. At ~60 % weekly, check in with him on what is left for the next video. ⚙️
- **F3.10** Do the prep (brief, download, setup, phase 1 cut, text plan) before the weekly reset; it costs almost nothing. After the reset, points go to visuals, review, sound, render. ⚙️
- **F3.11** Other sessions (the Brand manager) share the same limits. Leave them room; don't collide in the same window. ✅ *"my brand manager is working on another session. I'm trying not to conflict each other."* (2026-10-22)

### Script first
- **F3.12** What a script can do, a script does, not a helper by hand or by eye: listing, counting, measuring, log parsing, checks, bulk patches. Workers run it in one step. 🔁 3 times. *"I want us to use more scripts for tasks we are sure a script can handle instead of Claude"* (2026-10-30)
- **F3.13** Reuse before building: copy existing comps, adjustment clips and template-library pieces; patch by script for global changes; harvest each finished video into the template set. ✅ *"Do all the things that can make it cheaper"* (2026-10-30) · (2026-09-18)
- **F3.14** Don't re-study his finals: the [[03-Areas/video-editing/edit-grammar/edit-grammar|edit grammar]] notes are the study. ✅ (2026-10-08, 2026-10-13)
- **F3.15** Bulk data goes through scripts, never into context. Tool output prints counts and paths. Images: one contact sheet per beat, 1280 px wide at most, read once; frames pulled by script at low resolution. ⚙️
- **F3.16** Kit and install tools live in the job folder (`kits\inst\`), never only in a session scratchpad. ⚙️
- **F3.17** Flow AI B-roll on Omni Flash (~12 credits), not Veo 3.1 Quality (100 credits). ✅ (2026-10-03)

### Models and effort
- **F3.18** Main session on Opus 5.5. Effort never below `medium`. The job-by-job map is in [[00-System/model-routing|model routing]] → The map. ✅ *"No use of low effort, the lowest is medium"* (2026-09-29)
- **F3.19** Sonnet does all helping except the Opus jobs: a new look (plan, hero frames, anchors), the section pass, verifying blocking faults, turning his or the creative director's notes into fix specs, `needs Opus` items, Resolve debugging and new scripts. Quality must not drop. 🔁 3 times. ✅ *"if possible all helping done with sonnet, but I don't want the qulality to drop"* (2026-10-30)
- **F3.20** A Sonnet spec carries exact values and the approved anchor or library comp, and the scripted checks run before any reviewer looks. ⚙️
- **F3.21** Reading-heavy jobs (sweeps, long transcripts, research) may go to Gemini via `ask_gemini.py`; its answer is a draft. ✅ (2026-10-02)

### Sessions
- **F3.22** One step per session on big jobs. The main session compacts at 500k; at 460k write the RESUME block and commit. ✅ *"compact it by 500k, I don't want the quality of work and output to reduce"* (2026-10-13)
- **F3.23** When a session is heavy, or he says round up: stop runs, save RUN STATE and the RESUME block, and give him the prompt for the next session. Nothing is lost. 🔁 2 times. *"stop, save everything to prep for a new session, and then give me the prompt to give the next session"* (2026-10-15)
- **F3.24** At the end-of-job review run `python 00-System/scripts/usage_audit.py --session <id> --split`. Anything over a tenth of the cost that bought nothing becomes a rule ([[03-Areas/video-editing/sops/end-of-job-review|end-of-job review]]). ⚙️

## Never
- **F3.25** Regenerate comps to apply a global change. ✅ *"can you do that without having to burn tokens regenerating all the comps?"* (2026-10-23)
- **F3.26** Low effort. ✅ (2026-09-29)
- Superseded: *"not bothered about token usage"* (2026-10-13) → F3.2. Every review on Opus (2026-10-28) → F3.19. Fresh session past 100k (2026-10-02), end before 250k (2026-10-12), compact at 200k → F3.22. Ask before a fan-out past ~20 % weekly (2026-10-08) → helpers without asking (2026-10-24). Stop new agents at 85 % of the window (2026-10-08) → F3.7.

## Pictures
- (no picture yet: none needed; this section is about process)

## Questions for Samuel
- **Q-F3.a** Default ceiling when you haven't named one. Cold Email Goldrush took ~50 % of a week (2026-10-30: *"does that mean two videos can go in a week?"*); video 2 had *"maximum 70%"* (2026-10-22); Gamma *"By 90% weekly usage, we are already done with this video"* (2026-10-31). → Options: (1) 50 % of a week per video, so two fit (2) 70 % (3) ask at every job start. My pick: 1, and say the number at job start.
- **Q-F3.b** Use the week up or keep a reserve? 2026-10-13/14: *"by the reset, I should be around 99% usage"* and *"every five hours, we've used 100%"*. 2026-11-01: *"not to run out of credits as I need credits for other works"*. → Options: (1) keep a reserve; spend leftovers only on work you name (2) use it up by the reset. My pick: 1.

## Sources
Replaces the token parts of [[03-Areas/video-editing/sops/unattended-run|unattended run]] → Usage and [[03-Areas/video-editing/ways-of-working|ways of working]]; the long version stays in [[00-System/model-routing|model routing]] → On Max 20x, Audit 2026-10-28, Sonnet-first helpers.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
