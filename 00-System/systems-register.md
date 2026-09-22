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

Roster and planned agents: [[07-Agents/roster|roster]].

## SOPs and checklists — in the Brain

| Name | Type | Owner agent | Lives at | Trigger | Last used | Status |
|------|------|-------------|----------|---------|-----------|--------|
| Script creation, raw idea → script | SOP | content (Phase 4) | [[script-process]] | Samuel brings a raw story idea | unknown | active |
| Script review | checklist | content (Phase 4) | [[script-review-checklist]] | He sends a script for review | unknown | active |
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

## Scripts

| Script | Job | Run |
|--------|-----|-----|
| `00-System/scripts/build_adapters.py` | Generates every AI tool's adapter files (Claude Code, Gemini CLI) from the canonical profiles and skills; `--check` detects drift; `--package` zips a skill for claude.ai | after any profile or skill edit |
| `00-System/scripts/split_conversations.py` | Split the Claude chat export into one file per conversation (Phase 2 migration) | one-off, done |

## Job skills — not built yet

`brainstorm`, `plan`, `money-check`, `systemize`, `commit`. Built in Phase 4.

**The video-editor's job skills**, one per pipeline step ([[07-Agents/video-editor/profile|profile]]):

| Skill | Job | Plan |
|-------|-----|------|
| `routerise-cut` | Step 1 — cut from footage: sync → ripple silence → transcribe → remove bad takes. Encodes [[routerise-cut-workflow]]. | build |
| ideation / cut-sheet | Step 4 — a visual per sentence as a full HTML cut sheet. **The "existing ideation skill" from the brief does not exist** (decided 2026-09-21); build it. | build |
| `storyboard-preview` | Step 5 — approved storyboard as animated HTML/CSS for sign-off. | build |
| `html-to-fusion` | Step 6 — approved visuals → editable Fusion comps on the timeline. **Bridge proven 2026-09-21.** | build |

Reused as-is by the agent, not rebuilt: [[subtitle-transcript-formatter]] (step 3), [[video-edit-pass]] (step 2 / editorial), [[edit-clock]].

## Automations — none

Nothing is scheduled. Phase 6.

## Archived, not active

The legacy Accountability Engine's nine skills, its enforcer subagent and its automations are listed in [[legacy-review]], all `unreviewed`. None of them run.
