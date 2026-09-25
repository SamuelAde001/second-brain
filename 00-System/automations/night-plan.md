---
type: sop
area: me
status: active
updated: 2026-09-25
source: interview
tags: [automation, planning, daily]
---

# Night plan (automation)

**Every day at 8:45pm WAT** a session opens and runs the [[night-plan]] skill as the personal-life agent. It checks today against his three commitments and escalates any miss, closes out today, proposes tomorrow in timed chunks, and writes it into TickTick once Samuel answers (never Google Calendar).

- **Asked for by Samuel, 2026-09-22:** *"I want to plan things a night before the next day"*. He picked 8:45pm: before his 9:00pm call, so tomorrow is planned by 9:30pm as his [[02-Me/daily-routine|routine]] says.
- **Model:** Opus 5.5 (`claude-opus-5-5`), **since 2026-09-25**. Samuel: *"Yes move night plan to Opus"*, after the Sonnet run of 2026-09-24 missed a same-day replan. It was Sonnet 5 from 2026-09-23 (*"they aren't heavy tasks, they are not my agents"*). The night check is the judgement-heavy routine; the morning brief stays on Sonnet.
- **Where it runs:** a **cloud routine** on claude.ai, "Night plan (8:45pm WAT)", id `trig_01Pet8jENJ1CEguycgH9suEf` (https://claude.ai/code/routines/trig_01Pet8jENJ1CEguycgH9suEf). Cron `45 19 * * *` in UTC = 8:45pm WAT, no delay (checked 2026-09-22). Repo `SamuelAde001/second-brain`, connectors TickTick and Google Calendar, model tier strong (Opus 5.5). **This note is the canonical copy.** If the two differ, this one wins, and the routine is updated to match.
- **Why cloud (Samuel, 2026-09-22):** he couldn't see the routine or its notifications on his phone. A cloud routine runs with the PC off and shows in the Claude app on the phone, where he answers "Change anything, or go?". It replaced the desktop-app task `night-plan`, which is paused, not deleted.
- **Manage it:** the app sidebar → Scheduled. To change the time or the prompt, change this note first, then update the task.

## The prompt it runs

Rewritten 2026-09-25 (Samuel: the reports read *"like it's talking to itself"*, forgot rules he had settled in other chats, didn't list the day's main tasks, and didn't work from TickTick or check his habits). Formatting and checks now live in the skill; the prompt only points to it.

> Samuel's night check and plan for tomorrow, as PA. He asked for it on 2026-09-22 ("I want to plan things a night before the next day") and chose 8:45pm WAT. This is a cloud routine so he reads and answers it on his phone.
>
> You are in a clone of his Brain (GitHub SamuelAde001/second-brain). Its constitution is AGENTS.md. Token discipline: read only what each step needs. The machine runs in UTC; today is `TZ=Africa/Lagos date +%F`, tomorrow is the day after.
>
> 0. Sync first: `git fetch origin main && git checkout main && git merge --ff-only origin/main`. Rules he settled in other chats today only reach you this way.
> 1. Run the skill `night-plan` (canonical: `00-System/skills/night-plan/night-plan.md`) exactly, as PA. Step 0 of the skill comes first: read `07-Agents/personal-life/standing-rules.md` in full, then the profile, memory, commitments and **all** of today's daily note, replans included. Standing rules win over anything older.
> 2. TickTick is the record of the day: what was planned, what was ticked, what moved, the habits. Use its connector (load with ToolSearch if deferred), time zone Africa/Lagos. Ask him only what TickTick can't answer.
> 3. Send one message in the exact shape in step 3 of the skill: headed sections, one item per line, blank lines between sections, plain words, the main tasks for tomorrow listed, questions numbered at the end. Write to him, not to yourself. Then wait.
> 4. Straight after that message, call PushNotification (load with ToolSearch if deferred; `status: "proactive"`) with one line under 200 characters, e.g. "PA: 2 of 3 must-dos done, KD edit missed. Tomorrow's plan is ready. Answer 4 questions."
> 5. Write to TickTick only after he answers. Never Google Calendar. If he settles a new rule, update `standing-rules.md`.
> 6. Close as the skill says (daily notes with the hidden TickTick ID list, log line, commit `personal-life: plan for <YYYY-MM-DD>` ending with `Co-Authored-By: Claude <noreply@anthropic.com>`). Then `git fetch origin main`, `git merge origin/main` (never rebase), `git push origin HEAD:main`. Never force-push. On a merge conflict, stop and tell him.
> 7. Anything that needs the PC (Money sheet, DaVinci Resolve, `01-Inbox/_imports/`) goes as one line in `01-Inbox/`. If he asks for something that needs another agent's judgement (money, a script, an edit), hand it to a subagent on model opus that reads `07-Agents/<agent>/profile.md` and `memory.md`, and relay its answer.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
