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
| **video-editor** | The client editing work in DaVinci Resolve — the brief-to-delivery pipeline, and standing Resolve expertise. Samuel's most important agent. | generated → `.claude/agents/video-editor.md` | `standard`; `strong` for editorial judgement | **skeleton built 2026-09-21** — step 6 (HTML→Fusion) proven; skills not yet built |

## Planned — not built

| Agent | Owns | Brief |
|-------|------|-------|
| orchestrator | Routing and merging. The default entry point. | Phase 4 |
| finance | Categorise, summarise, runway, rule breaches, ledger + sheet writes, budget planning. A financial manager, not a logger. | [[03-Areas/finances/finance-agent-plan|Finance agent plan]] |
| personal-life | Tasks, schedule, focus — via TickTick. | Phase 4 |
| content | Script creation and review, brand content. | Phase 4 |

## Notes

- The **video-editor is the first agent built.** Its folder is the pattern the others follow.
- **Profiles are canonical and model-neutral.** Any AI can run an agent by reading its profile and memory; a tool's native agent file is generated from the profile by `00-System/scripts/build_adapters.py` ([[00-System/portability|portability]]).
- Tier per profile: cheapest that does the job well (`light` / `standard`); `strong` only for judgement-heavy work (editorial review, weekly synthesis).

Back to [[00-System/build-state|Build state]] · Constitution: [[AGENTS]] §7.
