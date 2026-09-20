---
type: sop
area: video-editing
status: active
source: claude-export
updated: 2026-09-20
tags: [sop, routerise]
---

# SOP — Routerise cut workflow (order of operations)

**Trigger:** starting the edit on any long-form talking-head video for [[../clients/routerise]] (Routerise / Alex / Frontal). Established 2026-09-14, on the project "1. Taking a step back from Claude."
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

## Done when

All four steps have run across the whole timeline: audio/picture synced and linked, silence rippled out at the settings above, a transcript exists for the cleaned timeline, and repeated-take clusters have been resolved (kept/cut) or flagged where no alternate take exists. The timeline is then ready for the visual/graphics pass (see [[../routerise-house-style]] and [[../fusion-node-system]]).

## Failure modes

- **Transcribing before the silence pass** — Resolve's transcription inflates word end times, so a multi-second silence can sit inside what it reports as a single word. Segmenting on transcript word gaps then leaves whole seconds of dead air buried inside one clip — on the reference video this produced an 11-second clip with roughly 4 seconds of flat waveform through the middle of it. **The waveform is the only source of truth for silence** — always run Ripple Delete Silence first.
- **Camera audio is dead** — waveform auto-sync will fail silently or produce garbage. Switch to the motion-correlation method (see Step 1).
- **Trusting file clock times for sync** — the DJI mic clock and Sony camera clock drift independently (~143 s apart in one observed case); never use filename timestamps to compute a sync offset.
- **Judging bad takes against raw transcript runs instead of timeline clips** — the silence pass changes what counts as "a run." Always re-judge against the clips as they sit on the timeline after step 2.

## Notes

Client and account-context details (mic setup, footage quirks) are in [[../clients/routerise]]. Established 2026-09-14 on project "1. Taking a step back from Claude" — note that document itself does not confirm which client/video it covers; see the open question logged in [[../tsb-graphics-pipeline]].
Registered in [[systems-register]].
