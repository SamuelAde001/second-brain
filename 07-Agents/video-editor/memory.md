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

## 2026-09-23 (night) — PC lag while rendering is GPU contention, not CPU/RAM

- **Measured during a Deliver render:** GPU 100% (Resolve alone on the 3D engine), VRAM 8.6/12 GB, CPU 15%, RAM 6.7 GB free, disk idle. The desktop (3840×2160) is composited on the same RTX 3060, so when Resolve holds the card, the whole PC stutters.
- **With `TdrDelay` = 60, Windows lets a long GPU job run up to 60 s before resetting.** A GPU job that used to crash Resolve after 2 s now freezes the desktop until it finishes. That's the cost of the crash fix. Lowering it brings the crashes back.
- **Raising Resolve's CPU priority, or lowering it, does nothing for this.** CPU isn't the bottleneck. Check `nvidia-smi` and the `\GPU Engine(*)\Utilization Percentage` counter first.
- **Samuel is putting TDR back to the default after tonight's render (2026-09-23).** Before any heavy Fusion caching or rendering, read `TdrDelay` (read-only registry). If it's unset, the 2 s watchdog is back and the §7 crash is expected on the heavy comps. Say so up front rather than rediscovering it from a crash.
- **Correction (2026-09-24):** TDR isn't going back to the default. Samuel chose **10 s** (`TdrDelay` = `TdrDdiDelay` = 10). Before heavy Fusion caching, read the value. At 10 s, a comp that needs longer than 10 s on the GPU can still crash with the §7 signature (`cudaErrorLaunchTimeout (702)` + `nvlddmkm` 153). If that happens, cache that clip alone.

## 2026-09-24 — Setting up a Routerise job from the card (first run: 4 AI Tools)

