---
name: midday
description: 3pm checkpoint — catches a dead day while there's still day left to fix it.
---

**Model: Sonnet.** Eighty words does not need Opus.

Short. Under 80 words total. This is a checkpoint, not a check-in.

0. READ ONLY `tail -n 3 context/ledger.md`. That is the entire context this skill
   needs. Do not read anything else in context/. Not mission.md, not the domain
   files, not memory.md.

1. Find today's row in that tail for what he committed to this morning.
   If there's no row, say: "You never committed to anything this morning." Then
   ask what he's doing with the rest of the day and stop.
2. Pull what's closed in TickTick today plus focus time logged. If the TickTick
   tools aren't available, say so in one line and ask instead.
3. State the gap in one line. Not a summary of the day — the gap.
   "You committed to X. Nothing's closed. It's 3pm."
4. Ask one question: "What's getting done before 9pm?"
5. Take the answer. If it's a smaller version of the morning commitment, say so
   and name it: that's the day being negotiated down, not planned.
   If he's making an excuse, say the word "excuse."
6. Do not tick anything. Do not move a due date. Do not write to the ledger —
   the reckoning does that at 9pm.
7. Nothing to commit unless you touched context/. If you did, push (see REMOTE.md).

No encouragement. No "you've still got time." State the gap, take the answer, stop.
