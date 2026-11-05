---
type: sop
area: video-editing
status: approved
approved: 2026-11-05
updated: 2026-11-05
source: interview
tags: [rulebook]
section: F4
---

# F4 · Sub-agent work

> **Read when:** planning a fan-out, writing a helper brief, sizing work per helper, restarting after a cut-off. The Editor. Helpers read their own profile instead. **Client values:** none. **Status:** approved by Samuel, 2026-11-05 (issues answered one by one, the rest approved in one go).

## Rules
### When and how many
- **F4.1** On video jobs, run parallel helpers, as many as the job needs, without asking. ✅ *"From now on the Editor can run parallel helper agents on video jobs, as many as the job needs. Write it into the rules."* (2026-10-24) · ✔ 2026-11-05
- **F4.2** Spawn an agent only for a specific planned task. Work that needs no agent, do yourself. 🔁 3 times. *"Make use of your agent well. The work that doesn't need an agent, do it yourself"* (2026-10-15) · ✔ 2026-11-05
- **F4.3** Pool: up to 14 helpers per workflow (his 16-core PC), two workflows at once only when the work splits cleanly. No 5-hour pacing (F3.7); use what the job needs, efficiently (F3.5). ✅ *"Don't you think we need more helpers than just 8 helpers at a time?"* (2026-10-24) ⚙️ · ✏ 2026-11-05
- **F4.4** At most ~6 helpers render through Resolve at once unless the render queue runs; the rest take work that needs no Resolve (planning, captures, generators, SFX picks). ⚙️ · ✔ 2026-11-05

### Who does what
- **F4.5** Opus thinks, Sonnet works. Opus (main session, `editor-builder`) plans, makes hero frames and anchors, does the section pass, verifies blocking faults, writes fix specs. Sonnet (`editor-worker`) builds beats and reviews beats from exact specs. 🔁 3 times. *"Opus should give the direction ... Sonnet should now be the one doing most of the grind"* (2026-10-28) · beat reviews to Sonnet (2026-10-30) · ✔ 2026-11-05
- **F4.6** Independent checking stays: a builder never signs off its own work. Reviewers stay lean: cards, records and stills only. ✅ *"Said builders should check their own card. Doesn't that mean that the quality will be bad or reduced"* (2026-10-24) · ✔ 2026-11-05
- **F4.7** The Editor still checks crops itself after the reviewers (it caught a kit fault they missed). Anything that fails the bar after several tries, the Editor fixes personally. ⚙️ · ✔ 2026-11-05
- **F4.8** Captures in Chrome and MCP work use the default helper type; the lean types have no browser. ⚙️ · ✔ 2026-11-05

### The brief
- **F4.9** The main agent prepares everything so helpers make no mistakes and forget nothing. ✅ *"you as the main agent should make sure you have everything well ready so that there is no mistakes"* (2026-10-28) · ✔ 2026-11-05
- **F4.10** A brief is one page: the rules its beats need, kit commands, check steps, plus only its own beats' records and hero frames, the review card and the client overlay. Never the whole plan, brief stack or Brain notes (long read lists hit the guard after 1-3 visuals; 21 beats were left unbuilt). ⚙️ · ✔ 2026-11-05
- **F4.11** A worker returns anything vague, or anything that failed twice, as `needs Opus`. It never guesses. ⚙️ · ✔ 2026-11-05

### Size, so no agent dies
- **F4.12** Give every agent enough room to finish: no agent dies mid-task. Make the pieces smaller; don't make the cap shorter. Helpers wrap at 300k and return at 350k. 🔁 4 times. *"I don't want any token to be lost in the process of failure."* (2026-10-20) · *"I don't want wasted tokens due to short caps"* (2026-10-28) · ✔ 2026-11-05
- **F4.13** Workers get 2-4 neighbouring beats so each finishes near 150k. Fix batches are 2-4 beats from one Opus fix spec per section. ⚙️ · ✔ 2026-11-05
- **F4.14** Never idle-wait: a helper's cache lives 5 minutes. Send a render, build the next piece; if nothing else, check every 4 minutes or less. (Helpers slept ~36 of 97 hours on video 2 waiting on the lock.) ⚙️ · ✔ 2026-11-05

