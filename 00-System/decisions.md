---
type: decision
area: system
status: active
updated: 2026-09-22
source: manual
tags: [decisions, system]
---

# Structural decisions

Decisions about the Brain itself: its structure, rules, agents and automations. Area-level decisions live in that area's `decisions.md`. Append-only.

---

## 2026-09-20 — Brain lives at `C:\Users\repzy\Desktop\My Second brain`
**Decided:** the Brain stays at its existing Desktop path rather than moving to `C:\SecondBrain` as the build spec assumed.
**Why:** Obsidian is already pointed at it, and the path is outside OneDrive and Dropbox, which was the actual requirement.
**Alternatives rejected:** moving it, which would break the existing Obsidian Brain registration for no gain.
**Who decided:** Samuel (Phase 0 gate).

## 2026-09-20 — GitHub is the sync spine, not a paid sync service
**Decided:** the private GitHub repo is both the backup and the PC-to-phone sync path. The PC commits and pushes; Android pulls and pushes through the Obsidian Git community plugin.
**Why:** Obsidian Sync costs money Samuel is not spending on this. The Brain is text-only and small, and the phone only writes to `01-Inbox/`, which keeps conflicts rare.
**Alternatives rejected:** Obsidian Sync Standard (paid). Syncthing (free, but two systems to maintain and no off-machine backup by itself) — kept as the documented fallback if the Git plugin proves flaky.
**Cost accepted:** a GitHub personal access token must live in the phone plugin's settings. It never goes in a note or the repo.
**Who decided:** Samuel (Phase 0 gate).

## 2026-09-20 — Contentinfluence is history, not an area
**Decided:** Contentinfluence gets imported into `03-Areas/personal-brand/` as a past attempt at personal-brand coaching — what it was, why it failed — not as its own area.
**Why:** it is a dead brand. The lessons matter; the structure does not.
**Who decided:** Samuel (Phase 0 gate).

## 2026-09-20 — No church area
**Decided:** the church / AAC media work gets no area. Files stay where they are on disk.
**Why:** there is not enough of it to manage. If church editing work ever needs tracking, it becomes a client note under video-editing.
**Who decided:** Samuel (Phase 0 gate).

## 2026-09-20 — HighSignals is the community; the personal brand is Samuel himself
**Decided:** `03-Areas/personal-brand/` is Samuel's own brand — him, Instagram handle @SamuelSignals. `03-Areas/community/` is HighSignals. The build spec had these conflated and called HighSignals the personal brand; it is wrong and the correction stands.
**Why:** Samuel said so plainly. Getting this wrong would have mislabelled every note, goal and content decision in two areas.
**Who decided:** Samuel, 2026-09-20.
**Follow-up:** the Phase 3 interview must settle where Called to Edit Academy, the mentorship program and the book sit relative to the brand and the community.

