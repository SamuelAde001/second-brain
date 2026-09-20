# Money

## SMART goal

- **₦1,000,000 saved and still there on 31 Dec 2026** — the money that moves him
  into the new house.
- **₦3,000,000 more by 31 July 2027** — marriage. Confirmed 2026-08-26 as **ON TOP
  of the ₦1M, not inclusive. ₦4,000,000 total.**
- **Emergency fund ₦300,000** — funded from January 2027, **after** the ₦1M closes.
  His call: it does not compete with the December target.
- **Building project funded at ₦500,000 every month, no shortfall.**

The investment pot does NOT count toward any of these. See Rule 7.

## Current number (as of 2026-09-02)

| Pot | Amount | Notes |
|---|---|---|
| Bank (liquid) | **₦962,371** | Payday A landed and is confirmed in the account. ₦934,600 of it is spoken for the same day; **₦27,771 is the real free number.** |
| Emergency fund | **₦0** | does not exist yet — starts Jan 2027 |
| Buffer | **₦0** | first ₦50,000 moves on Payday B, 14 Sep |
| Goal 1 — house | **₦0** | account now exists (Cowrywise). First ₦146,041 moves 14 Sep. |
| Cowrywise investment | **₦305,000** | locked, ring-fenced, +₦100,000/month to year end |
| **Available for goals** | **₦0** | |

Bank reconciles exactly: ₦143 opening + ₦962,228 converted = ₦962,371. The ₦143 is
what survived August — ₦2,503 on 27 Aug less ₦2,360 of recharge cards.

August income: **₦1,109,987** — of which ~₦200,000 was a savings withdrawal, not
income. **Real August income ≈ ₦910,000.**

Projected investment balance 31 Dec 2026: ₦305,000 + (Sep–Dec × ₦100,000) = **₦705,000**.
It does not pay out until January 2027, when he moves it into actual stocks.

## Where each pot physically lives

Added 2026-08-28. A pot with no account is a pot that cannot be funded on payday.

| Pot | Account | Payday |
|---|---|---|
| Buffer | **the savings account already called "Emergency"** — his answer 2026-08-28 | B |
| Cowrywise investment | Cowrywise, locked to Jan 2027 | A |
| Goal 1 — house | **Cowrywise** — created 2026-09-02 | B |
| Goal 2 — marriage | NOT SET (starts Jan 2027) | B |
| Emergency fund | the "Emergency" account (starts Jan 2027) | B |

**Goal 1 now has a home. Samuel opened it on Cowrywise, 2026-09-02.** That closes
the question that had a 14 September deadline on it, and it closes it well: a
Cowrywise plan is harder to raid than a bank account, which is exactly what Rule 1
needs.

**But it puts a SECOND name clash on the board, and this engine already has one.**
Cowrywise now holds two pots that mean opposite things: the ₦305,000 ring-fenced
investment that never counts toward any goal, and the ₦1M house money that is the
goal. In December the app will show roughly ₦1.7M as one balance. Two questions
have to be answered before the 14th, and they are on TickTick:

1. **Is it a separate plan from the investment, or the same one?** If the same, the
   ₦1M and the ring-fence are indistinguishable and Rule 7 stops meaning anything.
2. **What is the maturity date?** The ₦1M has to be *saved and still there on
   31 Dec 2026* and then spendable on the house. A lock that runs past December
   protects the target and blocks the purpose.

Two platforms, four pots, two name collisions — Buffer sharing the "Emergency"
account, and Goal 1 sharing Cowrywise. Neither is wrong. Both are the kind of thing
that reads fine today and is unreadable in December.

**The account is called "Emergency" but from September to December it holds the
BUFFER, not the emergency fund** — that pot does not start until January 2027.
From January two different pots would share one account and the balance stops
meaning anything. Decide before then.

## The one lever

