---
type: knowledge
area: finances
status: needs-input
updated: 2026-09-20
source: claude-export
tags: [budget, spreadsheet]
---

# Budget system — percentage-based, automated

From the chat `01-Inbox/_imports/processed/shortlist/finances/2026-07-16-percentage-based-budget-system-with-automated-calculations.md`, 2026-07-16.

## The problem Samuel was solving

His existing Google Sheets budget used fixed manually-typed amounts per category and, in his words, "is not good enough for my financial discipline." His income varies month to month, so he wanted a system where money entering the sheet is automatically divided into buckets by **percentage**, not typed in by hand.

## The three fixed buckets — his decision

Stated directly by him, 2026-07-16:

> "I want to have 20% for savings, 20% for business, 27.7% for building project."

- **Savings — 20%**
- **Business — 20%**
- **Building Project — 27.7%**
- **Remaining 32.3%** — split across expense categories (rent/feeding/family/etc.)

The specific categories and percentages that make up the remaining 32.3% were **never finalized by Samuel in this chat**. The categories used in the built spreadsheet (Tithe, Feeding, Family Support, and others, adding to 32.3%) were the assistant's placeholder example, explicitly flagged as such: "you'll rename/resize these to match your real life, since only you know how much ... [each] should actually get." Treat those specific sub-percentages as **not decided** — see needs-input below.

## What his existing sheet actually tracked (as of 2026-07-16)

Read from his own screenshots, not invented. Two categories of recurring buckets already existed on his old sheet:

**Personal category items:** Tithe, Savings, Dad, My Babe, Building Project, My money, Kemi, Gaming, Mom, Jos, Emergency funds, Givings. A later version of the sheet added: Feeding, TP, Wedding, Misc, Brand support, Clothing, Workers Salary.

**Business category items:** Capcut Pro, Canva, YouTube Premium, Editor, Google Sub, Data and recharge, HighSignals Devs.

**Business recurring payments** (from the sheet, no date range given beyond "as of 2026-07-16"): Google Sub NGN 23,000 (30th) · Data/recharge NGN 10,000 · Capcut Pro NGN 10,000 (14th) · X Premium NGN 8,000 (5th) · Canva Pro NGN 2,800 (22nd) · YouTube Premium NGN 1,700 (14th).

**Personal recurring payments:** Parents NGN 100,000 · Gym NGN 30,000.

## Income structure — his own words

> "My income comes in two batches. They don't pay me 100% income immediately, at the month end, I get paid 70% and at the middle of the next month I get paid 30% remaining."

He also gets irregular "extra income" from other streams. His income is USD-denominated ("my income is always in Dollars") and needs converting to NGN for the budget.

## What tool this runs in

The original ask was a **prompt for Gemini inside Google Sheets** to build the system. Partway through, Samuel switched the request: "Create for me a ready-made .XLSX file with everything you have said." The assistant built the workbook directly with `openpyxl` (Excel-compatible formulas, data validation, conditional formatting, named ranges) rather than writing a Gemini prompt, and the intended path is:

**File → Import → Upload → "Replace spreadsheet" or "Insert as new sheet"** to bring it into Google Sheets. Conditional formatting and data validation are stated to carry over on import, with the caveat that Google Sheets sometimes turns a hard-reject validation into a soft warning.

One feature — auto-filling today's date when a Date cell is clicked in the Expense Log — cannot live in an xlsx file, since xlsx can't execute code. It ships separately as a short Google Apps Script (`onSelectionChange` trigger) meant to be pasted into Google Sheets under **Extensions → Apps Script** after import. It watches the Expense Log's date column and stamps the current date into any blank cell clicked.

**Status: not confirmed whether Samuel has actually imported this into Google Sheets or is using it day to day.** No source states that. See needs-input.

## How the automation works

