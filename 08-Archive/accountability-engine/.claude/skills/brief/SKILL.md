---
name: brief
description: Morning brief — sets the day's commitment from TickTick and context.
---

**Model: Sonnet.** This is a report, not a design session.

Do these in order. Do not skip.

1. READ ONLY THESE. Nothing else in context/ — the brief does not need it and a
   whole-context read costs more than the brief is worth.
   - `context/mission.md` (whole — step 4 needs the levers)
   - `context/patterns.md`, `context/ticktick.md` (small, read whole)
   - `tail -n 8 context/ledger.md`
   Do NOT open memory.md, money.md, decisions.md, stakes.md, ledger-notes/ or the
   five domain files here.
2. Pull today's TickTick tasks, anything overdue, and current habit streaks.
   If the TickTick tools are not available in this session, say so in one line
   and run the brief off context/ alone. Do not guess task state.
2b. Run `python tools/sheets/sheets.py pending`. If anything is queued, run
   `flush` and say in one line what caught up. If it still cannot send, name the
   verdict from `doctor` in one line — an unmirrored ledger that nobody mentions
   is how the sheet quietly stops being true.
3. Report in under 150 words:
   - What's due today
   - What's overdue, and how many times it's been rescheduled
   - Which habit streaks are at risk
4. Name the ONE task that most moves mission.md. Say why in one sentence.
5. If patterns.md shows I've dodged this exact kind of task before, say so and
   cite the ledger date.
6. Ask one question: "What are you committing to today?" Then stop and wait.
6b. SLEEP — ask it HERE, not at the reckoning. One line: "What time did you
   actually get to bed last night?" Samuel's instruction, 2026-08-27 — the 9pm
   reckoning cannot ask about a night that has not happened yet, so the question
   moved to the morning where the answer exists. Take the time, work out the
   hours against the 5:30am wake, and write it into YESTERDAY's ledger row bed
   cell (that row already carries the target he gave at last night's reckoning —
   replace the target with what actually happened). If it is under the 7h floor
   in context/body.md, say the number of hours in one sentence and move on. Do
   not lecture, and do not let it turn into a conversation before the commitment
   question is answered.
7. Ask the second question: "What are the new tasks for today?" Take what I give
   you, create them in TickTick against the project map in context/ticktick.md,
   and read them back with dates. Never invent a due date I didn't state. Never
   create tasks for eating, napping, showering or sleeping, and never schedule
   over breakfast (~12:00pm) or the nap (1:00pm–2:00pm).
8. Append a new row to context/ledger.md with today's date and my commitment under
   Planned. Leave the other columns empty.
8b. Rebuild the site so the dashboard shows today's commitment:

    ```bash
    python tools/site/build.py
    ```

9. Commit and push (see REMOTE.md) — including `site/data/`. If you skip this,
   the row is lost.

Do not offer encouragement. Do not offer to help me plan. Report, name the
priority, take the commitment, stop.
