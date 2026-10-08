---
type: knowledge
area: video-editing
status: active
updated: 2026-10-08
source: local-folder
tags: [grammar, style, samuel, constructs]
---

> Samuel's shared rules in numbers (S0.1-S0.6), distilled from the grammar study for the B2B build (2026-10-07): section 4 of the job's `Docs\Build list v3 (2026-10-07).md`. Reusable on any Route Rise talking head. Index: [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]].

## 4. Shared kit (S0), built once

**S0.1 Media entrance (his C1).**
- Template: `ai4_V3_000100_1.comp`, already exported as `comps\his\HIS_NEOANIM_ADJ.setting`.
- Neo Anim: In 20 f, Expo ease-out, Position StartOffset 0.021 at −90°, StartBlur 5.5, Blend on, no Out.
- ResolveFX Vignette: black, multiply, size 1, softness 0.5, tool Blend 0.835.
- **Goes above every V2 media item in 2495–29939:** UI renders, websites, B-roll, Flow clips and captures, including items marked keep (calls vocabulary, Slack, the hero and so on).
- In K2/K3 clips it shares the V3 base clip with S0.2: MediaIn → Transform_Zoom → focus → Neo Anim → Vignette → MediaOut.
- Montage beats use In 8 f.

**S0.2 Focus base clip.**
- Template: `apollo_V8_002413_1.comp`. Generator: `engines\focusgen6.py`, with `render3.py` writing the `r_*` rect json.
- Spotlight: BrightnessContrast Gain 0.40–0.42, Saturation 0.5, under one inverted rounded rect (CornerRadius 0.12, SoftEdge 0.004). Pad the rect 14 px sideways and 5 px vertically.
- Zoom: at most 1.25 (never over 1.3).
- Every move takes 18 f, eased, with keys only where a move starts or ends.
- When words come faster than that, hold the zoom and hop only the rect (at least 10 f per hop, at least 30 f between hops).
- Spotlight fade-in 10–14 f.
- With no zoom, run a slow push 1.0 → 1.04–1.05 across the clip.
- Rect edges sit in padding, never through text. No text is cut by the frame edge.

**S0.3 Premium chain (pills and cards).**
- **Border:** an Instance of the shape mask with BorderWidth: 0.0012–0.0016 on pills, 0.0021–0.0046 on rings. Colour #FF5A1F or #FD9457, with NeoGlow (Gain 0.15, MasterBlur 1.5, Depth 4, Screen) on borders and rings only.
- **Static NeoLightSweep Pro:** band 0.07–0.1142, Angle −40, SoftEdge 0.0551, Distance 0.0015 at −130°.
- **DropShadow:** pills 0.5–0.55 / 0.008 / 0.31. Cards 0.6 / 0.012 / 0.45.
- **NeoBevel:** orbs and cards, Blend 0.15, LightAngle 138.4.
- **Moving shine:** one pass after the element lands. BrightnessContrast Gain 1.55–1.9 through an inclined RectangleMask (W 0.022, Angle −18) swiped over about 10 f.
- **Neo Anim:**
  - Elements: In 12–14 f, Out 8–10 f, Position + Blend + Blur, StartBlur 25.
  - Offset 0.02–0.04 for rows, 0.05–0.08 for cards, 0.10–0.12 for pills.
  - Direction follows the side: left −180°, right 0°, lower −90°, drops 90°.
  - Stagger 3–4 f.
  - Out finishes on the slot's last frame.

**S0.4 Text.**
- NeoMotionText preset 26, Geist.
- Two-tone: Char1 range plus Char1Color (1, 0.3529, 0.1216). Red tail #E6382E, or Char2Color (0.667, 0, 0) on Box main. Green #1FB85C.
- Word scope: InLength 18–25 f, Delay 0.28 s, PosDistance 0.0464.
- Built-in shadow 0.496 / 0.004 / 3.31. Two shines at intensity 0.335, width 0.0141, at 0.19 and 0.38.
- **No glow on title text** (F33).
- Titles: ExtraBold 0.058–0.070 at y 0.80–0.90.
- Floor: Size 0.024.