**Income Log.** Each income entry gets: source, currency (USD/NGN dropdown), original amount, an exchange rate (entered per row, not one shared global cell — so a rate change doesn't retroactively alter old entries), the calculated NGN amount, and a "Received? Yes/No" dropdown. Two totals are kept side by side: total **expected** income for the month (every row) and total **received** income so far (only rows marked Yes).

**Category / Bucket Allocation table.** One row per bucket (Savings, Business, Building Project, plus the expense categories), each with: percentage, **Allocated Budget** (= total expected income × percentage), **Budgeted** (pulled from the Budget Planner — money pre-planned for that category), **Unallocated**, **Expenses** (pulled live from the Expense Log via `SUMIF` matching on category), **Remainder** (Allocated − Expenses).

**Budget Planner.** A separate table for planning ahead — e.g. "Rice & Beans — NGN 20,000 — Feeding" — distinct from the Expense Log, which only records money actually spent. Planned vs. actual are two different numbers, each with its own remainder, matching what Samuel originally asked for.

**Expense Log and Budget Planner category dropdowns are self-updating** — both pull live from the Bucket Allocation table's category column, so renaming, adding, or removing a bucket updates every dropdown automatically with nothing retyped.

**The 70/30 cash-timing fix.** Because only part of expected income has usually landed, the system tracks two parallel numbers:
- **Budget Remainder** — based on the full expected month's income. Answers "is my plan on track."
- **Cash Balance** — based only on income marked Received. Answers "what's physically in my account."

A **Receipt Ratio** (Received ÷ Expected) scales every bucket's "Cash Available" proportionally as more income lands, so a bucket doesn't show money as safe to spend before it has actually arrived. This is described as an approximation — "it's not a perfect cash-flow model since it assumes proportional income distribution rather than lump payments to specific buckets" — not a full date-based cash waterfall.

**Percentage lock — reversed on Samuel's instruction.** The first build hard-blocked any entry that would push total allocation over 100% (a rejecting data-validation popup). Samuel rejected this:

> "It's giving me an error when the allocation percentage is not correct, I don't want any pop up messages, in fact, allow the allocation to me more than 100%, let me see it in red when it is more than 100% so I can adjust."

Final behavior: no blocking validation anywhere. The TOTAL % cell in the Category table turns **green at ≤100%, red at >100%** — color is the only signal.

**Conditional formatting (final state):** a category's Budgeted cell turns red if it exceeds its Allocated Budget; its Expenses cell turns red if it exceeds Allocated; Remainder and Cash Remainder turn red if negative.

**Dashboard — simplified on Samuel's instruction.** He said the first dashboard was "too complex and complicated," with words "hard to understand," and asked for "less complex" and "more user friendly." It was cut from 10 rows to 6, jargon removed:

| Old label | Final label |
|---|---|
| Total Income (Expected, Full Month) | Income This Month |
| Total Income (Received So Far) | Received So Far |
| Receipt Ratio (% of month received) | % Received |
| Total Expenses (Actual Spend) | Spent So Far |
| Budget Remainder (Full-Month Plan) | Left In Plan |
| CASH BALANCE (actual) | **CASH IN HAND** — the headline number, bold and gold-highlighted |

Rows duplicating the Category table (Total % Allocated, Total Allocated Budget, Total Budgeted) were dropped from the dashboard entirely.

## Worked example built into the sheet (demo data, not live figures)

Exchange rate NGN 1,600/USD. Income: USD 312.5 → **NGN 500,000** expected for the month, split as the 70/30 real-world pattern (received NGN 350,000 = 70%, pending NGN 150,000 = 30%, landing mid-following month).

Feeding bucket in the demo:
- Allocated Budget: NGN 30,000
- Budgeted (planned — "Rice & Beans"): NGN 20,000
- Unallocated: NGN 10,000
- Expense logged: NGN 8,000
- Remainder (full-month plan): NGN 22,000
- Cash Available (at 70% Receipt Ratio): NGN 21,000
- **Cash Remainder (actually safe to spend right now): NGN 13,000**

Whole-sheet reconciliation in the demo: total Cash Available NGN 350,000 (matches received income), total Cash Remainder **NGN 342,000** (= received NGN 350,000 − the one logged expense of NGN 8,000 in the demo data).

## needs-input

- The exact categories and percentages making up the 32.3% "remaining" bucket — never confirmed by Samuel, only proposed as an example.
- Whether this system was actually moved into Google Sheets and is in current use as of 2026-09-20.
- Whether the Apps Script auto-date snippet was ever pasted in.
- Current NGN↔USD exchange rate in use (the 1,600 figure above is from the worked example only, dated 2026-07-16 — not a standing rate).

Not yet added to `00-System/open-questions.md` — out of scope for this pass; flag for that file.

Back to [[03-Areas/finances/finances|Finances]]
