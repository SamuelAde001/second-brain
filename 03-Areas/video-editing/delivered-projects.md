---
type: knowledge
area: video-editing
status: needs-input
updated: 2026-09-22
source: manual
tags: [clients, delivered, income]
---

# Delivered projects

Every client video delivered so far, one row per video. The **video-editor agent owns this file** — it is the only one that writes to it. The **finance agent reads it, never writes it**, so a month's income is a lookup on invoice day instead of a recall (see [[03-Areas/finances/income|Income]] — nothing did this before 2026-09-22). **Append-only**: a wrong row is never edited or deleted — a dated correction line goes under the table instead.

## Delivered videos

| # | Project | End client | Via | Delivered | Rate USD | Batch | Source |
|---|---------|-----------|-----|-----------|----------|-------|--------|
| 1 | name unknown | Alex | Route Rise | — | 333.33 | 2026-05 | [[03-Areas/finances/income|Income]] |
| 2 | name unknown | Alex | Route Rise | — | 333.33 | 2026-05 | [[03-Areas/finances/income|Income]] |
| 3 | name unknown | Alex | Route Rise | — | 333.33 | 2026-05 | [[03-Areas/finances/income|Income]] |
| 4 | name unknown | Alex | Route Rise | — | 333.33 | 2026-05 | [[03-Areas/finances/income|Income]] |
| 5 | name unknown | Alex | Route Rise | — | 333.33 | 2026-05 | [[03-Areas/finances/income|Income]] |
| 6 | name unknown | Alex | Route Rise | — | 333.33 | 2026-06 | [[03-Areas/finances/income|Income]] |
| 7 | name unknown | Alex | Route Rise | — | 333.33 | 2026-06 | [[03-Areas/finances/income|Income]] |
| 8 | name unknown | Alex | Route Rise | — | 333.33 | 2026-06 | [[03-Areas/finances/income|Income]] |
| 9 | name unknown | Alex | Route Rise | — | 333.33 | 2026-06 | [[03-Areas/finances/income|Income]] |
| 10 | name unknown | Alex | Route Rise | — | 333.33 | 2026-07 | [[03-Areas/finances/income|Income]] |
| 11 | name unknown | Alex | Route Rise | — | 333.33 | 2026-07 | [[03-Areas/finances/income|Income]] |
| 12 | name unknown | Alex | Route Rise | — | 333.33 | 2026-08 | [[03-Areas/finances/income|Income]] |
| 13 | name unknown | Alex | Route Rise | — | 333.33 | 2026-08 | [[03-Areas/finances/income|Income]] |
| 14 | name unknown | second end client (unnamed) | Route Rise | — | 175 | 2026-08 | [[03-Areas/finances/income|Income]] |
| 15 | name unknown | second end client (unnamed) | Route Rise | — | 175 | 2026-08 | [[03-Areas/finances/income|Income]] |
| 16 | Andy video (Sep #1) — logged earlier as "Client #3" | Andy | Route Rise | 2026-09-08 | 333.33 | 2026-09 | [[08-Archive/accountability-engine/context/ledger-notes/2026-09|Accountability Engine — Sep 2026 ledger notes (archived)]] |
| 17 | Alex video (Sep #2) | Alex | Route Rise | — | 333.33 | 2026-09 | [[08-Archive/accountability-engine/context/ledger-notes/2026-09|Accountability Engine — Sep 2026 ledger notes (archived)]] |

Rows 1–15 come from the batch-count table in [[03-Areas/finances/income|Income]] (May 5 / June 4 / July 2 / August 4 videos), confirmed by Samuel 2026-09-20 as the live record. No video names, individual delivery dates or per-video splits exist anywhere in the Brain for May–July, so those rows carry `name unknown` and `—`. The single-rate assumption for May–July (all USD 333.33, one end client) follows directly from the source: the second end client is stated as "new August 2026" — before that there was one client at one rate. August's 2+2 split and both rates are stated explicitly in [[03-Areas/finances/income|Income]].

Rows 16–17 come from the archived Accountability Engine, which recorded two named deliveries inside a "4–14 Sep, routines dark" stretch: Andy's video (TickTick shows the render ticked **2026-09-08**; no formal delivery date was logged) and Alex's video (due 2026-09-10, delivery date never logged). The USD 333.33 rate on both is explicit in the source ("same rate as Andy"). **Neither row is in [[03-Areas/finances/income|Income]]'s batch table** — that table stops at August — so this is new information for finance, not a duplicate.

## Gaps — not yet reconciled

1. **Who is "Andy"?** The archived ledger calls Andy "the old client" at the same USD 333.33 rate as Alex. [[03-Areas/finances/income|Income]] and every current client note describe only two end clients ever: Alex (USD 333.33, "the original end client") and an unnamed second end client (USD 175, "new August 2026", ended). Andy at USD 333.33 fits neither description cleanly. This is the same unresolved tension [[03-Areas/video-editing/clients/routerise|Routerise]] already flags: Samuel called it "one client called Alex" on 2026-09-20; the engine's record says two, differently named. Not resolved here either — flagged, not guessed.
2. **Two more named-but-unplaced deliveries exist in the same archive**: "Client #1" (delivered 2026-08-26) and "Client #2" (started 2026-08-27, delivered 2026-09-02) — the numbering used before the Sep rename to Andy/Alex. They are **not** added as rows here because they can't be safely matched to 2 of the August batch's 4 "name unknown" rows without guessing — Client #2's delivery date falls in September even though the work started in August, and neither source says which rate applied. Adding them as new rows risked double-counting against the August batch of 4 already in the table.
3. **A video was in progress, not delivered, as of the last dated source**: "Alex video (Sep #3)", started 2026-09-15, due 2026-09-18 (archived ledger). The video-editor agent's own [[07-Agents/video-editor/memory|memory]] shows sync work on footage titled *"1. Taking a step back from Claude (and why you should too)"* as of 2026-09-21 — possibly the same job, not confirmed. Excluded from the table: no delivery is recorded anywhere.
4. **September is incomplete.** The archive stops mid-month; anything delivered between 2026-09-16 and today (2026-09-22) is not in this file because nothing recorded it. That gap is exactly what the "How a delivery gets recorded" rule below exists to close from now on.

## How a delivery gets recorded

When Samuel says a video is delivered, **one row is appended the same day** — never a backfill batch, never an edit to an existing row.

Ask him, in order, for whatever isn't already obvious from context:
1. The project name (or confirm it stays `name unknown`).
2. The end client (Alex, or whichever end client Route Rise assigned it to).
3. The delivery date.

**The rate is never asked and never guessed** — it comes from [[03-Areas/video-editing/clients/alex|clients/]] and [[03-Areas/finances/income|Income]], the standing USD 333.33 rate unless Samuel states a different one is in effect. `Via` defaults to Route Rise unless he says otherwise. `Batch` is the calendar month whose end-of-month invoice will cover the video, per [[03-Areas/video-editing/workflow|the workflow]] — normally the month the video is delivered in.

A mistake in an existing row gets a new, dated line right here, never a silent edit:

- (none yet)

Back to [[03-Areas/video-editing/video-editing|Video editing]]
