---
type: knowledge
area: system
status: active
updated: 2026-09-28
source: manual
tags: [systems]
---

# Systems register

Every SOP, skill and automation in this Brain. If it is not here, it does not exist as a system.

The ladder, lowest rung first: **SOP → checklist → skill → automation.** When a task has come up twice, propose the lowest rung that actually works, and build it only once Samuel agrees.

## Agents

| Agent | Owns | Profile → generated adapter | Status |
|-------|------|---------|--------|
| **orchestrator** (General Manager) | Routing, merging, the session protocol. The default entry point | none — runs as the main session → [[07-Agents/orchestrator/profile\|profile]] | **built 2026-09-22** |
| **video-editor** (Editor) | The DaVinci Resolve editing pipeline + standing Resolve expertise | none — runs in the main session → [[07-Agents/video-editor/profile\|profile]] | **built 2026-09-21**, in daily use on Route Rise jobs; runs from SOPs, scripts and small skills (2026-09-28) |
| **finance** (Money man) | Money: ledger, budget sheet, rules, pots, runway, month close. Never moves money | none — runs in the main session → [[07-Agents/finance/profile\|profile]] | **built 2026-09-22**; Money sheet connected 2026-09-22 |
| **personal-life** (PA) | His day and week, and his disciplinarian: night plan with a nightly accountability check, morning brief, weekly review; TickTick and Google Calendar (full write) | none — runs in the main session → [[07-Agents/personal-life/profile\|profile]] | **built 2026-09-22** |
| **content** (Brand manager) | His own brand, @SamuelSignals: ideas, scripts in his voice, draft reviews, the content log, the Sunday content report | none — runs in the main session → [[07-Agents/content/profile\|profile]] | **built 2026-09-22** |

No agent has a generated subagent adapter since 2026-09-23: all five run in the main session on Opus 5.5, with model and effort per job from [[00-System/model-routing|model routing]] (2026-09-29). Roster and planned agents: [[07-Agents/roster|roster]].

## SOPs and checklists — in the Brain