**Monthly surplus that survives the month.** Not income — surplus that is still
there on the 30th. Income doubled and halved across three months and the savings
balance did not move, which proves income was never the lever.

## Weekly minimum

Every naira in and out logged daily. **Zero unlogged days.** Seven rows in
`context/money-ledger.md` every week.

## Cost of breaking it

`[OPEN — no enforced forfeit exists. Asked 2026-08-26. See stakes.md.]`

## How it is verified

Bank balance screenshot sent to Claude Code at the evening reckoning, **plus a
spoken account of what went out that day.** A screenshot with no spend list is
not verification — it shows the number, not the decisions.

**The workbook:** Google Sheets — **"My Claude Budget"**, moved there 2026-08-26 so
Claude Code can write it directly instead of Samuel typing updates by hand. Tabs:
Dashboard, Setup, Income, Expenses, Transfers, Budget, Details. Covers Aug 2026 –
Jul 2027, so it reaches both targets.

`context/money-ledger.md` stays the text source of truth. The sheet is the
budgeting layer; the ledger is the record. **If the two disagree, the ledger wins.**

Claude writes it through `tools/sheets/` — an Apps Script web app bound to the
sheet. Setup and security are in `tools/sheets/README.md`; the credentials live in
a gitignored `.env`. The line items behind every category live in
`tools/sheets/plan.json`, and `tools/sheets/build_budget.py` rebuilds the Budget
and Details tabs from it.

Design point, straight out of the June–August failure: **nothing is typed on the
Budget or Dashboard tabs.** Budget's plan column reads Details, its month columns
read Expenses, and its savings block reads Transfers — all via SUMIFS. A budget
line cannot claim money moved when no row exists. That was the whole bug in the
old sheets.

**The Details tab** answers "what is this category actually made of" — every
subscription, every line, with its amount, due day, tier and payday. It is the only
place a plan number is typed. Cancelled items go Active=No; they are never deleted,
because a subscription that reappears in three months is a pattern and a deleted
row hides it.

---

## Income mechanics

- Paid in **USD**, converted to NGN on **Cleva**. **Measured on the 2026-09-02
  payment: ₦1,361.66/$** — ₦962,228 for $706.66. The June–August average was
  ₦1,365/$. Rate moves with the market; use the measured figure, not the average.
- **THERE IS A FLAT $5 CHARGE PER PAYMENT.** Confirmed 2026-09-02 to the cent:
  gross $711.66, received $706.66. It is flat, not a percentage — which means it
  costs proportionally more on the smaller 30% payment. **$10/month, ~₦13,617/year.**
  Every projection in this file that used a gross figure was overstated by it.
- Client pays **monthly in two stages: 70% at month end, 30% mid the following
  month.** The mid-month invoice is always the remainder of the previous month's
  batch — never a new batch. Every "mid-month payment" is last month's money.
- **Route Rise Media LTD is an AGENCY, and it is his only payer.** Corrected by
  Samuel 2026-08-27. Route Rise works with two end clients; Samuel edits for both
  and sends **one invoice to Route Rise covering both**. There is no second client
  and there never was — the earlier "second client" line in this file was wrong.
- **Rates: $333.33/video** on the original end client — he has tried to raise it,
  they will not move, he is content with it. **$175/video** on the second end
  client, new August 2026, 2 videos agreed, may or may not recur. Both rates are
  set by Route Rise.
- **One payer, one invoice, one relationship.** If Route Rise goes, 100% of his
  income goes with it — including the "$175 client", which is not a separate
  relationship he could keep.
- **Payment timing is Lewis's to control, not Samuel's.** 2026-08-27: Lewis
  Mountstephens told the Route Rise channel payments would be "a day or so later
  this month" — he is away till the 31st. August's 70% therefore lands ~1–3 Sep,
  not 31 Aug. No confirmed date. Invoice still goes out on the 29th regardless.
