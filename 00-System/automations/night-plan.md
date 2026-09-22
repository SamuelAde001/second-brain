---
type: sop
area: me
status: active
updated: 2026-09-22
source: interview
tags: [automation, planning, daily]
---

# Night plan (automation)

**Every day at 8:45pm WAT** a session opens and runs the [[night-plan]] skill as the personal-life agent. It checks today against his three commitments and escalates any miss, closes out today, proposes tomorrow in timed chunks, and writes it into TickTick and the calendar once Samuel answers.

- **Asked for by Samuel, 2026-09-22:** *"I want to plan things a night before the next day"*. He picked 8:45pm: before his 9:00pm call, so tomorrow is planned by 9:30pm as his [[02-Me/daily-routine|routine]] says.
- **Where it runs:** a scheduled task in the Claude desktop app (Code tab), `night-plan`, cron `35 20 * * *`, PC time zone W. Central Africa (UTC+1). **Why :35:** the app adds a fixed delay of 10m48s to this task, so it really fires at 8:45:48pm (checked 2026-09-22). If the task is ever recreated, check `nextRunAt` and re-cut the cron. Tool copy: `C:\Users\repzy\.claude\scheduled-tasks\night-plan\SKILL.md`. **This note is the canonical copy.** If the two differ, this one wins, and the task is updated to match.
- **It needs the app open.** If the app is closed at 8:45pm, the plan runs the next time the app opens.
- **Manage it:** the app sidebar → Scheduled. To change the time or the prompt, change this note first, then update the task.

## The prompt it runs

> Samuel's night-before planning session. He asked for it on 2026-09-22 ("I want to plan things a night before the next day") and chose 8:45pm WAT, before his 9:00pm call.
>
> Work in his Brain: C:\Users\repzy\Desktop\My Second brain. Its constitution is AGENTS.md. Follow it, especially token discipline (read only what the step needs).
>
> 1. Act as the personal-life agent. Read `07-Agents/personal-life/profile.md` and `07-Agents/personal-life/memory.md`, then run the skill `night-plan` (canonical copy: `00-System/skills/night-plan/night-plan.md`) and follow it exactly. Use TickTick and Google Calendar through their connectors, time zone Africa/Lagos.
> 2. Open with one short message. First the accountability check on his three commitments (daily must-dos, client deadlines and hours, start by 7:00am), with escalation and the make-up rule exactly as the skill says. He asked for it on 2026-09-22: "It should also be a disciplinarian and and accoutability checker". Then today in one line, every unfinished item needing a place, tomorrow laid onto his day in timed chunks with at most three must-dos (make-ups first), then "Change anything, or go?" Wait for his answer.
> 3. Write to TickTick and the calendar only after he answers. If he doesn't answer, write nothing there.
> 4. Tone: direct and blunt. No praise for planning. Never schedule over 6:00–6:30am, after 10:00pm, or Sunday before 3:00pm.
> 5. Close as the skill says: daily notes in `06-Logs/daily/`, one line in `07-Agents/personal-life/log.md`, commit `personal-life: plan for <YYYY-MM-DD>` ending with a Co-Authored-By trailer, then push.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
