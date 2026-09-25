---
type: knowledge
area: system
status: active
updated: 2026-09-22
source: manual
tags: [systems]
---

# Systems register

Every SOP, skill and automation in this Brain. If it is not here, it does not exist as a system.

The ladder, lowest rung first: **SOP → checklist → skill → automation.** When a task has come up twice, propose the lowest rung that actually works, and build it only once Samuel agrees.

## Agents

| Agent | Owns | Profile → generated adapter | Status |
|-------|------|---------|--------|
| **orchestrator** | Routing, merging, the session protocol. The default entry point | none — runs as the main session → [[07-Agents/orchestrator/profile\|profile]] | **built 2026-09-22** |
| **video-editor** | The DaVinci Resolve editing pipeline + standing Resolve expertise | `.claude/agents/video-editor.md` → [[07-Agents/video-editor/profile\|profile]] | **skeleton built 2026-09-21**; step 6 proven; skills pending |
| **finance** | Money: ledger, budget sheet, rules, pots, runway, month close. Never moves money | `.claude/agents/finance.md` → [[07-Agents/finance/profile\|profile]] | **built 2026-09-22**; sheet credentials pending |
| **personal-life** | His day and week, and his disciplinarian: night plan with a nightly accountability check, morning brief, weekly review; TickTick and Google Calendar (full write) | none — runs in the main session → [[07-Agents/personal-life/profile\|profile]] | **built 2026-09-22** |
| **content** | His own brand, @SamuelSignals: ideas, scripts in his voice, draft reviews, the content log, the Sunday content report | none — runs in the main session → [[07-Agents/content/profile\|profile]] | **built 2026-09-22** |

Roster and planned agents: [[07-Agents/roster|roster]].

## SOPs and checklists — in the Brain

| Name | Type | Owner agent | Lives at | Trigger | Last used | Status |
|------|------|-------------|----------|---------|-----------|--------|
| Script creation, raw idea → script | SOP | content | [[script-process]] | Samuel brings a raw story idea | unknown | active |
| Script review | checklist | content | [[script-review-checklist]] | He sends a script for review | unknown | active |
| Test a Scripnals APK | SOP | orchestrator | [[03-Areas/scripnals/sops/test-an-apk\|test-an-apk]] | The devs send a new APK | 2026-09-22 | active |
| Routerise cut workflow | SOP | video editing (Phase 4) | [[routerise-cut-workflow]] | A Routerise edit starts | unknown | active |
| Visual sheet pipeline | SOP + scripts (`scripts/visual-engine/`) | video editing | [[visual-sheet-pipeline]] | A cut is final and needs visuals | 2026-09-25 | active |

## Skills — in the Brain

Canonical copies live in `00-System/skills/<name>/<name>.md`, with scripts and assets beside them. Any AI can run them ([[00-System/portability|portability]]); Claude Code and Gemini CLI get generated copies in `.claude/skills/` and `.agents/skills/`. These four are **Samuel's own claude.ai skills** (`creatorType: user`), copied in 2026-09-22. The Brain copy is canonical; the claude.ai copies are adapters for chat on the phone and web — edit here, re-upload with `build_adapters.py --package`.

| Skill | What it does | Area | Files beside it |
|-------|--------------|------|-----------------|
| [[edit-clock]] | Standalone HTML pace widget kept beside Resolve: where the playhead should be now, time left, timeline needed per hour, ahead/behind. Reads WAT (UTC+1). **When Samuel asks for "a timer", this is what he means.** | [[03-Areas/video-editing/video-editing\|Video editing]] | `assets/edit-clock.html`, `scripts/pace.py`, `scripts/test_clock.js` |
| [[video-edit-pass]] | Two-phase edit-assist pass on a long-form talking-head cut: phase 1 reads subtitles + timeline XML and outputs a colour-coded marker EDL of what to cut; phase 2 builds a chaptered ALL-CAPS transcript plus chapter markers. | [[03-Areas/video-editing/video-editing\|Video editing]] | — |
| [[subtitle-transcript-formatter]] | Turns a raw SRT/VTT export into a clean, sectioned, ALL-CAPS .docx for editing from. | [[03-Areas/video-editing/video-editing\|Video editing]] | `scripts/build_docx.js` |
| [[yap-session-planner]] | Structures unscripted talk-to-camera content into a beat-by-beat outline to speak from. | [[03-Areas/personal-brand/personal-brand\|Personal brand]] | `references/frameworks.md` |

Verified 2026-09-22: `edit-clock`'s `pace.py` and its smoke test run from the Brain path, outside claude.ai.