- **He does not want more clients.** His reason: one client's workload is already
  high. His call. Not to be re-litigated at every check-in — but read the
  concentration risk below before advising on anything income-shaped.

## Verified batch history

| Batch | Videos | Notes |
|---|---|---|
| May | 5 | invoiced 06/14 |
| June | 4 | invoiced 06/29 (70%) + 07/14 (30%) |
| July | 2 | invoiced 07/29 (70%) + 08/14 (30%) |
| August | 4 | 2 × $333.33 + 2 × $175 = **$1,016.66 gross** — ONE Route Rise invoice covering both end clients |

**August, as it actually paid — corrected 2026-09-02:**

| | Gross | Charge | Net | ₦ |
|---|---|---|---|---|
| 70%, landed 2 Sep | $711.66 | $5.00 | **$706.66** | **₦962,228** confirmed |
| 30%, due ~14 Sep | $305.00 | $5.00 | $300.00 | ~₦408,497 at ₦1,361.66 |
| **Batch** | $1,016.66 | $10.00 | $1,006.66 | **~₦1,370,725** |

The record planned ₦1,387,741. **The batch is ₦17,016 lighter than planned** — ₦9,188
of it confirmed on the 70%, the rest an estimate that moves with the rate on the 14th.
Two causes, both structural and both recurring: the flat $10/month of charges, and a
rate ₦3.34 below the assumed average.

## Cash actually landing per calendar month

| Month | Income |
|---|---|
| June | ₦2,273,189 |
| July | ₦1,791,800 |
| August | ₦1,109,987 (~₦910,000 real — ₦200k was savings) |

**Income has halved in two months.** This is the single most important number in
the system.

## Monthly obligations — exact, from 2026-08-26

Samuel gave the real line items. They are on the Details tab and in
`tools/sheets/plan.json`. **Payday** is which half of the month pays it — see
"The two paydays" below.

| Item | Amount | Tier | Payday |
|---|---|---|---|
| Building project | ₦500,000 | Fixed | A |
| Parents | ₦100,000 | Committed | A |
| Girlfriend allowance | ₦100,000 | Committed | A |
| Subscriptions | ₦51,800 | mixed | split |
| Chores / household | ₦40,000 | Discretionary | B |
| Health — gym | ₦30,000 | Committed | A |
| Feeding | ₦30,000 | Committed | B |
| Creator visits (network) | ₦25,000 | Discretionary | B |
| Transport | ₦20,000 | Committed | B |
| Community admin salary | ₦15,000 | Fixed | B |
| Giving | ₦10,000 | Committed | B |
| Personal / misc | ₦10,000 | Discretionary | B |
| Data / airtime | ₦5,000 | Committed | B |
| **Obligations floor** | **₦936,800** | | |
| Investment contribution | ₦100,000 | Fixed | A |
| **Total committed outflow** | **₦1,036,800 / month** | | |

Subscriptions, exactly: Claude ₦33,500 (16th) · Google ₦15,000 (2nd) · YouTube
Premium ₦1,700 (17th) · Spotify ₦1,600 (5th) = **₦51,800**. YouTube and Spotify
kept — his words: they help his work, and they are his only entertainment.

**Cut and gone: CapCut ₦14,900 (2026-09-02) and Rubik's cube ₦6,860 (2026-08-26).**
CapCut went because he edits on DaVinci Resolve now — his call, unprompted, and it
is the best line on this page. It is **₦14,900 every month, ₦44,700 by December and
₦178,800 a year**, bought by cancelling something he had stopped using. Note the
shape of it: the obligations floor has now fallen twice, both times because he
changed a decision, and never once because income moved.

**The estimate was ₦1,044,500. The truth is ₦1,038,560 once personal/misc is
counted — a difference of ₦5,940.** Nothing got cheaper. Feeding's ₦150,000 did not
become savings, it moved house: into transport, data, household, the gym, and a misc
line that did not exist before. That is worth remembering the next time a category
looks like it has slack in it.

