---
type: knowledge
area: video-editing
status: needs-input
source: claude-export
updated: 2026-09-20
tags: [fusion, routerise]
---

# Routerise Fusion node system

Node layout, adjustment-clip system, and reusable build recipes, reverse-engineered from the reference project **"$7M Founder: How I Use Claude for Cold Outreach (B2B sales)"** (client Alex / Frontal, [[clients/routerise]]) — 107 Fusion comps, 3,612 raw tool instances. Companion to [[routerise-house-style]] (pacing/sound/colour) and [[cut-sheets]] (pre-production planning). Corrected against Samuel's own screenshots of his real node trees (`node-graphs-SAMUEL/`, 14 images) — **those screenshots are the authoritative reference for arrangement, over anything reconstructed from raw comp coordinates.**

**Corrections note:** an earlier pass of this study misread four things, corrected here after Samuel answered directly: (1) Geist, not Open Sans, is the house font going forward; (2) clip colours *are* the chapter system, not a rotating cycle; (3) the 1080p timeline / 4K export split is deliberate, not accidental; (4) the V1/V7 duplication is a deliberate clean/PiP switch, not a workflow accident. See [[routerise-house-style]] for the style-facing side of these.

## 1. Tool usage across the reference project (107 comps)

Raw counts are misleading: `LUTBezier` (711) and `LUTLookup` (644) are internal to the NeoAnim macro (~11 animation-curve controllers per instance) and `AudioDisplay` (228) is just MediaIn audio pins. Stripped of those, the real picture:

| Tool | Count |
|---|---|
| Merge | 430 |
| Background | 278 |
| MacroOperator | 224 |
| RectangleMask | 169 |
| MediaIn (Loader) | 168 |
| Transform | 97 |
| Text+ | 73 |
| ResolveFX GaussianBlur | 51 |
| EllipseMask | 43 |
| Fuse.NeoMotionText | 32 |
| ResolveFX Vignette | 31 |
| ResolveFX DropShadow | 28 |
| MatteControl | 16 |
| MagicMask | 4 |
| 3D (Renderer3D / Camera3D / SurfaceFBXMesh / MtlBlinn / lights) | ~27 |

**Complexity is barbell-shaped:** 59 comps at 1–3 tools (tiny), 18 at 4–10, 13 at 11–30, 13 at 31–80, and 4 "hero" builds at 80+ tools. Median comp = **3 tools**, mean = 16.5. Rule: keep comps small; reserve big set-piece builds for 3–4 moments per video.

**Macros actually used:** NeoAnim (107 instances / 62 comps — the workhorse), NeoLightSweepPro (60 / 25), Samuel's own ScreenFocusEmphasis (18 / 18), NeoBevel (16 / 9), NeoGlow (14 / 5), NeoHighlighter (6 / 4), NeoTextMotion / DreamGlow (1 each). Fuses used: `Fuse.NeoMotionText` (32), `Fuse.PizzaBlu_Outline_001` (8, the "Outline1" node), `Fuse.Duplicate` (7). ResolveFX inside Fusion: GaussianBlur (51), Vignette (31), DropShadow (28, strength mostly 0.5), Grid (7), MosaicBlur (7, `PixelFrequency 200` — used to pixelate private on-screen info).

