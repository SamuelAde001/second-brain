---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: F1
---

# F1 · Using DaVinci Resolve by Claude

> **Read when:** any step that touches Resolve: install, render, frame check, studying a timeline. The Editor and the one installer it names. Helpers read only F1.1 and F1.12. **Client values:** none. **Status:** draft, not yet approved by Samuel.

## Rules
### Who drives Resolve
- **F1.1** One driver at a time: the Editor, or the one installer it names. Helpers write files in the job folder and send renders to the render queue (`lab.py render … --nowait`), then keep building. ✅ *"While one agent is using DaVinci Resolve, the remaining agents are doing other things ... I don't want agents to have to be waiting"* (2026-10-24)
- **F1.2** When Samuel is working in Resolve, it is his until he says done: no scripts, no screen control, no renders. Do all other work outside Resolve and batch the Resolve steps for his go. 🔁 4 times. *"Don't do anything in Davinci for now as I am working there"* (2026-10-26) · *"do anything needed to do outside of resolve and when you really do need to use resolve, ping me"* (2026-10-09)
- **F1.3** Take a read-only snapshot of a timeline before he starts on it. The timeline he works on becomes his and is never rebuilt; the next build goes to a new version with his track carried over. ⚙️
- **F1.4** Lock handover: when he does a manual step (e.g. Magic Mask tracking), take the Resolve lock, stop every queue, keeper and watchdog, and tell him when it's safe. Release only when he says done. ✅ *"Take the Resolve lock for me now and tell me when it's safe."* (2026-10-15)
- **F1.5** Switch his project without asking, unless he has said he is using Resolve; then wait (A1.7, A1.8). A shared step runs as one block: save his project, load the job, run (no need to load his project back: A2.7, 2026-11-03); the older block also reloaded his project on his timeline, Edit page (`kits\inst\resolve_block.py`). ✅ (2026-10-09; asking dropped by A1.8, 2026-11-03)
- **F1.6** Another session may be rendering. Read the other jobs' RUN STATE and RESUME notes; never queue, stop or switch projects while a render runs. ⚙️
- **F1.7** You may start Resolve any time, and check its state yourself instead of asking him. ✅ *"Yes, you have full permission to always start resolve"* (2026-10-13) · *"Open resolve and check yourself"* (2026-10-10)

### Scripts first, screen control last
- **F1.8** Whatever a script can do, do it by script, across the whole video in one pass (disabling nodes, bevel off with `kits\brandfix.py`). Patch comps; don't regenerate them for a global change. 🔁 3 times. *"If there's anything that you can do with script, do it with script"* (2026-10-24) · *"can you do that without having to burn tokens regenerating all the comps?"* (2026-10-23)
- **F1.9** Screen control only for GUI-only steps (a menu path the API lacks, e.g. Ripple Delete Silence; opening a project from the Project Manager). Allowed while he is away; it stops the moment he needs the PC. ✅ *"Yes, you have permission to use screen control, excpet when I tell you I need to work on something else"* (2026-10-13) · *"Avoid using computer use when you don't need it"* (2026-09-24)
- **F1.10** When he is watching, narrate each step as you go. Switching pages is allowed; say when you do it. 🔁 3 times. *"Tell me out loud the steps you are taking, I am watching you"* (2026-09-25) · *"You can switch pages, I am not stopping you from doing that"* (2026-09-27)
- **F1.11** To see the Fusion viewer, use `scripts/fusion_view.ps1`, not page-hopping. And actually place the nodes. 🔁 2 times. ✅ *"why do you keep going to the fusion page?"* (2026-09-27)

### Getting visuals into his timeline
- **F1.12** Visuals are always editable Fusion nodes, so he can change text and animation himself without a re-render. Rendered video only for real-UI demos. OGraf/HTML is a preview aid, never the visual. 🔁 ✅ *"I can change the nodes, change the text, change the animation by myself."* (2026-09-27)
- **F1.13** Build a comp as a generated `.setting` and paste it once. Building node by node over many calls failed. ⚙️
- **F1.14** Place on an empty track: transparent base clip + `AppendToTimeline`, then import or paste. Check the timeline length is unchanged after every placement. ⚙️
- **F1.15** In his comp, touch only your own nodes, picked from your generated names list, never by exclusion (13 of his nodes were swept up). Never "fix" a layout change that could be his. Leave old leftovers parked and unconnected. ⚙️
- **F1.16** Test templates only on the scratch timeline `zz Lab (Editor)` or a scratch project; save his project first and put it back after. ✅ *"Yes, scratch project"* (2026-10-28)
- **F1.17** You see his work in it: he wants things visibly landing on the timeline, finished well enough to approve. ✅ *"I want to see things being done on the timeline ... make sure everything is perfect and Samuel can approve it"* (2026-10-15)

