---
type: project
area: video-editing
status: active
updated: 2026-10-18
source: manual
tags: [client, routerise, long-form]
---

# Route Rise — "2. I Gave Claude 10,000 SaaS Companies... Here's What I Found"

Client job through [[03-Areas/video-editing/clients/routerise|Route Rise]] (Alex, Frontal). Back to [[03-Areas/video-editing/video-editing|Video editing]]. Order and token budget: [[04-Projects/routerise-videos-2-and-4-plan|videos 2 and 4 plan]].

## Brief (ClickUp card, screenshot 2026-10-18)

- **Card:** 2. I Gave Claude 10,000 SaaS Companies... Here's What I Found · READY TO EDIT · tags edit-assigned, long form video
- **Dates on the card:** start today (Sun 2026-10-18) → due Thu 2026-10-22. Samuel, 2026-10-18: he starts Mon 2026-10-19, and the deadline can slip: *"I have no issues delaying as long as I have a perfect video"*.
- **Card holds:** 3 attachments, 2 subtasks, checklist 0/17. Not read yet.
- **Thumbnail:** "10,000 Startups" over four phone screens (Slack, Notion, Stripe, Clay).
- **Rate:** USD 333.33 unless Samuel says otherwise ([[03-Areas/video-editing/clients/routerise|client note]]).
- **Job folder (to make):** `Desktop\Video edits\Routerise\2. I Gave Claude 10,000 SaaS Companies... Here's What I Found\`. Straight apostrophe on purpose (the curly one breaks the MCP transport, 2026-10-12).

## Status

- 2026-10-18: documented, nothing started. Next: phase 1 of the plan (brief, footage, setup, sync, phase 1 cut, text visual plan) before the Wed 2026-10-21 23:00 reset.
- Usage readings per phase go here.

## Phase 1 run, 2026-10-19 (Editor)

Samuel, 2026-10-19: *"So let's download it and work on it, prep the video the way we normally do, till the cuts and the transcription as usual"*. Links he gave: Drive folder `7 - 10,000 SaaS Companies` and the ClickUp doc *Alex Vacca Scripts → 2. I Gave Claude 10,000 SaaS Companies…* (the card itself was not opened: no link to it). He OK'd switching Resolve off his *Welcome to called to Edit* project and screen control for the GUI steps.

- **Usage at start:** weekly 76 %, 5-hour 13 % (17:40 WAT).
- **Drive folder:** C0792.MP4 (9.5 GB, 21:31.8, 29.97, camera audio alive), TX01_MIC011 (21:23), TX01_MIC010 (10.7 s, uploaded twice, identical: pre-roll chatter before the camera started, not used), and the Script Google Doc. No Tella / screen recording, though the ClickUp script plans Claude Code demos.
- **Two scripts again.** ClickUp doc (Maria Fernanda Alvarez, 2026-09-30: "These two SaaS companies… $441 million more a year", 10,000 companies, prompt demos) and the Drive "Script" doc (2,318 words: Baremetrics vs Apollo, 3,000 companies, four patterns: proof, headline result, sales hiring, revenue per customer). **Alex read the Drive doc:** a whole-mic Whisper pass matched 156 of its 181 sentences, against 1 of 103 for ClickUp. Both saved in the job's `Docs\`.
- **Job folder** made per the setup SOP plus `Conformed audio\`; MIC010 and MIC011 conformed to 23.976-grid lossless copies (audio MD5s match).
- **Sync:** MIC011 starts **3.27 s after** the camera (camera-audio xcorr, z 47.0 at 0–6 min; 0.00 s residual at z 51.9 on 15:00–21:00: no drift). Mic on A1 at record frame 78.
- **Resolve:** creating the project while his project sat on the Deliver page hung Resolve (Not Responding, his project saved first); restarted with `restart_resolve.py`, then `CreateProject` worked. Project in folder *Routerise*, same name as the job folder, 1080p 23.976 YRGB, cache `C:\Users\repzy\Videos\CacheClip`, 13 bins by script. *A-roll synced (raw)*: V1 C0792 picture only, A1 MIC011 +6 dB, linked, blue lip-sync markers at 1500 and 29500.
- **Cut v1 (Editor) - ripple silence:** −33.4 / 0 / 3 / 2, cross fade off, by screen control; red only in gaps. 30,972 → 20,677 f, 320 clips, V1/A1 aligned.
- **Cut v2 (Editor) - noise clips removed:** 27 clips under −40 dB (101 f) ripple-deleted. 20,576 f (14:18), 293 clips, no gaps, V1/A1 aligned.
- Working files: job `Docs\Editor working files (2026-10-19)\` (LinkedIn helpers copied and adapted). Per-clip WAVs: `Conformed audio\Per-clip WAVs (Cut v2)\`.
- **Cut v3 (Editor) - retakes removed:** 77 of 293 clips cut (`v3_cut_list.json`), judged on per-clip Whisper text against the Drive script, last clean complete take kept. 16,447 f, 216 clips, V1/A1 aligned. Off-script chatter cut ("Perfect. Thank you", "What do you think?"); Alex's on-camera "remove these parts" honoured (the "one company … 15 and 50 million" line).
- **Cut v4 (Editor) - uhms trimmed:** `uhm_find.py --tight` (new flag, Samuel's LinkedIn trim depth) + 6 manual in-clip restarts, 68 keyboard lifts (every gap checked against the plan) + Delete Gaps. **16,001 f (11:07), 219 clips**, no gaps, V1/A1 aligned, camera-to-mic offset the same on every clip. The first build also lifted a "mid-filler" in Cut v2 clip 117 that was really "they are" (*"But they are not"*); that build was renamed *_old Cut v4 (c117 words cut) - delete* (Samuel deletes it) and Cut v4 was rebuilt without that trim.
- **Cut v5 (Editor) - sections:** clip colours + 12 duration markers: Hook (Baremetrics vs Apollo) Yellow · The study Blue · How Claude did it Green · Pattern 1 Proof Purple · Pattern 2 Result in the headline Teal · Pattern 3 Don't hire sales before it sells Navy · Pattern 4 More revenue from existing customers Tan · What barely made a difference Lime · What ties it together Brown · Where to start this month Olive · Honest limits Orange · Outro and CTA Violet.
- **Transcript:** `Docs\Transcript - Cut v5 sections (2026-10-19).docx` (`sections.py` → `transcript_docx.py`), Whisper's names fixed against the script, red notes for the judgement calls. Raw-vs-cut check (`raw_vs_cut.py`): nothing said on camera is missing; the flagged lines are Whisper wording or a later take kept on purpose.
- **Judgement calls (in the transcript):** Baremetrics: kept the last complete take ("about $1 million", "a few million"); an earlier take (Cut v2 2–5) says the script's 1.2 million / 4 million. Data cost "about $50" (script 8 dollars). "were 40% more likely to fail" (script 20 to 40%). Reply rate "around 1%" (script 0.64%). Kept the later freestyle "A new salesperson is not gonna fix that…" over "they just inherit the same fuzzy target".
- **Usage at end:** weekly 76 % (no measurable change), 5-hour 1 % after its reset. Phase 1 costs about nothing on the weekly card.
- **Phase 1 done 2026-10-19 ~20:45 WAT. Next: Samuel revises the cut on *Cut v5 (Editor) - sections*; then the text visual plan.**
- **2026-10-20: Alex sent Frontal brand kit v2.3.1 (must follow).** This video's visuals are the first in the new brand: no orange, no Geist. Study and style frames done ([[04-Projects/frontal-rebrand-video-kit|rebrand project]], job `Docs\Frontal brand study (Editor)\`); the text visual plan and the build wait on Samuel's answers there and the Frontal Fusion kit.

## Visual plan run, 2026-10-20 night (Editor)

Samuel, 2026-10-20 ~21:50 WAT, by voice before bed: start the visuals; transcribe his cut, plan the best visual for every section in the new brand, plan the nodes, get every resource from Chrome (B-roll, screen recordings, pictures, UI), UI *"accurate down to the last dot"*, show don't tell, our normal pacing, nothing he corrected before comes back, *"I don't want to make one single correction"*. Creative: text behind Alex, 3D, layered effects, beautiful motion design, *"when my creative director sees it, he's like, wow"*. Budget: weekly **81 % → 95 %**, then stop (he needs tokens for webinar planning on Wed). Pace agents; no failed or lost agents. Word-for-word brief: job `Docs\Visual plan v1 (Editor)\PLAN BRIEF.md`.

- **His answers (2026-10-20 ~22:00):** Claude demo = **Claude Code** in a terminal, rebuilt from real captures. B-roll: *"Stock B-roll just applies to stock B-roll from stock websites, real UI, and websites and all we have been using is fine, even AI B-roll is fine"*. Tonight = plan + captures + style frames; Fusion build after the Wed 2026-10-21 23:00 reset.
- **His cut:** *Cut v5 (Editor) - sections* is now 16,076 f (11:10.5), 217 clips (was 16,001 / 219). Section markers unchanged; ranges re-read from clip colours.
- **Usage at start:** weekly 81 %, 5-hour 3 % (21:52 WAT).
- Permissions taken before he slept: screen control (Resolve full; Explorer, TickTick click/full for focus), keep-awake, his Chrome (Baremetrics, Apollo, Claude, Wayback, Flow open without prompts).

### RESUME (Editor)
- Live state: job `Docs\RUN STATE.md` → ">>> NOW". Plan folder: `Docs\Visual plan v1 (Editor)\`.
- Steps: W1 prep (re-timed transcript, brief A + B) + 3 concepts + judge → W2 planners g1-g5 + reviewers + creative-director pass → W3 captures + Flow B-roll → W4 style frames → morning report. Stop at 95 % weekly.
