---
type: sop
area: video-editing
status: active
source: claude-export
updated: 2026-09-25
tags: [sop, routerise]
---

# SOP — Routerise cut workflow (order of operations)

**Trigger:** starting the edit on any long-form talking-head video for [[03-Areas/video-editing/clients/routerise|Routerise]] (Routerise / Alex / Frontal). Established 2026-09-14, on the project "1. Taking a step back from Claude."
**Owner:** Samuel.
**Time it takes:** needs-input — not stated in the source document.
**Last used:** needs-input — not stated; the workflow's establishment date (2026-09-14) is the only date recorded, and it may not be the same as when it was last used.

## Inputs

- A-roll: Sony XAVC `C07xx.MP4` — 3840×2160, 29.97fps, camera audio is `pcm_s16be` stereo scratch (never used in the edit).
- Mic: DJI `TX02_MICxxx_<date>_<time>_orig.wav` — mono, 48 kHz, 24-bit. Always carries timecode `00:00:00:00`, so timecode-based sync is never possible.
- Target timeline: 23.976 fps, 1920×1080 — A-roll on V1, screen recording on V2, mic WAV on A1 at **+6 dB**.

## Steps

**The order matters. Doing step 3 before step 2 is the mistake** — see Failure modes.

1. **Sync**
   - If the camera's scratch audio is good: use Resolve's auto-sync on waveform —
     `MediaPool.AutoSyncAudio([video, audio], {"syncMode": resolve.AUDIO_SYNC_WAVEFORM})`.
   - If the camera audio is dead (happened on the 13 Sep shoot — flat noise floor at −62 dBFS, no speech at all): waveform sync is impossible. Measure the offset from picture instead: decode the A-roll to a small grayscale crop of the head, take the mean absolute inter-frame difference as a motion signal, and cross-correlate it against the mic's speech envelope. On that take this gave a single clean correlation peak at z = 14.8, landing on exactly 125 frames @ 29.97 (4.1708 s).
   - **Never derive the offset from file clock times.** The DJI mic clock and the Sony camera clock run ~143 s apart — on the 2 Sep shoot the filenames predicted the mic starting 108 s *after* the camera, when the real synced timeline had it starting 34.9 s *before*.

   ### Verified in practice — 2026-09-21 (project "Claude tests")
   The decision tree, run end to end and confirmed on the 13 Sep shoot (`C0785-001.MP4` + `TX02_MIC015…184035.wav`):
   1. **Try DaVinci's scriptable waveform sync first** — `MediaPool.AutoSyncAudio([video, mic], {resolve.AUDIO_SYNC_MODE: resolve.AUDIO_SYNC_WAVEFORM})`. It **returned `False`** here (both clip orders). A `False` return is itself the dead-camera-audio signal — treat it as "fall through to motion sync", not as an error.
   2. **Confirm why (optional):** `ffmpeg volumedetect` on the camera track read **mean −77.8 dB / max −60.8 dB** — no speech — vs the mic at −29.8 / −4.9. Dead scratch audio, exactly as this SOP anticipated.
   3. **Motion-correlation fallback (the one that worked):** offset = **+4.000 s ≈ 120 frames @ 29.97**, peak **z = 7.6** — consistent with the prior measurement for this shoot (~4.17 s / 125 frames). Positive = the mic started *before* the video by that much.
   - **You do not need the whole clip.** Analysing the **first ~6 minutes** of each stream was enough; the sync offset is a single constant, so aligning one good section aligns the entire clip. (Samuel's rule, 2026-09-21.)
   - **Reproducible implementation** (no numpy): `ffmpeg` extracts a 20 Hz motion signal — `fps=20,scale=32x18,format=gray,tblend=all_mode=difference,signalstats,metadata=print` (YAVG per frame = mean abs inter-frame diff), GPU-decoded with `-hwaccel cuda` (~1 min for 6 min of 4K). The mic envelope is 20 Hz RMS from `-ar 2000 -f s16le`. Cross-correlate with a plain-Python FFT; the peak lag is the offset. Script kept at the agent's build scratch; fold into the `routerise-cut` skill. `ffmpeg` is Gyan build 9.0.1, installed 2026-09-21.
   - **Still open:** apply the +4.0 s offset on a timeline and ear-check it; and decide how the skill *applies* the offset (media-pool linked audio vs. placing the mic on A1 at the computed offset). Next session.

2. **Ripple Delete Silence** — a waveform pass, before anything else.
   - Menu path: `Clip > Audio Operations > Ripple Delete Silence…` — **not** under Timeline > Audio, **not** under Timeline > AI Tools, and **not** in the timeline clip right-click menu. The dialog that opens is titled **Remove Silence**.
   - Select every clip on the timeline first. With V1 and A1 linked, the ripple carries picture and sound together, so the A-roll cuts land exactly where the audio cuts land.
   - Settings for this client:

     | Field | Value |
     |---|---|
     | Threshold | **−38.0 dB** |
     | Pre head | **0** frames |
     | Post tail | **1** frame |
     | Minimum to strip | **3** frames |
     | Cross fade audio | **off** |

   - Doing this step programmatically instead of through the dialog is fine, as long as the detection reads the actual waveform at this same threshold and minimum duration.

   ### Route Rise #3 run (2026-09-25): Samuel's method, the one to follow
   Samuel, after two scripted cuts dropped lines and drifted out of sync: *"We are working with the origingal synced video raw now. Use the ripple delete silence tool in Davinici resolve"*.
   - **Work on a duplicate of the synced raw timeline** (`A-roll synced (raw)` → `Cut v4 (Editor) - ripple silence`). V1 camera, V2 Tella, A1 mic. **Delete the Tella audio track first**: only one audio drives the cut.
   - Select every clip (click the timeline, Ctrl+A; check off-screen tracks are included), then `Clip > Audio Operations > Ripple Delete Silence…`. The dialog previews the silence to be removed in red on the clips. Move the threshold and watch the red: it must sit only in gaps, never on a waveform.
   - **The settings change per video.** Samuel's settings for #3: Threshold **−33.4 dB**, Pre head **0**, Post tail **3**, Minimum to strip **2**, Cross fade **off**. The dialog's defaults (−28.4 / 0 / 2 / 6) are not safe.
   - **Resolve's threshold isn't the same scale as an ffmpeg RMS reading.** The raw mic measured −60 dB room tone and −36 to −27 dB speech in 50 ms RMS windows. But −48 in the dialog marked nothing as silence, while −40 and −36 caught the same gaps. Pick the value from the red preview, not from the RMS numbers.
   - **Result on #3:** 41,137 → 19,426 frames, 331 clips, V1/A1 clip-for-clip aligned. Sync kept, because the tool cuts every selected track at the same frame.
   - Driving the dialog by screen control: typed values in *Post tail* were sometimes not accepted (typed 1, stayed 0). **Ctrl+Z after a timeline duplicate can undo the duplicate itself.** Check by script which timeline is current after any undo.

   ### 2b. Remove the leftover noise clips (after the silence pass)
   Ripple Delete Silence leaves small clips of room noise, breaths and clicks. Samuel: *"there is going to be some noise, left in the timeline as small clips, ensure those are gone"*.
   1. Duplicate the silence timeline (`Cut v5 (Editor) - noise clips removed`), export its FCP7 XML to the job's `Docs\`.
   2. `python 03-Areas/video-editing/scripts/noise_clips.py <xml> <raw mic wav>` measures every A1 clip: **noise** = no 50 ms window above −40 dB; **ambiguous** = 12 frames or shorter with sound at speech level; the rest is speech.
   3. Ripple-delete the noise clips with `Timeline.DeleteClips([V1, A1 and V2 items at each span], True)`. Check first that no V2 clip straddles a span. Don't match V2 clips with a nested loop over API calls: 331 × 263 calls timed out at 60 s. Grab each track once into tuples.
   4. Colour ambiguous clips **Pink** with a Pink marker for Samuel. Never cut them.
   5. Verify: every kept clip's `GetLeftOffset(True)` on V1, A1 and V2 equals the silence timeline's, V1/A1 aligned, no gaps, and the duration dropped by exactly the noise total.
   - #3: 73 noise clips (310 frames) removed, 6 ambiguous left Pink, 258 clips, 19,116 frames. One 7-minute recording break (mic 12:03–19:00) was nothing but noise clips.
   - **This order applies to every voice-over, not just Route Rise** (Samuel, 2026-09-24: *"use the waveform to cut out the gaps, never cut with the transcription, and then after that, remove the mistakes"*). Samuel's own VO at home needs a higher threshold because the room is noisier: see [[07-Agents/content/memory|Brand manager memory]], 2026-09-24.

   ### Frame grid — the audio cut must sit on the video cut (Samuel's correction, 2026-09-24)
   Samuel: *"Why do we have places where the video cut is not aligned with the audio cut … it must be the exact same place"*.
   - **Cause:** the DJI mic WAV carries metadata that makes Resolve read it at **29.97 fps**, and Resolve won't let you change it (`SetClipProperty("FPS")` returns False). On a **23.976** timeline most 29.97 source frames fall between timeline frames. Resolve places audio to the sample, so each audio edge sat 0–0.8 of a frame after its video edge, different on every clip. The giveaway by script: audio clips come out 1 frame shorter than their video when the next clip already sits on the track.
   - **Fix:** make a lossless copy of the mic with the metadata stripped: `ffmpeg -i mic.wav -map_metadata -1 -c:a pcm_s24le -write_bext 0 -rf64 never "<job>\Conformed audio\<name> (23.976 grid, lossless copy).wav"`. Check the audio MD5s match (`-f md5`). Resolve reads the copy at the project rate (23.976), so source frames and timeline frames are the same grid. The client raw is untouched.
   - Build the cut with that copy: mic start frame = floor(start × 23.976), same length D on every track. Check afterwards that every A1 clip has the same start and duration as its V1 clip.
   - The Tella audio (44.1 kHz, 30 fps) has the same problem. Leave it off the cut timeline; it stays on the raw sync timeline as a reference.

   ### A camera–mic clock drift exists on long takes
   On Route Rise #3 the mic ran about 129 ppm slow against the camera (offset −9.775 s at 2:30, −9.952 s at 25:00, linear within 7 ms). One constant offset puts the ends 2 frames out of sync. Measure the offset in three windows (motion correlation at 30 Hz, 240 s each) and fit a line; place each clip's camera source from that line.

   **Correction, 2026-09-25:** the drift model above is suspect. Clips placed with it in Cut v2/v3 felt out of sync to Samuel, and a camera-vs-Tella picture check found no trend. The raw timeline's single constant offset is the one Samuel checked as perfect. Don't rebuild cuts clip by clip from a drift line. Cut a duplicate of the synced raw with Ripple Delete Silence, so every track is cut at the same frame (see the #3 run above).

3. **Transcribe** — only after the silence pass, not before.
   - `MediaPoolItem.TranscribeAudio(False, False)` returns `True` immediately; the actual result arrives asynchronously — poll `GetTranscription()` for 20–40 s. Set `transcriptionLanguage = "en"` first.
   - Word-level timecodes come back in the **clip's own frame rate** (29.97 NDF): `seconds = (((h*60+m)*60+s)*30+f) / (30000/1001)`.
   - Alternative: `Timeline > AI Tools > Create Subtitles from Audio…`.
   - **Resolve's transcription strips disfluencies** — across 3,351 words on the reference video it surfaced exactly one "ah." It cannot be used to hunt "um"s. If that's ever needed, use a word-level Whisper pass that keeps disfluencies instead.

4. **Remove bad takes** — judged against the clips now sitting on the timeline, not against raw transcript runs.
   - He shoots in takes, restarting a line until it lands. After the silence pass, each clip is roughly one phrase, so a retake reads as **a run of clips whose text repeats in the next run.**
   - Detection that works: normalise each run's first ~10 words and compare against the next 3–4 runs with `difflib.SequenceMatcher`, threshold **0.6**, chained into clusters.
   - **Picking the keeper is a judgement call, not a rule.** Usually the last complete take, but not always — sometimes the last attempt splits across a long pause and an earlier single clean delivery is better. Read the cluster.
   - Leave alone: misspeaks that were only said once with no alternate take. Cutting them costs the sentence — flag them instead of removing them.
   - **Per-clip transcription (2026-09-24):** one WAV per waveform clip in a bin, then `Folder.TranscribeAudio()` does all of them (295 in about 2 minutes). Don't sleep inside a `run_script` call while waiting: it blocks Resolve, and nothing transcribes. Poll in separate calls.
   - **An empty transcript is not silence.** Resolve returns nothing for short lead-in clips ("The tools that", "And at the end,", "Let's get into it."). Transcribe each empty clip joined to the next clip, and read what it adds. On Route Rise #3 all 32 empty clips were real words, and one of them changed a keeper choice.
   - **A retake inside one clip** (no pause long enough for the silence pass): use the word times only to find where it is, then cut at the lowest waveform point between the two takes. The cut still lands on the waveform.
   - **Tella recordings are a split layout** (camera left, screen right), and during talking parts the screen often shows Alex's teleprompter, not a demo. Classify the screen second by second (2 fps 32×20 thumbnails of the screen region, distance to a teleprompter frame) to know where the real demos are, and to spot promised demos that were never recorded.

## Done when

All four steps have run across the whole timeline: audio/picture synced and linked, silence rippled out at the settings above, a transcript exists for the cleaned timeline, and repeated-take clusters have been resolved (kept/cut) or flagged where no alternate take exists. The timeline is then ready for the visual/graphics pass (see [[routerise-house-style|Routerise house style]] and [[fusion-node-system|Fusion node system]]).

## Failure modes

- **Transcribing before the silence pass** — Resolve's transcription inflates word end times, so a multi-second silence can sit inside what it reports as a single word. Segmenting on transcript word gaps then leaves whole seconds of dead air buried inside one clip — on the reference video this produced an 11-second clip with roughly 4 seconds of flat waveform through the middle of it. **The waveform is the only source of truth for silence** — always run Ripple Delete Silence first.
- **Camera audio is dead** — waveform auto-sync will fail silently or produce garbage. Switch to the motion-correlation method (see Step 1).
- **Trusting file clock times for sync** — the DJI mic clock and Sony camera clock drift independently (~143 s apart in one observed case); never use filename timestamps to compute a sync offset.
- **Judging bad takes against raw transcript runs instead of timeline clips** — the silence pass changes what counts as "a run." Always re-judge against the clips as they sit on the timeline after step 2.

## Notes

Client and account-context details (mic setup, footage quirks) are in [[03-Areas/video-editing/clients/routerise|Routerise]]. Established 2026-09-14 on project "1. Taking a step back from Claude" — note that document itself does not confirm which client/video it covers; see the open question logged in [[tsb-graphics-pipeline|Tsb graphics pipeline]].
Registered in [[systems-register]].
