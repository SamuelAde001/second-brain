---
name: morning-brief
description: "Samuel's morning brief at 6:30am WAT, right after his prayer block: today's fixed times, the must-dos agreed last night, the client job and its deadline, anything overdue, and any commitment due today, in about ten lines. Use when a routine opens it at 6:30am, or when he asks 'what's on today', 'what's my day', 'brief me', 'what do I have today'. Not for planning a day that hasn't been planned (use night-plan) or the weekly look back (use weekly-review)."
type: skill
area: me
status: active
updated: 2026-09-22
source: interview
tags: [skill, planning, ticktick, daily]
---

# Morning brief

Samuel asked for a morning brief routine on 2026-09-22. **A routine opens this every day at 6:30am WAT**, straight after the 6:00–6:30am prayer block and before client work at 7:00am: [[00-System/automations/morning-brief|morning brief]].

Why this hour: [[02-Me/patterns|patterns]] P4. *"A gap opening at 6am costs a day; a gap opening at 5pm costs a block."* The brief means the day starts with a plan already on the screen.

**Runs in the main session.** Act as the personal-life agent: read `07-Agents/personal-life/profile.md` and `memory.md` first. Time zone `Africa/Lagos`.

## 1. Gather (tool calls, not files)

- TickTick: undone tasks dated today, and undone tasks dated before today (overdue).
- Google Calendar: today's events on every calendar he has.
- `06-Logs/daily/<today>.md` → `## Plan`, if last night's plan exists.
- `06-Logs/commitments.md`: anything due today (on Sundays, the 3:00pm money check).
- The week's miss count: `cat 06-Logs/daily/<Monday..yesterday>.md | grep -c "^- MISS:"` (0 on a Monday).

## 2. The brief, one message, ten lines or fewer

```
<Day> <YYYY-MM-DD>. Planned last night: yes / no.
Fixed: <time> <what> · <time> <what>
Make-up first: <missed must-do> (if any)
Must-dos: 1. … 2. … 3. …
Client: <job> — due <date>, <hours> left
Overdue: <n> — <names>
Due today: <commitment, if any>
Misses this week: <n>. Client work starts 7:00am.
```

- If there was **no plan last night**, say so in that one line, and take the must-dos from today's priority-5 tasks. Don't lecture.
- If a **client video is due today or tomorrow**, offer the edit clock once (skill `edit-clock`).
- If **anything is overdue or clashes**, end with one question proposing a date for each item. Otherwise end without a question.
- The last line always gives the week's miss count and the 7:00am start. It's a fact, not a pep talk. Don't ask him to confirm the start (he chose no check-ins); the night plan checks it.
- No motivational line. No praise.

## 3. Only if he answers

Apply what he says in TickTick and the calendar (profile → permissions). Then append one line to `07-Agents/personal-life/log.md`, commit `personal-life: morning changes <YYYY-MM-DD>` with the Co-Authored-By trailer, and push.

**If he doesn't answer, or nothing changed:** write nothing, log nothing, commit nothing. A read-out is not an action worth a commit.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
