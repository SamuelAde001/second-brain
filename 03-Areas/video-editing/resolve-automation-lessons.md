---
type: knowledge
area: video-editing
status: active
updated: 2026-09-28
source: manual
tags: [resolve, fusion, scripting, crashes, lessons]
---

# Resolve automation lessons

What the Editor learned driving DaVinci Resolve and Fusion by script, and why Resolve crashed or hung. Moved verbatim from the [[07-Agents/video-editor/memory|Editor's memory]] on 2026-09-28; entries keep their original dates. **Read before scripting Resolve or Fusion.** New technical lessons go here, newest at the bottom. Back to [[03-Areas/video-editing/video-editing|Video editing]] · crash fixes also in [[03-Areas/video-editing/troubleshooting|troubleshooting]].

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

## Open, to verify next
- `ImportFusionComp(path)` with a Python-generated `.comp`/`.setting` file — his actual "paste `.setting`" method, automated. Not yet tested; would sidestep per-input datatype fiddliness.
- Whether NeoLightSweep Pro / the Neo* macros can be instantiated via `AddTool` or only via paste-from-`.setting`.
- A clean, un-graded render of a card (grab from a clip with no heavy grade, or render the Fusion output directly).

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

## 2026-09-26 — Scripting a heavy 3D comp hangs Resolve: pass-through the renderer first

- Setting ~80 Transform3D inputs in one `run_script` call on a live comp (Software `Renderer3D` fed by a `MagicMask` cutout, 20 image planes) blew the 30 s limit, then Resolve went **Not Responding** and closed. There was no dump, no `nvlddmkm` 153 and no Application Error. Each `SetInput` re-renders the viewed comp.
- **Before bulk edits on a 3D comp:** set `Renderer3D` and `MagicMask` to pass-through (`TOOLB_PassThrough`), write in small calls (one ring per call), then turn them back on. Never leave `comp.Lock()` / `StartUndo` open across a call that could time out.
- Icon-ring method (Samuel's): each icon `Transform3D` gets Scale, Translate.Z = R, Pivot.Z = −R, Rotate.Y = i·360/n, which puts the ring centre at the origin. The ring's own Transform3D spins it about its default pivot.
- **Correction (same day):** in Transform3D the pivot offset is scaled by the tool's own Scale, so Pivot.Z = -R with Scale 0.075 gives a ring 0.02 wide. Place icons directly (Translate X = R·sin θ, Z = R·cos θ, Rotate Y = θ). Camera3D here (Fit=Height, URSA 4K gate) framed a width-1 plane at 57% from the AoV maths. Measure the render and scale camera Z instead of trusting the AoV formula. The final values that worked are in log.md, 2026-09-26.
- **Glow on one 3D object only:** give it a unique Material ID and set every other material to 0, because Fusion defaults ImagePlane3D to 1 or 2. Turn on the renderer's MaterialID channel, then use ChannelBooleans (RGBA ← `Material ID FG`, combo value 21) → ColorGain → Glow → additive Merge. Icons and cutouts occlude it correctly. `Glow.Glow` is steeply non-linear: 0.6 is barely visible, 0.9 is a good neon, 1.0 blows out.
- **Linear keyframes by script:** `AddModifier(id,"BezierSpline")`, `SetInput(id,v,frame)`, then `spline.SetKeyFrames({t0:{1:v0,"RH":{1:..,2:..}}, t1:{1:v1,"LH":{..}}}, True)` with handles at thirds. `comp.CurrentTime = n` works over the bridge.

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

## 2026-09-26 — Four-box build: what worked
- **Fusion polyline points** (PolylineMask / PolylineStroke) are centre-origin, x in width units, y in height units: X = px/1920 − 0.5, Y = 0.5 − py/1080. Verified by render.
- **PolylineStroke** inputs: `WriteOnStart/WriteOnEnd` (draw-on), colour `PaintApplyColor.Red/Green/Blue`, `CircleBrush.Size`, `Spacing`. PolylineMask write-on is `WritePosition/WriteLength`. ResolveFX MosaicBlur is `ofx.com.blackmagicdesign.resolvefx.MosaicBlur`, and `PixelFrequency` lower = bigger blocks (100 hides a 128 px logo; 200 doesn't).
- **Animating a macro's control from a generated file:** put a BezierSpline inside the macro's `Tools` and point the inner tool's input at it (Opacity: `Op.Gain`; Light Sweep: `Rectangle1.Center`). It shows as animated on the macro's control.
- A 454 KB paste (183 nodes, 13 macros) into his heavy comp inside `comp.Lock()` took under 60 s with no hang.
- `ImportFusionComp` on a scratch Fusion Composition replaced its comp (count stayed 1), so re-importing to iterate is fine there.

## 2026-09-27 — Wiring a big paste into a live, viewed comp hangs Resolve
- The 240-node paste into the circle comp went in fine (under 60 s). The **wiring call** after it (38 `ConnectInput`s + Loader clip resets inside `comp.Lock()`) timed out, and Resolve went Not Responding for 5+ minutes. The playhead was parked on that clip, with the Color page open, so every connection re-rendered the viewed frame through 16 Neo macros and 5 NeoTextMotion fuses, with VRAM at ~11 of 12 GB. The same wiring on a scratch timeline ran in seconds.
- **Next time:** before pasting into a live comp, move the playhead off the clip and switch to the Edit page. Wire in small calls (one pill per call), with no `comp.Lock()` held across a call that can time out. Connect `MediaOut1` last. Or ship the paste pre-wired where possible: plain tool-to-tool links survive a paste; only links into and out of macros and to his existing tools need a script.
- **His NeoAnim and NeoTextMotion can be copied from his own comps and re-timed by value:** NeoAnim `GlobalAnim.InOffset` / `InLength` are comp frames. `GlobalXF.Center` places the whole group, so build it at frame centre. NeoTextMotion `InOffsetF` / `InLengthF` are comp frames, and `Justify = 0` left-aligns with `Center` as the left edge. The AnimCurves modifiers outside the NeoAnim macro survive an import once they are renamed per instance. Verified on the scratch render.
- When copying tools out of a `.comp`, only names inside a macro's `Tools = ordered()` section are inner tools. Scanning every 4-tab line also catches input names (`StyledText`, `Size`…) and renames them, which silently breaks the tool.
- **Confirmed the same day:** wiring in small calls, with no Lock and the output connected last, finished instantly on the same 240-node paste. Samuel doesn't want page switches: *"why do you keep going to the fusion page?"* Never call `OpenPage` without telling him first. Still grabs need the Color page, so check frames in his own viewer instead, or ask him. Narrate each step as it happens (*"Tell me what you are doing as you go"*).
- **See his viewer without switching pages:** `powershell -File 03-Areas/video-editing/scripts/fusion_view.ps1 -Out <png> -Crop viewer -Scale 0.75`. To look at a given frame, set `comp.CurrentTime = n` over the bridge first. If he changes the viewer layout, re-save the area with `-SetViewer x,y,w,h` (fractions of the window). Use this instead of GrabStill on the Color page.
- **Loaders pasted by script DO need the Clip re-set** (confirmed 2026-09-27): skipped it, and icons rendered empty while `arrow-right.png` masks rendered as white boxes. Always re-set every pasted Loader.
- **Correction (2026-09-27): the FlowView IS reachable when the comp is open on the Fusion page.** `comp.CurrentFrame.FlowView` → `GetPosTable(tool)` (grid units, x step 1 = 110 px) and `SetPos(tool, x, y)` work, and `FlowView.Select()` clears the selection (pasted nodes stay selected and draw their on-screen controls over the viewer until then). So nodes can be arranged by script after a paste. Pasted positions land offset from the file's positions, so align by reading his anchors (`Merge1`, `MediaOut1`) and shifting my whole group by one offset.
- **Deleting nodes in his comp is blocked by the Claude Code auto-mode safety check** (irreversible), even when he says to finish; one or two batches may pass, then it stops. Don't plan around deletes. Paste a new set with a name tag (`gen_circle_pills.py <scratch> _B`), leave old leftovers unconnected and parked in one block, and tell him where.
- **Grouping by script (2026-09-27):** Fusion's Ctrl+G is the action `AddTool` with `{"id": "GroupOperator"}` (found through `fusion.ActionManager.GetActions()`: match on `.Name == "Group"`, then read `.Info`). `FlowView.Select(tool, True)` followed by `comp.DoAction("AddTool", {"id": "GroupOperator"})` created `Group1` from 139 selected tools. Resolve then hung on the next call (walking the whole tool list and `GetChildrenList`). Next time, group fewer tools per action. Or don't group leftovers at all: move them with `SetPos` into a compact block next to the tree, which never hung.
- **Standing rule (2026-09-27):** *"Whenever Davinci is unresponsive, tell me immediately."* After a `run_script` timeout, check `(Get-Process Resolve).Responding` once. If it's False, report straight away (the last call, the last save time). No multi-minute watching before telling him. Rule in [[03-Areas/video-editing/ways-of-working|ways of working]].
- **Never decide which nodes are mine from a snapshot of his nodes taken earlier (2026-09-27).** He keeps working in the comp between my steps. A "not in his original list" filter swept 13 of his new nodes into my leftover block. Always select mine by my own generated names list (`names.txt` from the generator, plus any tag), never by exclusion.
- `FlowView.SetPos` / `GetPosTable` are in **grid units** (1 x unit = 110 px of the .comp `Pos`, 1 y unit ≈ 33 px). Passing pixel values throws nodes thousands of units away.

## 2026-09-27 — Neo Anim from the fresh .setting, set by script
- The `.setting` holds the macro **plus 12 top-level AnimCurves modifiers outside it**. Copy and suffix all of them, or the controls go dead. PreXF's `Input` points at a `Text1` that doesn't exist; strip it.
- Fresh defaults animate everything (size 0→1, angle 90→0, blur 25→0, fade, rise from below) and **Out is on (50 frames, ending at the comp's end)**. On a short comp the out animation eats the in: turn `Out` off unless he wants one.
- The Off buttons only do `TOOLB_PassThrough = true` on the inner `NASize` / `NAAngle` / `NABlur` and set `ToggleControls.<X>Box = 0`. Doing the same by script is the macro's own off state, so his buttons still switch them back on.
- Slide direction is the `Vector1` Angle (published `Angle`): 0 = comes from the right, -90 = from below (default), -180 = from the left. Distance is `StartOffset` (frame widths).
- **Its fade is a Stencil merge against a 1920×1080 Background, so pixels outside the frame are never hidden.** Anything that sticks out of the group frame (badges above the top edge) shows before the start. Fix inside the macro: `PreXF` Center y 0.25 and `FinalXF` y 0.75 (both unpublished), which keeps his published Global controls at their defaults.

## 2026-09-27 — Card design A build notes
- **Samuel works in the comp while I build.** A node I read an hour earlier can be gone (he deleted `Transform4` mid-task). Re-read the chain before any step that depends on it, and never "fix" a layout change that could be his.
- A Background with alpha 0 but white RGB still **adds** white (Fusion colours aren't premultiplied there). To hide a fill, zero the RGB as well.
- Background `Type` takes the strings "Solid", "Horizontal", "Vertical", "Corner", "Gradient". Vertical runs across the whole frame, so a card in the top 42% only gets part of the ramp; a negative bottom colour pushes the ramp harder inside the card (the card's own pixels stay positive).
- **Neo Bevel's inner tools are written at column 0** in its `.setting` (`\nDisplace1 = …`, no tabs). Match tool names with `\n\t*`, not `\n\t+`, or they paste unsuffixed. Its controls: `Intensity` (default 25, turns an orange border nearly white; 10 keeps it orange), `LightAngle`, `Spread`, `Blend`.
- Text+ outline-only number: `Enabled1` 0, `Enabled2` 1, `Red2/Green2/Blue2`, `Thickness2` (0.03 reads bold at Size 0.125).
- A mask clipped to another mask's shape: plug the second mask into the first's `EffectMask` and set the first's `PaintMode` to "Multiply".
- **Design previews:** the Browser pane only snapshots local files and its screenshots time out. Serve the folder with `python -m http.server` and grab stills with headless Edge (`msedge --headless=new --screenshot=… --window-size=… --virtual-time-budget=4000 URL#f=80`); a `#f=N` hash freezes the preview on frame N.
- **Position elements at their source, never with a Neo Anim's Global Center (Samuel, 2026-09-27).** *"don't use the neo anim to bring them down to the center, centralise them and space them well"*: move each element's own mask/text/merge centres, and keep the Neo Anims at Global Center 0.5/0.5 so they animate only. Build cards inside the frame from the start; then the out-of-frame fade fix (PreXF/FinalXF) isn't needed.
- `fusion_view.ps1 -SetViewer` fractions don't match a full-window capture's fractions one-to-one (the crop landed ~230 px lower at 3862×2110). Set the area, capture once and adjust before trusting it.

## 2026-09-27 — Never position with a Merge
- **Samuel: "NEVER EVER Reposition anything with a Merge node."** Merges stay at Center 0.5/0.5, Size 1, Angle 0. Position and scale live on a Transform before the merge (Loader → Transform → Merge), or on the element's own Center. My generators used `Merge_Logo` Center/Size; fix that in `gen_tool_boxes.py`-style builds before reusing them.
- A small Loader (1024² tile) merged over a 1920×1080 canvas doesn't land 1:1 here: measured ~1.41–1.44× in both size and Transform offset, plus a constant vertical lift. Before the ResolveFX DropShadow was removed it mapped differently (the OFX output changes the image the Merge sees). Don't compute tile offsets from pixel maths alone. Set them, look in his viewer against a reference (the ring) and correct.

## 2026-09-27 — Five-window build in an adjustment clip (M02)
- **Page switches are fine (Samuel, 2026-09-27: "You can switch pages, I am not stopping you from doing that").** This replaces the earlier "never call OpenPage without telling him first". Still say it when it happens.
- **`comp.Paste()` and `DoAction("AddSetting")` only work on the comp open on the Fusion page** (`resolve.Fusion().CurrentComp`). On a comp fetched with `GetFusionCompByIndex` while on the Edit page, Paste returns False. Put the playhead on the clip, `OpenPage("fusion")`, check that `CurrentComp` has the same `COMPS_Name`, then paste.
- **A Loader in Resolve's Fusion can't read a .mov** (Clip_Length 0, Width 0, renders nothing). For rendered videos: import them into the Media Pool, then `AddTool("MediaIn")` + `SetInput("MediaID", mpi.GetMediaId())`. If `ClipName` still reads the host clip ("Adjustment Clip"), set MediaID to "" and back.
- **On the Fusion page, `AddTool` auto-connects to the selected node** and inserts Merges (Merge1–9 appeared). Call `FlowView.Select()` (clear) before every AddTool batch, then list every Merge afterwards.
- **Correction: the fresh `Neo Anim.setting` has every animation stage off** (NASize / NAPosition / NABlend / NABlur / NAAngle / NAMotionBlur all `PassThrough = true`), so it does nothing until switched on. Switch one on the way its On button does: `SetAttrs({"TOOLB_PassThrough": False})` on the inner tool (`FindTool("NASize_W1")` works) plus `ToggleControls_W1.SetInput("Size", 1)`. Out is on in the file, so turn it off in the text.
- Scaling with Neo Anim `GlobalSize` and positioning with a Transform after it works cleanly when the source element is centred in the frame: the macro scales around the centre, and the Transform moves the result.
- **`render.py` deletes every earlier render with the same beat id** (`<id>_*`) before it writes. Re-rendering M02a–e as .mp4 removed the .mov files the Media Pool clips pointed at. When the old files are still in use, give the new version a new id.
- **`TimelineItem.DeleteFusionCompByName` fails on a clip's only comp.** To reset an adjustment clip, delete your own nodes (select them by your own name pattern) and wire MediaIn1 → MediaOut1.

## 2026-09-28 (night build, Route Rise #3 Visuals v2) — placing and building comps by script

- **`InsertFusionCompositionIntoTimeline()` (and the other Insert* calls) RIPPLE the whole timeline** (insert edit on every track, splitting V1/A1/V4/V6). Two inserts pushed Cut v6 by 86 + 46 frames; recovered with Resolve Undo (Ctrl+Z) via computer use, checked against *Visuals v1* (an untouched copy). **Never use Insert* on a cut timeline.**
- **Safe placement:** a transparent base clip (`Graphics/Visuals v2/Fusion base 1080 transparent.mov`, 60 s PNG-in-MOV) placed with `MediaPool.AppendToTimeline([{..., trackIndex, recordFrame}])` (an overwrite, no ripple), then `TimelineItem.ImportFusionComp(path)` onto it. Assert the timeline length is unchanged after every placement. A clip at a different frame rate (29.97 B-roll) needs `endFrame` rounding checked; re-place if one frame short.
- **AppendToTimeline onto an occupied track fails silently** (returns an item whose GetStart() is None). V4 is full of his disabled Tella pieces; use an empty track.
- **Links into and out of Neo macros don't survive ImportFusionComp:** wire every macro input AND every merge that takes a macro's output with `ConnectInput` after import (`pk.py` stack() does this).
- **Fusion EllipseMask Height is in frame-width units** (use h / 1920 for an ellipse, not h / 1080).
- **Resolve caches Fusion output:** an Expression change doesn't invalidate it; nudge a real input (set a value and set it back) before checking.
- **Viewer captures lag one request** even with a playhead nudge; keep Resolve restored (not minimised) and read results knowing the previous frame may show.
- **Neo Bevel's column-0 inner tools break the macro slicer:** a comp with it imports empty. Use Light Sweep, or fix the slicer first.
- **Retargeting his reveal:** his Clay reveal (Cut v6 V3 723) = per-card Neo Anim -> Opacity macro -> ColorCorrector (desaturate) + MosaicBlur on the unrevealed contents + Transform10 pan/zoom (Path1, Size 1->1.143 over 44 f). Retarget by reconnecting his own splines (Op_1Gain, ColorCorrector1_1Saturation, MosaicBlur_Content1Blend) and re-aiming with a Pivot expression driven by `Path1.Displacement` (x' = Pivot + (x - Pivot)*Size + (Center - 0.5)). Script: job folder `Graphics/Visuals v2/rr3.py`.
- **Builders for his look:** `Graphics/Visuals v2/pillkit.py` (gen_circle_pills helpers) + `pk.py` / `pk2.py` (pill, arrow, tick, title, BGORANGE, his Moving dashed line, ringed hub, image card, Down fade) and one `build_*.py` per beat.

- **2026-09-29: never call `DuplicateTimeline` on a heavy timeline through the MCP.** On Route Rise #3 (77 Fusion items) it blocked Resolve's UI thread past the 30 s script timeout, memory climbed 4.8 → 17 GB, and Resolve had to be restarted. For A/B render tests, ask Samuel to toggle the track himself, or test in a separate small project.

