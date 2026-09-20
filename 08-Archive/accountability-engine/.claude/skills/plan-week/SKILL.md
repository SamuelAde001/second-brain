---
name: plan-week
description: Weekly planning — takes Samuel's week from him and lays it into TickTick around his fixed anchors.
---

Run this on Sunday, or whenever Samuel asks to plan the week. Works the same on
desktop or from his phone.

1. READ LIST — these and no more:
   - `context/mission.md`, `context/patterns.md`, `context/habits.md`,
     `context/ticktick.md` (whole; all small except mission)
   - `bash tools/section.sh context/body.md "Daily anchors" "The default day shape" "How editing work is chunked"`
   - `bash tools/section.sh context/audience.md "Weekly minimum" "The one lever"`
   - `tail -n 9 context/ledger.md`
   Not stakes.md, not money.md, not memory.md, not decisions.md, not the notes files.
2. Pull what's already in TickTick for the coming 7 days, plus anything overdue.
   If the TickTick tools are not available in this session, say so in one line and
   work from what Samuel tells you. Do not invent task state.
3. Report in under 150 words: what's already committed for the week, what's carried
   over, and how many times each carried-over item has been rescheduled.
4. Ask him, in this order, one question at a time. Wait for each answer:
   - "What client deadlines land this week, and what date is each stated for?"
   - "Is the Wednesday video banked by Tuesday night?" — the target is ONE video,
     published Wednesday 7:00pm. Publish day contains zero production. If he cannot
     say yes, find the block now, not on Wednesday.
   - "Which two lessons are you recording this week?" — course cadence is 2 lessons
     a week and it does not survive unless it is named on Sunday. Take the two
     lesson titles, not "some course work."
   - "What are you protecting course time with?" — the course loses to client work
     every time. If he gives no block, say that plainly.
5. Lay it out against the fixed anchors. Never schedule work over them. Never create
   tasks for eating, napping, showering or sleeping.
   - 5:30-6:15am  prayer + Bible study (45 min, combined)
   - 7:00-8:20am  gym on gym days (gate opens 7:00am; costs ~1.5h of client morning)
   - 12:00pm      breakfast
   - 1:00pm       nap (~1 hour)
   - 2:00-4:00pm  content or course block
   - 6:00pm       dinner
   - 6:30pm       HARD STOP — no evening work blocks
   - Sunday 7:30am-3:00pm is church and commute. Sunday is not a work buffer;
     plan it from 3:00pm.
   - While a fast is running, check context/habits.md for the replacement anchors
     (3:00pm first meal, 4:00pm nap) before laying anything out.
6. Create the tasks in TickTick with the dates he stated. Use the project ids in
   context/ticktick.md. Never invent a due date he didn't say. Never move an
   existing due date — if something needs to move, ask first.
7. Read the plan back as a one-line-per-day list. Ask: "Is that the week?"
8. When he confirms, append one line to context/memory.md dated today, recording
   what he committed the week to.
9. Commit and push (see REMOTE.md). If you skip this, the plan is lost.

Do not offer encouragement. Do not congratulate him for planning — planning is not
shipping. Take the week, write it down, stop.
