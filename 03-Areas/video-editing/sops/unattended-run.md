---
type: sop
area: video-editing
status: active
updated: 2026-10-24
source: interview
tags: [sop, unattended, overnight, versions]
---

# Unattended run: a whole job while Samuel is away

Samuel, 2026-10-13: *"I want to be able to let Claude work from the beginning till the end while I go to sleep and wake up and just have to review what has been done, not me babysitting Claude on every part ... I want to do it all at once and have reviews in versions"*. Also: *"I am not bothered about token usage as long as you give me the best results"*. Quality first; cut only waste (re-studying what is written down, oversized sessions). Decision and the Editor's one objection: [[03-Areas/video-editing/video-editing-decisions|decisions]], 2026-10-13. **First run: LinkedIn Training, 2026-10-13. Untested until then; fold what breaks back into this note.**

## The pieces

- **Conductor:** one Claude Code session acting as the Editor, titled `Editor run: <job>`. It never waits on Samuel between steps. It stays small: the heavy work runs in Workflow agents, each with its own fresh context, returning short summaries (counts, paths). It reads only what the current step needs.
- **Run state:** `Docs\RUN STATE.md` in the job folder. Fields: `status` (running · paused-5h · paused-weekly · blocked · done), `step`, `version`, `updated` (ISO, WAT), `next`. The conductor rewrites it at every step change and before any pause. It is the first thing read on any wake.
- **RESUME block** in the job's Brain note: the step in progress, the next step, files and timelines touched. Rewritten at every step end and when the context guard fires at 460k. After a compaction the conductor reads it and carries on by itself.
- **Watchdog:** the scheduled task `editor-run-watchdog`, hourly. If a session titled `Editor run: <job>` is working, it does nothing. If that session is idle with the run unfinished, it messages it to continue. If there is no such session, the watchdog becomes the conductor (it retitles itself). It only resumes when the usage card has room. When `RUN STATE` says done, it disables itself. To point it at a new job, update its prompt.
- **Keep-awake** for the whole run (`request_keep_awake`, `session_idle`).

## The run, in order

Each pass ends on a **new timeline, `<Visuals vN> (Editor)`**, made from a backup. Never edit the last version Samuel reviewed.

1. Read the job note, the [[03-Areas/video-editing/edit-grammar/edit-grammar|edit grammar]], [[03-Areas/video-editing/routerise-house-style|house style]] §11b, [[03-Areas/video-editing/ways-of-working|ways of working]] → Revision rules. Do not re-study past videos.
2. **Visual plan** against the cut, at the density in the job note.
3. **Intro:** build it from Samuel's suggested visuals if they are in the job note or `Docs\`. Otherwise ideate it yourself and build it, marked as the Editor's own idea.
4. **Build waves:** many small builders, each owning **1-3 visuals**, and one installer agent that alone touches Resolve. Install each wave as soon as it lands.
   - **Why so small** (first run, 2026-10-13): a helper starts at about 72k context (tools, CLAUDE.md, AGENTS.md) and the context guard stops it at 185k. Wave 1 gave builders 5-7 visuals and a reading list (plan header, brief, Brain notes). They spent 30-50k reading and built 6 of 24 visuals.
   - **Briefs are one rules page**, written once per job: `Graphics\Visuals vN\kits\BUILD RULES.md`, the job's distilled rules, real material, shared specs and hand-back format. Each builder prints only its own beats (`kitseats.py <ids>`) and never reads the plan, the brief or the Brain notes.
5. **Checks, quality first:** the scripted checks (lint, rawbreaks, identity, chain, NeoTextMotion range, blank tiles) **plus reviewer agents** wherever taste or readability is the question. Then a fix round.
6. MagicZoom pass, then sound per the last three finals.
7. Leave the timeline caching on the Edit page. No final render; delivery stays Samuel's call.
8. **Morning report** in the job note: what's built, what you're unsure of, what broke, which timeline to open. Send him a stills sheet (`SendUserFile`, proactive). Status `done` for this version.

His markers on version N are the brief for version N+1: read every one, track each to done.

## Usage

- Check the usage card (`get_usage`) before every wave.
- **Weekly cap:** Samuel wants the week used up, not wasted (2026-10-13: *"by the reset, I should be around 99% usage"*). Keep launching work until about 97 %, let what's running finish, then set `paused-weekly`. The first watchdog run after the reset resumes.
- **5-hour window:** at about 95 %, let running agents finish, set `paused-5h`. The watchdog resumes after the window resets.

## Resolve on an unattended night

- **Another session may be rendering.** Read the other jobs' `RESUME NOTE.md` in their final-render folders. Never queue, stop or switch projects while a render is running. Plan and build outside Resolve until it finishes.
- `DisableBackgroundTasksForCurrentResolveSession()` first in every scripted block. Restart without it at the end so the timeline caches.
- **Hung:** save by script if it answers, then `python 03-Areas/video-editing/scripts/restart_resolve.py` (Samuel, 2026-10-13: full permission). **Crashed:** the same script relaunches it. Then `GotoRootFolder` before `LoadProject`, reload the timeline, and note what was lost in the report.
- **Screen control** on Resolve is allowed for GUI-only steps while he is away (2026-10-13). It stops the moment he says he needs the PC.
- Permission prompts stall a night: no `Remove-Item` or `Stop-Process`. Leave temp files; the restart script is the only way to end Resolve.

Back to [[03-Areas/video-editing/video-editing|Video editing]]

## Hard rule: pace the agents (Samuel, 2026-10-15)
*"efficiency is a hard rule you must follow"*. Worker pool of 3-5 agents in every workflow; never fan out a whole job list at once. Usage card before every launch, expected cost written in RUN STATE (one agent ≈ 0.2-0.25 weekly points, a full 5-hour window ≈ 13). Pace each window to last 5 hours. Stop hung agents after ~30 min without progress. Why: [[07-Agents/video-editor/memory|Editor memory]] 2026-10-15.

**On Max 20x (2026-10-24, revised the same day to Samuel's order: speed, quality, efficiency, memory):** up to 14 helpers per workflow and two workflows at once when the work splits; the stop is the video's weekly budget, not a pool size. At most ~6 render through Resolve at once until the render queue exists. Pipeline, not waves. A fresh reviewer on every beat plus a section pass. The point figures above were measured on 5x; re-measure on the first 20x video. All rules: [[00-System/model-routing|model routing]] → On Max 20x.
