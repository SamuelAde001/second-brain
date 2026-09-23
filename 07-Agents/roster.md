---
type: agent
area: system
status: active
updated: 2026-09-23
source: interview
tags: [agents, roster]
---

# Agent roster

Every agent in the Brain. An agent owns a domain; a skill owns a job. The **orchestrator is the default entry point** and routes to specialists. Subagents report to the orchestrator, never to each other. Cross-domain work goes through [[handoffs]].

Each agent has a folder under `07-Agents/<name>/` with `profile.md` (mission, scope, permissions, limits), `memory.md` (append-only, what it has learned) and `log.md` (append-only, every action). An agent reads its own `profile.md` and `memory.md` before acting, and logs every action.

## Active

| Agent | Owns | Claude Code adapter | Tier | Status |
|-------|------|---------|-------|--------|
| **orchestrator** | Routing and merging. The default entry point, and the session protocol. Routes content work to the content agent. | none — it is the main session (`runs-as: main-session`) | `strong` | **built 2026-09-22** → [[07-Agents/orchestrator/profile\|profile]] |
| **video-editor** | The client editing work in DaVinci Resolve — the brief-to-delivery pipeline, and standing Resolve expertise. Samuel's most important agent. Keeps the [[03-Areas/video-editing/delivered-projects\|delivered projects]] record. | none — runs in the main session (`runs-as: main-session`) | `strong` | **skeleton built 2026-09-21** — step 6 (HTML→Fusion) proven; skills not yet built |
| **finance** | His financial manager: the money ledger, the budget sheet, the eight rules, pots, runway, budgets and the month close. Never moves money. | none — runs in the main session (`runs-as: main-session`) | `strong` | **built 2026-09-22** → [[07-Agents/finance/profile\|profile]] — skills `payday`, `budget`, `month-close`; sheet credentials pending |
| **personal-life** | His day and week, and his disciplinarian: holds him to his must-dos, client hours and deadlines and a 7:00am start, with escalation and a make-up rule. Plans tomorrow the night before, the 6:30am brief, the Sunday weekly review, TickTick and Google Calendar (full write), focus and habits. | none — runs in the main session (`runs-as: main-session`) | `strong` | **built 2026-09-22** → [[07-Agents/personal-life/profile\|profile]] — skills `night-plan`, `morning-brief`, `weekly-review`; three routines |
| **content** | His own brand, @SamuelSignals: ideas and hooks from his story bank, scripts in his voice, draft reviews, the content log, and the Sunday content report against 5,000 followers by December. Daily posting is reported, not enforced. Never posts. | none — runs in the main session (`runs-as: main-session`) | `strong` | **built 2026-09-22** → [[07-Agents/content/profile\|profile]] — skills `write-script`, `content-report` |

## Planned — not built

| Agent | Owns | Brief |
|-------|------|-------|
| — | Every planned agent is built. | — |

## Notes

- The **video-editor is the first agent built.** Its folder is the pattern the others follow.
- The **orchestrator is not a subagent.** It's the main session's role, because subagents can't launch subagents. Its profile has no generated adapter.
- **No agent is a subagent.** Samuel, 2026-09-23: *"I want all my agents to be Main, all of them should use OPUS 5.5, The only time I tell them to use something different is based on tasks"*. Every agent runs in the main session with its profile loaded, on Opus 5.5. A cheaper model or a subagent only when he asks for one on a given task.
- **Routines are not agents.** The morning brief and night plan run on Sonnet and hand a step to an agent when it needs one.
- **Profiles are canonical and model-neutral.** Any AI can run an agent by reading its profile and memory; a tool's native agent file is generated from the profile by `00-System/scripts/build_adapters.py` ([[00-System/portability|portability]]).
- Tier: every profile is `strong` (Opus 5.5), by Samuel's instruction of 2026-09-23. Cost is held down by scripts doing the bulk work, not by cheaper models.

Back to [[00-System/build-state|Build state]] · Constitution: [[AGENTS]] §7.