## 2026-09-20 — CORRECTION to the entry above: HighSignals is the umbrella brand
**Decided:** HighSignals is the whole brand. It contains four branches: HighSignals Community, HighSignals Academy, Mentorship, and the Scripnals app. Samuel's personal brand (@SamuelSignals) is a **separate brand outside HighSignals** whose job is to funnel people into it.
**Why:** Samuel stated it directly. The entry above, recorded earlier the same day, captured only half of the correction — that HighSignals is not his personal brand — and wrongly concluded it was just the community.
**What changed in the Brain:** new area `03-Areas/highsignals/` holds brand-level strategy. Community, Academy, Mentorship and Scripnals stay as top-level areas, each linking up to it. AGENTS.md §1 and §2 updated. `03-Areas/community/_index.md` conflict section replaced with the resolution.
**Alternatives rejected:** nesting the four branches inside `highsignals/` (deeper paths, longer cross-links); leaving the tree flat with no umbrella (brand-level strategy would have had nowhere to live).
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — Calibration: notes keep source detail verbatim
**Decided:** extracted notes preserve specifics — full topic banks, exact fixed lines, rejected alternatives, the reasoning behind a rule — rather than summarising them away.
**Why:** Samuel reviewed three sample notes at the Phase 2 calibration gate and confirmed the depth. The test is whether an agent can act from a note without coming back to him.
**Cost accepted:** longer notes, more context per read.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — Git permission rule added
**Decided:** `.claude/settings.json` allows `git add`, `commit`, `push`, `status`, `log`, `diff`, `ls-remote`, and denies reads of `.env`, `*.key`, `credentials*.json`, `token*.json`.
**Why:** Samuel did not want to run every push by hand. Pushing to his own private repo is the one outward action this build needs repeatedly.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — CORRECTION: the postgraduate engineering work is his sister's, not his
**Decided:** nothing about the postgraduate degree, EEE 804, the term papers, or any electrical/power-systems calculation goes in this Brain. Same for anything from the "comfort- cuts video edit" project — that work is not his either.
**Why:** Samuel said so plainly. Earlier the same day I created `02-Me/postgraduate-study.md` from the memory and projects export and told him it changed his capacity picture. That was wrong: the material was in his Claude account because he was helping his sister, not because it was his own commitment.
**What changed:** `02-Me/postgraduate-study.md` deleted. The "power systems engineering" line in `02-Me/_index.md` corrected in place with a note saying why. Butler-reel / Comfort Cuts material stripped out of `03-Areas/video-editing/cut-sheets.md` and the Comfort Cuts mention removed from the video-editing index. Open questions 25 and 26 voided. All study-tagged and Comfort-tagged conversations excluded from the distillation shortlist.
**The lesson, recorded because it will happen again:** material in his Claude account is not automatically *about him*. Work done for someone else looks identical in an export. When a source implies a major life commitment that appears nowhere else, ask before writing it into his identity.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — Every file gets a unique, readable name. No more `_index.md`
**Decided:** an area's overview note is named after the area (`03-Areas/finances/finances.md`), and its standing files are prefixed (`finances-goals.md`, `finances-log.md`, `finances-decisions.md`, `finances-ideas.md`). `02-Me/_index.md` became `about-samuel.md`. The template `area-index.md` became `area-overview.md`.
**Why:** Samuel: *"Why do I have so many index files, why are there not real names of files I can understand."* He was right. The original convention came from the build spec and produced ten files called `_index.md` plus ten called `goals.md`. It failed twice over: a filename told him nothing, and Obsidian resolves links by filename, so a bare link silently picked the wrong file. I had already patched the link symptom on 2026-09-20 without fixing the cause.
**What changed:** 52 files renamed with `git mv` (history preserved), links rewritten in 101 files, then a second pass repaired 14 files where the earlier link patch had produced wrong paths (`03-Areas/03-Areas/…`, `03-Areas/sops/…`). AGENTS.md §4, `conventions.md` and the templates now state the new scheme. Two missing area overview notes were created (`book.md`, `relationships.md`).
**Alternatives rejected:** keeping `_index.md` because Obsidian shows the folder name in some views — it does not help when reading the file tree, which is how Samuel actually looks at the Brain.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — Routerise is the agency, Alex is the client
**Decided:** Routerise is the agency Samuel works through. It assigned him one client, **Alex**, who runs Frontal. Rate **USD 333.33 per video** — the agency standard. One video in five days. Invoiced monthly, **70% at month end and 30% mid the following month**.
**Why:** Samuel stated it in the Phase 3 interview. The imported documents contradicted each other — one called Routerise "my company", another labelled the project "client: Alex / Frontal". The client note had carried that contradiction as an open question since import; it is now closed.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — Prune: delete what is not needed now
**Decided:** Samuel: *"We need to delete knowledge that is not needed presently, any old redundant knowledge that isn't needed shouldn't just pile our texts."* Four groups removed.

| Removed | Size | Why |
|---------|------|-----|
| Engine build artifacts — `site/`, `tools/`, `scorecard.html`, `PA.md` | 1.28 MB of 1.69 MB | Generated output and a 4,537-line duplicate of the repo. Not knowledge. `context/` history kept. |
| `voice-and-rules.md`, `content-pillars.md` | 87 lines | Thinner restatements of `brand-context.md`. Their unique parts — the six non-negotiables, the braces convention, the promotion rule, how he wants to be worked with — were folded in first. |
| `academy/courses.md` | 46 lines | Folded into `academy.md`. **Not deleted outright:** eight notes explicitly deferred to it rather than repeat the create-vs-edit boundary, so deleting it plainly would have lost that definition, not deduplicated it. |
| `video-editing/intro-concepts.md` | 91 lines | Unconfirmed proposals for a video matching no known client. |

