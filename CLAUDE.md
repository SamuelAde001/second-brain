@AGENTS.md

# Claude-specific notes

Everything that governs behaviour is in AGENTS.md above, and the Brain is model-agnostic (AGENTS.md §11, `00-System/portability.md`). This file is an adapter: it holds only what is specific to Claude Code. Nothing here may be the only copy of anything.

Claude Code is the **primary** AI in this Brain (portability.md → write tiers).

## Generated files — do not edit by hand
- `.claude/agents/<name>.md` — generated from `07-Agents/<name>/profile.md`. Except the orchestrator (`runs-as: main-session`): it is this session's own role, so it has no adapter.
- `.claude/skills/<name>/SKILL.md` (+ its files) — generated from `00-System/skills/<name>/`.
- Regenerate after any profile or skill change: `python 00-System/scripts/build_adapters.py`. Check with `--check` before committing.
- Profiles use neutral names; the script maps them. Tiers: `light` → haiku, `standard` → sonnet, `strong` → opus. Tools: `read`, `write`, `shell`, `send-file`, `web`, `mcp:<server>:<tool>` → Claude Code tool names. Maps live at the top of the script.
- The four skills also exist as claude.ai plugin copies (`anthropic-skills:*`). The Brain copy is canonical.

## Permissions
`.claude/settings.json`. Least privilege. Outside-Brain folders only via explicit additional-directory entries, each also listed in AGENTS.md §10 and the agent's profile.

## MCP servers
Listed neutrally in `00-System/portability.md` → Integrations. In Claude Code they appear as `mcp__<Server>__<tool>`.

## Token discipline (Pro plan)
- Usage limits are shared with Claude chat, on a rolling 5-hour window, with weekly caps.
- Bulk extraction runs in a subagent on the `light` tier. Judgement work runs on the main model.
- Before a large batch, write a checkpoint to `00-System/build-state.md` so a cutoff mid-batch loses nothing.
- **Never set `ANTHROPIC_API_KEY` system-wide.** If it is set, Claude Code silently bills the API instead of the Pro subscription.

## Claude Code's private memory
Not used for Brain facts (AGENTS.md §11 rule 2). If anything lands there, move it into the Brain.
