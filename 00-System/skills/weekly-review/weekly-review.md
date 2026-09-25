---
name: weekly-review
description: "Samuel's Sunday weekly review and next week's plan: what shipped, must-dos planned vs done, what slipped and which of his patterns it matches, focus hours and habit check-ins, commitments kept or missed, whether it was a 'good week' by his own bar, then next week laid out and written into TickTick as timed tasks (never Google Calendar). Runs in the Sunday 3:00pm session straight after the money check (sunday-check). Use when that session reaches it, or when he says 'weekly review', 'review my week', 'plan next week', 'how did the week go'. Not for money (sunday-check covers that) or a single day (night-plan)."
type: skill
area: me
status: active
updated: 2026-09-25
source: interview
tags: [skill, planning, review, weekly]
---

# Weekly review

Samuel, 2026-09-22: yes to a weekly review, and to have it **merged into the Sunday 3:00pm session**: money check first, then this. His rule: *"Sunday is not a work buffer. Plan Sunday from 3:00pm."* Routine: [[00-System/automations/sunday-money-check|Sunday money check + weekly review]].

**Runs in the main session.** Act as the personal-life agent: read `07-Agents/personal-life/standing-rules.md` first (what he has settled, in any chat; it wins over anything older), then `profile.md` and `memory.md`. The message follows standing rules → how the reports must read: headed sections, one item per line, plain words, questions numbered at the end. Time zone `Africa/Lagos`. The week runs Monday to Sunday; the note is the ISO week, `YYYY-Www`.

## 1. Gather (tool calls and scripts, not whole files)

- **Done.** TickTick: tasks completed Monday–today, counted by project.
- **Slipped.** TickTick: undone tasks dated this week or earlier.
- **Planned vs done.** The week's daily notes: `06-Logs/daily/<date>.md` → `## Plan` and `## Done`. They're short, so read them.
- **Client work.** `python 00-System/scripts/money_ledger.py videos YYYY-MM` for delivered videos. TickTick 📹 Video editing for what's still open and its deadline.
- **Focus.** TickTick focus records for the week, both types (pomodoro `0`, timing `1`), summed per day in hours.
- **Habits.** TickTick check-ins for the week (stamps `yyyyMMdd`), per habit, as x/7.
- **Commitments.** `06-Logs/commitments.md`. For the three daily ones (must-dos, client deadlines and hours, start by 7:00am), count `- KEPT:` and `- MISS:` lines per commitment across the week's daily notes with grep, and read the `why:` reasons.
- **Money.** Take the one-line result from the money check that just ran in this session. Don't recompute it.
- **Next week.** Google Calendar events on every calendar, plus TickTick tasks dated next week.

## 2. The review, one message

1. **Good week?** His bar: *"client work all done, with free days to do my content and other stuffs in my life."* Yes or no, and why, in one line.
2. **Numbers:** must-dos done / planned · tasks done by project · client videos delivered · focus hours (flag any day over 12h: *"it is an invoice"*, P2) · habits x/7 each · the money line.
3. **Slipped,** by name. If it matches one of his [[02-Me/patterns|patterns]], name that pattern once, quoting his words. Most often it's P1: content dropped while client work ran.
4. **Commitments:** for each of the three daily ones, kept x/7 and missed y/7, with the reasons he gave. If one reason repeats, name it once as the thing to fix next week. The highest escalation level the week reached. Any other commitment: kept or missed, in his words, once. No penalty beyond the make-up rule he chose ([[07-Agents/personal-life/profile|profile]] → discipline).

The habits were made to match his routine on 2026-09-22 (memory). Report each as x/7. Gym is measured against his minimum of 3 a week, and a week under 3 is named once. None of the habits is a marked commitment, so there's no escalation.

## 3. Next week, with him

- **Fixed first:** client deadlines, meetings, calendar events.
- **Client work sized in hours, not days** (P5). If the hours don't fit the mornings, say so with the arithmetic.
- **Content gets its blocks named**, because it's the block that gets dropped (P1).
- Ask: *"What has to be true by next Sunday?"* At most three outcomes, in his words. The cap is a build default, and he can change it.
- On his yes, write it into TickTick, every block a timed task (profile → TickTick rules). Nothing goes on Google Calendar. Nothing is written without his answer.

## 4. Record

- `06-Logs/weekly/<YYYY-Www>.md` from `00-System/templates/weekly.md`: fill What shipped, Numbers, What slipped and why, Commitments checked, Next week (his outcomes in his words). For Brain health, use counts from the shell only (`grep -rl "status: needs-input"`, the file count in `01-Inbox/`). Leave out anything you can't fill cheaply.
- Append one line to `07-Agents/personal-life/log.md`.
- Commit `personal-life: weekly review <YYYY-Www>` with the Co-Authored-By trailer, then push.

## Tone

Direct and blunt. Only shipping gets acknowledged, never planning. Each slip gets said once.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