- **Samuel, 2026-09-24:** *"Anything we work on for this project would be part of the editor agents training on how to do things."* So every step that worked got written into [[03-Areas/video-editing/sops/routerise-job-setup|Routerise job setup]], and the tools went into `03-Areas/video-editing/scripts/`.
- **Where things live:** the idea doc is on Route Rise Media's Notion (connector 404s; read it in Samuel's Chrome, signed in). Footage is in a link-shared Drive folder owned by `alex@frontal.so`. The screen recording is on **Tella**, reached through a one-line Google Doc called "Screenshare".
- **The Drive connector can't list children of a folder shared with him**, and shared folders aren't on his G: mount. The in-app browser lists a link-shared folder without sign-in; file IDs are on `[data-id]` elements.
- **Download speed:** one Drive connection ~2–3 MB/s; 10 parallel ranges ~5 MB/s when alone. Two big downloads at once share the line.
- **Tella:** the Download dialog calls `prod-stream.tella.tv/export?...` and `export/list?story_id=…` returns `downloadUrl` when the render is done. A 24-minute story at 4K = 1.08 GB, 3840×1912 30 fps. The only streamed variant is 1920×956 at 1.2 Mbps, too soft to edit from.
- **Resolve template:** the `Routerise` project folder holds a `Project Template` project (Raw vids, Screen records, Music, SFX library, Assets…, 1080p 23.976). A new job = `ExportProject` it to a scratch .drp, then `ImportProject(path, "<card title>")`.
- **Sign convention check on the old motion-sync script (2026-09-21):** it computed `IFFT(F_motion · conj(F_mic))`, which peaks at `mic_start − cam_start`. So its printed "+4.000 s, mic started before video" actually means **the mic started 4 s after the camera**. The SOP's "+4.0 s" was never ear-checked. `av_sync.py` uses the opposite product and was tested on synthetic data: positive = mic started earlier. Trust `av_sync.py`, and ear-check the first placement anyway.
- **Samuel's rule on Resolve projects (2026-09-24):** never copy `Project Template`. A copied project keeps the template's created date in the project list. Always `CreateProject` fresh and drag in the **"Folder structure template"** power bin's folders (GUI only; the API has no power bin access). His new-project defaults already match the old template.
- **The 4 AI Tools shoot:** camera scratch audio dead again (−61 dB), so dead camera audio looks like the norm for Alex's shoots, not a one-off. The mic started **9.88 s after** the camera. That's the opposite direction to what the 13 Sep label claimed. It fits the sign-error finding above: on both shoots the DJI mic was started after the camera.
- **The screen recording gets synced too, as part of setup** (Samuel's correction, 2026-09-24). The Tella export carries clean laptop-mic audio, so an audio-vs-mic cross-correlation is exact (z 14–35, 100 Hz agreed to the millisecond at both ends). Alex's Tella story had no cuts; sweep windows anyway. Watch the window-to-time mapping: with `xcorr(slice, full_mic)`, the lag *is* the mic time of the slice start. Don't add the slice start again (I did once and got times past the end of the file).

## 2026-09-24 — Route Rise #3 cut: waveform clips, frame grid, per-clip transcripts

- **Samuel's correction:** *"Why do we have places where the video cut is not aligned with the audio cut, did you use transcripts again, it must be the exact same place"*. The cut points were waveform ones. The fault was the frame grid: the DJI WAV reads as 29.97 fps (metadata, locked), the timeline is 23.976, and Resolve places audio sub-frame. **Always cut with a metadata-free lossless copy of the mic that reads at the timeline rate**, then check every A1 clip's start and duration against its V1 clip. Recipe in [[03-Areas/video-editing/sops/routerise-cut-workflow|the cut SOP]], "Frame grid".
- `AppendToTimeline` rules measured: video duration = floor(source frames × timeline fps ÷ source fps), so ask for ceil(D × source fps ÷ timeline fps) source frames. `recordFrame` places a clip exactly. `TimelineItem.AddMarker(0, …)` puts a marker at the clip's first frame. `Timeline.CreateSubtitlesFromAudio()` works by script and blocks until done (about 20 s for 9.5 min).
- **Camera–mic drift is real on a 28-minute take:** about 129 ppm. Fit a line from three motion-sync windows; one constant leaves the far end 2 frames out.
- **Per-clip transcripts:** `Folder.TranscribeAudio()` does a whole bin at once. A `time.sleep` inside `run_script` stalls it. Empty results are short words, not silence: re-transcribe joined to the next clip.
- **Alex's Tella exports are camera + screen side by side, and the screen is mostly his teleprompter.** Classify the screen before writing notes. On #3 the Railway dashboard and the 4-tool build were never on screen.
- **The video-edit-pass skill's `references/` and `scripts/` never made it into the Brain** (only the .md was copied). Phase 2 was run from the rules in the skill body, and `03-Areas/video-editing/scripts/transcript_docx.py` (stock Python) replaces `build_transcript.js`. The `docx` npm package isn't installed; Word is, and renders to PDF over COM. Windows' own PDF API (`Windows.Data.Pdf` from PowerShell) turns pages into PNGs for checking.
- Samuel declined screen control of Resolve on 2026-09-24. Verify by script, and leave the playhead on something for him to check.

## 2026-09-25 — Before handing over a cut, diff the raw transcript against the kept source ranges

- **What went wrong on Route Rise #3:** "keep the last clean take per retake cluster" dropped all four takes of the opening line, because the cluster was read as the first sentence *plus* its restarts, not as a sentence on its own. It also dropped two half-sentences inside kept clips (a list item, "ads on LinkedIn", and a clause). Samuel caught the missing hook.
- **The check (do it every time, before the transcript doc):** transcribe the whole raw mic (temp timeline + `CreateSubtitlesFromAudio`, about 60 s per 14 min; split longer takes), then for each raw line compute the share of its frames inside the cut's A1 `GetSourceStartFrame`/`GetSourceEndFrame` ranges. Every line under 50% gets read by eye: is the same content said somewhere in the cut? If not, it isn't a mistake, so put it back. Subtitle timing is loose, so a low % on a line the transcript doc shows is usually noise.
- **Always check the script's hook specifically.** Alex often records the opener several times at the very top of the take, before settling. The first line of the script must appear in the cut.
- `MediaPoolItem.TranscribeAudio()` returned True but produced nothing in 3+ minutes on the Tella clip. Use the temp-timeline subtitle route instead.
- The project note's Tella formula was written backwards: **mic t = Tella t + 270.7 s** (Tella starts 4:30 into the mic). The Railway dashboard *is* on the Tella recording. Look at frames before writing "not on screen".
- **Reading source positions back from a timeline:** `TimelineItem.GetSourceStartFrame()` floors a float (1553.9999 → 1553), so rebuilding from it moves clips a frame early. Use `round(GetLeftOffset(True))` in timeline frames; for a 29.97 camera on 23.976 that's × 1.25, for a 30 fps Tella × 30000/23976. There is no API to move or ripple-insert clips. To add clips into a cut: duplicate the timeline, clear its tracks and markers, and re-append the whole list with `recordFrame` (594 pieces in one `AppendToTimeline` call, frame-exact).
- **Rebuilding the transcript doc:** parse the previous .docx back into a `transcript_docx.py` spec (Heading1 fill = chapter hex, `F3ECFA` = prompt box, "NOTE: " = note, numId 1/2 = bullet/num), edit the lines, and shift note times by the inserted frames.

## 2026-09-25 — Cut from the synced raw with Resolve's own silence tool; don't rebuild cuts clip by clip

- **Samuel's method replaces my rebuilds:** duplicate the synced raw timeline, delete the Tella audio, select all, `Clip > Audio Operations > Ripple Delete Silence…`, then clean the leftover noise clips. Every track is cut at the same frame, so sync can't drift. My Cut v2/v3 rebuilds (placing each clip from a drift model) are what broke sync. Samuel: *"you are over complicating things"*.
- **The silence dialog's threshold isn't an ffmpeg RMS number.** Set it from the red preview on the clips. Samuel's #3 values: −33.4 dB / pre 0 / post 3 / min 2.
- **Never press Ctrl+Z to fix a small stray edit right after a script action.** Resolve's undo stack includes script operations, and it undid the whole timeline duplicate. Fix stray edits by script, or tell Samuel.
- **Samuel is fine with screen control of Resolve when he asks for a GUI step** (2026-09-25, overriding the 2026-09-24 "declined" for that task). He watches and corrects live, so narrate each step.
- Noise vs word in a short clip: level alone decides only the clear cases. Anything short with speech-level sound gets coloured for Samuel, never cut.
- **Marker colours ≠ clip colours.** `AddMarker(..., "Orange", ...)` returns False: there's no Orange marker. Marker colours: Blue, Cyan, Green, Yellow, Red, Pink, Purple, Fuchsia, Rose, Lavender, Sky, Mint, Lemon, Sand, Cocoa, Cream. AddMarker also fails on a frame that already has a marker.
- **Before ripple-deleting on a timeline with a subtitle track, delete the subtitle items first** (no ripple). Regenerate afterwards for the transcript check.
- **Flag colour on a colour-coded cut:** Orange, because it's outside the 8-section palette. Pink belongs to the Mid-CTA section.
- Subtitle export has no API route: File > Export > Subtitle… (GUI). Subtitle text can be read with `GetItemListInTrack("subtitle",1)` + `GetName()` when the GUI is blocked.

## 2026-09-25 — Samuel's verdict on Cut v6: what I got wrong, and the rules that follow

Samuel: *"you made some stupid mistakes still, left in parts that where obvously noise, you left in parts that was obviously retakes, left in some uhms"* and *"I removed most of your clutter"*. His final is 1:07 shorter than my Cut v6. Details in the cut SOP ("What Samuel still had to fix on Route Rise #3").
- **Never map a timeline-wide subtitle track onto clips by midpoint to judge retakes.** Subtitle lines span clip boundaries, so the text lands on the wrong clip. Transcribe per clip.
- **Decide, don't flag.** Last clean complete take, inside clips as well as across them. He cut every one of my "unsure" flags the way that rule says. Flags and markers are clutter to him. Keep them for content that exists nowhere else.
- **Short wordless clips between complete sentences are noise.** Cut them. My −40 dB rule was too strict.
- **He trims uhms and pauses inside clips** (2–65 frames, 30 places on #3). Resolve's transcripts can't see them. I need a filler-aware word-timed pass before I can do this.
- **The job isn't done until the uhms are out.** Silence → noise → retakes → uhms → transcript check.
- **Diffing his final against mine:** compare A1 source ranges (`GetLeftOffset(True)` + duration) of every clip against the reference cut. Covered / trimmed / removed per clip shows exactly what he changed. Worth doing on every job he finishes himself.

## 2026-09-25 — Why the TSB visuals were called mediocre (Samuel's own diagnosis)

- The TSB final (`v2.1.mp4`) includes **Samuel's corrections to Claude's 3:06–end**. It isn't Claude's work as delivered. To see what he fixed, diff Claude's original `.comp` files (`Claude Files\TSB comps\fx\`) against the comps now on the timeline.
- Claude faked effects: home-made glows instead of **NeoGlow**, "shadow boxes" instead of the **DropShadow** node. He builds depth with real nodes (NeoLightSweep, NeoGlow, DropShadow, NeoBevel, reflection). Rule in [[03-Areas/video-editing/ways-of-working|ways of working]].
- The intro is his. Ideate it on the sheet, never place visuals before it ends.

## 2026-09-25 — First visual-sheet run (Route Rise #3): what worked, what bit

- **HTML → frame-exact video works** with stdlib Python + headless Chrome over CDP (`scripts/visual-engine/`): about 6 fps per tab, 3 tabs in parallel, 59 visuals (≈ 5.5 min of screen) rendered in about 12 minutes total. The method is in [[03-Areas/video-editing/sops/visual-sheet-pipeline|the visual sheet pipeline]].
- **`AppendToTimeline` `endFrame` is exclusive.** I lost a frame on every clip the first time.
- **A scene that declares `const R` at top level silently empties the render**, because it shadows the engine's `R()`. The renderer now raises on `exceptionDetails`.
- **A re-rendered file with a new length keeps its old duration in Resolve's media pool.** Delete the item, re-import, re-place.
- **Small gaps between beats (1–8 frames) flash the A-roll** between full-frame visuals, and at the joins with the screen recording. Close them in `beats.py`.
- **ffmpeg overlay of one selected frame needs `setpts=PTS-STARTPTS`**, or it composites nothing. The `.mov` alpha was fine all along.
- **Reading the agency's Notion:** the Notion connector 404s on Route Rise pages, but "copy link" pages resolve to a public `*.notion.site` the in-app browser can read. The module pages hold their content in sub-pages (Visual stimulus / Sound design / Music) and in images (open the image URL directly).
- **YouTube in the in-app browser** plays ads, and the embed URL fails (error 153). Samuel's Chrome has no ads. Canvas `drawImage` of the YouTube `<video>` is not tainted, so frames can be exported.
- The Tella recording's screen side sits at x 1200–3683, y 154–1757 of the 3840×1912 frame. Crop it before using frames as UI.

## 2026-09-26 — Scripting a heavy 3D comp hangs Resolve: pass-through the renderer first

- Setting ~80 Transform3D inputs in one `run_script` call on a live comp (Software `Renderer3D` fed by a `MagicMask` cutout, 20 image planes) blew the 30 s limit, then Resolve went **Not Responding** and closed. There was no dump, no `nvlddmkm` 153 and no Application Error. Each `SetInput` re-renders the viewed comp.
- **Before bulk edits on a 3D comp:** set `Renderer3D` and `MagicMask` to pass-through (`TOOLB_PassThrough`), write in small calls (one ring per call), then turn them back on. Never leave `comp.Lock()` / `StartUndo` open across a call that could time out.
- Icon-ring method (Samuel's): each icon `Transform3D` gets Scale, Translate.Z = R, Pivot.Z = −R, Rotate.Y = i·360/n, which puts the ring centre at the origin. The ring's own Transform3D spins it about its default pivot.
- **Correction (same day):** in Transform3D the pivot offset is scaled by the tool's own Scale, so Pivot.Z = -R with Scale 0.075 gives a ring 0.02 wide. Place icons directly (Translate X = R·sin θ, Z = R·cos θ, Rotate Y = θ). Camera3D here (Fit=Height, URSA 4K gate) framed a width-1 plane at 57% from the AoV maths. Measure the render and scale camera Z instead of trusting the AoV formula. The final values that worked are in log.md, 2026-09-26.
- **Glow on one 3D object only:** give it a unique Material ID and set every other material to 0, because Fusion defaults ImagePlane3D to 1 or 2. Turn on the renderer's MaterialID channel, then use ChannelBooleans (RGBA ← `Material ID FG`, combo value 21) → ColorGain → Glow → additive Merge. Icons and cutouts occlude it correctly. `Glow.Glow` is steeply non-linear: 0.6 is barely visible, 0.9 is a good neon, 1.0 blows out.
- **Linear keyframes by script:** `AddModifier(id,"BezierSpline")`, `SetInput(id,v,frame)`, then `spline.SetKeyFrames({t0:{1:v0,"RH":{1:..,2:..}}, t1:{1:v1,"LH":{..}}}, True)` with handles at thirds. `comp.CurrentTime = n` works over the bridge.

## 2026-09-26 — Standing rule: "glow" means Neo Glow

- Samuel: *"always use Neo glow next time I ask for Glow"*. Any glow request uses the **Neo Glow** macro, not Fusion's stock `Glow`.
- Installed at `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\Neo folder\Neo Glow.setting` (plus `Neo Inner Glow.setting`). It's a macro, so it can't be added with `AddTool("Glow")`. Try `comp.Paste()` of the `.setting` contents or `AddTool` with its macro ID. Adding it by script is still unproven, so test it on the first use. If it can't be added by script, ask Samuel to drop it in and wire around it.
- Line thickness on a Shape3D torus = `SurfaceTorusInputs.Section`. The glow adds apparent width on top.

## 2026-09-26 — Text3D word animation: what works, what hangs
- **Follower works on Text3D over the bridge:** `text3d.AddModifier("StyledText", "StyledTextFollower")`. Its inputs are Range/FirstCharacter/LastCharacter, Order, Delay, DelayType, `DelayByCharacterPosition` (manual curve), plus the full per-character transform set (CharacterOffset, WordOffset, etc.). There's no word mode. For word-by-word, use Order = manual curve with a stepped delay per word, or a separate Text3D per word.
- **Don't chain a CLS modifier onto the Follower's `Text` input by script.** `follower.AddModifier("Text","StyledTextCLS")` inside `comp.Lock()` hung Resolve 21.1 outright (blank window, not responding). Text3D's StyledText takes one modifier. For per-word colour plus a Follower, split the words into separate Text3D nodes, or have Samuel add the CLS by hand.
- **Per-word control on one Text3D without CLS (worked 2026-09-26):** copy the node once per word (copy the inputs one by one, because `SaveSettings`/`LoadSettings` didn't carry over), keep the full string in every copy and show one word each with **Write On** (`Start`/`End`, fractions of the character count, cut at the spaces). The layout stays exact. Merge them with a Merge3D. Colour is `Red1/Green1/Blue1` (+ `RedBevel…`, `Red1Clone…`). Fade is `Opacity1`.
- **`AddModifier` drops a key at the comp's current time.** Delete any key before the intended start afterwards. **`SetKeyFrames` handle dicts didn't come back as written** (read back as relative offsets). For an exact ease, set a key on every frame.
- **Scale in the Route Rise #3 camera-tracked scene:** Text3D Size 30. Translate.X 40 ≈ 250 px on a 1080p frame. 4 units is invisible.

## 2026-09-26 — Adding a macro-heavy node group to a live comp by script
- **Paste route that works:** generate the `.setting` text in Python, `Set-Clipboard` it from PowerShell, then `comp.Paste()` (no args) inside `comp.Lock()`. This is Samuel's own paste method. `comp.Paste(dict)` is useless: `tool.SaveSettings()` returns `{"Tools": None}` over the bridge. `comp.Execute(lua)` silently did nothing. `ImportFusionComp(path)` works for testing, but it adds a new comp version to the clip, so use it on a scratch timeline, never on his clip.
- **Neo macros go in as full MacroOperator blocks** copied from `Macros\Neo folder\*.setting`. **Suffix every inner tool name per instance** (`NGBM_CB`, `Merge1_SW`), SourceOps and Expressions included, but not the `InstanceInput` control names. Without that, two Neo Glows cross-wire, and inner names like `Merge1`/`Rectangle1` collide with his own nodes.
- **Links into and out of a macro don't survive a paste or import.** Wire them after with `ConnectInput("MainInput1", tool)` and `ConnectInput("Foreground", macro)`. Macro outputs are `MainOutput1`. Controls are set by their published IDs: NeoGlow `Intensity`, Light Sweep `Input6` (intensity) and `Input3` (centre; animate it with an XYPath inside the macro).
- **Fusion units:** RectangleMask Height is a fraction of image height, but **EllipseMask Height is a fraction of width**, so a circle is W = H. Transform `Center` is an offset from (0.5, 0.5), and scaling around a point uses `Pivot`. The ResolveFX DropShadow ID is `ofx.com.blackmagicdesign.resolvefx.DropShadow`, with inputs `shadowStrength/shadowAngle/ShadowDistance/shadowBlur`.
- **A pasted Loader may render nothing until its `Clip` is re-set** (`SetInput("Clip","")`, then the path again).
- **`comp.Save(path)` relabels the comp's `COMPS_Name` to that file name.** Check the comp by its signature nodes, not its name, afterwards.
- **Read his comp's animation before timing an overlay.** His A-roll card animated 0→33, so the box keys start at 30. Read positions from a `comp.Save` copy (the FlowView is nil over the bridge) and place new groups clear of his tree.
