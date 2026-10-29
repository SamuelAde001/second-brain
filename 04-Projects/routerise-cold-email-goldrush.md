---
type: project
area: video-editing
status: active
updated: 2026-10-29
source: manual
tags: [client, routerise, long-form]
---

# Route Rise — "4. The Cold Email Goldrush Is back (Don't miss it)"

Client job through [[03-Areas/video-editing/clients/routerise|Route Rise]] (Alex, Frontal). Back to [[03-Areas/video-editing/video-editing|Video editing]]. Order and token budget: [[04-Projects/routerise-videos-2-and-4-plan|videos 2 and 4 plan]].

## Brief (ClickUp card, screenshot 2026-10-18)

- **Card:** 4. The Cold Email Goldrush Is back (Don't miss it) · READY TO EDIT · tags edit-assigned, edit-day2, +2 more not visible
- **Dates on the card:** Thu (2026-10-22) → Mon 2026-10-26. Samuel, 2026-10-18: *"the other video also would be done maybe weekend or nextweek depending on how much tokens I have"*; delay is fine.
- **Card holds:** 5 attachments, 3 subtasks, checklist 0/17. Not read yet.
- **Thumbnail:** Alex between a cracked Gmail gravestone (2026, red X) and a gold Gmail icon (2027, green tick).
- **Rate:** USD 333.33 unless Samuel says otherwise ([[03-Areas/video-editing/clients/routerise|client note]]).
- **Job folder (to make):** `Desktop\Video edits\Routerise\4. The Cold Email Goldrush Is back (Don't miss it)\`. Straight apostrophe on purpose.

## Status

- 2026-10-18: documented, nothing started. Starts after video 2 ([[04-Projects/routerise-claude-10000-saas|2. Claude 10,000 SaaS]]); see the plan for when.
- Usage readings per phase go here.

## Phase 1 run, 2026-10-26 (Editor)

Samuel, 2026-10-26: *"We need to start work fast on my new client's video, we are already late behind schedule, so start download, sorting, puting on the timeline and cutting as we always do"*. Links: Drive folder `8 - Cold Email GoldRush` and the ClickUp doc *Alex Vacca Scripts → 4. The Cold Email Goldrush Is back (Don't miss it)*. It is this Route Rise card (video 4), not a new client.

- **Usage at start:** weekly 55 %, 5-hour 0 % (08:35 WAT).
- **Drive folder:** C0793.MP4 (8.88 GB), TX01_MIC012_20260929_130404_orig.wav (19:58.7, 48 kHz 24-bit mono), the "Script" Google Doc. No screen recording. Same shoot day as video 2 (MIC011, C0792).
- **Two scripts again.** ClickUp doc (Maria Fernanda Alvarez, 2026-09-30): "AI killed cold email", three rules (don't chase the best list, proof is the offer, fix the holes). Drive "Script" doc (2026-09-29): "The cold email goldrush is back", two things (research every person, build something only for them), the Sarah emails, 10-80-10. Both in the job's `Docs\`.
- **Job folder** made per the setup SOP plus `Conformed audio\`; mic conformed to a 23.976-grid lossless copy (audio MD5s match).
- **Resolve:** video 2's project saved first; project created in *Routerise* (1080p, 23.976, YRGB, cache `C:\Users\repzy\Videos\CacheClip`), 13 bins by script, conformed mic in *Raw vids* (reads 23.976).
- Working files: job `Docs\Editor working files (2026-10-26)\` (video 2's helpers copied).
- **Alex read the Drive doc:** whole-mic Whisper matched 99 of its 125 sentences, against 0 of 152 for ClickUp. He freestyles around it (e.g. OpenAI's job post "150 to 160k", script 144 to 160). The mic has a ~1:40 break at 9:05-11:00 (room tone only).
- **Camera:** C0793.MP4 20:07.2, 3840x2160 29.97, camera audio alive. Download took 42 min at ~4-5 MB/s (one internet drop at 71 %; `drive_download.py` retried by itself).
- **Sync:** MIC012 starts **2.68 s after** the camera (camera-audio xcorr, z 48.1 at 0-6 min; 0.00 s residual at z 35.1 on 14:40-19:40, `sync_check.py`: no drift). *A-roll synced (raw)*: V1 C0793 picture only, A1 mic at record frame 64, +6 dB, linked, blue lip-sync markers at 1500 and 27000.
- **Cut v1 (Editor) - ripple silence:** −33.4 / 0 / 3 / 2, cross fade off (video 2's values, same room a day earlier; red only in gaps), by screen control. 28,944 → 17,469 f, 302 clips, V1/A1 aligned. A Calculator window behind Resolve blanked the menus in screenshots; minimising it fixed that.
- **Cut v2 (Editor) - noise clips removed:** 53 clips under −40 dB (249 f) plus the camera tail past the mic end. **17,079 f (11:52), 249 clips**, no gaps, V1/A1 aligned. Per-clip WAVs in `Conformed audio\Per-clip WAVs (Cut v2)\`; per-clip Whisper on the GPU (`uhm_transcribe.py --cuda`, new) did 259 files in 90 s.
- **Cut v3 (Editor) - retakes removed:** workflow wf_68b30a3e-def (3 judges + 3 skeptics, editor-builder, ~5 min, ~1 weekly point) on `clip_table.txt`; skeptics raised no disputes; the Editor read the whole table against the cut list and agreed. 91 of 249 clips cut (`v3_cut_list.json`, reasons in `retake_workflow_result.json`), last clean complete take kept. **12,425 f, 158 clips**, V1/A1 aligned, sources unchanged.
- **Cut v4 (Editor) - uhms trimmed:** `uhm_find.py --tight` + 4 manual in-clip cuts (`manual_trims.json`: c067 "And in the,", c106 "or someone, a team.", c229 "but right now...", c241 "Inboxes are f-" → "Inboxes"). No fillers or long pauses (teleprompter read): 60 tails of 3-9 f. 64 keyboard lifts (every gap matched the plan) + Delete Gaps. **12,082 f (8:24), 158 clips**, no gaps, V1/A1 aligned, camera-minus-mic 2.64-2.70 s on every clip.
- **Cut v5 (Editor) - sections:** clip colours + 12 duration markers: Hook Yellow · Who I am and the promise Blue · Why now Green · Most people used AI the wrong way Purple · Thing 1: research every person Teal · The Sarah emails Navy · Mid-CTA Pink · Thing 2: build something only for them Tan · Back to Sarah Lime · 10-80-10 Brown · Honest limits Orange · Outro and CTA Violet.
- **Transcript:** `Docs\Transcript - Cut v5 sections (2026-10-26).docx` (`sections.py` → `transcript_docx.py`), Whisper's mishearings fixed, red notes for the judgement calls. Raw-vs-cut check: nothing said on camera is missing; flagged lines are Whisper wording or a later take kept on purpose.
- **Judgement calls (in the transcript):** 551 campaigns "average reply rate 4x the market" (script: best tenth 4x the typical); data cost "less than seven dollars" (script ~8); "more than 4,000 emails" (script 400); OpenAI "150 to 160K" (script 144 to 160); "500 or more got only 2%" (script 2.4%); event emails "8.1%" per Whisper (script 3.1%, listen); Hunter 5.2%/4.4% line never said; honest-limits passage take 3 drops "a real setup costs money"; the outro's last take has no "Everyone's".
- **Usage at end:** weekly 56 % (55 at start), 5-hour 3 %.
- **Phase 1 done 2026-10-26 ~09:40 WAT. Next: Samuel revises the cut on *Cut v5 (Editor) - sections*; then the visual plan.**

## Samuel's cut revision, 2026-10-26 (before 12:00)

He revised *Cut v5 (Editor) - sections* in place and removed the 12 section markers (clip colours kept): **12,100 f (8:25), 159 clips**. Diff against Cut v4 (`cut_diff.py`): 9 heads trimmed (33 f, e.g. "The", "So", "what", "that"), 22 tails loosened by 1-3 f (51 f added), and **"Inboxes are" restored** (8 f): my c241 trim was one word too far. The `--tight` tails are about 1-3 f too tight in places. Timed text of his cut: `Docs\Editor working files (2026-10-26)\sentences.txt` (173 sentences), `cut_words.json`.

## Visual plan v1, 2026-10-26 (Editor)

Samuel, 2026-10-26: *"I need every screen recording visual to look exactly like a live demo of those things. I don't want it to be too zoomed in, but also not too zoomed out ... Every website that they mention should show the actual website look ... the UI must be one-to-one identical. Demo everything, plan all those things ... also plan the visuals, that's the motion graphics"*. The creative director hasn't reviewed video 2 yet; build on what video 2 established. *"Don't waste tokens ... I need speed. I need quality ... cross-check the works and don't make any mistakes that I will have to correct."* The brand manager is using the same limits today.

- Usage at start: weekly 56 %, 5-hour 3 % (12:10 WAT).
- **Permissions, Samuel 2026-10-26:** *"Yes you can use flow and all the sites needed, they are already logged in on my browser"*. Flow on his Google account for AI B-roll; logged-in sites in his Chrome (Claude in Chrome) for captures and UI reference. Private data (his inbox, DMs, other people's names) never goes on screen: made-up content in the 1:1 UI. Posting or sending as him stays his call.
- Workflow wf_2c44b7fd-5c0 (~23 agents, ~5-6 weekly points expected): plan brief + capture inventory + live-demo recorder pilot → 9 section planners → 9 fresh reviewer-fixers → assembler (plan_check, `beats.json`, `Visual plan v1.html`) + 5 hero frames. Outputs in the job's `Docs\Visual plan v1 (Editor)\`; live state in `Docs\RUN STATE.md`.
- **Plan v1 done 2026-10-26 ~13:40 WAT** (weekly 56 → 65 %: ~9 points, above the 5-6 estimate; 4.66M subagent tokens): 139 beats, coverage 83.1 % (hook 100, intro 93.4, body 80.6), plan_check clean; 35 captures with 14 calls for Samuel (`CAPTURE LIST.md`); 8 hero frames; live-demo recorder `demo pilot\record_demo.py` (recommended zoom 1536 CSS px). Editor's check: the look holds; the Gmail rebuild (SA-07) is not 1:1 yet and is redone against his real Gmail before any build. Sent to Samuel for his yes. **RESUME: job `Docs\RUN STATE.md` → NOW.** Resolve on hold (Samuel working in it).

## EN-04 redesign and halt, 2026-10-26 afternoon (Editor)

- Samuel rejected EN-04's boxes (10-80-10): *"I don't like the design of the boxes for the 80% part, we have done something like this before, use that style just with the new branding"*. Rule on the [[03-Areas/video-editing/samuel-review-card|review card]]. Redesign wf_e9fcbc63-2d3 (3 designers, judge, finisher; weekly 65 → 68 %): his own B2B 10-80-10 bar (video 1) re-skinned in Frontal, ten pixel cells, check bracket closing round the whole bar on "campaign". Word frames checked; sent to Samuel, his yes pending.
- Five other beats in the same box look (WN-02, WN-11, WR-03, T1-06, T1B-14) redesigned; their fresh review was stopped midway.
- **Halted ~17:00 WAT**, Samuel: *"Wait, halt on this video, my creative director has sent in corrections, I need to do them on the last video and send a version, and whatever correction he sent, you would implement here too incase"*. Restart order in the job's `Docs\RUN STATE.md` → HALTED: the CD's video 2 corrections first, then the box-beat review, then captures.

## Video 2 is the foundation, 2026-10-28 (Editor)

Samuel, 2026-10-28: *"Though video 2 is done, I am still not happy with the output though, so I want this video to be better, so even though it's a refrence, we need it to use that as a foundation"*. Relayed by the General Manager, with the rule that nothing in video 2's delivered files changes: work on copies.
- **Starting set:** 18 comps from video 2's final, three per type (chart, counter, list, lower third, page/UI, card), lint-clean on every placement-independent rule: [[03-Areas/video-editing/clients/frontal-template-library|Frontal template library]] → Video 2 foundation set. Builders start from these, re-time entrances to this video's words and give each at least its `min_D`. They still need a render review on the eye-only rules before the first build.
- **Patterns this video must not repeat** (lint on video 2's 185 final comps): NeoMotionText sliding from the left (PosDir 3, kit default) on 84 tools; lower thirds above y 900 and pill text under 56 px over footage; a counter, its label and its box entering on one frame; chart labels landing together; the last element landing under 36 f before the cut on most beats. Full list in the library note.
- **Before the build:** set PosDir 0 as `frfx.ntext`'s default in this job's kit copy; copy `kits\lab_with_queue_2026-10-28.py` from the master kit over this job's `kits\lab.py` (queue hand-off) and the four pipeline scripts beside it; run [[03-Areas/video-editing/sops/video-pipeline-tools|the pipeline tools]]: lint on every beat, the render queue, Samuel's preview page per section.

## Night run 2026-10-28 → Thu 18:00 (Editor)

Samuel, 2026-10-28 ~23:00, after the weekly reset: *"I need speed and I need quality"*. Full video by Thu 2026-10-29 18:00 WAT for his creative director, *"a perfect first version of a full video without any mistakes"*. The bar is the LinkedIn Training video in Frontal v2.3.1; video 2 is *"a huge mess"*, used only as what not to repeat (its foundation set is still the starting point). His rules tonight: [[03-Areas/video-editing/samuel-review-card|review card]] → S1-S7 (static NeoLightSweep on every box; MotionBlur off; one by one; slow smooth camera on everything; media adj clip = NeoAnim + Vignette + MagicZoom; his intro adj clip; screen recordings as before video 2). His words in full: [[03-Areas/video-editing/ways-of-working|ways of working]] 2026-10-28.

- **His answers, 23:20:** shine = the NeoLightSweep node as a static sheen; the animated shine only when necessary, done as in the earlier videos. MotionBlur off, soft blur-in kept. No approval stops overnight (the Editor takes the recommended answers on the 14 capture calls and the hero calls, EN-04 included, and approves looks against the review card and the LinkedIn bar; the Editor builds the intro with his intro adj clip; Resolve and screen control are the Editor's until 18:00). Video 2's draft renders deleted on his yes (39.3 GB; v6_final.mp4 and the v7 finals kept; C: 65 GB free).
- **Usage at start:** weekly 0 %, 5-hour 1 % (23:28 WAT).
- **Cut checked 23:50:** *Cut v5 (Editor) - sections* is unchanged since 2026-10-26 (12,100 f, 159 clips, every in/out point identical), so the plan's word timings hold.
- **Watchdog** `editor-run-watchdog` re-armed hourly for this job (resumes the run after a power cut; disables itself after Thu 20:00). Session: "Editor run: 4. Cold Email Goldrush".
- **Stage 1, build bible:** workflow wf_2b6c2fc0-340, 10 Opus readers + a critic, docs in the job's `Docs\Night run 2026-10-28 (Editor)\bible\` (screen-recording bar, shine/motion, adj clips and camera, build card + review checklist, kit setup + runbook, plan delta ×3, sound, captures, critic).

**RESUME (2026-10-28 23:55):** job `Docs\RUN STATE.md` → ">>> NOW (NIGHT RUN". Next: read the bible → `MASTER PLAN.md` in the night-run folder → plan v2, captures, kit style patch → builds (Sonnet workers, Opus review) → install on *Visuals v1 (Editor)* → adj clips + MagicZoom → review render + preview pages for Samuel ~10:00 → his notes → sound → 4K final by 17:00.

**RESUME (2026-10-29 10:40):** job `Docs\RUN STATE.md` → ">>> NOW" (newest line on top of NEXT). Done: all 44 section units passed Opus review; installed on *Visuals v1 (Editor)* 10:06 (verify ok); sound placed 10:10 (13 music, 72 SFX); A1 Voice Isolation kept at Samuel's own 31 (DECISIONS #56). Running: polish round wf_b8da8d73-b0b (accent shine on 14 nodes, stray cursors, edge-cut words, light gaps, two timings). Next: reinstall the changed manifests with the queue stopped → chunked 4K render (runbook section 10) + seam_audio → loudness to -16 LUFS → Opus check → 1080p copy to Samuel, by about 13:00; his notes; final by 17:00. Open for Samuel: Voice Isolation 31, the HK-00 intro adj placement. Samuel's latest words: *"PC is back"* (after the restart he asked for at 08:30).

**RESUME (2026-10-29 17:25):** job `Docs\RUN STATE.md` → ">>> NOW" (15:50 v3 ROUTE line). Samuel edited *Visuals v1 (Editor)* himself and left 5 markers; his words: *"be as fast as you can in implementing the corrections, and render it in 1080p, V1 quickly"*. Markers rebuilt (DECISIONS #64), installed on a copy of his timeline as *Visuals v3 (Editor)* (his timeline never touched, #62), 1080p render v3 done 17:16, Opus check per chunk (#65): T1-08 r9 and two sound fixes go into **v3b** (`Renders3b 1080p (Editor)3b_1080_master.mp4`, rendering). Open for Samuel: the 5-frame A-roll sliver at 90-94 his hook B-roll disable uncovered; his 7 disabled clips are kept off (list in #65). Next: send v3b phone parts, he delivers to the creative director.