| Name | Type | Owner agent | Lives at | Trigger | Last used | Status |
|------|------|-------------|----------|---------|-----------|--------|
| Script creation, raw idea → script | SOP | content | [[script-process]] | Samuel brings a raw story idea | unknown | active |
| Script review | checklist | content | [[script-review-checklist]] | He sends a script for review | unknown | active |
| Test a Scripnals APK | SOP | orchestrator | [[03-Areas/scripnals/sops/test-an-apk\|test-an-apk]] | The devs send a new APK | 2026-09-22 | active |
| Routerise cut workflow | SOP | video-editor | [[routerise-cut-workflow]] | A Routerise edit starts | 2026-09-24 | active |
| Visual sheet pipeline | SOP + scripts (`scripts/visual-engine/`) | video-editor | [[visual-sheet-pipeline]] | A cut is final and needs visuals | 2026-09-25 | active |
| End-of-job review | SOP | video-editor | [[end-of-job-review]] | A job is delivered | never (first: Route Rise #3) | active |

## Skills — in the Brain

Canonical copies live in `00-System/skills/<name>/<name>.md`, with scripts and assets beside them. Any AI can run them ([[00-System/portability|portability]]); Claude Code and Gemini CLI get generated copies in `.claude/skills/` and `.agents/skills/`. These four are **Samuel's own claude.ai skills** (`creatorType: user`), copied in 2026-09-22. The Brain copy is canonical; the claude.ai copies are adapters for chat on the phone and web — edit here, re-upload with `build_adapters.py --package`.

| Skill | What it does | Area | Files beside it |
|-------|--------------|------|-----------------|
| [[edit-clock]] | Standalone HTML pace widget kept beside Resolve: where the playhead should be now, time left, timeline needed per hour, ahead/behind. Reads WAT (UTC+1). **When Samuel asks for "a timer", this is what he means.** | [[03-Areas/video-editing/video-editing\|Video editing]] | `assets/edit-clock.html`, `scripts/pace.py`, `scripts/test_clock.js`, `scripts/resolve_bridge.py` (live mode: reads the Resolve playhead, 2026-10-02) |
| [[video-edit-pass]] | Two-phase edit-assist pass on a long-form talking-head cut: phase 1 reads subtitles + timeline XML and outputs a colour-coded marker EDL of what to cut; phase 2 builds a chaptered ALL-CAPS transcript plus chapter markers. | [[03-Areas/video-editing/video-editing\|Video editing]] | — |
| [[subtitle-transcript-formatter]] | Turns a raw SRT/VTT export into a clean, sectioned, ALL-CAPS .docx for editing from. | [[03-Areas/video-editing/video-editing\|Video editing]] | `scripts/build_docx.js` |
| [[yap-session-planner]] | Structures unscripted talk-to-camera content into a beat-by-beat outline to speak from. | [[03-Areas/personal-brand/personal-brand\|Personal brand]] | `references/frameworks.md` |

Verified 2026-09-22: `edit-clock`'s `pace.py` and its smoke test run from the Brain path, outside claude.ai.

**Finance skills**, rebuilt 2026-09-22 from the engine's rituals (legacy review R6–R8). Owner: the [[07-Agents/finance/profile|finance agent]]. `payday` and `budget` are conversations and run in the main session.

| Skill | What it does | Trigger | Last used | Status |
|-------|--------------|---------|-----------|--------|
| [[payday]] | Money landed: log it, mirror it to the sheet, then get the week-of-pay transfers and pots moved the same day (Rule 3) | He says he got paid | never (first: the September 70%) | active |
| [[budget]] | Set or change a month's plan, one named line per item on Details, and say whether the arithmetic works | He wants to budget or change a line | 2026-09-25 | active |
| [[month-close]] | What came in, went out, survived; Goal 1 pace; freeze the month's plan | Last day of the month, or he asks | never (first: 2026-09-30) | active |
| [[money-check]] | Before an off-plan spend: which line pays, what's left after, the verdict in three lines | He asks "can I spend X?" (commitment, 2026-09-22) | 2026-09-25 | active |
| [[sunday-check]] | Weekly: his balance → log the gap → name every line over plan, and what's left to payday | Every Sunday (commitment, 2026-09-22) | 2026-09-27 | active |

**Personal-life skills**, built 2026-09-22 from Samuel's answers. Owner: the [[07-Agents/personal-life/profile|personal-life agent]]. All three are conversations and run in the main session.

| Skill | What it does | Trigger | Last used | Status |
|-------|--------------|---------|-----------|--------|
| [[night-plan]] | The nightly accountability check on his three commitments (must-dos, client deadlines and hours, 7:00am start), with escalation and the make-up rule. Then close out today, lay tomorrow onto his day in timed chunks (at most three must-dos), write it to TickTick and the calendar once he agrees, and keep a short daily note | 8:45pm routine, or "plan tomorrow" | 2026-09-27 | active |
| [[morning-brief]] | Fixed times, must-dos, the client job and its deadline, anything overdue, in ten lines or fewer | 6:30am routine, or "what's on today" | 2026-09-27 | active |
| [[weekly-review]] | Good week by his own bar, the numbers (must-dos, focus, habits, money line), what slipped and which pattern it matches, then next week planned with him | Sunday 3:00pm session, after [[sunday-check]] | 2026-09-27 | active |

**Content skills**, built 2026-09-22 from Samuel's answers. Owner: the [[07-Agents/content/profile|content agent]]. Both run in the main session.

| Skill | What it does | Trigger | Last used | Status |
|-------|--------------|---------|-----------|--------|
| [[write-script]] | Raw idea → interview → hooks → script in his voice, or a review of his draft. Runs [[script-process]] and [[script-review-checklist]] | He brings an idea, a story or a draft | no log entry yet | active |
| [[content-report]] | Days with a post out of 7, followers and pace to 5,000 by December, best and worst post. Logs his numbers; never estimates one | Sunday 3:00pm session, after the money check | 2026-09-27 | active |

## Scripts

| Script | Job | Run |
|--------|-----|-----|
| `00-System/scripts/build_adapters.py` | Generates every AI tool's adapter files (Claude Code, Gemini CLI) from the canonical profiles and skills; `--check` detects drift; `--package` zips a skill for claude.ai | after any profile or skill edit |
| `00-System/scripts/build_scripnals_guides.py` | Validates the Scripnals guide library (`03-Areas/scripnals/guides/`), exports `_export/guides.json` + `vocab.json` for the devs, and shows what one request loads (`--select`, `--prompt`). `--check` fails if the export is stale | after any change to a guide entry |
| `00-System/scripts/build_scripnals_spec.py` | Builds the Scripnals AI spec PDF for the devs from `03-Areas/scripnals/ai-workflow.md`. `--figures` first re-draws the flow chart and screen mock-ups from `03-Areas/scripnals/assets/*.html`. Needs Chrome | after any change to the AI spec |
| `00-System/scripts/budget_sheet.py` | Rebuilds the "Money" Google Sheet (Overview, one tab per month, Ledger) from the money ledger, each month's plan and the goals, over Google's official Sheets API as a service account. `preview` prints it without touching the sheet, `doctor` checks the connection, `left` prints what's left per line this month (for `money-check`), `month-plan YYYY-MM` starts a month's plan from the standing plan, `freeze YYYY-MM` locks it at the close | after any ledger or plan change; `freeze` at every month close |
| `03-Areas/video-editing/scripts/drive_download.py` | Fast, resumable parallel-range download of a link-shared Drive file or any signed URL (Tella exports) | a new Routerise job's footage |
| `03-Areas/video-editing/scripts/md_to_docx.py` | Stock-Python Markdown → Word .docx for offline client briefs | saving a Notion idea doc offline |
| `03-Areas/video-editing/scripts/transcript_docx.py` | Timecoded ALL-CAPS editing transcript .docx from a JSON spec (video-edit-pass phase 2 format) | building a cut's transcript |
| `03-Areas/video-editing/scripts/waveform_segments.py` · `noise_clips.py` | Speech segments from the mic's 5 ms peaks; finds leftover room-noise clips after Ripple Delete Silence | cutting A-roll by waveform |
| `03-Areas/video-editing/scripts/resolve_cache_watch.py` · `resolve_crash_dump.py` | Watch render-cache progress per clip; read Resolve crash dumps (exception, module) | a heavy cache or a crash |
| `03-Areas/video-editing/scripts/chrome_grab.ps1` · `chrome_seq.ps1` · `fusion_view.ps1` | Full-resolution shots of Samuel's Chrome (still or a scroll as frames); a picture of Resolve's current viewer without touching the comp | real UI shots; checking a comp |
| `03-Areas/video-editing/scripts/fusion-box/` | Generators for Fusion comps by script (tool boxes, circle pills, window stack, Neo Anim, bevel card) | building motion graphics in Fusion |
| `03-Areas/video-editing/motion-gallery/build_review.py` | Builds a job's visual review page from the job's `review.json` + `scenes-*.js`, using the gallery's engine and `src/parts.js`. Every sentence of the cut in order, each visual animated in time with the words and a live caption, approve/change/drop + comment copied back to chat. `--stills --t=end\|mid` renders a QA still per visual with headless Chrome | a job's visual review |
| `03-Areas/video-editing/motion-gallery/build_gallery.py` | Builds the Motion gallery page (39 animated designs from `src/`, reference frames and an A-roll still inlined); `--stills --t=3.8 [--only=P01,B02]` renders one still per design with headless Chrome for QA | adding or changing a gallery design; a review round |
| `03-Areas/video-editing/scripts/ui-focus/` | Zoom, darken and highlight on adjustment clips for UI demos, built through the Resolve API (README beside it) | a UI demo or screen recording |
| `03-Areas/video-editing/scripts/av_sync.py` | Sync offset between camera clip and DJI mic: camera-audio cross-correlation, motion fallback when the scratch audio is dead | when Resolve's waveform auto-sync fails |
| `08-Archive/retired-scripts/sheets.py` | **Retired; archived 2026-09-28. Reads the old sheet only.** Client for the Apps Script bridge to the "My Claude Budget" sheet: `ping`, `read`, `ops`, `doctor`, `flush`/`pending` for queued batches. Credentials from Windows user variables only ([[03-Areas/finances/budget-system\|budget system]]) | any sheet read or write |
| `00-System/scripts/screen_time.py` | Reads StayFree's local data (PC apps, plus phone and Chrome sessions synced into its cache) from a temp copy and writes `06-Logs/screen-time/<date>.md`: social media by app and hour, 11pm–7am, and each session's times (background Chrome tabs excluded). `--check "HH:MM-HH:MM,…"` gives minutes inside work blocks. No flags prints today | 8:30pm by Task Scheduler ([[00-System/automations/screen-time\|screen time]]); by hand any time |
| `00-System/scripts/money_ledger.py` | Read-only totals from the money ledger (`totals`, `pots`, `last`) and the delivered-projects record (`videos`) | instead of reading either file |
| `00-System/scripts/session_start_sync.py` | Fetches GitHub, fast-forwards `main` (only on `main`, only fast-forward), lists any unmerged `claude/*` branches (a fallback: cloud sessions push to `main` since 2026-09-22), and names any `[gemini]` commits since Claude's last. Never merges, deletes or resets; always exits 0 | automatically, by the SessionStart hook |
| `00-System/scripts/relay.py` | `brief --from claude\|gemini`: prints what the other AI's latest session was doing (Samuel's last asks, its last replies and actions, files touched) plus uncommitted changes and recent commits. Reads the transcripts read-only, writes nothing ([[00-System/relay\|relay]]) | by Gemini's `/relay`; by Claude when Gemini did work |
| `00-System/scripts/ask_gemini.py` | Hands a job to Gemini CLI headless and prints its answer. Read-only by default; `--write` allows file edits, never commands or commits ([[00-System/relay\|relay]]) | by Claude, for reading-heavy jobs |
| `08-Archive/retired-scripts/split_conversations.py` | Split the Claude chat export into one file per conversation (Phase 2 migration). Archived 2026-09-28 | one-off, done |

