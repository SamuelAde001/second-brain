---
type: agent
area: video-editing
status: active
updated: 2026-09-28
source: interview
tags: [agent, memory]
---

# video-editor — memory

Append-only. What this agent has learned by doing. Newest at the bottom. Facts here were verified in action, not assumed (AGENTS.md rule 6).

---

## 2026-09-21 — Sync (SOP step 1) proven on real footage; ffmpeg installed

Test project **"Claude tests"** (Samuel's dedicated test project), footage at `C:\Users\repzy\Desktop\Video edits\Routerise\1. Taking a step back from Claude (and why you should too)\`.

- **`MediaPool.AutoSyncAudio(...AUDIO_SYNC_WAVEFORM)` returns `False` when the camera scratch audio is dead.** Verified: camera track −77.8 dB mean / no speech; mic −29.8 / −4.9. Both clip orders returned False. Treat `False` as "camera audio unusable → go to motion sync", not as a bug. Settings keys: `resolve.AUDIO_SYNC_MODE`, `AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO`, `AUDIO_SYNC_CHANNEL_NUMBER`, `AUDIO_SYNC_RETAIN_VIDEO_METADATA`; modes `AUDIO_SYNC_WAVEFORM/TIMECODE/IN/OUT/MARKER`.
- **Motion-correlation fallback works:** video motion (ffmpeg `tblend=all_mode=difference`+`signalstats` YAVG @20Hz, `-hwaccel cuda`) × mic RMS envelope (@20Hz from `-ar 2000 -f s16le`), plain-Python FFT cross-correlation. Result **+4.000 s ≈ 120 frames @ 29.97, z = 7.6** — matches the SOP's prior ~4.17 s / 125 frames for this shoot. Script: `motion_sync2.py` in this session's scratchpad (fold into the `routerise-cut` skill). **Only the first 6 min needed** — the offset is one constant; align a section, the whole clip follows (Samuel's rule).
- **ffmpeg installed** 2026-09-21: Gyan build **9.0.1** via winget (`Gyan.FFmpeg`), at `C:\Users\repzy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_..._8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\`. Not on the default shell PATH. **No ffmpeg/numpy/scipy before this**; stock Python 3.14 only. When the agent runs as a subagent, this media folder needs a grant in `.claude/settings.json` (AGENTS.md §10) — not granted yet.
- **Not yet done:** ear-check the +4.0 s on a timeline; decide how to *apply* the offset (media-pool linked audio vs. mic on A1 at the offset, per the SOP target: A-roll V1, mic A1 at +6 dB).

## 2026-09-22 — Delivered-projects record built; the archive holds client-history detail the current Brain doesn't

Built [[03-Areas/video-editing/delivered-projects|delivered-projects]] on Samuel's request, no Resolve touched.

- **`03-Areas/finances/income.md`'s batch table (May 5 / June 4 / July 2 / August 4) is a count, not a record** — no video names or per-video dates exist anywhere for that period. Rows had to go in as `name unknown`. If Samuel wants this filled in retroactively, it isn't recoverable from the Brain as it stands — it would need his memory or the client folder names.
- **The archived Accountability Engine (`08-Archive/accountability-engine/context/`) has real per-video detail income.md doesn't**: named jobs, delivery dates (some, e.g. from TickTick), and a whole second client-naming scheme ("Andy", "Alex", "Client #1/2/3") that doesn't cleanly map onto income.md's "Alex + one unnamed second end client" story. `ledger.md` + `ledger-notes/*.md` are prose (grep only, per this agent's profile); **`site.json` in the same folder is structured** (`history` array with `name`/`delivered`/`verdict`/`fee_usd` fields) — worth grepping first next time money-history questions come up, it's denser and cheaper than the prose ledger.
- **Don't force a reconciliation across sources that disagree.** Income.md (Samuel-confirmed 2026-09-20) says one end client (Alex) plus one ended second end client (USD 175, unnamed). The archive independently names "Andy" at USD 333.33 (Alex's rate, not 175) as a distinct "old client." Rather than pick one, both are recorded and the conflict is flagged as open — this is the same tension [[03-Areas/video-editing/clients/routerise|Routerise]] already carried unresolved from 2026-09-20. Guessing which is right would have put a wrong number in a file finance treats as ground truth.
- **Don't add a named row just because a name exists.** Two more names surfaced ("Client #1" delivered 2026-08-26, "Client #2" delivered 2026-09-02) that could plausibly be 2 of the August batch's 4 — but nothing says which, and adding them as new rows risked double-counting against income.md's confirmed count of 4. Left out, flagged instead.

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

## 2026-09-26 — Standing rule: "glow" means Neo Glow

- Samuel: *"always use Neo glow next time I ask for Glow"*. Any glow request uses the **Neo Glow** macro, not Fusion's stock `Glow`.
- Installed at `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\Neo folder\Neo Glow.setting` (plus `Neo Inner Glow.setting`). It's a macro, so it can't be added with `AddTool("Glow")`. Try `comp.Paste()` of the `.setting` contents or `AddTool` with its macro ID. Adding it by script is still unproven, so test it on the first use. If it can't be added by script, ask Samuel to drop it in and wire around it.
- Line thickness on a Shape3D torus = `SurfaceTorusInputs.Section`. The glow adds apparent width on top.

## 2026-09-26 — What Samuel changed in my four-box build (the gap to close)
- I built each element as a separate over-comp merge. He groups each family onto its own transparent canvas and moves the whole content layer over a static background. **Design the group structure first, then the elements.**
- My timing was about twice as slow (18-frame moves, 8-frame stagger). His: 8-frame moves, a stagger of about 4 frames, lines in about 6 frames.
- I drew right-angle lines with 4 points. His lines have 2 points, are curved, and all come from one point on the speaker's card.
- One shine for the set, not one per item. The sweep is narrow (about 0.07). No box drop shadows.
- He added a title and question pills, so the visual previews the segment. **A visual should say what the section is about, not only show the items.**
- He set MosaicBlur back to 200 (his value) from my 100.
- Reading a comp he edited: `comp.Save()` to the scratchpad, then parse top-level tools (`\n\t\t(\w+) = ([\w.]+) {`) and their 4-tab `Input { SourceOp }` links. It's cheap, and it shows exactly what he restructured.

## 2026-09-27 — UI demos: focus on adjustment clips, built by API
- Samuel's rules (full screen UI, no motion graphics, focus on an adjustment clip) are in [[03-Areas/video-editing/ways-of-working|ways of working]]. Tools: `scripts/ui-focus/` (README there).
- **`ImportFusionComp` returns None on an adjustment clip** (works on a video clip). Build the nodes by API instead: `AddTool`, `AddModifier(inp, "BezierSpline")` + `SetKeyFrames({t:{1:v}})`, `AddModifier("Center","XYPath")` for points.
- **Connect `MediaOut1` after `comp.Unlock()`.** Wired inside the Lock, the Edit page kept showing the untouched frame although every input read back correct.
- The sandbox can't read files and `fusion.GetClipboard()` gives no text. Data route that works: write a `.comp` holding one Note with the JSON in `Comments`, `ImportFusionComp` it onto a scratch video clip, read `FindTool("DataNote").GetInput("Comments")`.
- `InsertGeneratorIntoTimeline("Adjustment Clip")` uses the timeline In/Out (`SetMarkInOut(a, b-1)` → exact a–b) and the **patched destination track**; the patch has no API. Move it in the GUI with mouse down / small moves / mouse up (a plain drag didn't take). Lock every other track (video and audio) while inserting, then compare all tracks before/after.
- An adjustment clip's comp sees the composited 1920×1080 frame, 1 comp frame = 1 timeline frame, so focus boxes are frame fractions measured on the framed picture.
- Screen-recording framing on #3: Tella clips at Zoom 1.65, Pan -372, Tilt 60, which shows source px x 1207–3534, y 374–1683. Copy that onto any inserted Tella clip.
- `AppendToTimeline` with `mediaType: 1` places video only (no Tella audio).

## 2026-09-27 — HTML UI mockups are full-screen UI too
- I built the prospect-list mockup as a floating window on the desk with a counter chip, though the full-screen/no-MG rule was already in ways of working. **Before any UI mockup, read the "UI demos" section of ways of working.** A mockup is the software filling the frame, edge to edge, static camera, nothing that isn't part of the UI. The Visuals v1 kit (`deskWallpaper`, `macWin`, `chip`, `neo`, `vignette`) is for motion-graphic beats, not for UI.
- `AppendToTimeline` clipInfo `endFrame` is exclusive: frames 0–74 give a 74-frame clip. `endFrame: 73` left the clip one frame short.
- Placing a rendered visual into a marker: read the marker (`GetMarkers`, frame + duration), render exactly that many frames with `render.render_beat({"id","scene","start","end","layer":"full"})`, then `AppendToTimeline` with `trackIndex`, `recordFrame`, `mediaType: 1`.
- **Pace of a UI filling up (Samuel, 2026-09-27):** typing cell by cell with 16 rows in 3 s "feels too fast". Fill a sheet row by row (whole rows landing), at about 0.3 s per row, 8 rows in a 3 s shot. Re-render to the same path and call `MediaPoolItem.ReplaceClip(path)` to refresh it in Resolve without touching the timeline item.
- **A UI mockup that "fills up" fills the whole visible sheet** by the end of the shot. Cutting the row count to slow the pace was wrong: keep every row and change the cadence (whole rows, gaps that tighten). **No selection or highlight boxes in UI mockups** (Samuel: "Don't add that row highlighter"). Highlighting is the adjustment clip's job, and only when he asks.

## 2026-09-27 — Real UI from Samuel's Chrome and Google Images
- **Standing: use his Chrome (Claude in Chrome) for anything that needs a login or a real page, and Google Images for real product screenshots.** Rule in [[03-Areas/video-editing/ways-of-working|ways of working]]. Signed in on 2026-09-27: LinkedIn yes, Instantly no (redirects to login), Apollo not confirmed (it hung loading).
- **The extension's screenshot is CSS-sized** (about 1057–1568 px wide). For video, grab the window at device pixels with `scripts/chrome_grab.ps1` (PrintWindow). His Chrome is maximised on a 2560×1440 CSS / DPR 1.5 screen (3862×2110 window grab), and `resize_window` has no effect while it's maximised. A 16:9 page crop of 2100×1181 at x 866 frames a centred site well.
- **Real scrolls:** `scripts/chrome_seq.ps1` grabs the window in a loop and files each grab under the step number in the tab title. The page script sets the title to `moving` → scrolls → waits 450 ms → `S<nn>`, then holds 1.4 s. Start the recorder in the background (title `READY`) before launching the page script, and don't return a Promise from `javascript_tool` for a long run. LinkedIn scrolls inside `main#workspace`, not the window.
- **Chrome's "Claude started debugging" bar comes and goes between grabs**, which moves the page by about 90 device px. Find the page top per frame (first run of rows brighter than 200 on a 1 px column at x=40, below y 150) and crop from there, +6 px.
- **The extension's virtual cursor is drawn into the page** where the last click or hover landed. Hover at the far left edge (outside the crop) before recording.
- Google Images results can be read from the page: regex `["url",h,w]` triples out of `innerHTML`. Strip the query strings or the tool blocks the output. Image search `&tbm=isch&tbs=isz:l` gives large sizes.
- LinkedIn's bottom Messaging dock shows his inbox. Hide it with page CSS (`#msg-overlay…{display:none}`) before a grab, and keep a public figure's profile on screen rather than a private person's.

## 2026-09-28 — Technical lessons moved out

The Resolve and Fusion scripting and crash lessons (MCP bridge, Fusion API, TDR and cache crashes, comp builds by script) moved verbatim to [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]], to keep this memory short. Read that note before scripting Resolve or Fusion. New technical lessons go there; lessons about how Samuel works and what he wants stay here.


## 2026-09-28 — A flagged job is a question, not a footnote

- The 2026-09-22 backfill of delivered-projects noted "Alex video (Sep #3)" as in progress and left it out. Nobody asked Samuel, so on invoice eve the record said 2 videos when he had done 4. An open flag in delivered-projects gets asked at the next session. Before the invoice on the 29th, confirm the month's count with him.

## 2026-09-28 — Cache and drives
- **G: is Google Drive (GoogleDriveFS), not a local disk.** Never put cache, proxies or footage there. The only local disk is C:.
- Route Rise #3 project UUID = `3b3169d0-b3d3-4b98-af1c-48cd4e27c73e` (its CacheClip folder). A backup copy of that cache is in `C:\Usersepzy\Videos\CacheClip-backup\`. Delete it once the job is delivered: it takes 8.85 GB on a nearly full C:.
- Resolve keeps its render cache across restarts. Nothing has to be re-cached as long as the cache folder, the cache location setting and the cached clips stay the same.
- Correction (2026-09-28): the backup path above is mangled. It is `C:\Users\repzy\Videos\CacheClip-backup\`.
