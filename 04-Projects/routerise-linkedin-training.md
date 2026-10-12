---
type: project
area: video-editing
status: active
updated: 2026-09-29
source: manual
tags: [client, routerise, long-form]
---

# Route Rise — "3. The Most Valuable B2B LinkedIn Training You'll Ever Watch"

Client job through [[03-Areas/video-editing/clients/routerise|Route Rise]] (Alex, Frontal). Back to [[03-Areas/video-editing/video-editing|Video editing]].

**October order (by card dates):** [[04-Projects/routerise-cancel-apollo|Cancel Apollo]] → [[04-Projects/routerise-ai-b2b-marketing|AI B2B Marketing]] → **3 of 3**.

## Brief (ClickUp card, 2026-09-29)

- **Card:** 3. The Most Valuable B2B LinkedIn Training You'll Ever Watch · READY TO EDIT · long form video
- **Dates:** start Wed 2026-10-07 → **due Mon 2026-10-12, 1:30am WAT**, so it is delivered on **Sat 2026-10-10**. Sunday is buffer only.
- **Title options on the card:** The Most Valuable B2B LinkedIn Training You'll Ever Watch · I've Posted 1000 LinkedIn Posts. Only 6 Make Money · I've Posted 1000 LinkedIn Posts. Only 6 Made Money
- **Idea doc:** https://striped-thief-c4a.notion.site/3-The-Most-Valuable-B2B-LinkedIn-Training-You-ll-Ever-Watch-3e073bd1b02b81bc963bc741d36ce16a (not read yet)
- **Drive:** "6 - LinkedIn Masterclass", https://drive.google.com/drive/folders/1SkilG2mkNI69v06d2GqVKVXqAQay8m_C
- **Rate:** USD 333.33 unless Samuel says otherwise.

## Nothing downloaded yet (Samuel: save space)

Drive IDs for `drive_download.py` / Drive export:
- C0791.MP4 (14.06 GB): `1IbTMRyFAUjgcyEm7uts9_3MtjaD5j-nF`
- TX02_MIC024_20260927_181201_orig.wav (247.2 MB): `15v5v57D16nKG5Vs8NDar2Fy7XUlts2OC`
- TX02_MIC025_20260927_184202_orig.wav (14.5 MB): `1K6cFnSFkkNosuARNb09y1zrIJEz1tUcK`
- Google Doc "Script": `17WJKLIulz5kFfE16Tkz_836K8--94HLhKarSAAg41LM` (export `docs.google.com/document/d/<id>/export?format=docx`)
- No screen-share doc in the folder.

## Schedule (TickTick, 📹Video editing)

| When (WAT) | Step |
|---|---|
| Tue 10-06 1:00pm | Editor starts the download while AI B2B renders |
| Wed 10-07 7:00–8:00am | Resolve setup + sync |
| Wed 10-07 8:00am–1:00pm | Cut |
| Wed 10-07 7:00–9:00pm | Claude pass + visual cut sheet |
| Thu 10-08 7:00am–1:00pm, 7:00–9:00pm | Visuals |
| Fri 10-09 7:00am–1:00pm, 7:00–8:30pm | Visuals (Bible study at 8:30) |
| Sat 10-10 7:00am–1:00pm | Finish visuals + sound, render started by 1:00pm |
| Sat 10-10 7:00–9:00pm | Review the render, deliver |

**2026-10-10 (PA):** Samuel: *"I have not started"*. The schedule above is dead; its TickTick blocks were abandoned. Card still due Mon 2026-10-12 1:30am WAT. New plan not set.
**2026-10-10 (PA):** Samuel: *"They know about the linkeding video, I would start that on Monday"*. Start Mon 2026-10-12. New delivery date not recorded.

**2026-10-11 (PA):** Samuel: due **Fri 2026-10-16**. Edit block 1 Mon 10-12 7:00am–1:00pm in TickTick.

## Phase 1 run, 2026-10-12 (Editor)

Samuel, 2026-10-12: *"Download the video, cut it up and all the things we do in phase 1 before I revise the cuts"*. Script link he gave: the ClickUp doc *Alex Vacca Scripts → 3. The Most Valuable B2B LinkedIn Training You'll Ever Watch* (last updated 2026-09-29). Phase 1 = the B2B run's steps 1-8: setup, sync, ripple silence, noise clips, retakes, uhms, raw-vs-cut check, sections + transcript. Then stop for his revision.

