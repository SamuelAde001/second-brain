---
type: sop
area: video-editing
status: active
updated: 2026-10-13
source: interview
tags: [sop, unattended, overnight, versions]
---

# Unattended run: a whole job while Samuel is away

Samuel, 2026-10-13: *"I want to be able to let Claude work from the beginning till the end while I go to sleep and wake up and just have to review what has been done, not me babysitting Claude on every part ... I want to do it all at once and have reviews in versions"*. Also: *"I am not bothered about token usage as long as you give me the best results"*. Quality first; cut only waste (re-studying what is written down, oversized sessions). Decision and the Editor's one objection: [[03-Areas/video-editing/video-editing-decisions|decisions]], 2026-10-13. **First run: LinkedIn Training, 2026-10-13. Untested until then; fold what breaks back into this note.**

## The pieces

- **Conductor:** one Claude Code session acting as the Editor, titled `Editor run: <job>`. It never waits on Samuel between steps. It stays small: the heavy work runs in Workflow agents, each with its own fresh context, returning short summaries (counts, paths). It reads only what the current step needs.
- **Run state:** `Docs\RUN STATE.md` in the job folder. Fields: `status` (running · paused-5h · paused-weekly · blocked · done), `step`, `version`, `updated` (ISO, WAT), `next`. The conductor rewrites it at every step change and before any pause. It is the first thing read on any wake.
- **RESUME block** in the job's Brain note: the step in progress, the next step, files and timelines touched. Rewritten at every step end and when the context guard fires at 160k. After a compaction the conductor reads it and carries on by itself.
- **Watchdog:** the scheduled task `editor-run-watchdog`, hourly. If a session titled `Editor run: <job>` is working, it does nothing. If that session is idle with the run unfinished, it messages it to continue. If there is no such session, the watchdog becomes the conductor (it retitles itself). It only resumes when the usage card has room. When `RUN STATE` says done, it disables itself. To point it at a new job, update its prompt.
- **Keep-awake** for the whole run (`request_keep_awake`, `session_idle`).

## The run, in order

Each pass ends on a **new timeline, `<Visuals vN> (Editor)`**, made from a backup. Never edit the last version Samuel reviewed.

1. Read the job note, the [[03-Areas/video-editing/edit-grammar/edit-grammar|edit grammar]], [[03-Areas/video-editing/routerise-house-style|house style]] §11b, [[03-Areas/video-editing/ways-of-working|ways of working]] → Revision rules. Do not re-study past videos.
2. **Visual plan** against the cut, at the density in the job note.
3. **Intro:** build it from Samuel's suggested visuals if they are in the job note or `Docs\`. Otherwise ideate it yourself and build it, marked as the Editor's own idea.
4. **Build waves:** 4-5 builders per wave, each owning 6-10 visuals. Briefs carry the rules from step 1 and the Resolve traps. Install each wave as soon as it lands.
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
