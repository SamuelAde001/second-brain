# Decisions log (append-only)

What came out of brainstorming in the Claude PA project and what got built from it.
Newest at the bottom. Never rewrite a row — correct it with a new one.

Format:
`YYYY-MM-DD — DECISION: <what was decided> | BUILT: <what Claude Code did, or PENDING>`

---

2026-08-24 — DECISION: split the engine in two — Claude Code operates, the Claude
project on claude.ai brainstorms; both read the same repo. | BUILT: tools/bundle.sh
generates PA.md, PROJECT.md holds the project instructions, this log carries
decisions back.

2026-08-26 — DECISION: engine expands from task/deadline tracking to full
life coverage across five domain files (spiritual, money, audience, body,
people), each carrying a SMART goal, current number, single lever, weekly
minimum, cost of breaking it, and an explicit verification method. Daily
check-in stays under five minutes; domains sweep weekly on rotation rather
than being interrogated daily. Design happens this week, build happens
Sunday 30 Aug — never on top of the live client deadline.
| BUILT: PENDING — full spec being written in the Claude project.

2026-08-26 — DECISION: five-domain expansion BUILT. context/spirit.md, money.md,
audience.md, body.md, people.md created, each with SMART goal, current number,
lever, weekly minimum, cost and verification method. money-ledger.md added for
daily every-naira logging. Domains sweep one per week at the weekly review; the
daily reckoning stays under five minutes. | BUILT: all five domain files plus
money-ledger.md written. CLAUDE.md Files list and Hard rules updated. reckon
gained steps 2d (money) and 2e (sleep) and a five-minute ceiling; reckoning-week
gained steps 8-11 (domain sweep, money week, content block test, concentration);
plan-week rewritten for the one-video target, the course cadence question and the
full anchor list. New skill .claude/skills/month/SKILL.md for the month-end close.
Built 6 days early — 26 Aug, not the planned Sunday 30 Aug.

2026-08-26 — DECISION: content block moves from morning to AFTERNOON (2:00-4:00pm)
at Samuel's instruction, reversing the same-day morning-block design rule. The
objection was stated and overruled. Test condition: if the afternoon block is
eaten by client work twice in one week, it goes back to mornings. The weekly
review states the count every week. | BUILT: all five recurring content-machine
tasks in 📽Content Creation moved to 2:00pm — Thu ideation 2-3pm, Fri script
2-4pm, Sat film 2-5pm, Mon edit 2-5pm, Tue finish/bank 2-4pm. Dates untouched,
time-of-day only. Wed PUBLISH left at 6:45-7:00pm. Saturday and Monday are 3h
against a 2h window and take the first hour of client block 2 — written into
audience.md and body.md, not hidden. The three one-off CONTENT #1 tasks (31 Aug,
1 Sep, 2 Sep) carry real dates and were NOT moved — asked instead.

2026-08-26 — DECISION: Called to Edit ships GRADUALLY by module, not as one launch.
37 lessons, 2 recorded, 35 remaining at ~70 min each. Cadence 2 lessons/week
(~2.5h). Module 1 (11 remaining lessons through LIVE EDIT 01) beta-launches
mid-October; full course completes early January 2027 at that cadence. The
original full-course-by-October plan was rejected as arithmetically identical to
the 25 Aug death march. | BUILT: 11 Module 1 lesson tasks plus a "Module 1 beta
launch" task created in Course recording, all UNDATED — dates blocked until
Samuel names the course block day. Module table and the 41-hour arithmetic
written into context/audience.md. 16 Oct launch date proposed, not confirmed.

2026-08-26 — DECISION: gym 3×/week, 7:00-8:20am (gate opens 7am), floor of 2,
from 1 Sep. Costs ~1.5h of client morning per gym day, ~4.5h/week, accepted
knowingly. | BUILT: TickTick habit "Gym" created (id 6a8eec9b8f0800ee1524083a),
weekly Mon/Wed/Fri, targetStartDate 20260901. Recurring task "💪 Gym — 7:00-8:20am"
created in 💓health, Mon/Wed/Fri, first occurrence Wed 2 Sep. The Sleep habit was
NOT created — Samuel has not given his sleep floor. Not invented.

2026-08-26 — DECISION: money accountability is now daily. Bank balance screenshot
plus a spoken spend list at every reckoning, written to context/money-ledger.md.
Savings are untouchable outside three named emergencies; any withdrawal is logged
same-day with his reason. Trigger: ₦900,250 was booked to Savings/Emergency across
June-August and none of it survives; the August building payment dropped from
₦500k to ₦200k as a result. | BUILT: money.md and money-ledger.md written, reckon
step 2d added, month skill created. CORRECTION TO THIS DECISION, from Samuel the
same day: ₦305,000 of the ₦900,250 DOES survive — it is the Cowrywise investment,
funded at ₦100,000/month. ₦595,250 is what is actually gone. The build used his
numbers, not the spec numbers.

