---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: B2
---

# B2 · Comps and adjustment clips

> **Read when:** building, installing or reviewing any visual (every beat builder and reviewer). **Client values:** none here; colours and corner shapes inside comps come from the client overlay. **Status:** draft, not yet approved by Samuel.

## Rules

### Adjustment clips are the default
- **B2.1** Anything that is not a source clip goes on an adjustment clip: focus, lighting, highlight, extra zoom, text over footage, pills and graphics over the A-roll. Use them a lot. 🔁 ×4 ✅ *"You make use of adjustment clips a lot, as that's how I used to edit"* (2026-10-14; also 2026-09-27, 2026-10-07, 2026-10-22) · ✔ 2026-11-05
- **B2.2** Keep the treatment off the media clip and out of its own comp, so he can adjust it. The media clip's own comp stays pass-through. ✅ *"must be on an adjustment clip not on the clip itself so I can always adjust things"* (2026-09-27) · ✔ 2026-11-05
- **B2.3** Build on real adjustment clips, never on transparent base clips with a MediaIn reading the layers below. ✅ *"Use Adjusment clips instead of what you used, it is not giving the same results"* (2026-10-07; replaces the Apollo base-clip method of 2026-10-02) · ✔ 2026-11-05
- **B2.4** To repeat a visual, copy his adjustment clip and its nodes and adjust them. When he points at one of his own elements, lift it from his comp with its settings; never redraw it. ✅ *"just copy the adjustment clip and and nodes, and adjust things well"* (2026-09-27) · ✔ 2026-11-05
- **B2.5** Every visual except a UI demo is live Fusion nodes, never a rendered video, so he can change text and animation on a revision. ✅ *"I want it to be actual nodes, not videos"* (2026-09-27) Page zooms and highlights stay on adjustment clips, never baked into a render. ⚙️ See Q-B2.c. · ✔ 2026-11-05
- **B2.6** One adjustment clip may carry a Fusion comp **and** an Edit-page plugin (e.g. MagicZoom), so one clip owns both the look and the move. 🎬 (27 % of his 117 adjustment clips in 7M) · ✔ 2026-11-05

### The kinds of adjustment clip
- **B2.7** **Media adjustment clip** — on every screen recording, page, UI, screenshot, website, render and B-roll, from the media's first frame to its last. Three parts, in this order: 🔁 ×7 ✅ 🎬 *"there was an adjustment clip that I always put in on top of screen recordings"* (2026-10-28); *"Where is my adjutment clip that we always put on screen recording visuals"* (2026-10-25) · ✔ 2026-11-05
  - NeoAnim In 20 f, Expo ease-out, Position StartOffset 0.021 at −90°, StartBlur 5.5, Blend on, no Out.
  - ResolveFX Vignette: black, oval, multiply, size 1, softness 0.5, Blend 0.835 (see Q-B2.a).
  - MagicZoom V3 slow zoom-in on the same clip (depth in B5.3).
  - Template: `Visual Assets\Samuel templates (Editor)\HIS_NEOANIM_ADJ.setting` (his `ai4_V3_000100_1.comp`). Found in all three finals (26× AI4, 26× Apollo, ~45× TSB).
- **B2.8** All three parts, every time. NeoAnim alone is wrong. ✅ *"the adjustment clips you used in this last video was wrong because you only use [NeoAnim]"* (2026-10-28) · ✔ 2026-11-05
- **B2.9** Montage beats use the same entrance at In 8 f. 💡 · ✔ 2026-11-05
- **B2.10** **Intro adjustment clip** — frames 0-28 of every video: `HK01_samuel_intro_adj.setting`. GaussianBlur 0.4 → 0 over f0-6, Transform Size 1.594 → 1.0 over f0-20, pivot (0.529, 0.67), MotionBlur Quality 10 / Shutter 330. Copy it byte for byte; no MagicZoom in 0-28. 🔁 ×2 ✅ *"there is one adjustment clip I always put at the intro of my videos"* (2026-10-28; also 2026-10-25) · ✔ 2026-11-05
- **B2.11** **Focus adjustment clip** (V3) — over UI and pages: darken the rest with Brightness Contrast outside a soft RectangleMask, highlight the spoken element, eased zoom keyed to the words. Chain: Rectangle_Focus → Background_Dim → Merge_Dim → Transform_Zoom. ✅ (2026-09-27, 2026-10-03) Look in C6, moves in B5. · ✔ 2026-11-05
- **B2.12** **Section slam / zoom-out reveal** — the same recipe as B2.10, 28 f, at each section start and on the return to camera after a full-frame run. 🎬 (TSB, AI4) · ✔ 2026-11-05
- **B2.13** **A-roll zoom clip** — MagicZoom only, on an adjustment clip over the A-roll. On the A-roll the zoom type is **Standard** with a **Linear** curve. Zoom & Hold only on emphasis statements. Depth and pacing in B5. ✅ *"the magic zoom settings should be set to zoom type, standard and curve linear for A-roll, only time we use the usual zoom and hold is for empasis statement areas"* (2026-11-05) · ✏ 2026-11-05
- **B2.14** **Reframe clip** — transform only (Zoom 1.16 / 1.30 / 1.33, Pan/Tilt as needed), spanning a whole stack (some 400-1059 f), so a framing change costs one clip. Never reframe by moving source clips. 🎬 · ✔ 2026-11-05
- **B2.15** **Text over footage** — on an adjustment clip above the clip, darkened "the way we do it": NeoTextMotion over a dark bottom gradient (`Down fade`), nothing else. Key statements get his "Box main" caption bar (Down fade + Box main + shine). ✅ *"on an adjustment clip above this clip darkened the way we do it"* (2026-10-14) 🎬 · ✔ 2026-11-05
- **B2.16** **Graphics over the A-roll** (pills by his side, "link in the description") — on an adjustment clip, entering with NeoAnim. ✅ *"Pills, on an adjustment clip, on screen by his side"* (2026-09-27) · ✔ 2026-11-05
- **B2.17** **Pain punch** — from the pain phrase to the visual's end: a red Vignette (multiply, colour 1/0/0), optionally a ColorCorrector desaturate before it, stacked with a punch-in. **Only on B-roll or screen UI on top, never on the A-roll.** ✅ *"don't do that on an A-roll, only on top B-roll or screen UI"* (2026-11-05) 🎬 (AI4) · ✏ 2026-11-05

