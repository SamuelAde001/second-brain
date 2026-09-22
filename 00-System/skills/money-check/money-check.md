---
name: money-check
description: "Samuel asks before spending money that isn't in the month's plan, and gets a one-line answer: which plan line it would come from, what's left after, and whether it breaks the month. Use whenever he says 'can I spend', 'can I afford', 'should I buy', 'I want to send someone money', 'is it okay to…', names an amount he's about to spend, or asks about something on his wish list. He committed to asking first on 2026-09-22. Not for logging money already spent after the fact (log it, then run this if it was off-plan) or for payday (use payday)."
type: skill
area: finances
status: active
updated: 2026-09-22
source: manual
tags: [skill, finances, check]
---

# Money check

Samuel, 2026-09-22: *"You can see I spend out of hand, I need the Financial agent to keep me in check."* He chose to ask before any spend that isn't in the month's plan ([[06-Logs/commitments|commitments]]). This skill is the answer he gets. It's also the Phase 4 `money-check` job skill.

**Runs in the main session.** Act as the finance agent: read `07-Agents/finance/profile.md` and `memory.md` first.

## 1. Get the state. One command, nothing read whole

```
python 00-System/scripts/budget_sheet.py left
```

That gives the bank as of the last row, every line with what's left, anything over, the unplanned spending so far, and the Buffer.

## 2. Answer in three lines, no more

1. **Which line pays for it**, and what that line has left after: *"From Eating out: NGN 10,000 left → NGN 4,000 after."*
2. **The bank after**, as of the last row: *"Bank NGN 61,567 → NGN 55,567."*
3. **The verdict**, one of:
   - **Fits.** The line covers it.
   - **Fits, but empties the line.** Name what that line was still for.
   - **Doesn't fit.** Say the shortfall in NGN and which line it would come out of instead, following Rule 8's cut order: personal/misc → creator visits → household → Buffer. If the Buffer is empty: *"Nothing under you. Rule 8: an urgency is negotiated, not funded."* Never suggest Goal 1 or the investment.
   - **It's a savings pot.** If it could only come from Goal 1, the emergency fund or Cowrywise, say it's Rule 1 or Rule 7 and name the three allowed reasons. It's his call. Say the cost once, then stop.

No lecture, no second warning. He decides.

## 3. If he goes ahead

He tells you it's spent, or he said yes → append the row to `03-Areas/finances/money-ledger.md` with the category of the line that paid for it, then `python 00-System/scripts/budget_sheet.py build`. If he doesn't answer, write nothing: only money that moved gets a row.

## 4. For something on the wish list

Use the four steps in [[03-Areas/finances/wish-list|the wish list]] instead of a one-liner.

Log one line in `07-Agents/finance/log.md`: the ask, the verdict, what he chose.
