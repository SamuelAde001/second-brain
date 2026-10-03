---
type: decision
area: system
status: active
updated: 2026-10-02
source: manual
tags: [decisions, system]
---

# Structural decisions

Decisions about the Brain itself: its structure, rules, agents and automations. Area-level decisions live in that area's `decisions.md`. Append-only.

---

Entries from 2026-09-20 to 2026-09-22, the build (Brain location, sync, naming, the agents and the first routines), are in [[00-System/decisions-2026-09-20-to-22|Structural decisions, 2026-09-20 to 22]].

## 2026-09-23 — Routines send a phone push

**Samuel:** *"I didn't see my routine send me notification on my phone this morning, I turned on my phone after the routine but I didn't see the notification on my phone"*.

**Found:** the 2026-09-23 morning brief ran on time (fired 6:34am WAT, finished in 48s, brief correct). It sent no push: a finished cloud routine does not notify the phone by itself, and neither prompt told it to.

**What:** both cloud routines (morning brief, night plan) now end their first message with a `PushNotification` call, one line under 200 characters. The tool is on each routine's allowed list. Canonical prompts updated in `00-System/automations/`. A manual test run of the morning brief at 7:01am WAT got "Mobile push requested"; whether it reached the phone is for Samuel to confirm.

**Who decided:** fix applied by the orchestrator on Samuel's report.

## 2026-09-23 — Every agent runs in the main session on Opus 5.5; routines stay on Sonnet

**Samuel:** *"I want all my agents to be Main, all of them should use OPUS 5.5, The only time I tell them to use something different is based on tasks"*. Then, on the routines: *"We can have the routines run on Sonnet since they aren't heavy tasks, they are not my agents, but they may call agents if needed to do better tasks"*.

**What:**
1. `video-editor` and `finance` now carry `runs-as: main-session`, like the other three. Their generated subagent files (`.claude/agents/`, `.gemini/agents/`) are pruned. No agent is a subagent.
2. Every profile is tier `strong`. `.claude/settings.json` sets the project default model to `claude-opus-5-5`.
3. A cheaper model or a subagent is used only when Samuel asks for one on a given task. Bulk work stays in scripts (AGENTS.md rule 10).
4. The morning brief and night plan cloud routines stay on `claude-sonnet-5`. They are not agents. Each gained step 8 and the `Agent` tool: a step that needs an agent's judgement goes to a subagent on Opus that reads that agent's profile and memory.
5. Updated: AGENTS.md §7, CLAUDE.md token discipline, portability tiers, the orchestrator's routing, the roster, `month-close`, the two routine notes.

**Objection (logged once, per the objection protocol):** Opus on every agent uses up the Pro plan's shared 5-hour and weekly limits faster than Sonnet did, and the video-editor pipeline was the heaviest consumer. The mitigation is the existing one: scripts do the bulk work, and nothing big is read into context.

**Not changed:** the Sunday session (`sunday-money-check`) is a desktop scheduled task. Those take no model setting, so it runs on the project default, now Opus 5.5.

**Who decided:** Samuel.

## 2026-09-23 — Agents have names, and every reply says which one is working

**Samuel:** the names are *"1. General Manager 2. Editor 3. Money man 4. PA 5. Brand manager"* (orchestrator, video-editor, finance, personal-life, content, in that order). Then: *"When a particular agent handles tasks, or is called opon, I want to always know which Agent is working on a task, even if we switch agent midtasks, always tell me the agent working now"*.

**What:** each profile has a `called:` field and says its name under its title. A message that opens with a name goes to that agent. Every reply opens with the working agent's name in bold brackets (**[PA]**), and each switch mid-task gets a new name line. It's written in AGENTS.md §7, the roster, the orchestrator's routing and a CLAUDE.md pointer. Folder and file names stay the same so no link breaks.

**Who decided:** Samuel.

## 2026-09-23 — Everything planned is a timed TickTick task; nothing goes on Google Calendar

**Samuel:** *"Always put what ever is planned in a schedule so I can see it on my tiktik calender, don't schedule on google cal"*.

**What:** every block of a plan (work, must-dos, meetings, and the routine blocks: nap, gym, dinner, the call) is a TickTick timed task with a start and an end, reminders at the start and 5 minutes before, so it shows on the TickTick calendar. This replaces the all-day-task shape. Google Calendar becomes read only. That replaces the 2026-09-22 rule that a meeting went in both places, and drops the inviting and joint-calendar permissions, since nothing is written there now. Updated: the personal-life profile, `night-plan`, `morning-brief`, `weekly-review`, the TickTick map, the orchestrator's limits, the roster, portability. Adapters regenerated.

