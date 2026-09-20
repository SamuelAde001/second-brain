---
type: decision
area: system
status: active
updated: 2026-09-20
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

