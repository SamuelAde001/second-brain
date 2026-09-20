---
type: knowledge
area: system
status: active
updated: 2026-09-20
source: manual
tags: [migration]
---

# Migration report

One section per source: what was extracted, where it went, what was skipped and why, and any conflicts found. Append-only.

Order of migration, highest signal first: project handover docs → local editing folder and project knowledge files → memory export → Claude account export → Accountability Engine (legacy archive) → skills.

---

## Sources staged 2026-09-20

`01-Inbox/_imports/claude-export/` — Claude account export, requested 2026-09-20. Five zips, all verified intact.

| File | Contents | Uncompressed |
|------|----------|--------------|
| `conversations-000.zip` | `conversations.json` — 235 conversations, 3,088,580 characters (~772k tokens), dated 2025-12 to 2026-09. 66 conversations under 2,000 characters. | 29.84 MB |
| `projects-000.zip` | 11 project files — the Claude project documents | 0.25 MB |
| `memories-000.zip` | 1 memory file — the memory export | 0.15 MB |
| `light_metadata-000.zip` | `users.json`, `login_history.json` | 0.01 MB |
| `frames-000.zip` | 30 files — artifact HTML and metadata | 1.49 MB |

Conversations by month: 2025-12 (2), 2026-02 (2), 2026-03 (6), 2026-04 (4), 2026-05 (5), 2026-06 (7), 2026-07 (54), 2026-08 (103), 2026-09 (52).

Note: the export's download URLs are session-bound and single-use. A command-line fetch returned HTTP 403; Samuel downloaded all five in-browser and they were copied (not moved) into `_imports/`.

Other sources identified in Phase 0 and not yet staged: `Desktop/engine` (legacy Accountability Engine), the HighSignals and Downloads handover docs, `Video edits/Routerise/Claude Files/`, `Desktop/Contentinfluence/`, `Desktop/Money-2026.xlsx`. Full inventory with paths and sizes: `00-System/build-state.md`.

Nothing has been extracted yet. Phase 2 begins after Phase 1 is signed off.