**Also removed at his instruction:** one piece of personal material from `02-Me/discipline.md`. Not described here.

**Standing rule this sets:** a note earns its place by being the current, best record of something. When two notes cover the same ground, the thinner one is merged into the fuller one and deleted — not left as a second version to drift out of date.

**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — It is called the Brain
**Decided:** the system is **the Brain**. Not "the vault".
**Why:** Samuel's instruction. The build spec used "vault" throughout and I inherited it without asking.
**What changed:** 78 occurrences across 36 files, including AGENTS.md, CLAUDE.md, GEMINI.md and conventions. Obsidian's own interface still labels the folder a "vault" — that is Obsidian's word and is noted once in conventions, nowhere else.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — The engine's financial system is the current one, and it becomes active
**Decided:** the Accountability Engine's money system is **not legacy**. Samuel: *"The Engine's financial system is the most up to date and current system, use that system, it has the most current and correct data."* Its rules, pots, obligations, paydays and goals are imported into `03-Areas/finances/` as **active**, and its Google Sheets budget tooling comes with it.
**Why:** he said so, and the dates back him up — the engine's `money.md` was maintained into September 2026, while the percentage-based design in the Claude export dates from 2026-07-16 and was never confirmed as in use.
**What this reverses:** the finance items in `00-System/legacy-review.md` (M1–M8, G2–G5, F3, R6–R8, R12) were marked `unreviewed` pending a keep/change/drop. They are now **kept**. The rest of the legacy review — habits, rituals, patterns, people rules — stays unreviewed.
**Also restored:** `08-Archive/accountability-engine/tools/sheets/` (`build_budget.py`, `sheets.py`, `Code.gs`, `plan.json`, README), deleted earlier the same day in the prune as "build tooling". That was wrong — it is the live budget system. Recovered from git history, which is why history is never rewritten.
**Caveat he stated:** *"though I haven't updated my recent spendings"* — the ledger is behind reality. Numbers carry their own dates and must not be presented as current balances.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — Three finance rules changed, by Samuel, in the Phase 3 interview
**1. Spending log.** The engine's *"every naira in and out logged daily, zero unlogged days"* is replaced: **major spends get their own dated row, minor spends are logged in bulk.** What counts as major is his judgement until he sets a threshold. Objection stated once and not repeated: bulk rows hide where small money goes, and small money is what the personal/misc and household lines are made of.
**2. Rule 7 after the break.** September took NGN 368,041 out of the ring-fenced investment. **It is not refilled** — *"I won't refill it, I would just continue the normal savings."* The pot ends 2026 near NGN 336,959 instead of NGN 705,000. Rule 7's "never pauses" survives; "never touched" now has a precedent.
**3. The second end client has ended.** One end client, one rate, USD 333.33/video. The "August mix" arithmetic across the finance notes is historical.
**Also recorded:** the wedding is self-funded with no budget set yet; and **video volume is not disclosed in advance** — *"I don't know how many videos I would do at the end of the month till pay time."* That makes income forecasting impossible and break-even (~3 videos) the only reliable planning number.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — The finance agent is a financial manager, not a logger
**Decided:** it categorises, summarises, calculates runway, flags rule breaches, writes to the ledger and the sheet, and plans budgets *with* him. His words: *"it is a professional financial manager for me."*
**Limits not asked for but applied**, to be confirmed at the Phase 4 gate: never moves money, never writes a number without a source and a date, never presents a stale balance as current, never stores account credentials, never forecasts income as if the video count were known.
**Who decided:** Samuel, 2026-09-20. Brief: `03-Areas/finances/finance-agent-plan.md`.

