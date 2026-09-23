---
type: knowledge
area: video-editing
status: needs-input
source: claude-export
updated: 2026-09-23
tags: [troubleshooting, resolve]
---

# Troubleshooting log

Recurring problems in the edit and what actually fixed them. Distilled from Claude conversations, not the Brain's own testing — where a fix was proposed but Samuel never confirmed it worked, it is marked **proposed — unverified**, not solved. Do not upgrade a proposed fix to solved without Samuel's own confirmation (AGENTS.md §5.7).

**Appending a new entry:** add it at the bottom, following this shape — Date · Status · Symptom (as it appeared) · Cause (once found) · Fix that worked (or Proposed fix — not confirmed) · What to check first next time.

Related: [[toolchain]] for the hardware/software this runs on. [[routerise-house-style]] §11 has a separate, earlier set of confirmed Resolve-stability crash causes (Fairlight device-scan crash, `ExportCurrentFrameAsStill()` crash, render-resolution mismatch) — check there too before assuming a crash is new.

---

## 1. M4V media offline mid-file, plays fine at the start

**Date:** 2026-08-11 · **Status:** solved

**Symptom (as it appeared):** A client-supplied `SITE 1_ISP_A CAM COMPRESSED.m4v` (portrait 4K, ~51 min, H.264 High Profile Level 5.2, reported 59.99fps) played back fine in VLC but showed "Media Offline" for parts of the timeline in Resolve, while the beginning played normally.

**What was ruled out, in order:**
1. **Variable frame rate.** VLC showed an odd repeating rate (`59.939393`) which looked VFR-like at first. Ruled out once Resolve itself parsed the file's own metadata cleanly as standard NTSC `59.940` (186,681 frames, end TC `00:51:51:21` — the math checks out exactly), meaning Resolve read the container/timecode fine. Not a frame-rate confusion problem.
2. **Hardware decode choking under VRAM pressure** (Quadro T1000, 4GB) on a demanding H.264 High Profile L5.2 4K60-class stream. Plausible in isolation, but ruled out as the *primary* cause once proxy generation also failed —
3. **Regenerating Optimized Media/Proxy in Resolve baked in "Media Offline" at the exact same points.** This was the real turning point: proxy generation forces Resolve to decode and re-encode the *entire* source. If that process itself fails at the same timestamps, Resolve's decoder can't read those frames at all — not a live-playback/VRAM timing issue, a read failure.
4. **Confirmed in a second, more fault-tolerant decoder:** Samuel found VLC also breaks at the same ~9-minute mark (plays, then restarts/glitches at that timestamp). Two independent decoders failing at the identical point is a strong signal of real damage in the file itself, not a Resolve-specific quirk.
5. **Confirmed the client's own platform ("Shade") plays the file clean end-to-end.** That means a good version exists somewhere upstream — the master, or the platform's own transcode — and the specific `...COMPRESSED.m4v` file Samuel had downloaded was the damaged derivative.

