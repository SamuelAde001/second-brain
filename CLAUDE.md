@AGENTS.md

# Claude-specific notes

Everything that governs behaviour is in AGENTS.md above, and the Brain is model-agnostic (AGENTS.md §11, `00-System/portability.md`). This file is an adapter: it holds only what is specific to Claude Code. Nothing here may be the only copy of anything.

Claude Code is one of two **equal primaries** in this Brain; the other is Gemini in Antigravity (Samuel, 2026-10-02; portability.md → write tiers). GEMINI.md is its adapter.

## Generated files — do not edit by hand
- `.claude/agents/<name>.md` — generated from `07-Agents/<name>/profile.md`. Except the orchestrator (`runs-as: main-session`): it is this session's own role, so it has no adapter.
- `.claude/skills/<name>/SKILL.md` (+ its files) — generated from `00-System/skills/<name>/`.
- Regenerate after any profile or skill change: `python 00-System/scripts/build_adapters.py`. Check with `--check` before committing.
- Profiles use neutral names; the script maps them. Tiers: `light` → haiku, `standard` → sonnet, `strong` → opus. Tools: `read`, `write`, `shell`, `send-file`, `web`, `mcp:<server>:<tool>` → Claude Code tool names. Maps live at the top of the script.
- The four skills also exist as claude.ai plugin copies (`anthropic-skills:*`). The Brain copy is canonical.

## Agent names
Every reply starts with the working agent's name, e.g. **[PA]**, and marks every switch mid-task. Names and the rule: AGENTS.md §7.

## Permissions
`.claude/settings.json`. Least privilege. Gemini runs under the same deny and ask rules through `.agents/hooks.json` → `00-System/scripts/agy_guard.py`: change both together. Outside-Brain folders only via explicit additional-directory entries, each also listed in AGENTS.md §10 and the agent's profile.

## MCP servers
Listed neutrally in `00-System/portability.md` → Integrations. In Claude Code they appear as `mcp__<Server>__<tool>`.

## Token discipline (Max plan)
- Plan: **Max, the USD 100 tier**, on Samuel's new account since 2026-10-06 (was Pro; runbook `00-System/account-migration-max.md`). Usage limits are still shared with Claude chat: a rolling 5-hour window, a weekly cap on all models and a separate weekly Fable cap. Extra usage is off. Check them with the app's usage card, never guess.
- Every agent runs in the main session on Opus 5.5, the project default model in `.claude/settings.json` (Samuel, 2026-09-23). Bulk extraction is done by scripts, not read into context. Model and effort per job: `00-System/model-routing.md` (Samuel, 2026-09-29). Skills set `effort` (floor `medium`) and, for the few Sonnet jobs, `tier: standard` + `context: fork`; `build_adapters.py` maps them. A session can't switch its own model: the General Manager names the right one at session start and Samuel picks it in the model menu. Any other subagent or cheaper model only when he asks, except the Editor's parallel helpers on video jobs (AGENTS.md §7, 2026-10-24). Cloud routines run on Sonnet, except the night plan (Opus, 2026-09-25).
- Before a large batch, write a checkpoint to `00-System/build-state.md` so a cutoff mid-batch loses nothing.
- Gemini (Antigravity app and CLI, `agy`) is an equal primary: when Claude's limits run out, or whenever Samuel would rather use it, he works there instead. It also takes reading-heavy jobs through `00-System/scripts/ask_gemini.py`. Protocol: `00-System/relay.md`.
- **Never set `ANTHROPIC_API_KEY` system-wide.** If it is set, Claude Code silently bills the API instead of the Max subscription.

## Session size
Canonical rule: `00-System/model-routing.md` → Session size is enforced. The session compacts at 500k (`autoCompactWindow` in `.claude/settings.json`), and `00-System/scripts/context_guard.py` (PostToolUse hook) asks for a checkpoint at 460k and makes helper agents return by 350k.

## Compact instructions
When compacting, keep: the working agent's name; the job and its Brain note path; the step in progress and the next step; Samuel's latest instructions word for word; open decisions and questions waiting on him; files, Resolve timelines and folders touched this session; the latest usage-card reading. Drop tool output, image contents and resolved back-and-forth. (Same list in model-routing.md.)

## Claude Code's private memory
Not used for Brain facts (AGENTS.md §11 rule 2). If anything lands there, move it into the Brain.