### Flow
- **F4.15** Pipeline, not waves: each beat goes build → review → fix as soon as its last step ends. Install each piece as soon as it passes; never hold installs for the whole batch. ✅ he asked why so much was left (2026-10-07) ⚙️ · ✔ 2026-11-05
- **F4.16** Helpers never drive Resolve (F1.1): they drop render requests in the queue and keep working. ⚙️ · ✔ 2026-11-05
- **F4.17** Fast mode, when he wants corrections fast: one lab render per fixer, checkers review the fixer's stills, no second check round. ✅ *"We need to get this correction done fast"* (2026-10-26) · ✔ 2026-11-05
- **F4.18** Headless Chrome captures run one after another (`queue.sh`, skip existing, retry once); separate queues need their own `RR_PORT`. ⚙️ · ✔ 2026-11-05
- **F4.19** A big piece (the intro) may run in its own session at the same intensity. ✅ (2026-10-08) · ✔ 2026-11-05

### After a cut-off
- **F4.20** Builders resume from what is already in their folders: each writes a manifest and a FIX_REPORT. Relaunch only the pieces with no result on disk; retry a null agent once. ⚙️ · ✔ 2026-11-05
- **F4.21** Keep the plan, workflow script and resume note in the job's Docs and the Brain, never only in the session. ⚙️ · ✔ 2026-11-05

### Telling Samuel
- **F4.22** The Editor logs every fan-out in its log. When he asks, show the flow: what each agent did and what the Editor passed down, with a diagram. ✅ *"I need to understand the flow of what Editor has been doing and what he passed down to the other agents, if possible give me a digram"* (2026-10-15) · ✔ 2026-11-05

## Never (strict)
- **F4.23** 60-100 agents at once (83 at once burned the 5-hour window, 197 calls failed). 🔁 2 times. ❌ *"Don't don't spawn out 100 agents like you did the other day."* (2026-10-15) · ✔ 2026-11-05
- **F4.24** Two fixers on one beat. Merge tasks by beat; dedupe before install (two jobs once built the same text-overs). Never launch with an empty beats list. ⚙️ · ✔ 2026-11-05
- **F4.25** `resumeFromRunId` on a multi-iteration workflow after a restart: it re-runs finished agents. ⚙️ · ✔ 2026-11-05
- **F4.26** A fixed time limit on helpers (the 4-minute limit made them slower, re-reading). The 4-minute check in F4.14 is how often to look, not a limit. ❌ (2026-10-24) · ✔ 2026-11-05

## Pictures
- (no picture yet: none needed; this section is about process)

## Questions for Samuel
- **Q-F4.a** Pool size. You said 3-5 (2026-10-15), then *"at most 7 agents"* (2026-10-22), then *"more helpers than just 8"* (2026-10-24), then *"as much agents that you think is reasonable for every 5 hours"* (2026-10-26). The 14-per-workflow cap is ours, not yours. → Options: (1) up to 14 per workflow, the stop is the job ceiling (2) a fixed number you name. My pick: 1. → Samuel: (1), up to 14 per workflow; no 5-hour pacing (2026-11-05).
- **Q-F4.b** Corrections under a deadline. 2026-10-25: *"every single individual correction ... should have their own individual agents working on it ... and then other agents cross check"*. The 2026-10-28 audit found that one fixer plus one checker per marker was 69 % of helper spend, and switched to one Opus fix spec per section with workers fixing 2-4 beats each. → Options: (1) batches of 2-4 beats per worker, checked independently (2) one agent per correction. My pick: 1. → Samuel: (1), batches of 2-4 beats per worker, checked independently (2026-11-05).

## Sources
Draws on [[00-System/model-routing|model routing]] → On Max 20x, Audit 2026-10-28, Sonnet-first helpers; [[03-Areas/video-editing/sops/unattended-run|unattended run]] step 4; [[07-Agents/editor-builder/profile|editor-builder]] and [[07-Agents/editor-worker/profile|editor-worker]] profiles; [[07-Agents/video-editor/profile|Editor profile]] → Parallel helpers.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
