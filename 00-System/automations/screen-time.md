---
type: sop
area: me
status: active
updated: 2026-09-28
source: interview
tags: [automation, screen-time, social-media, stayfree]
---

# Screen time (automation)

**Every day at 8:30pm WAT** the PC writes today's StayFree screen time into the Brain and pushes it to GitHub, so the 8:45pm [[00-System/automations/night-plan|night plan]] (a cloud routine that can't see the PC) can check the commitment *social media only while eating* ([[06-Logs/commitments|commitments]], 2026-09-28).

- **Asked for by Samuel, 2026-09-28:** asked whether the PA could read his StayFree usage *"to help keep me accountable"*, then *"yes build it"*. **No tokens:** it's a plain Python script, not an AI session.
- **What runs:** `pythonw 00-System/scripts/screen_time.py --write --push --refresh`, from Windows Task Scheduler, task **"Brain - screen time"**, daily 8:30pm, runs late if the PC was asleep. Registered 2026-09-28. Started through the Windows Store alias `%LOCALAPPDATA%\Microsoft\WindowsApps\pythonw.exe`.
- **What it reads (read-only, outside the Brain, AGENTS.md §10):** StayFree's Windows app data, `%LOCALAPPDATA%\Packages\37081StayFreeApps.StayFree3_fqhk48m1tsma0\LocalCache\Roaming\StayFree\` — `usage.db` (this PC's apps) and `config.db` (a cache of sessions synced from the phone and the Chrome extension). Both are copied to a temp folder and read there. Only session rows are read.
- **What it writes:** `06-Logs/screen-time/<today>.md` and yesterday's again (now complete, so last night's 11pm–midnight is in), one line in `06-Logs/automation/screen-time-runs.md`, then commits only those files and pushes (pull, merge, push; never force).
- **Phone data depends on the StayFree app being open on the PC.** It pulls phone sessions on its own while running (seen 2026-09-28: 08:37 → 10:09 with no action). If phone data is over 2 hours old, the script opens StayFree, waits 90 seconds, and reads again. If it's still stale, the file says so and the night plan asks for a screenshot.
- **PC off at 8:30pm:** no file. The night plan says so and asks for a StayFree screenshot. Never a miss on missing data.
- **Manage it:** Task Scheduler → "Brain - screen time". Run by hand: `python 00-System/scripts/screen_time.py` prints today without writing.

Back to [[02-Me/daily-routine|daily routine]]
