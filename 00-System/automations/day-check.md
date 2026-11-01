---
type: sop
area: me
status: active
updated: 2026-11-01
source: interview
tags: [automation, daily, 60-days]
---

# Day check (automation)

**Every day at 9:40pm WAT** a cloud session runs as PA, reads today in TickTick (tasks done and open, habits due), says whether he is on track for [[04-Projects/sixty-days-of-greatness|60 Days of Greatness]], and asks if anything is missing. It doesn't plan tomorrow; he does that himself.

- **Asked for by Samuel, 2026-11-01:** *"Remove the routines cause they don't really help me and I skipped them, just a routine that reads what I have done for the day to check if I am on track and ask me if anything is missing"*. Replaces [[00-System/automations/night-plan|night plan]] and [[00-System/automations/morning-brief|morning brief]].
- **Where:** claude.ai scheduled task "Day check (9:40pm WAT)", id `trig_01NqyP3N2D8Hd1nz5pbA4wpm` (https://claude.ai/code/routines/trig_01NqyP3N2D8Hd1nz5pbA4wpm), cron `CRON_TZ=Africa/Lagos 40 21 * * *`, Default cloud environment, fresh session each run, push notification on. No repo attached: the prompt carries the challenge list itself and writes nothing to the Brain.
- **Needs the TickTick connector**, which an agent can't attach. Samuel adds it in the routine's page (2026-11-01, open-questions).
- **The prompt:** stored in the task. Bedtime habits he ticks last (No Fap, Journal, Social media discipline, Sleep) are reported as "last night" the next day, never asked about. It ticks things only when he says they were done.

Back to [[07-Agents/personal-life/profile|personal-life]] · [[00-System/systems-register|Systems register]]
