---
type: knowledge
area: system
status: active
updated: 2026-09-22
source: manual
tags: [conventions]
---

# Conventions

> **It is called the Brain.** Not "the vault" — Samuel's instruction, 2026-09-20. Obsidian's own UI calls any folder it opens a "vault"; that is Obsidian's word, not ours. In every note, every agent profile and every reply, it is **the Brain**.

The short version is in AGENTS.md §4. This is the full version, for when a rule needs settling.

## Filenames
- kebab-case, lowercase, no spaces: `client-onboarding.md`, not `Client Onboarding.md`.
- Dates in filenames only for logs: daily `YYYY-MM-DD.md`, weekly `YYYY-Www.md` (ISO week, e.g. `2026-W38.md`).
- An area's overview note is named after the area: `03-Areas/finances/finances.md`. Never `_index.md`.
- One subject per file. The filename says the subject, not the category.

## Frontmatter
Every note. No exceptions, including logs.

| Field | Rule |
|---|---|
| `type` | area, project, knowledge, sop, log, person, client, decision, agent, skill |
| `area` | the folder under `03-Areas/` it belongs to, or `me` / `system` |
| `status` | active, paused, done, needs-input |
| `updated` | ISO date of the last real change to the content |
| `source` | interview, project-handover, claude-export, memory-export, local-folder, legacy-accountability-engine, manual |
| `tags` | list, lowercase, sparse. Tags are for cross-cutting retrieval only; the folder already says the area. |

### Extra fields for agents and skills
- **Agent profiles** (`07-Agents/<name>/profile.md`) also carry `name`, `description`, `tier` and `tools`, in neutral terms. `00-System/scripts/build_adapters.py` reads them to generate each AI tool's native agent file.
- **Skills** (`00-System/skills/<name>/<name>.md`) also carry `name` and `description` — the open Agent Skills fields. The main file is named after the skill, not `SKILL.md`, so the unique-filename rule holds; the script renames it for tools that need `SKILL.md`.
- Full vocabulary: [[00-System/portability|portability]].

`status: needs-input` means a human answer is missing. Every one of those also gets a line in `open-questions.md`.

## Links
- `[[wikilinks]]`, never raw paths.
- Every note links back to its area overview note.
- A link to a note that does not exist yet is allowed and useful — it marks a gap.

### Ambiguous filenames — the one link rule that bites
The build originally gave every area a file called `_index.md`, plus `goals.md`, `log.md`, `decisions.md` and `ideas.md`. That produced ten identically named files, told Samuel nothing about what any of them held, and broke linking — Obsidian resolves a bare `_index`-style link by filename and silently picks the wrong one.

- Link those five by **full Brain path with an alias**: `[[03-Areas/video-editing/video-editing|Video editing]]`.
- Link everything else short: `[[brand-context]]`, `[[script-process]]`.
- **There is no `../` in wikilinks.** `../community/community` does not resolve — it is a broken link that looks fine in the editor.

Checked across the Brain on 2026-09-20 and fixed in 79 files.

## Size
- Split a note past roughly 300 lines. The split children link to each other and to the index.
- Merge a fragment under roughly 10 lines into its parent note.

## Dates, money, numbers
- ISO dates always: `2026-09-20`. Never "last Tuesday" in a note.
- Money always carries a currency code: NGN 450,000, USD 1,200. Never a bare number, never a bare symbol.
- A number without a date is worthless. Say what it was and when.

## Logs
- Append-only. Newest entry at the bottom.
- Format: `- YYYY-MM-DD — what happened`.
- A mistake is corrected with a new dated entry that says what was wrong. The original line stays.

## Decisions
- Area-level decisions go in that area's `decisions.md`.
- Decisions about the Brain's own structure, rules or agents go in `00-System/decisions.md`.
- Use the `decision` template. A decision without a "why" is not a decision record.

## Commit messages
- One line, imperative, says what changed and where: `video-editing: add client note for Routerise`.
- Prefix `[<tool>]` when a guest AI made the commit, e.g. `[gemini]` ([[00-System/portability|portability]] → write tiers).
- Commit after every completed piece of work, not in one lump at the end.

## What does not go in the Brain
- Tasks and schedules — those live in TickTick.
- Video, audio, project files, exports — those stay on disk where they are.
- Anything on the never-store list in AGENTS.md §6.
- Raw chat transcripts pasted into an area. Distil, then link the source.
