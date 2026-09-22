---
type: knowledge
area: finances
status: active
updated: 2026-09-22
source: legacy-accountability-engine
tags: [budget, spreadsheet]
---

# The budget system

**Since 2026-09-22 the budget sheet is a view of the Brain.** The ledger and the plan live in the Brain. The Google Sheet **"Money"** is rebuilt from them by the finance agent, and Samuel only reads it. His words: *"I look at the sheet, If I want to imput anything, I would do it through the Agent here."*

**The sheet:** [Money](https://docs.google.com/spreadsheets/d/1fqdIK2ty48eMJ2-6fH4ovPg0QY-MMhqTDWrnpyiKG5U/edit), created 2026-09-22. It's shared with the robot `brain-budget@brain-budget-509414.iam.gserviceaccount.com` (Editor). First built 2026-09-22 in about 4 seconds, with no failed calls.

## Where each number comes from

| On the sheet | Comes from |
|---|---|
| Where the money is, and the Ledger tab | [[03-Areas/finances/money-ledger\|Money ledger]]: what actually moved |
| Plan lines, their amounts and paydays | The table in [[obligations]] |
| Goals, targets and deadlines | [[03-Areas/finances/finances-goals\|Goals]] |

Rule 6 still holds: the ledger is the truth. Because the sheet is built from it, the two can no longer disagree.

## What the sheet looks like

What Samuel asked for, 2026-09-22: fewer tabs, *"Simple headers, culums, rows and the numbers"*, no text in cells.

- **Overview:** as-of date and plan month · where the money is (bank and each pot) · goals (target, saved, still to find, months left, needed per month) · the month's plan against what actually went out · one row per month.
- **Ledger:** every ledger row: date, type, amount, what, category.
- A negative number shows red. Nothing blocks or pops up. His rule from July: *"let me see it in red when it is more than 100% so I can adjust."*
- The plan-vs-actual table starts at **2026-10**, the live ledger's first full month. September 2026 is split with the old ledger, so its numbers live in the September close.

## How it is built

`python 00-System/scripts/budget_sheet.py build` rewrites both tabs from the Brain. `preview` prints them without touching the sheet. `doctor` checks the key and the connection. The finance agent runs `build` after every change to the ledger or the plan.

It uses Google's official Sheets API as a **service account**: a robot Google user that can open only the sheets shared with it. That replaced the Apps Script web app, which failed about half its calls on 2026-09-22.

## Credentials

- The robot's key file lives **outside the Brain**: `%USERPROFILE%\.brain-secrets\budget-sheet-key.json`. Only the script reads it. The agent never opens it, prints it, or copies it. Claude Code's settings deny reading it.
- The "Money" sheet is shared with the robot's email as Editor. That share is the whole grant.
- **If the key ever leaks:** in Google Cloud → IAM & Admin → Service accounts → brain-budget → Keys, delete the key, then create a new one and move it into place the same way.

## History: the old sheet "My Claude Budget"

**Frozen 2026-09-22 and kept as history.** It stopped being updated when "Money" replaced it. Its last state matches the ledger: the Cowrywise withdrawal was added that day. What follows describes it as it was.

The live system, confirmed by Samuel 2026-09-20. A Google Sheet called **"My Claude Budget"**, created 2026-08-26 and last modified **2026-09-16**.

It was moved to Google Sheets so Claude Code could write it directly instead of Samuel typing updates by hand.

**Tabs:** Dashboard · Setup · Income · Expenses · Transfers · Budget · Details. It covers **August 2026 – July 2027**, so it reaches both goals.

### The ledger is the source of truth, not the sheet

The engine's `context/money-ledger.md` is the text record. **The sheet is the budgeting layer; the ledger is the record. If the two disagree, the ledger wins** — Rule 6 in [[money-rules]].

That is not theoretical: the sheet and the ledger currently disagree about Cowrywise by NGN 368,041. See [[pots-and-accounts]].

### The design rule that fixed the old sheet

> **Nothing is typed on the Budget or Dashboard tabs.**

Budget's plan column reads Details. Its month columns read Expenses. Its savings block reads Transfers — all through `SUMIFS`. **A budget line cannot claim money moved when no row exists.**

That was the entire bug in the old sheets, and it is what let NGN 900,250 be booked to savings when only NGN 305,000 existed.

The Dashboard says it on its own face:

> *"Nothing is typed on this sheet. If a number here is wrong, the row that is wrong is on Income, Expenses or Transfers."*

### The Details tab

Answers "what is this category actually made of" — every subscription, every line, with amount, due day, tier and payday. **It is the only place a plan number is typed.**

**Cancelled items go Active = No. They are never deleted** — a subscription that reappears in three months is a pattern, and a deleted row hides it.

### How the finance agent writes it

Through an **Apps Script web app bound to the sheet.** It's still deployed in the sheet; only the client moved. Since 2026-09-22 the client lives in the Brain:

- `00-System/scripts/sheets.py`: the client. `ping`, `read`, `ops`, `doctor`, and `flush`/`pending` for batches that couldn't be delivered. Ported from the engine; only the paths and the credential handling changed.
- `00-System/scripts/sheets-apps-script.gs`: the script inside the sheet, with a placeholder instead of the token. Needed only to redeploy.
- A batch that can't reach the sheet parks in `06-Logs/automation/sheet-queue.jsonl`. The next session that can reach the sheet sends it. Nothing is dropped.
- The engine's originals, including `build_budget.py` and `plan.json`, stay at `08-Archive/accountability-engine/tools/sheets/`. *(They were deleted in the 2026-09-20 prune as "build tooling" and restored from git history the same day once Samuel confirmed this system is live.)*

The ledger is written first, then the sheet mirrors it. Row by row: [[03-Areas/finances/money-ledger|money ledger]] and the [[07-Agents/finance/profile|finance agent]].

### Credentials

The web app URL and its token work together like a password. **They never live in the Brain, a file the agent reads, or a chat.** They are Windows user variables on this PC, which `sheets.py` reads from the registry. Decided 2026-09-22 ([[00-System/decisions|decisions]]).

**Samuel runs this once, himself,** in PowerShell. It copies the three values from the old engine's `.env` into his user variables and prints only their names:

```powershell
Get-Content "$env:USERPROFILE\Desktop\engine\.env" | ForEach-Object { if ($_ -match '^\s*(?:export\s+)?(SHEETS_WEBAPP_URL|SHEETS_TOKEN|SHEETS_ID)\s*[=:]\s*["'']?(.+?)["'']?\s*$') { Set-ItemProperty -Path HKCU:\Environment -Name $Matches[1] -Value $Matches[2]; "saved $($Matches[1])" } }
```

It writes the registry directly. The first version used `[Environment]::SetEnvironmentVariable`, which tells every open window about the change and froze PowerShell for minutes on 2026-09-22 (the values were saved anyway). Connected and verified the same day: `doctor` reached "My Claude Budget", 7 tabs.

Then check: `python 00-System/scripts/sheets.py doctor`. No restart needed.

**If the token ever leaks:** change `TOKEN` in the Apps Script editor, Deploy → Manage deployments → edit → New version, then set `SHEETS_TOKEN` again with the same command pattern. `python 00-System/scripts/sheets.py script` puts the script, token filled in, on the clipboard. It never prints it.

### What the Dashboard shows

Read 2026-09-16, with the live figures in [[pots-and-accounts]]:

- **Where the money is** — bank liquid, Goal 1, emergency fund, Cowrywise investment, buffer, and "SAVED TOWARD THE GOAL" which deliberately excludes the investment and the buffer.
- **Goal 1 and Goal 2 progress** — target, saved, still to find, months remaining, and **needed per month from here**. That last one is the honest number: *"If this number keeps going up, the month is being lost."*
- **Reality check** — obligations floor NGN 936,800, plus the NGN 100,000 investment, so **committed outflow NGN 1,036,800/month**, and the income needed to hit the goal: **NGN 1,291,313/month**.
- **What the client mix produces** — 4 videos clears it, the August mix clears it, 2 videos is short by NGN 381,322.
- **Month by month** — income in, spent, surplus, and what moved to each pot. September 2026: **income NGN 1,373,937, spent NGN 1,273,708, surplus NGN 100,229.**
- **THE MONTH MUST BALANCE** — bills + one-offs + every pot = income, exactly.

### The earlier percentage design — not adopted

A different budget was designed on 2026-07-16 in a Claude chat: fixed buckets of Savings 20%, Business 20%, Building Project 27.7%, with the remaining 32.3% split across expense categories, built as an `.xlsx` with `openpyxl` for import into Google Sheets.

**It was never adopted.** The 32.3% split was never finalised, and Samuel confirmed on 2026-09-20 that the engine's system is the current one. The percentage design is recorded here in one paragraph rather than kept as a second, competing budget note.

One thing from it is worth carrying: his instruction on how the sheet should behave when allocation is wrong.

> *"I don't want any pop up messages, in fact, allow the allocation to me more than 100%, let me see it in red when it is more than 100% so I can adjust."*

**No blocking validation. Colour is the only signal.** Apply that to anything built for him.

Related: [[money-rules]] · [[obligations]] · [[income]] · [[pots-and-accounts]]. Back to [[03-Areas/finances/finances|Finances]]
