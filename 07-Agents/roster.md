---
type: agent
area: system
status: active
updated: 2026-09-21
source: interview
tags: [agents, roster]
---

# Agent roster

Every agent in the Brain. An agent owns a domain; a skill owns a job. The **orchestrator is the default entry point** and routes to specialists. Subagents report to the orchestrator, never to each other. Cross-domain work goes through [[handoffs]].

Each agent has a folder under `07-Agents/<name>/` with `profile.md` (mission, scope, permissions, limits), `memory.md` (append-only, what it has learned) and `log.md` (append-only, every action). An agent reads its own `profile.md` and `memory.md` before acting, and logs every action.

## Active

| Agent | Owns | Wrapper | Model | Status |
|-------|------|---------|-------|--------|
| **video-editor** | The client editing work in DaVinci Resolve — the brief-to-delivery pipeline, and standing Resolve expertise. Samuel's most important agent. | `.claude/agents/video-editor.md` | cheapest that does the job; strongest for editorial judgement | **skeleton built 2026-09-21** — step 6 (HTML→Fusion) proven; skills not yet built |

## Planned — not built

| Agent | Owns | Brief |
|-------|------|-------|
| orchestrator | Routing and merging. The default entry point. | Phase 4 |
| finance | Categorise, summarise, runway, rule breaches, ledger + sheet writes, budget planning. A financial manager, not a logger. | [[03-Areas/finances/finance-agent-plan|Finance agent plan]] |
| personal-life | Tasks, schedule, focus — via TickTick. | Phase 4 |
| content | Script creation and review, brand content. | Phase 4 |

## Notes

- The **video-editor is the first agent built.** Its folder is the pattern the others follow.
- Model choice per CLAUDE.md: cheapest model that does the job well; reserve the strongest model for judgement-heavy work (editorial review, weekly synthesis).

Back to [[00-System/build-state|Build state]] · Constitution: [[AGENTS]] §7.
