---
name: budget
description: Set or change the month's plan — take Samuel's spending plans, categorise them, write them into the sheet, and say out loud whether the arithmetic works.
---

Triggered when Samuel says he wants to budget, or wants to change what a category
gets, or adds/removes a subscription or a recurring line.

A budget here is not a wish list. It is a claim that the money exists. This skill's
job is to write the claim down **and then check it against the money that actually
exists**, before he acts on it.

## 1. Read first

`context/money.md` (rules, obligations floor, the goal arithmetic) — whole, this
skill needs the arithmetic — and nothing else from context/. Then the current
sheet state:

```bash
python tools/sheets/sheets.py read Details
python tools/sheets/sheets.py read Budget A1:C40
```

`git pull` first. Never run this from memory.

## 2. Ask

- **Which month is this for?**
- **How much money are you budgeting?** What is actually in the account today, and
  what is expected to land this month — kept separate. Do not let expected money be
  treated as money in hand. The 30% mid-month payment is the previous month's
  batch; it is real, but it is dated.
- **Then let him talk.** Take his plans in his own words, whole. Do not interrupt
  to categorise. Write them down first.

## 3. Categorise

Map every line onto the categories on the **Setup** tab:

`Building project · Parents · Girlfriend · Community admin · Subscriptions ·
Feeding · Giving · Transport · Creator visits · Data / airtime · Health ·
Chores / household · Other`

Savings are NOT expense categories. They live in the Savings Plan block and move
through **Transfers**.

Rules for categorising:

- If something does not fit, **ask** which category it belongs to. Do not invent a
  category and do not quietly drop it into Other. "Other" that grows every month is
  a category he is hiding something in — say so.
- Read his line back to him in the category you put it in. One line each.

## 4. Every line becomes a named item on Details

This is the whole point of the Details tab: **a category total is never a mystery
number.** ₦84,500 of subscriptions is not a budget line, it is Claude + CapCut +
Google + whatever else, each with its own amount and renewal date.

Write one row per item:
`Category | Item | ₦ Amount | Frequency | Renews / due | Active? | Note`

- Changing an amount → edit that item's row.
- Cancelling something → set Active to `No`. **Do not delete the row.** A cancelled
  subscription that reappears in three months is a pattern, and a deleted row hides
  it.
- Adding something new → new row, and say what it displaces. Money is not new
  because a line item is new.

The **Budget** tab's `Plan / month` column reads Details with SUMIFS. Never type a
plan number on Budget directly — if the plan and the detail disagree, one of them
is a lie, and this design makes that impossible.

## 5. Now do the arithmetic out loud

Total the plan. Add the savings plan for that month (building, Cowrywise ₦100,000,
Goal 1, and from January 2027 marriage + emergency fund). Compare to money in hand
plus expected.

Then say it plainly:

- **If it does not balance, say the shortfall in naira.** Do not quietly trim a
  category to make it fit. Show him the gap and make him choose what goes.
- **Rule 4:** building project ₦500,000 before any discretionary line. If his plan
  underfunds it, name it and name the August ₦300,000 shortfall.
- **Rule 7:** ₦100,000 Cowrywise is not a variable. It does not flex to make a
  month work.
- **Rule 1:** if the plan only balances by taking from savings, that is not a
  budget. Only three permitted withdrawals — medical emergency, building shortfall
  that would stop work, family emergency. A girlfriend's visit is not an emergency.
- If the month's plan leaves less surplus than the ₦1M needs, **say the number the
  December target is short by.** Every month.

## 6. Write it

Run `python tools/sheets/sheets.py flush` first, then push Details and the Budget
plan column to the sheet in one `ops` batch sent with `--queue "budget <month>"`.
Confirm back what changed — category, old number, new number. If the batch was
queued rather than written, say so in that line — a queued plan is not a plan the
sheet has.

## 7. Record

- Append material changes to `context/money.md` (the obligations table, if a
  recurring line changed) — but never rewrite history, and never change
  `mission.md` or `stakes.md`.
- Anything he decided that should survive the session → `context/memory.md`.
- Commit and push. Run `bash tools/bundle.sh` if anything under `context/` changed.

---

Never congratulate him for making a budget. A budget is a plan, and plans are the
addiction. The only thing worth acknowledging is a month where the plan and the
Expenses tab ended up matching.
