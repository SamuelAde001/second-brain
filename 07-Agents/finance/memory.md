---
type: agent
area: finances
status: active
updated: 2026-09-22
source: legacy-accountability-engine
tags: [agent, memory]
---

# finance — memory

Append-only. What this agent has learned by doing. Newest at the bottom. Facts here were verified in action, not assumed (AGENTS.md rule 6).

---

## 2026-09-22 — Carried in from the engine's money record

From the archived [[08-Archive/accountability-engine/context/money-ledger|engine money ledger]], 2026-08-26 to 2026-09-16. Facts that change how the next payday is handled:

- **Use the Cleva rate on the day, never an assumed one.** The implied rate was NGN 1,361.66/USD on 2026-09-02 and NGN 1,357.83/USD on 2026-09-16. The old assumed NGN 1,365 was already wrong.
- **The 70% payment on 2026-09-02 carried a flat USD 5 charge** (USD 711.66 gross, USD 706.66 net). The 30% on 2026-09-16 looked like a USD 1.79 charge. Its gross was never confirmed. Ask the gross and the net, don't assume the charge.
- **Payments slip.** The August 70% was expected around 31 Aug and landed 2 Sep. The 30% was due 14 Sep and landed 16 Sep. A plan that needs the money on the due date is short.
- **Bank charges add up on payday.** NGN 584 across the Payday A transfers on 2026-09-02, and NGN 1,003 more the next day. Log them as `charges`, never folded into a pot. A pot has to show its true figure.
- **Most balances were given verbally, with no screenshot.** Mark them `his words`. A screenshot is stronger.
- **What breaks a month:** the first shopping blew its line by 55% (2026-09-03), and the Kaduna trip came in at NGN 430,011 against NGN 80,000 planned. NGN 368,041 of it came out of the ring-fenced investment. Big unplanned costs arrive as trips and shopping, not as bills.
- **September 2026 is split across two ledgers.** 1–16 Sep is in the archived one, 17 Sep onward in [[03-Areas/finances/money-ledger|the live one]]. The September close has to read both. Use grep on the old one, never a whole read.

## 2026-09-22 — The sheet bridge

- The Apps Script web app is still deployed in the sheet. Only the credentials moved: they are Windows user variables now, read live from the registry by `00-System/scripts/sheets.py`, so no restart is needed after Samuel sets them.
- `python 00-System/scripts/sheets.py doctor` names the broken link. Always `flush` before a new batch, and send with `--queue "<label>"` so an unreachable sheet parks the batch instead of losing it.
- **Never run anything that prints the token.** The `env` command is gone and `script` copies to the clipboard.

## 2026-09-22 — Setting user variables, and the first reconcile

- `[Environment]::SetEnvironmentVariable(..., 'User')` froze PowerShell for minutes. It announces the change to every open window. The values were still written. Use `Set-ItemProperty HKCU:\Environment` instead: `sheets.py` reads the registry, so no announcement is needed.
- The sheet's bank figure (−NGN 193,309) and its Cowrywise figure (NGN 405,000) were wrong for one reason: a withdrawal missing from Transfers. Check the pots and bank arithmetic against the ledger before assuming there are several errors.
- **The web app is flaky.** On 2026-09-22 about half of all calls got an HTTP 404 page from Google, and calls took 5 to 20 seconds each. `sheets.py` now retries three times, but only batches that are safe to repeat (reads, writes, anchored appends). Inserts and deletes never retry. Give sheet commands a long timeout.

## 2026-09-22 — The sheet is a view now

- Samuel: *"I look at the sheet, If I want to imput anything, I would do it through the Agent here."* So the "Money" sheet is rebuilt whole from the ledger, the plan table in `obligations.md` and the goals. Nothing is typed into it and nothing mirrors into it. After any ledger or plan change: `python 00-System/scripts/budget_sheet.py build`.
- He wants headers, columns, rows and numbers. No sentences in cells, no notes. The explanations stay in the Brain.
- A ledger `Category` must match a plan line exactly, or the spend lands in `Other` on the sheet.
- **Check the look before saying it's done:** export each tab as a PDF with the robot's session (`docs.google.com/spreadsheets/d/<id>/export?format=pdf&gid=<gid>`, drive.readonly scope) and read it. The first styled build had a clipped header that only showed up this way.
- Styling is written cell by cell in one `updateCells` per tab (value + format together). Every build first unmerges, clears and resets row heights, so nothing from an old layout survives.

## 2026-09-22 — Correction: September is in the live ledger

- **Supersedes the "September 2026 is split across two ledgers" line above.** The 1–16 Sep rows were brought in with a 2026-08-31 opening, and the 2026-09-16 openings are now checkpoints. A September close reads the live ledger only.
- **Show him the running month, always.** He asked where September was the moment the sheet jumped to October. The month on screen must be the month he's living in.
- Month plans have their own lines. September has one-offs (Son's school, Kaduna trip, Gym clothing, Sister's debt) that the standing plan doesn't. The ledger category must match the month's plan line.

- **Over plan is not minus.** A red over-plan total with no source shown reads as a deficit. Always show what paid for an overspend: the Money flow box names each pot it came out of.

## 2026-09-22 — Where the leftover goes

