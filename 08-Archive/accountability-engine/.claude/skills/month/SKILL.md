---
name: month
description: Month-end financial close — what came in, what went out, what survived.
---

Run on the last day of the month, or when Samuel asks.

1. Read `context/money.md` (whole — this skill genuinely needs the arithmetic)
   and `context/money-ledger.md`. Nothing else in context/.
2. State four numbers and nothing else first:
   - Total in
   - Total out
   - Savings moved, and savings still there
   - Building project: paid in full, or the shortfall amount
3. Compare against the ₦1M-by-31-Dec target. State months remaining and the
   monthly surplus required from here. If the required number went up, say so.
4. Invoice check: how many videos in this month's batch, at what rates, and what
   the 70% lands as. Flag any video below $333 and the naira cost of the gap.
5. Investment check: confirm the ₦100,000 went to Cowrywise and state the running
   balance. It is ring-fenced — it does not count toward the ₦1M or the ₦3M
   (money.md Rule 7). Report it separately, never inside the savings number.
6. Reconcile the mirror. Run `python tools/sheets/sheets.py flush`, then read the
   month's rows off the Income, Expenses and Transfers tabs and total them.
   Compare against the same totals from `context/money-ledger.md`. State both
   numbers in one line each. If they differ, the ledger wins — say which days are
   missing from the sheet and write them, do not adjust the ledger. A close that
   never opened the sheet is a close of half the record.
7. Ask one question: "What are you cutting next month?" Take the answer.
8. Append the month's close to context/memory.md. Commit and push.

No encouragement. The numbers do the work.
