---
type: knowledge
area: system
status: active
updated: 2026-09-20
source: manual
tags: [systems]
---

# Systems register

Every SOP, skill and automation in this vault. If it is not here, it does not exist as a system.

The ladder, lowest rung first: **SOP → checklist → skill → automation.** When a task has come up twice, propose the lowest rung that actually works, and build it only once Samuel agrees.

## SOPs and checklists — in the vault

| Name | Type | Owner agent | Lives at | Trigger | Last used | Status |
|------|------|-------------|----------|---------|-----------|--------|
| Script creation, raw idea → script | SOP | content (Phase 4) | [[script-process]] | Samuel brings a raw story idea | unknown | active |
| Script review | checklist | content (Phase 4) | [[script-review-checklist]] | He sends a script for review | unknown | active |
| Routerise cut workflow | SOP | video editing (Phase 4) | [[routerise-cut-workflow]] | A Routerise edit starts | unknown | active |

## Skills — exist, but not in this vault

These four are **platform-provided plugin skills**, invoked by name in Claude Code. They are not files under `.claude/skills/`, and they are not on disk anywhere on this PC — so they could not be copied into the vault during migration.

| Skill | What it does | Area |
|-------|--------------|------|
| `edit-clock` | Standalone HTML pace widget kept beside Resolve: where the playhead should be now, time left, timeline needed per hour, ahead/behind. Reads WAT (UTC+1). **When Samuel asks for "a timer", this is what he means.** | [[03-Areas/video-editing/_index\|Video editing]] |
| `video-edit-pass` | Two-phase edit-assist pass on a long-form talking-head cut: phase 1 reads subtitles + timeline XML and outputs a colour-coded marker EDL of what to cut; phase 2 builds a chaptered ALL-CAPS transcript plus chapter markers. | [[03-Areas/video-editing/_index\|Video editing]] |
| `subtitle-transcript-formatter` | Turns a raw SRT/VTT export into a clean, sectioned, ALL-CAPS .docx for editing from. | [[03-Areas/video-editing/_index\|Video editing]] |
| `yap-session-planner` | Structures unscripted talk-to-camera content into a beat-by-beat outline to speak from. | [[03-Areas/personal-brand/_index\|Personal brand]] |

**Portability gap:** AGENTS.md §8 says skills are plain-markdown files any model can read. These four are not, so Gemini CLI cannot run them. Phase 7 decides whether to author vault-local equivalents. Logged as an open question.

## Job skills — not built yet

`brainstorm`, `plan`, `money-check`, `systemize`, `commit`, plus the editing job skills defined in the Phase 3 video-editing interview. Built in Phase 4.

## Automations — none

Nothing is scheduled. Phase 6.

## Archived, not active

The legacy Accountability Engine's nine skills, its enforcer subagent and its automations are listed in [[legacy-review]], all `unreviewed`. None of them run.