**S0.5 BGORANGE.**
- His macro, `My macros\BGORANGE.setting`.
- Set its Background and blur tools to float16 to stop the banding (D7).
- Content push 1.0 → 1.036–1.04, on a Transform on the content canvas.

**S0.6 Down fade.**
- His macro: gradient black α 0.62–0.65 → #1B0903, through a soft rect (W 1.073, H 0.619, Soft 0.0583, centre y −0.119).
- In 8 f, out 7 f.

**S0.7 Active state.** His Opacity macro (or BrightnessContrast) takes inactive elements to Gain 0.42–0.62 and Saturation 0–0.64 over 6–8 f. One orange focus at a time.

**S0.8 Hide until said.** ResolveFX MosaicBlur, PixelFrequency 200, on that layer only. Blend 1 → 0 over 8 f on the word.

**S0.9 Line marker.**
- Neo Highlighter Pro (`tsb_V5_004830_1.comp`, `tsb_V6_004923_1`, `tsb_V7_004928_1`): #FD9457, multiply, FastNoise → Displace 0.01 edge, drop shadow 0.1 / 0.02 / 0.4.
- Wipes left to right over the spoken words, one stroke per line.
- **Strokes must sit under the zoom.** Either put them in the V3 comp upstream of Transform_Zoom, or hold the zoom still while any stroke is visible.

**S0.10 Medallion (P01).**
- White Ellipse 140 px with an Instance ring (9 px #FF5A1F + NeoGlow).
- The logo goes Loader → Transform, clipped to an 88 px circle.
- Variants: 72 / 96 / 120 / 128 px with 4–6 px rings.

**S0.11 Section slam.**
- Template: `tsb_V5_000480_1.comp` (identical to `ai4_V4_000000_1`).
- Transform Size 1.594 → 1.0 over 20 f, pivot (0.529, 0.67), MotionBlur Quality 10 / Shutter 330. GaussianBlur 0.4 → 0 over 6 f.
- A 28 f base clip on V2 at the chapter's first frame.

**S0.12 Sound cues.** On montage cuts, SFX Camera_01 at −33.2. On UI clicks and chips, Mouse Click (5) at −29.3.

---

## The constructs used on the B2B video (K1-K20, each copied from one of his comps)

- K1. Breaths and removals (plain A-roll on whole V1 clips; Samuel adds punch-ins)
- K2. UI demo: new HTML engine scene (V2 render + V3 S0.1/S0.2)
- K3. UI demo: re-render or re-key an existing render
- K4. Report or website page: lockup → spotlight → line marker
- K5. Website and logo lockup beats, and the brand beat
- K6. Chapter lower-third + section slam
- K7. 7-step roadmap motif
- K8. Tier card reveal (`ai4_V3_000723_1.comp`)
- K9. Glass checklist beside Alex (`ai4_V3_005556_1.comp`)
- K10. Rapid montage (one real source per spoken item)
- K11. People B-roll beats
- K12. Number contrast flanking Alex (4 AI C20 layout from stills `qa\finals\ai4z` at 559.02; placement `apollo_V3_001190_1`)
- K13. Cards beside Alex
- K14. Logo tiles over the A-roll (`apollo_V3_003928_1.comp`)
- K15. BGORANGE motion graphics
- K16. Caption family (rotated so neighbours differ)
- K17. CTA caption (`apollo_V2_013082_1` / `apollo_V3_005918_1`)
- K18. Green/red concept cards (`tsb_V3_001154_1.comp`)
- K19. Overlay fixes over the A-roll (existing V4 comps)
- K20. Global polish (P3)

Full construct specs with every instance: the job's build list, section 5.

Back to [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]]
