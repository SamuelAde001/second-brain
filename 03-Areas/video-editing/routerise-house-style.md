---
type: knowledge
area: video-editing
status: needs-input
source: claude-export
updated: 2026-09-20
tags: [house-style, routerise]
---

# Routerise house style — pacing, cuts, sound, look

Style reference for cutting long-form talking-head video for [[clients/routerise]] (Alex / Frontal). Reverse-engineered by Samuel from the actual Resolve project data of the reference cut, **"$7M Founder: How I Use Claude for Cold Outreach (B2B sales)"** (DB folder `Routerise`, Timeline 1, Resolve Studio 21.1.0.0014) — a ~7:30 video, 503 video items, 253 audio items across 10 video / 7 audio tracks. Companion doc: [[fusion-node-system]] for how the graphics themselves are built. Workflow order (sync → silence → transcribe → bad takes) is [[sops/routerise-cut-workflow]].

**Status note:** several rules below are marked "confirmed" (Samuel answered directly) vs. "proposed / open" (Claude's read of the data, not yet approved). Do not treat a proposed rule as settled — see §9.

## 1. Delivery spec

Taken from the actual render job that produced the reference cut (`v2.mp4`):

| Setting | Value |
|---|---|
| Format / codec | MP4 · H.265 NVIDIA · Main10 profile (10-bit) |
| Resolution | 3840 × 2160 — **upscaled on export from a 1920×1080 timeline** |
| Frame rate | 23.976 |
| Audio | AAC · 16-bit · 48 kHz |
| Render mode | Single clip · Custom preset · no multi-pass · no network optimisation |
| Timeline | 1920×1080, output 1920×1080, 23.976 fps |
| Colour science | DaVinci YRGB · timeline colour space DaVinci WG/Intermediate · output Rec.709 Gamma 2.2 · data levels Video · SuperScale off |

**Confirmed by Samuel:** the 1080p→4K upscale on export is deliberate — 1080p keeps the system responsive while editing; 4K is what Alex wants delivered.

There is also a separate render job exporting Timeline 2 as MP3 only (audio, no video) — the transcription pass.

## 2. The ten structural rules

From the client quick-reference (`START-HERE`), consistent with the measured data:

1. **No transitions. Ever.** Zero dissolves/wipes across 503 video clips in the reference. Cuts only. Fades (3–12 frames) allowed on graphics only, never on A-roll.
2. **Chapter the script, then colour the A-roll by chapter** — and change the music track on the same frame. In the reference, all 9 chapters line up frame-for-frame with clip-colour runs and music cues. See §4.
3. **Cut A-roll to a ~2.4 s median.** Hold up to 11 s when the point earns it; go sub-second for emphasis. See §5 for the full distribution.
4. **One camera, external lav on A1 at +6 dB**, synced clips, never camera audio.
5. **Never put an effect on a source clip** — the only exception is PIP. Everything else goes on an adjustment clip or a Fusion comp on top. (Adjustment-clip system detail: [[fusion-node-system]].)
6. **No Dynamic Zoom. MagicZoom V3 for every zoom** — slow zooms and quick punch-ins, speed and depth tuned to context, always on an adjustment clip, never a source clip. Samuel's own words: *"I prefer MagicZoom V3 instead of Dynamic Zoom, I use it for slow zooms, and quick punch ins and the speed and depth of the zoom differs in different contexts."* Data check: `DynamicZoomEnabled` is false on every clip in the reference timeline.
7. **Demo sections strip everything** — no music, no SFX, no graphics. Screen recording plus PIP only. See §7.
8. **Keep a clean A-roll on V1.** Disable the PIP layer (V7) and the screen-recording layer (V3) above it and you instantly have a pure client A-roll version. Confirmed deliberate by Samuel — not an accident of workflow.
9. **SFX mark graphic reveals, not cuts.** ~1 in 3 reveals get an SFX hit; almost never a cut. Small reused palette (~10 files) spread across 4 tracks. See §8.
10. **Reframe a whole stack with a transform-only adjustment clip**, never by moving source clips.

## 3. Track layout

| Track | Items (reference) | Role |
|---|---|---|
| V1 | 165 | A-roll, full length, clean, no PIP |
| V2 | 63 | Mixed "hero" layer — full-frame Fusion builds, B-roll, compound Fusion Clips; mostly the zoom/move layer (MagicZoom-only adjustment clips) |
| V3 | 129 | Screen recording (83× clips) + adjustment clips carrying graphics that move with it |
| V4 | 44 | Graphics + punch-in/transform-only adjustment clips |
| V5–V6 | 16 / 4 | Overflow graphics; rare top graphics |
| V7 | 82 | Mirrored A-roll PIP (81 clips) — see §7 |
| A1 | 165 | Synced lavalier, **+6.0 dB on every clip**, set once, never rides |
| A2 | 6 | Music (6 tracks, one per section) |
| A3–A6 | 82 total | SFX, spread across 4 tracks so hits can overlap |

## 4. The section/chapter system

**The single most useful pattern found.** A-roll clips are colour-coded, the colour runs are contiguous blocks that map exactly to script sections/chapters, and the music cue changes on precisely the same boundary.

Reference video — 9 transcript chapters, matched frame-for-frame to A-roll clip-colour runs (chapter 3 is the only one that splits across two colours, exactly where the music drops to silence at 1:43.98):

| Chapter | Transcript range | Clip colour |
|---|---|---|
| 1 — The Hook | 00:00.04 – 00:31.70 | Purple |
| 2 — Missing Piece One: A Source With Signals | 00:31.70 – 01:13.36 | Orange |
| 3 — Missing Piece Two: The Tiering System | 01:13.36 – 02:01.79 | Teal → Pink (splits at the silence beat) |
| 4 — The Three Tools | 02:01.79 – 03:07.52 | Yellow |
| 5 — The Offer | 03:07.52 – 03:29.88 | Orange |
| 6 — Building and Tiering the List | 03:29.88 – 05:32.37 | Teal |
| 7 — The Tier One Campaign | 05:32.37 – 06:28.72 | Yellow |
| 8 — How to Work Each Tier | 06:28.72 – 07:15.14 | Purple |
| 9 — Outro | 07:15.14 – 07:29.70 | Orange |

**Colour→meaning mapping — proposed, not yet approved.** No fixed colour-to-section-type scheme existed before this study; the table below is Claude's proposed scheme built to fit how the reference video was actually cut, explicitly flagged as needing Samuel's sign-off:

| Colour | Proposed meaning |
|---|---|
| Purple | Hook & Outro — top and tail, camera only |
| Orange | Problem / stakes — what's broken |
| Yellow | Teaching — concepts, tools, frameworks |
| Teal | Demo — screen recording + PIP (reserving Teal exclusively for demo sections would make "where does the PIP system apply" readable at a glance on the timeline) |
| Pink | Emphasis beat — a deliberate silence/turn |
| Blue | Client-supplied B-roll / third-party footage |

Only 4 timeline markers exist in the reference (all blue, unnamed) — **the clip colours, not markers, are the real structural map.**

## 5. A-roll cut rhythm

- One camera (`C0782.MP4`, 3840×2160), cut 165 times in the reference, plus the same footage duplicated to V7 for PIP (§7).
- Audio is external and synced, never camera audio. Two lav files in the reference (`TX02_MIC012` × 118 clips, `TX02_MIC013` × 47 clips — a battery/card change mid-shoot, confirmed **not** a fixed convention, just whatever audio was supplied that day).
- Sync: all 165 V1 clips have byte-identical in/out points to their A1 partners; only 6 distinct source offsets exist across the whole timeline, clustered at −1045 and +52905 frames — exactly two sync points, one per lav file.
- Mic level +6.0 dB on all 165 clips, set once, never automated.

| Metric | Value |
|---|---|
| Clips | 165 over 7:29.9 |
| Mean | 65.4 f (2.73 s) |
| Median | 57 f (2.38 s) |
| Shortest / longest | 8 f (0.33 s) / 262 f (10.9 s) |
| Under 1 s | 26 clips (16%) |
| 1–2 s | 45 (27%) |
| 2–3 s | 32 (19%) |
| 3–5 s | 40 (24%) |
| 5 s+ | 22 (13%) |

So: a cut roughly every 2.4 seconds with a long tail — holds up to 11 s when the point needs it, sub-second machine-gun cuts for emphasis.

**Retiming is essentially unused:** 502 of 503 clips at 100% speed. Only 3 clips retimed (one at 1864% — a timelapse), plus 6 freeze frames (0% speed).

## 6. Zooms

**MagicZoom V3 (MrAlexTech) for every zoom, never Dynamic Zoom** — see Rule 6 above. All 51 MagicZoom V3 instances in the reference project sit on adjustment clips; not one is on a source clip. Full adjustment-clip audit (which track carries which job, and how MagicZoom stacks with Fusion comps) is in [[fusion-node-system]] §3.

## 7. The PIP demo system

The mechanism behind Rule 7 (demo sections strip everything) and Rule 8 (clean A-roll on V1):

1. **V3** carries the screen recording, punched in to a fixed zoom in the reference (Zoom 1.65 / Pan −372 / Tilt +60), cut into 81 pieces.
2. **V7** carries the *same A-roll clips as V1*, duplicated up (79 of 81 share identical timeline-start and source-start frames with their V1 counterpart) — with **FlipX = true (mirrored)**.
3. Those clips each carry the Edit-page effect **SSC PiP Pro** (Stirling Supply Co), cropping to a **circular inset, bottom-right, with a soft light ring and drop shadow.**

**Why the mirror matters:** flipping him horizontally turns his body and eyeline so he faces *into* the screen content rather than away from it. Without the flip, the PiP fights the layout.

**Confirmed by Samuel:** the V1/V7 duplication (rather than cutting the PiP into V1 directly) is a deliberate switch — V1 stays the clean, PiP-free A-roll; disable V7 and V3 and you instantly have a pure client cut (Rule 8).

In the reference, the V7 run is contiguous except for one 34-second gap (6:28.9–7:02.9) — exactly where music returns (`ES_Open Road` starts 6:28.89). Confirmed: that gap is simply the demo being over, not an accident.

**Open / not verified:** whether the PIP's position or size is ever animated within a clip, or whether it's always one fixed preset dropped on the clip. The DRT export compresses these parameters so this could not be read from the data — ask Samuel if it matters for a new video.

## 8. Sound design

- **6 music tracks in the reference**, all Epidemic Sound, one per section, changing exactly on section boundaries (§4). Levels −25.1 to −41.9 dB, **set once per track, never automated per clip.**
- **82 SFX hits from only 10 distinct files** — a deliberately tiny, reused palette: `UI Double Beep 03` (32 total), `Multiple UI Beeps 01` (11), `Swoosh_03` (10), `Arpeggiated UI Beep 03` (6), `Cybernetic Data Processing 1`, `Multiple UI Beeps 12`, `ES_Low Hit`, `cinematic riser 4`, `Camera_01`, `ES_Axon Terminal`.
- SFX spread across 4 tracks (A3–A6) so hits can overlap.
- **SFX marks graphics, not cuts.** Only 8% of A-roll cuts have an SFX within 4 frames, vs. 35% of graphic reveals within 6 frames — cuts are silent, reveals get sound, and even then only about a third of them so it never becomes wallpaper.

**The demo-section rule (Rule 7), measured:** per 30-second window from 3:30–6:30, SFX count = 0, music absent, Fusion graphics drop from ~19 per window to 1–4. Everything strips away to just the screen recording plus PIP. At 6:28.9, music returns, SFX returns (10 hits in that window), PIP ends.

## 9. Typography and colour

### Typography
| | |
|---|---|
| Font (reference video) | Open Sans, 64 of 72 Text+ nodes, Bold on 69 of 72 |
| Secondary in the reference | Geist (8 nodes) |
| **Confirmed by Samuel — corrected reading** | **Geist is Alex's brand font, the default going forward. Open Sans was used ad-hoc in the reference and should not be repeated.** |
| Case | Overwhelmingly ALL CAPS for chips, labels, titles; sentence case for longer explanatory lines |
| Size (Fusion normalised) | Clustered at 0.0218 / 0.0255 / 0.0333 / 0.0489 / 0.0511 — roughly a 5-step scale |

**Two-tone headline rule:** headlines split across two lines, line 1 in white, line 2 in the accent colour (e.g. "DIFFERENT WAYS OF" white / "ENGAGING WITH THOSE LEADS" orange) — the accent line carries the meaning.

**Open:** which Geist weight maps to which role (titles / chips / body) — the family runs Thin→Black and this isn't resolved.

### Palette (Frontal — reference project; accent changes per client)

| Hex | Uses | Role |
|---|---|---|
| `#FF5A1F` | 56 | Primary accent. Chips, pills, borders, highlight line |
| `#FFFFFF` | 48 | Primary text |
| `#FD9457` | 22 | Secondary / lighter orange, gradient partner |
| `#1B0903` | 15 | Deep warm brown-black — the background ground |
| `#000000` | 11 | True black |
| `#001921` | 8 | Dark teal (rare, contrast accent) |
| `#110602` / `#46190A` / `#591E0B` | 7 / 4 / 3 | Warm dark ramp |
| `#BE4117` @ 0.72 alpha | 3 | Translucent panel fill (e.g. the TIER card) |
| `#0E0E0E` / `#0F0F0F` / `#212121` | 5 / 2 / 3 | Near-black panel fills |

A warm orange-on-near-black system, no cool tones except a rare dark teal. Backgrounds are a dark warm brown with a radial glow behind the subject, not flat black.

**Colour rule:** fill = accent × ~0.10 (`#1B0903` for the Frontal accent). Border = the accent itself. Secondary/lighter tint `#FD9457`.

**Don't be misled:** the most common raw Background colour by node count is `#FFACEA` (pink) — every instance has alpha 0, an inherited placeholder inside the Neo macros, not a design colour.

### Shapes
- Rounded rectangles everywhere. `RectangleMask.CornerRadius` clusters at **0.30–0.34** (cards), **0.66–0.81** (pills/chips), **1.0** (full capsule).
- Chips/pills: orange gradient fill, white bold caps, occasional large ghosted numeral behind ("1", "2") at low opacity.
- Cards: translucent orange fill, 2–3 px bright orange border, outer glow, generous radius.
- Connectors: thin orange lines, dotted/dashed leaders between elements.
- Neon outline-only diagrams (e.g. the lead funnel graphic): orange stroke, no fill, with glow.

## 10. Animation timing constants

From 106 NeoAnim instances in the reference — remarkably consistent, and the most directly reusable numbers here:

| Parameter | Values | Reading |
|---|---|---|
| InLength | 25 f (64×) · 20 f (32×) | ~1.04 s or ~0.83 s in |
| OutLength | 25 f (8×) · 20 f (1×) | Out animation is rare — things animate in and stay |
| Angle | −90 (84×) · −270 (9×) · −180 (6×) | Slide up from below is the default |
| StartBlur | 25 (75×) · 5.5 (31×) | Heavy directional blur on entry |
| MotionBlur | 1 on all 106 | Always on |
| StartOffset | 0.44 (39×), 0.018 (20×), 0.0435 (10×), 0.094, 0.15… | Per-element stagger for word-by-word reveal |

**The signature move, in one line:** slide up from below over 20–25 frames, motion blur on, heavy start blur, staggered per word.

`NeoLightSweepPro` runs at `Distance 0.0015` (58 of 60 instances) with `GlobalOut` of 80 / 53 / 198 / 127 frames.

## 11. Operational notes — Resolve stability

Logged during the study because it cost real time (Resolve crashed three times while building this reference):

| Cause | Rule |
|---|---|
| Crash during Fairlight WASAPI audio-device scan (Bluetooth headphones switching to AUTO) | Connect audio devices *before* opening Resolve. |
| `Project.ExportCurrentFrameAsStill()` → gallery refresh → freed-memory crash (`0xDEADBEEF` marker) | **Never call `ExportCurrentFrameAsStill()`.** Use Deliver-page single-frame render jobs instead. |
| UI framebuffer resize after a render completed at a different resolution than the timeline | **Don't render at a resolution different from the timeline's.** Set the timeline resolution to match. |

**Also:** when Resolve appears closed but is still in Task Manager (observed sitting at ~13.4 GB RAM), every DaVinci process must be ended before it will relaunch.

**Safe method for grabbing single frames** (used for 24 frames in this study):
1. Set the timeline's own resolution to match the render resolution.
2. `SetCurrentRenderFormatAndCodec("jpg", "YUV420_8")`.
3. Per frame: `SetRenderSettings` with `SelectAllFrames: False`, `MarkIn == MarkOut == frame`, then `AddRenderJob()`.
4. `StartRendering(all_jobs)` — 12 frames rendered in well under 10 s.
5. Apply settings **one key per `SetRenderSettings` call** — a batched dict silently returns `False` and falls back to defaults.

## 12. Open questions (unresolved as of 2026-09-20)

These were live at the end of the study and are not confirmed one way or the other:

1. Is the colour→section-type mapping in §4 to be adopted as-is, or reassigned?
2. Is SSC PiP Pro always one fixed preset per clip, or is position/size ever animated within a clip?
3. Which specific weights of Geist map to which roles (titles / chips / body)?
4. The **PJT text-animator pack** (62 presets) and the **Neo Texts** preset library (~100 presets) are installed but completely unused in the reference project — deliberate (don't fit the look), or just not top-of-mind? This decides whether future videos should pull from them.
5. When does Samuel reach for **NeoTextMotion** (`Fuse.NeoMotionText`, used on ~32 of 105 text elements in the reference, roughly 1 in 3) instead of plain Text+ with NeoAnim? Per-character/word control, or just the faster starting point?

Back to [[_index]]
