---
name: sunday-check
description: "Samuel's weekly money check-in, every Sunday: he sends his bank balance, the finance agent works out what went unlogged since the last entry, logs it, rebuilds the 'Money' sheet and names every line that's over plan, plus what's left until the next payday. Use when he sends a balance or a bank screenshot on a Sunday, says 'Sunday check', 'weekly check', 'here's my balance', or it's Sunday and he opens a session without having done it. He committed to it on 2026-09-22."
type: skill
area: finances
status: active
updated: 2026-09-22
source: manual
tags: [skill, finances, check, weekly]
---

# Sunday check

Samuel chose it on 2026-09-22 (*"both checks"*) to keep his spending in check ([[06-Logs/commitments|commitments]]). The agent can't see his bank, so this weekly balance is what keeps the record honest between paydays.

**Runs in the main session.** Act as the finance agent: read `07-Agents/finance/profile.md` and `memory.md` first.

## 1. His balance

- **What's in the bank right now?** A screenshot is best. Say which it is: `screenshot` or `his words`.
- **Anything big since the last entry that isn't logged?** Any money taken out of a pot? A pot withdrawal is its own `from-pot` row, with the reason in his words (Rule 2).

## 2. Log the gap

```
python 00-System/scripts/money_ledger.py pots
```

Gap = derived bank − his balance − anything he just itemised. Log the gap as one `bulk` row, category `Other`, What `Minor spends <from>–<to>`, Note `derived`, followed by a `balance` row with his figure. If he can itemise any of it, itemise it instead. If he can't give a balance, log nothing and say the week stays open. **Never invent a figure.**

Then: `python 00-System/scripts/budget_sheet.py build`.

## 3. Tell him, short

```
python 00-System/scripts/budget_sheet.py left
```

- The week in one line: what went out, and how much of it was unplanned.
- **Every line over plan**, by name and amount. No softening.
- **What's left until the next payday**, and how many days that has to last. Payments have landed two days late before.
- If a commitment in [[06-Logs/commitments|commitments]] slipped, say so once, quoting his own words.

No praise for a good week. Numbers only.

## 4. Close

One line in `07-Agents/finance/log.md`. Commit: `finance: sunday check <date>`.
