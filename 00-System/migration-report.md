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

---

## Source 2 — Claude project knowledge files (2026-09-20)

Extracted from `projects-000.zip` to `01-Inbox/_imports/claude-export/extracted/docs/`. 11 projects, 7 with content, 206,197 characters of documents.

| Project | Docs | Extracted to |
|---------|------|--------------|
| Video Editing project | 8 docs, 78,450 chars | `03-Areas/video-editing/`: `clients/routerise.md`, `routerise-house-style.md`, `fusion-node-system.md`, `sops/routerise-cut-workflow.md`, `tsb-graphics-pipeline.md`, `cut-sheets.md` |
| HighSignals Academy | 2 docs, 54,134 chars | `03-Areas/academy/called-to-edit-beginners/` — `_index.md`, `teaching-rules.md`, 7 module notes |
| Content Creation | 5 docs, 39,436 chars | `03-Areas/personal-brand/`: `brand-context.md`, `script-process.md`, `storytelling-structures.md`, `ideas.md` (30 story ideas) |
| HighSignals brand | instructions only, 2,286 chars | `03-Areas/highsignals/_index.md` — name meaning, mission, four branches, community rules |
| Scripnals | instructions only, 2,011 chars | Already covered by `03-Areas/scripnals/_index.md` — duplicate of the handover doc |
| MY PA | instructions only, 2,508 chars | Tone rules → `02-Me/how-to-work-with-me.md`. The system it describes → `00-System/legacy-review.md` |
| comfort- cuts video edit | 1 doc, 34,177 chars | `03-Areas/video-editing/cut-sheets.md` (Butler reel) |

**Recovered:** `HighSignals_Content_Context.md` — the "HighSignals — Content & Brand Context" doc Samuel believed he had deleted. It was in the Content Creation project. Open question 13 is answered.

**Skipped:** `Content-Creation/_project-instructions.md` — byte-for-byte the same material as `Claude_Instructions_HighSignals.md` plus the script process, both already distilled. Academic projects (Post graduate master project ×2, instrumentation and control) hold no documents.

**TSB:** the graphics-pipeline document never spells the acronym out. Every asset uses a `TSB_` prefix and the document's title is "Taking a Step Back from Claude" — recorded as a strong inference, explicitly not as fact.

## Source 3 — memory export (2026-09-20)

`memories-000.zip` → 44 memory files, 89,107 characters, plus a conversations memory and 7 project memories. Written to `extracted/memory-files/`.

| Memory file | Extracted to |
|-------------|--------------|
| `/profile.md`, `/preferences.md` | `02-Me/_index.md`, `02-Me/how-to-work-with-me.md` |
| `/topics/video-editing-toolchain.md` | `03-Areas/video-editing/toolchain.md` |
| `/topics/fitness.md`, `/food-and-drink.md`, `/interests.md`, `/recent-work.md` | `02-Me/_index.md` |
| `/areas/client-acquisition.md` | `03-Areas/video-editing/client-acquisition.md` |
| `/areas/instagram-content-strategy.md` | `03-Areas/personal-brand/instagram-strategy.md` |
| `/areas/butler-reel.md` | `03-Areas/video-editing/cut-sheets.md` |
| `/projects/…/areas/eee-804.md`, `dielectric-term-paper.md`, `hvdc-ac-dynamics-term-paper.md` | `02-Me/postgraduate-study.md` |
| `/areas/second-brain.md`, `/areas/accountability-engine.md` | Confirm this build's own scope; the engine entry confirms "most of its rules no longer work for him" |

**Two contradictions resolved** by `/profile.md` (2026-09-04): the city is **Abuja**, not Lagos; the branch is **Nigerian Air Force**, not army. Open questions 14 and 15 closed.

**A new fact the build spec did not have:** Samuel is an **active postgraduate engineering student** — EEE 804 Advanced Instrumentation and Measurement, plus two term papers, current to 2026-09-16. Recorded in `02-Me/postgraduate-study.md`. This changes capacity planning, so it is open questions 25 and 26.

**Not yet distilled:** the seven per-project memory files (~60,000 chars) covering the video-editing, content-creation, brand, academy, Scripnals, custom-brand and PA projects.

## Source 5 — Accountability Engine, archived (2026-09-20)

Copied whole from `Desktop/engine` to `08-Archive/accountability-engine/` — 81 files, 1.69 MB. Source repo `github.com/SamuelAde001/engine`, HEAD `e01cd60` (2026-09-16). `.env` deliberately excluded and listed in `security-flags.md`.

Nothing from it was installed, merged or activated. `00-System/legacy-review.md` lists **50 items** — 23 rules, 6 goals, 5 failure patterns, 16 rituals/agents/automations — each tagged with its domain and marked `unreviewed`, for keep/change/drop during the Phase 3 interview.

## Phase 2 pass 1 — conversation triage (2026-09-20)

`00-System/scripts/split_conversations.py` (stdlib only) split `conversations.json` into 235 markdown files under `01-Inbox/_imports/processed/conversations/` and wrote `triage.csv`.

- Suggested keep: 111 conversations, ~627,000 est tokens. **Too large to distil on a Pro plan.**
- Suggested drop: 124 conversations, ~145,000 est tokens.
- A tighter proposal — `triage-proposal.csv` — caps the areas the Brain already covers deeply (video-editing, personal-brand, academy) at their largest few and keeps everything in the thin areas: 39 conversations, ~369,000 est tokens.

Awaiting Samuel's trim at the Phase 2 pass-1 gate.

---

## Correction — 2026-09-20

Samuel: the postgraduate coursework, the term papers and every electrical/power-systems calculation in the export are **his sister's work, not his**. The "comfort- cuts video edit" project is likewise not his.

Removed: `02-Me/postgraduate-study.md` (deleted), the postgrad line in `02-Me/_index.md`, the "power systems engineering" interest claim (corrected in place), all Butler-reel/Comfort Cuts content from `03-Areas/video-editing/cut-sheets.md`, and the Comfort Cuts mention in the video-editing index. Open questions 25 and 26 voided.

Excluded from all further distillation: any conversation matching the `study` keyword set, the "Eight-channel data-acquisition system design" conversation, and anything from the Comfort Cuts project.

The source files stay untouched in `01-Inbox/_imports/` — sources are read-only. They are simply not drawn from.