### How an adjustment clip works with the media under it
- **B2.18** An adjustment clip's comp receives the finished frame of every track below it (1920×1080) as its MediaIn. Frame 0 of the comp is the clip's first frame. Only adjustment clips see the layers below; Fusion Composition generators and Fusion clips render on their own. ⚙️
- **B2.19** Start the adjustment clip on the media's first frame and end it on the media's last. When he moves one, his placement stands. ✅ *"I move the adjustment clip here"* (2026-10-24)
- **B2.20** A comp that starts from a clear Background must Merge over MediaIn_Below, or the media turns black. ⚙️ (2026-10-24)
- **B2.21** When working in his comps, add to the comp he has open, or add a new comp version on the clip; never overwrite his comp. ✅ *"Add it to the fusion comp I was in at that moment"* (2026-09-26) ⚙️
- **B2.22** The Fusion page never opens an adjustment clip, so its comps are written by script (.drt round trip, or in-place import on an existing clip: `kits\inst\inplace.py`, `adjconv.py`). After a swap on a cached clip, nudge one input (Blend 0.999 → 1.0) so Resolve drops the old cache, and check a second still. ⚙️ How: [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]], open before any install.

### Keep comps light
- **B2.23** Comps must play back smoothly on his PC. A heavy visual is a fault. ✅ *"this visual is too intensive on the computer"* (2026-10-24)
- **B2.24** Neo Bevel stays in comps but switched off (PassThrough). Kits build it off (`frfx.bevel`); finished comps are switched off by script (`kits\brandfix.py`), not regenerated. ✅ *"Neo bevel node in the comps are really lagging it down"* (2026-10-23)
- **B2.25** A device that repeats stays light: no reflections or glow on every card. A heavy one crashed his cache. ✅ (2026-10-10)

## Never
- **B2.26** Never put an effect, MagicZoom or treatment on a source clip (only exception: the PIP). 🎬
- **B2.27** Never use a Fusion comp for a zoom-in. ✅ *"Never use fusion comp for this zoom in effect, always use Adjustment clips"* (2026-10-14)
- **B2.28** Never put motion graphics on a screen recording or UI demo: highlight, cursor movement and the media adjustment clip only. 🔁 ×2 ✅ *"Since when did we start putting motion graphics on screen recording visuals"* (2026-11-01; also 2026-10-07)
- **B2.29** Never leave out the media adjustment clip or one of its three parts. Never lower the vignette Blend (video 2 used 0.4) or set the NeoAnim slide to 0 (pages landed static). ✅ ⚙️ (2026-10-25, 2026-10-27)
- **B2.30** Never edit his intro adjustment clip. ✅ (2026-10-25)
- **B2.31** Never insert an adjustment clip with `InsertGeneratorIntoTimeline`: it ripples V1. ⚙️ (2026-10-10)

## Pictures
- ![[_attachments/rulebook/b2-media-adj-proof.jpg|360]] ⚙️ media adjustment clip (NeoAnim + vignette + MagicZoom) proof sheet, Cold Email, our lab test passed 2026-10-29 (not yet seen by Samuel)

## Questions for Samuel
- **Q-B2.a** Vignette strength on the media clip. Your three finals and the template: Blend 0.835 (measured 2026-10-07). The Gamma job note: "small vignette (Blend 0.638)" (2026-11-01). → Options: (1) 0.835 on every client (2) 0.638 for Gamma only, in its overlay (3) 0.638 everywhere. My pick: (1), it is what your finals use. → Samuel: (1), 0.835 on every client (2026-11-05).
- **Q-B2.b** When a range has no adjustment clip to host a comp, may we use a base clip and tell you (our method since 2026-10-10), or must we always create an adjustment clip (your 2026-10-07 ruling)? → Options: (1) always an adjustment clip (2) base clip as a last resort, flagged. My pick: (1). → Samuel: (1), always an adjustment clip (2026-11-05).
- **Q-B2.c** Heavy comps. You said every non-demo visual stays live nodes (2026-09-27), but in AI4 the workflow graphics and the face bubble were rendered in place, and on 2026-10-24 a heavy comp was a fault. → Options: (1) always live nodes, kept light (2) render heavy ones in place and keep the comp saved beside the render. My pick: (2).

## Sources
Replaces the adjustment-clip rules in [[03-Areas/video-editing/ways-of-working|Ways of working]] and [[03-Areas/video-editing/routerise-house-style|Route Rise house style]] (§2, §11b), and draws on [[03-Areas/video-editing/fusion-node-system|Fusion node system]] §2 and §8, [[03-Areas/video-editing/edit-grammar/edit-grammar-shared-rules|Edit grammar: shared rules]] (S0.1, S0.11), [[03-Areas/video-editing/edit-grammar/edit-grammar-ai4|Edit grammar: AI4]], [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]], [[04-Projects/routerise-gamma-claude-mcp-rich|Gamma job]], [[04-Projects/routerise-linkedin-training|LinkedIn job]].

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
