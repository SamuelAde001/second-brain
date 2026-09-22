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
- **Where it runs:** a **cloud routine** on claude.ai, "Night plan (8:45pm WAT)", id `trig_01Pet8jENJ1CEguycgH9suEf` (https://claude.ai/code/routines/trig_01Pet8jENJ1CEguycgH9suEf). Cron `45 19 * * *` in UTC = 8:45pm WAT, no delay (checked 2026-09-22). Repo `SamuelAde001/second-brain`, connectors TickTick and Google Calendar, model tier standard (Sonnet 5). **This note is the canonical copy.** If the two differ, this one wins, and the routine is updated to match.
- **Why cloud (Samuel, 2026-09-22):** he couldn't see the routine or its notifications on his phone. A cloud routine runs with the PC off and shows in the Claude app on the phone, where he answers "Change anything, or go?". It replaced the desktop-app task `night-plan`, which is paused, not deleted.
- **Manage it:** the app sidebar → Scheduled. To change the time or the prompt, change this note first, then update the task.

## The prompt it runs

> Samuel's night-before planning session. He asked for it on 2026-09-22 ("I want to plan things a night before the next day") and chose 8:45pm WAT, before his 9:00pm call. This is a cloud routine so he can read and answer it on his phone.
>
> You are in a clone of his Brain (GitHub SamuelAde001/second-brain). Its constitution is AGENTS.md. Follow it, especially token discipline (read only what the step needs). This machine runs in UTC: today's date is the date in Africa/Lagos (UTC+1). Get it with `TZ=Africa/Lagos date +%F`. Tomorrow is the next day after that.
>
> 1. Act as the personal-life agent. Read `07-Agents/personal-life/profile.md` and `07-Agents/personal-life/memory.md`, then run the skill `night-plan` (canonical copy: `00-System/skills/night-plan/night-plan.md`) and follow it exactly. Use TickTick and Google Calendar through their connectors (load them with ToolSearch if deferred), time zone Africa/Lagos.
> 2. Open with one short message. First the accountability check on his three commitments (daily must-dos, client deadlines and hours, start by 7:00am), with escalation and the make-up rule exactly as the skill says. He asked for it on 2026-09-22: "It should also be a disciplinarian and and accoutability checker". Then today in one line, every unfinished item needing a place, tomorrow laid onto his day in timed chunks with at most three must-dos (make-ups first), then "Change anything, or go?" Wait for his answer.
> 3. Write to TickTick and the calendar only after he answers. If he doesn't answer, write nothing there.
> 4. Tone: direct and blunt. No praise for planning. Never schedule over 6:00–6:30am, after 10:00pm, or Sunday before 3:00pm.
> 5. Close as the skill says: daily notes in `06-Logs/daily/`, one line in `07-Agents/personal-life/log.md`, commit `personal-life: plan for <YYYY-MM-DD>` ending with the trailer `Co-Authored-By: Claude <noreply@anthropic.com>`. Then follow `00-System/portability.md` -> Cloud sessions and the PC: `git fetch origin main`, `git merge origin/main` (never rebase), `git push origin HEAD:main`. Never force-push. On a merge conflict, stop and tell him.
> 6. Anything that needs the PC (Money sheet, DaVinci Resolve, `01-Inbox/_imports/`) goes as one line in `01-Inbox/` for the PC. Do not attempt it.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
