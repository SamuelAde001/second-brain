---
name: night-plan
description: "Plan Samuel's tomorrow with him the night before: close out today (what got done, what didn't), lay tomorrow onto his real day in timed chunks, agree it with him, then write it into TickTick (and meetings onto Google Calendar) and a short daily note. Use when a routine opens it at 8:45pm WAT, or when he says 'plan tomorrow', 'plan my day', 'what am I doing tomorrow', 'set up tomorrow', or it's evening and tomorrow isn't planned. Not for the morning read-out (use morning-brief) or the Sunday week plan (use weekly-review)."
type: skill
area: me
status: active
updated: 2026-09-22
source: interview
tags: [skill, planning, ticktick, daily]
---

# Night plan

Samuel, 2026-09-22: *"I want to plan things a night before the next day."* His routine already says tomorrow is planned by 9:30pm ([[02-Me/daily-routine|daily routine]]). **A routine opens this every day at 8:45pm WAT**, before his 9:00pm call: [[00-System/automations/night-plan|night plan]].

**Runs in the main session.** Act as the personal-life agent: read `07-Agents/personal-life/profile.md` and `memory.md` first. Time zone `Africa/Lagos` on every call.

Why timed chunks: in [[02-Me/patterns|patterns]] (P5), the day that closed a client job in about eight hours was *"built into timed chunks before it started."* The day that wasn't built that way was lost.

## 1. Gather (tool calls, not files)

- **Today's result.** TickTick: tasks completed today, plus tasks still undone that were due today or earlier (the overdue ones).
- **Today's plan,** if a note exists: `06-Logs/daily/<today>.md` → `## Plan`.
- **Tomorrow.** TickTick: tasks already dated tomorrow. Google Calendar: tomorrow's events on every calendar he has.
- **Deadlines coming.** TickTick: undone tasks due in the next 7 days in 📹 Video editing, plus anything priority 5.
- **Commitments** due tomorrow: `06-Logs/commitments.md` (small file).
- **Carried items.** Grep the last three daily notes for anything already carried twice: `grep -l "<task title>" 06-Logs/daily/*.md`.

## 2. Propose, in one message

Keep it short. Times first.

1. **Today, one line.** Must-dos done out of planned, by name. What didn't get done, by name.
2. **Every unfinished item gets a place:** tomorrow, a named later date, or dropped. He chooses. A task carried a third time gets named once, as P5: *"the estimate never moves once the job starts."*
3. **Tomorrow, laid onto his day** ([[07-Agents/personal-life/profile|profile]] → his day):
   - Fixed times first (meetings, calls, the gym if it's a gym day).
   - **Client work 7:00am–1:00pm.** Name the job and its deadline, and say how many hours are left against that deadline. If the hours don't fit the days left, say so once, with the arithmetic.
   - Content 3:00–4:30pm and 7:00–9:00pm (client work instead in a deadline week).
   - **At most three must-dos,** marked priority 5. This cap is a build default, and he can change it.
4. **One question:** *"Change anything, or go?"* Then wait.

Never schedule over 6:00–6:30am, after 10:00pm, or Sunday before 3:00pm. Never invent a task or deadline.

## 3. On his answer, write it

- **TickTick.** Create or move each task to its date, in the project the [[00-System/ticktick-map|TickTick map]] gives it. Must-dos priority 5, the rest 3. Anything at a fixed time is a timed task with reminders at the time and 5 minutes before. Client video tasks follow the naming rule (*"Alex video (Sep #3) — edit block 4"*). Complete what he says is done. Delete only on his word.
- **Google Calendar.** Any meeting also goes on his primary calendar. No invitees unless he says so. Nothing on the joint calendar without his word.
- **If he doesn't answer,** write nothing to TickTick or the calendar. Log the line in step 4 and stop.

## 4. Record

- **Today's note** `06-Logs/daily/<today>.md` (create it from `00-System/templates/daily.md` if it's missing): append `## Done`, listing must-dos done / not done and anything carried, one line each.
- **Tomorrow's note** `06-Logs/daily/<tomorrow>.md` from the template, with only `## Plan` filled in: the fixed times, the must-dos and the client job with its hours. Leave out the template's empty sections. The task list stays in TickTick; this note is the record of what was planned.
- Append one line to `07-Agents/personal-life/log.md`.
- Commit `personal-life: plan for <tomorrow>` with the Co-Authored-By trailer, then push.

## Tone

Direct and blunt. No praise for planning. A slip gets named once, in his words, then leave it.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
