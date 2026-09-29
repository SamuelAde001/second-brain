---
type: agent
area: system
status: active
updated: 2026-09-22
source: manual
tags: [agent, log]
---

# orchestrator — log

Append-only. Every action this agent takes, dated, newest at the bottom.

---

- 2026-09-22 — Profile, memory and log created (Phase 4). Runs as the main session: `runs-as: main-session`, so no subagent adapter is generated.
- 2026-09-22 — Before the profile existed, ran the last Phase 3 interviews as the main session: scripnals, academy, community + highsignals, book, and the `02-Me` gaps. Read three Scripnals architecture PDFs outside the Brain, a one-off read Samuel approved in chat. A credential-named file in the same folder was flagged, not opened.
- 2026-09-22 — Scripnals session run as the orchestrator (the Scripnals area is its own domain). Installed and walked the APK on BlueStacks over ADB. Read the PRD and master doc with Samuel's go-ahead. Wrote current-build, ai-workflow (spec v1), dev-bug-list, guide-library-brief, roadmap and sops/test-an-apk. Added `00-System/scripts/build_scripnals_spec.py`. Commits d44bcd8..HEAD.
- 2026-09-22 — Scripnals guide library session. Web research (Instagram's own ranking and recommendation pages, Mosseri via Social Media Today, Meta's engagement-bait rules, Kallaway, Socialinsider, Parker/Stone). Wrote `guide-library-research.md`, 66 entries in `guides/`, `guide-library.md`, `00-System/scripts/build_scripnals_guides.py`. Spec to v1.1 (Proposed), mock-ups and flow chart edited, PDF v1.1 built. Open questions 75–80.
- 2026-09-22 — Applied Samuel's review of the guide library: merged niches and formats into one note each, rewrote all 51 entries terse, added "guides are advice" to the master prompt and core-voice, reverted the panel mock-up and flow chart, rebuilt spec PDF v1.1. Closed open questions 75, 76, 78, 79; 80 partly.
- 2026-09-22 — Built the finance agent (profile, memory, log, skills `payday` / `budget` / `month-close`, live ledger, ledger script, sheet client ported). Routed the delivered-projects backfill to the video-editor subagent: 17 rows, 15 unnamed. Closed open questions 61 and 62; opened 81. Recorded Samuel sending the Scripnals guides to the devs.
- 2026-09-22 — Built the personal-life agent from Samuel's six answers and three routine times. Read TickTick (habits, focus, tasks, preference) and the Google Calendar list live, no writes. Created scheduled tasks `night-plan` and `morning-brief`, extended `sunday-money-check` with the weekly review, and offset the crons for the app's per-task delay. Updated roster, routing, the TickTick map, portability, AGENTS.md §7–8, the register, decisions and open questions.
- 2026-09-22 — Samuel asked for personal-life to be a disciplinarian and accountability checker. Asked him four questions (what, how hard, cost, check-ins), then built it: commitments, profile, the three skills, the night-plan routine, stakes note, decision.
- 2026-09-22 — Samuel answered the habits, gym-days and HighSignals-calendar questions. Habit fixed in TickTick; routine, health, profile, memory, night-plan, weekly-review, TickTick map updated; open questions 83–84 closed.
- 2026-09-28 — Tidy at Samuel's word ("Tidy"), 7 commits: build-state cut to 51 lines (history → `build-history.md`); retired scripts → `08-Archive/retired-scripts/`; systems register corrected from the logs; decisions 2026-09-20..22 and the Editor's technical lessons moved verbatim to their own notes; two open questions closed on evidence; orphans linked; inbox note filed. Three deletions and the two remote-branch deletions were refused by the auto-mode classifier and are left for Samuel. `ui-focus/` kept: it's a live tool, not trash.
- 2026-09-28 — Samuel dropped the four job skills and the Editor's pipeline skills ("Drop them"; the pipeline still changes). Decision recorded; AGENTS.md §8, systems register, Editor profile and build-state updated. Phase 4 closed.
- 2026-09-28 — End-of-job review for the Editor, on Samuel's yes: SOP, profile trigger, Runs counts on the SOPs, register row, decision.

Back to [[07-Agents/orchestrator/profile|Profile]]
- 2026-09-22 — At Samuel's request: created cloud routines for the morning brief and night plan, paused the desktop tasks, and allowed the routines' tools in `.claude/settings.json` (deletes still ask). Automation notes, register, decisions and build-state updated.
- 2026-09-23 — Samuel got no phone notification from the morning brief. Run had succeeded; no push was ever sent. Added a PushNotification step to both cloud routines (prompt + allowed tools) and their canonical notes; test run requested the push.
- 2026-09-23 — At Samuel's request: all five agents set to main session and tier `strong` (Opus 5.5); video-editor and finance adapters pruned; project default model set; routines kept on Sonnet with a hand-off-to-agent step. Decision logged.
- 2026-09-23 — Agent names added (General Manager, Editor, Money man, PA, Brand manager) and the always-name-the-working-agent rule written into AGENTS.md §7, roster, routing, CLAUDE.md. Decision logged.
- 2026-09-24 — Samuel asked to write in the Brain himself through Obsidian. Pick-up of his edits written into AGENTS.md rule 8 and §12 and portability; decision logged.
- 2026-09-24 — At Samuel's question about colours: added 13 graph colour groups (one per area/folder) to `.obsidian/graph.json`.
- 2026-09-24 — Graph colours were overwritten by the open Obsidian; rewritten after Samuel closed it, via a wait-for-exit watcher. Graph search now hides `01-Inbox/_imports` (334 unlinked migration files). Lesson in memory.
- 2026-09-28 — Brain health audit at Samuel's request, by script (no files read into context beyond build-state, registers and log tails). 282 notes. Links clean (1 real broken link). Found: build-state, systems register and open questions stale; decisions.md and video-editor memory over the size rule; handoffs unused; Phase 4 job skills untouched since 2026-09-22; trash candidates listed to Samuel. Nothing changed or deleted; tidy waits for his yes.
- 2026-09-29 — At Samuel's request, mapped every agent job, skill and routine to a model and effort level. Checked live: plan usage, the last 40 sessions (about 22 Editor), the session start-up load (~70k tokens), Claude Code's skill model/effort/fork fields and API prices. Wrote [[00-System/model-routing|Model routing]] as a proposal (needs-input); nothing switched yet.
- 2026-09-29 — Samuel: "yes to all three", then "No use of low effort, the lowest is medium". Built the routing: `build_adapters.py` now maps skill `tier`/`effort`/`context: fork` into Claude Code; all 14 skills carry an effort (floor medium); `subtitle-transcript-formatter` runs as a Sonnet helper and `video-edit-pass` hands its phase-2 write-out to one. Updated AGENTS.md §7, CLAUDE.md, orchestrator and video-editor profiles, roster, portability, systems register, build state, both routine notes; decision recorded. Listed the plugins and connectors for Samuel to switch off in claude.ai (no agent can).
- 2026-09-29 — Samuel asked what could earn him more before year end, from everything in the Brain. Read goals, patterns, finances, video-editing, HighSignals branches, personal brand. Ranked options with estimates in chat; added them as raw ideas to [[03-Areas/finances/finances-ideas|Finance ideas]]. Suggestions only, nothing decided.