**Finance skills**, rebuilt 2026-09-22 from the engine's rituals (legacy review R6–R8). Owner: the [[07-Agents/finance/profile|finance agent]]. `payday` and `budget` are conversations and run in the main session.

| Skill | What it does | Trigger | Last used | Status |
|-------|--------------|---------|-----------|--------|
| [[payday]] | Money landed: log it, mirror it to the sheet, then get the week-of-pay transfers and pots moved the same day (Rule 3) | He says he got paid | never | active |
| [[budget]] | Set or change a month's plan, one named line per item on Details, and say whether the arithmetic works | He wants to budget or change a line | never | active |
| [[month-close]] | What came in, went out, survived; Goal 1 pace; freeze the month's plan | Last day of the month, or he asks | never | active |
| [[money-check]] | Before an off-plan spend: which line pays, what's left after, the verdict in three lines | He asks "can I spend X?" (commitment, 2026-09-22) | never | active |
| [[sunday-check]] | Weekly: his balance → log the gap → name every line over plan, and what's left to payday | Every Sunday (commitment, 2026-09-22) | never | active |

**Personal-life skills**, built 2026-09-22 from Samuel's answers. Owner: the [[07-Agents/personal-life/profile|personal-life agent]]. All three are conversations and run in the main session.

| Skill | What it does | Trigger | Last used | Status |
|-------|--------------|---------|-----------|--------|
| [[night-plan]] | The nightly accountability check on his three commitments (must-dos, client deadlines and hours, 7:00am start), with escalation and the make-up rule. Then close out today, lay tomorrow onto his day in timed chunks (at most three must-dos), write it to TickTick and the calendar once he agrees, and keep a short daily note | 8:45pm routine, or "plan tomorrow" | never | active |
| [[morning-brief]] | Fixed times, must-dos, the client job and its deadline, anything overdue, in ten lines or fewer | 6:30am routine, or "what's on today" | never | active |
| [[weekly-review]] | Good week by his own bar, the numbers (must-dos, focus, habits, money line), what slipped and which pattern it matches, then next week planned with him | Sunday 3:00pm session, after [[sunday-check]] | never | active |

**Content skills**, built 2026-09-22 from Samuel's answers. Owner: the [[07-Agents/content/profile|content agent]]. Both run in the main session.

| Skill | What it does | Trigger | Last used | Status |
|-------|--------------|---------|-----------|--------|
| [[write-script]] | Raw idea → interview → hooks → script in his voice, or a review of his draft. Runs [[script-process]] and [[script-review-checklist]] | He brings an idea, a story or a draft | never | active |
| [[content-report]] | Days with a post out of 7, followers and pace to 5,000 by December, best and worst post. Logs his numbers; never estimates one | Sunday 3:00pm session, after the money check | never | active |

## Scripts

| Script | Job | Run |
|--------|-----|-----|
| `00-System/scripts/build_adapters.py` | Generates every AI tool's adapter files (Claude Code, Gemini CLI) from the canonical profiles and skills; `--check` detects drift; `--package` zips a skill for claude.ai | after any profile or skill edit |
| `00-System/scripts/build_scripnals_guides.py` | Validates the Scripnals guide library (`03-Areas/scripnals/guides/`), exports `_export/guides.json` + `vocab.json` for the devs, and shows what one request loads (`--select`, `--prompt`). `--check` fails if the export is stale | after any change to a guide entry |
| `00-System/scripts/build_scripnals_spec.py` | Builds the Scripnals AI spec PDF for the devs from `03-Areas/scripnals/ai-workflow.md`. `--figures` first re-draws the flow chart and screen mock-ups from `03-Areas/scripnals/assets/*.html`. Needs Chrome | after any change to the AI spec |
| `00-System/scripts/budget_sheet.py` | Rebuilds the "Money" Google Sheet (Overview, one tab per month, Ledger) from the money ledger, each month's plan and the goals, over Google's official Sheets API as a service account. `preview` prints it without touching the sheet, `doctor` checks the connection, `left` prints what's left per line this month (for `money-check`), `month-plan YYYY-MM` starts a month's plan from the standing plan, `freeze YYYY-MM` locks it at the close | after any ledger or plan change; `freeze` at every month close |
| `03-Areas/video-editing/scripts/drive_download.py` | Fast, resumable parallel-range download of a link-shared Drive file or any signed URL (Tella exports) | a new Routerise job's footage |
| `03-Areas/video-editing/scripts/md_to_docx.py` | Stock-Python Markdown → Word .docx for offline client briefs | saving a Notion idea doc offline |
| `03-Areas/video-editing/scripts/av_sync.py` | Sync offset between camera clip and DJI mic: camera-audio cross-correlation, motion fallback when the scratch audio is dead | when Resolve's waveform auto-sync fails |
| `00-System/scripts/sheets.py` | **Legacy since 2026-09-22; read the old sheet only.** Client for the Apps Script bridge to the "My Claude Budget" sheet: `ping`, `read`, `ops`, `doctor`, `flush`/`pending` for queued batches. Credentials from Windows user variables only ([[03-Areas/finances/budget-system\|budget system]]) | any sheet read or write |
| `00-System/scripts/money_ledger.py` | Read-only totals from the money ledger (`totals`, `pots`, `last`) and the delivered-projects record (`videos`) | instead of reading either file |
| `00-System/scripts/session_start_sync.py` | Fetches GitHub, fast-forwards `main` (only on `main`, only fast-forward), and lists any unmerged `claude/*` branches (a fallback: cloud sessions push to `main` since 2026-09-22). Never merges, deletes or resets; always exits 0 | automatically, by the SessionStart hook |
| `00-System/scripts/split_conversations.py` | Split the Claude chat export into one file per conversation (Phase 2 migration) | one-off, done |

