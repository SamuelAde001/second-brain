---
type: knowledge
area: video-editing
status: needs-input
source: claude-export
updated: 2026-09-20
tags: [fusion, graphics-pipeline, tooling]
---

# TSB graphics pipeline — HTML scene to native Fusion comp

Source: `tsb-graphics-pipeline.md` in the claude-export, dated 2026-09-19 (document's own subtitle: "third pass: every graphic that is not a screenshot or UI mockup is now a Fusion comp; `accounts` converted on request later the same day; `lego2` rebuilt fully native the same day"). Where the edit is: **Timeline 2, from 3:06 to 10:40**. Backup of the pre-edit state: **"Timeline 2 - BACKUP before Claude."**

This is a different system from [[fusion-node-system]]: that note documents Samuel building Fusion node trees by hand inside Resolve. This note documents a custom **compiler tool** — an HTML/JS scene gets recorded, extracted and compiled straight into a `.comp` file, which is then dropped onto a timeline clip. The two systems share vocabulary (NeoAnim, RectangleMask/Background rigs, Merge collectors) because the compiler outputs the same kind of node trees Samuel builds manually.

## What "TSB" stands for

The document never spells out "TSB" as an acronym anywhere in its text. The strongest evidence is the document's own title: **"Taking a Step Back from Claude: how the 3:06 to end visuals were built."** Every comp, folder and carrier-clip name in the document carries a `TSB_` prefix — `TSB comps/`, `TSB_lego2`, `TSB_accounts`, `TSB_whiteboard_376`, `TSB_rule_249`, `Claude TSB/carrier_[0000-0719].png`. The initials of "Taking a Step Back" are T-S-B, matching every prefix used. That correspondence is the only evidence in the source — it is not stated outright, so treat it as a strong inference, not a confirmed fact.

**Which client/project this belongs to — needs-input.** The document never names a client. The one internal clue is in "Real sources used" (below): the graphics pull from "Frontal case studies: AirOps, Design Pickle and Teikametrics" — Frontal is Alex's agency (see [[03-Areas/video-editing/clients/routerise|Routerise]]), which suggests this is Routerise/Frontal work, but the document doesn't confirm it and doesn't say whether "Timeline 2" here is the same Resolve project/timeline referenced elsewhere in [[routerise-house-style]]. Consistent with the flag already recorded in [[03-Areas/video-editing/clients/routerise|Routerise]] ("Client attribution for this document is itself unconfirmed"), this is left unresolved rather than guessed.

## The rule that drives everything

Samuel, 2026-09-19: **"graphics are always nodes."**

> Every visual must be built from Fusion nodes so he can edit it later. No PNG sequences or rasterised graphics standing in for a visual. The compiler's raster fallbacks are not acceptable output.

Exception: the shared TSB background/grid/vignette plates (`r1`, `r2`, `r13`/`r14`) are still Loaders — everything else has to become real nodes.

**21 comps still carry a raster PNG-sequence fallback** and need converting the same way as `lego2`: `bigco`, `brain`, `bulbs`, `cutadd`, `cutnoise`, `donut`, `dopamine`, `flat`, `fuel`, `genai` (×2), `gps` (×2), `icp25`, `needle`, `noise1`, `noisesig` (×2), `paths`, `retreat`, `signoise2` (×2), `sigsell`, `sys247` (×2), `toolfirst`. Find them with:
```
grep -l '_0000.png' "TSB comps/fx/"*.comp
```

## Case study — TSB_lego2 (V2, 6391–6513), rebuilt native

Line: *"But most people added blocks instead, even though every single block they added cost them 10 cents."*

Samuel's direction: the added blocks go **on the sides of the Lego (the two pillars), increasing the height** — not a middle column. The old version was a single 122-frame PNG sequence (`fx_assets\lego2\r4_/r5_`) and was rejected.

New build script: `Claude Files\tools\build_lego2.py`, writes `TSB comps\fx\TSB_lego2.comp`. Old raster comp kept at `TSB comps\fx\_raster_backup\TSB_lego2_raster.comp`.

- Every brick = `RectangleMask` → `Background` (vertical gradient for top highlight / bottom shade), Instance mask with Solid off for the edge seam, Instance mask soft + offset for the drop shadow, stud masks chained through `EffectMask`.
- **`RectangleMask_Stud_Master` drives every stud** — bricks, base plate and roof are Instances with only Center deinstanced.
- One 2-stud brick shape (`RectangleMask_Brick_*`) shared by three colour sets (Orange / Yellow / Blue). Each placed brick is a `Transform_Brick_*` of its colour master.
- Added blocks alternate right, left, right, left, right at **f16/28/40/52/64**; each slides in from its side (Transform with MotionBlur on), lands at t+10, and the roof lifts that side and settles (overshoot + settle). Build ends level, two bricks taller, at **f75**.
- Roof pose computed from the two pillar heights (Pivot at roof bottom-centre; Center Y + Angle splines). Wobble f0–16.
- `+10¢` = one TextPlus + glow, five Transform placements on the inner side of each new block. Cost card **$0.00 → $0.50** in steps on each landing (f26/38/50/62/74); card moved to **x 1470** so the raised roof clears it.
- `Transform_Lego_Structure` (identity) moves/scales the whole build. 20 labelled Underlays; layout = rows + vertical collector columns.
- Verified by Deliver-page frame grabs at **f0/12/19/21/27/39/45/57/58/76/80/110**.

## What's on the timeline now

- **67 editable Fusion comps (clip colour Apricot).** Each is a transparent carrier clip (`Claude TSB/carrier_[0000-0719].png`) whose comp is named `TSB_<name>`.
  - Split scenes use offset comps: `TSB_whiteboard_376` and `TSB_rule_249`. Fusion comp time starts at the clip's in-point, so every keyframe is shifted.
- **Built from Samuel's own templates:** lower thirds — `askq`, `attention`, `choose`; Steve Jobs quote — `jobslt`; B-roll caption cards — `cap_newstuff`, `cap_claude`, `cap_build`.
- **Still rendered video (13 clips)** — only the ones that are screenshots or UI windows: `airops1/2/3`, `nature`, `dp1`, `dp2`, `teika`, `book`, `replies`, `tracker`, `tabs` (×2), `jobpost`.
- **B-roll treatment.** 14 teal NeoAnim + Vignette adjustment clips on V3. The B-roll clips' own comps are passthrough.
- **Zooms.** 34 MagicZoom adjustment clips on V2.

## Case study — TSB_accounts (V2, 5610–5750), converted from MP4 to a native comp

Line: *"...what we did was cut all of the accounts that didn't matter so they could focus on the ones that actually did."*

Samuel asked for this one to be a Fusion comp rather than a rendered video. Same design as the MP4 (HubSpot target-accounts table, 14 of 18 rows struck and faded, 2,400 → 180 counter, 4 rows flip to TIER 1, CUT / FOCUS chips).

Built with `fu/build_accounts.py` (in the compiler zip). On top of `compile2` it:
- fixes the TIER pill (was orange from frame 0; now grey until the f98 swap, then orange),
- drops the sampled-width Transform the counter groups got (it squashed the text) and right-justifies the counter (`HorizontalLeftCenterRight = 1`) so "2,400" grows leftwards,
- forces the thousands-comma expression (`compile2` only picks it when the FINAL counter text has a comma),
- renames every flow node to start with its node type (`Transform_`, `RectangleMask_`, `TextPlus_`, `Background_Canvas_`, `Loader_Plate_`...),
- adds 22 labelled Underlays (window, counter, each ROW KEEP / ROW CUT, both chips) and spaces the row segments apart.

Assets: `TSB comps\fx_assets\accounts\` (r1 plate, r2 grid, r6 header rule, scissors + crosshair icons). Verified by Deliver-page frame grabs against the HTML scene: matches, including the counter comma and final frame.

## How the native comps are made — the pipeline

1. **Design.** Each graphic is first built as an HTML scene (`engine/scenes/*.js`), timed to the word-level transcript.
2. **Extract.** `extract_run.js` loads the scene, records every animation call and walks the DOM. It outputs a layer tree: cards, pills, text lines with per-word colours, icons, images, raster shapes and animations.
3. **Compile.** `compile.py` writes a `.comp` using standard nodes only:
   - **Cards:** `Mask_*` RectangleMask plus Instance masks for Line, Glow and Shadow (the box-with-outline rig — see [[fusion-node-system]] Recipe 1), and Background fills (gradient where the design has one).
   - **Text:** `Text_*` TextPlus in Geist ExtraBold/Black, with `StyledTextCLS` for word colours, and a TextGlow instance + Blur for glowing titles.
   - **Assets:** `Icon_*` / `Img_*` / `Plate_*` Loaders from `Claude Files\TSB comps\fx_assets\<scene>\`.
   - **Animation:** `XF_*` Transform with an XYPath (slide), Size and XSize splines, a `Blur_*` spline, Merge Blend (fade), `Shine_*` BrightnessContrast with a moving angled mask (sweep), and a TextPlus `Count` user control with a `Text(string.format())` expression for counters.
4. **Templates.** `templates.py` edits his comps directly: text, char-range highlights (`Char1RangeLow/High` are fractions of the character count), `InOffsetF` start offsets, and caption-card width measured from the text.
5. **Place.** `Claude Files\tools\tsb_fxplace.py` deletes the matching TSB_ clip, appends a carrier of the exact length and imports the comp. To swap a comp on an existing clip: `tools\fxapply.py` (import, keep one comp, rename).

Source for all of this: `Claude Files\tools\fusion_compiler.zip`.

### Restoring the extractor environment (not carried by the zip)

- `engine/assets/Geist-Variable.woff2` + `GeistMono-Variable.woff2`: from the npm `geist` package (`dist/fonts/...`).
- `engine/icons/*.svg`: from npm `lucide-static` (`icons/`).
- `engine/assets/words.js`: `window.WORDSDATA = <words_timeline2.json "words">;`
- `engine/assets/rects.js`: `window.RECTS = {};` is enough for scenes without screenshots.
- Check: re-extracting `flat` reproduced `fu/json2/flat.json` byte-for-byte and `TSB_flat.comp` at the same size.
- Run: `NODE_PATH=<global node_modules> node engine/extract_run2.js <scene>` then `python3 fu/compile2.py <scene>` (outputs to `fu/out/`).

## Compiler v2 (`extract2.js` + `compile2.py`)

- Samples every element on every frame, so tick-driven motion becomes keyframes: translate, rotate, scale, opacity, blur, grayscale and width.
  - Channels driven by WAAPI animations keep exact bezier keys.
  - Channels driven only by `tick()` get line-simplified (RDP) linear keys in an `XFs_*` Transform.
  - A static CSS transform becomes an `XF0_*` Transform.
- **Changing text:**
  - Numbers become a `Count` user control with an expression; comma thousands use a `:` Lua expression.
  - Typed text becomes a `Chars` control with `string.sub`.
  - Swapped labels become separate text nodes with step blends.
- Colour/background/border animations crossfade two versions of the box (`Was_*` / `Now_*`).
  - **Known gap:** a colour change driven only by `tick()` (e.g. a pill switching colour on a frame) is NOT detected — the box is extracted in its final colour. Split it into Was/Now boxes by hand (see `build_accounts.py`).
- **Raster fallbacks — NOT ACCEPTABLE to Samuel** (see the rule at the top); must be rebuilt as nodes:
  - SVGs are pixel-diffed across 5 frames: static ones become a single PNG, animated ones a PNG sequence.
  - Dense text-free subtrees (more than 60 elements, e.g. people grids, building rows, Lego builds) become one raster or sequence.
  - Identical PNGs share one Loader.
- **Fonts:** ✓ ✕ render in "Segoe UI Symbol," because Geist lacks them. Georgia uses 0.725× the Geist size factor.

## Calibration facts (verified by render)

- **StyledTextCLS ranges are inclusive:** `{id, start, end}` colours characters start..end, so pass `end = exclusive_end − 1`.
- **TextPlus Size:** ≈ 0.92 × css_px / 1080.
- **Transform Center** is a translation around (0.5, 0.5); Pivot is set separately. Angle rotates about Pivot (verified on the lego2 roof).
- **Background colours are not premultiplied.** Multiply RGB by alpha yourself, or low-alpha fills show up bright.
- **Loaders:** set `PostMultiplyByAlpha = 1` for straight-alpha PNGs.
- **RectangleMask units:** Width is relative to image width, Height to image height. `CornerRadius = radius / (min side / 2)`.
- **Mask chaining:** a RectangleMask's `EffectMask` input takes another mask; default `PaintMode` "Merge" = union (options: Merge, Add, Subtract, Minimum, Maximum, Average, Multiply, Replace, Invert, None, Ignore). Instances (`SourceOp = "<master>"` + only the deinstanced inputs) work for masks and TextPlus.
- **Transform motion blur:** `MotionBlur = 1`, `Quality` (used 5) — verified input IDs via the API and by render.
- **Text+ `HorizontalJustificationNew` is ambiguous,** so each text line is its own centred TextPlus. For a right-anchored line use `HorizontalLeftCenterRight = 1` with Center.x at the right edge (verified on the accounts counter).
- **NeoMotionText Char1 colour:** in `v5_text` it defaults to black. Set `Char1ColorR = 1` explicitly.
- **Underlay `Pos` is the centre** of the underlay (matching how node Pos works); Size is full width/height.

## Resolve gotchas (from this project)

- **Paste goes back to the source clip's track,** not the destination patch. To paste adjustment clips on V3, first get a copy onto V3: paste on V4 in empty space, drag it down one track, then copy it from V3.
- **Split:** set the playhead with the API, click empty timeline space, then press Ctrl+\\. Typing a timecode in the same batch is unreliable.
- **A clip's last Fusion comp can't be deleted.** Rewire it to MediaIn → MediaOut through the Fusion API instead.
- **Re-importing a comp whose name already exists on the clip** (`ImportFusionComp` onto a clip that already has `TSB_<name>`) updated that comp in place — the clip still had one comp, carrying the new content (confirmed again on lego2).
- **`device_commit_files` can deliver a stale file** when the same outputs path is rewritten. Give every bundle a new name (lego2 used `outputs/_push/v1`, `v2` → `TSB comps\_incoming\vN\`), check md5 on the device, then copy into place.
- `device_commit_files` re-encodes PNGs (bigger files, different md5) but the pixels are identical — compare pixels, not checksums.
- **Fusion comp time is clip-relative.** A carrier appended with startFrame = N still starts the comp at 0, so split segments need their own offset comps.
- `AppendToTimeline` ignores startFrame/endFrame for single stills (fixed 120-frame length). Use sequences or video.
- Frame grabs: set Deliver `FormatWidth`/`FormatHeight` to the timeline's 1920×1080, one key per call, before the jpg jobs (done 2026-09-19 — reset to 3840×2160 before the final 4K export).
- TickTick steals focus from Resolve. Keep it on the computer-use allowlist.
- `device_bash` on his PC works again as of 2026-09-19 (python3, node, ffmpeg available in the Linux VM).

## Real sources used

- **Frontal case studies:** AirOps, Design Pickle and Teikametrics.
- **Other screenshots:** the Nature Lego paper, clay.com, apollo.io, and book.frontal.so.
- **McKinsey:** a quote card, because the site blocks automated capture.

## needs-input

- Which client/project this Timeline 2 build belongs to — not stated (see "What TSB stands for" above).
- Whether this "Timeline 2" is the same Resolve timeline referenced in [[routerise-house-style]] (which mentions a Timeline 2 used only for an MP3 transcription export) — not stated; could be the same project or a different one.
- Location and contents of `engine/scenes/*.js`, the HTML scene sources themselves, are referenced but not included in this document.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