**Who decided:** Samuel.

## 2026-09-23 — TDR timeout goes back to the Windows default after tonight's render

**Samuel:** *"set TdrDelay to how it was after this render"*.

**What:** after the current Resolve render finishes, Samuel deletes `TdrDelay` and `TdrDdiDelay` (set to 60 earlier today to stop the render-cache crash) and reboots. The GPU watchdog goes back to 2 s. He runs it himself: it's a system setting, which agents don't change.

**Objection (Editor), logged once:** the 60 s timeout is what stopped Resolve crashing on heavy Fusion comps ([[03-Areas/video-editing/troubleshooting|Troubleshooting]] §7). At 2 s the crash comes back, and the $7M Founder caching isn't finished (the rest of batch 2, batch 3, the Magic Mask clips). The cost of keeping 60 s is the desktop lagging during renders. 10 s would be a middle ground.

**Who decided:** Samuel.

## 2026-09-24 — Update: TDR timeout goes to 10 s, not back to the default

**Samuel:** *"okay set it to 10 then"*.

**What:** this replaces the 2026-09-23 entry above. `TdrDelay` and `TdrDdiDelay` go from 60 to 10, not deleted. That means shorter desktop freezes during renders and some protection against the render-cache crash. Samuel runs it himself (a system setting) and reboots after the current render.

**Who decided:** Samuel.

## 2026-09-24 — Samuel writes in the Brain himself, through Obsidian on the PC

**Samuel:** *"I want to sometimes put notes and inputs in the brain myself via Obsidian"*.

**What:** on the PC, Obsidian is open on the Brain folder itself, so what he types lands straight in the Brain. Nothing has to be merged. He may write in any folder; `01-Inbox/` is for anything he isn't sure where to put. At session start, every agent session runs `git status`, takes any change no agent made as his, adds missing frontmatter (`source: manual`) and a link back to the area, files it only if it's clearly misplaced, never rewrites his words, and commits it as `Samuel (Obsidian): …`. Rule 8 (the phone writes to the inbox only) stands: phone sync isn't set up. Updated: AGENTS.md rule 8 and §12, portability access modes.

**Who decided:** Samuel (writing in Obsidian). The pick-up steps are the General Manager's.

## 2026-09-24 — Brand manager gets read-only access to the personal-brand footage folder

**Samuel:** *"C:\Users\repzy\Desktop\Video edits\My videos\Instagram Samuel Signals — This path is where every footage concerning My personal brand lives"*, in answer to the request to go to his B-roll archive and identify and arrange the B-roll.

**What:** the content agent can read that folder (`.claude/settings.json` additionalDirectories plus a Read allow, AGENTS.md §10, content profile). Scripts only: listing, ffprobe, frame grabs into the session scratchpad. Nothing there is moved, renamed or deleted without his yes for that batch (rule 5). The catalogue lives in the Brain at [[03-Areas/personal-brand/b-roll-archive|B-roll archive]]. Closes open question 89.

**Who decided:** Samuel (the path and the job). Read-only by default is the Brand manager's call, from rule 5.


## 2026-09-25 — PA standing rules; the brief and night plan rebuilt around TickTick

**Samuel:** *"I don't like the way the The morning Brief and Night plan send there reports"* · *"they forget things that I have settled before on another chat"* · *"majorly work with the ticktick app, they should work well with that to see what has been planned, what has been ticked, what has been adjusted"* · *"Habits I said I would keep"* · *"it sends report not well formatted for me to understand like it's talking to itself"* · *"it should list the tasks for the day, not just the calender, but the main task for the day"* · *"crosscheck the routines to see how they can be better"*.

**What:** (1) New `07-Agents/personal-life/standing-rules.md`: the current settled rules for his day, habits, content and commitments, plus how reports must read. Read first by the brief, the night plan and the weekly review; it wins over older lines. Any session that settles such a rule updates it and pushes (AGENTS.md §9, orchestrator standing duties, PA profile). It is a current-state file, edited in place; history stays in PA memory and log. (2) `night-plan`: reads the whole daily note (replans included); checks each planned task by its TickTick ID (a hidden `%% ticktick: … %%` line written at plan time) as done, not done, moved or removed; reads all three habits; asks only what TickTick can't answer; one fixed message shape with numbered questions. (3) `morning-brief`: main tasks from TickTick first, then the schedule, habits, client, overdue, yesterday; Google Calendar events others created are listed apart from his plan. (4) Both routine prompts shortened to point at the skills, with a git sync first.

**Why:** the run logs showed the 2026-09-24 night run missed a same-day replan (the "3 videos" error), checked two habits of three, and the 2026-09-25 brief collapsed into one paragraph and listed one task out of four.