## How the Editor's pipeline runs — no pipeline skills

`brainstorm`, `plan`, `systemize` and `commit` were **dropped 2026-09-28**, and so were the Editor's planned pipeline skills (`routerise-cut`, cut-sheet, `storyboard-preview`, `html-to-fusion`). Samuel: *"The editor pipeline is still learning, I can't turn it to a skill yet cause I constantly still make changes, and nothing is really the same for now, I think the best is editor has SOP's and small skills for repeated specific tasks, and scripts he uses"*. The Editor works from:

| Step | Runs from |
|------|-----------|
| Job setup, cut | [[routerise-job-setup]] · [[routerise-cut-workflow]] SOPs; `av_sync.py`, `waveform_segments.py`, `noise_clips.py`, `transcript_docx.py` |
| Visual per sentence, preview | [[visual-sheet-pipeline]] SOP; `scripts/visual-engine/` |
| Fusion comps on the timeline | `scripts/fusion-box/`, `scripts/ui-focus/`; [[03-Areas/video-editing/resolve-automation-lessons\|Resolve automation lessons]] |

A small skill gets built only when a specific task repeats the same way (the ladder at the top of this note). [[00-System/decisions|Decision]], 2026-09-28.

Reused as-is by the agent, not rebuilt: [[subtitle-transcript-formatter]] (step 3), [[video-edit-pass]] (step 2 / editorial), [[edit-clock]].

