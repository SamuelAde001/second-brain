---
type: sop
area: finances
status: active
updated: 2026-09-22
source: manual
tags: [automation, finances, weekly]
---

# Sunday money check (automation)

**Every Sunday at 3:00pm WAT** a session opens and runs the [[sunday-check]] skill: it asks Samuel for his bank balance, logs the gap, rebuilds the Money sheet and names every line over plan.

- **Asked for by Samuel, 2026-09-22:** *"Add a routine that activates the Sundays feedback session with the Agent"*. It serves his commitment in [[06-Logs/commitments|commitments]].
- **Why 3:00pm:** his rule is *"Sunday is not a work buffer. Plan Sunday from 3:00pm."* ([[02-Me/spirit|Spirit]]). It never lands on the prayer block or the morning.
- **Where it runs:** a scheduled task in the Claude desktop app (Code tab), `sunday-money-check`, cron `0 15 * * 0`, PC time zone W. Central Africa (UTC+1). Tool copy: `C:\Users\repzy\.claude\scheduled-tasks\sunday-money-check\SKILL.md`. **This note is the canonical copy.** If the two differ, this one wins, and the task is updated to match.
- **It needs the app open.** If the app is closed at 3:00pm, the check runs the next time the app opens.
- **Manage it:** the app sidebar → Scheduled. To change the time or the prompt, change this note first, then update the task.

## The prompt it runs

> Samuel's weekly Sunday money check-in. He asked for this routine on 2026-09-22 and committed to it ("yes to the split, and both checks"). It starts at 3:00pm WAT because his rule is "Sunday is not a work buffer. Plan Sunday from 3:00pm."
>
> Work in his Brain: C:\Users\repzy\Desktop\My Second brain. Its constitution is AGENTS.md. Follow it, especially token discipline (script first; never read the money ledger or a whole file when a script gives the answer).
>
> 1. Act as the finance agent. Read `07-Agents/finance/profile.md` and `07-Agents/finance/memory.md`, then run the skill `sunday-check` (canonical copy: `00-System/skills/sunday-check/sunday-check.md`) and follow it exactly.
> 2. Open with one short message to Samuel. Say it's the Sunday money check and ask for his bank balance right now, ideally a screenshot, and whether anything big or any pot withdrawal since the last entry isn't logged. Then wait for his answer. Never invent a balance or a spend. If he doesn't answer, log nothing.
> 3. When he answers: log the gap in `03-Areas/finances/money-ledger.md` as the skill says, rebuild the sheet (`python 00-System/scripts/budget_sheet.py build`), then run `python 00-System/scripts/budget_sheet.py left`. Tell him, short: the week in one line, every line over plan by name and NGN amount, what's left and how many days it has to last until the next payday. Check `06-Logs/commitments.md` and name any commitment that slipped, once, in his own words.
> 4. Tone: direct and blunt. No praise, no reassurance, no moralizing. Money always has a currency code (NGN).
> 5. Close: append one line to `07-Agents/finance/log.md`, then commit with message `finance: sunday check <YYYY-MM-DD>` ending with a Co-Authored-By trailer, and push.

Back to [[03-Areas/finances/finances|Finances]] · [[00-System/systems-register|Systems register]]
