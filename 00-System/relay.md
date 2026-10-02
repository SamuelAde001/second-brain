---
type: sop
area: system
status: active
updated: 2026-10-02
source: interview
tags: [portability, gemini, antigravity, relay, limits]
---

# Relay: Claude Code and Gemini on the same work

> Samuel, 2026-10-02: *"I don't like the fact that my tokens can finish on Claude and I have to wait for Claude before I resume, I want Claude to be able to talk with Gemini CLI to get some work done, or I can continue some work that Claude was doing in Gemini CLI"*.

**Gemini here means Antigravity CLI (`agy`).** Google stopped "Sign in with Google" for Gemini CLI on personal, AI Pro and AI Ultra accounts on 2026-06-18 and replaced it with Antigravity CLI, which comes with his Google One AI Pro plan. Found 2026-10-02 when his sign-in failed. Antigravity reads AGENTS.md and GEMINI.md itself, and runs the Brain's skills from `.agents/skills/`. Both AIs work on the same Brain folder on the PC, so nothing needs copying, and Gemini's limits are separate from Claude's.

| Mode | Who drives | What happens |
|---|---|---|
| **Helper** | Claude Code | Claude hands Gemini a reading job with `00-System/scripts/ask_gemini.py` and gets the answer back, spending only the question and the answer from its own limits |
| **Backup** | Samuel, in Gemini | Claude's limits ran out mid-task. Samuel opens `agy` in the Brain and types `/pick-up`; Gemini reads what Claude was doing and carries on. `/hand-back` when he returns to Claude |

`00-System/scripts/relay.py` connects them. It reads the other AI's latest saved session (Claude Code's transcript, or Antigravity's under `%USERPROFILE%\.gemini\antigravity-cli\`; outside the Brain, read-only, AGENTS.md §10) plus `git status` and the last commits, and prints a brief. It writes nothing. Claude can be cut off with no warning, so the brief comes from the transcript Claude Code saves as it goes, not from a note Claude has to remember to write. Going back, Claude reads the relay log entry Gemini writes at `/hand-back`, and the brief from Gemini's session if there is no entry.

## One-time setup (Samuel)

In PowerShell (not Administrator):

1. Install: `irm https://antigravity.google/cli/install.ps1 | iex`. It installs to `%LOCALAPPDATA%\agy\bin` and adds itself to PATH; open a new terminal after.
2. `cd "C:\Users\repzy\Desktop\My Second brain"`, then `agy`. Sign in with Google in the browser it opens (the AI Pro account). If it offers to import Gemini CLI settings, yes. If it asks to trust the folder, yes.
3. In agy, type `/mcp`. `resolve` and `ticktick` are listed (from `.agents/mcp_config.json`). TickTick shows *Unauthorized* until you sign in: arrow to `ticktick`, Enter, choose authenticate, approve in the browser, paste the code back if it asks.
4. Tell Claude it's done. (Sign-in and the helper test passed 2026-10-02.)

Login tokens stay in Windows' credential manager and `%USERPROFILE%\.gemini\`, never in the Brain.

### What Gemini is connected to

| Service | How | Notes |
|---|---|---|
| DaVinci Resolve | `ResolveMCP.exe`, Blackmagic's own server, in `.agents/mcp_config.json` | the same server Claude Code uses; Resolve must be open |
| TickTick | TickTick's official server, `https://mcp.ticktick.com/`, in `.agents/mcp_config.json` | own sign-in (step 3) |
| Gmail, Google Calendar, Drive | **not yet.** Google's Workspace MCP servers for Antigravity need a Google Cloud project with an OAuth client that Samuel creates ([codelab](https://codelabs.developers.google.com/google-workspace-mcp-antigravity)). The OAuth secret goes in his user-level `%USERPROFILE%\.gemini\config\mcp_config.json`, never the Brain | when connected, the Brain's rules still hold: nothing is ever scheduled on Google Calendar, nothing is sent from Gmail without Samuel's yes on that message |

## Helper mode: Claude hands a job to Gemini

```
python 00-System/scripts/ask_gemini.py "the task"
python 00-System/scripts/ask_gemini.py --file <task file in the scratchpad>
```

- **Read-only.** agy runs headless in its default mode, which refuses any tool that isn't pre-approved. It reads, searches and answers. It never writes, runs commands or commits. Tested 2026-10-02: told to create a file, it tried and the file was never made.
- **Hand over:** reading-heavy sweeps (many notes, long transcripts or exports), web research, summaries, checking a long file for something. Jobs where most of the cost is reading, not judging.
- **Keep in Claude:** decisions, anything in Samuel's voice (scripts, hooks), finance rule enforcement, editorial calls on a cut, and every write.
- **Treat the answer as a draft.** It's checked like any source: nothing enters the Brain on Gemini's word alone if the note it cites says otherwise.
- The task stands alone: Gemini starts fresh with AGENTS.md and nothing of Claude's conversation.

## Backup mode

**Picking up** — the [[pick-up]] skill: brief → load the working agent → tell Samuel what was in progress and the next step → wait for his go → carry on under AGENTS.md in full. Commits start with `[gemini]`; push after each.

**Working where Samuel can follow it** (Samuel, 2026-10-02: *"I can't tell what it is doing"*). Gemini's own step summaries are too terse to follow, so in every session:
1. Before the first tool call, say in plain words what you understood, what "done" means, and the steps (3–6 lines). If the ask is vague or big (e.g. "finish the edit"), ask one question to pin it down instead of exploring.
2. After each step, one line: what you just did and what you found, e.g. *"Opened the Apollo project: 3 timelines, the latest is Visuals v1."*
3. Before anything that changes Resolve, TickTick or a client's files, say exactly what will change and wait for his yes.
4. Client deliverables and judgement-heavy edits (what to cut, what goes on screen) are the Editor's calls at full strength: in Gemini, prepare and report; don't decide.

**What Gemini can't reach:** Gmail, Calendar and Drive until they're connected (above), and folders outside the Brain unless Samuel adds them to the session (for the Editor, the Route Rise folder). It says so and stops at that step.

**Handing back** — the [[hand-back]] skill: commit what's finished, one entry in [[06-Logs/relay/relay-log|the relay log]] (done, half-done, next step), push.

**Claude coming back:** the session-start hook names any `[gemini]` commits since Claude's last. The General Manager runs [[pick-up]] from its side: reads the newest relay-log entry, reviews the `[gemini]` commits, fixes or files what needs it (a dated correction where a log is involved), says what it changed, and carries on.

## Write tiers

Gemini is the **backup** AI ([[00-System/portability|portability]] → write tiers): while Samuel works in it, it writes like the primary under the same rules, prefixed `[gemini]`, and Claude reviews its commits. As Claude's helper it is read-only.

Back to [[00-System/portability|Portability]] · [[00-System/systems-register|Systems register]] · Constitution: [[AGENTS]]
