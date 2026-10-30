---
type: project
area: video-editing
status: active
updated: 2026-10-30
source: manual
tags: [client, routerise, gamma, long-form]
---

# Route Rise — "3. Claude + Gamma App MCP Will Make You Rich"

Client job through [[03-Areas/video-editing/clients/routerise|Route Rise]] for [[03-Areas/video-editing/clients/gamma|Gamma]] (not Alex). Back to [[03-Areas/video-editing/video-editing|Video editing]].

## Brief (ClickUp card, screenshot 2026-10-30)

- **Card:** 3. Claude + Gamma App MCP Will Make You Rich · EDITING IN PROGRESS · tags edit-assigned, edit-day2, +1 not shown · two assignees · checklist 17 items, not read yet.
- **Script:** ClickUp doc, `https://app.clickup.com/9012764231/v/dc/8ck7qj7-11112/8ck7qj7-1232`.
- **Footage:** Google Drive folder *Ep. 12 - Claude + Gamma will make you rich* (Oct 21).
- **Dates on the card:** none set. Samuel, 2026-10-30: starts today, deadline next week (exact day not given).
- **Rate:** USD 175 (Samuel, 2026-10-30).
- **Invoice:** goes on the **October 2026 batch** even if it isn't finished by 2026-10-31. Samuel, 2026-10-30: *"even though I may not finish it before 31st, it is allowed for me to add it to my invoice"*.
- **Look:** Gamma is not Alex, so the Frontal brand kit does not apply. Edit standard: [[03-Areas/video-editing/creative-director/creative-director-standard|creative director standard]] under Samuel's corrections. Gamma's own brand: needs-input.
- **Job folder (to make):** `Desktop\Video edits\Routerise\3. Claude + Gamma App MCP Will Make You Rich\`. Earlier Gamma job for reference: `I Created 40 Social Media Posts in 10 Minutes Using Claude + Gamma\` (August 2026).

## Status

- 2026-10-30: documented, nothing started. Next: download the footage and read the script and checklist, then phase 1 (sync, silence, noise, retakes, uhms, sections, transcript) as on the Alex jobs.
- 2026-10-30 (Editor): phase 1 started on Samuel's go (*"download the footage, cut it and as we normally do and wait till I revise the cuts"*). Card #869exr4bc (`https://app.clickup.com/t/9012764231/869exr4bc`). Drive folder `16Ef4mBcP1oUlRVMbH9Ok08shuoSFqJOJ`: `Footage/A` (C4164.MP4 20.4 GB, 44:47; C4165.MP4 9.7 GB, 21:22), `Footage/B` (C4032.MP4 21.1 GB; C4033.MP4 10.0 GB), Sony ILCE-7M4, 3840x2160 **25p**, each with its M01.XML; `Ep 12 - Audio.mp3` (48 kHz stereo, 43:42). Downloads run in a minimised cmd window (`Docs\download.cmd`, log `Docs\download.log`), A-cam first, at ~1.4 MB/s (~6 h for A-cam, ~12 h all).
- Whole-audio Whisper (GPU) in the scratchpad: ~2 min of crew chat before the hook, retakes throughout, outro ends 43:20, so the audio matches A-cam clip 1 (44:47). What the 21-min second clips hold: not known until downloaded.
- The ClickUp script doc refuses access in Samuel's Chrome ("You need access to this Doc"): asked Samuel. Resolve had his *Talking head* project open: asked before switching. Timeline rate 25 fps assumed (footage 25p): asked.
- Plan: cut on A-cam + mic, add B-cam afterwards per clip from A-cam source times.

## Phase 1 run, 2026-10-30 (Editor)

- **Resolve project** *3. Claude + Gamma App MCP Will Make You Rich* in the `Routerise` folder, made fresh, **25 fps**, 1920x1080, cache on `C:\Users\repzy\Videos\CacheClip`. The 13 bins were made by API with the template names (screen control was not granted this session, so no power-bin drag). Samuel's *Talking head* project was saved first.
- **Sync:** camera scratch audio alive (max -2.4 dB). `av_sync.py` camera-audio method: the mic starts **49.78 s after the camera** (z 30.6), the same at 10, 25 and 40 min (no drift). Mic = `Conformed audio\Ep 12 - Audio (wav copy).wav` (lossless decode of the MP3, reads at 25 fps). *A-roll synced (raw)*: camera picture V1, mic A1 at frame 1245, +6 dB, linked, two lip-sync markers.
- **Cut v2 (Editor) - silence + noise removed:** built by script, not the Ripple Delete Silence dialog: per-frame peak of the mic, threshold **-40 dB** (room tone peaks at about -54, speech -24 to -15), head 1 f, tail 3 f, gaps of 2 f or more stripped; 1,272 clips, then 532 noise clips (no 40 ms RMS above -40 dB) dropped: **740 clips, 41,353 f (27:34)**, V1/A1 aligned on every clip. Safe here because camera, mic and timeline are all 25 fps.
- **Retakes:** per-clip Whisper on the GPU (740 clips, 5 min). The Editor read the whole clip table and cut **451 clips**: the crew chat (start, 16:44-18:25, 20:10-22:29, 27:30-29:24, the long laughing break 30:19-35:03) and every earlier take, keeping the last clean complete take. A 3-gram check of every cut clip against the kept text found nothing said only once. Manual in-clip trims: c058 (restart "a small group of people are -"), c088 ("you should build a" before the retake).
- **Cut v4 (Editor) - retakes + uhms removed:** `uhm_find.py --tight --fps 25` (new `--fps` flag) with tails loosened 2 f (video 4 lesson): 183 trims, mostly tails, 8 pauses. 296 clips, 20,682 f.
- **Cut v5 (Editor) - sections:** v4 plus the leading "Okay," cut on two lines (c072, c477). **20,658 f (13:46), 296 clips**, V1/A1 aligned, camera-minus-mic offset 1245 f on every clip. 12 sections, clip colours + duration markers: Hook Yellow · The way people teach it fails Blue · One product isn't a business Green · The price tier model Purple · Why Gamma: three reasons Teal · Tier 1: the lead magnet Navy · Lead magnet build Brown · Tier 2: the written course Pink · Written course build Tan · Tier 3: the premium cohort Lime · Cohort build and the money Orange · Sell it with content + CTA Violet.
- **Transcript:** `Docs\Transcript - Cut v5 sections (2026-10-30).docx`, Whisper's mishearings fixed (Gemma/Cloud/Clod -> Gamma/Claude, Justin Welsh), prompts boxed, red notes. Two lines to listen to: "a cohort with a long ten seats" and "We're how many hours he's been building it".
- Working files: `Docs\Editor working files (2026-10-30)\` (clip_table, whisper_words, v2_clips, v3_cut_list, trims, segs_v2..v5, sections, cut_words, sentences).
- **Not in yet:** A-cam clip 2 (C4165, 21:22; the mic ends 14 s before clip 1 does, so it has no mic) and both B-cam files, still downloading. B-cam goes on V2 per clip from the A-cam source times once it lands.
- **Phase 1 done 2026-10-30 ~17:35 WAT on A-cam. Next: Samuel revises *Cut v5 (Editor) - sections*.**
- 2026-10-30 18:20 (Editor): **A-cam clip 2 (C4165) is a different episode**, not this one: camera-audio Whisper shows a video on McKinsey presentations ("I uploaded a thousand slides from McKinsey presentations into Claude…", Gamma rebuild, end card to "three presentations you can make"), shot the same day. Not used in this cut. B-cam C4033 (same length) is most likely its B-cam; it is still queued in the download.
