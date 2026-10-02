---
type: sop
area: system
status: active
updated: 2026-10-02
source: interview
tags: [portability, gemini, antigravity, relay, limits]
---

# Relay: Claude Code and Gemini, equal, on the same work

> Samuel, 2026-10-02: *"I don't like the fact that my tokens can finish on Claude and I have to wait for Claude before I resume, I want Claude to be able to talk with Gemini CLI to get some work done, or I can continue some work that Claude was doing in Gemini CLI"*.
>
> Samuel, 2026-10-02, later: *"I want to Gemini Antigravity app to have access to all you can do, and be able to do everything you can do, just in case I don't feel like using you, you both should be on the same level, and not Gemini being second in place"*.

**Claude Code and Gemini are equal primaries.** Gemini here means **Antigravity**, the desktop app or the CLI (`agy`). Google stopped "Sign in with Google" for Gemini CLI on personal, AI Pro and AI Ultra accounts on 2026-06-18 and replaced it with Antigravity, which comes with his Google One AI Pro plan. Antigravity reads AGENTS.md and GEMINI.md itself, runs the Brain's skills from `.agents/skills/`, and its limits are separate from Claude's. Both AIs work on the same Brain folder on the PC, so nothing needs copying. Samuel uses whichever he wants; neither outranks the other.

