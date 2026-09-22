---
type: log
area: finances
status: active
updated: 2026-09-22
source: legacy-accountability-engine
tags: [ledger, money]
---

# Money ledger

**The record of what actually moved.** Rule 6: the ledger is the truth, the sheet is a plan. If the two disagree, the ledger wins ([[money-rules]]). Written by the [[07-Agents/finance/profile|finance agent]].

**Append-only.** Newest at the bottom. A wrong row is never edited: add a `correction` row that says which row it corrects and what the right figure is.

History up to 2026-09-16 stays in the old ledger: [[08-Archive/accountability-engine/context/money-ledger|engine money ledger]]. The `opening` rows below carry its last position forward.

## How a row is written

- **One line per cell, short.** The explanation goes in [[03-Areas/finances/finances-log|the finance log]], not here. The old ledger's paragraph-long cells cost a fortune to load.
- **Amounts in NGN, digits with commas, no symbol**, like `174,732`. A USD amount goes in the Note with its rate.
- **Every row says where the figure came from** in the Note: `screenshot`, `his words`, `derived`, or `sheet`. A row with no source is not written.
- **Minor spends are never invented to make a month balance.** If he can't give a bulk figure, the gap stays a gap.

| Type | Use it for |
|---|---|
| `opening` | The starting position carried in from the old ledger. `What` = the pot or `Bank` |
| `in` | Money landed in NGN. The Note has USD gross/net, the Cleva rate, the batch and stage (70% or 30%) |
| `major` | A **major** spend: a transfer or payment sent in the week of pay, or the first main shopping. Its own row, the day it happens |
| `bulk` | **Minor** spends: everything spent from what's left after the week-of-pay budgets go out. One row per period. `What` = the date range |
| `to-pot` | Money moved into a pot. `Category` = the pot name |
| `from-pot` | Money taken out of a pot. Rule 2: logged the same day, with the reason in his words |
| `charges` | Bank charges he can't attribute to a named transfer |
| `balance` | A balance he reported. `NGN` = the balance, `What` = the account nickname. It moves no money |
| `correction` | Says an earlier row was wrong. `What` names that row by date and type; `NGN` is `—`. The money fix is a second row of the same type as the wrong one, with a minus amount (e.g. `-2,000`) |

Pot names, exactly: `Goal 1`, `Buffer`, `Cowrywise investment`, `Emergency fund`, `Goal 2`.

Totals by script, never by reading the whole file: `python 00-System/scripts/money_ledger.py totals 2026-10` · `pots` · `last 10`.

## Ledger

| Date | Type | NGN | What | Category | Note |
|---|---|---|---|---|---|
| 2026-09-16 | opening | 174,732 | Bank | — | derived in old ledger after Payday B transfers; not screenshot-verified. NGN 57,532 of it unassigned, his call |
| 2026-09-16 | opening | 146,041 | Goal 1 | Goal 1 | old ledger, moved on Payday B 2026-09-16 |
| 2026-09-16 | opening | 50,000 | Buffer | Buffer | old ledger, moved on Payday B 2026-09-16 |
| 2026-09-16 | opening | 36,959 | Cowrywise investment | Cowrywise investment | his words 2026-09-15, after the NGN 368,041 Kaduna withdrawal. The sheet still says 405,000 |
| 2026-09-16 | opening | 0 | Emergency fund | Emergency fund | starts January 2027 |

Back to [[03-Areas/finances/finances|Finances]]
