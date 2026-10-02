---
type: sop
area: system
status: active
updated: 2026-10-02
source: interview
tags: [portability, gemini, relay, limits]
---

# Relay: Claude Code and Gemini CLI on the same work

> Samuel, 2026-10-02: *"I don't like the fact that my tokens can finish on Claude and I have to wait for Claude before I resume, I want Claude to be able to talk with Gemini CLI to get some work done, or I can continue some work that Claude was doing in Gemini CLI"*.

Two ways the two AIs share work. Both run on the same Brain folder on the PC, so nothing needs copying: the files, the git history and the agents are the same. Gemini's limits are separate from Claude's, which is the point.

| Mode | Who drives | What happens |
|---|---|---|
| **Helper** | Claude Code | Claude hands Gemini a job with `00-System/scripts/ask_gemini.py` and gets the answer back, spending only the question and the answer from its own limits |
| **Backup** | Samuel, in Gemini | Claude's limits ran out mid-task. Samuel opens Gemini in the Brain and types `/relay`; Gemini reads what Claude was doing and carries on. `/handback` when he returns to Claude |

The connective tissue is `00-System/scripts/relay.py`. It reads the other AI's latest chat history (kept outside the Brain, read-only, AGENTS.md §10) plus `git status` and the last commits, and prints a brief. It writes nothing. Claude can be cut off with no warning, so the brief is built from the transcript Claude Code saves as it goes, not from a note Claude has to remember to write.

## One-time setup (Samuel)

1. Open a terminal in the Brain folder and run `gemini`.
2. When it asks, **trust this folder**. Without trust, Gemini ignores `.gemini/settings.json` and the `/relay` and `/handback` commands.
3. **Sign in with Google** (the account on Google One AI Pro: higher Gemini CLI limits than a free account). The login token stays in `%USERPROFILE%\.gemini\`, never in the Brain.
4. Tell Claude it's done. Claude runs a test job through `ask_gemini.py`.

## Helper mode: Claude hands a job to Gemini

```
python 00-System/scripts/ask_gemini.py "the task"
python 00-System/scripts/ask_gemini.py --file <task file in the scratchpad>
python 00-System/scripts/ask_gemini.py --write --file <task file>
```

- **Read-only by default** (Gemini's plan mode): it reads, searches and uses the web, and cannot write or run commands. `--write` lets it create and edit files, but still not run commands, commit or push. Claude reviews `git diff` before anything is committed, and commits it itself with `[gemini]` at the start of the message.
- **Hand over:** reading-heavy sweeps (many notes, long transcripts or exports), web research, summaries, first drafts of plain notes, checking a long file for something. Jobs where most of the cost is reading, not judging.
- **Keep in Claude:** decisions, anything going to Samuel in his own voice (scripts, hooks), finance rule enforcement, editorial calls on a cut, and anything that needs an MCP server (TickTick, Resolve, Calendar) — Gemini has none.
- **Treat the answer as a draft.** Gemini's answer is checked like any source: no fact enters the Brain on its word alone if the note it cites says otherwise.
- The task is written so it stands alone: Gemini starts fresh with AGENTS.md and nothing of Claude's conversation.

## Picking up in Gemini (`/relay`)

1. Read the relay brief that `/relay` injects: what Samuel last asked, Claude's last replies (each starts with the working agent's name), its last actions, the files it touched, uncommitted changes, the last commits.
2. Read `00-System/build-state.md`, then the working agent's `07-Agents/<name>/profile.md` and `memory.md`. Act as that agent, and open every reply with its name, as AGENTS.md §7 says.
3. In 3–5 lines tell Samuel: which agent, what was in progress, what is done (committed or on disk), and the next step. **Wait for his go** before acting. The brief can be wrong about intent.
4. Carry on. Same rules as Claude: AGENTS.md in full, append-only logs, no deleting, no rewriting history, never store anything on the §6 list.
5. Commit after each completed piece with `[gemini]` at the start of the message, then push.
6. **Cannot do in Gemini:** anything that needs TickTick, DaVinci Resolve, Google Calendar, Gmail or Drive (not connected), and folders outside the Brain unless Samuel started Gemini with `--include-directories` for that folder (the Route Rise folder, for the Editor). Say so and stop at that step.

## Handing back to Claude (`/handback`)

1. Commit any finished work (`[gemini] …`). Unfinished edits stay on disk, uncommitted, and are named in the log entry.
2. Append one entry to [[06-Logs/relay/relay-log|the relay log]]: date and time (WAT), agent, what was done (with commit hashes), what is half-done, the next step.
3. Push.

## Claude coming back

The session-start hook names any `[gemini]` commits made since Claude's last commit. When it does, or when Samuel says Gemini did some work, the General Manager:

1. Reads the newest entry in the relay log, and `python 00-System/scripts/relay.py brief --from gemini` if the log has no entry for it.
2. Reviews the `[gemini]` commits (`git show`), fixes or files what needs it with a dated correction where a log is involved, and says what it changed.
3. Carries on from the next step.

## Write tiers

Gemini is the **backup** AI ([[00-System/portability|portability]] → write tiers): while Samuel is working in it, it writes like the primary under the same rules, prefixed `[gemini]`, and Claude reviews its commits. In helper mode it is read-only unless Claude passes `--write`.

Back to [[00-System/portability|Portability]] · [[00-System/systems-register|Systems register]] · Constitution: [[AGENTS]]
