---
name: payday
description: "Money landed. Log it in Samuel's money ledger, rebuild his 'Money' sheet, then get the week-of-pay transfers and the savings moved the same day, before it gets spent (money Rule 3). Use whenever Samuel says he got paid, money landed or came in, Cleva converted, the 70% or the 30% arrived, Route Rise paid, or it's Payday A or Payday B, even if he only mentions an amount. Not for planning a month that hasn't been paid yet (use budget) or for the month-end close (use month-close)."
type: skill
area: finances
status: active
updated: 2026-09-22
source: legacy-accountability-engine
tags: [skill, finances, payday]
---

# Payday

Rebuilt 2026-09-22 from the engine's `paid` ritual (legacy review R8, kept).

**The point is not the logging.** Logging takes a minute. The point is Rule 3: **savings and the week-of-pay transfers move the day the money lands.** June to August 2026 proved that money saved at month end was never saved: NGN 595,250 of it. So don't let him leave this skill with the money sitting whole in the account.

**Runs in the main session.** It's a conversation. Act as the finance agent: read `07-Agents/finance/profile.md` and `07-Agents/finance/memory.md` first.

## 1. Read, and nothing else

- `03-Areas/finances/money-rules.md`: the eight rules
- `03-Areas/finances/income.md`: the payment shape. The mid-month payment is **always the previous month's 30%**, never new money
- The month's plan, `03-Areas/finances/plans/plan-YYYY-MM.md` (or `obligations.md` if the month has no plan file yet): its lines and which are Payday A or B
- `python 00-System/scripts/money_ledger.py pots` and `last 8`: where the record stands, as of when
- `python 00-System/scripts/money_ledger.py videos <batch YYYY-MM>`: what the video-editor recorded as delivered for this batch

## 2. Close the gap since the last payday first

Before the new money is logged, ask:
- **What's the balance right now, before this payment?** A screenshot is best. Say which it is.
- **Anything major since the last payday that isn't logged?** Anything taken out of a pot? A pot withdrawal is Rule 2: its own `from-pot` row, reason in his words.

Then the minor spends since the last payday are one `bulk` row: derived bank − balance now − unlogged majors. Mark it `derived`. If he can't give a balance, write no bulk row and say the gap stays open. **Never invent a figure to make it balance.**

## 3. The payment: one question at a time, short answers

- **How much, and in what currency?** Gross and net, if USD.
- **What rate did Cleva give on the day?** The actual rate. If he doesn't know, ask him to check. Assumed rates have been wrong before.
- **Who paid?** Route Rise, or someone else.
- **Which batch, which stage?** 70% or 30%. If he calls a 30% payment "this month's money", correct him.
- **How many videos?** Check the count from `videos` against his. If they differ, ask which videos are missing, and hand the missing rows to the video-editor through the orchestrator. Finance never writes that record.
- **What date did it land?** Not the invoice date.

**Do the NGN arithmetic out loud:** USD net × rate = NGN. Show it.

Append the `in` row to `03-Areas/finances/money-ledger.md`. The Note carries USD gross/net, the rate, the batch and the stage.

## 4. Now the part that matters: move it

With the numbers in front of him, list this payday's lines, with amounts, from the month's plan file (its Payday column). The pots move by Rule 3: Cowrywise on Payday A; Goal 1 and the Buffer on Payday B.

- **Rule 4:** the building project, NGN 500,000, is paid in full before any discretionary line.
- **Rule 7:** Cowrywise NGN 100,000 never pauses and never counts toward a goal.
- **Rule 3 excess:** if Payday A leaves more than NGN 50,000 free after its commitments, the excess moves the same day.
- From January 2027: Goal 2 (marriage) and the NGN 300,000 emergency fund join the list.

Ask what is **actually going out today**, in naira. Then write:
- each payment sent → a `major` row, category = the line in the month's plan, exactly
- each pot funded → a `to-pot` row, pot name exact
- bank charges he can't attribute → one `charges` row
- **only for money that actually moved.** A row for Friday's transfer is Rule 6 broken. If he says "I'll move it later", say it once: **later is how NGN 595,250 disappeared.** Ask what changes later. Don't write the row.

The first main shopping of the pay cycle is **major**. When it happens, it gets its own row.

## 5. Rebuild the sheet

```
python 00-System/scripts/budget_sheet.py build
```

The "Money" sheet is rebuilt from the ledger, so it can't disagree with it. If the build fails, say so. The ledger is already written, so nothing is lost. Run the build again next session.

## 6. What it did to the runway: two lines, no more

- Goal 1 now, as of today, against NGN 1,000,000 by 2026-12-31, and the NGN per month still needed from here.
- On pace or off. If off, the number he's behind by. If the batch came in under 4 × USD 333.33, name the video count and what it cost. That is the one-payer risk in `income.md`, in real money.

## 7. Close

Append a line to `07-Agents/finance/log.md`, and anything new about how money behaves to its `memory.md`. Commit: `finance: payday <date> <stage>`.

Don't congratulate him for being paid. Getting paid is not shipping. Moving the money the same day is.
