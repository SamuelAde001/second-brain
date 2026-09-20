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

---

## Source 1 — project handover docs (2026-09-20)

Copied to `01-Inbox/_imports/handover-docs/` (originals untouched):

| File | Origin | Dated |
|------|--------|-------|
| `academy-project-setup.md` | `Desktop/HighSignals/HighSignals Documents/` | 2026-07-23 |
| `scripnals-project-setup.md` | `Desktop/HighSignals/HighSignals Documents/` | 2026-07-23 |
| `Claude_Instructions_HighSignals.md` | `Downloads/` | 2026-07-24 |
| `Guiding While Riding - Series Reference.md` | `Downloads/` | 2026-08-11 |

### Extracted to

| Note | From | What |
|------|------|------|
| `03-Areas/personal-brand/voice-and-rules.md` | Claude instructions | Six non-negotiables, script shape, length rules, visual-direction convention, the two reasons his content flops, how he wants to be worked with |
| `03-Areas/personal-brand/content-pillars.md` | Claude instructions | Five pillars, three open naming projects |
| `03-Areas/personal-brand/script-review-checklist.md` | Claude instructions | Seven-point review SOP and required output format |
| `03-Areas/personal-brand/series/guiding-while-riding.md` | Series reference | Concept, Hook→Mantra→Tip→Steps→CTA structure, fixed mantra and CTA lines, 31-topic bank in 6 phases, rejected names |
| `03-Areas/academy/courses.md` | Academy setup | Three courses, the create-vs-edit boundary, the design risk, the signal-vs-noise filter |
| `03-Areas/academy/_index.md` | Academy setup | Area index |
| `03-Areas/scripnals/_index.md` | Scripnals setup | Core loop, promise, dual-audience rule, product filter, build bias, name origin and rejected names, four TBDs |
| `03-Areas/community/_index.md` | Both setup docs | Ascension model, and the HighSignals naming conflict |
| `03-Areas/personal-brand/_index.md` | All | Area index |

Also scaffolded `goals.md`, `log.md`, `decisions.md`, `ideas.md` for all nine areas (36 files, empty, `goals.md` marked `needs-input`).

### Skipped, and why

- The "copy this into claude.ai" scaffolding in both setup docs — instructions for building a Claude project, not durable facts about Samuel's work.
- `Guiding While Riding - Series Reference_1.md` — byte-identical duplicate, verified with `diff`.
- The reference to a companion doc "HighSignals — Content & Brand Context" — **not found on disk**. If it exists, it is the single richest brand source still missing. Worth asking Samuel for.

### Conflicts found

1. **HighSignals: ecosystem or community?** The setup docs (2026-07-23) describe an umbrella ecosystem with four branches. Samuel stated on 2026-09-20 that HighSignals is his community and his personal brand is himself, @SamuelSignals. Both versions recorded with their dates; `03-Areas/community/_index.md` marked `needs-input`. Open question 3.
2. **Academy naming.** The build spec says "Called to Edit Academy (course)", singular. The source doc describes three courses under an Academy: Called to Create, Called to Edit Beginners, Called to Edit Advanced. The source doc is more specific and more recent than the spec's summary, so it was followed. Not treated as a conflict needing Samuel — but worth confirming in the interview.

### Suggestions recorded as suggestions, not decisions

The Scripnals doc's launch sequencing ("ship the core loop first, then layer in personalisation") is written in the source as a recommendation. It is recorded in the area index as a build bias from the doc, not as a decision Samuel made.

### Corrections after the calibration gate (2026-09-20)

- **Conflict 1 resolved by Samuel.** HighSignals is the umbrella brand over Community, Academy, Mentorship and Scripnals. The personal brand is separate and funnels into it. New area `03-Areas/highsignals/` created; the four branch indexes and `personal-brand/_index.md` rewired; AGENTS.md updated. The ascension model from the July docs is recorded in the umbrella index as unconfirmed.
- **Missing companion doc.** Samuel believes he deleted "HighSignals — Content & Brand Context" and has deprioritised it: his priorities have shifted since it was written. It will be rebuilt by interview when needed, not hunted for. Open question 13.
- **Calibration verdict:** depth confirmed correct. Notes keep source detail verbatim.