### Before and after a big Resolve step
- **F1.18** Before any install, full render or long build: save, `resolve_guard.py preflight --for install` (or `render`), `restart_resolve.py --force`, `open_job.py`. Installs run with the render queue stopped. Never run a cache and lab renders together. ⚙️
- **F1.19** At the end, leave Resolve on the working timeline, Edit page, project saved and restarted so it caches. ⚙️
- **F1.20** Logged-in web tools (Frame.io, Gamma) go through his Chrome via Claude in Chrome, main session only. When another session is using his Chrome, use headless Chrome with its own profile (`pipeline\capture\record_demo.py`). ✅ *"Gamma in chrome is logged in"* (2026-10-31) · (2026-10-22)
- **F1.21** He is fluent in Resolve, Fusion and OBS: don't explain the basics. 💡

### Where the how-to lives
- **F1.22** Open [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] before any API call you have not made on this job, and whenever a call fails. It holds paste, wiring, placement, frame grabs, caching and loading. ⚙️
- **F1.23** Open [[03-Areas/video-editing/sops/fusion-build|Fusion build SOP]] before building into a comp, and [[03-Areas/video-editing/sops/video-pipeline-tools|video pipeline tools]] for script paths, the render queue and the kit copies (never edit a kit copy). ⚙️

## Never
- **F1.24** Any `Insert*` call (`InsertFusionCompositionIntoTimeline`, `InsertGeneratorIntoTimeline`) on a cut timeline: it ripples every track, locks or not. ⚙️ failed 3 times (2026-09-28, 10-03, 10-10)
- **F1.25** An animated PNG, PNG sequence or other raster standing in for a visual. ✅ *"graphics are always nodes"* (≤2026-09-19)
- **F1.26** Ctrl+Z after a script action: Resolve's undo includes scripted operations. ⚙️
- **F1.27** Pasting through the Windows clipboard: his copying overwrites it. Paste from a file. ⚙️
- **F1.28** `DuplicateTimeline` on a heavy timeline through the MCP (blocked Resolve, memory 4.8 to 17 GB). ⚙️
- **F1.29** Changing Windows or system settings (TdrDelay and the like): give him the commands, he runs them. ✅ *"This all started when I changed that setting in the powershell, I want to return it to normal"* (2026-09-25)
- **F1.30** Touching his colour grade. 💡
- Superseded: never switch pages (OpenPage) without telling him (2026-09-27, morning), replaced the same day by F1.10.

## Pictures
- (no picture yet: none needed; this section is about process)

## Questions for Samuel
- **Q-F1.a** Screen control: on 2026-10-22 you said *"the only reason you would notify me for a permission is if you are doing screen ... and if you want to delete something"*. On 2026-10-24 the standing rule became "use every tool without asking, except deleting your things or keys". Does screen control still need a ping first? (A3.12, 2026-11-03: for the silence cut, *"ping me when you need it"*.) (Your A1.8 on 2026-11-03, *"use everytool without asking"*, points to no ping.) → Options: (1) no ping when you are away; ping only when you may be at the PC (2) always ping first. My pick: 1.
- **Q-F1.b** "Never touch his colour grade" (F1.30) comes from the Editor profile, not from your words. Keep it as a hard rule? → Options: (1) yes (2) only when you say so per job. My pick: 1.

## Sources
Replaces the Resolve-sharing parts of [[03-Areas/video-editing/ways-of-working|ways of working]] and [[07-Agents/video-editor/profile|Editor profile]]; draws on [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]], [[03-Areas/video-editing/sops/fusion-build|Fusion build SOP]], [[03-Areas/video-editing/sops/video-pipeline-tools|video pipeline tools]], [[03-Areas/video-editing/sops/unattended-run|unattended run]].

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