| Mode | Who drives | What happens |
|---|---|---|
| **Switching** | Samuel | He moves from one AI to the other (limits ran out, or he'd rather). He types `/pick-up` in the one he moves to; it reads what the other was doing and carries on. `/hand-back` in the one he leaves, when he has the chance |
| **Helper** | Claude Code | Claude hands Gemini a reading job with `00-System/scripts/ask_gemini.py` and gets the answer back, spending only the question and the answer from its own limits |

`00-System/scripts/relay.py` connects them. It reads the other AI's latest saved session (Claude Code's transcript, or the newer of Antigravity's app and CLI sessions under `%USERPROFILE%\.gemini\antigravity\` and `antigravity-cli\`; outside the Brain, read-only, AGENTS.md §10) plus `git status` and the last commits, and prints a brief. It writes nothing. Either AI can be cut off with no warning, so the brief comes from the transcript each tool saves as it goes, not from a note the AI has to remember to write.

## Same rules, both AIs

| | Claude Code | Gemini (Antigravity) |
|---|---|---|
| Rules | AGENTS.md via CLAUDE.md | AGENTS.md, natively, plus GEMINI.md |
| Agents and skills | `.claude/agents/`, `.claude/skills/` (generated) | the profiles, `.agents/skills/` (generated) |
| Session start (pull GitHub, name the other AI's new commits) | SessionStart hook in `.claude/settings.json` | first-turn hook in `.agents/hooks.json` |
| Secrets never read; deletes, system changes, installs and history rewrites wait for Samuel's yes | `.claude/settings.json` deny and ask lists | `.agents/hooks.json` → `00-System/scripts/agy_guard.py`, the same lists. **Change both together** |
| Commits | trailer `Co-Authored-By: Claude …` | trailer `Co-Authored-By: Gemini (Antigravity) <noreply@google.com>` (until 2026-10-02 a `[gemini]` prefix) |
| Model | Opus 5.5 (strong tier) | Gemini 3.1 Pro (High), Samuel's pick ([[00-System/portability\|portability]] → tiers) |

The guard was tested 2026-10-02 in `agy`: a read of the secrets folder was blocked by the hook, ordinary commands ran, and the session-start note arrived. In a headless `agy -p` run the "ask Samuel" check did not stop a delete, because there is no one to ask, so the headless helper runs in plan mode (read-only) instead. Not yet seen in the app: the approval prompt on a delete. Samuel sees it the first time one comes up.

## What each AI can reach

| | Claude Code | Gemini (Antigravity) |
|---|---|---|
| The Brain: read, write, git, push, scripts (incl. the Money sheet) | yes | yes |
| Outside-Brain folders in AGENTS.md §10 | yes, per `.claude/settings.json` | yes (the app allows files outside the workspace; in `agy`, `--add-dir`) |
| DaVinci Resolve | yes | yes (`ResolveMCP.exe`; Resolve must be open) |
| TickTick | yes | yes, after Samuel signs in once (below) |
| Notion | yes | yes, after Samuel signs in once (below) |
| Gmail, Google Calendar, Drive | yes | **not yet.** Google's Workspace servers for Antigravity need a Google Cloud OAuth client that Samuel creates ([codelab](https://codelabs.developers.google.com/google-workspace-mcp-antigravity)); the secret goes in `%USERPROFILE%\.gemini\config\mcp_config.json`, never the Brain |
| Web search and pages | yes | yes, built in |
| Browser | its own browser pane, and Chrome | Antigravity's browser agent |
| Controlling desktop apps by screen (computer use) | yes | **no.** Possible only through a third-party Windows MCP server, installed with Samuel's yes |
| Cloud routines (6:30am brief, 8:45pm night plan, Sunday session) | they run on Claude | none. They keep running on Claude whichever AI he chats in |
| From the phone | Claude app cloud sessions (PC can be off) | Antigravity's remote control, on in its settings, PC on. Not yet tested |
| Hand the other a reading job | `ask_gemini.py` | not yet: needs the Claude Code CLI on the PC (Samuel's yes to install) |

Gmail and Calendar keep their Brain rules in both: nothing is scheduled on Google Calendar, nothing is sent from Gmail without Samuel's yes on that message.

## One-time setup (Samuel)

In PowerShell (not Administrator):

1. Install the CLI: `irm https://antigravity.google/cli/install.ps1 | iex`. It installs to `%LOCALAPPDATA%\agy\bin` and adds itself to PATH; open a new terminal after. (Done 2026-10-02. The app is installed too.)
2. `cd "C:\Users\repzy\Desktop\My Second brain"`, then `agy`. Sign in with Google in the browser it opens (the AI Pro account). Trust the folder. (Done 2026-10-02.)
3. **Sign in to TickTick and Notion:** in agy, type `/mcp`. Arrow to `ticktick`, Enter, authenticate, approve in the browser, paste the code back if it asks. Same for `notion`. In the app, the same servers show under its MCP settings.
4. **Model:** pick Gemini 3.1 Pro (High) in the app's model menu, and in agy with `/model` (agy's saved default is 3.8 Flash).

Login tokens stay in Windows' credential manager and `%USERPROFILE%\.gemini\`, never in the Brain.

## Helper mode: Claude hands a job to Gemini

```
python 00-System/scripts/ask_gemini.py "the task"
python 00-System/scripts/ask_gemini.py --file <task file in the scratchpad>
```

- **Read-only for that call.** agy runs headless in plan mode (`--mode plan`). It reads, searches and answers; it never writes, runs commands or commits. Tested 2026-10-02 after Samuel set agy to always-proceed: told to create a file and run a command, it did neither.
- **Hand over:** reading-heavy sweeps (many notes, long transcripts or exports), web research, summaries, checking a long file for something. Jobs where most of the cost is reading.
- **The answer is a draft:** the session that asked keeps the judgement and does every write. Nothing enters the Brain on the helper's word alone if the note it cites says otherwise.
- The task stands alone: Gemini starts fresh with AGENTS.md and nothing of Claude's conversation.

This is a mode of one call, not a rank. When Samuel works in Gemini, Gemini does the judging and the writing.

## Switching

**Picking up:** the [[pick-up]] skill: newest relay-log entry, then the brief → load the working agent → tell Samuel what was in progress and the next step → wait for his go → carry on under AGENTS.md in full. Commits carry the AI's own trailer; push after each.

**The other AI's commits:** the session-start note in each AI names the commits the other made since its own last. Read them (`git show`), say in one line what you found, and fix only what is actually wrong (a dated correction where a log is involved). Neither reviews the other as a senior.

**Chats count too** (Samuel to Gemini, 2026-10-02: *"I want it that even when I am just chatting about somethings, you log them so Claude knows what's going on in case"*). Either AI, at the end of a chat that touched live work or settled something not recorded anywhere else, appends one line to [[06-Logs/relay/relay-log|the relay log]]. Anything he settles still goes where AGENTS.md says (standing rules, decisions, the area's log) in the same session.

**Working where Samuel can follow it** (Samuel, 2026-10-02: *"I can't tell what it is doing"*). Both AIs, every session:
1. Before the first tool call, say in plain words what you understood, what "done" means, and the steps (3–6 lines). If the ask is vague or big (e.g. "finish the edit"), ask one question to pin it down instead of exploring.
2. After each step, one line: what you just did and what you found, e.g. *"Opened the Apollo project: 3 timelines, the latest is Visuals v1."*
3. Before anything that changes Resolve, TickTick or a client's files, say exactly what will change and wait for his yes.

**Handing back:** the [[hand-back]] skill: commit what's finished, one entry in [[06-Logs/relay/relay-log|the relay log]] (done, half-done, next step), push.

**Can't reach it:** a step that needs a connection this AI doesn't have (table above) is said out loud and stopped at, never guessed.

Back to [[00-System/portability|Portability]] · [[00-System/systems-register|Systems register]] · Constitution: [[AGENTS]]
