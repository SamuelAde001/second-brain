---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: A2
---

# A2 · Import into Resolve and syncing

> **Read when:** making the Resolve project, importing, syncing camera, mic and screen recording, adding a second camera, or naming and duplicating timelines (Editor, setup step and every new timeline). **Client values:** frame rate per client in [[03-Areas/video-editing/clients/alex|Alex]] and [[03-Areas/video-editing/clients/gamma|Gamma]]. **Status:** draft, not yet approved by Samuel.

## Rules
### The project
- **A2.1** Make a fresh project for each job, in the Project Manager folder `Routerise`. Never copy the `Project Template` project: the copy keeps the template's creation date. ✅ *"Don't copy the template… it keeps the date created same as the day the template was created"* (2026-09-24) · ✔ 2026-11-03
- **A2.2** Bins: drag the 13 folders from the "Folder structure template" power bin onto Master (GUI only). Then confirm by script that Master holds AI Vids, Assets, Chat GPTweb images, Client's B-rolls, Fusion Comps and Adjustments, Musics, Raw vids, Screen records, Screenshots, SFX, Shorts B-rolls, Visual Inspo, Youtube B-rolls. If screen control is declined, make the 13 bins by script with those names. ✅ *"create a new project and copy the bin in power bin called Folder structure"* (2026-09-24) · ✔ 2026-11-03
- **A2.3** Settings: 1920×1080, DaVinci YRGB, cache in `C:\Users\repzy\Videos\CacheClip`, timeline working luminance SDR 100 (one project was found on HDR 1000). The grade itself is Samuel's call. 🎬 ⚙️ · ✔ 2026-11-03
- **A2.4** The timeline frame rate is the client raws' frame rate, so nothing judders or drops frames (Alex's Sony raws 29.97, Gamma's 25p). **Never above 30 fps: no 60 fps timelines.** ✅ *"use the frame rate of the client raws for the timeline so we don't get issues"* · *"never 60fps, nothing more than 30 fps"* (2026-11-03) · ✏ 2026-11-03
- **A2.5** On a 4K video, generate proxies when they are needed (Half or Quarter, DNxHR LB, Prefer Proxies), where possible. Deliver uses the originals. ✅ *"Making the video a proxy solved a lot of the cap"* (2026-09-25) · *"if possible generate proxies when needed on a 4k video"* (2026-11-03) · ✏ 2026-11-03
- **A2.6** Don't create a project while Resolve sits on the Deliver page of another project: it hangs. Save his project, go to the Project Manager, create, expect a restart (`restart_resolve.py`). 🔁 (2026-10-19, 2026-10-28) ⚙️ · ✔ 2026-11-03
- **A2.7** If the open project isn't this job's, switch without asking unless he has said he is using Resolve (A1.7, A1.8). Save his project first; no need to load it back afterwards. ✅ (2026-10-08) · *"no need to load it back afterwards"* (2026-11-03) · ✏ 2026-11-03
- **A2.8** Project library: new Route Rise jobs in `Routerise/`, delivered ones in `Routerise/Delivered/`, other clients in `Clients/<client>/`, personal brand in `Samuel Signals/`, `HighSignals/`, tests in `Tests & experiments/`, deletion candidates in `_Review to delete/`. Move projects only in the Project Manager GUI, never the open one. ✅ *"go through Davinci resolve project manager and help me sort everything properly"* (2026-10-14) · ✔ 2026-11-03

### Import
- **A2.9** A-roll and mic go into `Raw vids`; the screen recording into `Screen records`. ⚙️ · ✔ 2026-11-03
- **A2.10** One camera, an external mic on A1 at +6 dB. Camera audio is never used in the edit. 🎬 (2026-09-14) · ✔ 2026-11-03
- **A2.11** Two mic files in one project are just what the client supplied, not a convention. ✅ (2026-09-14) · ✔ 2026-11-03

