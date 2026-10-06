---
type: sop
area: system
status: active
updated: 2026-10-06
source: manual
tags: [claude, plan, migration, accounts]
---

# Move to the Claude Max $100 plan (new account)

Samuel, 2026-10-06: *"Tonight I would be paying for the Max $100 plan on my other account so that I can migrate from pro plan, so prepare everything needed for that."* His weekly Pro limit ran out on Sunday and stayed full until today.

**What moves and what doesn't.** The Brain is on GitHub and holds every rule, agent, skill, prompt and decision, so none of it moves. What is tied to the *claude.ai account* does not follow a subscription to a different account: connectors, cloud routines, the GitHub App link, uploaded skills, chat memory and chat history. Those are rebuilt on the new account, in the order below.

One thing worth knowing before tonight: if the Max plan can be bought on the **current** account instead, none of this section is needed and it is a five-minute upgrade. Samuel chose the other account, so the rest assumes that.

Area: [[00-System/systems-register|Systems register]] · Plan rules today: `CLAUDE.md` → Token discipline

## What is ready (done 2026-10-06)

- **Skill zips** for the four claude.ai skills, built from the Brain copies: `C:\Users\repzy\Desktop\Claude account migration kit\skill-zips\` (`edit-clock`, `video-edit-pass`, `subtitle-transcript-formatter`, `yap-session-planner`).
- **Routine prompts as plain text**, ready to paste: `...\Claude account migration kit\routine-prompts\` (`morning-brief.txt`, `night-plan.txt`, `sunday-money-check.txt`). Extracted from the canonical notes in [[00-System/automations/morning-brief|morning-brief]], [[00-System/automations/night-plan|night-plan]] and [[00-System/automations/sunday-money-check|sunday-money-check]]. Settings for each (time, model, effort, connectors) are in those notes.
- Checked: no `ANTHROPIC_API_KEY` or token is set on the PC, so Claude Code will bill the subscription once signed in, not the API.

## Status, 2026-10-06 (afternoon, General Manager)

Checked from Claude Code on the new account:

- [x] **1. Paid.** Usage card reads plan **Max**: 5-hour window, weekly all models, weekly Fable; extra usage off. Paid on claude.ai, Cleva card, NGN 143,942 (ledger).
- [x] **2. Desktop app on the new account.** No `ANTHROPIC_API_KEY` in the environment.
- [x] **3. Connectors.** TickTick and Google Calendar added by Samuel; both tested (today's tasks and the calendar list read back).
- [x] **4. Permission IDs.** Swapped in both settings files: TickTick `6f1cbea4-dd7a-49b8-948c-9d212b86965d`, Google Calendar `f1580cca-def5-4557-a3af-bef3139f7e0a`.
- [x] **5. GitHub** connected on the new account by Samuel; the test run cloned the repo.
- [x] **6. Routines rebuilt** in a new cloud environment `Default` (`env_01Q12cyHPZ9WDEqLkNm8vTFi`): Morning brief `trig_01BaBcE4pPcSJ8tAgXfVAkVV` (Sonnet 5.5), Night plan `trig_01VEkuULMBcqFWrFyWCB3y3q` (Opus 5.5), both with TickTick and Google Calendar. Morning brief fired by hand 2026-10-06 17:00 WAT: cloned, synced, loaded both connectors. 
- [ ] **Old routines off** on the old account (Samuel): the new night plan fires tonight at 8:45pm, so the old one must be off before then or he gets two.
- [x] **7. Sunday task.** It did not survive the switch (no scheduled tasks listed). Recreated from the canonical prompt in [[00-System/automations/sunday-money-check|sunday-money-check]], cron `0 15 * * 0`. First run Sunday 2026-10-11.
- [ ] **8. Skill zips** and **9. chat memory**: Samuel, on claude.ai.
- [ ] **Terminal CLI** (`claude auth status`): logged out. Samuel runs `claude auth login` with the new account if he wants `claude` in a terminal.
- [x] Plan lines rewritten: CLAUDE.md, AGENTS.md §1, toolchain, model routing.

## Tonight, in order

**1. Pay and confirm.** On the new account: subscribe to Max, the $100 tier. Check Settings → Usage on that account shows it.

**2. Sign the Claude desktop app into the new account.** Sign out of the old one first. The Code tab, this Brain's folder and the scheduled task stay as they are; they belong to the PC, not the account.

**3. Reconnect the connectors on the new account** (Settings → Connectors). The Brain uses:

| Connector | Needed for | Priority |
|---|---|---|
| TickTick | night plan, morning brief, weekly review, everything planning | **first** |
| Google Calendar | morning brief, night plan (read) | **first** |
| Notion · Gmail · Google Drive · vidIQ | unused until Samuel says so ([[00-System/portability|portability]] → Integrations) | later, optional |
| DaVinci Resolve | local server, not a connector; comes with the desktop app config on the PC | check it still appears |

The 70,000-token session start load is mostly connectors and plugins the Brain never uses (see [[00-System/model-routing|model routing]]). Don't reconnect the ones in the "later" row until needed.

**4. Fix the permission rules.** `.claude/settings.json` and `.claude/settings.local.json` allow TickTick and Calendar tools by the *old account's connector IDs*: `mcp__0033a1e9-0365-41cc-8c9b-7d79a9fcca73__*` (TickTick) and `mcp__a5641035-0f40-4dde-9da3-d31977042c78__*` (Google Calendar). The new account's connectors will have different IDs, so every TickTick call would ask permission again. Open a Claude Code session after step 3 and say **"account switched, run the post-switch checklist"**: the General Manager swaps the IDs in both files, then commits the settings change. Gemini's guard (`.agents/hooks.json`) doesn't use these IDs and is unaffected.

**5. Connect GitHub for cloud sessions.** On the new account, install the Claude GitHub App on `SamuelAde001/second-brain` (private). Without it the routines and phone sessions cannot clone the Brain. Keep Samuel's 2026-09-22 rule: cloud sessions push straight to `main`. If the new account's cloud environment restricts pushes to a `claude/…` branch, that is handled by the merge-and-push-to-main rule in [[00-System/portability|portability]] → Cloud sessions and the PC.

**6. Recreate the two cloud routines** (claude.ai → Code → Routines). Both: repo `SamuelAde001/second-brain`, connectors TickTick and Google Calendar.

| Routine | Cron (UTC) | Time | Model | Prompt file |
|---|---|---|---|---|
| Morning brief (6:30am WAT) | `30 5 * * *` | 6:30am WAT (fires ~6:34) | Sonnet 5.5, standard | `morning-brief.txt` |
| Night plan (8:45pm WAT) | `45 19 * * *` | 8:45pm WAT | Opus 5.5, strong | `night-plan.txt` |

The old routines (`trig_01UN9y23v1UwoBtBq3qmoJiH`, `trig_01Pet8jENJ1CEguycgH9suEf`) live on the old account. **Disable them there after the new ones are confirmed**, or both fire and you get two briefs and two night plans, and two sessions pushing to `main`. Don't delete until the new ones have run once.

**7. The Sunday check needs nothing rebuilt.** `sunday-money-check` is a desktop-app scheduled task, tied to the PC. Check it still shows under Scheduled once the app is on the new account; if not, recreate it from `sunday-money-check.txt` (cron `0 15 * * 0`).

**8. Upload the four skills** (Customize → Skills on the new account) from the zips. Only matters for chat on the phone and web, where the Brain isn't reachable; Claude Code uses the Brain copies.

**9. Carry over what chat knew about him.** On the old account, ask Claude to export its memory about him (Settings → Capabilities → memory, or "write out everything you remember about me, as a list"), then paste it into the new account's chat with the import-memory flow. Optional: the Brain is the real memory ([[AGENTS]] §11), so skip this if the Brain already covers it. Old chat history stays on the old account; the Claude export copy is in `01-Inbox/_imports/` already.

**10. Test before bed.** In the new account's Claude app on the phone, start a session on the Brain and ask for the morning brief. If it reads TickTick and today's day correctly, the chain works: GitHub App, connector, repo. Then run the night plan once by hand rather than waiting for 8:45pm.

## After it works (the General Manager does these, on Samuel's word)

The plan-sizing facts in the Brain are Pro-sized and should be rewritten once Max is real, not before. A draft of what changes:

- `CLAUDE.md` → *Token discipline (Pro plan)* becomes the Max numbers: ask Samuel for the 5-hour and weekly usage he sees, never guess them. The "script first" rule stays, it saves money in any plan.
- [[00-System/model-routing|Model routing]]: the plan-use line ("5-hour window 28%, weekly 31%") is stale. Opus stays the default for agents; Samuel's floor `medium` effort stays. With more room, ask whether `high` should be the default on judgement jobs. His call.
- [[00-System/automations/morning-brief|Morning brief]] on Sonnet stays: Samuel chose it on 2026-09-23 because it isn't a heavy task, not because of limits.
- Gemini remains an equal primary and the fallback if the Max weekly limit ever fills ([[00-System/relay|relay]]).

## Money

The $100 plan is not in the October plan. On 2026-10-04 the Money man worked out a gap of NGN 82,283 against the plan and was waiting for Samuel to say whether it comes from Goal 1 or Buffer ([[03-Areas/finances/finances-decisions|finance decisions]]). He has now said he is paying tonight. **Open:** where the money comes from, and whether the "other account" is his own card or someone else paying. Logged in [[00-System/open-questions|open questions]]; the Money man records the decision when Samuel states it. Payday A had not landed as of 2026-10-05 and the bank was at NGN 0.

## If something fails

| Symptom | Cause | Fix |
|---|---|---|
| Every TickTick call asks permission | old connector IDs in settings | step 4 |
| Routine session says it cannot clone the repo | GitHub App not on the new account | step 5 |
| Two morning briefs | old routine still on | disable it, step 6 |
| `claude` in a terminal says not logged in | the terminal CLI is separate from the desktop app | `claude auth login` in a terminal, with the new account (it was logged out already on 2026-10-06) |
| Billing shows API charges | `ANTHROPIC_API_KEY` set | it isn't today; keep it that way |
