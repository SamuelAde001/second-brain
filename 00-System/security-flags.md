---
type: knowledge
area: system
status: active
updated: 2026-09-20
source: manual
tags: [security]
---

# Security flags

Files found on this machine that contain, or may contain, items on the never-store list in AGENTS.md §6, or other people's personal data. **Nothing listed here is ever copied into the Brain.** The path is recorded so import scripts skip it and so Samuel knows it exists.

| Date | Path | What it is | Action |
|------|------|------------|--------|
| 2026-09-20 | `Desktop/engine/.env` | Environment file in the legacy Accountability Engine repo. Almost certainly holds API keys and a Telegram bot token. | Excluded from the archive copy in Phase 2. Never read, never committed. |
| 2026-09-20 | `Desktop/HighSignals/…ExportBlock…/HighSignals Membership form *.csv` and `HighSignals Members *.md` | Notion export of community member records — other people's personal data. | Not imported. Community notes describe the community, not its members. |
| 2026-09-20 | `Documents/parsec_backup_codes.txt` | Backup / recovery codes. | Not imported. Worth moving into a password manager and deleting the file. |
| 2026-09-20 | `Desktop/Downloader/cookies.txt` | Browser session cookies used by a downloader tool — session credentials. | Not imported. |

## Standing note

The Claude export in `01-Inbox/_imports/claude-export/` is chat history. It may contain account nicknames, amounts, names of real people, and possibly credentials pasted into a chat at some point. Phase 2 distillation applies AGENTS.md §6 to everything it extracts, not only to obvious credential files.

## Import scans performed

| Date | Scope | Result |
|------|-------|--------|
| 2026-09-20 | `08-Archive/accountability-engine/` — 81 files copied from `Desktop/engine` | **Clean.** No credentials, account numbers, BVN, NIN, tokens or passwords. `SHEETS_TOKEN` appears only as a variable name and a `__SHEETS_TOKEN__` placeholder. Long digit strings are TickTick project IDs. `.env` deliberately not copied. |

