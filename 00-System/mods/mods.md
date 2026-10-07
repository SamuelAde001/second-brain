---
type: knowledge
area: system
status: active
updated: 2026-10-07
source: manual
tags: [claude-code, mods, tokens, usage]
---

# Claude Code mods

Samuel, 2026-10-07: *"see what Claude code Mods we can build that would be helpful for my workflow ... also I can see major details like token usage, context"*.

A **mod** is a Claude Code plugin of function hooks (TypeScript): it can draw a band above the prompt, a side pane, a status-line entry or a toast, add a slash command, and allow, block or react to tool calls. It runs inside Claude Code and **costs no tokens**: it reads the engine's own figures, it never asks the model anything. Claude Code only; Gemini has no equivalent, so a mod may never be the only place a rule lives (AGENTS.md §11).

**Canonical source: `00-System/mods/<name>/`.** While building, Claude Code works on a session copy under `%USERPROFILE%\.claude\dev-mods\<session>\`; copy back here after every change.

## Built

| Mod | What it shows or does | Status |
|---|---|---|
| `brain-hud` | Band above the prompt: working agent (from the **[Name]** tag), context fill, 5-hour and weekly limits with reset times in WAT, files not committed. `/brain` opens a pane with bars, the context split by category (system, MCP tools, skills, memory) and the session's API-value in USD (a size gauge, not billed on Max). `/brain hide` / `/brain show`. Toasts at 75% and 90% of a limit (90% says run `/hand-back`) and at 70% and 85% context | built 2026-10-07; loads in the session that built it. Loading it in every session needs one line in `~/.claude/settings.json` (Samuel's yes) |

## Ideas, not yet agreed

Ranked by how much they'd save him. Suggestions only (AGENTS.md rule 7).

1. **rulebook-guard**: the engine refuses what AGENTS.md forbids, instead of relying on the model to remember: edits in `01-Inbox/_imports/`, `08-Archive/accountability-engine/`, generated `.claude/agents|skills` files, client raws in `Video edits\Routerise\`; a bank-card-, BVN- or key-shaped number written into a note (§6); force pushes. Reminds to run `build_adapters.py` after a profile or skill edit.
2. **render-watch** (Editor): a pane with the Resolve render queue's progress through `resolve_bridge.py`, a sound and a toast when a render finishes or fails.
3. **job-clock** (Editor): the edit clock inside Claude Code: playhead from Resolve, the deadline from the job note, ahead or behind.
4. **today band** (PA): the next TickTick block with a countdown and must-dos done out of 3. Needs a check that a mod can call the TickTick connector directly.
5. **read-guard** (rule 10, script first): warns before a big file is read whole into context.
6. **done chime**: a sound when a long turn ends, for when he walks away during a Fusion build or render.
7. **webinar countdown** (Brand manager): days to the Called to Edit webinar, sign-ups and paid.

Seen elsewhere (2026-10-07): community catalogues at github.com/hamzafer/claude-code-mods and github.com/karanb192/awesome-claude-code-mods (usage meters, context bars, guards, PR trackers, Markdown preview, games while waiting).

Back to [[00-System/systems-register|Systems register]]