**Fix that worked (confirmed 2026-08-11, Samuel's own words):** *"redownloading the file has worked."* Re-downloading from Shade replaced the locally damaged "COMPRESSED" copy with a clean one.

**Proposed but never reached — do not treat as verified:**
- Toggling Resolve's H.264 decode from Hardware to Software (`Playback > Video and Audio Decode Options` / `Preferences > Decode`) — offered as a diagnostic step, never confirmed tested.
- Escalating to HandBrake as a repair pass if software decode failed: MP4, H.265 (x265), Constant Framerate, Constant Quality RF 16–18, Preset Medium/Slow, all filters off, audio passthrough AAC or re-encode to match. Never reached — the redownload fixed it first.
- `ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate,avg_frame_rate,nb_frames -of default=noprint_wrappers=1 "<file>"` to directly confirm VFR — offered, never confirmed run.

**What to check first, next time:**
1. Run MediaInfo/ffprobe on the file before doing anything else (30 seconds, rules a lot in or out).
2. Play the suspect section in a second, more fault-tolerant decoder (VLC). If it also breaks at the same timestamp, that's real file damage, not a Resolve-only issue.
3. Try generating Optimized Media/Proxy. If proxy generation itself fails at the same point, that's a read failure in the source, not a playback/decode-under-load problem.
4. Check whether the file plays clean on the platform it came from. If it does, a good copy exists upstream — ask for a fresh download or the original master rather than trying to repair the local copy.
5. If re-downloading, compare file size in bytes against the original: same size points to corruption baked into what the platform is serving (need a fresh export from them); different size points to a genuinely bad first transfer.
6. A filename containing "COMPRESSED" (or similar) is itself a flag — it means an extra lossy pass happened before the file reached you, which is a plausible failure point independent of the download.
7. Jump straight to the previously-broken timestamp to confirm a fix, rather than watching front-to-back.

**Related, separate follow-up — proposed, unverified:** once the file was clean, Samuel asked about setting his timeline to "around 30fps" for this 59.94fps-native source. Recommendation given: use **29.97fps, not flat 30.00** — 59.94 ÷ 29.97 = exactly 2 (clean frame-decimation, Resolve just drops every other frame, no blending/judder), while 59.94 ÷ 30.00 = 1.998 (not clean, can drift into duplicated/blended frames over a long timeline, especially with pans). Set in `Project Settings > Master Settings > Timeline Frame Rate`, before cutting — changing it after cutting forces a reconform and cut points can shift. No confirmation in the source that Samuel applied this or that it held up in practice.

---

## 2. Export preset name didn't match its actual codec

**Date:** 2026-08-29 · **Status:** solved (caught same session)

**Symptom:** A saved Deliver-page preset was named `4k h264`, but its actual **Codec** field was set to H.265.

**Cause:** not established beyond "the label and the setting had drifted apart" — likely from copying/renaming an existing preset without updating both.

**Fix:** corrected so the preset name matches its codec before using it.

**What to check first, next time:** before grabbing any saved export preset, confirm the Codec field matches what the preset's name claims. The risk called out explicitly: grabbing the wrong preset on a deadline and not noticing until the client can't open the file.

---

## 3. "Restricted VBR" option not visible in Resolve's rate-control dropdown

**Date:** 2026-08-29 · **Status:** solved (same session)

**Symptom:** While setting up a 4K H.265 master, Samuel couldn't find a "Restricted VBR" rate-control option in the Deliver panel.

**Cause:** "Restricted VBR" was Claude's own descriptive term for the concept, not Resolve's actual UI label — and the available options differ by which **Encoder** is selected:
- **NVENC (hardware)** exposes **"Variable Bitrate (Target Kbps)"** — Target + Max fields.
- **Native (software x265)** exposes a Quality dropdown with a **"Restrict to"** max-kb/s field instead.

Also relevant: in Resolve's dark UI, an unselected rate-control option renders dimmer than the selected one — this can read as disabled/greyed-out when it's actually just not the current selection.

**Fix:** select **"Variable Bitrate (Target Kbps)"** directly if staying on NVENC, or switch **Encoder** to **Native** to get the Quality + "Restrict to" path. Samuel proceeded with Target Kbps rate control on NVENC and confirmed the resulting build as his working master.

**What to check first:** which Encoder is selected (Auto / NVENC / Native) before hunting for a specific rate-control field — the available options change with it.

---

## 4. H.264 generation loss across repeated re-exports (4K) — reference + settings adopted

**Date:** 2026-08-29 · **Status:** reference (mechanics) + solved (export settings actually built into his working master)

Not a single incident — an analysis Samuel requested, followed by concrete settings he then built and confirmed ("This is my master now"). Values below are explicitly **modeled estimates**, not measurements — flagged in the source as accurate in shape, ±2–3 dB in absolute value depending on content, encoder, and preset.

**The mechanics, in short:**
- At 4K/30p and 25 Mbps, bits-per-pixel ≈ 0.100 — well under the ~0.15–0.25 bpp "visually transparent" range for H.264. Generation 1 is already lossy.
- H.264's 16×16 macroblock grid is small relative to a 4K frame (32,400 macroblocks/frame), so a real share of bitrate goes to block overhead rather than picture — the exact problem HEVC's 64×64 CTUs exist to fix.
- **Quantization drift:** each re-encode analyzes the *previous* generation's output (including its own artifacts) and re-quantizes onto a slightly different grid each time. Errors don't cancel — they accumulate roughly like a random walk.
- **Artifact becomes signal:** ringing/mosquito noise/block edges are high-frequency structured content the next pass's rate control can't tell apart from real detail, so it spends bits preserving garbage — this is why loss compounds fastest in the first few generations.
- **Macroblock misalignment only matters if a transform (scale/crop/reposition/stabilization) sits on the timeline between passes** — roughly doubles per-generation loss when it does. A straight passthrough re-export doesn't suffer this.
- Temporal misalignment (I-frame placement shifting generation to generation) and the deblock/re-block loop (smoothing the same seams, then re-sharpening them) both always apply, regardless of transforms.
- Chroma degrades roughly 1.5× faster than luma per pass — saturated reds and skin tones fall apart before luma detail does.
- Loss **plateaus**, not because it stops, but because a fully-quantized, low-entropy image becomes cheap to re-encode — the chain approaches a fixed point.

**Modeled degradation curve (4K/30p, 25 Mbps, x264 High Profile, ~2s GOP, no timeline transform, 8-bit 4:2:0):**

| Gen | PSNR (dB) | Visual fidelity | What you'd see |
|---|---|---|---|
| 1 | 41.5 | 98% | Invisible to almost everyone |
| 2 | 38.8 | 93% | Trained eye catches mosquito noise |
| 5 | 35.0 | 82% | Obvious to a client |
| 10 | 32.45 | 72.5% | Effectively stable garbage (asymptote ≈ 31.5 dB) |

Roughly half the total 10-generation loss (4.4 of 9.05 dB) happens in just the first two re-encodes.

**Rules adopted as a result:**
- **Never round-trip through H.264.** Use DNxHR HQX or ProRes 422 HQ as the intermediate for any export→reimport→re-export cycle — 10-bit 4:2:2, effectively transparent across 5–10 generations (~0.3 dB total loss vs. ~9 dB for H.264). File size cost: 10–15× larger.
- **Deliver every version from the original timeline, never re-cut an exported master.** Every client deliverable should be Generation 1.
- **A client-supplied H.264 file is already Gen 1 minimum** — often Gen 2–3 if it came off a phone, through a messaging app, or downloaded from a platform. Your own export from it starts several generations deep before you've done anything.
- **H.265 does not fix generation loss** — same shape of decay curve, just a better-quality Gen 1 (roughly matches H.264 at ~2× the bitrate at 4K). It costs 2–4× encode time (less on hardware encoders) and carries real compatibility risk for client delivery: older Windows machines need a paid codec extension, some can't play it at all. Not automatically "better overall" for client work — a file the client can't open is worth 0% fidelity.
- **Turn off any timeline transform you don't need** (a stray 100.1% scale from an old stabilization pass, etc.) — costs real quality on every re-encode for nothing.

**Export settings Samuel actually built and confirmed as his working H.265 master:**

| Setting | Value |
|---|---|
| Encoding Profile | Main10 |
| Rate Control | Variable Bitrate (Target Kbps) |
| Target Bitrate | 35,000 kbps (his NVENC build exposes one Target field, no separate Max ceiling — on very busy shots it can't burst above this; raise to 40–45,000 if specific sections fall apart) |
| Encoder | Auto → resolves to NVENC (fast; trades ~15–20% quality-per-bit vs. Native x265. Raise target to ~45,000 for NVENC speed at native-equivalent quality) |
| Preset | Medium |
| Two Pass | Disabled (reasonable given single-target rate control has less to gain from it) |
| Lookahead | 32 (raised from 16 — free quality, doesn't add a render pass) |
| AQ Strength | 8 |
| Adaptive B-frames | On |
| Advanced Settings → Data levels | **Video (16–235)**, not Auto — Auto can silently guess wrong and crush blacks / clip highlights permanently into the delivered file |
| Audio | AAC, 320 kbps, 48 kHz |

**General target-bitrate reference (H.265, 23.976p; H.264 equivalents ≈ double every number):**

| Content | Target/Max kbps | Size per minute |
|---|---|---|
| Talking head, clean background | 22,000 / 32,000 | ~165 MB |
| General purpose default | 35,000 / 50,000 | ~260 MB |
| Grain / foliage / water / fast motion | 50,000 / 70,000 | ~375 MB |
| Client review copy (not final) | 12,000 / 18,000 | ~90 MB |

**Proposed, not confirmed built:** keeping a second preset, `4K H264 Safe` (H.264 High profile, Target/Max 60,000/85,000 kbps, Preset Slower, Two Pass on), as the default until a client confirms H.265 works for them. Suggested, not confirmed as actually saved.

---

## 5. WhatsApp Status heavily degrades exported footage

**Date:** 2026-08-29 · **Status:** proposed — unverified (Samuel asked the question; no confirmation in the source that any of this was tried)

**Symptom:** *"when I upload to whatsapp Status to show my friends my edit, it degrades the footage hugely."*

**Cause (mechanism explained, not independently measured):** a three-stage pipeline —
1. **Client-side re-encode on the phone, before upload.** WhatsApp downscales Status video to roughly 848×480 or 720×1280, drops to ~800–1500 kbps, and re-encodes to H.264 **Baseline** profile — no B-frames, no CABAC entropy coding, ~10–15% less efficient than High profile. A 35 Mbps 4K master can be crushed to ~1 Mbps at a quarter of the resolution in one pass.
2. **A hard 16MB / 30-second cap.** If the source is longer or busier, quality drops further to fit.
3. **A possible second re-encode on the viewer's device** on download/save — meaning what a friend sees may be Generation 3, not Generation 2.

**Proposed fix — not confirmed tested:** export a dedicated Status version rather than sending the client master:

| Setting | Value |
|---|---|
| Resolution | 1080×1920 vertical (or 1920×1080 horizontal) — pre-downscale in Resolve rather than letting the phone's encoder guess; this matters more than any bitrate number |
| Codec | H.264 (not H.265 — the phone re-encode handles it worse) |
| Profile | High |
| Rate control | Target/Max 10,000 / 14,000 kbps |
| Frame rate | Match source, prefer 30p over 60p |
| Keyframes | Every 30 frames |
| Preset | Slower |
| Audio | AAC 192 kbps, 48 kHz |
| Duration / size | Under 30s / under 16MB |

Also proposed: cut grain/heavy texture for the Status cut, increase text size 20–30% (thin fonts vanish at this resolution), avoid whip pans and fast motion (where blocking shows worst), slightly reduce saturation on extreme reds (4:2:0 chroma at 1 Mbps bleeds badly there).

**Better distribution options, also proposed and unconfirmed:** send via WhatsApp's **Document/file attachment** instead of the video share sheet — bypasses the video compression pipeline entirely, works up to 2GB, flagged as "the single biggest quality win available." Or share an unlisted YouTube link or a Google Drive link instead of Status.

**What to check first:** whether the Document-attachment route is acceptable before building a dedicated Status export pipeline — it's free and skips the whole problem.

---

## 6. Preventing Resolve crashes/hangs on motion-graphics-heavy renders

**Date:** 2026-08-29 · **Status:** preventative — unverified (Samuel asked pre-emptively; no crash had actually occurred in the source conversation, and no fix was confirmed against a real incident)

**Context:** asked on an RTX 3060 12GB / i5 13th-gen / 32GB RAM machine, wanting to avoid crashes on "highly animated motion graphic bits" before they happened. Treat everything below as a checklist to try if a crash does happen, not a confirmed fix for one that did.

**Export-panel factors flagged as risk:**
- **Encoder: Auto** is the riskiest single setting — it resolves to NVENC, which then contends with Fusion/OpenFX for the same GPU. If a specific section reliably hangs, switch Encoder to **Native** for that render (moves encoding to CPU, out of GPU contention).
- **Two Pass on a Fusion-heavy timeline** doubles exposure to any Fusion instability by evaluating every comp twice — keep it off for these timelines.
- **Individual clips vs. Single clip** render mode: Individual clips gives a natural recovery point if something fails partway; Single clip doesn't.

**Preferences → Memory and GPU:**
- Cap Fusion memory cache at roughly 30–40% of system RAM (or ~8GB as a concrete number given) — uncapped, Fusion will consume everything and Resolve dies.
- Set GPU processing mode to **CUDA** explicitly, not Auto.
- Select the GPU manually rather than leaving it on Auto.

**The single biggest flagged crash cause: VRAM exhaustion.** Each intermediate buffer in a Fusion node tree is roughly 100MB at 32-bit float at 4K — a 30-node comp with several blurs/glows plus Temporal Noise Reduction plus the export encoder can hit the ceiling. Specific offenders, in order of how much VRAM they eat:
1. **Optical Flow anything** (speed ramps, retimes, Speed Warp) — called out as "the single most crash-prone feature in Resolve." Switch to Frame Blend if a crash can't otherwise be diagnosed.
2. **Temporal Noise Reduction** — described as the worst VRAM offender in Resolve; holds multiple frames in VRAM if it's on any clip in the timeline.
3. 32-bit float Fusion processing where 16-bit would do (halves memory; rarely needed for motion graphics).
4. Large blur/glow radii at 4K, stacked OpenFX on one clip, multiple 4K sources visible at once (multicam/split-screen).

**Workflow fix flagged as the real solution, not just a mitigation:** pre-render heavy Fusion sections to an intermediate file (right-click → Render In Place, or export the range to DNxHR HQX and cut that in instead of the live comp) so the final export has nothing left to compute — just re-encoding flat footage. Alternative, less permanent version: Smart Render Cache set to User, then Render Cache Fusion Output on the heavy clips before exporting.

**Other flagged causes:** NVIDIA **Studio** drivers, not Game Ready (Studio drivers are validated against Resolve; a crash that started right after a driver update is often the driver — roll back); scratch disk full or on a slow drive; Auto Save/Live Save during a long render (turn Live Save off first); Fusion expressions referencing frames outside the render range (causes hangs that look like infinite loops).

**Practical pre-render checklist proposed:** restart Resolve before a long render (Fusion leaks memory across a session), close anything else on the GPU, cache/pre-render Fusion comps first, confirm the project is 16-bit float unless 32 is specifically needed, confirm Temporal NR is off unless needed, and render a 10-second test across the worst section before committing to a full export.

## 7. Resolve crashes while render-caching (Fusion null read) — root cause: GPU timeout (TDR), found 2026-09-23; fix pending Samuel's reboot

**Symptom:** Resolve 21.1.0.14 closes with no dialog while render cache runs, in *$7M Founder How I Use Claude for Cold Outreach* and *3. The Only Claude Dropshipping Guide… (Copy)*. 7 crashes on 2026-09-23. The one at 16:36 happened while caching a specific adjustment clip.

**What the evidence says** (logs, Windows event log, Resolve's two dumps from that day):
- Every recorded crash since 2026-09-14 is in `fusionsystem.dll` (`0xc0000005`). The 16:36 dump shows a **read of address 0x0** (null pointer); the 16:15 dump a read of `0xc47` (a field of a null object). The whole stack is Fusion's own code: no OFX plugin and no NVIDIA driver on it. Fusion is rendering a node that has no image and dereferences it.
- Where the empty image comes from, per the log: **the project's render cache is corrupt** (1,398 failed reads of `CacheClip\9e0c3aa8…` on 2026-09-23 between 14:37 and 16:09, 80 more at 16:34:59, one minute before the 16:36 crash); **Fusion nodes with nothing feeding them** (`MediaIn1 cannot get frame` 540×, `MosaicBlur1 cannot get Parameter for Source` 33×, Dropshipping project); **VRAM exhaustion** (16:15: Fusion used 9.5 of 11.6 GB, allowance −2.3 GB).
- In $7M Founder, Timeline 1 carries an **adjustment clip (frames 1505–1631) and a Fusion composition**, and the log invalidates their cache on every project open. An adjustment clip with Fusion on it renders from the composite of everything beneath it, so a bad cached frame underneath reaches Fusion as nothing.
- Ruled out: system RAM (32 GB, 62 GB pagefile, no low-memory event since 2026-09-07), disk space, MCP scripting.

**Proposed fix, in order:** (1) open the project, set Playback → Render Cache → None at once, then Playback → Delete Render Cache → All; (2) open the adjustment clip's Fusion comp and fix any node with an empty input, and the Dropshipping comp's `MosaicBlur1` and `MediaIn1`; (3) Render Cache → User and cache Fusion output clip by clip, with GPU-heavy apps closed; (4) check for a newer 21.1.x. To get moving before (2), disable the adjustment clip (select, `D`), cache, re-enable.

**Raising Resolve's or Fusion's RAM limit won't fix this** (asked 2026-09-23). System RAM is ruled out, and the limits were already Resolve 51% / Fusion 42% of 32 GB. A bigger Fusion cache adds memory pressure and does nothing about a null read or VRAM. If anything, bring Fusion down toward section 6's 30–40%.

**Update 2026-09-23 20:15. Root cause found: a Windows GPU timeout, not the cache.** Controlled test: the render cache fully deleted, Render Cache → User, and only a few clips flagged at a time. Batch 1 (32 clips, 0:00–1:02, 1,715 frames) cached cleanly in 4 min. Batch 2 crashed 11 frames into the **V4 Fusion Composition at 1621–1708** (378 nodes: 4 NeoLightSweep Pro, 4 NeoAnim, ResolveFX Grid + GaussianBlur, SoftGlows, no Magic Mask). The cache was clean, so a corrupt cache is a consequence, not the cause. The sequence in the log:
1. `Fusion | WARN | Low GPU memory … allowed -2381 MB, used 9657 MB`. Resolve alone holds ~8 GB of the RTX 3060's 12 GB while idle, and other apps together hold ~0.5 GB.
2. `DVIP | ERROR | CUDA error cudaErrorLaunchTimeout (702)`. A GPU job ran longer than Windows' **TDR watchdog (default 2 s; `TdrDelay` is not set on this PC)**.
3. The System log shows `nvlddmkm` event **153**, a driver reset, at 20:15:51. Same at 18:27:07, before the 18:26 crash, and 8× on 2026-09-20.
4. Resolve loses its GPU context, Fusion reads a null (dump: read of `0x587`), and the crash lands at `fusionsystem.dll+0x30c290`. The 18:31 crash in `nvoglv64.dll` (0xc0000409) is the same event hitting the OpenGL side.

Magic Mask (in 4 comps: V2 283–415, Fusion Clip 2 546–585, V3 1505–1631, V2 9360–9637) adds GPU load but is not required for the crash.

**Fix:** raise the TDR timeout. Samuel runs these as admin, then reboots (a system setting; agents don't change it):
`reg add "HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" /v TdrDelay /t REG_DWORD /d 60 /f` and the same with `/v TdrDdiDelay`. A heavy frame then gets up to 60 s instead of 2 s. The cost: a genuinely hung GPU freezes the screen for up to 60 s before recovering. Also turn off the Parsec virtual display when not streaming, since every extra display costs VRAM. Cache clip by clip with `scripts/resolve_cache_watch.py` (per-clip progress, stops on a crash) and the queue in `scripts/cache-queue-7m-founder.json`.

**Scripting note:** a cache flag set by script (`TimelineItem.SetFusionOutputCache(resolve.CACHE_ENABLED)`; takes the constant, not a word) does nothing until the background cacher is woken. Set Render Cache to None, switch page and back, then set it to User again.

**Reading a new crash:** `davinci_resolve.log` for what happened before it; the Windows Application log (`Application Error`, ID 1000) for the module; Resolve's own `.dmp` in `Support\logs\` for exception, address and stack — parse with `03-Areas/video-editing/scripts/resolve_crash_dump.py`. Some crashes leave no Windows event and an empty `crash_archive.txt` entry; the dump is still there.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