### Syncing
- **A2.12** Try Resolve's auto-sync by audio waveform first. If it fails (it returns False when the camera's scratch audio is dead, the norm on Alex's shoots), run `03-Areas/video-editing/scripts/av_sync.py "<camera>" "<mic>"`: audio cross-correlation if the camera audio is alive, motion correlation if dead. ✅ *"We can use Davinci Sync by audio waveform feature, if that doesn't work, we would try and sync video"* (2026-09-21) · ✔ 2026-11-03
- **A2.13** One constant offset per camera and mic pair. Align one section and the whole clip follows; motion sync needs only the first ~6 minutes. ✅ (2026-09-21) Samuel checked the constant offset as perfect (2026-09-25). · ✔ 2026-11-03
- **A2.14** Measure only where he talks to camera; ignore weak windows (z 3 to 5 gave garbage). Confirm the offset on a second talking stretch, then ear-check the first placement. A positive `av_sync.py` offset means the mic started first. ⚙️ · ✔ 2026-11-03
- **A2.15** Sync the screen recording to the video too, as part of setup: cross-correlate its audio against the mic (20 Hz over the whole length, then 100 Hz on a 90 s stretch; sweep 120 s windows to catch cuts in the recording). ✅ *"Good Job so far, but you haven't synced the screen recording to the video also, do that"* (2026-09-24) · ✔ 2026-11-03
- **A2.16** One main audio for cutting. The screen recording's audio stays only on the raw sync timeline, as a disabled reference. ✅ *"I removed the audio of the screen recording, cause we don't need that, only one main audio"* (2026-09-25) · ✔ 2026-11-03
- **A2.17** Conform the mic before cutting: a lossless, metadata-stripped copy that reads at the timeline rate, in `Conformed audio\`, its audio MD5 matching the original (the raw DJI WAV reads as 29.97 and puts audio cuts off the video cuts). Decode an MP3 mic to a lossless WAV the same way. ✅ (2026-09-24) · ✔ 2026-11-03
- **A2.18** After every cut pass, check every A1 clip's start and duration equal its V1 clip. ✅ *"Why do we have places where the video cut is not aligned with the audio cut … it must be the exact same place"* (2026-09-24) · ✔ 2026-11-03
- **A2.19** Several camera clips: sync each clip to its own mic and check each on a second stretch; conform every mic. ⚙️ · ✔ 2026-11-03

### The raw sync timeline
- **A2.20** Build `A-roll synced (raw)`: camera picture on V1 from the start, mic on A1 linked to it, screen recording on V2 with its audio on A2, linked and disabled. Markers: a blue "Lip-sync check" at the start and end of the A-roll (one pair per camera clip), a green "Screen sync check" about a minute in. ⚙️
- **A2.21** Take setup to "on the timeline and synced", tell Samuel, then go on with the cut (A1.1). ✅ *"Get all the things sorted till putting on the timeline and syncing audio, let me know"* (2026-09-24)
- **A2.22** The synced raw is the master. When a cut goes wrong, go back to it and re-cut from it. ✅ *"We are working with the origingal synced video raw now"* (2026-09-25)
- **A2.23** Lip-sync markers stay on the raw; remove them from the cut timelines. ⚙️

### Second camera
- **A2.24** Cut on A-cam and mic first. Then duplicate the cut as a new timeline and put B-cam on V2 with exactly V1's cut points (B source = A source + the offset from sample-level camera-audio cross-correlation). Verify every start and end, then disable V2 where A-cam should show. ✅ *"the cut lines must be exactly the same, just on another track"* (2026-10-30)
- **A2.25** Choosing angles is the Editor's judgement. Starting point used on Gamma Ep12: switch at a tight jump cut (removed gap 2 s or less) once a stretch passes 5 s on A or 4 s on B; force a switch at 12 s (A) or 8 s (B); B about 45 % of the runtime. ✅ *"disable some parts based on what you feel would be right"* (2026-10-30) 💡 for the numbers

### Timelines: names and duplicates
- **A2.26** Name every Editor timeline with its version, "(Editor)" and the step: `Cut v4 (Editor) - ripple silence`, `Cut v5 (Editor) - noise clips removed`, `Cut v6 (Editor) - retakes removed`, `Visuals v1 (Editor)`. ⚙️
- **A2.27** Rename superseded timelines `zz <name> old HHMMSS (Editor)`; never delete them. Scratch timelines go only when Samuel says. ⚙️
- **A2.28** Never write to Samuel's own cut or re-cut. When he has worked on a timeline himself (cuts, grade, disabled clips, A1 noise reduction), duplicate HIS timeline and build on the copy; all his changes must survive. Visuals go on their own timeline, never on a Cut timeline. 🔁 (2026-10-22, 2026-10-31) ✅ *"this timeline that I'm using is what you will duplicate when you're working"* (2026-10-31)
- **A2.29** Revising the Editor's own timeline: he caches the whole video before review, so work in place (only touched clips re-cache). A new timeline is fine if faster, as long as the whole timeline is cached again at the end. ✅ (2026-10-10, 2026-10-15) Replaces "duplicate before any write" (2026-09-18, 2026-09-21) and "don't duplicate timelines" (2026-09-27).
- **A2.30** Before any build, export his current cut and diff it against the last one. If he changed it, re-time the word maps and the plan to the live cut (an old map drifted 15 to 69 frames). ⚙️

### Scripting the timeline
- **A2.31** How `AppendToTimeline`, source offsets and a scripted cut rebuild behave (only when camera, mic copy and timeline share one rate; 150 clips per call): open [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] and [[03-Areas/video-editing/sops/routerise-cut-workflow|cut workflow]] before scripting a timeline. ⚙️

## Never
- **A2.32** Never sync from file clock times. The DJI and Sony clocks ran ~143 s apart; filenames predicted +108 s when the truth was −34.9 s. ⚙️
- **A2.33** Never place clips from a drift line (the old "129 ppm" model). Cuts built that way felt out of sync to Samuel; use the one constant offset. ✅ (2026-09-25)
- **A2.34** Never use camera audio or the screen recording's audio in the cut. ✅ (2026-09-25)
- **A2.35** No agent deletes a Resolve project. Leave a clearly named leftover in `_Review to delete/` for him. ✅ (2026-10-14)

## Pictures
- (no picture yet: a screenshot of a correct `A-roll synced (raw)` timeline with its sync markers would help)

## Questions for Samuel
- **Q-A2.a** Frame rate: Alex's raws are 29.97 but the timeline is 23.976 (frames dropped, possible judder). Open since 2026-09-25. → Options: (1) keep 23.976, as in every approved final (2) match the footage. My pick: (1), unless Route Rise's delivery spec says otherwise. → Samuel: use the client raws' frame rate (2026-11-03). A2.4 updated; 23.976 is no longer the Alex default.
- **Q-A2.b** Revisions: you said "work on one timeline" (2026-10-10), then "a new timeline is fine if faster" (2026-10-15), then "duplicate the timeline I'm using" (2026-10-31). My reading is A2.28 + A2.29: your timeline gets duplicated; the Editor's own timeline is fixed in place or on a copy, cache redone. → Options: (1) confirm this reading (2) always duplicate. My pick: (1).
- **Q-A2.c** Second-camera switching numbers (A2.25) come from one video. → Options: (1) keep as the default (2) leave fully to judgement each time. My pick: (1).

## Sources
Replaces or draws on [[03-Areas/video-editing/sops/routerise-job-setup|Route Rise job setup]], [[03-Areas/video-editing/sops/routerise-cut-workflow|Route Rise cut workflow]], [[03-Areas/video-editing/resolve-project-library|Resolve project library]], [[03-Areas/video-editing/resolve-performance|Resolve performance]], [[03-Areas/video-editing/routerise-house-style|Route Rise house style]], [[03-Areas/video-editing/ways-of-working|Ways of working]], [[03-Areas/video-editing/sops/unattended-run|Unattended run]], [[07-Agents/video-editor/memory|Editor memory]] and the job notes.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