## Automations

| Automation | What it does | Schedule | Runs in | Canonical note | Status |
|---|---|---|---|---|---|
| Sunday money check + content report + weekly review | Opens a session that runs [[sunday-check]] (his balance, the gap logged, the sheet rebuilt, every line over plan), then [[content-report]], then [[weekly-review]] in the same session (merged, Samuel 2026-09-22) | Sundays 3:00pm WAT (`0 15 * * 0`) | Claude desktop app scheduled task `sunday-money-check`; needs the app open | [[00-System/automations/sunday-money-check\|sunday-money-check]] | active from 2026-09-27 |
| Night plan | Opens a session that runs [[night-plan]]: today closed out, tomorrow planned with him and written to TickTick | Daily 8:45pm WAT (cron `45 19 * * *` UTC) | claude.ai cloud routine `trig_01Pet8jENJ1CEguycgH9suEf`; runs with the PC off, shows on the phone (moved from the desktop app 2026-09-22) | [[00-System/automations/night-plan\|night-plan]] | active from 2026-09-22 |
| Brain sync on session start | Every Claude Code session on the PC opens by pulling what the phone (a cloud session) or anything else pushed to GitHub, and names any cloud branch still waiting to be merged | every session start, including the scheduled ones | Claude Code SessionStart hook in `.claude/settings.json` → `00-System/scripts/session_start_sync.py` | [[00-System/portability\|portability]] → Cloud sessions and the PC | active from 2026-09-22 |
| Screen time | Writes today's StayFree screen time into the Brain and pushes it, for the night plan's social media check | Daily 8:30pm WAT | Windows Task Scheduler on the PC, task "Brain - screen time"; plain Python, no AI; needs the PC on | [[00-System/automations/screen-time\|screen-time]] | active from 2026-09-28 |
| Morning brief | Opens a session that runs [[morning-brief]]: today in ten lines | Daily ~6:34am WAT (cron `30 5 * * *` UTC + ~4 min service delay) | claude.ai cloud routine `trig_01UN9y23v1UwoBtBq3qmoJiH`; runs with the PC off, shows on the phone (moved from the desktop app 2026-09-22) | [[00-System/automations/morning-brief\|morning-brief]] | active from 2026-09-23 |

The rest of the automations are Phase 6.

## Archived, not active

The legacy Accountability Engine's nine skills, its enforcer subagent and its automations are listed in [[legacy-review]], all `unreviewed`. None of them run.