**Who decided:** Samuel (what's wrong and what he wants). The file, the ID tracking and the message shapes are the General Manager's build.

## 2026-09-25 — The night plan routine runs on Opus

**Samuel:** *"Yes move night plan to Opus"*, on the General Manager's recommendation after the Sonnet run of 2026-09-24 called "Record 3" a miss against a replan made that morning.

**What:** routine `trig_01Pet8jENJ1CEguycgH9suEf` model `claude-sonnet-5` → `claude-opus-5-5`. The morning brief and the Sunday session stay on Sonnet. Updated: the automation note, AGENTS.md §7, the orchestrator profile, the roster. This narrows the 2026-09-23 rule that routines run on Sonnet.

**Cost:** Opus uses more of the shared Pro limit on every night run.

## 2026-09-28 — Social media is checked nightly from StayFree

**Samuel:** *"Social media doomscrolling at the wrong times are part of what is making me less productive"* · asked whether the PA could read his StayFree usage *"to help keep me accountable"* · *"yes build it, YouTube counts as social media but sometimes it's used for work"*.

**What:** a new commitment, *social media only while eating* ([[06-Logs/commitments|commitments]]). `00-System/scripts/screen_time.py` reads StayFree's local Windows data read-only (the PC's own apps, plus the phone and Chrome sessions StayFree caches from its cloud sync) and writes `06-Logs/screen-time/<date>.md`. Windows Task Scheduler runs it at 8:30pm and pushes, so the 8:45pm cloud night plan can read it. Night-plan skill, standing rules, PA profile, AGENTS.md §10 and the systems register updated. New automation note: [[00-System/automations/screen-time|screen time]].

**Why a script, not computer use:** Samuel asked about computer use reading StayFree daily. The General Manager's recommendation was a script: the same data is on disk with exact times, a script costs no Pro usage, it doesn't take over the mouse, and the night plan is a cloud routine that can't see the PC screen anyway. Computer use stays a fallback only.

**Who decided:** Samuel (the commitment, the build, YouTube counts). The PA's defaults, not his words yet: meal windows 1:00–2:00pm and 6:30–7:30pm, a miss at 10 minutes or more outside them, WhatsApp not counted.

## 2026-09-28 — Social media rule changed: work blocks and bedtime, not meals

**Samuel, same day:** *"No, I can't limit social media to when I am eating, Social media should not be used when I am activly beant to be doing a work … or I am done with the task for that moment I can use Social media, but obviously not late in the night when it's time for bed and not early mornings"*.

**What:** the check counts social media inside his work blocks (timed TickTick tasks at priority 3 or 5, ended early when ticked) and 11:00pm–7:00am. Meal windows removed. `screen_time.py` now writes each social session's times into the day's file (hidden `%% social: … %%` line) and has `--check "HH:MM-HH:MM,…"`, which the cloud night plan runs against the day's work blocks. Updated: the script, the night-plan skill, standing rules, commitments (new dated line), the automation note, daily routine.

**Who decided:** Samuel (the rule). The PA's defaults, not his words yet: bedtime-and-morning as 11:00pm–7:00am, a miss at 10 minutes or more.

**Addendum, same day — lofi.** Samuel: *"I sometimes listen to Lofi from youtube when working though so I don't know if that counts since youtube window is not active when working"*. Checked: the StayFree Chrome extension counted 60m of YouTube on 2026-09-27/28 while Resolve was the window in front. The script now counts a site only while Chrome is the foreground window on the PC. This morning's YouTube dropped from 2h 00m to 47m.

## 2026-09-28 — Tidy: long files split, state separated from history

**What:** after an audit Samuel asked for (*"Tidy"*):
- `build-state.md` holds the current state only (about 50 lines, read at every session start). Its narrative and session log moved verbatim to [[00-System/build-history|Build history]]; new session log lines go there.
- This file's 2026-09-20 to 2026-09-22 entries moved verbatim to [[00-System/decisions-2026-09-20-to-22|their own file]].
- The Editor's Resolve and Fusion scripting and crash lessons moved verbatim from its memory to [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]]. Its profile says to read that note before scripting Resolve or Fusion.
- The retired sheet bridge (`sheets.py`, `sheets-apps-script.gs`) and the migration splitter moved to `08-Archive/retired-scripts/`.
**Why:** the notes read at every start had grown past the 300-line rule, and every agent session paid for them. Nothing was deleted; moving text verbatim keeps the history.
**Blocked:** three deletions (an empty duplicate log, a superseded PDF, a finished cache queue) were refused by Claude Code's auto-mode classifier. They wait for Samuel.

