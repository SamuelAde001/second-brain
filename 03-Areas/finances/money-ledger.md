---
type: log
area: finances
status: active
updated: 2026-09-23
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

Pot names, exactly: `Goal 1`, `Buffer`, `Investment fund`, `Emergency fund`, `Goal 2`. `Cowrywise investment` is history only: from 2026-09-28 Cowrywise savings is part of the `Buffer` and the locked investment is the `Investment fund`.

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
| 2026-09-23 | bulk | 5,000 | Sent to someone who needed it | Extra cash | his words: "I sent 5k to someone that really needed it just now"; NGN taken from "5k"; recipient not named; told after, not asked first; covered by the 2026-09-22 NGN 7,000 gift |
| 2026-09-23 | correction | — | 2026-09-22 bulk Loan to a friend 10,000: not a loan, given | — | his words: "It is not coming back, also the 10k is not coming back too, I decided to give them completly". Fixed by the two rows below |
| 2026-09-23 | bulk | -10,000 | Loan to a friend (moved to Giving) | Loan to a friend | reverses the 2026-09-22 loan row |
| 2026-09-23 | bulk | 10,000 | Given to a friend (was a loan, not coming back) | Giving | his words: "It is not coming back, also the 10k is not coming back too, I decided to give them completly" |
| 2026-09-23 | correction | — | 2026-09-23 bulk Sent to someone who needed it 5,000: given, not a loan | — | his words: "It is not coming back, also the 10k is not coming back too, I decided to give them completly". No change to the row |
| 2026-09-25 | bulk | 30,000 | Ticket, creatives networking event (2026-09-26, 2:00pm) | Networking event | his words: "I just paid for the event ticket now, 30k"; NGN taken from "30k"; money-check said doesn't fit, paid from the Buffer refill + Eating out (plan changed 2026-09-25) |
| 2026-09-26 | bulk | 12,302 | Transportation | Transport | derived: NGN 13,567 (ledger) − NGN 1,265 (his words); his words: "I spent the out of the money that was in my account on transportation yesterday"; told 2026-09-27 at the Sunday check |
| 2026-09-27 | balance | 1,265 | Bank | — | his words: "Right now, just 1,265 in my account right now"; no screenshot |
| 2026-09-27 | from-pot | 30,000 | Cowrywise withdrawal, not yet in the bank | Cowrywise investment | his words: "I just withdrew 30,000 from cowrywise investment cause I don't like having nothing much in my account, the money would arrive tomorrow as it takes 24hrs to process"; in transit, due 2026-09-28; not in the 1,265 balance above; not asked first |
| 2026-09-28 | correction | — | Cowrywise investment pot (all rows): it is Cowrywise savings, not the investment. The investment is a separate fund run by his finance manager, existing NGN 60,000 per his words, not in this ledger | Cowrywise investment | his words: "The 6,959 is actually savings, the investment is in a different place with my finance manager who invests for me"; "I have an existing 60k investment already locked". Pot split waits on his answer about Rule 7 |
| 2026-09-28 | from-pot | 6,959 | Relabel: Cowrywise savings leaves the old pot name. No money moved | Cowrywise investment | his words: "It's withdrawable, put it toward the Buffer"; paired with the to-pot row below, bank unchanged |
| 2026-09-28 | to-pot | 6,959 | Relabel: Cowrywise savings counted in the Buffer. No money moved | Buffer | his words: "It's withdrawable, put it toward the Buffer"; paired with the from-pot row above, bank unchanged |
| 2026-08-31 | opening | 60,000 | Investment fund | Investment fund | his words 2026-09-28: "I have an existing 60k investment already locked", run by his finance manager. Date it went in not known; entered at the starting position because no row moved it |
| 2026-09-28 | correction | — | Pot names from today: `Investment fund` (locked, Rule 7) and `Buffer` (includes Cowrywise savings). `Cowrywise investment` is history only | — | his words 2026-09-28; plan-2026-10 changes |
| 2026-09-28 | bulk | 13,000 | Debt girlfriend owed someone, paid by Samuel | Girlfriend — extra | his words: "I had to pay a debt my babe owed someone, 13k"; day not given, logged as told 2026-09-28; not asked first |
| 2026-10-04 | bulk | 10,000 | Eating out | Eating out | his words: "10k on eating out" |
| 2026-10-04 | bulk | 5,000 | Given to someone | Giving | his words: "5k I gave someone" |
| 2026-10-04 | bulk | 3,265 | Recharge card | Data / airtime | derived: NGN 18,265 on hand - 15,000 = 3,265; his words: "the rest was used on recharge card" |
| 2026-10-04 | balance | 0 | Bank | — | derived from his words: "spent all the money on hand" |
| 2026-10-04 | correction | — | 2026-10-04 bulk rows Eating out 10,000, Giving 5,000, Recharge card 3,265: September's leftover cash, not October's budget | — | his words 2026-10-04: "is not part of this month's budget, it was out of the money on hand from last month". Fixed by the six rows below; bank unchanged |
| 2026-10-04 | bulk | -10,000 | Eating out (moved to September) | Eating out | reverses the 2026-10-04 Eating out row |
| 2026-10-04 | bulk | -5,000 | Given to someone (moved to September) | Giving | reverses the 2026-10-04 Giving row |
| 2026-10-04 | bulk | -3,265 | Recharge card (moved to September) | Data / airtime | reverses the 2026-10-04 Recharge card row |
| 2026-09-30 | bulk | 10,000 | Eating out | Eating out | spent 2026-10-04 from September's cash on hand, booked to September; his words 2026-10-04: "is not part of this month's budget, it was out of the money on hand from last month" |
| 2026-09-30 | bulk | 5,000 | Given to someone | Giving | spent 2026-10-04 from September's cash on hand, booked to September; his words 2026-10-04: "is not part of this month's budget, it was out of the money on hand from last month"; September's plan had Giving at 0 |
| 2026-09-30 | bulk | 3,265 | Recharge card | Data / airtime | spent 2026-10-04 from September's cash on hand, booked to September; his words 2026-10-04: "is not part of this month's budget, it was out of the money on hand from last month"; derived: NGN 18,265 on hand - 15,000 |
| 2026-10-04 | balance | 0 | Bank | — | same balance restated after the correction rows above, so the derived bank reads 0 again; no money moved |
| 2026-10-06 | in | 1,238,416 | Route Rise, September batch 70% | — | his words: "1,238,416 in my account after conversion"; landed 2026-10-06 (told same day); USD gross/net and the Cleva rate not yet given; USD 3 kept back by Cleva for a virtual card whose activation failed, not converted; plan expected NGN 1,260,501 |
| 2026-10-06 | major | 143,942 | Claude Max, claude.ai, Cleva card | Claude Max upgrade | his words: "N143,942 was charged for $107.5"; NGN 1,339/USD on the card |
| 2026-10-06 | major | 500,000 | Building project | Building project | his words: "I just sent ... Building"; Rule 4 kept in full |
| 2026-10-06 | major | 100,000 | Parents | Parents | his words: "Parents was sent 100k instead of 150k"; plan 150,000 |
| 2026-10-06 | major | 100,000 | Girlfriend allowance | Girlfriend allowance | his words: "GF allowance" |
| 2026-10-06 | major | 30,000 | Ex-Jam contribution | Ex-Jam get-together | his words: "Ex-Jam allowance"; plan 30,000 |
| 2026-10-06 | major | 50,000 | Former PA debt | Former PA debt | his words: "Former PA debt" |
| 2026-10-06 | to-pot | 60,000 | Investment fund (his finance manager) | Investment fund | his words: "Investment fund"; Rule 3 and Rule 7 kept: Payday A |
| 2026-10-06 | major | 20,150 | First main shopping, Dellamond (invoice 114624): household and cleaning items | Chores / household | receipt screenshot; 11 items: foam, 3 air fresheners, cotton buds, bar soap, Dettol, toilet cleaner, Hypo, detergent, Izal; POS Moniepoint |
| 2026-10-06 | major | 27,400 | First main shopping, Dellamond (invoice 114624): food and snacks | Feeding | receipt screenshot; cookies, Goldenmorn, cornflakes, Super2 biscuit, candy, cheese balls, Sesamix, Schweppes |
| 2026-10-06 | major | 10,650 | First main shopping, Dellamond (invoice 114624): baby oil, lip care, fashion cap | Personal / misc | receipt screenshot; 2,200 + 2,950 + 5,500; receipt total 58,200 = 20,150 + 27,400 + 10,650; category my call, baby oil could be Chores |
| 2026-10-06 | major | 15,000 | Community admin salary | Community admin salary | his words: "15k went to my admin, I changed my mind and sent him the money"; plan 15,000 Payday A |
| 2026-10-06 | bulk | 5,100 | Cash withdrawn to hold, for small transportations | Transport | his words: "Withdrew 5.1k to hold on hand, for small transportations"; counted as spent on Transport when withdrawn; any unspent cash is still Transport |
| 2026-10-06 | bulk | 5,100 | Hanger, cream and some sweets | Personal / misc | his words: "5.1K went to buying hanger, my cream and some sweets"; split not given, booked whole to Personal / misc |
| 2026-10-06 | bulk | 4,000 | Chicken | Feeding | his words: "4000 went to buying chicken" |
| 2026-10-06 | correction | — | 2026-10-06 Personal / misc rows (10,650 shopping, 5,100 hanger/cream/sweets): baby oil, lip care, hanger and cream are Chores; sweets are Feeding | — | his words: "Baby oil is for me under chores, including Nivea lip care, Hanger, and cream, I don't know how much they cost but just split them". Fixed by the rows below; total unchanged |
| 2026-10-06 | major | -5,150 | Baby oil 2,200 + Nivea lip care 2,950 (moved to Chores) | Personal / misc | reverses part of the 10,650 row; receipt prices |
| 2026-10-06 | major | 5,150 | Baby oil and Nivea lip care | Chores / household | his words; receipt prices |
| 2026-10-06 | bulk | -5,100 | Hanger, cream and sweets (split below) | Personal / misc | reverses the 5,100 row |
| 2026-10-06 | bulk | 3,400 | Hanger and cream | Chores / household | his words: "just split them"; prices unknown, split in three equal parts of 1,700 |
| 2026-10-06 | bulk | 1,700 | Sweets | Feeding | his words: "just split them"; one third of 5,100 |
| 2026-10-08 | bulk | 2,500 | Data | Data / airtime | his words: "Spent 2500 on data"; logged 2026-10-08, day assumed |
| 2026-10-08 | bulk | 6,200 | Eating out | Eating out | his words: "Spent 6200 eating out"; logged 2026-10-08, day assumed |
| 2026-10-08 | bulk | 5,000 | Girlfriend, "some stuffs" | Girlfriend extras | his words: "Gave GF 5k for some stuffs"; booked to Girlfriend extras, not the allowance; logged 2026-10-08, day assumed |
| 2026-10-09 | bulk | 5,000 | Giving, to someone | Giving | his words: "5k went to giving yesterday someone" (said 2026-10-10) |
| 2026-10-10 | bulk | 8,000 | Girlfriend, foodstuffs | Girlfriend extras | his words: "Gave my GF 8k for some foodstuffs"; booked to Girlfriend extras, not the allowance; logged 2026-10-10, day assumed |
| 2026-10-10 | major | 30,000 | Gym | Health — gym | his words: "30k went to Gym"; logged 2026-10-10, day assumed |
| 2026-10-10 | major | 30,000 | Graphic designer, advance on NGN 60,000 | Graphic designer | his words: "My Graphics designer is charging me 60k, most of that money would hopefully come from the signups, but I gave him 30k advance from my cash on hand"; NGN 30,000 still owed; logged 2026-10-10, day assumed |
| 2026-10-10 | bulk | 6,315 | TikTok ads | Webinar ads | his words: "Tiktok Ads 6315"; booked to Webinar ads; logged 2026-10-10, day assumed |
| 2026-10-10 | balance | 77,709 | Bank | — | his words: "I have 77,709 sitted in my account right now"; rows added up to 74,059, the +3,650 is not explained; Flutterwave webinar money passed through and was moved to a separate account (not personal money, not logged here); no screenshot |
| 2026-10-10 | major | 30,000 | Instagram ads | Webinar ads | his words: "30k sent for instagram Ads" (said 2026-10-11); from his own bank, per plan line A 36,315 |
| 2026-10-10 | bulk | 3,000 | Haircut | Personal / misc | his words: "3k for haircut" (said 2026-10-11) |
| 2026-10-10 | bulk | 4,000 | Eating out | Eating out | his words: "4k on eating out" (said 2026-10-11) |
| 2026-10-11 | bulk | 5,000 | Cash withdrawn for transport | Transport | his words: "5k withdrewn for transport"; counted as spent when withdrawn |
| 2026-10-11 | bulk | 4,000 | Giving, someone in need at church | Giving | his words: "4k giving to someone in need at the church" |
| 2026-10-11 | bulk | 5,000 | Girlfriend, food | Girlfriend extras | his words: "5k sent to GF for food"; booked to Girlfriend extras, not the allowance |
| 2026-10-11 | bulk | 10,400 | Eating out | Eating out | his words: "10,400 eating out" |
| 2026-10-11 | bulk | 309 | Minor spends 2026-10-10 to 2026-10-11 | Other | derived; rows give 16,309, he said "16k", likely rounding |
| 2026-10-11 | balance | 16,000 | Bank | — | his words: "I have presenlty 16k in my bank account now"; Sunday check; no screenshot. Webinar money not counted: 29,340 separate account + 48,925 Flutterwave unsettled (his words) |
| 2026-10-12 | in | 25,000 | Graphic designer advance back from webinar money (25,000 of 30,000) | — | his words: "Yes I sent back the 25k to me" (said 2026-10-14); planned for 2026-10-12, day assumed |
| 2026-10-14 | major | -8,580 | Webinar ads, unspent money returned | Webinar ads | his words: "I stopped the ad before the ad spend could finish, the remaining ad money was 8,580 which I have already returned to my account"; day it landed not given; ads cost 27,735 net
| 2026-10-12 | bulk | 6,400 | Eating out | Eating out | his words: "Spent 6,400 on eating out on Monday" (said 2026-10-14) |
| 2026-10-13 | bulk | 6,000 | Giving, someone in need | Giving | his words: "gave 6,000 to someone who was in need yesterday" (said 2026-10-14) |
| 2026-10-13 | bulk | 5,500 | Feeding | Feeding | his words: "spent 5,500 on feeding again yesterday" (said 2026-10-14) |
| 2026-10-14 | correction | — | 2026-10-14 major -8,580 Webinar ads refund: landed 2026-10-13, not 10-14 | — | his words: "recieved the 8580 yesterday from the ads"; same month, totals unchanged |
| 2026-10-12 | bulk | 12,000 | Girlfriend's gas (part 1 of 25,000) | Girlfriend extras | his words: "Her 25k gas has left" (said 2026-10-14); split as agreed 2026-10-11 |
| 2026-10-12 | bulk | 13,000 | Girlfriend's gas (part 2 of 25,000) | Extra cash | same transfer |
| 2026-10-14 | bulk | 8,580 | Girlfriend's subscription (part 1 of 30,000) | Girlfriend extras | his words: "The Sub is paid today"; the released ads money, plan changed 2026-10-14 |
| 2026-10-14 | bulk | 4,659 | Girlfriend's subscription (part 2 of 30,000) | Extra cash | same payment; empties Extra cash |
| 2026-10-14 | bulk | 1,500 | Girlfriend's subscription (part 3 of 30,000) | Personal / misc | same payment; Rule 8 cut order |
| 2026-10-14 | bulk | 15,261 | Girlfriend's subscription (part 4 of 30,000) | Chores / household | same payment; Rule 8 cut order (creator visits is 0); his own gas ~4,000 not happening (his words) |
| 2026-10-14 | in | 32,735 | Webinar money paid back to Samuel (advance 5,000 + ads 27,735) | — | his words: "I have paid myself the 32,735 already now"; webinar money owes him nothing now |
| 2026-10-14 | correction | — | 2026-10-14 bulk rows "Girlfriend's subscription" parts 1-4 (30,000): not paid yet | — | his words: "I haven't paid the SUB yet"; Money man misread "The Sub is paid today" |
| 2026-10-14 | bulk | -8,580 | Girlfriend's subscription part 1 reversed | Girlfriend extras | correction above |
| 2026-10-14 | bulk | -4,659 | Girlfriend's subscription part 2 reversed | Extra cash | correction above |
| 2026-10-14 | bulk | -1,500 | Girlfriend's subscription part 3 reversed | Personal / misc | correction above |
| 2026-10-14 | bulk | -15,261 | Girlfriend's subscription part 4 reversed | Chores / household | correction above |
| 2026-10-14 | bulk | 84 | Minor spends 2026-10-11 to 2026-10-14 | Other | derived; rows give 39,415, he has 39,331 |
| 2026-10-14 | balance | 39,331 | Bank | — | his words: "what is in my account now after withdrawing the 32k from the webinar is 39331"; before the GF subscription. Webinar account 30,313 (his words) |
| 2026-10-14 | bulk | 8,580 | Girlfriend's subscription (part 1 of 30,000) | Girlfriend extras | his words: "Just sent the sub now"; the released ads money, plan changed 2026-10-14 |
| 2026-10-14 | bulk | 4,659 | Girlfriend's subscription (part 2 of 30,000) | Extra cash | same payment; empties Extra cash |
| 2026-10-14 | bulk | 1,500 | Girlfriend's subscription (part 3 of 30,000) | Personal / misc | same payment; Rule 8 cut order |
| 2026-10-14 | bulk | 15,261 | Girlfriend's subscription (part 4 of 30,000) | Chores / household | same payment; Rule 8 cut order (creator visits is 0) |
| 2026-10-14 | bulk | 2,500 | Food for girlfriend | Girlfriend extras | his words: "I just sent 2.5k to my GF for some food"; Girlfriend extras was already empty, so over plan by 2,500 |
| 2026-10-14 | charges | 11 | Bank charges | — | derived; rows give 6,831, he has 6,820 |
| 2026-10-14 | balance | 6,820 | Bank | — | his words: "6,820 in my personal account"; no screenshot. Webinar money not counted: 49,883 webinar account + 4,892 Flutterwave (his words) |
| 2026-10-15 | bulk | 6,000 | Plumber, water issue in the house | Chores / household | his words: "there was a water issue in the house so I had to pay plumber 6000 from my personal money"; before Payday B; day assumed |
| 2026-10-16 | in | 569,096.50 | Route Rise, September batch 30% + bonus | — | invoice #14: 30% USD 399.99 + bonus USD 25.00 = USD 424.99 billed; USD 421.59 received (his words), USD 3.40 lost to charges; NGN 569,096.50 after Cleva (his words) = about NGN 1,349.88/USD; day landed assumed today; plan expected NGN 536,343 |
| 2026-10-16 | charges | 17.50 | Bank charges | — | derived; rows give 569,916.50, he has 569,899 |
| 2026-10-16 | balance | 569,899 | Bank | — | his words: "what is in my personal account right now is N569,899"; no screenshot. Webinar money not counted: 44,084 webinar account + 14,677 Flutterwave (his words) |
| 2026-10-16 | to-pot | 200,000 | Goal 1, Payday B | Goal 1 | his words: "I just sent 200k for goal 1, so I have a round number"; plan 199,752, the extra 248 from Extra cash; Rule 3 kept: same day as Payday B |
| 2026-10-16 | to-pot | 50,000 | Buffer, Payday B | Buffer | his words: "and 50k for buffer"; plan cut from 114,891 to 50,000 the same day; Rule 3 kept |
| 2026-10-16 | bulk | 30,000 | Girlfriend, sent | Girlfriend extras | his words: "Sent my GF 30k"; planned 2026-10-16 |
| 2026-10-16 | bulk | 15,430 | Yoghurt 8,430 + turkey 5,000 + banana 2,000 | Feeding | his words: "I spent 8,430 on some yougort, and 5000, on buying a turkey, and 2000 on bannana" |
| 2026-10-17 | bulk | 15,329 | SMFest seminar fee | Creator visits (network) — SMFest 2026-10-17 | his words: "SMFest fee - 15329"; plan 15,000, over by 329; day assumed (seminar 2026-10-17) |
| 2026-10-17 | bulk | 1,700 | Google YouTube subscription | Subscriptions | his words: "Google Youtube sub - 1,700"; told 2026-10-18; day assumed |
| 2026-10-17 | bulk | 15,000 | Google One subscription (AI Plus 2 TB) | Subscriptions | his words: "Google one sub - 15,000"; told 2026-10-18; day assumed |
| 2026-10-17 | bulk | 25,000 | Girlfriend's bible | Girlfriend extras | his words: "Babe's bible 25,000"; not in the plan, line already fully spent, so over by 25,000; told 2026-10-18; day assumed |
| 2026-10-17 | bulk | 4,100 | Transport on the SMFest outing (2,100 + 2,000) | Transport | his words: "2,100 TP, 2000,tp"; day assumed |
| 2026-10-17 | bulk | 14,000 | Food on the SMFest outing (4,000 + 10,000) | Eating out | his words: "4000 food,10000 food"; day assumed |
| 2026-10-17 | bulk | 5,100 | Things for his parents | Parents | his words: "5100, parents"; the one-off 10,000 for this visit; day assumed |
| 2026-10-18 | bulk | 10,200 | POS cash withdrawal for Sunday transport | Transport | his words: "10,200 POS withdraw for TP of Sunday"; day assumed |
| 2026-10-18 | bulk | 9,400 | Food today | Feeding | his words: "Food today 9400"; Feeding, not Eating out, is Money man's guess, he was told |
| 2026-10-18 | bulk | 1,518 | Minor spends 2026-10-16 to 2026-10-18 | Other | derived; rows give 174,640, he has 173,122; likely POS and transfer charges |
| 2026-10-18 | balance | 173,122 | Bank | — | his words: "Current bank account is 173,122"; no screenshot. Webinar money not counted: 11,507 webinar account + 29,355 Flutterwave (his words) |

Back to [[03-Areas/finances/finances|Finances]]

