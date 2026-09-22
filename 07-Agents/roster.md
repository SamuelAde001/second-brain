---
type: agent
area: system
status: active
updated: 2026-09-22
source: interview
tags: [agents, roster]
---

# Agent roster

Every agent in the Brain. An agent owns a domain; a skill owns a job. The **orchestrator is the default entry point** and routes to specialists. Subagents report to the orchestrator, never to each other. Cross-domain work goes through [[handoffs]].

Each agent has a folder under `07-Agents/<name>/` with `profile.md` (mission, scope, permissions, limits), `memory.md` (append-only, what it has learned) and `log.md` (append-only, every action). An agent reads its own `profile.md` and `memory.md` before acting, and logs every action.

## Active

| Agent | Owns | Claude Code adapter | Tier | Status |
|-------|------|---------|-------|--------|
| **orchestrator** | Routing and merging. The default entry point, and the session protocol. Works the personal-life and content domains itself until those agents exist. | none — it is the main session (`runs-as: main-session`) | `strong` | **built 2026-09-22** → [[07-Agents/orchestrator/profile\|profile]] |
| **video-editor** | The client editing work in DaVinci Resolve — the brief-to-delivery pipeline, and standing Resolve expertise. Samuel's most important agent. Keeps the [[03-Areas/video-editing/delivered-projects\|delivered projects]] record. | generated → `.claude/agents/video-editor.md` | `standard`; `strong` for editorial judgement | **skeleton built 2026-09-21** — step 6 (HTML→Fusion) proven; skills not yet built |
| **finance** | His financial manager: the money ledger, the budget sheet, the eight rules, pots, runway, budgets and the month close. Never moves money. | generated → `.claude/agents/finance.md`; conversations run in the main session | `standard` | **built 2026-09-22** → [[07-Agents/finance/profile\|profile]] — skills `payday`, `budget`, `month-close`; sheet credentials pending |

## Planned — not built

| Agent | Owns | Brief |
|-------|------|-------|
| personal-life | Tasks, schedule, focus — via TickTick. | Phase 4 |
| content | Script creation and review, brand content. | Phase 4 |

## Notes

- The **video-editor is the first agent built.** Its folder is the pattern the others follow.
- The **orchestrator is not a subagent.** It's the main session's role, because subagents can't launch subagents. Its profile has no generated adapter.
- **Profiles are canonical and model-neutral.** Any AI can run an agent by reading its profile and memory; a tool's native agent file is generated from the profile by `00-System/scripts/build_adapters.py` ([[00-System/portability|portability]]).
- Tier per profile: cheapest that does the job well (`light` / `standard`); `strong` only for judgement-heavy work (editorial review, weekly synthesis).

Back to [[00-System/build-state|Build state]] · Constitution: [[AGENTS]] §7.
