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

**Added 2026-09-22 — one starting position.** The starting position is the set of `opening` rows with the **earliest** date. A later `opening` row is a **checkpoint**: the scripts check the rows add up to it at the end of its day, and never apply it. That is how September 2026 came in from the old ledger without editing a row.

Pot names, exactly: `Goal 1`, `Buffer`, `Cowrywise investment`, `Emergency fund`, `Goal 2`.

**Category** for a spend row is a line from that month's plan (`03-Areas/finances/plans/plan-YYYY-MM.md`, or the standing plan in [[obligations]] if the month has none), exactly as written there (`Building project`, `Feeding`, `Kaduna trip`…), or `Other` if none fits. That is how the sheet matches spending to the plan.

Totals by script, never by reading the whole file: `python 00-System/scripts/money_ledger.py totals 2026-10` · `pots` · `last 10`.

## Ledger

| Date | Type | NGN | What | Category | Note |
|---|---|---|---|---|---|
| 2026-09-16 | opening | 174,732 | Bank | — | derived in old ledger after Payday B transfers; not screenshot-verified. NGN 57,532 of it unassigned, his call |
| 2026-09-16 | opening | 146,041 | Goal 1 | Goal 1 | old ledger, moved on Payday B 2026-09-16 |
| 2026-09-16 | opening | 50,000 | Buffer | Buffer | old ledger, moved on Payday B 2026-09-16 |
| 2026-09-16 | opening | 36,959 | Cowrywise investment | Cowrywise investment | his words 2026-09-15, after the NGN 368,041 Kaduna withdrawal. The sheet still says 405,000 |
| 2026-09-16 | opening | 0 | Emergency fund | Emergency fund | starts January 2027 |
| 2026-09-22 | correction | — | 2026-09-16 opening rows: now checkpoints. September 1–16 brought in from the old ledger: 2026-08-31 opening + the rows below | — | Samuel asked to see September (2026-09-22). Rows transcribed from 08-Archive/accountability-engine/context/money-ledger.md; they add up to the 2026-09-16 checkpoints exactly |
| 2026-08-31 | opening | 2,503 | Bank | — | his words: unchanged 27 Aug–1 Sep, backfilled at his confirmation; old ledger |
| 2026-08-31 | opening | 0 | Goal 1 | Goal 1 | old ledger: first money moved 2026-09-16 |
| 2026-08-31 | opening | 0 | Buffer | Buffer | old ledger: first money moved 2026-09-16 |
| 2026-08-31 | opening | 305,000 | Cowrywise investment | Cowrywise investment | old ledger, 2026-08-26 opening |
| 2026-08-31 | opening | 0 | Emergency fund | Emergency fund | starts January 2027 |
| 2026-09-02 | bulk | 2,360 | Recharge cards | Data / airtime | his words: NGN 2,000 for someone else + NGN 360, days not given; old ledger 2026-09-02 |
| 2026-09-02 | in | 962,228 | Route Rise, August batch 70% | — | USD 711.66 gross, USD 706.66 net × NGN 1,361.66 (Cleva); bank confirmed; old ledger 2026-09-02 |
| 2026-09-02 | major | 500,000 | Building project | Building project | his words; old ledger 2026-09-02 |
| 2026-09-02 | major | 100,000 | Son's school | Son's school | his words; old ledger 2026-09-02 |
| 2026-09-02 | to-pot | 100,000 | Cowrywise | Cowrywise investment | Rule 3 kept: Payday A; old ledger 2026-09-02 |
| 2026-09-02 | major | 50,000 | Girlfriend allowance | Girlfriend allowance | his words; old ledger 2026-09-02 |
| 2026-09-02 | charges | 584 | Transfer charges | Other | NGN 250 on Cowrywise + NGN 334 not attributed; derived from balance; old ledger 2026-09-02 |
| 2026-09-03 | major | 15,000 | Google | Subscriptions | his words; old ledger 2026-09-03 |
| 2026-09-03 | bulk | 2,500 | Recharge card | Data / airtime | his words; old ledger 2026-09-03 |
| 2026-09-03 | major | 26,000 | Gym clothes | Gym clothing | his words; old ledger 2026-09-03 |
| 2026-09-03 | major | 51,150 | First main shopping | Feeding | his words, a total only: one bag, feeding + household + personal, not split; old ledger 2026-09-03 |
| 2026-09-03 | charges | 1,003 | Bank charges | Other | his words "probably bank charges"; derived; old ledger 2026-09-03 |
| 2026-09-15 | from-pot | 368,041 | Kaduna trip | Cowrywise investment | his words: "kaduna was more expensive that plan and I ended up taking out of my Inestment money to fund Kaduna"; Rule 7 broken; logged late; old ledger 2026-09-15 |
| 2026-09-15 | bulk | 430,011 | Kaduna trip | Kaduna trip | Tehila Foundation meeting, 4–15 Sep, not itemised; derived at the 16 Sep budget check; old ledger 2026-09-16 |
| 2026-09-15 | bulk | 30,000 | Gym membership | Health — gym | derived: taken at plan; old ledger 2026-09-16 |
| 2026-09-15 | bulk | 10,000 | Transport | Transport | derived: taken at plan; old ledger 2026-09-16 |
| 2026-09-15 | bulk | 1,600 | Spotify | Subscriptions | derived: taken at plan; old ledger 2026-09-16 |
| 2026-09-15 | bulk | 5,000 | Haircut + garri | Personal / misc | derived: taken at plan; old ledger 2026-09-16 |
| 2026-09-15 | bulk | 3,500 | Chicken meal | Feeding | his words, reported 16 Sep; old ledger 2026-09-15 |
| 2026-09-16 | in | 411,709 | Route Rise, August batch 30% | — | USD 303.21 net × NGN 1,357.83 (Cleva); old ledger 2026-09-16 |
| 2026-09-16 | to-pot | 146,041 | Goal 1 | Goal 1 | Rule 3 kept: Payday B; old ledger 2026-09-16 |
| 2026-09-16 | to-pot | 50,000 | Buffer | Buffer | Rule 3 kept: Payday B; old ledger 2026-09-16 |
| 2026-09-16 | major | 40,000 | Kemi, repayment 1 of 2 | Sister's debt | his words; NGN 50,000 still owed, no date; old ledger 2026-09-16 |
| 2026-09-16 | major | 5,000 | Clothes wash | Chores / household | his words; old ledger 2026-09-16 |
| 2026-09-18 | major | 28,500 | Google (upgrade for Flow) | Subscriptions | his words: "I had to increase my google subscription because of the work I was doing needed me to use Flow, and my google plan wasn't enough"; dated 18 Sep by him. The old NGN 15,000 plan was already paid 2026-09-03 |
| 2026-09-21 | from-pot | 50,000 | Buffer withdrawal | Buffer | his words: "So I withdrew the 50k, I had in buffer yesterday, it is now in my account"; reason not given, asked 2026-09-22 |
| 2026-09-22 | major | 16,850 | Household shopping | Chores / household | his words; day not given (16–22 Sep); first main shopping of the Payday B cycle |
| 2026-09-22 | bulk | 3,500 | Chicken | Feeding | his words; day not given; asked whether this is the 2026-09-15 chicken meal again |
| 2026-09-22 | major | 1,700 | YouTube Premium | Subscriptions | his words; bills on the 17th; debit day not given |
| 2026-09-22 | major | 33,500 | Claude | Subscriptions | his words; bills on the 16th; was not in the 2026-09-16 derived balance |
| 2026-09-22 | bulk | 30,000 | Girlfriend's data subscription | Girlfriend — extra | his words: she ran out of data; may recur next month if she gets no gig |
| 2026-09-22 | bulk | 5,000 | Food at home, for girlfriend | Girlfriend — extra | his words; day not given |
| 2026-09-22 | bulk | 10,000 | Loan to a friend | Loan to a friend | his words: to be paid back at the end of the month. When repaid, log a minus row in this category |
| 2026-09-22 | bulk | 3,500 | Sister, for her child's birthday | Gifts | his words; day not given |
| 2026-09-22 | bulk | 17,000 | Friend's birthday gift | Gifts | his words; day not given |
| 2026-09-22 | bulk | 7,700 | Restaurant food | Eating out | his words; day not given |
| 2026-09-22 | bulk | 5,000 | Girlfriend's hair | Girlfriend — extra | his words; day not given |
| 2026-09-22 | bulk | 915 | Unaccounted (probably transfer charges) | Other | derived: NGN 61,567 (his words, live) against the rows; not confirmed |
| 2026-09-22 | balance | 61,567 | Bank | — | his words: "What is in my bank account now live is 61,567" |
| 2026-09-22 | correction | — | 2026-09-21 from-pot Buffer 50,000: reason now given | — | his words: "Well, I had only 6k or so left in my account, and I know I still need money for some things that may come up before Spetember ends, so we can plan on them" |
| 2026-09-22 | correction | — | 2026-09-22 bulk Chicken 3,500: eating out, not feeding | — | his words: "The chicken is just part of me eating out once a while". Fixed by the two rows below |
| 2026-09-22 | bulk | -3,500 | Chicken (moved to Eating out) | Feeding | reverses the 2026-09-22 Chicken row |
| 2026-09-22 | bulk | 3,500 | Chicken | Eating out | his words: "The chicken is just part of me eating out once a while" |
| 2026-09-22 | correction | — | 2026-09-22 bulk Unaccounted 915: transfer charges | — | his words: "Yes all tranfer charges". Fixed by the two rows below |
| 2026-09-22 | bulk | -915 | Unaccounted (moved to charges) | Other | reverses the 2026-09-22 Unaccounted row |
| 2026-09-22 | charges | 915 | Transfer charges, 16–22 Sep | Other | his words: "Yes all tranfer charges" |
| 2026-09-22 | bulk | 15,000 | Girlfriend's light bill (part 1 of 20,000 sent) | Extra cash | his words: "I just sent her 20k now"; she asked for 30,000; money-check said doesn't fit |
| 2026-09-22 | bulk | 5,000 | Girlfriend's light bill (part 2 of 20,000 sent) | Eating out | same transfer; Extra cash only had 15,000, rest from Eating out (Rule 8 cut order) |
| 2026-09-22 | in | 7,000 | Gift from someone | — | his words: "I recieved a 7k money from someone yesterday as a gift"; told 2026-09-23; NGN taken from "7k"; giver not named |

Back to [[03-Areas/finances/finances|Finances]]
