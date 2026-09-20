@AGENTS.md

# Claude-specific notes

Everything that governs behaviour is in AGENTS.md above. This file holds only what is specific to Claude Code.

## Where things are
- Skills: `.claude/skills/<name>/SKILL.md`
- Subagent wrappers: `.claude/agents/<name>.md` — each one says: read `07-Agents/<name>/profile.md` and `memory.md` before acting, log to `07-Agents/<name>/log.md`.
- Permissions: `.claude/settings.json`. Least privilege. Outside-vault folders only via explicit additional-directory entries, each also listed in AGENTS.md §10.

## MCP servers
- **TickTick** — tasks, schedule, focus. Used by the orchestrator and the personal-life agent. Tasks live there, not in the vault.
- **DaVinci Resolve Studio** — used by the video-editing agent.
- Others are connected to this machine (Gmail, Google Calendar, Google Drive, Notion, vidIQ) but no agent uses them until Samuel says so.

## Model choice
Cheapest model that does the job well. Reserve the strongest model for judgment-heavy work: editorial review, finance rule enforcement, weekly synthesis, the interview.

## Token discipline (Pro plan)
- Usage limits are shared with Claude chat, on a rolling 5-hour window, with weekly caps.
- Script first. Never read a large file into context to count, filter, split or search it.
- Bulk extraction runs in a subagent on a cheaper model. Judgment work runs on the main model.
- Before a large batch, write a checkpoint to `00-System/build-state.md` so a cutoff mid-batch loses nothing.
- **Never set `ANTHROPIC_API_KEY` system-wide.** If it is set, Claude Code silently bills the API instead of the Pro subscription.

## Session protocol during the build
Start: read `00-System/build-state.md`, then AGENTS.md. State current phase, last completed step, next step. Continue.
End: update build-state, commit, push, one line on what happens next session.
