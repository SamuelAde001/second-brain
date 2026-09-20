---
name: paid
description: Money landed. Log it, then move savings the same hour — before it gets spent.
---

Triggered when Samuel says he got paid. The point of this skill is not the logging.
The logging takes 30 seconds. The point is **money.md Rule 3: savings move FIRST,
on the day the money lands.** June–August proved that money saved at the end of the
month is money that was never saved — ₦595,250 of it.

So: log it, then make him move it, in the same conversation. Do not let him leave
this skill with the money sitting whole in the current account.

## 1. Read first

`context/money.md` — the rules, the batch history, the rate. Never run this from
memory. `git pull` first (REMOTE.md). Money is the one place a whole-file read is
worth it; do NOT also pull in the other domain files, the ledger notes or memory.md.

## 2. Ask, one question at a time. Short answers.

- **How much, and in what?** USD or NGN.
- **What rate did Cleva give?** If USD. Not the assumed 1,365 — the actual rate on
  the day. If he doesn't know, ask him to check; the assumed rate is a guess and
  guesses have been ₦40,000 wrong.
- **Who paid?** Route Rise Media LTD, the $175 client, or something else.
- **Which batch is this settling, and which stage?** 70% or 30%. Remember: the
  mid-month payment is ALWAYS the previous month's remaining 30%, never a new
  batch. If he calls a 30% payment "this month's money", correct him.
- **How many videos.**
- **What date did it LAND?** Not the invoice date. If it landed yesterday and he's
  telling you today, use yesterday.

Do the NGN arithmetic out loud. Show the multiplication.

## 3. Write it to the sheet

One row on **Income**, via `python tools/sheets/sheets.py`. Columns:
`Date | Month | Source | Videos | USD | Rate ₦/$ | ₦ from USD | ₦ other income | ₦ IN | Stage / note`

Append below the last real row. Never overwrite a row.

Run `python tools/sheets/sheets.py flush` first, then send this batch with
`--queue "paid <date> <source>"`. Works identically from the desktop, a cloud
routine or the phone: reachable, it writes; unreachable, it parks in
`context/sheet-queue.jsonl` and the next session that can reach the bridge sends
it. If it queued, say so plainly — do not report the sheet as written.

## 4. Now the part that matters — move it

Immediately, in the same breath, with the numbers in front of him:

- **Building project — ₦500,000.** Rule 4: paid in full before any discretionary
  line. August was ₦200,000. That shortfall is on the record. Ask what is going to
  the building today.
- **Cowrywise — ₦100,000.** Rule 7. Never pauses, never negotiable, never counts
  toward the ₦1M or the ₦3M.
- **Savings toward Goal 1.** Whatever the month's plan says. If there is no plan
  for the month, say so and run `/budget` instead of guessing.
- **From January 2027: marriage savings and the ₦300,000 emergency fund** join this
  list.

Ask what he is ACTUALLY moving today, in naira. Then:

- Write one **Transfers** row per pot that actually moved — `To pot`.
- **Only rows for money that actually moved.** A Transfers row for money he intends
  to move on Friday is Rule 6 broken: a budget line that says money was saved when
  no money moved is a lie in a spreadsheet.
- If he says "I'll move it later", say the word: **later is how ₦595,250
  disappeared.** Then ask what changes later. Do not write the row.

## 5. Write the ledger

Append the `In` amount and any savings moved to `context/money-ledger.md`. The
ledger is the source of truth; the sheet is the mirror. If the two ever disagree,
the ledger wins.

**And append every pot that moved to `context/spend.jsonl`,** one JSON object per
line, category `"Savings — <pot name>"` exactly as the pot is named in
`tools/sheets/plan.json`. Any transfer charge the bank took goes on its own line
under `"Bank charges"`, never folded into the pot amount — a pot has to read its
true figure. The site's Budget page reads ONLY this file for what has been paid;
a pot moved and not written here shows as unfunded on the site while the ledger
says it moved.

## 6. State what it did to the runway

Two lines, no more:

- What this payment does to the ₦1M by 31 Dec.
- Whether the month is on or off the pace.

If it puts him behind, say the number he is behind by. If income came in below the
4×$333.33 mix, name it — that is the concentration risk in `money.md` showing up in
real money, and the course is the only lever he owns.

## 7. Commit and push

Ledger, sheet confirmation, and anything appended to `context/memory.md`.

---

Do not congratulate him for being paid. Getting paid is not shipping. Moving the
money the same day is.
