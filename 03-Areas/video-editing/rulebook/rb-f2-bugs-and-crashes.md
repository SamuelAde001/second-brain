---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: F2
---

# F2 · Bugs, crashes, bug reports

> **Read when:** Resolve crashes, hangs or slows down; a script or helper fails; before a long cache or render. The Editor and the main session (Resolve debugging is an Opus job). **Client values:** none. **Status:** draft, not yet approved by Samuel.

## Rules
### Resolve crashed or hung
- **F2.1** Crashed: relaunch it yourself at once (`restart_resolve.py`, then `open_job.py`, or `GotoRootFolder` → `OpenFolder("Routerise")` → `LoadProject` → timeline), check the last saved state and carry on. Never stop and wait. 🔁 4 times. *"When resolve crashes, open it back yourself, I am not always on my PC"* (2026-10-03) · *"When davinci creashes, next time start it up back"* (2026-10-07)
- **F2.2** Unresponsive: after one `run_script` timeout, check `(Get-Process Resolve).Responding` once. If False, tell him in the same reply (last call, last save time), then restart with `restart_resolve.py` (`--force` when Windows says it responds but it doesn't). No minutes of watching first. ✅ *"Whenever Davinci is unresponsive, tell me immediately"* (2026-09-27)
- **F2.3** Find what made it crash and fix that, then finish the job (the cache, the install). A restart alone is not a fix. ✅ *"if it crashes, find what makes it crash and fix it"* (2026-09-23)
- **F2.4** A timed-out `run_script` keeps running inside Resolve. Probe with a trivial call before the next one; keep batches under ~35 s. If `GetCurrentPage()` returns None, a dialog is blocking: check his screen before blaming the script. ⚙️
- **F2.5** Expect crashes on long installs and caches. Save before every risky step and every long export loop; the driver script relaunches, reopens and retries. ⚙️

### Known causes (check these first)
- **F2.6** Render-cache crash `fusionsystem.dll+0x30c290` = GPU timeout (TDR). Check System log `nvlddmkm` 153, read `TdrDelay` (read-only) before any heavy cache or render. Setting it is his job (admin + reboot); give him the commands. ⚙️
- **F2.7** Memory: Resolve climbs to 13-44 GB during installs, then Fusion and imports fail at random. Save and restart between big batches (peak fell from 31.5 GB to 11.8 GB). ⚙️
- **F2.8** Stuck engine: viewer not following `SetCurrentTimecode`, or ~85 s a frame = move the playhead, save, restart. A hung cacher: `kits\cache_tl.py` treats 5 min without frames as a hang; after 5 stalls in a row, find the comp (match cache frame counts to Fusion item durations) and turn that clip's cache off. ⚙️
- **F2.9** Heavy looks cost stability: Neo Bevel lags playback and render; reflections or glow on every card crashed his cache. Flag them in the plan. ⚙️ (2026-10-10, 2026-10-23)
- **F2.10** Leftovers fill memory and hold locks: stray headless Chromes (`resolve_guard.py clean-chromes --dry-run`, then without), Python children of a stopped pipeline (kill by command line), stray Resolve MCP servers from other sessions. Never close his own Chrome. ⚙️
- **F2.11** Connect audio devices before opening Resolve (Bluetooth switch → WASAPI scan crash). If Resolve looks closed but still sits in Task Manager, end every DaVinci process before relaunching. ⚙️
- **F2.12** Files named with digits before the extension (`thumb_01.png`) import as image sequences and go Media Offline: no trailing digits, one folder per plate. ⚙️

### Slow PC and caching
- **F2.13** Proxies fixed most of the caching slowdown: make them on every job. ✅ *"Making the video a proxy solved a lot of the cap"* (2026-09-25)
- **F2.14** Don't lead with "close your browser" (~0.5 GB VRAM at most) or CPU priority (does nothing). The performance checklist is his to apply; check settings by script, never trust a report that they were applied. ⚙️

### Reporting a bug
- **F2.15** Tell him in one block: what broke, last call, last save time, what was lost, what you did, what's next. If he is away and you need him, ping his phone (F5.11). 💡
- **F2.16** Log every new bug in [[03-Areas/video-editing/troubleshooting|troubleshooting]] at the bottom: Date · Status · Symptom · Cause · Fix that worked (or proposed) · What to check first. A proposed fix stays proposed until he confirms it. ⚙️
- **F2.17** Crash evidence is parsed by script, never read into context: `Support\logs\davinci_resolve.log`, `crash_archive.txt`, Windows Application log (ID 1000), System log `nvlddmkm`, Resolve's `.dmp` via `scripts/resolve_crash_dump.py` (dump first). ⚙️
- **F2.18** Every Resolve trap found on a job goes into [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] the same session, so no one hits it twice. ⚙️

### Where the how-to lives
- **F2.19** [[03-Areas/video-editing/troubleshooting|Troubleshooting]] §7 for crash logs and the TDR history; [[03-Areas/video-editing/resolve-performance|Resolve performance]] for the caching checklist and hardware; [[03-Areas/video-editing/sops/unattended-run|unattended run]] for restarts during a night run. Power cuts and resuming: F5.10. ⚙️

## Never
- **F2.20** Probe a comp tool with `Output.GetValue`, or walk every comp's tool list on a ~400-op timeline: both crashed Resolve. ⚙️
- **F2.21** Bulk `ExportCurrentFrameAsStill` (~240 exports crashed it): grab frames with Deliver render jobs. ⚙️
- **F2.22** `Remove-Item` or `Stop-Process` during an unattended night (permission prompts stall it): `restart_resolve.py` is the only way to end Resolve. ⚙️
- **F2.23** Change a system setting yourself. ✅ *"I want to return it to normal"* (2026-09-25)

## Pictures
- (no picture yet: none needed; this section is about process)

## Questions for Samuel
- **Q-F2.a** TdrDelay: 60 s was proposed 2026-09-23; you reverted to the 2 s default 2026-09-25; on 2026-10-24 you chose 10 s, but it read unset that day after a Windows Update. Is 10 s set now? → Options: (1) yes, agents only check it (2) not set, you'll run the commands (3) leave at 2 s and cache heavy comps one at a time. My pick: 2.
- **Q-F2.b** There is no bug-report format in any source; F2.15 is my proposal. Should every crash ping your phone, or only crashes that stop the job? → Options: (1) ping only when the job is stopped or work was lost (2) ping every crash. My pick: 1.

## Sources
Draws on [[03-Areas/video-editing/troubleshooting|troubleshooting]], [[03-Areas/video-editing/resolve-performance|Resolve performance]], [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]], [[03-Areas/video-editing/sops/unattended-run|unattended run]], [[03-Areas/video-editing/ways-of-working|ways of working]] → When Resolve stops responding.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
