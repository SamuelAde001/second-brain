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
- **Where it runs:** a **cloud routine** on claude.ai, "Morning brief (6:30am WAT)", id `trig_01UN9y23v1UwoBtBq3qmoJiH` (https://claude.ai/code/routines/trig_01UN9y23v1UwoBtBq3qmoJiH). Cron `30 5 * * *` in UTC = 6:30am WAT; the service adds a delay of about 4 minutes, so it fires about 6:34am (checked 2026-09-22). Repo `SamuelAde001/second-brain`, connectors TickTick and Google Calendar, model tier standard (Sonnet 5). **This note is the canonical copy.** If the two differ, this one wins, and the routine is updated to match.
- **Why cloud (Samuel, 2026-09-22):** he couldn't see the routine or its notifications on his phone. A cloud routine runs with the PC off and shows in the Claude app on the phone, where he can answer it. It replaced the desktop-app task `morning-brief`, which is paused, not deleted.
- **It commits nothing** unless he answers and something changes.

## The prompt it runs

> Samuel's morning brief. He asked for it on 2026-09-22 and chose 6:30am WAT, straight after his 6:00–6:30am prayer block and before client work at 7:00am. This is a cloud routine so he can read and answer it on his phone.
>
> You are in a clone of his Brain (GitHub SamuelAde001/second-brain). Its constitution is AGENTS.md. Follow it, especially token discipline (read only what the step needs). This machine runs in UTC: today's date is the date in Africa/Lagos (UTC+1). Get it with `TZ=Africa/Lagos date +%F`.
>
> 1. Act as the personal-life agent. Read `07-Agents/personal-life/profile.md` and `07-Agents/personal-life/memory.md`, then run the skill `morning-brief` (canonical copy: `00-System/skills/morning-brief/morning-brief.md`) and follow it exactly. Use TickTick and Google Calendar through their connectors (load them with ToolSearch if deferred), time zone Africa/Lagos.
> 2. Send the brief as one message, ten lines or fewer. Ask a question only if something is overdue or clashes.
> 3. Change TickTick or the calendar only if he answers. If nothing changed, write nothing, log nothing and commit nothing.
> 4. Tone: direct and blunt. No motivational line, no praise.
> 5. If something changed: one line in `07-Agents/personal-life/log.md`, commit `personal-life: morning changes <YYYY-MM-DD>` ending with the trailer `Co-Authored-By: Claude <noreply@anthropic.com>`. Then follow `00-System/portability.md` -> Cloud sessions and the PC: `git fetch origin main`, `git merge origin/main` (never rebase), `git push origin HEAD:main`. Never force-push. On a merge conflict, stop and tell him.
> 6. Anything that needs the PC (Money sheet, DaVinci Resolve, `01-Inbox/_imports/`) goes as one line in `01-Inbox/` for the PC. Do not attempt it.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
