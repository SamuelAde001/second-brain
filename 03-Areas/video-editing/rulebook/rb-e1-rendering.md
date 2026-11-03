---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: E1
---

# E1 · Rendering and delivery

> **Read when:** caching a timeline for his review, rendering a review copy or a final, naming a version, and on delivery day. **Client values:** resolution, frame rate and whether the client wants 4K (client overlay: K2 Alex, K3 Gamma; [[03-Areas/video-editing/clients/alex|Alex]], [[03-Areas/video-editing/clients/gamma|Gamma]]). **Status:** draft, not yet approved by Samuel.

## Rules
### Who decides
- **E1.1** Delivery is Samuel's. He watches every version before it goes to the client, the CD or Frame.io, and he sends it himself. The Editor never sends. ✅ *"I would only revise it after the render has been done before i send to the client"* (2026-10-10) 🔁 ×3
- **E1.2** Render a final only when he asks. No final render in an unattended run unless he says so. ✅ (2026-10-13) ⚙️
- **E1.3** When he says "just render", render and watch it. No cross-checking that round. ✅ *"help me render it again, don't crosscheck anything as I don't have anymore tokens, just watch the render"* (2026-10-27)
- **E1.4** Tell him the moment a render lands: push notification and the file right away, then run the checks. ✅ *"Why didn't you tell me"* (2026-10-29)

### Caching for his review
- **E1.5** (Superseded by A2.29, 2026-11-03: review on a render timeline, not a cache. Still for his decision.) Cache the whole timeline before you ping him, so he watches without stutter. Tell him when it is fully cached. 🔁 ×7 ✅ *"cache the whole video on the timeline first so that I can watch through everything without stutter"* (2026-09-23) See Q-E1.a.
- **E1.6** Re-cache only what changed. Never bulk-toggle Fusion output cache on a timeline that is already cached. ✅ *"the cache has been set back which is annoying"* (2026-10-09)
- **E1.7** Leave a clip uncached when he says he is reviewing it. ✅ *"Leave that clip uncached; I'm reviewing v5 now."* (2026-10-15)
- **E1.8** Watch caching and renders for crashes and stalls. If a comp stalls, profile it and fix it. 🔁 ×4 ✅ *"Profile a stalled comp and fix it."* (2026-10-24)
- **E1.9** Before restarting Resolve, save the project's render cache elsewhere so it need not rebuild. Delete that backup only on his yes after delivery. ✅ (2026-09-28)
- **E1.10** Check free space on C: before a long cache or render: a whole video needs 35-40 GB; never let C: drop under 10 GB. ✅ (2026-10-08) ⚙️
- **E1.11** Don't work in Resolve while `cache_tl.py` runs. Cache settings (DNxHR SQ, Render Cache User) and the background-cacher stall: [[03-Areas/video-editing/resolve-performance|Resolve performance]]. ⚙️
- **E1.12** Overnight: if the job is done and fully cached before 07:00, put the PC to sleep. When he asks, sleep it after a successful render too. ✅ *"If you are done and the video is fully cached and it's not yet 7am, put my computer to sleep"* (2026-10-15)

### Final render
- **E1.13** Never render a final from the render cache. Final and review renders run from a fresh Resolve with the cache off. 🔁 ×2 ✅ *"I can't use the cache for render, it is always lower quality"* (2026-09-28) ✅ *"my client would pick on it"* (2026-10-10)
- **E1.14** Never ProRes for a delivery. ✅ *"Not proRess, use H.264, proRess would be good large"* (2026-10-10)
- **E1.15** Quick version (V1 when urgent, or a fast correction round): H.264 MP4, 1080p. ✅ *"render it in 1080p, V1 quickly"* (2026-10-29)
- **E1.16** 4K master when he asks: his preset **4K H265 MASTER HIGH**. ✅ *"This is my master now"* (2026-08-29) 🔁 ×3
  - MP4, H.265 NVIDIA Main10, 3840×2160, Variable Bitrate 35,000 Kbps, Encoder Auto (NVENC), Preset Medium, Two Pass off, Lookahead 32, AQ Strength 8, Adaptive B-frames on, Data levels Video, AAC 320 kbps 48 kHz.
  - The 4K is upscaled on export from the 1920×1080 timeline. That is deliberate: 1080p keeps editing fast. ✅ (2026-09-14)
  - Frame rate = the timeline's (client overlay).
- **E1.17** Before using any saved preset, check its Codec field matches its name (`4k h264` was set to H.265). ⚙️
- **E1.18** Start the render early on delivery day (by 13:00; a full render once took 3 h 55 min). Render in Place heavy Tella clips first; it is faster. ✅ *"I noticed that Render in place is faster at rendering things"* (2026-09-29)