## 2026-09-20 — Course paused; Wednesday teaching ended; the brand is what is working
**Course — paused.** Samuel: *"I am pausing the course right now cause I don't have enough time… based on demand, people want a course specially on DaVinci Resolve, and video editing career in general, so I may rebuild the course from ground up."* No recording, no launch. The 16 October beta date is dead. The CapCut curriculum is kept as design, not as a plan. Full course price: still not set.
**Wednesday teaching — ended.** *"I started the Wednesday teaching and stopped cause I didn't have time again and it was no longer relevant to my audience."* Its note is folded into `03-Areas/community/community.md` and deleted. The community now has 20 free members, an admin to be paid NGN 15,000 from end of month, and no scheduled activity.
**The brand grew.** Instagram 460 → **671**, TikTok 550 → **673** in about 25 days. His attribution: a new **storytelling B-roll series** and **narrowing to video-editing content**.
**The pattern across all three, stated once:** the two things that stopped were aimed at a general creator audience; the thing that grew was aimed at video editors. The audience has answered a question he was still deciding by committee.
**The consequence, also stated once:** the finance system needs the course to carry ~NGN 42,530/month from January, and calls it the only income line he controls. Paused, that number has no source, and nothing has replaced it.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-21 — The video-editor is the first agent; its skeleton is built and step 6 is proven
**Decided:** the dedicated video-editing agent session (recommended next action from the 2026-09-20 build-state) runs first. Scope for this session, confirmed by Samuel: **skeleton + prove step 6** — build the agent's files and prove the risky HTML→Fusion bridge on a duplicated timeline, not the whole thing in one pass (his brief: *"not in one pass, and not tonight"*).
**What was built:** `07-Agents/roster.md`, `handoffs.md`, and `07-Agents/video-editor/{profile,memory,log}.md`, plus the `.claude/agents/video-editor.md` wrapper. This is the **first agent in the Brain** and the pattern the others follow (AGENTS.md §7).
**What was proven:** on a duplicate of `Timeline 2` in the reference project, an 8-node house-style card was built programmatically as **editable Fusion nodes** via the Resolve MCP (Resolve 21.1) and rendered over the footage. The step-6 bridge works. No live timeline was touched; Samuel's context was restored.
**Decided along the way:** the "existing ideation skill" the brief refers to **does not exist yet** — the cut-sheet HTML process is it, to be built as a Brain skill. And OGraf HTML (new in Resolve 21) is a step-5 preview aid only, never step-6 output, because Samuel's rule is that visuals are always editable Fusion nodes.
**Still unproven, logged for the next Resolve session:** Fusion **Instance** nodes and the Neo* third-party macros over the bridge (the shine layer), and `ImportFusionComp` with a generated `.setting`. Details in [[07-Agents/video-editor/memory|the agent's memory]].
**Who decided:** Samuel, 2026-09-21.

## 2026-09-22 — The Brain is AI-agnostic: canonical files, generated adapters
**Samuel:** *"I want to ensure that this Second brain I am building is AI agnostic which means it should be able to be used by any AI model or agent that I link to access it."*
**What changed:**
- [[00-System/portability|Portability]] written: three layers (canonical · adapters · tool-private state), the rules, tiers instead of model names, neutral tool names, the linked-AI registry, write tiers, access modes, a boot prompt, and the checklist for linking a new AI.
- **Agent profiles are canonical** and carry `name` / `description` / `tier` / `tools` in neutral terms. `.claude/agents/video-editor.md` is now generated from the profile; everything in the hand-written version was already in the profile.
- **Skills are canonical in `00-System/skills/<name>/<name>.md`** — visible in Obsidian, unique filenames — instead of `.claude/skills/`, which Obsidian hides and only Claude reads.
- `00-System/scripts/build_adapters.py` generates the adapters for **Claude Code** (`.claude/agents/`, `.claude/skills/`) and **Gemini CLI** (`.gemini/agents/`, `.agents/skills/`); `--check` detects drift; `--package` zips a skill for claude.ai. The Gemini formats and tool names were verified against the installed Gemini CLI 0.60.0 docs. Generated Gemini agents are told they are guests and which tools they lack (no MCP servers are connected in Gemini).
- **The four "platform" skills were on disk all along**, in the Claude desktop app's plugin cache behind Windows' packaged-app redirect (`AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\...`). The 2026-09-20 search looked at the un-redirected path. The manifest marks all four `creatorType: user`. Copied in, source untouched, claude.ai sandbox paths translated. `edit-clock` verified running from the Brain. Open question 28 answered.
- The MCP list and the session protocol moved out of CLAUDE.md into canonical files (portability, AGENTS.md §12). CLAUDE.md and GEMINI.md are adapters only. AGENTS.md gains §11.
**Why:** before this, the agent wrapper held content, the skill location was Claude-only, four skills existed only inside claude.ai, and the MCP list and session protocol lived in CLAUDE.md — another AI would have missed all of it.
**Alternatives rejected:** symlinks from `.claude/` to canonical files (unreliable on Windows and in git without Developer Mode); thin pointer adapters (every Claude invocation pays an extra file read); adapters written now for tools not yet linked (their formats unverified — added per tool at link time).
**Suggestion, not Samuel's decision:** a newly linked AI is a *guest* (inbox + logs, `[<tool>]` commit prefix) until he says otherwise. This extends the existing Gemini overflow rule; he can change any AI's tier.
**Who decided:** Samuel set the goal, 2026-09-22. The mechanism is the build's.

## 2026-09-22 — The orchestrator is the main session, not a subagent

**What:** `07-Agents/orchestrator/` built: profile, memory and log. The profile carries `runs-as: main-session`. `build_adapters.py` still validates it but generates **no** subagent file for it. AGENTS.md §12 now tells every AI's main session to follow the orchestrator profile. `06-Logs/commitments.md` created, since AGENTS.md §9 names it and it didn't exist.
**Why:** in Claude Code, a subagent can't launch another subagent. An orchestrator subagent could never route to `video-editor`, so the role has to be played by the session Samuel is talking to. That is also how any AI without native subagents runs it, so the design is the same everywhere.
**Alternatives rejected:** a generated `.claude/agents/orchestrator.md`. It would show up as a choosable subagent that can't do its one job.
**Routing until the other agents exist:** the orchestrator works the finance, personal-life and content domains itself, from the area notes. Table in the [[07-Agents/orchestrator/profile|profile]].
**Who decided:** the build (Phase 4, "orchestrator next" in build state). Mechanism only. No change to anything Samuel decided.

## 2026-09-22 — The Scripnals guide library is tagged entries with a generated JSON export
**Samuel:** *"The guide library should be robust, but well sorted to content types, niches and content formats etc. so that the AI can easy search through and find what he wants. The content library should be in a format that AI's can read easily and can be sorted in a database easily."*
**What changed:**
- `03-Areas/scripnals/guides/` holds one Markdown file per entry (66), in nine kind folders. A flat frontmatter carries six tag fields. The body is the text the AI reads.
- `00-System/scripts/build_scripnals_guides.py` validates every entry against one controlled vocabulary, exports `guides/_export/guides.json` and `vocab.json` (generated, never hand-edited), and simulates the matching rule.
- **Guide entries carry no backlink** to the area, because their body goes straight into the prompt. `guides/guide-library.md` is their link to the area. Exception to AGENTS.md §4 "every note links back", for these files only.
- The approved spec's "one file per folder, no search" becomes "every entry whose tags match", with a word budget. Plus two new inputs, niche and format. That part is a product change, so it is **Proposed** in spec v1.1 until Samuel says yes (open question 80).
**Why:** one file per folder can't sort by niche or format, and one hook file loaded whole wastes words on patterns that don't fit the content type. Markdown stays easy for Samuel to edit. JSON drops into a database or a server's memory with no parsing.
**Who decided:** Samuel asked for the shape (quote above). The mechanism is the main session's. The spec change waits for his yes.
**Correction, 2026-09-22 (same day):** Samuel dropped the niche and format inputs. There are now four tag fields, not six, and 51 entries, not 66: the 10 niches and 7 formats became one note each. The entries were rewritten token-light (budget 2,400 words). His words: [[03-Areas/scripnals/scripnals-decisions|Scripnals decisions]].

## 2026-09-22 — The finance agent is built; its conversations run in the main session

**What:** `07-Agents/finance/`: profile, memory and log, plus a generated `.claude/agents/finance.md`. Skills `payday`, `budget` and `month-close` in `00-System/skills/`, rebuilt from the engine's `paid`, `budget` and `month` (legacy review R6–R8). A live ledger at `03-Areas/finances/money-ledger.md`, opened with the 2026-09-16 position; the engine's ledger stays archived as history. `00-System/scripts/money_ledger.py` totals the ledger so no agent reads it whole. The sheet client moved to `00-System/scripts/sheets.py`, and its queue to `06-Logs/automation/`.

**Samuel's calls, 2026-09-22:**
- **The six hard limits are confirmed**: never moves money · never writes a number without a source and a date · never shows an old balance as current · never stores account details · never forecasts income as if the video count were known · never quietly re-plans around a broken rule.
- **Major spend:** *"Major spends are mostly the ones that get sent or transferred to accounts the week of pay, Minors are just after the main big budgets go out, whats left for me, are minor spends, except, first main shopping."* Rule 2 amended by a dated addition. Open question 61 closed.
- **Delivered videos:** *"My video editing agent should count the projects done so far with there names, and details so that the finance agent can get that knowledge."* The video-editor owns `03-Areas/video-editing/delivered-projects.md` (standing job 8). Finance reads it, never writes it. Open question 62 closed. Gaps: open question 81.
- **Sheet credentials:** he runs a one-line command that copies them from the old engine `.env` into Windows user variables. `sheets.py` reads them from the registry. No secret in the Brain, a file the agent reads, or a chat.

**The build's calls (mechanism only):**
- **Conversations run in the main session.** A subagent can't ask Samuel anything mid-run, so `payday` and `budget` run with the finance profile loaded into the orchestrator (AGENTS.md §7). The subagent does work where every input is in hand: totals, reconciling, scenarios.
- **The bulk-row rhythm:** at each payday, and at the month close. The agent asks for the balance, then derives the minor spends, marked `derived`. Samuel can change the rhythm.
- **A new ledger format:** typed rows (`in`, `major`, `bulk`, `to-pot`, `from-pot`, `charges`, `balance`, `correction`), one line per cell. The engine's paragraph-long cells made the file too expensive to read. A mistake is fixed with a correction note and a minus row.
- **No `spend.jsonl` twin.** The engine kept one for its website, which is gone. The typed table is machine-readable on its own.
- `sheets.py` has no `env` command, and `script` goes to the clipboard, so the token can't land in a transcript.

**Objection, stated once:** under the major-spend definition, a big unplanned spend paid from the leftover (a Kaduna-sized trip) goes in the bulk row with no line of its own. Only pot withdrawals are guaranteed their own row. Recorded; executed as he defined it.

**Who decided:** Samuel for the limits, the definition, the delivered-videos owner and the credentials route. The build for the mechanism.

## 2026-09-22 — A new "Money" sheet, built from the Brain; the old sheet is frozen

**Samuel:** *"I think I need to build a better sheets, this one looks confusing, and for the fact that there is connection issues, what can we do?"* Then: *"I wish to see most things on fewer tabs"* · *"I don't want random text on the sheets, let's see Simple headers, culums, rows and the numbers"* · *"I look at the sheet, If I want to imput anything, I would do it through the Agent here"* · *"Yes, let's get an official setup"*.

**What changed:**
- The sheet is now a **view**. `00-System/scripts/budget_sheet.py` rebuilds a new Google Sheet, "Money", from the ledger, the plan table in `obligations.md` and the goals. Two tabs, Overview and Ledger. Headers and numbers only; negatives in red.
- **The plan lives in the Brain.** The table in `obligations.md` is the only place a plan number lives. The old sheet's Details tab no longer counts. The `budget` skill changes that table, with his yes, and keeps a trace of the old figure.
- **The connection is Google's official Sheets API** with a service account. Its key sits outside the Brain at `%USERPROFILE%\.brain-secrets\budget-sheet-key.json`. It's read by the script only, listed in AGENTS.md §10, and denied to Claude Code's Read tool.
- "My Claude Budget" is frozen as history. `sheets.py` stays for reading it only.
- The plan-vs-actual table starts at 2026-10. September is split across two ledgers and is handled in the September close.

**Why:** the Apps Script web app failed about half its calls. Seven tabs and sentences in cells were confusing. A sheet he never types into doesn't need a mirror that can drift: a rebuild can't disagree with the ledger.

**Alternatives rejected:** keeping the web app with retries (hides the failures, doesn't fix them). Signing in as Samuel through OAuth (unverified apps get tokens that expire after 7 days). Reusing the HighSignals project key on the Desktop (another project's credential, already flagged).

**Who decided:** Samuel for the shape and the official API. The build for the mechanism.

## 2026-09-22 — The Money sheet gets a look, a tab per month, and one owner

**Samuel:** *"make it more aesthetics with colors, better bugger heading, each section has it's own coloring, color coding text, boxes, and sections"* · *"I want everymonth as we go forward to have its's own sheet inside this sheet so I can once in a while check past month and see what I did that month"* · *"If I want to make any adjustment to the sheets in a way, even in the way things are arranged, the financial agent would be the one in charge of all that"*.

**What changed:** `budget_sheet.py` paints every tab. Big title, a coloured band per section, boxed tables, colour-coded numbers, no gridlines. Headers and numbers still only, no sentences. One tab per month from October 2026, newest first. The Overview's month names link to them.

**How past months stay true:** at each close, `budget_sheet.py snapshot YYYY-MM` freezes that month's plan to `03-Areas/finances/plans/plan-YYYY-MM.md`, and its tab reads the frozen copy from then on. Without that, a later plan change would quietly rewrite what an old month had planned. The snapshot is written once and never rewritten. The ledger was already append-only.

**Owner:** the finance agent owns the sheet, numbers and layout. A layout change is a change to `budget_sheet.py`, then a rebuild. Nobody edits the sheet by hand.

**Who decided:** Samuel for the look, the monthly tabs and the ownership. The build for the snapshot mechanism.

## 2026-09-22 — Correction: September gets its own tab; each month has its own plan file

**Samuel:** *"Wait, I need to see September too, where are still in september and some budgetting may still be needed in september, you are showing me only october when that is not our current month"*

**Corrects** the two entries above that started the sheet at 2026-10 and froze plans with `snapshot`.
- **September came into the live ledger.** A 2026-08-31 opening plus the 1–16 Sep rows were transcribed from the old ledger. The ledger's starting position is now its earliest `opening` rows. The 2026-09-16 opening rows became checkpoints: the scripts verify them and don't apply them. The rows add up to every checkpoint exactly, and to the old Dashboard's September totals (NGN 1,373,937 in, NGN 1,273,708 spent). No row was edited.
- **Each month has its own plan file,** `03-Areas/finances/plans/plan-YYYY-MM.md`. September's is the 2 Sep replan plus his 16 Sep cuts, with each change and whose call it was. `obligations.md` is the standing plan a month starts from. The running month's plan can change, with a trace. At the close it is frozen (`freeze`) and never edited again. `snapshot` is gone.
- Checkpoint rows and correction notes stay in the Brain but don't show on the sheet.

**Who decided:** Samuel for seeing September and budgeting it. The build for the mechanism.

## 2026-09-22 — Two checks to keep Samuel's spending in check

**Samuel:** *"You can see I spend out of hand, I need the Financial agent to keep me in check"* Then: *"yes to the split, and both checks"*.

**What:** skill `money-check` (before any off-plan spend: which line pays, what's left after, a verdict in three lines, and he decides) and skill `sunday-check` (every Sunday: his balance, the gap logged, every line over plan named). Both are in `06-Logs/commitments.md`, the first entries there. `budget_sheet.py left` gives the numbers for both without reading the ledger. `money-check` is the Phase 4 job skill of that name, built early for finance.

**Also agreed:** the rest of September. Church / transport NGN 10,000 · eating out NGN 10,000 · extra cash NGN 15,000. What's left on 30 Sep (NGN 26,567) goes back into the Buffer, and the NGN 10,000 loan follows when repaid.

**No penalty.** Self-enforced penalties *"don't work"* ([[02-Me/stakes-and-accountability|stakes and accountability]]). A missed check is named once, in his words.

**Who decided:** Samuel for the checks and the split. The build for the skills.

## 2026-09-22 — First automation: the Sunday money check

**Samuel:** *"Add a routine that activates the Sundays feedback session with the Agent"*

**What:** a scheduled task in the Claude desktop app, `sunday-money-check`, every Sunday at 3:00pm WAT. It opens a session that runs `sunday-check`. The canonical copy of its prompt and schedule is `00-System/automations/sunday-money-check.md`; the app's task file is a tool copy (AGENTS.md §11 rule 1).

**Why this and not a cloud routine:** the check needs his answer (his balance), the sheet key outside the Brain, and his PC's Python. A cloud routine has none of those. A TickTick reminder would only remind; this opens the conversation.

**Why 3:00pm:** his Sunday rule, *"Plan Sunday from 3:00pm"* ([[02-Me/spirit|Spirit]]).

**Limit, stated once:** it runs only while the app is open. If the app is closed, it runs at the next launch.

**Who decided:** Samuel asked for the routine. The time comes from his own rule. The mechanism is the build's.
