---
type: knowledge
area: system
status: needs-input
updated: 2026-09-29
source: manual
tags: [models, tokens, effort, routing]
---

# Model routing: which model and effort for which job

Proposal, 2026-09-29, at Samuel's request: *"Which tasks should use Sonnet and which should use Opus, I want us to have a way of automatically switching"*, and *"Map including their effort level needed, and what would give me the best results"*. **Nothing here is decided until he says yes** (AGENTS.md §5 rule 7). Until then the standing rule holds: every agent on Opus 5.5 in the main session.

## What the choice actually costs

API prices, the best proxy for how fast each model uses up the Pro limit (Anthropic doesn't publish the exact weighting):

| | Fresh input | Output | Cached input (re-read every turn) |
|---|---|---|---|
| Opus 5.5 | USD 4 / 1M tokens | USD 20 / 1M | USD 0.20 / 1M |
| Sonnet 5.5 | USD 2 / 1M | USD 10 / 1M | USD 0.20 / 1M |

Four facts shape everything below:

1. **Sonnet is half price on new input and output, and the same price on cached input.** In a long session most tokens are cached re-reads, so Sonnet saves less there than "half" suggests. It saves most on jobs that write a lot (long transcripts, whole HTML files).
2. **The cache belongs to one model.** Switching model mid-session makes the new model re-read the whole conversation at full price. A Sonnet turn in the middle of a long Opus session usually costs *more* than staying on Opus. So Sonnet only pays where the context starts fresh: a new session, a cloud routine, or a forked helper.
3. **Effort is the cheaper dial.** Effort (`low` → `medium` → `high` → `xhigh` → `max`) sets how hard the model thinks. Opus 5.5 at `low` often matches older models at `high`. Turning effort down on easy jobs keeps one model and one cache. The Claude Code default for both models is `medium`.
4. **A Claude Code session can't switch its own model.** The app refuses it. What can switch automatically: a skill (its frontmatter sets model and effort while it runs), a forked helper (runs in its own context on its own model), and a routine (model fixed per routine).

## Where the tokens go (checked 2026-09-29)

- **About 22 of the last 40 sessions (2026-09-24 → 29) were Editor work:** Fusion comps, visuals, Resolve caching and renders, cuts. That's where the volume is. Money, PA and content sessions are short and few.
- **Every session starts at about 70,000 tokens before a word is said:** system tools ~32k, MCP tools ~16k, the skills list ~10k, memory files ~6k. Much of it is plugins the Brain never uses (marketing, SOX/finance, data, design, product-management). That load is paid on every turn of every session, on any model.
- Plan use at the time of checking: 5-hour window 28%, weekly 31%.

## The rule (proposed)

1. **Opus 5.5 stays the default for every agent in the main session.** Results first, and one model keeps one cache.
2. **Effort is set per job, automatically**, through each skill's frontmatter. Most jobs don't need more than `medium`; a few are worth `high`; `xhigh` only for hard Resolve debugging and changes to the Brain's structure; `max` never by default.
3. **Sonnet 5.5 where the context starts fresh and the job is well specified:** cloud routines that read and report, forked helpers for output-heavy mechanical jobs, and a fresh session for batch builds of an approved design.
4. **Opus stays on anything where a mistake reaches a client, his money, or his own judgement.** Cheaper model there is a false saving: one redo costs more than the difference.
5. **When a new session's job fits a different setting, the General Manager says so in one line at the start** (e.g. *"batch render job: Sonnet, effort medium; switch in the model menu or say go"*). He switches; the app won't let a session re-price itself.

## The map

Tier: **O** = Opus 5.5, **S** = Sonnet 5.5. How: **skill** = frontmatter on the skill, automatic · **fork** = runs as a helper with its own context, automatic · **routine** = set on the routine · **session** = the General Manager names it at the start · **default** = nothing to set.

### Editor — most of the volume

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| Job setup, footage download, folders | O | low | default | Scripts do it (`drive_download.py`); the model only runs them |
| Cut: sync, ripple silence, waveform segments | O | medium | default | Scripts do the work; judgement on which take is bad |
| `video-edit-pass` phase 1: duplicates, misspeaks, redundancy, missing sections | O | high | skill | Editorial judgement over a long transcript. A missed bad take reaches the client |
| Sectionalising the cut | O | high | default | "Must be right before anything proceeds" |
| `subtitle-transcript-formatter` | S | medium | fork | Mechanical and output-heavy: the whole transcript is written out. Half price on the part that costs most |
| `video-edit-pass` phase 2: chaptered transcript | S | medium | fork | Same shape as the formatter, once phase 1 is approved |
| Visual sheet: a visual per sentence | O | high | default | Creative, his taste, the deliverable he approves |
| New visual style or motion design (HTML/CSS) | O | medium | default | Design quality matters; Opus is stronger at visual output |
| Batch builds of already-approved visuals, renders onto the duplicate timeline | S | medium | session | Specified by the approved sheet; long and output-heavy. A fresh session for the batch |
| Fusion comps through the Resolve API | O | high | default | Poorly documented API, known hangs (`DuplicateTimeline`). Wrong code wastes a render |
| Resolve bugs, crashes, cache and render diagnosis | O | high → xhigh | session | Hard, multi-step. `xhigh` when a crash or hang is being chased |
| New scripts (sound design, automation) | O | medium | default | Code that he'll reuse; worth getting right once |
| `edit-clock` | O | low | skill | Tiny: fills a template and runs `pace.py` |
| Delivered-projects row | O | low | default | One line, part of the end-of-job review |
| End-of-job review | O | medium | default | Lessons folded into SOPs; judgement, but once per job |

### Money man

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| `payday` | O | medium | skill | Scripts do the arithmetic; transfers must be right. Short |
| `budget` | O | high | skill | Trade-offs against money that exists; he pushes back. Monthly |
| `month-close` | O | high | skill | Goal 1 pace, the freeze. Once a month, so the cost is small |
| `money-check` | O | low | skill | Three lines from `budget_sheet.py left`. On Sonnet it would cost more, not less (rule 2 above) |
| `sunday-check` | O | medium | skill | Logging a gap from his balance; runs in the Sunday session with the review |

### PA

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| Morning brief (cloud routine) | S | low | routine + skill | Reads TickTick and reports. Already on Sonnet |
| Night plan (cloud routine) | O | high | routine + skill | The accountability core. Sonnet missed a same-day replan on 2026-09-24 |
| `weekly-review` | O | high | skill | Patterns, misses, next week's plan. Once a week |
| Add, move, complete TickTick tasks | O | low | default | Mechanical |
| Replanning around a clash (wedding, church, a new job) | O | medium | default | Judgement on his real week |
| Discipline and habit conversations | O | medium | default | His words quoted back correctly matter more than speed |

### Brand manager

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| `write-script` | O | high | skill | His voice, the hook. Low volume, high stakes for the brand |
| Ideas and hooks | O | high | default | Creative judgement |
| `yap-session-planner` | O | medium | skill | Interview and a short outline |
| `content-report` | O | low | skill | Logs his numbers, computes pace |

### General Manager

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| Session start, filing his Obsidian edits, commits, adapter rebuilds | O | low | default | Mechanical; the session is already on Opus |
| Brain structure and decisions, HighSignals, Scripnals, the book, `02-Me` | O | high | default | Judgement he lives with |
| Web research and sweeps across many files | S | medium | fork | Reading-heavy, fresh context, only the conclusion comes back |

### Routines

| Routine | Tier | Effort | Change |
|---|---|---|---|
| Morning brief, cloud | S | low | effort pinned through the skill |
| Night plan, cloud | O | high | effort pinned through the skill |
| Sunday session, desktop | O (session default) | per skill: `sunday-check` medium, `content-report` low, `weekly-review` high | effort pinned through each skill |
| Screen time | no AI | — | none |

## How it runs automatically

1. **Canonical skills get two neutral fields:** `effort:` (`low`…`max`) and, where it applies, `tier:` plus `context: fork`. `build_adapters.py` maps them into the Claude Code copy (`model: sonnet`, `effort: high`, `context: fork`). Today it copies only `name` and `description`, so the script needs that change. Claude Code then applies them whenever the skill runs, on the PC and in the cloud routines.
2. **The two forked jobs** (`subtitle-transcript-formatter`, `video-edit-pass` phase 2) and research sweeps run as helpers on Sonnet. This makes a standing exception to *"a subagent only when Samuel asks"*: the exception needs his yes.
3. **Routines** keep their model on the routine; the night plan and morning brief notes stay canonical.
4. **Session-level:** the General Manager's session-start line names model and effort when the job calls for a change (Editor batch builds → Sonnet; Resolve crash hunts → `xhigh`).

## Separate savings that don't touch quality

- **Turn off the plugins the Brain never uses.** About 26,000 of the 70,000 start-up tokens are MCP tools and skill listings, many unused. Every turn of every session pays for them. His call which ones stay.
- **One session per job.** A Resolve session left running all day re-reads its whole history every turn. Start fresh when the job changes; the Brain holds the memory.
- **Scripts first** already does the rest (AGENTS.md rule 10).

## Open to confirm

- The map as a whole, or changes to any row.
- The standing exception for Sonnet helpers (rule 3 and the two forked jobs).
- Which unused plugins to turn off.

Back to [[00-System/build-state|Build state]] · [[07-Agents/roster|Roster]] · [[00-System/systems-register|Systems register]]