Changed 2026-08-26 at his instruction: giving ₦20,000→₦10,000 ("only when someone
asks" — `spirit.md` records no tithe commitment, so nothing pulls against it);
feeding ₦50,000→₦30,000 (his sister feeds him); transport ₦30,000→₦20,000;
personal/misc ₦50,000→₦10,000. Gym ₦30,000 **added**, starting September — he is
resuming it. **The gym is not a line to raid.** It is the one item on this list
that pays him back.

Creator visits added 2026-08-26 at ₦25,000/month, his number. It is a real line now,
not a good intention — and it cost the December target ₦100,000 across four months.
That trade is stated below, not hidden.

## The two paydays

One batch, two dates. This is now the spine of the budget.

| | Payday A — 70% | Payday B — 30% |
|---|---|---|
| Lands | end of the **previous** month | around the **14th** |
| Funds | the 1st – 14th | the 15th – month end |
| Expected in | ~₦962,228 measured | ~₦408,497 est |
| Committed | ₦846,600 | ₦190,200 |
| **Free** | **₦115,628** | **₦218,297** |

Updated 2026-09-02 for the measured rate, the flat $5 charge and the CapCut cut.
The "expected in" figures are now NET of charges — the old ones were gross, and
that error was worth ₦17,016 a month. **These are the numbers for a normal month;
September itself is replanned below and looks nothing like this.**

The 30% is always the previous month's remaining batch, never a new one.

**They do not pay at weekends.** If a payday falls on a Saturday or Sunday the money
lands the following Monday night. Two slips are already on the calendar:

- **Oct 70%: Sat 31 Oct → Mon 2 Nov.** The tightest point of the year. November's
  front half is funded on the 2nd, and Google bills on the 2nd, CapCut the 4th.
- **Nov 30%: Sat 14 Nov → Mon 16 Nov.**

Both are on the Budget tab's payday calendar.

Removed and no longer owed:

- **Editor (₦50k) and workers (₦100k) — cut.** His words: *"it was financially
  unwise at that moment and it takes time to manage them too... no one can edit my
  style of videos yet, I need to make my content my style before hiring any."*
  Only the ₦15k community admin stands.
- **HighSignals devs — ₦0.** Paid ₦150k in July; they have since agreed to work
  free because August was low. They are friends. Nothing owed. He intends to sort
  them out when Scripnals launches.
- **Commercial loans — all cleared.** Okash, FairMoney, bank loan. Gone. Do not
  carry forward.

**But one debt is live, added 2026-08-26: he owes his sister ₦90,000.** ₦40,000 goes
in September on Payday B. **₦50,000 remains, with no date on it** — his words: "can
hold for anytime I am free with more funds, no deadline." She is not pressing, so it
is not scheduled. It is written down here anyway, because an undated debt is the
kind of thing that ambushes a month, and because "when I have more funds" is the
same sentence that moves due dates. Bring it up the first month that closes with the
buffer full.

## September 2026, as replanned

Rebuilt 2026-09-02, the day Payday A landed, against **confirmed** money rather than
projections. Every figure below is either measured or named as an estimate.

**In:** ₦962,371 in the bank now (confirmed) + ~₦408,497 on the 14th (estimate)
= **~₦1,370,868.**

**What changed on 2026-09-02, and who changed it:**

| Change | ₦ | Whose call |
|---|---|---|
| Parents — cancelled for September only | **−100,000** | Samuel. He spoke to his dad and his dad agreed. October onward it is back to ₦100,000. |
| CapCut — cancelled outright | **−14,900/mo** | Samuel. DaVinci Resolve does the job. |
| Girlfriend allowance 100,000 → 50,000 | −50,000 | Confirmed with her |
| Son's school 50,000 → 100,000 | +50,000 | Confirmed with her. **Due before the 14th**, so it stays on Payday A. |
| Kaduna trip 50,000 → 80,000 | +30,000 | Samuel — he has not travelled in a while and the real cost is unknown |
| Gym clothing — new one-off | +10,000 | Buys the 6×/week movement habit |
| Payment charges + rate | +17,016 | Route Rise/Cleva. Not his call, and it recurs. |

The girlfriend lines cancel out exactly: ₦150,000 either way. Only the split moved.

**Payday A — 2 to 14 September. ₦962,371 available.**

| | ₦ |
|---|---|
| Building project | 500,000 |
| Son's school | 100,000 |
| Cowrywise | 100,000 |
| Kaduna trip | 80,000 |
| Girlfriend allowance | 50,000 |
| Gym membership | 30,000 |
| Food shop | 30,000 |
| Google (2nd) | 15,000 |
| Gym clothing | 10,000 |
| Transport — house + church | 10,000 |
| Haircut, floss, pen | 5,000 |
| Hypo, soaps | 3,000 |
| Spotify (5th) | 1,600 |
| Parents · CapCut | **0 — cancelled** |
| **Out** | **934,600** |
| **CUSHION, 2–14 SEP** | **₦27,771** |

**Payday B — 15 to 30 September. ~₦408,497 expected.**

Goal 1 ₦146,041 · Buffer ₦50,000 · sister ₦40,000 · household remainder ₦37,000 ·
Claude ₦33,500 · creator visits ₦25,000 · community admin ₦15,000 · giving ₦10,000 ·
transport remainder ₦10,000 · data ₦5,000 · misc remainder ₦5,000 · YouTube ₦1,700
= **₦378,241. Free: ₦30,256.**

**The month closes with ₦58,027 free** — with Goal 1 whole, Cowrywise whole, and
creator visits still funded.

### Two structural fixes made the same day

**1. The front half was funded.** Until 2026-09-02 the plan put feeding, transport,
household and personal/misc entirely on Payday B, leaving the 1st–14th with ₦871.
That is not a budget, and it had already cost something real: he missed church on
30 August for want of ₦5,000. Each of those lines is now split — its front-half
share moves on Payday A, the remainder on B. Same monthly totals, ₦27,771 of
actual cushion. **The failure was never the size of the budget. It was the timing
of it.**

**2. The shopping list turned out to be already funded.** Samuel gave a ₦68,000 list
of things he needed. Categorised against the existing lines, ₦48,000 of it was
already inside Feeding, Household, Personal/misc and Transport — and the food came
to exactly ₦30,000, the Feeding line to the naira. Only ₦20,000 was new money, and
₦10,000 of that (snacks, his words: *"not essential"*) was deliberately left
unallocated inside the cushion instead. The list lives in `context/things-to-buy.md`
and on TickTick.

### What was NOT done, and why

**Cowrywise was not cut.** Samuel offered ₦40,000 out of it to build a cushion.
Declined, and he agreed: Rule 7 is his own rule, closed in writing on 2026-08-26
with *"it never pauses"* — and once parents came off, the cushion existed anyway. It
would have broken the hardest rule in the file to solve a problem that had already
been solved by a better decision.

### Goal 1 after September

The opening balance that carries into Goal 1 is **₦143, not ₦3,503** — ₦2,360 went on
recharge cards in the last week of August. So Goal 1 lands at ₦1,004,307 against
₦1,000,000: **a margin of ₦4,307, down from ₦7,667.**

October–December each run **₦17,016 lighter** than planned (charges + rate) and
**₦14,900 better** (CapCut) — a net **₦2,116/month**, or ₦6,351 across the quarter.
**That comes out of the Buffer, not Goal 1.** Which is precisely what the Buffer is
for, and the first time it has been used as designed instead of savings being raided.

## The savings hole

June–August the sheets booked **₦750,000 to Savings** and **₦150,250 to Emergency
funds** — **₦900,250 total.**

What actually survives:

| | |
|---|---|
| Booked to savings/emergency | ₦900,250 |
| Survives, as the Cowrywise investment | ₦305,000 |
| **Gone** | **₦595,250** |

His words on the ₦595,250: *"unplanned event came in and I used all the money
saved."* The August building payment dropped from ₦500,000 to ₦200,000 as a direct
consequence — a **₦300,000 shortfall** on the one obligation that is the entire
point of the ₦1M target.

A third of it became a real asset. Two thirds evaporated because no rule existed
saying what savings are for. That is the fix — not a tighter budget.

## Does the ₦1M close?

Starting balance ₦3,503. Four months: September, October, November, December.

**Recalculated 2026-08-26 on his real line items, and it is materially better.**

| Scenario | Gross / month | After ₦951,700 + ₦100k investment |
|---|---|---|
| August mix (2×$333 + 2×$175) | ₦1,387,741 | **₦336,041** |
| 4 × $333.33 | ₦1,819,982 | ₦768,282 |
| 2 videos / month | ₦909,991 | **−₦141,709 — underwater** |

At the August mix, with September's ₦140,000 of one-offs (son's school ₦50,000,
Kaduna ₦50,000, sister ₦40,000):

