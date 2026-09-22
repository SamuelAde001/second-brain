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

Roster and planned agents: [[07-Agents/roster|roster]].

## SOPs and checklists — in the Brain

| Name | Type | Owner agent | Lives at | Trigger | Last used | Status |
|------|------|-------------|----------|---------|-----------|--------|
| Script creation, raw idea → script | SOP | content (Phase 4) | [[script-process]] | Samuel brings a raw story idea | unknown | active |
| Script review | checklist | content (Phase 4) | [[script-review-checklist]] | He sends a script for review | unknown | active |
| Test a Scripnals APK | SOP | orchestrator | [[03-Areas/scripnals/sops/test-an-apk\|test-an-apk]] | The devs send a new APK | 2026-09-22 | active |
| Routerise cut workflow | SOP | video editing (Phase 4) | [[routerise-cut-workflow]] | A Routerise edit starts | unknown | active |

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

## Scripts

| Script | Job | Run |
|--------|-----|-----|
| `00-System/scripts/build_adapters.py` | Generates every AI tool's adapter files (Claude Code, Gemini CLI) from the canonical profiles and skills; `--check` detects drift; `--package` zips a skill for claude.ai | after any profile or skill edit |
| `00-System/scripts/build_scripnals_guides.py` | Validates the Scripnals guide library (`03-Areas/scripnals/guides/`), exports `_export/guides.json` + `vocab.json` for the devs, and shows what one request loads (`--select`, `--prompt`). `--check` fails if the export is stale | after any change to a guide entry |
| `00-System/scripts/build_scripnals_spec.py` | Builds the Scripnals AI spec PDF for the devs from `03-Areas/scripnals/ai-workflow.md`. `--figures` first re-draws the flow chart and screen mock-ups from `03-Areas/scripnals/assets/*.html`. Needs Chrome | after any change to the AI spec |
| `00-System/scripts/budget_sheet.py` | Rebuilds the "Money" Google Sheet (Overview, one tab per month, Ledger) from the money ledger, each month's plan and the goals, over Google's official Sheets API as a service account. `preview` prints it without touching the sheet, `doctor` checks the connection, `left` prints what's left per line this month (for `money-check`), `month-plan YYYY-MM` starts a month's plan from the standing plan, `freeze YYYY-MM` locks it at the close | after any ledger or plan change; `freeze` at every month close |
| `00-System/scripts/sheets.py` | **Legacy since 2026-09-22; read the old sheet only.** Client for the Apps Script bridge to the "My Claude Budget" sheet: `ping`, `read`, `ops`, `doctor`, `flush`/`pending` for queued batches. Credentials from Windows user variables only ([[03-Areas/finances/budget-system\|budget system]]) | any sheet read or write |
| `00-System/scripts/money_ledger.py` | Read-only totals from the money ledger (`totals`, `pots`, `last`) and the delivered-projects record (`videos`) | instead of reading either file |
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
| Sunday money check | Opens a session that runs [[sunday-check]]: asks for his balance, logs the gap, rebuilds the sheet, names every line over plan | Sundays 3:00pm WAT (`0 15 * * 0`) | Claude desktop app scheduled task `sunday-money-check`; needs the app open | [[00-System/automations/sunday-money-check\|sunday-money-check]] | active from 2026-09-27 |

The rest of the automations are Phase 6.

## Archived, not active

The legacy Accountability Engine's nine skills, its enforcer subagent and its automations are listed in [[legacy-review]], all `unreviewed`. None of them run.
