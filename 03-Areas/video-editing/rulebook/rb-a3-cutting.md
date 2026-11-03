---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: A3
---

# A3 · Cutting

> **Read when:** phase 1, the cut (after sync, before the transcript doc), and when diffing Samuel's cut revision. Editor and any cut helper. **Client values:** none (silence settings are set per video). **Status:** draft, not yet approved by Samuel.

## Rules
### Order and gates
- **A3.1** Fixed order: sync → Ripple Delete Silence on the waveform → remove leftover noise clips → per-clip transcript → remove retakes and mistakes → uhm and pause pass → raw-vs-cut check → read the whole transcript. Transcribing before the silence pass is the mistake. ✅ 🔁×2 *"use the waveform to cut out the gaps, never cut with the transcription, and then after that, remove the mistakes"* (2026-09-24) · ✔ 2026-11-03
- **A3.2** Cut every synced track together (camera, mic, screen recording). Picture must never drift from the audio. ✅ *"Remove the gaps with the waveform (Including the screen record all synced together)"* (2026-09-24) · ✔ 2026-11-03
- **A3.3** Work on a duplicate of the original synced raw. Keep each stage as its own named timeline: Cut v1 silence → Cut v2 noise removed → Cut v3 retakes removed → Cut v4 uhms trimmed → sections. ✅ *"We are working with the origingal synced video raw now"* (2026-09-25) ⚙️ · ✔ 2026-11-03
- **A3.4** Sectionalise the cut into its major sections; split talk from demo. It must be right before anything else proceeds. ✅ (2026-09-20, 2026-09-25) · ✔ 2026-11-03
- **A3.5** Phase 1 ends at cut + transcript + sections. Then stop and wait for Samuel's cut revision. No visual plan until he says the cut is done. ✅ 🔁×6 *"cut it and as we normally do and wait till I revise the cuts"* (2026-10-30; also 10-06, 10-12, 10-19, 10-20, 10-26) · ✔ 2026-11-03
- **A3.6** Build on his revised timeline: duplicate it, keep his trims, never touch his grade or noise reduction. ✅ 🔁×2 *"I just did final touches on the cut and cleaned up the timeline, added color corrections"* (2026-10-12; again 2026-10-31) · ✔ 2026-11-03
- **A3.7** Diff his revised cut against yours on every job he touches (`cut_diff.py`, A1 source ranges per clip) and write the lesson into the Editor memory. ⚙️ · ✔ 2026-11-03
- **A3.8** Fast, but no mistakes. Write down the cut method used on each job. ✅ *"Document the methods we used and continue work, don't waste time but don't make mistakes"* (2026-09-25) · ✔ 2026-11-03

### Silence
- **A3.9** Use Resolve's own `Clip > Audio Operations > Ripple Delete Silence…`, not scripted cuts. Delete the Tella audio track first so one mic drives it. Select every clip, off-screen tracks included. ✅ *"Use the ripple delete silence tool in Davinici resolve"* (2026-09-25)
- **A3.10** Settings change per video. Move the threshold until the red preview sits only in gaps, never on a waveform. His #3 settings: threshold −33.4 dB, pre head 0, post tail 3, minimum 2, cross fade off. The dialog defaults are not safe; ffmpeg RMS numbers don't map to the dialog. ✅ *"find the best settings that fit the video, without cutting out words"* (2026-09-25)
- **A3.11** One mic file per run. After the pass, count clips per source and re-run on any file it skipped (a DJI 30-minute split). ⚙️
- **A3.12** A scripted silence cut (per-frame mic peak at −40 dB, head 1 f, tail 3 f, min gap 2 f) only when screen control is refused and camera, mic and timeline share one frame rate. See Q-A3.a. ⚙️ (2026-10-30)

### Noise
- **A3.13** After the silence pass, remove every leftover noise clip: room noise, breaths, clicks, camera tail past the mic end, camera pieces with no mic under them. ✅ *"there is going to be some noise, left in the timeline as small clips, ensure those are gone"* (2026-09-25)
- **A3.14** Noise test: under −40 dB is noise; −40 to −36 dB with no Whisper word is noise; any clip under ~1 s with no word, between sentences that read complete, is noise. A −40 dB rule alone was too strict. ✅ (2026-09-25) ⚙️ (2026-10-12)
- **A3.15** Before deleting a noise clip, check no real word sits in it (word-timed transcript). Whisper's stock line "Um, so, uh, we start with the list" on a 7-13 f clip is noise. ⚙️