| Month | Income | − Bills | − One-offs | − Cowrywise | − Buffer | → Goal 1 | Left |
|---|---|---|---|---|---|---|---|
| Sep | 1,387,741 | 951,700 | 140,000 | 100,000 | 50,000 | **146,041** | **0** |
| Oct | 1,387,741 | 951,700 | — | 100,000 | 50,000 | **286,041** | **0** |
| Nov | 1,387,741 | 951,700 | — | 100,000 | 50,000 | **286,041** | **0** |
| Dec | 1,387,741 | 951,700 | — | 100,000 | 50,000 | **286,041** | **0** |
| | | | | | **200,000** | **1,004,164** | |

**₦1,004,164 + the ₦3,503 opening = ₦1,007,667 against a ₦1,000,000 target**, with
the buffer landing on exactly ₦200,000 the same month.

**Set 2026-08-28: Goal 1 is budgeted per month, not as a flat average.** The sheet
used to carry ₦249,124/month — ₦996,497 ÷ 4. That is an average, and it asked
September for ₦103,083 September does not have, because September carries
₦140,000 of one-offs the other three months do not. A plan that asks for money
you do not have gets paid out of the building fund or the buffer. Same finish
line, four honest numbers instead of one convenient one.

**Every month now balances to zero.** Bills + one-offs + every pot = income,
exactly. That is the point: a leftover is money with no name on it, and money with
no name on it is what ₦595,250 was. The Budget tab proves it in a block called
THE MONTH MUST BALANCE, and the site's Budget page shows the same table.

