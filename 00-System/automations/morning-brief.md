---
type: sop
area: me
status: active
updated: 2026-09-22
source: interview
tags: [automation, planning, daily]
---

# Morning brief (automation)

**Every day at 6:30am WAT** a session opens and runs the [[morning-brief]] skill as the personal-life agent: today's fixed times, must-dos, client job, anything overdue, in ten lines or fewer.

- **Asked for by Samuel, 2026-09-22:** "Yes a morning brief routine". He picked 6:30am: straight after the prayer block (6:00–6:30am, never touched) and before client work at 7:00am.
- **Where it runs:** a scheduled task in the Claude desktop app (Code tab), `morning-brief`, cron `21 6 * * *`, PC time zone W. Central Africa (UTC+1). **Why :21:** the app adds a fixed delay of 9m32s to this task, so it really fires at 6:30:32am, after the prayer block (checked 2026-09-22). If the task is ever recreated, check `nextRunAt` and re-cut the cron. Tool copy: `C:\Users\repzy\.claude\scheduled-tasks\morning-brief\SKILL.md`. **This note is the canonical copy.** If the two differ, this one wins, and the task is updated to match.
- **It needs the app open.** If the PC is off at 6:30am, the brief is waiting when the app next opens.
- **It commits nothing** unless he answers and something changes.

## The prompt it runs

> Samuel's morning brief. He asked for it on 2026-09-22 and chose 6:30am WAT, straight after his 6:00–6:30am prayer block and before client work at 7:00am.
>
> Work in his Brain: C:\Users\repzy\Desktop\My Second brain. Its constitution is AGENTS.md. Follow it, especially token discipline (read only what the step needs).
>
> 1. Act as the personal-life agent. Read `07-Agents/personal-life/profile.md` and `07-Agents/personal-life/memory.md`, then run the skill `morning-brief` (canonical copy: `00-System/skills/morning-brief/morning-brief.md`) and follow it exactly. Use TickTick and Google Calendar through their connectors, time zone Africa/Lagos.
> 2. Send the brief as one message, ten lines or fewer. Ask a question only if something is overdue or clashes.
> 3. Change TickTick or the calendar only if he answers. If nothing changed, write nothing, log nothing and commit nothing.
> 4. Tone: direct and blunt. No motivational line, no praise.
> 5. If something changed: one line in `07-Agents/personal-life/log.md`, commit `personal-life: morning changes <YYYY-MM-DD>` ending with a Co-Authored-By trailer, then push.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