### Retakes and mistakes
- **A3.16** Decide, don't flag. Keep the last clean complete take, across clips and inside one clip. No colour flags or markers on the cut; colour a clip only when its content exists nowhere else. ✅ *"I removed most of your clutter"* (2026-09-25)
- **A3.17** Picking the keeper is judgement: usually the last complete take, but read the whole cluster (a last attempt split by a long pause can lose to an earlier clean one). Write each call (which take, why) as a red note in the transcript for his cut review. ⚙️
- **A3.18** Judge retakes from per-clip transcripts of the timeline after the silence pass (one WAV per clip). Never from a whole-file transcript or a subtitle track mapped by midpoint: they drop repeats and put words on the wrong clip. ✅ 🔁×2 (2026-09-25, 2026-10-06)
- **A3.19** An empty transcript is not silence: transcribe each empty clip joined to the next and read what it adds. ⚙️
- **A3.20** Retake inside one clip: find it by word times, cut at the lowest waveform point between the two takes. ⚙️
- **A3.21** Check every restart for a second restart, and check whether a line you restored is a retake of a later clip. A retake cluster is a sentence on its own, not the first sentence plus its restarts. ✅ (2026-09-25)
- **A3.22** A fragment the next clip continues (not repeats) is part of the kept sentence: keep it ("Inboxes are" + "full of"). ✅ 🎬 (his revision, 2026-10-26)
- **A3.23** A misspeak said once with no other take: leave it (cutting it costs the sentence). ⚙️
- **A3.24** Cut what Alex tells the editor to remove on camera ("remove this") and off-script chatter; note it in the transcript. Cut a leading "Okay," on lines. ⚙️

### Never lose a line
- **A3.25** Never cut something meant to be in the video. Crosscheck the client's original script. The script's hook must be in the cut; Alex often records the opener several times at the very top. ✅ 🔁×2 *"never cut something that was meant to be in the video, crosscheck the clients original script"* (2026-09-25)
- **A3.26** Cut to what is spoken, not what is written: Alex goes off script. The script decides only a word Whisper is unsure of. ✅ (2026-09-20) 🎯 (2026-10-26)
- **A3.27** Before hand-over, run the raw-vs-cut check (`raw_vs_cut.py`): every raw mic line under 50 % covered by the kept A1 must be a removed retake, an on-camera "remove this", or noise. Read each by eye; restore what isn't said elsewhere. Add the 3-gram check so nothing said only once is lost. ⚙️
- **A3.28** After every delete, verify each kept clip's source position on V1, A1 and V2 is unchanged, no gaps, V1 and A1 equal. ⚙️
- **A3.29** If the kept take says a different number from the script, keep the take and flag the number in the transcript. The on-screen number follows what Alex says (C4). ⚙️ 🎯 (2026-10-26)
- **A3.30** After the final cut, read the whole transcript to confirm it makes sense. ✅ (2026-09-25)

### Uhms, pauses, heads and tails
- **A3.31** No uhm left in. The cut isn't done until the uhms are out. ✅ 🏢 *"left in parts that was obviously retakes, left in some uhms"* (2026-09-25)
- **A3.32** Uhm pass: `uhm_transcribe.py --cuda`, then `uhm_find.py --fps`, lifts by keyboard on a duplicate, Delete Gaps, check by script. Steps: the cut SOP step 5. ⚙️
- **A3.33** Re-transcribe every mid-filler clip without the filler prompt before lifting it: the prompt turns real words into "uh" ("But they are not" → "But uh, not"). ⚙️
- **A3.34** A teleprompter read has few uhms. The work is loose tails, long pauses, in-clip restarts and stutters ("the, the, the"). Read per-clip text for single-word stutters. A finder "loud" SKIP over ~1 s is likely a false start or room-tone dead air: trim it by hand. ✅ 🎬 (his LinkedIn trims, 2026-10-12)
- **A3.35** Heads: trim to the first word onset (he took a median 6-7 f more off). Trim false-start head words ("The", "So", "what", "that"). ✅ 🎬 (2026-10-12, 2026-10-20, 2026-10-26)
- **A3.36** Tails: ~4-5 f after the last word, not ~2 f. Where a thought or section ends, leave more breath (up to ~13 f into a chapter). ✅ 🎬 (2026-10-26, replaces the 2026-10-12 ~2 f; video 2 diff 2026-10-20)
- **A3.37** Pauses inside clips: cut anything over ~0.5 s down to ~0.22-0.25 s; remove wordless 3-8 f pause clips. 🎬 (2026-10-12, 2026-10-20)
- **A3.38** Leave a small natural gap uncut now and then, so the cut doesn't feel machine-made. 🎯 (2026-10-22) See Q-A3.c.
- **A3.39** Screen demos: trim the 5-31 f pauses inside dictated prompts, but keep a 1.7-2.4 s silent hold after each prompt where the screen changes, so the viewer sees the result. ✅ 🎬 (2026-09-29)
- **A3.40** A-roll shape in his finals: a jump cut about every 2-4 s (median ~2.4-2.8 s), held up to ~11 s when the point earns it; every clip at 100 % speed. Pacing detail: C15. 🎬