That margin is only ₦7,667, and that is the right trade. ₦207,000 of margin with no
buffer means the first urgency in October gets paid out of savings — which is
exactly how ₦595,250 disappeared. Margin has never stopped a raid. A buffer does.

Before his 26 Aug cuts this cleared December by **₦227 across four months.** The
cuts — giving, feeding, transport, personal/misc, the Rubik's sub — are what turned
a coin flip into a plan with a cushion. Worth saying once: that was his own doing,
and it is the first time the arithmetic has moved because he changed behaviour
rather than because income moved.

**2 videos/month is what July was.** It is already visible in the building payments.
At that mix he is ₦141,709 underwater every month, and steps 1–3 of the lean ladder
only free ₦55,000 of it. The buffer is the only legal answer — Rule 1 forbids
savings, Rule 7 forbids pausing Cowrywise. That is not a hypothetical: it is why
Rule 8 exists.

### Goal 2 — and this is the real problem

Samuel confirmed 2026-08-26: **the ₦3M is ON TOP of the ₦1M. ₦4,000,000 total.**

Jan–July 2027 is seven months. ₦3,000,000 over seven months is **₦428,571/month.**

**CORRECTED 2026-08-28, and the correction is material.** This table used to read
"surplus ₦243,000–₦277,000, SHORT by ₦152,000–₦186,000 every month." Both halves
were wrong. The surplus figure was the pre-26-Aug number, superseded by his own
cuts the same day — it is ₦336,041 now. And it subtracted Cowrywise from a period
in which Cowrywise has already stopped: Rule 7 funds it "until the year ends," so
from January that ₦100,000/month is free. Two errors stacked in one row.