## 2026-09-28 — The four job skills are dropped; the Editor grows by SOPs, small skills and scripts

**What:** `brainstorm`, `plan`, `systemize` and `commit` will not be built. Samuel, asked why he'd need them: *"Drop them"*. The Editor's four planned pipeline skills (`routerise-cut`, cut-sheet, `storyboard-preview`, `html-to-fusion`) are dropped as well. Samuel: *"The editor pipeline is still learning, I can't turn it to a skill yet cause I constantly still make changes, and nothing is really the same for now, I think the best is editor has SOP's and small skills for repeated specific tasks, and scripts he uses"*.
**So:** the Editor works from its SOPs, its scripts and [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]]. A small skill is built only for a specific task that repeats the same way (the systems register's ladder: SOP → checklist → skill → automation, lowest rung first). With nothing left to build, **Phase 4 is closed** (2026-09-28).
**Why:** the General Manager's audit found no note describing what the four job skills would do, and each overlapped something already running (agents think ideas through, night-plan/weekly-review/budget plan, the PA holds commitments, git commits are a rule). The pipeline still changes every job, so a skill would freeze it too early.

## 2026-09-28 — The Editor closes every job with a review

**What:** a standing step the day a job is delivered: record what Samuel fixed (with a count), fold each new rule into one place, sort the job's scripts into tested and one-off, and track which steps ran unchanged. [[03-Areas/video-editing/sops/end-of-job-review|End-of-job review]]. Samuel: *"yes"*, to the General Manager's proposal.
**Why:** with the pipeline kept as SOPs and scripts, the risks are rules scattered across six notes, one-off scripts mixed with tested ones, and no measure of whether the Editor is doing more of the work. Three unchanged runs of a step make it a small-skill candidate.


## 2026-09-29 — Model and effort per job; Sonnet helpers for mechanical jobs; effort floor medium

**What:** every agent still runs in the main session on Opus 5.5, but each job now has a set model and effort ([[00-System/model-routing|Model routing]]). Skills carry `effort` (and `tier` + `context: fork` for the Sonnet jobs); `build_adapters.py` maps them, so Claude Code applies them automatically on the PC and in the cloud routines. Sonnet 5.5 runs as a helper with its own context, without Samuel asking each time, on `subtitle-transcript-formatter`, the `video-edit-pass` phase-2 transcript, and reading-heavy sweeps and web research. Batch builds of approved visuals go to a fresh Sonnet session, which the General Manager names at session start. Samuel: *"yes to all three"*, then *"No use of low effort, the lowest is medium"*.
**Replaces:** the 2026-09-23 rule that a cheaper model or a subagent runs only when he asks on a given task. That still holds for everything the map doesn't name.
**Why:** he asked to cut time and cost without losing output quality. Sonnet costs half as much on new input and output but the same on cached input, and the cache belongs to one model, so switching mid-session usually costs more. Effort is the cheaper dial. Sonnet only pays where the context starts fresh and the job is mechanical and output-heavy.

## 2026-09-29 — Objection logged: brand strategist

Samuel is hiring a brand strategist (NGN 50,000, one-off). The Brand manager objected once: [[brand-context]] already holds positioning, pillars, tone and posting structure, and the gap is output and numbers. He decided: *"I think I would go ahead and have the Strategist, cause what I am doing is not working and is Random, I feel having someone in the loop would really be helpful"*. Executed. Record: [[03-Areas/personal-brand/personal-brand-decisions|Personal brand decisions]].

## 2026-10-02 — Gemini CLI becomes the backup AI; Claude can hand it jobs

**What:** Gemini CLI moves from guest to **backup**. When Claude's limits run out, Samuel opens Gemini in the Brain and types `/relay`: it reads a brief of what Claude was doing (built by `relay.py` from Claude Code's saved transcript and git, so it works even when Claude is cut off mid-task) and carries on, writing like the primary under the same rules, commits prefixed `[gemini]`. `/handback` logs where it stands in `06-Logs/relay/relay-log.md`, commits and pushes. Claude can also hand Gemini reading-heavy jobs through `ask_gemini.py` (read-only unless Claude allows edits). The session-start hook names `[gemini]` commits for Claude to review. Protocol: [[00-System/relay|Relay]].
Samuel: *"I don't like the fact that my tokens can finish on Claude and I have to wait for Claude before I resume, I want Claude to be able to talk with Gemini CLI to get some work done, or I can continue some work that Claude was doing in Gemini CLI, let's set it up"*. That is also his go-ahead for Brain content going to Google through Gemini (the orchestrator's "first Gemini test" gate).
**Read access added:** `relay.py` reads Claude Code's transcripts and Gemini's chats outside the Brain, read-only, printing to stdout only (AGENTS.md §10).
**Why backup and not guest:** a guest writes only to `01-Inbox/` and `06-Logs/`, so it could not continue any real task. Full write with `[gemini]` commits and Claude's review keeps the record clean.
**Not connected in Gemini:** TickTick, Resolve, Calendar, Gmail, Drive. Steps that need them wait for Claude.

## 2026-10-02 — Gemini gets TickTick, Resolve, Gmail, Calendar and Drive

**What:** Samuel: *"I want Gemini to be able to do TickTick, DaVinci Resolve, Calendar, Gmail and Drive"*. `.gemini/settings.json` now connects Blackmagic's `ResolveMCP.exe` (the same server Claude Code uses) and TickTick's official server `https://mcp.ticktick.com/` (its own sign-in). Gmail, Calendar and Drive come through Google's Workspace extension for Gemini CLI, installed per PC. The Brain's rules carry over unchanged: nothing scheduled on Google Calendar, no Gmail send without his yes on that message, the PA's TickTick rules, the Editor's Resolve SOPs. [[00-System/relay|Relay]] → What Gemini is connected to.
**Correction to the entry above:** Gemini CLI is not on his PATH. The 0.60.0 copy lives in the Claude app's private storage, which only Claude's own shell sees. He installs a real copy with `npm install -g @google/gemini-cli`.

## 2026-10-02 — Gemini CLI replaced by Antigravity CLI

**What:** Samuel's Gemini CLI sign-in failed: *"This client is no longer supported for Gemini Code Assist for individuals"*. Google ended Login with Google for Gemini CLI on personal, AI Pro and AI Ultra accounts on 2026-06-18; Antigravity CLI (`agy`) replaces it and comes with his AI Pro plan. The relay moves to it: Resolve and TickTick in `.agents/mcp_config.json`, `/relay` and `/handback` (Gemini CLI commands, deleted the same day they were made) become the skills `pick-up` and `hand-back`, which any AI runs; `ask_gemini.py` calls `agy` and is read-only. The backup tier, the `[gemini]` prefix and the rules are unchanged. [[00-System/relay|Relay]].
**Correction to the entry above:** the Google Workspace extension is for Gemini CLI. In Antigravity, Gmail, Calendar and Drive need Google's Workspace MCP servers and a Google Cloud OAuth client Samuel creates. Not connected yet.

## 2026-10-02 — Gemini becomes an equal primary

**What:** Samuel: *"I want to Gemini Antigravity app to have access to all you can do, and be able to do everything you can do, just in case I don't feel like using you, you both should be on the same level, and not Gemini being second in place"*. Claude Code and Gemini in Antigravity (app and CLI) are now **equal primaries**. "Backup" is gone everywhere (AGENTS.md §11, CLAUDE.md, GEMINI.md, portability, relay, the pick-up and hand-back skills, the orchestrator profile). Each signs commits with its own `Co-Authored-By` trailer instead of a `[gemini]` prefix, and neither reviews the other as a senior: whichever runs next reads the other's new commits.
**Parity built the same day:** Gemini's guard rails mirror Claude's deny and ask lists (`.agents/hooks.json` → `00-System/scripts/agy_guard.py`; tested: secrets read blocked, ordinary commands run). Session start runs in Gemini too (first-turn hook → `session_start_sync.py --for gemini`). `relay.py` reads the Antigravity app's sessions, not only the CLI's. Notion added to Gemini. Tiers mapped for Gemini, strong = Gemini 3.1 Pro (High), his pick in the app. The helper call `ask_gemini.py` runs in plan mode, because agy is now on always-proceed and a headless run has no one to ask.
**Not at parity, and why:** Gmail, Calendar and Drive (need a Google Cloud OAuth client he creates); computer use (needs a third-party Windows MCP server, his yes to install); cloud routines (they run on Claude regardless); Gemini handing Claude a job (needs the Claude Code CLI installed). Listed in [[00-System/relay|relay]] → What each AI can reach.
**Source:** Samuel, in chat with Claude Code, 2026-10-02.
## 2026-10-03 — Chrome browser for Workspace instead of OAuth extensions
Samuel: *"Alright, when you want to use Gmail, Calendar, and Drive, just use my chrome browser instead"*.
**What**: The plan to create a Google Cloud OAuth client for Gmail, Calendar, and Drive is dropped. Instead, any tasks requiring them will be done by automating the Chrome browser via the computer-use MCP server.
**Who decided**: Samuel.

