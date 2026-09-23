---
type: agent
area: video-editing
status: active
updated: 2026-09-22
source: interview
tags: [agent, memory]
---

# video-editor — memory

Append-only. What this agent has learned by doing. Newest at the bottom. Facts here were verified in action, not assumed (AGENTS.md rule 6).

---

## 2026-09-21 — The Resolve MCP bridge, proven

Verified live against Resolve **21.1**, project *"1. Taking a step back from Claude (and why you should too)"*.

- **Entry point is the `resolve` global.** Not `app.GetResolve()` — `app` is undefined in this sandbox. Start every script from `resolve`.
- **Sandbox is locked down:** `import os` (and other filesystem imports) is blocked — `PermissionError: import not allowed`. `import json` is fine. Do listing/filesystem work outside Resolve.
- **~10s hard limit per `run_script` call.** The **first Fusion operation of a session spins Fusion up and blows the limit** — it half-completed a `DuplicateTimeline` + `AddFusionComp` chain the first time. Fix: warm Fusion with a lone `AddFusionComp` (or any single Fusion call) first, then build in the next call. Keep each call small.
- **Duplicate a timeline** with `timeline.DuplicateTimeline("<name>")` → returns the new timeline. Non-destructive; it is the sanctioned "duplicate first" op. Then `project.SetCurrentTimeline(dup)`.
- **Fusion comp on a clip:** `timelineItem.AddFusionComp()` → a live FusionComp exposing the full Fusion tool API (`AddTool`, `FindTool`, `GetToolList`, `Lock`). `GetFusionCompByIndex(1)` re-fetches it.
- **Build nodes:** `comp.AddTool("<ToolID>", x, y)` — the `x, y` **are** the flow position (pass them here; `comp.CurrentFrame` is `nil` over the bridge, so `FlowView.SetPos` does **not** work). Tool IDs used: `RectangleMask`, `Background`, `TextPlus`, `Merge`.
- **Set values:** `tool.SetInput("Width", 0.5)` etc. — scalar inputs work directly. `TextPlus` uses `StyledText`, `Size`, `Red1/Green1/Blue1`. `Background` uses `TopLeftRed/Green/Blue`. Avoid Point-type inputs (e.g. mask `Center`) — leave them at the 0.5,0.5 default (already centred).
- **Name nodes:** `tool.SetAttrs({"TOOLS_Name": "Background_Fill_D01"})`.
- **Connect:** `dest.ConnectInput("EffectMask", maskTool)`, `merge.ConnectInput("Background", x)`, `merge.ConnectInput("Foreground", y)`, `MediaOut1.ConnectInput("Input", finalMerge)`.
- **`GetToolList()` returns a dict keyed by int** — iterate `.values()`, not the object directly.
- **Grab a still to show Samuel:** `timeline.SetCurrentTimecode(timeline.GetStartTimecode())` → `resolve.OpenPage("color")` → `still = timeline.GrabStill()` → `project.GetGallery().GetCurrentStillAlbum().ExportStills([still], out_dir, "prefix", "jpg")`. The still is **post-grade** — a heavy clip grade (blur/glow) will distort the card; say so, do not present it as the card's true look.
- **Courtesy:** restore Samuel's context at the end — `SetCurrentTimeline` back to his working timeline, `OpenPage("edit")`.

### The house-style card, built node-by-node (step-6 proof)
Bordered card = larger light RectangleMask→Background behind a smaller dark RectangleMask→Background, merged, text merged over, whole thing merged over `MediaIn1`, into `MediaOut1`. This **stacked-rect** border avoids the uncertain hollow-mask input IDs (`Solid`/`BorderWidth`) and is guaranteed to render. The **true house method** (Instance of the mask with `Solid=0`, `BorderWidth ~0.00184`, plus a NeoLightSweep Pro shine) is the fine-tuning layer Samuel adds — Fusion **Instance** tools and third-party macros (NeoLightSweep, NeoBevel, NeoAnim, NeoTextMotion, MosaicBlur) were **not** attempted over the bridge and remain unproven programmatically. Worked accent: border `#ff5a1f` = (1, 0.3529, 0.1216), fill = (0.1059, 0.0353, 0.0118).

## 2026-09-21 — Resolve 21 changed the HTML→Fusion picture
`get_whats_new since=20.0`: Resolve 21 (2026-06-03) added **native OGraf HTML graphics** and **native Lottie** on the Edit and Fusion pages, a **new Macro Editor** (publish Fusion macros to edit effects), **Krokodove + 100+ motion-graphics tools**, and new scripting APIs (timeline clip selection, get-timeline-from-mediapool-entry in 21.0.4, Speech Generator, IntelliSearch, speaker detection, disable-all-background-tasks). OGraf is a **preview** path only — it renders HTML, not editable nodes — so it does not replace step 6, but it may accelerate step 5. Test before relying on it.

