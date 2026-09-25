---
type: sop
area: me
status: active
updated: 2026-09-25
source: interview
tags: [automation, planning, daily]
---

# Morning brief (automation)

**Every day at 6:30am WAT** a session opens and runs the [[morning-brief]] skill as the personal-life agent: today's fixed times, must-dos, client job, anything overdue, in ten lines or fewer.

- **Asked for by Samuel, 2026-09-22:** "Yes a morning brief routine". He picked 6:30am: straight after the prayer block (6:00–6:30am, never touched) and before client work at 7:00am.
- **Model:** Sonnet 5 (`claude-sonnet-5`). Samuel, 2026-09-23: *"they aren't heavy tasks, they are not my agents, but they may call agents if needed to do better tasks"*. A step that needs an agent's judgement is handed to a subagent on Opus 5.5 with that agent's profile.
- **Where it runs:** a **cloud routine** on claude.ai, "Morning brief (6:30am WAT)", id `trig_01UN9y23v1UwoBtBq3qmoJiH` (https://claude.ai/code/routines/trig_01UN9y23v1UwoBtBq3qmoJiH). Cron `30 5 * * *` in UTC = 6:30am WAT; the service adds a delay of about 4 minutes, so it fires about 6:34am (checked 2026-09-22). Repo `SamuelAde001/second-brain`, connectors TickTick and Google Calendar, model tier standard (Sonnet 5). **This note is the canonical copy.** If the two differ, this one wins, and the routine is updated to match.
- **Why cloud (Samuel, 2026-09-22):** he couldn't see the routine or its notifications on his phone. A cloud routine runs with the PC off and shows in the Claude app on the phone, where he can answer it. It replaced the desktop-app task `morning-brief`, which is paused, not deleted.
- **It commits nothing** unless he answers and something changes.

## The prompt it runs

Rewritten 2026-09-25 (Samuel: the reports read *"like it's talking to itself"*, forgot rules he had settled in other chats, didn't list the day's main tasks, and didn't work from TickTick or check his habits). Formatting and checks now live in the skill; the prompt only points to it.

> Samuel's morning brief, as PA. He asked for it on 2026-09-22 and chose 6:30am WAT, after his 6:00–6:30am prayer block and before client work at 7:00am. This is a cloud routine so he reads it on his phone.
>
> You are in a clone of his Brain (GitHub SamuelAde001/second-brain). Its constitution is AGENTS.md. Token discipline: read only what each step needs. The machine runs in UTC; today is `TZ=Africa/Lagos date +%F`.
>
> 0. Sync first: `git fetch origin main && git checkout main && git merge --ff-only origin/main`.
> 1. Run the skill `morning-brief` (canonical: `00-System/skills/morning-brief/morning-brief.md`) exactly, as PA. Step 0 of the skill comes first: read `07-Agents/personal-life/standing-rules.md` in full, then the profile, memory, today's note and last night's check. Standing rules win over anything older.
> 2. Build the day from TickTick (every task dated today, with times), plus habits, overdue tasks and Google Calendar (read only). Connectors via ToolSearch if deferred, time zone Africa/Lagos.
> 3. Send one message in the exact shape in step 2 of the skill: **Main tasks first**, then the schedule, habits, client, overdue, yesterday's result. Headed sections, one item per line, blank lines between sections, plain words. Write to him, not to yourself. Ask a question only if something is overdue or clashes.
> 4. Straight after, call PushNotification (load with ToolSearch if deferred; `status: "proactive"`) with one line under 200 characters: the top main tasks with times, plus anything overdue. Every run.
> 5. Change TickTick only if he answers. Never Google Calendar. If nothing changed, write, log and commit nothing. If something changed: a log line, commit `personal-life: morning changes <YYYY-MM-DD>` ending with `Co-Authored-By: Claude <noreply@anthropic.com>`, then `git fetch origin main`, `git merge origin/main`, `git push origin HEAD:main`. Never force-push.
> 6. Anything that needs the PC goes as one line in `01-Inbox/`. Another agent's judgement: a subagent on model opus with that agent's profile and memory.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
