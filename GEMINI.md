# GEMINI.md

The rules for this vault are in **AGENTS.md** at the vault root. Read it first, in full, before doing anything here. It is the constitution: who Samuel is, the vault map, how to find things, note conventions, operating rules, what must never be stored, and the agent and logging protocols.

`.gemini/settings.json` sets `context.fileName` to `["AGENTS.md", "GEMINI.md"]`, so AGENTS.md should load automatically. If it did not, open it manually.

## Gemini's role in this vault (overflow protocol)

Gemini CLI is the second model and the overflow option when Claude Pro limits are hit.

- Gemini writes only to `01-Inbox/` and `06-Logs/` unless Samuel explicitly widens that for the session.
- It follows AGENTS.md, including the append-only rule and the never-store list.
- It prefixes every commit message with `[gemini]`.
- At the next Claude session, the orchestrator reviews every `[gemini]` commit and files or fixes whatever needs it.

Full detail: `00-System/portability.md` (written in Phase 7).
