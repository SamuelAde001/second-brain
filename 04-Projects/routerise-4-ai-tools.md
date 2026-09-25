---
type: project
area: video-editing
status: active
updated: 2026-09-25
source: manual
tags: [client, routerise, long-form]
---

# Route Rise #3 — "I Tried 100+ AI Tools. These 4 Are Best for Businesses"

Client job through [[03-Areas/video-editing/clients/routerise|Route Rise]]. Back to [[03-Areas/video-editing/video-editing|Video editing]].

## Brief (from the task card Samuel shared, 2026-09-24)

- **Title:** 3. I Tried 100+ AI Tools. These 4 Are Best for Businesses
- **Status on the card:** READY TO EDIT · tag: long form video · 10 checklist items on the card (not seen)
- **Dates:** start 2026-09-24 → **due Monday 2026-09-28**
- **Assignees:** Samuel + one other ("SD"), not identified
- **Idea doc (review & approve):** https://app.notion.com/p/3c073bd1b02b8187a826cf3affb931a0 — in the client's Notion workspace; the Brain's Notion connector can't open it.
- **Footage:** Google Drive folder "3 - 4 AI Tools" — shared from the client; not found in Samuel's own Drive.
- **Rate:** standard USD 333.33 unless Samuel says otherwise ([[03-Areas/video-editing/delivered-projects|delivered projects]] rule).

## Deadline maths

Route Rise's 5-day cap starts today (2026-09-24), so Monday is day 5. Sunday is inside the window and he doesn't work it: **about 3.5 working days**, with today mostly taken by Ep 3 content. His normal pace is 3–5 days on visuals alone ([[03-Areas/video-editing/workflow|workflow]]), so this only lands if the cut sheet is approved Friday night and Saturday and Monday are all visuals. Delivery time on Monday is not stated; the plan assumes by 6:30pm WAT with 7–9pm as buffer.

## Schedule (in TickTick, 📹Video editing)

| When (WAT) | Step |
|---|---|
| Thu 09-24 3:30–5:00pm | Kickoff: approve idea doc, get script, download footage, check which 4 tools the footage actually shows, list what's missing |
| Fri 09-25 7:00–10:30am | Cut: duplicate timeline, sync, ripple silence, remove fluff |
| Fri 09-25 10:30am–1:00pm | Claude pass: SRT + XML → what's still uncut, sections locked, transcript |
| Fri 09-25 7:00–9:00pm | Visual ideation: full HTML cut sheet, every sentence, approved tonight |
| Sat 09-26 7:00am–1:00pm | Visuals: intro + first half |
| Sat 09-26 7:00–9:00pm | Visuals: to ~75% |
| Sun 09-27 | Off |
| Mon 09-28 7:00am–1:00pm | Visuals: finish |
| Mon 09-28 2:30–5:00pm | SFX, music, PII blur check, watch-down |
| Mon 09-28 5:00–6:30pm | Render + deliver |

## Watch for (from the client note)

- Alex names tools on camera that don't match the footage (Higgsfield vs Arcads, twice). A video that is literally "these 4 tools" makes this the first check.
- Cut to the VO, not the script. Show real on-screen numbers, not rounded VO ones.
- Blur PII: emails, phone numbers, cards, addresses, store URLs.
- House style: cuts only, MagicZoom V3, Geist, native Fusion nodes, B-roll from YouTube/TikTok only.

## What arrived (2026-09-24)

