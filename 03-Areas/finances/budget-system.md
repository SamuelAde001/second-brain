---
type: knowledge
area: finances
status: active
updated: 2026-09-20
source: legacy-accountability-engine
tags: [budget, spreadsheet]
---

# The budget system — "My Claude Budget"

The live system, confirmed by Samuel 2026-09-20. A Google Sheet called **"My Claude Budget"**, created 2026-08-26 and last modified **2026-09-16**.

It was moved to Google Sheets so Claude Code could write it directly instead of Samuel typing updates by hand.

**Tabs:** Dashboard · Setup · Income · Expenses · Transfers · Budget · Details. It covers **August 2026 – July 2027**, so it reaches both goals.

## The ledger is the source of truth, not the sheet

The engine's `context/money-ledger.md` is the text record. **The sheet is the budgeting layer; the ledger is the record. If the two disagree, the ledger wins** — Rule 6 in [[money-rules]].

That is not theoretical: the sheet and the ledger currently disagree about Cowrywise by NGN 368,041. See [[pots-and-accounts]].

## The design rule that fixed the old sheet

> **Nothing is typed on the Budget or Dashboard tabs.**

Budget's plan column reads Details. Its month columns read Expenses. Its savings block reads Transfers — all through `SUMIFS`. **A budget line cannot claim money moved when no row exists.**

That was the entire bug in the old sheets, and it is what let NGN 900,250 be booked to savings when only NGN 305,000 existed.

The Dashboard says it on its own face:

> *"Nothing is typed on this sheet. If a number here is wrong, the row that is wrong is on Income, Expenses or Transfers."*

## The Details tab

Answers "what is this category actually made of" — every subscription, every line, with amount, due day, tier and payday. **It is the only place a plan number is typed.**

**Cancelled items go Active = No. They are never deleted** — a subscription that reappears in three months is a pattern, and a deleted row hides it.

## How Claude writes it

Through `tools/sheets/` in the engine repo — an **Apps Script web app bound to the sheet**. Credentials live in a gitignored `.env` that was never copied into the Brain.

- `tools/sheets/README.md` — setup and security
- `tools/sheets/plan.json` — the line items behind every category
- `tools/sheets/build_budget.py` — rebuilds the Budget and Details tabs from `plan.json`
- `tools/sheets/Code.gs` — the Apps Script itself

Archived at `08-Archive/accountability-engine/tools/sheets/`. *(These files were deleted in the 2026-09-20 prune as "build tooling" and restored from git history the same day once Samuel confirmed this system is live. They are not build artifacts — they are the budget system.)*

## What the Dashboard shows

Read 2026-09-16, with the live figures in [[pots-and-accounts]]:

- **Where the money is** — bank liquid, Goal 1, emergency fund, Cowrywise investment, buffer, and "SAVED TOWARD THE GOAL" which deliberately excludes the investment and the buffer.
- **Goal 1 and Goal 2 progress** — target, saved, still to find, months remaining, and **needed per month from here**. That last one is the honest number: *"If this number keeps going up, the month is being lost."*
- **Reality check** — obligations floor NGN 936,800, plus the NGN 100,000 investment, so **committed outflow NGN 1,036,800/month**, and the income needed to hit the goal: **NGN 1,291,313/month**.
- **What the client mix produces** — 4 videos clears it, the August mix clears it, 2 videos is short by NGN 381,322.
- **Month by month** — income in, spent, surplus, and what moved to each pot. September 2026: **income NGN 1,373,937, spent NGN 1,273,708, surplus NGN 100,229.**
- **THE MONTH MUST BALANCE** — bills + one-offs + every pot = income, exactly.

## The earlier percentage design — not adopted

A different budget was designed on 2026-07-16 in a Claude chat: fixed buckets of Savings 20%, Business 20%, Building Project 27.7%, with the remaining 32.3% split across expense categories, built as an `.xlsx` with `openpyxl` for import into Google Sheets.

**It was never adopted.** The 32.3% split was never finalised, and Samuel confirmed on 2026-09-20 that the engine's system is the current one. The percentage design is recorded here in one paragraph rather than kept as a second, competing budget note.

One thing from it is worth carrying: his instruction on how the sheet should behave when allocation is wrong.

> *"I don't want any pop up messages, in fact, allow the allocation to me more than 100%, let me see it in red when it is more than 100% so I can adjust."*

**No blocking validation. Colour is the only signal.** Apply that to anything built for him.

Related: [[money-rules]] · [[obligations]] · [[income]] · [[pots-and-accounts]]. Back to [[03-Areas/finances/finances|Finances]]