**Installed but not used on this project:** 184 macros total on the shelf. The entire PJT text-animator pack (62 `pjt_*_ta` presets) went unused, as did most of "My macros" (Arrowline, Number Counter, Text_Infinite_Scroller, Glass effect, Shine box with text, Rectangle_V3, Boxed text…), the Neo Texts preset library (~100 CBC/WBW/Text × FadeIn/PopUp/Slide/Rot presets), and fuses Drain, Smoke, Funky Smoke, PixelSorting_XS, RevRectangle, Neo_Glitch, Neo_Chroma, Neo_Shatter, Neo_Tritone, Neo_LongShadow, Neo_LensDistort. Only third-party OFX installed: `HiggsfieldColorMatch.ofx` (not used here). **Open question:** deliberate exclusion (doesn't fit the look) or just "NeoAnim is faster to reach for" — unresolved, worth asking before assuming either library is off-limits.

Edit-page effects (invisible to the scripting API — recovered from the exported DRT `FieldsBlob`, hex-decoded): **SSC PiP Pro** (Stirling Supply Co, 81 clips — the PIP, see [[routerise-house-style]] §7), **MagicZoom V3** (MrAlexTech, 51 clips — zooms, see house-style §6), **Neo Highlighter Pro** (2 clips, as an Edit-page Generator — the orange highlighter bar over on-screen text).

## 2. Adjustment clips — the system

Samuel's own description: *"Adjustment clips are my most flexible system… some have nodes in fusion, some have plugins in edit page, some are just for zooms."* **117 adjustment clips** in the reference, breaking down as:

| What it carries | Count | Share |
|---|---|---|
| Fusion comp only | 52 | 44% |
| Fusion comp + MagicZoom V3 | 32 | 27% |
| MagicZoom V3 only | 19 | 16% |
| Transform only (reframe) | 12 | 10% |
| Empty / pass-through | 2 | 2% |

**All 51 MagicZoom V3 instances in the project sit on adjustment clips — none on a source clip.** 32 clips carry both a Fusion comp and MagicZoom V3 stacked together (graphic and camera move on one clip). Median adjustment-clip duration ~73 frames (3 s).

**By track — what each track is actually for:**

| Track | Composition | Reading |
|---|---|---|
| V2 | 17 MagicZoom-only, 6 Fusion-only | The zoom/move layer — mostly pure camera moves |
| V3 | 21 Fusion+MagicZoom, 17 Fusion-only, 1 MagicZoom | The workhorse — graphics that move |
| V4 | 18 Fusion-only, 12 transform-only, 7 Fusion+MagicZoom | Graphics + static reframes |
| V5 | 8 Fusion-only, 2 Fusion+MagicZoom, 1 MagicZoom | Overflow |
| V6 / V7 | 4 / 1 | Rare top layers |

**The three jobs, named:**
- **Job 1 — Reframe the whole stack** (12 clips, transform-only, mostly on V4): Zoom **1.16 / 1.30 / 1.33** with varying Pan/Tilt, some running 400–1059 frames. Punches into the *composited* result (screen recording + whatever graphics sit on it) without touching a source clip — this is why changing the framing costs one clip, not twenty.
- **Job 2 — Carry a Fusion build** (84 clips) — the graphics layer, see §4–5.
- **Job 3 — Carry an Edit-page plugin only** (51 MagicZoom, 2 Neo Highlighter). Neo Highlighter Pro sits on two Fusion Generator clips on V4 (at 3:35.1 and 3:36.6 in the reference) — the highlighter bar over on-screen text.

**Why this system works:** an adjustment clip can be moved, trimmed, duplicated, disabled and re-stacked without touching anything underneath. Stacking a Fusion comp *and* an Edit-page plugin on the same clip means one object owns both "what it looks like" and "how it moves."

## 3. Node layout convention (from Samuel's own screenshots)

The layout is **two-axis, not one spine** — three stages:

```
STAGE 1 — ELEMENT CHAINS (horizontal, left → right, one per visual element, stacked vertically)
  Instance_Rect ┐
  Rectangle ────┴→ Background → GaussianBlur → Merge → Merge → NeoBevel
                   → NeoLightSweep → DropShadow → NeoAnim ──┐
  (Text+ / PNG / Ellipse drop into this row from above)     │
                                                            │
STAGE 2 — VERTICAL COLLECTOR (a column of Merges on the right)
                                          Merge6 ←──────────┘
                                          Merge7 ←── row 2
                                          Merge8 ←── row 3
                                          DropShadow
                                             │
STAGE 3 — BASE SPINE (horizontal, along the bottom)
  Adjustment Clip → Merge2 → ────────────→ Merge1 → MediaOut1
                                             ↑
                                    (collector drops in here)
```

- Each visual element gets its own horizontal row; identical chains stack vertically (e.g. three pill rows, three numbered card rows).
- A vertical column of Merges on the right collects the rows in order, top to bottom.
- The source (Adjustment Clip / MediaIn) runs along the very bottom as the base layer; the collected graphics drop onto it at the final Merge.
- `MediaOut1` sits at the far bottom-right, always.

**Effects order on a row, consistent across screenshots:** `… → NeoBevel → NeoLightSweep → DropShadow → NeoAnim →` into the collector. `BrightnessContrast` (often masked by a Rectangle) appears late, just before/after the collector, to sit the graphic into the plate.

**Measured payoff — this is not a stylistic opinion:** across all 107 comps, only 2 actually use the `Merge_Spine` naming, and they are the two tidiest big builds in the project (median connection length 220–275 units). Every other comp ≥30 nodes runs a median link of 429, up to 1167 in the worst case (`V2 @6:55.0`, 57 nodes). **The spine convention roughly halves connection length.** 49 of 107 comps carry at least some semantic names even without the full spine layout, so the naming habit is spreading on its own.

**Node naming:** `Type_Role_D##` — e.g. `Background_LeadCard_Fill_D01`, `EllipseMask_Avatar_Border_D01`. Applied to 178 of 1,809 flow nodes (9%), concentrated in the newer cut-sheet builds; the rest are Resolve defaults. **Never rename Samuel's existing nodes.**

**Components get copy-pasted between comps.** Node names like `Merge_LeadCard_D01_2`, `Merge_LeadCard_D01_2_1`, `Background_LeadCard_Fill_D01_2` recur across *different* comps — a rig (e.g. Lead Card) is built once and pasted where needed. Worth formalising as a small library of `.setting` components (LeadCard, Avatar, Chip, Meter, NameBar) to paste from.

### Techniques the screenshots revealed that raw comp data alone did not
- **Dashed connector lines = `Polygon → Paint`.** Each dashed leader (e.g. pyramid to lead table) is a `Background2 → Paint1 ← Polygon1` pair, one per line, merged together — not `PolylineStroke`.
- **`Template` / `Template_1` nodes** — saved Fusion templates dropped in as a single node, then driven with `NeoLightSweep → NeoTextMotion → NeoAnim`. A component library already in practice.
- **NeoHighlighter chained 3×** on one screenshot/image to highlight three separate lines, then into `Outline1`.
- **`Outline1`** (the PizzaBlu Outline fuse) sits right after the text/image and before the Transform — used to outline text and screenshots, not as an afterthought.
- **MagicMask sits at the very bottom, next to the output.** The Adjustment Clip feeds *both* `MagicMask1` and the base `Merge1`; the masked subject merges back on top of the finished graphics (`Merge1 → Merge6 → Transform4 → MediaOut1`) — the hand-in-front-of-graphic move, always last in the comp.
- **The 3D rig:** `ImagePlane3D` + `Camera3D` + `Instance_Camera` + `AmbientLight` + 2× `DirectionalLight` + 2× `SpotLight` → `Merge3D1`, then **two** `Renderer3D` outputs — one for the object, one routed through `Opacity → GaussianBlur` for a real floor reflection (not a flipped copy).
- **Reused sub-chain signature**, appearing in nearly every build: `Instance_Rect + Rectangle → Background → GaussianBlur → Merge11_3_2 → Merge3_2_1_… → NeoLightSweep` — the frosted card with border, copy-pasted between comps.

## 4. Build recipes, node by node

**Recipe 1 — Box with outline** *(the foundation of everything)*
```
RectangleMask_X_Fill ─────────────→ Background_X_Fill    (dark fill: accent × ~0.10)
                    ↘
Instance_Rectangle (Solid=0, BorderWidth≈0.00184) → Background_X_Border  (bright accent)
                                                          ↓
                                              Merge_X_D01  (border over fill)
                                                          ↓
                                        NeoLightSweepPro   (the shine)
```
Verified colour pair (Frontal): border `#FF5A1F` (1, 0.3529, 0.1216), fill `#1B0903` (0.1059, 0.0353, 0.0118). `RectangleMask.CornerRadius` clusters: 0.30–0.34 cards · 0.66–0.81 pills · 1.0 full capsule.

**Recipe 2 — Circle with outline.** Identical to Recipe 1, with `EllipseMask_Avatar_Fill` + `EllipseMask_Avatar_Border` (instance, Solid off, border on).

**Recipe 3 — Avatar inside a circle**
```
MediaIn (photo) → Transform → MatteControl ← EllipseMask_Avatar_Fill
                                    ↓
                                 Merge (over Background_Avatar_Fill)
                                    ↓
                    Merge_Avatar_D01  →  Transform (position on card)
                                    ↓
                            Merge_Spine_D0n
```
`MatteControl` crops the photo to the circle — not a mask on the Merge.

**Recipe 4 — Frosted-glass panel**
```
RectangleMask → Background → GaussianBlur → Merge → Merge (EffectMask = the same rectangle)
```
51 GaussianBlur instances in the reference use this pattern — the translucent card look (e.g. the TIER 2 panel).

**Recipe 5 — "Emphasis reveal"** — 31 of 107 comps, the most-used pattern in the project
```
MediaIn1 → NeoAnim → Vignette1 → MediaOut1
```
Three nodes. Measured NeoAnim values: `Angle −90`, `InLength 20`, `StartBlur 5.5`, `StartOffset 0.0435`, `MotionBlur 1`. Vignette `Blend 0.835`, `anamorphism 1.78`.

**Recipe 6 — Screen focus** — 14 comps
```
MediaIn1 → ScreenFocusEmphasis (Samuel's own macro) → MediaOut1
```

**Recipe 7 — Hand/body in front of a graphic** — 4 comps
```
MediaIn1 → MagicMask1 ──→ Merge (as foreground, over the finished graphic)
```
Visible at 6:40 in the reference — Alex's hand passes in front of the 3D tier pyramid. Cheap depth, big effect.

**Recipe 8 — Real 3D**
```
SurfaceFBXMesh → MtlBlinn → Merge3D ← Camera3D + LightSpot + LightDirectional → Renderer3D
```
An imported FBX mesh, lit and rendered — the 3-tier pyramid graphic. Not faked perspective. Used in 2 comps.

## 5. Node tree → what you see on screen (worked examples from the reference)

| Time | On screen | Node structure |
|---|---|---|
| 0:44 | "SIGNALS" lead card, avatar, three orange outline chips with connector lines | 2× frosted-glass chains, `DropShadow` on each, `MosaicBlur` masking private data, `MagicMask` + `NeoAnim`, `MediaIn` entering bottom-right |
| 1:07.6 | "TOP ENGAGEMENT LIST" — stacked lead cards, avatars, white pill chips | 180 flow nodes; one element row per card (`RectangleMask_LeadCard_Fill/Border → Backgrounds → Merge_LeadCard_D01`), avatar via `EllipseMask + MatteControl`, all converging on `Merge_Spine_D01..13` |
| 1:48 | Neon outline funnel, dashed "FIT SCORE FILTER", glowing "YOUR BUSINESS" box | Outline-only shapes (masked Background, no fill), `NeoGlow`, counters as `TextPlus` |
| 3:35 | Orange highlighter sweeping over on-screen text | Neo Highlighter Pro as an Edit-page Generator on V4 (no Fusion) |
| 3:43–7:08 | Circular mirrored PIP over punched screen recording | No Fusion — SSC PiP Pro on 81 FlipX'd A-roll clips on V7 |
| 6:40 | 3D tier pyramid, hand passing in front, two-tone title | `Renderer3D` + FBX mesh; `MagicMask` for the hand; `TextPlus` white line + orange line |
| 6:57 | Translucent orange "TIER 2" card, words sliding up staggered | Frosted panel + `NeoBevel` + `NeoLightSweepPro`; per-word `TextPlus` → `NeoAnim` with staggered `StartOffset` |

## 6. NeoTextMotion

Samuel: *"I use a lot of NeoTextMotion for Typography."* In the reference: `Fuse.NeoMotionText` × 32, plus one `NeoTextMotion` macro instance — roughly one in three text elements (73 `TextPlus` vs. 32 `NeoMotionText`) is driven by it instead of plain `Text+` + NeoAnim. **Open question:** when to pick NeoTextMotion over `Text+ + NeoAnim` — per-character/word control, or just the faster starting point? Not resolved in the source material.

## 7. Screenshot reference — `node-graphs-SAMUEL/`

Samuel's own 14 screenshots of real node trees are the authoritative arrangement reference (raw comp coordinates alone under-describe the layout — see §3).

| File | Shows |
|---|---|
| S01 | Frontal site + three pill rows (OUTBOUND / ADS / CONTENT / REVOPS) — clearest rows → vertical collector example |
| S02, S08 | Minimal comps: Adjustment Clip → Merge → MediaOut1 with NeoTextMotion dropping in |
| S03 | Card + symbol + text with a secondary vertical collector |
| S04, S06, S12 | "SORTING INTO TIERS" — pyramid, lead table, Polygon→Paint dashed leaders |
| S07 | "YOUR CONTENT vs COMPETITOR" — MagicMask at the output |
| S09 | SIGNALS card with MosaicBlur privacy masking |
| S10, S13 | `Template` nodes used as single-node components |
| S11 | Three numbered card rows + NeoGlow |
| S14 | The full 3D rig, two Renderer3D outputs for object + reflection |

**Capture note for future sessions:** Resolve's Fusion Nodes panel **cannot** be captured by scripted GDI screenshots (`CopyFromScreen`) — it's a GPU surface and reads back solid black, while the Viewer beside it captures fine. Windows Graphics Capture tools (Snipping Tool, Win+Shift+S) work — that's how Samuel took these. Also: the Fusion page shows the comp of the clip *selected on the Edit page*, and `LoadFusionCompByName()` does not reliably change what `GetCurrentComp()` returns, so scripting a step-through of comps doesn't work either. **Ask Samuel for screenshots rather than trying to grab them.**

## 8. Rules this adds

- Default container for anything that isn't a source clip is an adjustment clip; one clip can own both the Fusion build and the Edit-page move.
- Never put MagicZoom on a source clip — always an adjustment clip above.
- Reframe a whole stack with a transform-only adjustment clip.
- One horizontal `Merge_Spine_D##` chain, left → right; each element's generator stack sits directly above its entry merge.
- Effects inline on the spine in order: NeoBevel → NeoLightSweep → DropShadow → NeoAnim.
- `MediaIn` enters bottom-right; `MediaOut1` far right.
- Name every new node `Type_Role_D##`. Never rename Samuel's existing nodes.
- Geist is the brand font (Alex/Frontal), not Open Sans. ALL CAPS bold for chips/titles; two-tone headline, white line + accent line.
- Accent colour is per-client. Frontal = `#FF5A1F`. Fill = accent × ~0.10. Border = the accent.

## 9. Still open

1. Should the tidy spine layout in §3 be enforced on every comp, or is sprawl acceptable for quick one-offs?
2. NeoTextMotion vs. Text+ + NeoAnim — what's the actual deciding factor (§6)?
3. Which Geist weights map to which roles (titles, chips, body)?
4. Is the PJT pack / Neo Texts library worth deliberately trialling on a future video, given it's installed but unused (§1)?

Back to [[03-Areas/video-editing/_index|Video editing]]