### Chunks and crashes
- **E1.19** Render in resumable chunks so a crash or power cut loses one chunk, not the video. About 2,010 frames a chunk, Resolve restarted before each (one 4K pass crashed at ~3,000 f; Resolve leaks memory). Monitor it. 🔁 ×3 ✅ *"render it in phases in case of a crash"* (2026-10-16)
- **E1.20** Join video only (stream copy). Render the whole timeline's audio in ONE audio-only pass and mux it on. Never join chunk audio (20 ms dropouts at every join). ⚙️ (2026-10-25; replaces the 2026-10-10 overlap-seam method)
- **E1.21** After a power cut: keep the partial file (rename it, never delete), check whether it can resume, otherwise restart the render. ✅ *"if not, restart the render"* (2026-09-29)
- **E1.22** A fix after review re-renders only the chunk (or range) holding it, plus its seams. Prove nothing else moved before re-joining. ✅ (2026-10-10) ⚙️
- **E1.23** One script owns Resolve for renders (the render queue); helpers drop requests in its folder and never drive Resolve themselves. ⚙️ (2026-10-28)
- **E1.24** Scripts and Deliver-page traps (`finish\finish.sh`, `render_chunks.sh`, `resolve_guard.py preflight --for render`, absolute `TargetDir`, `VideoQuality` returns False, `DeleteAllRenderJobs()` after a restart): [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] and [[03-Areas/video-editing/sops/video-pipeline-tools|video pipeline tools]]. Open when you run a render. ⚙️

### Check the render
- **E1.25** Before you call a render good: full decode clean, every frame on its timestamp, exact chunk frame counts, audio and video the same length and aligned, seams clean, flash and media-offline scan, a contact sheet looked at. Check each chunk as it lands. ⚙️
- **E1.26** Loudness: see [[03-Areas/video-editing/rulebook/rb-d2-sound-effects|D2]] → Mix and loudness (target not confirmed, Q-D2.a).

### Names and versions
- **E1.27** Name a version the way he names it. A re-render after his or the CD's corrections is v2 next to his v1; quick correction rounds follow on (v3, v3b). ✅ *"render it again same way as before, name it v2"* (2026-10-16) 🔁 ×3
- **E1.28** After CD corrections: implement, check, render 4K, send as V2 (for him to watch first). ✅ *"We render it in 4K and we send it as a V2"* (2026-10-26)
- **E1.29** A re-rendered file always gets a new file name. A render written over the same path keeps showing old frames in Resolve. ⚙️
- **E1.30** Send him a 1080p watch copy and phone-size parts for review on his phone. ⚙️ (2026-10-29)

### After delivery
- **E1.31** When he starts a new Route Rise video, the last one is delivered. Add its delivered-projects row the same day without asking. ✅ *"I would never start working on a new routerise video if I haven't delivered the last"* (2026-10-14) → [[03-Areas/video-editing/delivered-projects|delivered projects]]
- **E1.32** Then run the end-of-job review ([[03-Areas/video-editing/rulebook/rb-e2-revisions-and-quality|E2]]).

## Never
- **E1.33** Never a final from the render cache. ❌ ✅ (2026-09-28, 2026-10-10)
- **E1.34** Never ProRes for delivery. ❌ ✅ (2026-10-10)
- **E1.35** Never send anything to the client, the CD or Frame.io yourself. ❌ ✅
- **E1.36** Never render the whole 4K in one pass. ❌ ⚙️

## Pictures
- (no picture yet: a screenshot of his 4K H265 MASTER HIGH preset on the Deliver page)

## Questions for Samuel
- **Q-E1.a** How do you review now? Until 2026-10-16 you reviewed from a fully cached timeline (seven times). Since video 2 (2026-10-24) the Editor sends a 1080p review render plus phone parts, and on video 4 that was the plan. → Options: (1) cached timeline; (2) 1080p render + phone parts; (3) both. My pick: (3): the render for your phone, the cache for marking in Resolve. → Samuel (2026-11-03, A2.29): a render, imported onto its own timeline for his markers; no cache for review.
- **Q-E1.b** Delivery file name. No rule exists; only "v1/v2" and the job title. → Options: (1) `<video title> v<N>.mp4` in the job folder; (2) your own pattern. My pick: (1).
- **Q-E1.c** Upload. You wanted a system that spots a finished render, uploads it to the right Frame.io folder and posts the link on Slack for the CD (2026-09-28, *"we would work on a system for this later"*). → Options: (1) build it now; (2) keep sending by hand. My pick: (2) until you say; you watch every version first anyway.

## Sources
Replaces and draws on [[03-Areas/video-editing/routerise-house-style|Route Rise house style]] §1 and §11, [[03-Areas/video-editing/troubleshooting|troubleshooting]] §2-§4, [[03-Areas/video-editing/resolve-performance|Resolve performance]], [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]], [[03-Areas/video-editing/sops/unattended-run|unattended run]], [[03-Areas/video-editing/ways-of-working|ways of working]], the AI B2B, LinkedIn, 10000 SaaS, Cold Email and Gamma job notes.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