2026-08-26 — DECISION (Samuel, correcting the build spec): the Cowrywise investment
is ring-fenced. Balance is ₦305,000, not ₦400,000. He keeps funding it at
₦100,000/month until the year ends (~₦705,000 by 31 Dec). It does not pay out
until January 2027, when it moves into actual stocks. New savings and the
emergency fund are built OUTSIDE it, and it is never spent on the ₦1M or the ₦3M.
Liquid bank balance at the build: ₦3,503. | BUILT: money.md Rule 7, CLAUDE.md hard
rule, month skill step 5, money-ledger.md note column. The goal arithmetic was
recomputed with the ₦100k/month contribution treated as committed outflow: ₦1M by
31 Dec now closes with ₦70k-₦210k of margin across four months, not comfortably.
Said once and not re-argued.

2026-08-26 — DECISION: Claude Code becomes the primary interface. Samuel is moving
day-to-day conversation, brainstorming and planning into Claude Code rather than
alternating between two Claudes. The Claude project on claude.ai remains as an
occasional deeper-thinking layer reading the same bundle. | BUILT: CLAUDE.md and
PROJECT.md updated.

2026-08-26 — DECISION: Samuel lives in ABUJA, not Lagos. Engine had it wrong from
the build. | BUILT: CLAUDE.md and PROJECT.md corrected, memory.md appended.
Timezone unchanged (WAT, UTC+1) so no schedule changed.

2026-08-26 — DECISION: Samuel asked for a real budgeting and logging spreadsheet —
income, budget lines logged when they actually pay, and daily expenses — to replace
the old sheets that booked savings that never moved. | BUILT: Money-2026.xlsx on the
Desktop. Six tabs, Aug 2026 - Jul 2027. Verified in Excel, zero formula errors,
wiring tested end to end. Nothing is typed on Budget or Dashboard — Budget reads
actuals from Expenses by SUMIFS, so a budget line cannot claim money moved when no
row exists. Not committed to the repo: binary, changes daily; money-ledger.md stays
the text source of truth and wins any disagreement.

2026-08-26 — DECISION (Batch A): sleep floor is 7 HOURS, bed 10:30pm against the
5:30am wake. Course block is SUNDAY 5:00-7:30pm, two lessons per session, with
Sunday dinner moved. | BUILT: TickTick habit "Sleep by 10:30pm" (6a8ef0058f0804d720eb9be9),
daily from 1 Sep, reminder 10:15pm. Recurring "COURSE — record 2 lessons (2.5h)"
Sundays 5:00-7:30pm from Sun 6 Sep. All 11 Module 1 lessons dated Sun 6/13/20/27 Sep
and 4 Oct (two each) with LIVE EDIT 01 alone on Sun 11 Oct. body.md, habits.md and
audience.md updated. HARD STOP EXCEPTION recorded: 7:30pm is an hour past the 6:30pm
stop, sanctioned Sunday-only and non-client-work; if a weekday block cites it, that
is the rule eroding and it gets called the FIRST time.

2026-08-26 — DECISION (Batch B): the ₦3M for July 2027 is ON TOP of the ₦1M —
₦4,000,000 total. Emergency fund ₦300,000, funded from January 2027 AFTER the ₦1M
closes. Creator visits budgeted at ₦25,000/month. The ₦100,000/month investment
NEVER pauses, even if December is behind. | BUILT: money.md and people.md rewritten
with the new arithmetic; workbook updated with the creator-visit line and a GOAL 2
dashboard block, re-verified zero errors. THE FINDING: the creator-visit line moved
the ₦1M from a close to a coin flip (₦973k-₦1,107k against ₦1,000,000 from a ₦3,503
start), and the ₦3M-on-top needs ₦428,571/month against a ₦243k-₦277k surplus, which
is impossible at the August mix. Conclusion written into money.md and mission.md:
FROM JANUARY THE COURSE MUST CARRY ~₦170,000/MONTH or the July 2027 number does not
happen. Every skipped Sunday course block is a payment missed on that ₦1.2M.

2026-08-26 — DECISION (Batch C): Module 1 beta priced ₦10,000, rising at full launch.
Sold by a link, manual payment and access. Free community gets it free. Launch
CONFIRMED Friday 16 October 2026. | BUILT: TickTick launch task dated 16 Oct
(all-day); audience.md commercials table written. OBJECTION STATED ONCE AND NOT
RE-ARGUED: at ₦10,000, free to the 20 warmest people, fulfilled by hand, this is a
testimonial engine and not revenue — 17 sales/month would be needed to hit ₦170k.
The strategy holds only if testimonials are actually collected, and only if the FULL
COURSE PRICE is set before 16 Oct, since the beta price anchors it. That price is
now the load-bearing open question.