## Job skills — not built yet

`brainstorm`, `plan`, `systemize`, `commit`. Built in Phase 4. (`money-check` and the finance rituals are built. See above.)

**The video-editor's job skills**, one per pipeline step ([[07-Agents/video-editor/profile|profile]]):

| Skill | Job | Plan |
|-------|-----|------|
| `routerise-cut` | Step 1 — cut from footage: sync → ripple silence → transcribe → remove bad takes. Encodes [[routerise-cut-workflow]]. | build |
| ideation / cut-sheet | Step 4 — a visual per sentence as a full HTML cut sheet. **The "existing ideation skill" from the brief does not exist** (decided 2026-09-21); build it. | build |
| `storyboard-preview` | Step 5 — approved storyboard as animated HTML/CSS for sign-off. | build |
| `html-to-fusion` | Step 6 — approved visuals → editable Fusion comps on the timeline. **Bridge proven 2026-09-21.** | build |

Reused as-is by the agent, not rebuilt: [[subtitle-transcript-formatter]] (step 3), [[video-edit-pass]] (step 2 / editorial), [[edit-clock]].

## Automations

| Automation | What it does | Schedule | Runs in | Canonical note | Status |
|---|---|---|---|---|---|
| Sunday money check + content report + weekly review | Opens a session that runs [[sunday-check]] (his balance, the gap logged, the sheet rebuilt, every line over plan), then [[content-report]], then [[weekly-review]] in the same session (merged, Samuel 2026-09-22) | Sundays 3:00pm WAT (`0 15 * * 0`) | Claude desktop app scheduled task `sunday-money-check`; needs the app open | [[00-System/automations/sunday-money-check\|sunday-money-check]] | active from 2026-09-27 |
| Night plan | Opens a session that runs [[night-plan]]: today closed out, tomorrow planned with him and written to TickTick | Daily 8:45pm WAT (cron `45 19 * * *` UTC) | claude.ai cloud routine `trig_01Pet8jENJ1CEguycgH9suEf`; runs with the PC off, shows on the phone (moved from the desktop app 2026-09-22) | [[00-System/automations/night-plan\|night-plan]] | active from 2026-09-22 |
| Brain sync on session start | Every Claude Code session on the PC opens by pulling what the phone (a cloud session) or anything else pushed to GitHub, and names any cloud branch still waiting to be merged | every session start, including the scheduled ones | Claude Code SessionStart hook in `.claude/settings.json` → `00-System/scripts/session_start_sync.py` | [[00-System/portability\|portability]] → Cloud sessions and the PC | active from 2026-09-22 |
| Morning brief | Opens a session that runs [[morning-brief]]: today in ten lines | Daily ~6:34am WAT (cron `30 5 * * *` UTC + ~4 min service delay) | claude.ai cloud routine `trig_01UN9y23v1UwoBtBq3qmoJiH`; runs with the PC off, shows on the phone (moved from the desktop app 2026-09-22) | [[00-System/automations/morning-brief\|morning-brief]] | active from 2026-09-23 |

The rest of the automations are Phase 6.

## Archived, not active

The legacy Accountability Engine's nine skills, its enforcer subagent and its automations are listed in [[legacy-review]], all `unreviewed`. None of them run.