From January: income ₦1,387,741 − bills ₦951,700 = **₦436,041 free per month.**

| At this mix | Free/month | Goal 2 needs ₦428,571 | + emergency fund ₦50,000 |
|---|---|---|---|
| August mix | ₦436,041 | clears by ₦7,470 | **SHORT ₦42,530/month** |
| 4 × $333.33 | ₦868,282 | clears easily | clears easily |
| 2 videos / month | −₦41,709 | underwater on the BILLS | — |

**So the ₦3M is not arithmetically impossible. It is arithmetically knife-edge.**
At the August mix, Goal 2 alone clears by ₦7,470 a month — a margin of 1.7% — and
the emergency fund on top of it does not fit, leaving ₦42,530/month to find.

That is a much smaller hole than this file used to claim, and it does not make the
position safe. It makes it fragile in a different way: **the whole thing now rests
on the August mix holding for seven straight months, and July was a 2-video month
in which he could not even cover the bills.** The exposure was never the size of
the gap. It is that Route Rise decides the volume.

And per the concentration risk below, **4-video months are not his decision.** Route
Rise sets the volume. Which leaves exactly one lever he owns:

> **From January the course has to carry roughly ₦42,530/month — about ₦300,000
> across the seven months — to fund the emergency fund alongside the ₦3M. Revised
> down from ₦170,000/month on 2026-08-28, when the arithmetic above was corrected.**

That is the number when the August mix holds. **It is ₦470,000/month if a 2-video
month repeats**, because a 2-video month does not cover the bills, let alone a pot.
The course's real job was never the ₦42,530. It is that it is the only income line
whose existence he controls.

That is the whole argument for the course, in one line, with a number attached. Every
Sunday the 5:00pm course block gets skipped is a payment missed on that ₦1.2M. The
weekly review says so.

The rate mix costs real money: 2 videos at $175 instead of $333.33 is **$316.66
lost on this batch alone (~₦432,000)**. Same payer, two rates — so that discount
is Route Rise's pricing on one of its end clients, not a separate client he could
walk away from.

## The concentration risk

One PAYER. Not one client — one payer. Route Rise is an agency; the two end
clients behind it are Route Rise's relationships, not his. Volume decided entirely
by Route Rise. Both rates set by Route Rise. One invoice a month.

**Corrected 2026-08-27.** This file used to carry a "second client" line that read
like the beginnings of diversification. It was not. The concentration is total:
100% of income arrives through one invoice to one company, and the "$175 client"
does not survive Route Rise leaving.

**"Hit 4 videos a month" is not a SMART goal** — the A fails. Achievement is
another company's decision, not his.

He has ruled out taking more clients. That is his call. But it means the course is
no longer the "#2 thing" — **it is the only income line whose existence he
controls.** Every time course work gets dropped for client work, that is the
diversification being traded away for the concentration.

The weekly review says so, out loud, every week.

## Rules