2026-08-26 — DECISION (Batch D): church media team is Sunday only, inside the
service — no schedulable time cost. All THREE daily check-ins stay: 7am / 3pm / 9pm.
| BUILT: spirit.md updated; no change needed to the routines in REMOTE.md.

2026-08-26 — DECISION (Batch E, THE FORFEIT — first real third-party mechanism in
the system): Claude Code generates a visual scorecard at every evening reckoning,
scoring the day. Samuel screenshots it and sends it to his girlfriend. His words:
"she is the best person to keep me accountable." | BUILT: reckon step 7b generates
and publishes the scorecard as an Artifact to the same URL nightly — score, what
shipped, what did not, every habit by name, bed time against the 10:30pm floor, and
the money row, with no softening and UNVERIFIED on anything he did not confirm.
reckoning-week step 6b asks how many days he actually sent it. stakes.md carries the
mechanism and the remaining gap: the card is generated regardless, but the sending
is still his choice, and a week with none sent means it has gone back to
self-policed.

2026-08-26 — DECISION: mission.md and stakes.md drafts APPROVED and applied at
Samuel's word. | BUILT: mission.md gained the income reality, the full course plan
and the IG/TikTok numbers with 5,000 marked AMBITION against the SMART version
(18 unbroken Wednesdays). stakes.md gained the scorecard mechanism and the
savings-rule section. The 2026-08-23 unenforced note was left intact — history, not
rewritten.

2026-08-26 — DECISION: the budget moves to Google Sheets ("My Claude Budget") and
Claude Code writes it directly. Samuel's reason: he does not want to type updates by
hand. | BUILT: the Google Drive connector can read a sheet but cannot write a cell,
and the Sheets API needs a Cloud project, so the bridge is an Apps Script web app
bound to the sheet — one paste, one deploy, generic primitives so it never needs
re-pasting. tools/sheets/{Code.gs, sheets.py, README.md}. Credentials in a gitignored
.env; the committed Code.gs carries a __SHEETS_TOKEN__ placeholder so the secret
never enters git history. Samuel proposed falling back to Excel-in-browser via the
Chrome extension when the first deploy 403'd; REJECTED and explained — browser
automation cannot fire from a cloud routine or his phone, which is the whole of
REMOTE.md. The 403 was one dropdown ("Who has access") set wrong. He fixed it.

2026-08-26 — DECISION: the Budget tab gets a Details tab behind it. Samuel's ask:
"I need to know what actually makes up each budget category." | BUILT: Details is
the only place a plan number is typed; Budget's plan column reads it with SUMIFS,
so a category total can always be broken down. Cancelled items go Active=No and are
never deleted — a subscription that reappears is a pattern, and a deleted row hides
it. Savings block added to Budget per his ask (building/Goal 1, Cowrywise, marriage,
emergency fund, buffer), reading Transfers, so a savings line cannot claim money
that never moved.

2026-08-26 — DECISION (his real numbers, first time the budget has been exact):
subscriptions are ₦73,560 not the ₦51k–84.5k guess — Claude 33,500 / Google 15,000 /
CapCut 14,900 / Rubik's 6,860 / YouTube 1,700 / Spotify 1,600. Then cut, same
session: Rubik's OUT, giving 20k→10k, feeding 50k→30k, transport 30k→20k,
personal/misc 50k→10k. Gym ₦30,000 ADDED from September. Obligations floor is now
**₦951,700**. | BUILT: plan.json, Details tab, money.md obligations table rewritten.
The finding worth keeping: his estimate and his truth differed by ₦5,940 — feeding's
₦150,000 did not become savings, it moved into transport, data, household, gym and
a misc line. Nothing got cheaper.

2026-08-26 — DECISION: the two paydays become the spine of the budget. Every line
item carries Payday A (70%, lands end of previous month, funds 1st–14th) or Payday B
(30%, lands ~14th, funds 15th–end), so expenses can be pushed to the back half when
the front is loaded — his own instinct, now on paper. Girlfriend MOVED to A (she
needs it for household essentials); community admin MOVED to B (he is paid
mid-month). | BUILT: Budget payday block, Details payday column. September proved it
immediately — Payday A came out ₦15,084 over, so giving and feeding moved to B.

2026-08-26 — DECISION: Rule 3 AMENDED and Rule 8 ADDED. Rule 3 was "savings move
first on the day the 70% lands"; Goal 1 now moves on Payday B at Samuel's request
(Payday A is always full), with an exception that any Payday A surplus over ₦50,000
moves the same day rather than sitting loose for a fortnight. Rule 8 creates the
BUFFER: ₦50,000/month to ₦200,000, fed also by underspend and by any 4-video month's
excess, and it — not savings — is where urgencies come from. The lean-month cut
order is decided in advance: personal/misc → creator visits → household to ₦20,000 →
buffer → only then a conversation. | BUILT: money.md rules, Setup tab, Budget lean
ladder. The argument that carried it: at a 2-video month he is ₦141,709 underwater
and the discretionary cuts only free ₦55,000 — with Rule 1 forbidding savings and
Rule 7 forbidding a Cowrywise pause, the buffer is the only legal way to balance
that month.