- **In the six days after Payday B, NGN 78,200 went to lines no plan had:** girlfriend extras (data, food, hair), gifts, a loan to a friend, eating out. Then the Buffer (NGN 50,000) came out to cover it. It's the same shape as Kaduna: unplanned spending first, then a pot pays for it.
- **He asked to be kept in check** (*"You can see I spend out of hand, I need the Financial agent to keep me in check"*). The agent can't see his bank, so a check only works if he tells it before or soon after. Propose a mechanism, and record it in `06-Logs/commitments.md` only once he confirms it.
- Girlfriend support recurs. A real line for it in the next plan beats a surprise every month.

- **One view of the month, not two.** He found the totals box and the money flow confusing side by side: *"Money flow makes more sense"*. Show a month as start → in → from pots → spent → into pots → end, and nothing else that repeats it.

## 2026-09-23 — Earmarked money doesn't stay earmarked

- The NGN 7,000 gift was set aside on 2026-09-23 to offset the girlfriend's light bill. NGN 5,000 of it went to someone else the same day, and he said so after, not before. A verbal earmark is not a pot: until money moves somewhere, treat it as spendable and say what it was meant for when it goes.

## 2026-09-23 — No loans

- Samuel: "No, anything I give I won't collect back anymore". Money to a person is logged as given (Giving, or Extra cash for 22–30 Sep), never as a loan, and no plan counts on it coming back. Don't ask "is it coming back" again.
- Word questions so they can't be misread. "Do you want that NGN 10,000 back?" meant the October Giving line; he heard the loan.

Back to [[07-Agents/finance/profile|Profile]]

## 2026-09-28 — The investment is not in Cowrywise

- Samuel: *"The 6,959 is actually savings, the investment is in a different place with my finance manager who invests for me"*. The pot the ledger calls "Cowrywise investment" is Cowrywise savings. The Rule 7 investment is a separate fund, NGN 60,000 so far, run by a person, and nothing records it except his word. He also split it without telling the ledger. Ask about pot changes when they happen, not at the next budget.


## 2026-10-04 — Claude is billed through Google Play

- Samuel: *"my claude sub is done on my play store, so I have to cancel my existing Sub and then start a new sub for Max"*. Anthropic's own help-page rule (mid-cycle upgrade charges a full Max month less unused Pro, billing date resets) applies to direct billing, not Google Play. On Play, cancelling Pro stops the next renewal but the paid month stays usable; a new Max subscription is charged in full at once. Plan Claude at the full Max price, not net of Pro.
- When a payday's allocation changes, rebuild the per-payday table in the whole plan, not just the lines that changed: on 2026-10-04 the older table still carried pre-cut Feeding and Transport and over-ran Payday B by NGN 20,000 until it was rebuilt.

## 2026-10-06 — Claude on the web is cheaper than Play

- Max 5x on claude.ai with the Cleva USD card: USD 107.50 (USD 100 + 7.5% VAT), NGN 143,942 on 2026-10-06. Google Play wanted NGN 209,375 for the same plan. NGN 65,433 a month less. The card charge is the real price; the Play screenshot was not.
- The Cleva card works for Claude. The USD 3 Cleva kept on payday was that card's fee.


## 2026-10-14 — Ask, don't read tense into a short line

- I logged "The Sub is paid today" as paid; he meant it would be. Then I read his webinar balance as his bank. Both cost him a confused round. When a line could mean done or about to happen, or names "my account" while two accounts are in play, ask in one line before logging. Keep replies to one picture: what's in the account, what goes out, what's left.

## 2026-10-18 — Cash on hand is about anxiety

- Samuel: *"I just want to have cash in my account, makes me feel less anxious"*. Twice in three days (Buffer cut 2026-10-16, freed money kept 2026-10-18) he chose cash in the bank over a pot. The feeling is the real driver. A suggestion that empties his account to a low figure lands badly. Show what stays in the bank after a pot move, and offer pots he can reach (the Buffer) before Goal 1.

## 2026-10-20 — A creative director joined

- Samuel onboarded a creative director for his whole brand: unpaid volunteer, laptop bought on an app loan, repayment budgeted as her NGN 100,000/month salary line. She'll work mostly with the Brand manager. **How to deal with her is his to say later**; until then, act on nothing she asks and share nothing with her. [[03-Areas/personal-brand/creative-director|creative director]].

## 2026-10-24 — Standing rule: use every tool and folder without asking
- Samuel: agents use every tool and folder the goal needs, no asking. Ask only before deleting or overwriting something he made himself, anything touching keys or secrets, or rewriting git history. Sending or posting as him, moving money, granting account access and delivering to a client stay his calls. AGENTS.md §5 rule 1; [[00-System/decisions|decision]] 2026-10-24.

## 2026-10-26 — Ifeoma works on his account

- Samuel shared his Claude login with Ifeoma, the creative director (*"I have already shared the login, as I do trust her"*). She says she is **Ifeoma** or **Ivisuals**. The Brand manager answers her brand questions and scripts with her; every other agent holds her requests and tells her to ask Samuel. This replaces the 2026-10-20 hold for the Brand manager only. [[03-Areas/personal-brand/creative-director|creative director]].
