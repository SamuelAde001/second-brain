---
name: budget
description: "Set or change a month's money plan with Samuel: take his spending plans in his own words, categorise them, write each one as a named line on the 'My Claude Budget' sheet's Details tab, then say out loud whether the arithmetic works against the money that actually exists. Use whenever he wants to budget, plan a month, replan after a short month, change what a category gets, or add, cancel or change a subscription or recurring line. Not for logging money that landed (use payday) or closing a finished month (use month-close)."
type: skill
area: finances
status: active
updated: 2026-09-22
source: legacy-accountability-engine
tags: [skill, finances, budget]
---

# Budget

Rebuilt 2026-09-22 from the engine's `budget` ritual (legacy review R7, kept).

A budget is not a wish list. **It's a claim that the money exists.** This skill writes the claim down, then checks it against the money that actually exists, before he acts on it.

**Runs in the main session.** It's a conversation. Act as the finance agent: read `07-Agents/finance/profile.md` and `07-Agents/finance/memory.md` first.

## 1. Read

- `03-Areas/finances/money-rules.md`, `obligations.md`, `finances-goals.md`: the rules, the floor, the goal arithmetic
- `python 00-System/scripts/money_ledger.py pots`: the pots, as of the last row
- `python 00-System/scripts/money_ledger.py videos <month>`: videos already delivered for the batch
- The sheet's current plan: `python 00-System/scripts/sheets.py read Details` and `read Setup`. If the bridge is down, say so and plan from `obligations.md`. The batch queues.

## 2. Ask

- **Which month?**
- **How much money is there to budget?** What's in the account today, and what's expected to land, **kept separate.** Expected money is not money in hand. The 30% mid-month payment is last month's batch: real, but dated, and payments have landed two days late.
- **Which video count does this plan assume?** Show what 2, 3 and 4 videos produce at USD 333.33 (`income.md`). He picks. The plan names it (hard limit 5).
- **Then let him talk.** Take his plans in his own words, whole, without interrupting to categorise. Write them down first.

## 3. Categorise

Map every line onto a category on the sheet's **Setup** tab. Savings are not expense categories: pots move through **Transfers**.

- If a line doesn't fit, **ask** where it belongs. Don't invent a category, and don't quietly drop it into Other. If "Other" grows every month, it's a category he's hiding something in. Say so.
- Read each line back to him in the category you put it in. One line each.

## 4. Every line is a named item on Details

**A category total is never a mystery number.** Subscriptions are Claude + CapCut + Google + the rest, each with its amount and renewal date.

One row per item: `Category | Item | Amount | Frequency | Renews / due | Active? | Note` (check the tab's header row first).

- Changing an amount → edit that item's row, **with his yes**. It overwrites his entry (profile: must ask).
- Cancelling → set Active to `No`. **Never delete the row.** A cancelled subscription that comes back in three months is a pattern, and a deleted row hides it.
- Adding → a new row, and say what it displaces. A new line item doesn't make new money.
- **Never type a plan number on the Budget or Dashboard tabs.** They read Details through SUMIFS ([[03-Areas/finances/budget-system|budget system]]).

## 5. The arithmetic, out loud

Total the plan. Add the pots for the month: building NGN 500,000, Cowrywise NGN 100,000, Goal 1, the Buffer, and from January 2027 Goal 2 and the emergency fund. Compare to money in hand plus expected, at the chosen video count.

- **If it doesn't balance, say the shortfall in NGN.** Don't trim a category quietly to make it fit. Show the gap and make him choose what goes. If he wants the cut order, it's Rule 8: personal/misc → creator visits → household down to NGN 20,000 → the Buffer → a conversation.
- **Rule 4:** if the plan underfunds the building, name it, and name the August NGN 300,000 shortfall.
- **Rule 7:** Cowrywise NGN 100,000 doesn't flex.
- **Rule 1:** a plan that only balances by taking from savings is not a budget.
- **Goal 1:** say what the plan leaves toward NGN 1,000,000 by 2026-12-31, and the NGN per month still needed from here. If that number went up, say so. Every month.
- **Overspend shows red, never blocks.** His rule for the sheet: *"let me see it in red when it is more than 100% so I can adjust."* No pop-ups, no validation that stops him.

## 6. Write it

```
python 00-System/scripts/sheets.py flush
python 00-System/scripts/sheets.py ops <file> --queue "budget <YYYY-MM>"
```

Confirm what changed, one line per item: category, old amount, new amount. If it queued, say so. A queued plan is not a plan the sheet has.

## 7. Record

- A **recurring** line that changed → a dated note in `obligations.md`. Never rewrite the old figure. Say what it was and when it changed.
- A decision he made → `03-Areas/finances/finances-decisions.md`, in his words.
- One line in `07-Agents/finance/log.md`. Commit: `finance: budget <YYYY-MM>`.

Never congratulate him for making a budget. A budget is a plan. The only thing worth acknowledging is a month where the plan and the record ended up matching.