### Superseded (kept for the record)
- **A3.41** ~~Fixed client settings −38.0 dB / 0 / 1 / 3~~ (2026-09-14) → per-video settings from the red preview, A3.10 (2026-09-25).
- **A3.42** ~~If unsure which take is best, keep both and colour the uncertain one~~ (2026-09-25, said twice) and ~~Pink / Orange clips with markers for Samuel~~ → decide, no clutter, A3.16 (his verdict, same day).
- **A3.43** ~~Tails ~2 f / `--tight` as is~~ (2026-10-12) → A3.36 (2026-10-26).
- **A3.44** ~~On-screen cards follow the script number~~ (2026-10-06) → A3.29 (2026-10-26).

## Never
- **A3.45** Never cut from the transcript; never transcribe before the silence pass. ❌ *"never cut with the transcription"* (2026-09-24)
- **A3.46** Never rebuild a cut clip by clip with a drift model, and never cut in a way that knocks picture out of sync. ❌ *"making the video go out of sync, you are over complicating things"* (2026-09-25)
- **A3.47** Never hand over a cut with obvious noise, retakes or uhms left in. ❌ *"you made some stupid mistakes still, left in parts that where obvously noise"* (2026-09-25); again on Gamma ❌ *"I adjusted some of the cuts because the cuts were bad"* (2026-10-31)
- **A3.48** Never lift a "filler" that is a real word, and never cut one word too far into a kept sentence. ❌ (2026-10-19, 2026-10-26)
- **A3.49** No transitions on A-roll (cuts only) and no retiming. 🎬 🏢

## Pictures
- (no picture yet: a before/after waveform still of one of his tail/head trims from the video 4 cut diff, and the Ripple Delete Silence red preview sitting only in gaps)

## Questions for Samuel
- **Q-A3.a** Silence method. You set Ripple Delete Silence in the dialog as the method and scolded scripted cuts (2026-09-25). On Gamma Ep. 12 screen control was refused, so the Editor cut silence by script at −40 dB (2026-10-30), and on 2026-10-31 you said the cuts were bad (not clear if silence, retakes or trims). → Options: (1) dialog always; (2) script allowed only when screen control is refused and every frame rate matches, then diff your revision. My pick: (1) by default, (2) as the fallback, and diff the Gamma revision to find what was bad.
- **Q-A3.b** Genuinely unsure takes. Your verdict: decide, flags are clutter (2026-09-25). The Editor profile still says ask you on a real judgement call. → Options: (1) always decide and note the call in the transcript; (2) decide, but ask in chat when the two takes carry different content (e.g. a different number). My pick: (2).
- **Q-A3.c** The creative director wants a small natural gap now and then (2026-10-22); your own revisions tighten every pause (178 spots on LinkedIn, 2026-10-12). → Options: (1) tight everywhere; (2) tight, with the extra breath only at thought and section ends (A3.36). My pick: (2).

## Sources
Draws on and replaces the rules in [[03-Areas/video-editing/sops/routerise-cut-workflow|Route Rise cut workflow]] (open it for the GUI steps, script commands and failure modes), [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] (open for dialog and API quirks), [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]], [[03-Areas/video-editing/routerise-house-style|Route Rise house style]], [[03-Areas/video-editing/ways-of-working|Ways of working]], [[03-Areas/video-editing/creative-director/creative-director-standard|Creative director standard]], [[07-Agents/video-editor/memory|Editor memory]].

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