- **Job folder:** `Desktop\Video edits\Routerise\3. The Most Valuable B2B LinkedIn Training You'll Ever Watch\` (straight apostrophe on purpose: the curly one breaks the MCP transport). Subfolders per the setup SOP plus `Conformed audio\`.
- **Two scripts exist.** ClickUp (1,183 words: *"I've posted thousands of times… six of them made me the most money"*, four patterns) and the Google Doc "Script" in the Drive folder (2,764 words: *"I've posted on LinkedIn more than 700 times… 70,000 followers… 33 sales calls"*). Both saved in `Docs\`. Which one Alex read is settled from the footage.
- **Drive folder unchanged since 2026-09-29:** C0791.MP4 + MIC024 (30:00) + MIC025 (1:45) + the Script doc. No Tella / screen-share doc.
- **Mics conformed** to 23.976-grid lossless copies in `Conformed audio\` (audio MD5s match the raws).
- **Resolve project** created in folder *Routerise*, same name as the job folder: 1080p, 23.976, YRGB, cache `C:\Users\repzy\Videos\CacheClip`. Samuel declined screen control for the power-bin drag, so the 13 bins were made by script with the power bin's names. An older project *Linkedin project* in the same folder holds unrelated thumbnail/promo clips; untouched.
- C: had 40 GB free before the 15 GB camera download.
- **Script used: the Drive Google Doc.** A whole-mic Whisper pass matched 168 of its 200 sentences (≥50 % 3-gram coverage), against 9 of 74 for the ClickUp script. The ClickUp doc is an earlier draft; the cut is judged against the Drive doc.
- **Sync:** camera scratch audio is alive (max −6.1 dB). MIC024 starts **1.35 s before** C0791 (camera-audio xcorr, z 51.6 at 0–6 min, the same 1.35 s at z 29.8 on 23:20–28:20: no drift). MIC025 continues seamlessly at camera 1798.8 s (z 23.1). Mic start trimmed 32 frames; MIC025 at record frame 43129.
- **A-roll synced (raw):** V1 C0791 (picture only, 0–45791), A1 MIC024 + MIC025 at +6 dB, all three linked, two blue lip-sync markers (1500, 44000).
- **Cut v1 (Editor) - ripple silence:** −33.4 / 0 / 3 / 2, cross fade off, by screen control (Samuel's yes). Run twice (all selected, then MIC025 alone: the tool takes one mic file per run). 45,791 → 38,393 frames, 933 clips, V1/A1 aligned.
- **Cut v2 (Editor) - noise clips removed:** levels split cleanly (speech clips peak −27 to −15 dB, noise −54 to −40). Removed 688 clips (6,061 f): every clip under −40 dB, plus −40 to −36 dB clips with no Whisper word, and the camera tail with no mic. **22:23, 245 clips, 32,195 frames**; V1/A1 on the same frames, no gaps, camera-to-mic offset unchanged on every clip. Kept for the retake pass: the quiet worded clips (134 "It", 206 "fuck.", 632 "of" in Cut v1 numbers) and 11 wordless clips above −36 dB.
- Working files: job `Docs\Editor working files (2026-10-12)\` (`li_clips.py`, `li_perclip.py`, `v1_clips.json`, `v2_clips.json`, `words_whisper.json`, the two XMLs, the B2B helper scripts). Per-clip WAVs: `Conformed audio\Per-clip WAVs (Cut v2)\`.
- **Cut v3 (Editor) - retakes removed:** 82 of 245 clips cut (`v3_cut_list.json`), each judged on its own per-clip Whisper text (`whisper_words.json`; wordless clips read joined to the next) against the Drive script, last clean complete take kept. **17:03, 163 clips**, V1/A1 aligned. Off-script chatter cut ("Perfect", "Fuck.", "I need five minutes. I have, like, seven lines more"). Raw-vs-cut check (`li_raw_vs_cut.py`): every script line said in the raw is in the cut (the misses are Whisper wording or a later retake of the same line).
  - **Judgement calls, flagged in the transcript:** kept take says **74,000 followers**, script 70,000. "Stay for the last one": kept the **sign-ups** take (script and the Post 6 payoff), not the later "meetings booked" take. "Fastest way to build trust": kept the take with *"Ask for their time before you ask for their money"* (script) over two later takes without it. Kept the later freestyle take of "most LinkedIn trainings give you templates" (Cut v2 24–25) over the script-tight one (23).
- **Cut v4 (Editor) - uhms trimmed:** `uhm_find.py` plus manual trims (in-clip restarts at Cut v2 42, 109, 129, 191, 229, the "You You" at 24, and long room-tone pauses at 24, 172, 179, 206 that sat at about −33 dB, so the finder had skipped them as loud). 61 keyboard lifts + Delete Gaps, every gap checked against the plan before closing (`trims_applied.json`). **15:39 (22,547 f), 177 clips**, no gaps, V1/A1 aligned, camera-to-mic offset unchanged on every clip.
- **Cut v5 (Editor) - sections:** clip colours + 12 duration markers: Hook Yellow · Post 1 product demo Blue · Post 2 guide Green · Post 3 tool post Purple · Mid-video CTA Pink · Post 4 shift post Teal · Post 5 "my team didn't want me to give this away" Navy (starts inside a clip at "Now, this next post", frame 12337) · Post 6 low-likes / best sign-up day Tan · Rule 1 Lime · Rule 2 Brown · Rule 3 Olive · Outro and CTA Violet. Stray lip-sync markers removed from the cut timelines (kept on the raw).
- **Transcript:** `Docs\Transcript - Cut v5 sections (2026-10-12).docx` (`li_sections.py` → `transcript_docx.py`), names and terms fixed against the script, red notes for the judgement calls.
- **Phase 1 done 2026-10-12 ~08:30. Next: Samuel revises the cut on *Cut v5*; then the visual plan.**

## Samuel's cut revision, 2026-10-12

Samuel: *"I just did final touches on the cut and cleaned up the timeline, added color corrections"*. He worked on *Cut v5 (Editor) - sections* itself: **14:35 (20,992 f), 233 clips**, markers removed, grade added (not to be touched). Diff against Cut v4 (`li_diff.py`, camera source frames): he removed **1,563 f (65 s) in 178 spans** and extended two spots (8 f).
- **81 head trims** (696 f, median 7 f), **39 tail trims** (416 f, median 5 f), **57 cuts inside clips** (434 f, median 6 f: breaths and short pauses), **1 whole clip** ("In one month.", 17 f).
- Content cuts: *"and add to your newsletter"* + *"never"* at the 190/191 join (66 f), the garbled *"and the posts people ask for look a lot"* (50 f), a 64 f false start before "First, the opening line is exactly what I built" (the finder had skipped that head as loud), 41–43 f spans at Cut v4 5043 and 9940.
- None of the Editor's 82 retake cuts or 61 trims was restored.

## Token budget for the visuals, 2026-10-12 (General Manager)

Samuel asked whether the visuals can be done at the B2B quality bar before his weekly limit runs out. Usage card at 12:20 WAT: weekly 80 %, resets **Wed 2026-10-14 23:00 WAT**. Measured from the Claude Code transcripts by script (cost units = API-price weights; this week 1 % of the weekly cap is at least ~4.7M units, so ~95M are left before the reset).

- **What past videos cost:** 4 AI Tools ~99M, Apollo ~114M (both on the old Pro account), **AI B2B ~569M, about 120 % of a Max week**. B2B phase 1 cost 11.5M; LinkedIn phase 1 cost 5.8M.
- **Where B2B went:** workflow subagents 390M (69 %). Self-QA fix and review rounds before Samuel saw anything 204M (36 %). Visuals v1 rejected 51M plus the v3 rebuild 129M. Intro build + 24-agent review 64M. Samuel's 61-marker round 54M. **Studies of past videos only 26M (4.5 %).** The mechanism: 79 % of all units were cache reads, because main sessions ran at 700k-965k context and long-lived builders kept growing theirs.
- **Repeating B2B as it happened on this 14:35 cut:** ~340-390M, about 75-85 % of a week. Does not fit.
- **Lean plan at B2B density** (~150-160 comps): ~125-170M in total. Before the reset: re-map + visual plan (~7M), one sample section (Post 1, ~6-8M), build waves with scripted installs and checks (~40-50M), ending near 91-92 %. After the reset, Thu-Fri: readable-size review + one fix round, MagicZoom pass, Samuel's marker round(s) (~30-45M), sound (~5M), render (~6M). Deliverable Fri 2026-10-16, tight.
- **Rules for these sessions:** no re-study (edit-grammar is the study); text plan then a sample section, each with Samuel's yes, before any fan-out; a fresh session per step, ending before ~250k context; 4-5 builders per wave, each owning 6-10 visuals, briefs carrying S0, the 2026-10-10 revision rules, house style §11b chain rules and the Resolve traps; no verifier swarms, replaced by the zero-token scripted checks after each install (lint, rawbreaks, identity, chain, NeoTextMotion range, blank-tile detector on stills) plus one look at readable size; Resolve work by external scripts with one summary line; check the usage card before every launch, stop at 92 % before the reset.
- **Waiting on Samuel:** (1) the QA trade: scripted checks + one look + one fix round, instead of the B2B adversarial rounds he asked for on 2026-10-07/08 (those don't fit before Fri); (2) who does the intro, him or the Editor; (3) density: ~150-160 comps as in B2B, or fewer.

**Samuel's answers, 2026-10-12:**
- **Sessions:** *"First we need to fix oversized sessions as it looks like that is what costs the most"* and *"We need to break sessions, or make them compact after a certain limit"*. Fixed before the visual plan.
- **Cross-checking stays:** *"I still do need cross checking but if the scripts can do the checking as well as the agents did, that's fine cause the quality still needs to be maintained"*. Scripted checks have to catch what the B2B reviewer agents caught; where a script can't (taste, readability), a look at readable size stays.
- **Intro:** *"You will do the intro, I would suggest the visuals for the intro so you know what to do"*. The Editor builds it from his suggested visuals; wait for them.
- **Density:** *"Density remains the same"*. ~150-160 comps for 14:35, as in B2B.