2026-08-26 — DECISION: Samuel's cuts moved the December verdict from ₦227 of margin
across four months to ₦1,207,667 against the ₦1M — closing at ₦1,007,667 after
₦200,000 goes to the buffer. | BUILT: money.md "Does the ₦1M close?" rewritten.
Worth recording once: this is the first time the arithmetic moved because he changed
behaviour rather than because income moved.

2026-08-26 — FACTS ADDED, not previously in the engine: (a) he has a SON with his
girlfriend, whose money rides inside her allowance — which is why the allowance
varies; September carries +₦50,000 for school. OPEN: termly or one-off? (b) he owes
his SISTER ₦90,000; ₦40,000 goes in September, ₦50,000 is undated ("anytime I am
free with more funds"). money.md's "loans all cleared" was wrong and is corrected.
(c) Route Rise does not pay at weekends — a payday on a Saturday lands Monday night.
Oct 70% slips Sat 31 Oct → Mon 2 Nov and Nov 30% slips Sat 14 Nov → Mon 16 Nov,
making early November the tightest point of the year. | BUILT: people.md, money.md,
Budget payday calendar.

| 2026-08-27 | Samuel (Claude Code) | The budget sheet must be writable from the cloud and the phone, not just this desktop. Two blockers found: `.env` is gitignored so cloud clones have no credentials, and Apps Script is not on the cloud "Trusted" network allowlist (`/exec` also 302s to `script.googleusercontent.com`). Fix is one-time cloud-environment config — Custom network access plus the three `SHEETS_*` variables. Backed by a queue: `--queue` parks undeliverable batches in `context/sheet-queue.jsonl`, `flush` replays them from wherever the bridge is reachable, `doctor` names the broken link. The 2026-08-26 unmirrored row was backfilled. | BUILT |

2026-08-27 — DECISION: cut the engine's running cost without cutting what it does.
Six changes: (1) ledger.md splits into a compact one-row-per-day scoreboard plus
context/ledger-notes/YYYY-MM.md for the narrative; (2) every skill declares the
exact files it reads instead of "read context/", using tail and tools/section.sh;
(3) scorecard.html is generated by tools/scorecard/build.py from a ~30-line
context/scorecard-day.json, never hand-written; (4) PA.md is denied to Read in
this repo — it is a generated duplicate; (5) brief/midday/capture run on Sonnet,
everything else on Opus; (6) one check-in per session, /clear between them.
| BUILT: all six, 2026-08-27. Scorecard verified byte-for-byte identical in
rendered text. All ledger prose preserved verbatim in ledger-notes/2026-08.md.

| 2026-08-27 | Samuel (Claude Code) | Cloud environment "Default" configured — Network access Custom (`script.google.com`, `*.googleusercontent.com`) plus the three `SHEETS_*` variables. VERIFIED from a real cloud session, not from the desktop: `doctor` reached 'My Claude Budget', all 7 tabs read back, no `.env` in the clone, queue empty. The bridge is now live from this machine, the routines and the phone. The old "Connector probe" routine was repurposed into a read-only bridge probe and renamed "Bridge probe (diagnostic — disabled, run by hand)" — fire it manually whenever the bridge is suspect. Known tradeoff, accepted: `SHEETS_TOKEN` lives in a cloud environment variable, which the platform warns is visible to anyone using that environment. Personal account, single user. Never share this environment. | BUILT |

## 2026-08-27 — the sheet now shows the balance, and stops judging an unplanned month — BUILT

Samuel, reading the Budget tab: his ₦1,000 recharge was being measured against a
plan he had not agreed to for a month that had not started. Three things were
true at once and none of them were visible on the tab he was looking at.

Decided and built in the same session:

1. **`WHERE YOU STAND TODAY` block, top of Budget.** The bank figure existed only
   on Dashboard, so Budget could show a ₦1,000 spend against a ₦951,700 plan and
   never say what was in the account. It now shows the balance AND its four
   parts — opening balance, money in, money out, net moved to pots — so the
   number can be checked by eye instead of trusted.

2. **The plan column declares its own start.** `plan_start: "2026-09"` in
   plan.json. Aug 26 is greyed, marked ‡, and excluded from `vs plan`, which now
   spans 11 planned months, not 12. The baseline was set on 26 Aug FOR September;
   comparing August to it invented an overspend that never happened.

3. **August income was NOT back-filled, deliberately.** Samuel asked for it and
   it was the wrong fix — Setup!B5 (₦3,503) is an opening balance dated
   2026-08-26 that already nets out June–August. Adding that income to the Income
   tab would have counted it twice and broken the bank figure. Instead the tab
   says so in plain words. `tracking_start` records the boundary.

Two live Dashboard bugs found while wiring it, both silent, both fixed:

- `Obligations floor / month` read `Budget!$B$18`. After an earlier Budget
  rebuild that cell became Personal / misc, so the Dashboard reported a ₦10,000
  monthly floor against a real ₦951,700. **`Income needed to hit the goal` was
  understated by ~₦940,000 — it reads ₦1,292,970/month, not ₦351,270.** That
  number needs a conversation.
- The pot rows summed Transfers on "Savings" / "Emergency" / "Investment" after
  the pots were renamed to "Goal 1 — house" / "Emergency fund" / "Cowrywise
  investment". The SUMIFS could never match again, so the Dashboard would have
  shown ₦0 saved however much money actually moved — the exact lie Rule 6 exists
  to stop. Buffer added as its own row; it is excluded from SAVED TOWARD THE GOAL
  on purpose, being money meant to be spent.

All of it regenerates from `python tools/sheets/build_budget.py`. Re-runnable —
the Dashboard block is rewritten in place, never inserted, so repeat runs cannot
grow the tab.

## 2026-09-02 — three rule changes, all his, all BUILT

**1. THE 5-DAY CLIENT CAP IS A CONTRACTUAL TERM, NOT AN INTERNAL TARGET.**
His words: *"The decision for the deadline of my clients videos are not to me, but
to Route rise, they insist 5 days max from start."* BUILT: `context/body.md` carries
it as a standing rule — Sunday is not a working day inside the five, MUST-CLOSE /
STRETCH buys slack forward, a go/no-go marker at the end of Day 2 messages the client
while it is still a warning, and revisions displace the stretch and never the
must-close. Client #3 built to it: start Thu 3 Sep, ship Mon 7 Sep, send 12 noon.

**2. TASK NAMES MUST BE READABLE ON A LOCK SCREEN.**
His words: *"use simple names that make it clear what task it is, not weird numbers
that when I see the notification I don't know what it is."* BUILT: rule added to
CLAUDE.md under Hard rules; every task created this session renamed to plain language.
Times, chunk numbers and reasoning move into the task BODY. The title is the
notification and nothing else.

**3. NO MORE NIGHTLY SCORECARD.**
His words: *"Don't generate a report card any more every night, we have the dashboard
now, so to reduce tokens."* BUILT: step 7b of the reckon skill replaced with an
explicit do-not; CLAUDE.md's cost-discipline entry rewritten; the weekly review's
scorecard check replaced with "did anyone else see this week?".

**The cost was stated once and he can overrule it.** The card was the only
accountability mechanism in `context/stakes.md` with a THIRD PARTY in it — he
screenshotted it and sent it to his girlfriend. The dashboard replaces the reporting,
not the witness. A site only he opens is self-policing, which is the exact thing the
card existed to stop, and the site has never successfully deployed (six failed Pages
runs, recorded 28 Aug). If a run of days goes soft, this is a named candidate cause,
not a mystery.

## 2026-09-02 — morning movement, six days a week — BUILT

He asked whether the gym should be daily, and morning or evening.

**Evening refused** — dinner 6:00pm, hard stop 6:30pm, bed 10:30pm; an evening session
puts a training spike two hours from a bedtime he has never hit, and sleep is the wall
the gym itself stands on. **Daily gym refused** — the habit started 1 Sep with ZERO
logged sessions, and daily costs ~10h30/week of client morning against a 5-day cap.

BUILT instead, and his instinct about killing the 6:50am decision was right:
gym Mon/Wed/Fri 7:00–8:20am, **run 30 min + bathe Tue/Thu/Sat 7:00–7:55am** (his call:
*"we would have a run instead of a bike, 30 mins is enough"*), Sunday off. Bathing sits
INSIDE both blocks — his point: *"when I come back from Gym and run, I need to bathe."*
Client block 1 starts 8:30am on gym days, 8:00am on run days.

TickTick: habit `6a984bc38f0842fe13de746c` "Morning movement (gym or run)", 6×/week.
The old Gym habit `6a8eec9b8f0800ee1524083a` ARCHIVED — it double-logged against this
one. The 3× full-session target lives in the Mon/Wed/Fri task, not a second habit.

**Honest price: 7h30/week of client morning, up from 4h30.** Paid on purpose, not
recovered by working past 6:30pm. Escalation to 4×/week is EARNED — two consecutive
weeks of 3 logged sessions first.

## 2026-09-02 — THE SITE IS LIVE. First successful deploy ever. BUILT.

`https://samuelade001.github.io/engine/` is serving the real record. Verified by
`tools/site/published.sh`: local and live content_hash both `0da3999a5a544679`.

**The cause of the six failures, recorded 28 Aug and unexplained until now: the repo's
Pages source was set to "deploy from a branch", not "GitHub Actions."** So
`actions/configure-pages` failed on every run, and the branch source meanwhile served
the repo root — which is why the URL answered 200 with a stale page while
`site/data/os.json` was never at `/data/os.json`. Every session that reported "rebuilt
and pushed" was telling the truth and was still wrong about the only thing that
mattered.

**Fix: `enablement: true` on `actions/configure-pages@v5`** in
`.github/workflows/pages.yml`. It flips the source to GitHub Actions from inside the
workflow, so this cannot silently regress on a settings change.

**The lesson that generalises beyond this repo: a push is not a publish.** Run
`bash tools/site/published.sh` after any session that writes to `context/`. It compares
content hashes with the build clock stripped, so this machine's WAT stamps and the CI
runner's UTC stamps do not produce false mismatches.

## 2026-09-02 — THE SITE MUST ALWAYS BE IN SYNC. Rule set, and three real bugs found proving why.

His words: *"At all times the site must be in sync with everything, let it be a rule,
cause I check the site to know what is going on."*

**The audit found the site quietly lying in several places.** All fixed:

| Was showing | Truth |
|---|---|
| "While fasting" anchor card, 25–31 Aug | The fast was DROPPED 28 Aug. Card replaced with Morning movement. |
| Countdown: Client #2 deadline 30 Aug | Shipped 2 Sep, 2.5 days late. Retired. |
| Countdown: detox/fast decision 31 Aug | Decided 2 Sep. Retired. |
| Countdown: content cadence starts 2 Sep | It did not start. Retired. |
| Goal: "Gym, 3× a week" | Habit archived 2 Sep. Now Morning movement 6×/week. |
| Content: "Next publish — Wed 2 Sep" | Nothing published. Now "Weeks banked 0/18". |
| Content callout: "at risk, needs his call" | Resolved — a confirmed miss, P1 confirmed. |
| Nothing about the 5-day client cap | Added as a goal: deliveries inside the cap, 0 of 3. |
| No countdowns for Client #3, Kaduna, Payday B | All three added. |

**THE ROOT CAUSE, and it is the important part.** `build.py` stamped `?v=` on
`data/os.js` ONLY. Every app script — `app.js`, `charts.js`, `pages/*.js` — was served
with no version, so browsers and the CDN cached them indefinitely. **The numbers
updated and the code that RENDERS them never did.** That is why a dead fasting card
survived a rule change and why the new out-of-sync banner did not appear until the
stamping was widened. Fixed: every local script is now stamped with the build hash.

**TWO NEW MECHANISMS so this cannot rot silently again:**

1. **`build.py` now emits staleness warnings** — ledger behind today, pots older than
   the last ledger row, money ledger behind, countdowns in the past, habit log behind
   or naming habits no longer tracked. They warn, never block: a stale record shown
   with a warning still beats no record.
2. **The dashboard renders those warnings as a red banner at the very top**, before
   anything else on the page can be believed. Verified live 2 Sep — it is currently
   showing four, all genuine.

**The standing rule, now in CLAUDE.md:** every session that writes `context/` ends
with build → commit → push → `published.sh`. A push is not a publish. And when a rule
dies, hunt down the page that draws it — data alone is not enough.

## 2026-09-02 — NOTHING FACT-BEARING IS HARDCODED. Rule set, enforced by the build.

His words: *"Nothing should be hard coded, let it be easily updatable once the data is
updated, so we don't need to code always, it should just be an update to the data and
the frontend reads from the data."*

**This was the real disease; every stale panel today was a symptom.** The work page's
whole client schedule — five days, their labels, their states — was a `const DAYS`
array inside `work.js`. It could not go out of date "by accident"; it could only ever
be right on the day it was typed. Same for the spirit page's church card.

BUILT:

- **`work` block in `context/site.json`** — the cap, the job in flight with its five
  days and each day's must-close, and a history of every delivery. `work.js` now
  renders whatever is there. Client #3 appears without a line of code being written.
- **`spirit` block in `context/site.json`** — next church date, status, and why the
  last one was missed. The hardcoded "Church, 30 Aug — OFF" card is gone.
- **Two build guards.** One warns when the current job is past its due date or has
  every day marked done. One scans every page script for a PAST date hardcoded inside
  a `statCard(...)` and names the file and line. Prose may cite a past date — a status
  card may not, because a status card claims to describe right now.

**Also found and fixed while auditing, and it is the worst bug so far:** the site
reported **average sleep 8h 45m**. The parser read the ledger cell `1:42am (19h day)`
and took "19h" — the length of the WORKING day — as nineteen hours of sleep. The real
average across recorded nights is **5h 20m**, under the 7-hour floor every single
night. A comforting number, confidently wrong, on the one page about the thing every
other rule stands on. `parse_bed_cell` now rejects a parenthetical qualified by
"day"/"span"/"awake"/"work" and warns on any value outside 0–14h.

**REMAINING DEBT, named so it is not forgotten.** The narrative callouts on money,
course, content, people and systems still quote figures inline. They are not status
cards so they do not go stale silently in the same way, but the same rule applies:
when one of those numbers changes in `context/`, the prose must follow. Moving those
into a `notes` block in `site.json` is the next step and has not been done.

## 2026-09-02 — the prose moved out of the code. 44 callouts now live in site.json.

Finishing the rule set earlier the same day: *"Nothing should be hard coded... it
should just be an update to the data and the frontend reads from the data."*

**Every static callout and chart note on the site is now a data entry.** They live in
`context/site.json` under `notes`, keyed by page and id, and the page scripts call
`notesFor('<page>', '<id>')`. Rewriting a sentence — a figure that moved, a rule that
died — is a data edit. No JavaScript is touched.

- **44 moved** across all 11 pages.
- **7 left in code deliberately.** Those interpolate live values — the out-of-sync
  banner counts its own warnings, the budget page prints `plan_start` and computed
  shortfalls, the work page prints the cap note. They are templates over data, not
  hardcoded facts, and moving them would break them.
- Migration tool kept at `tools/site/extract_notes.py`, re-runnable.

**Three build guards now protect this**, on top of the staleness and hardcoded-date
checks added earlier:

1. A `notesFor()` call whose id is missing from `site.json` → warned, and the page
   renders a visible `[missing note …]` marker rather than silently nothing.
2. A note in `site.json` that no page renders → warned. This one exists because it
   already happened: testing another guard, a `git checkout` of `work.js` reverted it
   to the pre-migration index and silently undid its migration. The data survived, the
   call site did not, and nothing would have said so.
3. Icons are stored as real characters, not `\uXXXX` escapes. The first migration
   pass stored the escape text and would have printed `\u{1F6A9}` on the page.

**How to change any sentence on the site now:** find it in `context/site.json` under
`notes.<page>.<id>`, edit it, run `python tools/site/build.py`, commit, push, then
`bash tools/site/published.sh`. That is the whole loop.

## 2026-09-02 — September replanned on confirmed money. Parents cancelled, CapCut cut, the front half funded. BUILT.

Payday A landed and was verified in the bank the same hour: **$706.66 net, ₦962,228,
bank ₦962,371** — reconciling exactly to ₦143 + ₦962,228. Everything below was decided
against money that exists, not against a projection.

**Two things the record had structurally wrong, both found by checking plan against
the actual payment:**

1. **Income was booked GROSS.** There is a **flat $5 charge per payment**, twice a
   month — confirmed to the cent, $711.66 invoiced against $706.66 received — and the
   measured rate is ₦1,361.66/$, not the ₦1,365 average being assumed. Together those
   overstated every month by **₦17,016**. `build.py` now nets the charge out of the
   balance block, and every payday figure on the site is net.
2. **The front half of the month was never funded.** Feeding, transport, household and
   personal/misc all sat on Payday B, leaving 1–14 September with **₦871**. That had
   already cost something real and it is in the ledger: **church missed on 30 August
   for want of ₦5,000.** Each of those lines is now split — front-half share on Payday
   A, remainder on B. Same monthly totals, **₦27,771 of actual cushion.** The failure
   was the timing of the budget, not the size of it.

**Samuel's decisions, all his own:**

| Decision | Effect |
|---|---|
| **Parents cancelled for September** — he spoke to his dad and his dad agreed | −₦100,000, September only. The lever that turned the month from ₦41,973 underwater into ₦58,027 free. |
| **CapCut cancelled outright** — he edits on DaVinci Resolve | −₦14,900/month, ₦44,700 by December, ₦178,800/year. Obligations floor ₦951,700 → **₦936,800**. |
| Girlfriend ₦100,000 → ₦50,000; son's school ₦50,000 → ₦100,000 | Net zero. ₦150,000 either way; only the split moved. School due before the 14th, so it stays on Payday A. |
| Kaduna ₦50,000 → ₦80,000 | Still a guess. Any overrun comes from the Buffer, never Goal 1. |
| Gym clothing ₦10,000 added | Buys the 6×/week movement habit. |
| **Goal 1 account created, on Cowrywise** | Closes an open question that had a 14 September deadline on it. |

**Declined, and he agreed: ₦40,000 out of Cowrywise.** He offered it to build a
cushion. Rule 7 is his own, closed in writing on 26 August with *"it never pauses"* —
and once the parents payment came off, the cushion existed anyway. **It would have
broken the hardest rule in the file to solve a problem a better decision had already
solved.** Worth recording because the temptation was reasonable and the answer was
still no.

**The Goal 1 account creates a second name clash.** Cowrywise now holds the ₦305,000
ring-fenced investment AND the ₦1M house money — two pots that mean opposite things,
showing as one balance. The Buffer already shares the "Emergency" account with the
future emergency fund. So the Budget page's pots callout was rewritten to **derive
clashes from the data** instead of asserting one hardcoded case; it now catches both,
and will catch the next one without a code change. Two questions still open: is the
Goal 1 plan separate from the investment, and does its lock expire before 31 Dec.

**New: `context/things-to-buy.md`,** a buy-now list and a wish list, rendered on the
Budget page and mirrored to TickTick as two checklists he ticks and adds to.
The finding that justified it: **his ₦68,000 shopping list was ₦48,000 already
funded.** The food came to exactly ₦30,000 — the Feeding line to the naira. Only
₦20,000 was new, and ₦10,000 of that (snacks, his words *"not essential"*) was left
unallocated inside the cushion rather than budgeted.

**A real bug in the sheets bridge, found because the Budget tab would not move.**
`append` used Apps Script's `getLastRow()`, which counts formatting and footer text,
so two payday rows landed at Income 125 and Expenses 405 — **outside the SUMIF windows
the Budget tab reads** (`Income!$I$5:$I$124`, `Expenses!$E$5:$E$404`). The rows were
on the tabs and invisible to every total, and the bank figure sat on a stale ₦2,503.
**This is Rule 6 running backwards** — not a plan claiming money that never moved, but
money that moved and no total able to see it — and it would have repeated silently at
every reckoning. `sheets.py append` now finds the last row with a date in column A,
passes it as `after`, and warns loudly if a batch still lands past the readable range.

**De-hardcoded in the same pass,** per the 2026-09-02 rule: the two-payday amounts, the
₦146,041 Goal 1 line, the obligations floor in `money.js`, and the bank card's
subtitle *"everything he can spend today"* — which on a payday is the most misleading
sentence on the site, since ₦934,600 of that balance was already committed. The payday
table now subtracts the pots and calls the result a **cushion**, not free.


---

## 2026-09-02 — evening reckoning. BUILT.

**The append fix from this afternoon only covered one code path, and tonight's
reckoning drove straight through the other one.** `sheets.py append` was taught to
anchor on the last dated row in column A. The reckoning does not use that verb — the
reckon skill mirrors money with `ops payload.json --queue`, which went to the raw
Apps Script `append` and `getLastRow()` all over again. Four Payday A expense rows
landed at **Expenses 405–408** and the Cowrywise transfer at **Transfers 125**, both
outside the windows the Budget tab sums. Same bug, same night, second path — caught
only because the rows were read back after writing.

**Fixed at the chokepoint instead of at the caller.** `_anchor_appends()` and
`_warn_out_of_range()` now run inside `send()`, which every path goes through: `ops`,
`append`, and `flush`. Appends to the same tab in one batch stack rather than collide.
The duplicated logic in the `append` verb is deleted — one implementation, not two.
`READABLE_TO` is a module constant so the caps live next to the code that enforces them.

**The lesson, and it is the general one:** a fix applied at the call site is a fix for
the call site. The bug was in what `send()` let through, so that is where the guard
belongs. The verification step is what actually caught it — the rows were written,
the tool reported success, and the sheet was still wrong. **Reading back after a
write is not paranoia; it is the only thing that distinguishes "sent" from "landed."**

Stray rows cleared, batch re-sent, and the sheet's bank figure now reads **₦211,787**,
matching `context/money-ledger.md` to the naira.

**Also recorded tonight:** Goal 1's account is picked (Cowrywise, opened at the budget
session) — `plan.json`'s "NO ACCOUNT YET" note was stale and is corrected. It carries
the warning that this is now the SECOND name clash on the sheet: Goal 1 and the
ring-fenced investment share a platform, and Rule 7 says the investment never counts
toward the ₦1M.

## 2026-09-15 — Routines deleted, two-touch structure, new day shape — BUILT

- Cloud routines deleted by Samuel. Replaced by two self-started touches: a 9:00–9:30pm
  planning session (reckon + tomorrow's tasks) and the Sunday week plan. No brief, no
  midday. CLAUDE.md, REMOTE.md updated. — BUILT
- New day shape from 16 Sep (context/body.md). Hard stop 6:30pm → 9:00pm, prayer
  45 → 30 min at 6:15am, gym to 5:00pm. Site rule lists moved into data. — BUILT
- Client videos named by month: "Sep #3 — Alex". — BUILT