```
1. Savings are untouchable. The only permitted withdrawals are: medical emergency,
   building-project shortfall that would stop work, and family emergency. Nothing
   else. A girlfriend's visit is not an emergency.
2. Any withdrawal from savings gets logged the same day in context/money-ledger.md
   with the amount and the reason, in Samuel's own words. No silent withdrawals.
3. Savings move ON A PAYDAY, the day the money lands — never at month end. Money
   saved at the end of the month is money that was never saved.
   Cowrywise moves on Payday A. Goal 1 and the Buffer move on Payday B — Samuel's
   call 2026-08-26, because Payday A is nearly always full.
   EXCEPTION: if Payday A leaves more than ₦50,000 free after its commitments,
   that excess moves the same day. Six figures sitting loose for fourteen days is
   how ₦595,250 disappeared.
4. Building project is paid in full (₦500,000) before any discretionary line.
   August was ₦200,000. That is a shortfall of ₦300,000 and it is on the record.
5. No new work below $333/video — whether it is a new Route Rise end client or a
   new payer — without logging the reason in money-ledger.md. The August batch
   lost ~₦432,000 to the $175 rate.
6. A budget line that says money was saved when no money was saved is a lie in a
   spreadsheet. The daily ledger is the truth; the spreadsheet is a plan.
7. The investment is ring-fenced. ₦100,000/month goes to Cowrywise until the year
   ends. It is not touched for the ₦1M, the ₦3M, the building, or anything else.
   New savings and the emergency fund are built OUTSIDE it. It does not pay out
   until January 2027, when it moves into actual stocks. Samuel's rule, 2026-08-26.
8. THE BUFFER is where urgencies come from — not savings. ₦50,000/month to a
   ₦200,000 target, plus any month-end underspend, plus the whole excess of any
   4-video month. When a month lands short, the cut order is already decided:
   personal/misc → creator visits → household down to ₦20,000 → the buffer covers
   the rest → and ONLY THEN a conversation. If the buffer is empty, an urgency
   gets negotiated, not funded. It never gets funded from Goal 1.
```

**Said once about Rule 7, and not to be re-argued:** he is putting ₦100,000/month
into a locked pot he refuses to count toward his goals, while holding ₦3,503 liquid
and a ₦1M target with ₦70k of margin. That is a deliberate trade — long-term wealth
bought with short-term fragility. It is his call. It is written down so that if
December comes up short, the reason is on the record and not a mystery.

## Open questions

**Answered 2026-08-26:**

- ~~₦3M on top or inclusive?~~ **ON TOP. ₦4,000,000 total by 31 July 2027.**
- ~~Emergency fund?~~ **₦300,000, funded from January 2027, after the ₦1M closes.**
- ~~Creator visits budget?~~ **₦25,000/month.** Now a line in the obligations table.
- ~~Does the investment pause if the ₦1M is behind in November?~~ **No. It never
  pauses.** Ring-fenced in both directions, no escape hatch. Stated once: this means
  if December is short, the house move slips rather than the contribution. His trade,
  made with the numbers in front of him.

**Still open:**

- Wedding July 2027: total budget, and who pays which part? `[OPEN — asked 2026-08-26]`
- What is the enforced consequence for breaking the savings rule? `[OPEN — unenforced]`
- What does the course have to be priced at to carry ₦170,000/month from January?
  Depends on the beta price, which is still open in `context/audience.md`. `[OPEN]`

## September 2026 — what actually happened (added 2026-09-16)

- **Kaduna cost ~₦430,011 against ₦80,000 planned** (derived, not itemised). ₦368,041 of it
  came out of the Cowrywise investment, which now holds ₦36,959. Rule 7 broke. There is
  no refill plan yet; at ₦100,000/month Oct–Dec the investment ends the year near ₦336,959, not ₦705,000.
- **Payday B, 16 Sep:** ₦411,709. Goal 1 ₦146,041 and Buffer ₦50,000 moved the same day.
  Sister ₦40,000 paid (₦50,000 still owed).
- **September cuts, his calls:** creator visits ₦0, community admin held (the admin is
  working for free for now), giving ₦0. **Feeding ₦30,000 added** for the second half.
- **₦57,532 left unassigned in the current account, his call** — "liquid cash for anything
  that comes up." Named once: unassigned cash is how ₦595,250 went, and the Buffer
  exists for this. Check what it is at month end; whatever survives goes to a pot.