- **End client: Alex Vacca** (Drive folder owner `alex@frontal.so`; Notion "Client: Alex Vacca").
- **Drive folder "3 - 4 AI Tools":** `C0786.MP4` (A-roll, 12.56 GB), `TX02_MIC017_20260924_111422_orig.wav` (mic, 27:54, mono 48 kHz), and a "Screenshare" doc linking to Tella.
- **Tella screen recording** "Top 4 Tools for B2B GTM Workflows", 23:55, exported 4K (3840×1912, 30 fps). Chapters: 00:00 Wedge Agent Feeder · 01:57 Railway Hosting · 05:22 Claude and GTM OS · 17:32 Whisper Flow · 20:23 Bringing Tools Together.
- **The 4 tools:** Clay, Railway, Claude, Wispr Flow. Title is the backup framing; the first-choice title was "I Tried 100+ Claude Skills. These 6 Are Best for Businesses".
- **Script structure:** Hook → Clay (+demo) → Railway (+demo) → Mid-CTA (Frontal free call) → Claude (+demo in "Frontal OS") → Wispr Flow (+Notetaker demo) → 4-tool system build (daily signal automation) → CTA (end-screen video). Writer: Alan Perce.
- **Local folder:** `C:\Users\repzy\Desktop\Video edits\Routerise\3. I Tried 100+ AI Tools. These 4 Are Best for Businesses\`. Offline brief: `Docs\Idea doc and script.docx` (+ `.md`).
- **Resolve project:** same name, in the `Routerise` project folder, **created fresh on 2026-09-24** with the 13 bins from the "Folder structure template" power bin. Samuel rejected copying the template because a copy keeps the template's created date. A leftover "(template copy - to delete)" project sits in the same folder; Resolve refused to delete it by script.
- **Timeline "A-roll synced (raw)":** C0786 picture on V1 from frame 0; mic on A1 from frame 237, linked, at +6 dB. The mic started **9.88 s after** the camera (motion sync; the camera's scratch audio is dead at −61 dB). Two blue "Lip-sync check" markers at 1:00 and 25:30. There's no speech on the mic from about 11:00 to 18:30.
- **Tella screen recording synced:** V2 from frame 6727 (camera time 280.58 s), its audio on A2, disabled, as a reference. Tella time t = mic time t + 270.700 s, checked at two points with no drift and no cuts (audio xcorr, z 14–29). Tella 8:00–15:00 is silent on both sources: a pause in the recording. A green "Screen sync check" marker sits a minute in.
- Set up by the [[03-Areas/video-editing/sops/routerise-job-setup|Routerise job setup]] SOP, written on this job.

## The cut (2026-09-24, Editor)

- **Timeline "Cut v2 (Editor) - frame-locked": 201 clips, 9:34.** V1 A-roll, V2 Tella screen, A1 mic at +6 dB. Each clip is linked across all three tracks and cut on the same frame. Gaps were cut from the waveform (−38 dB). Mistakes and retakes were cut as whole clips, keeping the last clean take. From 27:56 of mic.
- The mic on this timeline is `Conformed audio\TX02_MIC017 mic (23.976 grid, lossless copy).wav`, the same samples as the raw (MD5 checked). The raw's metadata made Resolve read it at 29.97 fps, which put the audio cuts off the video cuts on v1. v1 is kept as *OLD Cut v1 (audio off the frame grid)*.
- **8 chapters, colour-coded** (duration markers + clip colours): 1 Hook and intro (yellow) · 2 Clay (blue) · 3 Railway (purple) · 4 Mid-video CTA (pink) · 5 Claude (teal/cyan) · 6 Wispr Flow (green) · 7 Bringing the 4 tools together (tan/sand) · 8 Outro (violet/lavender).
- **28 check markers** on the mic clips: joins, keeper choices, two in-clip retake cuts, the 4-frame "work." clip, and every screen jump where silent screen action was removed (the biggest: 8 minutes of Claude running, at 4:39).
- **Transcript:** `Docs\Transcript - Cut v2 (2026-09-24).docx`. ALL CAPS, one section per chapter in its colour, red notes at every A-roll ↔ screen switch, purple boxes on the two prompts.
- **Found while cutting (needs Samuel or Alex):**
  - The Railway dashboard ("here is the project… our small database") is not on the screen recording. The screen shows the teleprompter there.
  - The scripted 4-tool system build demo was never screen-recorded. Chapter 7 is talk only and needs built visuals.
  - Most talking parts of the Tella file show Alex's teleprompter, not a demo. Real demo stretches: Clay 1:22–2:04, playbook page 2:34–2:40, Claude 4:05–6:02, Wispr Flow + frontal.so 6:33–7:55.
  - Check by ear: "one provider can find the email" (probably "can't"), "ICP and time estimates" (probably TAM), "inside of BloD".

## The cut, redone from the synced raw (2026-09-25, Samuel's method)

Cut v2/v3 were rebuilt clip by clip with a drift model and went out of sync. Samuel restarted the cut from the synced raw. The method is in [[03-Areas/video-editing/sops/routerise-cut-workflow|the cut SOP]], steps 2 and 2b.
- **Cut v4 (Editor) - ripple silence:** duplicate of *A-roll synced (raw)*, Tella audio deleted, Ripple Delete Silence run by Samuel at −33.4 dB / pre 0 / post 3 / min 2. 331 clips, 19,426 frames.
- **Cut v5 (Editor) - noise clips removed:** 73 leftover noise clips (310 frames) ripple-deleted after a level check on every clip. 6 short clips with speech-level sound kept for Samuel. 258 clips. XML: `Docs\Cut v4 ripple silence (2026-09-25).xml`, `Docs\Cut v5 noise removed (2026-09-25).xml`. Subtitles: `Docs\Cut v5 subtitles (2026-09-25).srt`.
- **Cut v6 (Editor) - retakes removed: 11:02, 204 clips. The current cut.** 54 retake/false-start clips cut (3,237 frames), always keeping the last clean complete take; judged from the v5 subtitles per clip against the script. Every kept clip's source position on V1, A1 and V2 was verified identical to v4/v5 after each delete.
- **20 Orange clips + Yellow/Pink markers for Samuel:** in-clip retakes that need a razor (1:42 "figure out what and", 0:32 "if you've ever built… if", 7:20 "putting all that context by writing" ×2, 9:08 "bring these four tools together" ×2, 10:29 "whether the resource" ×2, 10:42 "Claude helps us research" ×2), the 1:13 "improve your chances" tangle, "Kenny is absolute Kenny", a possible repeat at 5:32, the first clip (sound before take 1), a 1.7 s unlabelled clip at 9:15, and the 6 short-sound clips (the two at 4:21 are the word "Claude", a false start before "So the third tool is Claude").
- **Transcript crosscheck (fresh subtitles on v6):** reads as one piece, every script section present in order, no other repeats.
- **8 sections colour-coded** as before (clip colours + duration markers): Hook 0:00 · Clay 0:30 · Railway 2:33 · Mid-CTA 3:54 · Claude 4:23 · Wispr Flow 7:01 · Bringing the 4 together 9:10 · Outro 10:51.

## Final cut (Samuel, 2026-09-25)

- **Samuel finished the cut on the timeline "Cut v6 (Editor) - retakes removed": 9:55, 191 clips. This is the final cut.** Sync checked (V1/A1 aligned, camera–mic offset unchanged on every piece), no noise clips, no flash frames, no gaps, nothing from outside v5. All markers removed. XML: `Docs\Final cut by Samuel (2026-09-25).xml`.
- 11 sections by clip colour: Hook 0:00 · Clay 0:30 · Clay demo 1:29 · Railway 2:14 · Railway demo 2:29 · Mid-CTA 3:34 · Claude + GTM OS demo 4:03 · Wispr Flow 6:24 · Wispr Flow demo 6:55 · Together 8:15 · Outro 9:43.
- **Transcript:** `Docs\Transcript - Final cut (2026-09-25).docx`, one chapter per colour run, prompts boxed, 5 check-by-ear notes: "one provider can find" (can't?), "ICP and time estimates" (TAM?), "all the odd one play", "B2B about campaign" (outbound?), and whether the "I" in "how would I actually bring" survived the trim at 8:15.
- What the Editor missed and why: [[03-Areas/video-editing/sops/routerise-cut-workflow|cut SOP]], "What Samuel still had to fix on Route Rise #3".

## Visuals plan (proposed 2026-09-25, waiting for Samuel's go)

Samuel's brief (2026-09-25): a visual for every main sentence, *"show and not tell"*, built as rendered HTML videos placed on the timeline (not Fusion nodes yet). He approves per beat, then approved ones get rebuilt as Fusion comps. The TSB visuals Claude made were called *"very mediocre… shallow… didn't have depth"* by his creative director. Study his own edits first: the finals of *$7M Founder* and *Taking a step back from Claude*, and their main timelines.

Found before planning:
- Samuel's working timeline is *Cut v6 (Editor) - retakes removed* (9:55). He added Tella on V4 and the mirrored A-roll PIP on V6, 161 pieces each, 71 disabled. Screen rec on: 1:29–2:14, 2:49–3:06, 3:09–3:15, 4:26–6:24, 6:55–8:15. The rest (~5.5 min) is A-roll, where visuals can go.
- Finals: `$7M…2.mp4` (7:30) and `1. Taking a step back…2.1.mp4` (10:41). TSB `v2.mp4` is a broken render (no moov atom).
- Reusable study material: `Claude Files\Style Study - Cold Outreach\` (frames, 13 node screenshots, `timeline1_full.json`), `Claude Files\TSB frames\`, `TSB comps\`. On TSB, Claude built 3:06–end and Samuel built 0:00–3:06 ([[03-Areas/video-editing/tsb-graphics-pipeline|TSB pipeline]]).
- Render tooling: Chrome + `Claude Files\tools\cdp_shot.py` (stdlib CDP), ffmpeg 9.0.1, node. No PIL/numpy.

Steps: (1) study both finals and timelines, read-only → a visual-vocabulary note; (2) visual sheet, one row per sentence; (3) style check: the hook's visuals rendered and placed first; (4) build and render the rest; (5) place on a duplicate *Visuals v1 (Editor)*, V7; (6) Samuel reviews per beat; (7) Brain notes and commit.

## Visuals v1 (in progress, 2026-09-25)

- Timeline *Visuals v1 (Editor)* = duplicate of Cut v6 (Samuel's final cut with Tella V4 + PIP V6). Visuals on **V7 "Claude visuals v1"**, one video per sentence, Apricot. Subtitle track (for timings) disabled.
- Source of truth: `Graphics\Visuals v1\beats.py`. Scenes in `scenes\src\`, renders in `renders\`, stills in `stills\`. Re-render one beat: `python render.py B07`, then re-place it.
- AppendToTimeline `endFrame` is **exclusive** (pass the full frame count).
- Done: Clay B01–B12. Next: Railway B13–B25, mid-CTA B26–B32, Claude B33–B36, Wispr B37–B41, together B42–B63, outro B64.

## Open

- Monday delivery time — needs-input.

## Log

- 2026-09-24 — Job received. Documented and scheduled by Editor.
- 2026-09-24 — Footage downloaded and sorted, brief saved offline, fresh Resolve project built from the power-bin folder structure, A-roll and mic synced on a timeline. Next: Samuel's lip-sync check, then the cut (ripple silence).
- 2026-09-24 — Cut built (Cut v2, frame-locked, 9:34), chapters colour-coded, transcript written. Samuel caught audio cuts off the video cuts on v1; fixed with a 23.976-grid mic copy. Next: Samuel reviews the cut and the check markers, then the Claude pass / cut sheet.
- 2026-09-25 — Samuel found the scripted hook missing. Crosscheck of every raw mic line vs Cut v2: 4 places wrongly cut (opener "I've tested a lot of AI tools… I realized something", 4 takes at mic 0:20–0:47; Clay "look for a lot of different data points… useful signal" mic 4:43; "running ads on LinkedIn" mic 5:01; "to actually make it real" mic 25:23). Everything else cut is a true retake or a slip. Correction: the Railway dashboard IS on the Tella recording (~Tella 3:25–4:00), and the sync line above reads the wrong way round: mic t = Tella t + 270.7 s. Next: restore the four into a Cut v3 once Samuel picks the hook take.
- 2026-09-25 — **Cut v3 (Editor) - 4 restores** built (9:52, 209 clips; v2 kept as is). Opener: take 1 + take 4 (orange) on the timeline for Samuel to pick one. Clay lines and "make it real" restored. Blue "Restored" markers on every new clip. Transcript: `Docs\Transcript - Cut v3 (2026-09-25).docx`. Next: Samuel listens to the restores, picks the hook take, then visuals.
- 2026-09-25 — Cut restarted from the synced raw on Samuel's instructions: Ripple Delete Silence (Cut v4), noise clips removed (Cut v5), retakes removed and sections colour-coded (**Cut v6, 11:02**). 20 Orange clips left for Samuel. Next: Samuel resolves the Orange clips, then the transcript doc and the Claude pass / cut sheet.
- 2026-09-25 — Samuel finished the cut himself (9:55, final). Editor diffed it against Cut v6 for lessons, checked it (clean), and wrote the final transcript. Next: the Claude pass / cut sheet for visuals.