## 2026-09-21 — Sync (SOP step 1) proven on real footage; ffmpeg installed

Test project **"Claude tests"** (Samuel's dedicated test project), footage at `C:\Users\repzy\Desktop\Video edits\Routerise\1. Taking a step back from Claude (and why you should too)\`.

- **`MediaPool.AutoSyncAudio(...AUDIO_SYNC_WAVEFORM)` returns `False` when the camera scratch audio is dead.** Verified: camera track −77.8 dB mean / no speech; mic −29.8 / −4.9. Both clip orders returned False. Treat `False` as "camera audio unusable → go to motion sync", not as a bug. Settings keys: `resolve.AUDIO_SYNC_MODE`, `AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO`, `AUDIO_SYNC_CHANNEL_NUMBER`, `AUDIO_SYNC_RETAIN_VIDEO_METADATA`; modes `AUDIO_SYNC_WAVEFORM/TIMECODE/IN/OUT/MARKER`.
- **Motion-correlation fallback works:** video motion (ffmpeg `tblend=all_mode=difference`+`signalstats` YAVG @20Hz, `-hwaccel cuda`) × mic RMS envelope (@20Hz from `-ar 2000 -f s16le`), plain-Python FFT cross-correlation. Result **+4.000 s ≈ 120 frames @ 29.97, z = 7.6** — matches the SOP's prior ~4.17 s / 125 frames for this shoot. Script: `motion_sync2.py` in this session's scratchpad (fold into the `routerise-cut` skill). **Only the first 6 min needed** — the offset is one constant; align a section, the whole clip follows (Samuel's rule).
- **ffmpeg installed** 2026-09-21: Gyan build **9.0.1** via winget (`Gyan.FFmpeg`), at `C:\Users\repzy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_..._8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\`. Not on the default shell PATH. **No ffmpeg/numpy/scipy before this**; stock Python 3.14 only. When the agent runs as a subagent, this media folder needs a grant in `.claude/settings.json` (AGENTS.md §10) — not granted yet.
- **Not yet done:** ear-check the +4.0 s on a timeline; decide how to *apply* the offset (media-pool linked audio vs. mic on A1 at the offset, per the SOP target: A-roll V1, mic A1 at +6 dB).

## Open, to verify next
- `ImportFusionComp(path)` with a Python-generated `.comp`/`.setting` file — his actual "paste `.setting`" method, automated. Not yet tested; would sidestep per-input datatype fiddliness.
- Whether NeoLightSweep Pro / the Neo* macros can be instantiated via `AddTool` or only via paste-from-`.setting`.
- A clean, un-graded render of a card (grab from a clip with no heavy grade, or render the Fusion output directly).

## 2026-09-22 — Delivered-projects record built; the archive holds client-history detail the current Brain doesn't

Built [[03-Areas/video-editing/delivered-projects|delivered-projects]] on Samuel's request, no Resolve touched.

- **`03-Areas/finances/income.md`'s batch table (May 5 / June 4 / July 2 / August 4) is a count, not a record** — no video names or per-video dates exist anywhere for that period. Rows had to go in as `name unknown`. If Samuel wants this filled in retroactively, it isn't recoverable from the Brain as it stands — it would need his memory or the client folder names.
- **The archived Accountability Engine (`08-Archive/accountability-engine/context/`) has real per-video detail income.md doesn't**: named jobs, delivery dates (some, e.g. from TickTick), and a whole second client-naming scheme ("Andy", "Alex", "Client #1/2/3") that doesn't cleanly map onto income.md's "Alex + one unnamed second end client" story. `ledger.md` + `ledger-notes/*.md` are prose (grep only, per this agent's profile); **`site.json` in the same folder is structured** (`history` array with `name`/`delivered`/`verdict`/`fee_usd` fields) — worth grepping first next time money-history questions come up, it's denser and cheaper than the prose ledger.
- **Don't force a reconciliation across sources that disagree.** Income.md (Samuel-confirmed 2026-09-20) says one end client (Alex) plus one ended second end client (USD 175, unnamed). The archive independently names "Andy" at USD 333.33 (Alex's rate, not 175) as a distinct "old client." Rather than pick one, both are recorded and the conflict is flagged as open — this is the same tension [[03-Areas/video-editing/clients/routerise|Routerise]] already carried unresolved from 2026-09-20. Guessing which is right would have put a wrong number in a file finance treats as ground truth.
- **Don't add a named row just because a name exists.** Two more names surfaced ("Client #1" delivered 2026-08-26, "Client #2" delivered 2026-09-02) that could plausibly be 2 of the August batch's 4 — but nothing says which, and adding them as new rows risked double-counting against income.md's confirmed count of 4. Left out, flagged instead.

## 2026-09-23 — Where Resolve crash evidence lives, and what the recurring crash is

- **Evidence, all read-only:** `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\logs\davinci_resolve.log` (+ `.1`–`.5`, ~2 MB each, rolled; format `[thread] | category | LEVEL | YYYY-MM-DD HH:MM:SS,ms | msg`, local WAT time). `Support\crash_archive.txt` has one entry per crash (time, uptime, build) but only raw addresses, no symbols. The **faulting DLL comes from the Windows Application event log** (`Application Error`, ID 1000). `mcpb.log` timestamps are UTC. Memory prefs are in `Preferences\config.dat` (`Local.Resource.ResolveMemoryPercentage = 51`, `FusionMemoryPercentage = 42`). Parse with a script, never read the logs into context.
- **The recurring crash (Resolve 21.1.0.14):** `fusionsystem.dll`, `0xc0000005`, offset `0x30c290`, same WER fault bucket every time since 2026-09-14 (on 20.x/21.0 it was offset `0x24c6b0`). It is Fusion's engine, not the GPU driver or RAM. It fires when render cache makes Fusion render every frame of every comp in the background.
- **What sits next to it in the log:** Fusion nodes fed nothing (`MediaIn1 cannot get frame for time N`, `MosaicBlur1 cannot get Parameter for Source`, earlier `Background2_1_3_2_5_1 cannot get mask image`), `IO | ERROR | Failed to read frame … CacheClip\<project-uuid>\…` (corrupt cache left by the previous crash, which makes the project re-crash minutes after reopening), and `Fusion | WARN | Low GPU memory … allowed -NNNN MB` (Fusion out of the RTX 3060's 11.6 GB VRAM; a 3840×2160 desktop runs on the same card).
- **Not the cause today:** system RAM (no Resource-Exhaustion events since 2026-09-07, when Resolve hit 58 GB of commit), disk space (C: 212 GB free), MCP scripting (only handshakes in `mcp.log`). Older crashes in `lua5.1.dll`/`fusionscript.dll` (2026-09-01 to 09-07) are scripting crashes, a different bug.
- **Project UUID ↔ cache folder:** the autosave line `Incremental backup to …/Resolve Project Backups/<uuid>/` names the project's UUID; its render cache is `C:\Users\repzy\Videos\CacheClip\<uuid>\`. `$7M Founder…` = `9e0c3aa8-c877-4956-86d4-01c783c9c848`.
- **Resolve writes its own minidump** to `Support\logs\<uuid>.dmp` (older ones move to `Support\logs\LogArchive\`) even when Windows logs no `Application Error` event and `crash_archive.txt` has an empty stack. `03-Areas/video-editing/scripts/resolve_crash_dump.py` reads it with stock Python: exception code, module+offset, the address read (0x0 = null pointer), and a heuristic stack. Check the dump first; it is the only source that names the module for every crash.

## 2026-09-23 (evening) — The render-cache crash is a GPU timeout (TDR); how to cache a heavy timeline safely

- **Root cause, proven by a controlled run:** Resolve holds ~8 GB of the RTX 3060's 12 GB at idle. A heavy Fusion comp pushes Fusion's allowance negative (`Low GPU memory … allowed -2381 MB`). A CUDA job then passes Windows' 2-second TDR watchdog (`cudaErrorLaunchTimeout (702)` in the log, `nvlddmkm` event 153 in the System log), the driver resets, and Fusion null-reads at `fusionsystem.dll+0x30c290`. Corrupt cache and Magic Mask make it worse but aren't required: it crashed on a clean cache with no Magic Mask in the comp. `TdrDelay` is unset (2 s). The fix is Samuel's to apply (system setting): TdrDelay/TdrDdiDelay = 60, then reboot.
- **Check the System log for `nvlddmkm` 153 first** on any Resolve crash. If one sits within seconds of the crash, it's a GPU timeout.
- **The cache folder name is the timeline item's `GetUniqueId()`**: `CacheClip\<project uid>\<folder>\<item uid>\<uid>\SourceOne\<frame>.dvcc`, one file per frame. So progress per clip, and which clip was caching at a crash, can be read from disk. `scripts/resolve_cache_watch.py` does it.
- **A cache flag set by script needs a wake-up:** `SetFusionOutputCache(resolve.CACHE_ENABLED)` (strings like "On"/"enabled" return False). The background cacher ignores it until Render Cache goes None → page switch → User. `perfRenderCacheMode` values: `none`/`smart`/`user`.
- **Only adjustment clips take the layers below as input.** Fusion Composition generators and Fusion clips render standalone. When deferring a heavy clip, also defer the adjustment clips stacked above it.
- **Closing Chrome etc. frees ~0.5 GB at most.** The VRAM is Resolve's own. Don't lead with "close your browser".
