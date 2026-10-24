---
type: knowledge
area: system
status: active
updated: 2026-10-24
source: manual
tags: [models, tokens, effort, routing]
---

# Model routing: which model and effort for which job

Built 2026-09-29 at Samuel's request: *"Which tasks should use Sonnet and which should use Opus, I want us to have a way of automatically switching"*, and *"Map including their effort level needed, and what would give me the best results"*. **Decided the same day:** *"yes to all three"* (the map, Sonnet helpers without asking each time, the plugin list), and *"No use of low effort, the lowest is medium"*. Decision record: [[00-System/decisions|decisions]], 2026-09-29.

## What the choice actually costs

API prices, the best proxy for how fast each model uses up the Pro limit (Anthropic doesn't publish the exact weighting):

| | Fresh input | Output | Cached input (re-read every turn) |
|---|---|---|---|
| Opus 5.5 | USD 4 / 1M tokens | USD 20 / 1M | USD 0.20 / 1M |
| Sonnet 5.5 | USD 2 / 1M | USD 10 / 1M | USD 0.20 / 1M |

Four facts shape everything below:

1. **Sonnet is half price on new input and output, and the same price on cached input.** In a long session most tokens are cached re-reads, so Sonnet saves less there than "half" suggests. It saves most on jobs that write a lot (long transcripts, whole HTML files).
2. **The cache belongs to one model.** Switching model mid-session makes the new model re-read the whole conversation at full price. A Sonnet turn in the middle of a long Opus session usually costs *more* than staying on Opus. So Sonnet only pays where the context starts fresh: a new session, a cloud routine, or a forked helper.
3. **Effort is the cheaper dial.** Effort (`low` → `medium` → `high` → `xhigh` → `max`) sets how hard the model thinks. Opus 5.5 at a lower effort often matches older models at a higher one. Turning effort down on easy jobs keeps one model and one cache. The Claude Code default for both models is `medium`, which is also Samuel's floor: `low` is never used.
4. **A Claude Code session can't switch its own model.** The app refuses it. What can switch automatically: a skill (its frontmatter sets model and effort while it runs), a forked helper (runs in its own context on its own model), and a routine (model fixed per routine).

## Where the tokens go (checked 2026-09-29)

- **About 22 of the last 40 sessions (2026-09-24 → 29) were Editor work:** Fusion comps, visuals, Resolve caching and renders, cuts. That's where the volume is. Money, PA and content sessions are short and few.
- **Every session starts at about 70,000 tokens before a word is said:** system tools ~32k, MCP tools ~16k, the skills list ~10k, memory files ~6k. Much of it is plugins the Brain never uses (marketing, SOX/finance, data, design, product-management). That load is paid on every turn of every session, on any model.
- Plan use at the time of checking: 5-hour window 28%, weekly 31% (on Pro).
- **2026-10-24: moved to Max 20x** (see On Max 20x below).
- **2026-10-06: moved to Max, USD 100 tier** ([[00-System/account-migration-max|plan move]]). Limits: 5-hour window, weekly all models, weekly Fable; extra usage off. The rule below is unchanged. Whether `high` becomes the default effort on judgement jobs now there is more room is Samuel's call, not asked yet.

## The rule

1. **Opus 5.5 stays the default for every agent in the main session.** Results first, and one model keeps one cache.
2. **Effort is set per job, automatically**, through each skill's frontmatter. **Never below `medium`** (Samuel). Most jobs need `medium`; a few are worth `high`; `xhigh` only for hard Resolve debugging and changes to the Brain's structure; `max` never by default.
3. **Sonnet 5.5 where the context starts fresh and the job is well specified:** cloud routines that read and report, forked helpers for output-heavy mechanical jobs, and a fresh session for batch builds of an approved design.
4. **Opus stays on anything where a mistake reaches a client, his money, or his own judgement.** Cheaper model there is a false saving: one redo costs more than the difference.
5. **When a new session's job fits a different setting, the General Manager says so in one line at the start** (e.g. *"batch render job: Sonnet, effort medium; switch in the model menu or say go"*). He switches; the app won't let a session re-price itself.
6. **Gemini takes reading-heavy jobs off Claude's limits** (Samuel, 2026-10-02): sweeps across many files, long transcripts and exports, web research, summaries. Claude sends them through `ask_gemini.py` instead of a Sonnet fork when its limits are tight or the job is mostly reading; Gemini's limits are separate. The answer is a draft: the session that asked keeps the judgement. When Samuel works in Gemini, the same map holds with the Gemini models in [[00-System/portability|portability]] → tiers. [[00-System/relay|Relay]].

## On Max 20x (2026-10-24)

Samuel upgraded to Max 20x on 2026-10-24 to edit faster: *"I'm looking for speed, right? I'm looking for much more good headroom around the usage, right? But I also want to make sure that we don't waste anything."* The General Manager measured the week before with `00-System/scripts/usage_audit.py --since 2026-10-19` (1,776 cost units at API prices):

- **Helpers were 53 % of all spend**, main sessions 45 %. Video 2's run-3 session alone (`1162acdc`) was 731 units, 41 % of the week.
- **27 % of helper spend was cache thrown away.** Helpers cache for 5 minutes, main sessions for 1 hour (checked in the transcripts). A helper tool call that ran 5-15 minutes (a render, a Whisper pass, a wait loop) made it rewrite its whole context at 1.25x. ~249 units, 14 % of everything.
- **25 % of helper spend was start-up re-reads:** every helper starts at ~74,000 tokens (tool definitions, CLAUDE.md, AGENTS.md) and re-reads them every turn (median 28 turns).
- **A fresh reviewer per group tripled build cost:** 1.4 weekly points per group with a reviewer, 0.5 builder-only with self-review (video 2, waves 1 and 2, on 5x).
- **No helper ran on Sonnet** (0 of 7,844 workflow turns), though this map sends mechanical jobs there.
- **Rework was the biggest loss of time and tokens:** video 2's plan v1 (11 points) and *Visuals v1* (16 points) were rejected on look after being built at scale.

The rules from here (the General Manager's, on Samuel's ask to optimise for 20x):

1. **No helper waits past its cache.** Every tool call in a helper finishes in under 4 minutes. Renders, Whisper, Resolve caching, stills through Deliver and installs run in the main session, or the helper starts them in the background and checks in slices of 4 minutes or less (`timeout 230 bash -c 'until <done>; do sleep 15; done'`, then check again). No `sleep` or Monitor wait past 4 minutes in a helper.
2. **Builder-only with self-review is the default.** The builder checks its own work against the job's review card. A fresh reviewer only for hero beats and beats Samuel marked.
3. **Lean helper type.** Helpers that only read, write files and run scripts start as `editor-builder` (`agentType: 'editor-builder'` in a workflow, profile [[07-Agents/editor-builder/profile|editor-builder]]): six tools instead of the full set. Captures in Chrome, Resolve calls and anything else that needs MCP use the default helper. Its start-up saving is unmeasured: check it with `usage_audit.py` on its first run.
4. **Short brief, short output.** The brief names the 2-4 files the piece needs, not a reading list. Tool output is counts and paths. One script call does a whole check.
5. **Images:** one contact sheet per beat, 1280 px wide at most, read once near the end, not single frames one at a time. An image stays in the context and is re-read every turn after it.
6. **Sonnet for mechanical helpers:** `model: 'sonnet', effort: 'medium'` on install lists, captures from a given URL list, transcript formatting, stills sheets, render and cache babysitting. Planners, builders and anything Samuel judges stay on Opus.
7. **Look lock before scale.** Samuel approves 3-4 hero frames of a new look before a full plan or a build fans out (the 2026-10-21 route, made standing).
8. **Pool:** the 5-hour window is about 4x bigger on 20x, so 8 helpers at a time (was 3-5), up to 12 for short steps when the weekly bar has room. The weekly bar is now the limit that runs out: usage card between waves.
9. **Measure every video:** weekly % at each stage (cut, plan, build, each review round, sound) in the job note, and `usage_audit.py --session <id>` at the end-of-job review. The bar read 0 % right after the upgrade (2026-10-24), so the first full video on 20x gives the real cost per video.

## The map

Tier: **O** = Opus 5.5, **S** = Sonnet 5.5. How: **skill** = frontmatter on the skill, automatic · **fork** = runs as a helper with its own context, automatic · **routine** = set on the routine · **session** = the General Manager names it at the start · **default** = nothing to set.

### Editor — most of the volume

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| Job setup, footage download, folders | O | medium | default | Scripts do it (`drive_download.py`); the model only runs them |
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
| `edit-clock` | O | medium | skill | Tiny: fills a template and runs `pace.py` |
| Delivered-projects row | O | medium | default | One line, part of the end-of-job review |
| End-of-job review | O | medium | default | Lessons folded into SOPs; judgement, but once per job |

### Money man

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| `payday` | O | medium | skill | Scripts do the arithmetic; transfers must be right. Short |
| `budget` | O | high | skill | Trade-offs against money that exists; he pushes back. Monthly |
| `month-close` | O | high | skill | Goal 1 pace, the freeze. Once a month, so the cost is small |
| `money-check` | O | medium | skill | Three lines from `budget_sheet.py left`. On Sonnet it would cost more, not less (rule 2 above) |
| `spend` | O | medium | skill | Logging his listed spends against plan lines; `money_ledger.py recap` gives the breakdown, so nothing is read whole |
| `sunday-check` | O | medium | skill | Logging a gap from his balance; runs in the Sunday session with the review |

### PA

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| Morning brief (cloud routine) | S | medium | routine + skill | Reads TickTick and reports. Already on Sonnet |
| Night plan (cloud routine) | O | high | routine + skill | The accountability core. Sonnet missed a same-day replan on 2026-09-24 |
| `weekly-review` | O | high | skill | Patterns, misses, next week's plan. Once a week |
| Add, move, complete TickTick tasks | O | medium | default | Mechanical |
| Replanning around a clash (wedding, church, a new job) | O | medium | default | Judgement on his real week |
| Discipline and habit conversations | O | medium | default | His words quoted back correctly matter more than speed |

### Brand manager

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| `write-script` | O | high | skill | His voice, the hook. Low volume, high stakes for the brand |
| Ideas and hooks | O | high | default | Creative judgement |
| `yap-session-planner` | O | medium | skill | Interview and a short outline |
| `content-report` | O | medium | skill | Logs his numbers, computes pace |

### General Manager

| Job | Tier | Effort | How | Why |
|---|---|---|---|---|
| Session start, filing his Obsidian edits, commits, adapter rebuilds | O | medium | default | Mechanical; the session is already on Opus |
| Brain structure and decisions, HighSignals, Scripnals, the book, `02-Me` | O | high | default | Judgement he lives with |
| Web research and sweeps across many files | S | medium | fork | Reading-heavy, fresh context, only the conclusion comes back |

### Routines

| Routine | Tier | Effort | Change |
|---|---|---|---|
| Morning brief, cloud | S | medium | effort pinned through the skill |
| Night plan, cloud | O | high | effort pinned through the skill |
| Sunday session, desktop | O (session default) | per skill: `sunday-check` medium, `content-report` medium, `weekly-review` high | effort pinned through each skill |
| Screen time | no AI | — | none |

## How it runs automatically

1. **Canonical skills carry neutral fields:** `effort:` (`medium`…`max`) and, where it applies, `tier:` plus `context: fork`. `build_adapters.py` maps them into the Claude Code copy (`model: sonnet`, `effort: high`, `context: fork`). It used to copy only `name` and `description`, so the script was changed 2026-09-29. Claude Code then applies them whenever the skill runs, on the PC and in the cloud routines.
2. **The two forked jobs** (`subtitle-transcript-formatter`, `video-edit-pass` phase 2) and research sweeps run as helpers on Sonnet. A standing exception to *"a subagent only when Samuel asks"*, which he approved 2026-09-29.
2b. **The Editor's parallel helpers (Samuel, 2026-10-24: *"Yes. From now on the Editor can run parallel helper agents on video jobs, as many as the job needs. Write it into the rules."*).** On any video job the Editor fans out helper agents in parallel, as many as the job needs, without asking. Tier per helper follows this map: judgement pieces (edit pass, visual ideas, Fusion design) on Opus, mechanical output-heavy pieces (transcripts, batch builds of approved designs) on Sonnet, effort never below `medium`. Rules: [[07-Agents/video-editor/profile|Editor profile]] → Parallel helpers.
3. **Routines** keep their model on the routine; the night plan and morning brief notes stay canonical.
4. **Session-level:** the General Manager's session-start line names model and effort when the job calls for a change (Editor batch builds → Sonnet; Resolve crash hunts → `xhigh`).

## Separate savings that don't touch quality

- **Turn off the plugins the Brain never uses.** About 26,000 of the 70,000 start-up tokens are MCP tools and skill listings, many unused. Every turn of every session pays for them. His call which ones stay.
- **One session per job.** A Resolve session left running all day re-reads its whole history every turn. Start fresh when the job changes; the Brain holds the memory.
- **Fresh session past 100k context** (Samuel, 2026-10-02: *"yes do both"*). The 1M window means a session never hits a wall, so it keeps growing and every turn re-reads all of it: at 147k, a one-line reply costs about 147k input tokens. Once the context meter passes 100k, the working agent says so; Samuel runs `/compact` if the job continues, or ends it (update build-state, commit) and opens a new session. Checked 2026-10-02: 11 sessions that day, two with transcripts of about 14–15 MB from screenshot-heavy visual work.
- **Session size is enforced, not remembered** (Samuel, 2026-10-12: *"We need to break sessions, or make them compact after a certain limit"*). The 100k rule above was never acted on: the B2B video's sessions ran at 700k-965k, 79 % of its ~569M cost units were cache re-reads, and the video cost about 120 % of a Max week ([[04-Projects/routerise-linkedin-training|LinkedIn job note]] → Token budget). Now:
  - **Main session compacts at 500k** (`autoCompactWindow: 500000` in `.claude/settings.json`; the 1M default compacted at ~967k). Was 200k from 2026-10-12; raised 2026-10-13 (Samuel: *"I don't want the quality of work and output to reduce when I have to always compact knowledge"*).
  - **Context guard** (`00-System/scripts/context_guard.py`, a hook after every tool call). Main session at 460k: write the job's RESUME block into the job note and commit before the compaction, or end the session if the step is done. Helper agents at 300k: finish the current item and wrap up. At 350k: save to disk and return a hand-over now (raised from 150k / 185k, Samuel 2026-10-22: *"Let's increase all the agents' workload so that they can be able to do good work"*).
  - **One step per session** for big jobs (plan, sample, each build wave, review, Samuel's round, render). Each opens from the job note's RESUME block.
  - **Workflow briefs size each agent's scope** to finish under ~300k: one section or 6-10 visuals per builder, short tool output (counts and paths), files to disk.
  - **What a compaction keeps** (also in CLAUDE.md → Compact instructions): the working agent's name, the job and its note path, the step in progress and the next one, Samuel's latest instructions word for word, open decisions, files and timelines touched, and the usage-card reading.
- **Images cost the most.** Crop screenshots to what matters; pull video frames by script at low resolution.
- **Scripts first** already does the rest (AGENTS.md rule 10).

## Plugins and connectors (listed 2026-09-29)

Plugins are switched on for the whole claude.ai account (Settings → Customize / Plugins), so they load into every Claude Code session and chat. **Samuel turns them off; no agent can.** None is used by the Brain, which has its own skills for money, content and planning.

| Plugin | What it loads | Brain use | Recommendation |
|---|---|---|---|
| `marketing` | 8 skills + Canva, HubSpot, Ahrefs, Similarweb, Klaviyo, Supermetrics (none signed in) | none; the Brand manager does this | off |
| `finance` | 9 corporate-accounting skills (SOX, journal entries, reconciliation) + Snowflake, Databricks, BigQuery | none; clashes by name with the Money man's `month-close` job | off |
| `data` | 11 SQL and dashboard skills + Snowflake, Databricks, Hex, Definite (Definite fails every session) | none | off |
| `product-management` | 10 PM skills + Figma, Amplitude ×2, Pendo, Intercom, Fireflies, Similarweb | none | off (Scripnals work goes through the General Manager) |
| `design` | 7 design-review skills | none | off |
| `productivity` | 4 skills + Slack, Notion, Asana, Linear, Atlassian, Monday, ClickUp | none, and its memory and `TASKS.md` skills contradict the Brain's rules (TickTick holds tasks; the Brain is the only memory) | off |
| `pdf-viewer` | 5 skills + a 9-tool viewer | none recorded | off unless he wants PDF annotation |

Each of those five business plugins also registers its own Gmail and Google Calendar servers, which fail in every session; the real Gmail and Calendar connectors are separate and stay.

Connectors (Settings → Connectors), for his call:

| Connector | Brain use | Recommendation |
|---|---|---|
| TickTick, Google Calendar | the PA's daily tools | keep |
| DaVinci Resolve (the one set up in Claude Code) | the Editor, every job | keep |
| **DaVinci Resolve Studio** (desktop extension) | a duplicate of the one above: same 14 tools, never used in the Brain | remove the duplicate. Samuel said yes 2026-10-02; a desktop extension, so only he can switch it off (Claude desktop → Settings → Extensions) |
| Notion | 20 notes use it (shot lists, client idea docs) | keep |
| Google Drive | client footage links | keep |
| Gmail | 3 notes | keep if he wants email read; otherwise off |
| vidIQ | 5 notes mention it | his call |
| Claude Docs, visualize | not used by the Brain | leave; they cost little |

After he switches them off, the next session's start-up load gets measured against the ~70,000 tokens recorded above.

Back to [[00-System/build-state|Build state]] · [[07-Agents/roster|Roster]] · [[00-System/systems-register|Systems register]]
