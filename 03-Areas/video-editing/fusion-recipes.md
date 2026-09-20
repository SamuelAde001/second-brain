---
type: knowledge
area: video-editing
status: needs-input
source: claude-export
updated: 2026-09-20
tags: [fusion, build-recipes]
---

# Fusion build recipes

Reproducible node-by-node builds, distilled from two Claude conversations: a shiny 3D icon build and a 40-image grid layout. Companion to [[fusion-node-system]], which covers Samuel's general node layout conventions (the spine/collector pattern, node naming `Type_Role_D##`, adjustment-clip system) — link there rather than repeating those rules here. General principle from [[fusion-node-system]] §8 applies to every recipe below: name new nodes `Type_Role_D##`, never rename Samuel's existing ones.

None of the recipes below were confirmed built and tested in a live Fusion project during these conversations — they're accurate node recipes handed over for Samuel to build, not verified renders. Follow them, but expect some tuning, same as any node recipe from a session where Claude couldn't test-render.

**Standing rule, Samuel's own words (2026-08-14):** *"Next time when I ask you something, look for other inbuilt ways of achieving that same result."* Before reaching for a custom/workaround build, search broadly for whether Fusion already has a native tool for it — don't anchor on the exact node name used in the request and stop looking the moment one specific limitation is confirmed. (This is exactly what went wrong before Recipe B below was found — see "Ruled out" at the end.)

---

## Recipe A — 2.5D glossy icon (compositing fake, no real geometry)

Status: given as a full recipe, **not the approach Samuel ended up using** for this icon (he wanted real 3D — see Recipe B) — but kept here as the lighter-weight technique for any icon where true 3D isn't worth the render cost. Described in the source as "indistinguishable" from real 3D for a static render, and much lighter on a 4GB-VRAM card.

Real hex values pulled directly from Samuel's reference image (not invented): base orange `#DE6435` → `#E97E58` (shifts warmer toward top-right), bevel highlight `#F0B5A1`, bevel shadow `#431000`, background `#131110` (not pure black), cast shadow `#571E0C`, logo white `#FBFBF9` (slightly warm, not pure white).

**1. Box base**
- `Background1` → flat fill, `#DE6435`.
- `Rectangle` mask, centered, corner radius ~18–20% of width (iOS-icon proportions). Use the native Radius/Corner control if your Resolve version has it on the Rectangle mask; if not, fake it: sharp-corner rectangle → `Blur` (~15–20px) → push contrast/threshold back up. Keep the blur radius small relative to the shape so only the corners round off, not the flat edges.
- Feed this mask into `Background1` — it's the box silhouette every downstream mask reuses.

**2. Bevel ring — the fake curvature, does most of the work of reading as "3D"**
- Duplicate the rectangle mask, scale it down ~6–8% inset, same center. `ChannelBooleans` (Subtract) against the original → a thin ring = the curved edge.
- `Background2` → linear gradient, angle ~135°, `#F0B5A1` (top-left) through the base orange to `#431000` (bottom-right).
- Merge that gradient into the ring mask only, ~85% opacity, Normal or Soft Light.

**3. Face gloss**
- `Background3` → radial gradient, center biased upper-left, `#E97E58` fading to transparent, Screen ~40%, masked to the whole box.
- `Ellipse`, small, heavily blurred (60–80px), positioned near (0.35, 0.18) normalized — the hard specular hotspot, Screen ~70%.
- Optional second, thinner diagonal `Ellipse` at lower opacity for a secondary reflection streak.

**4. Ambient occlusion**
- A second inset, deeper than the bevel ring (~12–14%), heavily feathered.
- Dark warm fill (`#2A0900`–`#431000`), Multiply, ~25–30%, biased stronger toward the bottom via a masked gradient — this is what makes the edges feel recessed instead of flat-pasted.

**5. Logo group**
- `MediaIn` (the logo asset) → `Transform`, scale to ~38–42% of box width, centered.
- Same bevel trick at small scale: inset the logo's alpha, subtract, thin ring, subtle gradient `#FBFBF9` → soft shadow, Soft Light ~60%.
- Tiny drop shadow: duplicate the silhouette → small blur (8–12px) → offset 3–5px down-right → dark, Multiply ~50%. This is what "seats" the logo into the surface instead of it looking pasted on top.

**6. Ground shadow + reflection**
- Duplicate the finished box stack, flip vertically, fade the alpha with a gradient over the bottom ~40%, darken/desaturate, Screen ~20–25% — the soft reflection under the box.
- Separately, a wide, heavily blurred dark ellipse directly under the box, Multiply, low opacity — the contact shadow. Cast-shadow color `#571E0C`.

**7. Background + grade**
- `Background4` — `#131110`.
- `ColorCorrector` — small saturation/contrast lift.
- Light `FastNoise`, Overlay ~3–5% — at UHD the large smooth gradients above will band without it; cheap on a T1000-class card compared to a heavier denoise/grain pass.

Assemble the seven groups through a Merge spine per [[fusion-node-system]] §3's collector convention, ending at `MediaOut1`.

---

## Recipe B — True 3D glossy box icon (native Extrude3D pipeline)

Status: the approach Samuel actually pursued after clarifying he wanted real geometry, not painted shading ("let's create the box with shape 3D and the light and the extrude, not making sides"). This is the corrected, native pipeline — see "Ruled out" below for what was tried first and why it was dropped.

**1. Shape → geometry**
- `sRectangle` — the vector **Shape Tool** rectangle, *not* the raster `Rectangle` mask tool (different icon, same toolbar area). Check **Solid**. Set Width/Height for the footprint. Push **Corner Radius** — a parameter built into `sRectangle` itself, independent of size — fairly high for the rounded-squircle look.
- A raster `Rectangle` mask painted onto a `Background` **cannot** feed `Extrude3D` — it produces pixels, not geometry. `Extrude3D` only accepts Fusion's vector Shape Tools (`sRectangle`, `sEllipse`, `sPolygon`, `sPath`), a separate system from masks/mattes.

**2. Extrude3D**
- Add `Extrude3D`, `ShapeInput` ← `sRectangle`.
- Set **Depth** (thickness) above 0, and **Bevel Depth** above 0 for the rolled edge.
- Enable **Front Bevel**. Leave **Back Bevel** off — it's hidden from camera on this shot and only costs render time.
- Push the **bevel smoothing-angle** control toward smooth — this is what decides whether the edge reads as a soft roll or a faceted chamfer.
- Requires Resolve/Fusion **18.6 or later** — confirm the version before relying on this node.

**3. Materials — Extrude3D has two separate inputs**
- One texture/material input for the **front face**, one for the **bevel band** — so the rolled edge can carry a shinier value than the flat face, which is what actually sells "glossy plastic" (the edge visibly shinier than the center).
- Material node: **Phong** (3D Material Nodes category; search "Phong" or shorthand `3Ph`) — purpose-built for the sharp, hard specular hotspot of injection-molded plastic. Fusion's four illumination shaders: **Blinn** (general-purpose default, reads matte/diffuse), **Phong** (tighter, sharper highlight — the right one here), **Cook Torrance** (more parameters, closer to a roughness/Fresnel model — reach for this if Phong's highlight feels too one-knob), **Ward** (anisotropic, for brushed metal — wrong tool for this).
- Wire Phong's output into Extrude3D's `MaterialInput` (front) and/or `BevelMaterialInput` (edge). Push **Specular Intensity** up on both, keep **Specular Exponent** fairly high for a small, hard, bright hotspot rather than a broad soft one — a bit more Specular Intensity on the bevel input specifically, since that's the part that should read shinier.

**4. Logo — a separate object, not a baked texture**
- `MediaIn` (the flat logo asset) → `Image Plane 3D`. Scale to ~75–80% of the box's flat front area.
- `Transform3D` → position at Z just proud of the extruded front face (small negative Z offset), so it's a physically separate raised piece, not a decal.
- Turn on **Cast Shadow** on the logo plane, **Receive Shadow** on the `Extrude3D` mesh, and set the key light's shadow type to **Soft**. Fusion renders the logo's own contact shadow onto the box automatically from this — no hand-painted shadow needed.

**5. Lighting**
- `Light3D` #1 (Point), upper-left-front of the box, shadows on — the key/hotspot light.
- `Light3D` #2 (Point or low-intensity Ambient), camera-side, low intensity, no shadows — fill only, keeps the shadow side off pure black.

**6. Camera + orientation**
- `Camera3D`, roughly centered, normal perspective (not orthographic — the bevel needs real perspective falloff to read).
- Easier than moving the camera: put a `Transform3D` on the box itself and rotate it a few degrees — **X ≈ −8°, Y ≈ −12°** — to reveal the top and left bevel, matching a classic hero-angle icon presentation.

**7. Assemble**
`Merge3D` (Extrude3D + Image Plane3D + Light3D key + Light3D fill + Camera3D) → `Renderer3D` → out to 2D comp for the background (`#131110`), a light `ColorCorrector`, and a touch of grain to kill UHD gradient banding.

**Honest caveat from the source:** untested in real Fusion — whether `Extrude3D`'s native bevel reads as a genuinely smooth curve or a faceted chamfer, even with smoothing pushed up, wasn't verified. If it looks faceted, the fallback is the custom OBJ mesh under "Ruled out" below, which has a guaranteed continuous quarter-circle bevel.

### Reflective surface — three tiers, cheapest first

1. **Fake it with specular (often enough).** No new node — just push the Phong/Cook Torrance Specular Intensity up, keep the highlight tight. Reads as reflective to the eye without needing environment mapping. Right amount of effort if the icon just needs to *look* glossy rather than mirror an actual room.
2. **Real environment reflection — the `Reflect` material node (`3Rr`).** Feed an equirectangular ("latlong," 2:1 aspect) image through a `SphereMap3D` node first, which wraps it into a spherical environment. Connect that into `Reflect`'s **Reflection Color** input. `Reflect` also takes a **Reflection Intensity** input (alpha-masked — the bevel can be made more reflective than the flat face) and a **Background Material** input for the base diffuse. In Controls, set reflection strength to **By Angle**, not Constant — gives Fresnel-style falloff (more reflective at grazing angles, less face-on), which reads far more like real plastic/glass. Limitation: this is environment mapping only — it won't reflect the logo plane or the box's own bevel, just whatever image is fed to the sphere map.
3. **One object actually reflecting another** (e.g. a glossy floor reflecting the box). Fusion's 3D renderer is not a ray/path tracer, so there's no native support — both options below are workarounds. (a) Cube-map trick: six cameras + six `Renderer3D` passes baked into a cube map fed to `Reflect` — real, but heavy; not recommended on a 4GB card. (b) Mirrored-camera trick — the one actually used for the floor reflection here, see Recipe C.

Recommended starting combo for a static icon: tier 2 (`Reflect` + `SphereMap3D`, By Angle) layered on top of the Phong specular from the material setup above.

---

## Recipe C — Mirrored-camera floor reflection

Status: worked through step by step at Samuel's request, citing Bryan Ray's documented Fusion technique (the coffee-cup-and-saucer tutorial). Two sub-options exist — the camera-mirror method he asked for, and a cheaper geometry-mirror alternative recommended specifically for this static shot.

1. **Establish the floor's world Y height** — where the box sits. If the floor is at world Y = 0, `Transform3D`'s default pivot already works correctly for the scale flip. If not, offset the pivot/Center Y to the floor's actual height before applying the scale.
2. **Instance the camera, don't just duplicate it.** Fusion's **Instance** tool keeps the copy linked to the original, so any later animation on the real camera propagates automatically to the mirrored one — a plain duplicate needs manual re-syncing.
3. Feed that camera instance into a new `Transform3D`. Unlock the scale axes and set **Scale Y = −1.0** — one negative-Y scale correctly flips both position and orientation together as a single matrix operation. Don't try to hand-derive mirrored pitch/roll by flipping Euler-angle signs — it's error-prone and convention-dependent; let the negative-scale transform do the math.
4. Feed the `Transform3D` output into a second `Merge3D` alongside the same scene geometry.
5. Duplicate `Renderer3D` so the new copy points at the mirrored camera instance specifically.
6. Composite: layer the mirrored-camera render beneath the beauty render. Expect to still manually nudge the `Transform3D`'s **Translate Y** to get the reflection's contact point to line up with the object's bottom edge — even the source tutorial describes this alignment step as "tedious and time consuming," a normal part of the process, not a sign something's wrong.
7. In 2D: reduce the reflection layer's opacity, add a vertical gradient/fade mask for falloff, apply a slight blur (glossy, not mirror-perfect), and darken/desaturate slightly — real floor reflections read dimmer than their source.

**Cost flag, explicit in the source:** this technique costs a full second `Renderer3D` pass every frame. Worth it for a moving camera or animated scene. **For a static hero shot with no camera movement** (which this icon actually is), mirror the object's geometry instead — duplicate the box+logo `Merge3D` group behind a `Transform3D` with Scale Y = −1, single render pass — identical result for half the GPU cost. Recommended default on a 4GB-class card; reserve the camera-mirror method for animated/tracked shots.

---

## Recipe D — Uniform card grid from N images (40-image / 4×10 worked example)

Status: built and iterated with Samuel across two rounds in the same conversation — the per-card node chain and grid math below match his own confirmed reference card. Two explicit corrections he gave mid-build are folded in as rules, not left as the original (rejected) approach.

**Per-card node chain**, repeated once per image:

`MediaIn` → `Transform` (cover-fit scale, unique per image) → `Merge` onto a transparent canvas (forces the Domain of Definition to the full comp resolution before the mask math, since the crop mask is defined in full-canvas coordinates) → `MatteControl` (crop, using a `Rectangle` mask, **inverted**, small corner radius) → `Transform` (uniform size-down, identical value across every card) → `Transform` (grid position — unique Center per card) → `DropShadow` (last node in the chain).

All per-card chains then merge sequentially onto one shared canvas via a `Merge` chain, ending at a single grid output that feeds into the comp's existing background branch → Adjustment Clip → Media Out.

**Per-card cover-fit scale — a formula, not a guess:**

```
Size = max(target_crop_width / native_width, target_crop_height / native_height) × safety_factor(~1.01–1.02)
```

Calibrated against Samuel's own proven value: a 928×1152 source image at `Transform.Size = 0.917`, which the math confirms fully covers an 838.92×1053px crop rectangle (height is the binding constraint). Every image gets its own correctly-derived Size instead of a shared guess — necessary because every source image has a different native resolution.

**Grid math (4 rows × 10 columns worked example, 1920×1080 canvas):**
- Reference crop mask: 838.92 × 1053px (~4:5 portrait — the target every image is cover-fit and cropped into).
- Uniform grid-scale factor (the second, identical Transform on every card) = the minimum of (cell width ÷ card's fractional width) and (cell height ÷ card's fractional height). Worked out to **0.203** for this 4×10 grid with margins/gutters — final on-screen card size ≈ 170.5 × 213.9px, enough to breathe with drop shadows visible without cards touching.
- Grid cell centers, from margin fractions + gutter spacing. Fusion's Y-axis increases upward, so: `topY = 1 - gridMarginY - cellHeight/2 - row*(cellHeight+gutterY)` — top row gets the highest Y.
- Reading order: card 1 = top-left, filling left → right, then top → bottom.

**Ambiguity worth flagging if this recurs:** "each row should be 10, 4 columns" doesn't disambiguate 10-rows-of-4 from 4-rows-of-10. Resolved here by picking whichever orientation keeps grid cells closer to the source cards' own aspect ratio (portrait cards → 10-per-row/4-rows keeps cells roughly portrait; the other way makes cells absurdly wide and flat). Confirm explicitly with Samuel if it's not obvious from the source material.

**Two corrections Samuel gave mid-build — both are now the rule, not an option:**

1. *"I don't like the shared Grid mask and the Shared Grid canvas... I want every Mask and canvas to be stand alone"* — for neatness and later per-card adjustment, and to avoid one shared node fanning long connector lines out to every card. **Rule: give every card its own `Rectangle` mask and its own canvas `Background` node**, even though this means more total nodes (40 of each, in this example) instead of one shared pair. Do not default to sharing a mask/canvas across a batch of repeated card builds.
2. *"I want the images to be re-arranged based on the names, so that identical cards can all be together in one place in order of how they where made"* — group images by concept and revision lineage (an original next to its "Fixed" version, a draft next to its final revision), walked through in the order the material was actually made/used — not raw filename or import order. Worth defaulting to this for any future multi-asset grid or montage.

---

## Ruled out (context, so the same research loop doesn't repeat)

- **`Shape 3D` Cube primitive has no native corner-rounding control** — confirmed limitation (Blackmagic forum). Don't reach for it expecting rounded edges; this is what sent the first pass down the custom-mesh route below.
- **Custom rounded-box OBJ mesh**, generated in Python (superellipse cross-section, quarter-circle bevel sweep around the visible front perimeter, ~954 verts) and imported via the `FBX Mesh 3D` node — which despite its name also accepts OBJ/3DS/DAE/DXF. A working, guaranteed-smooth fallback, but superseded once the native `sRectangle → Extrude3D` pipeline (Recipe B) was found. Keep it as the fallback specifically if `Extrude3D`'s bevel reads faceted even with smoothing pushed up.
- **Text3D's extrude/bevel** is real but limited to text glyphs (a custom-font-glyph workaround exists to extrude arbitrary shapes through it) — unnecessary once `Extrude3D` is known.
- A raster `Rectangle` mask on a `Background` cannot feed `Extrude3D` directly — see Recipe B step 1. This was Samuel's own proposed workflow, corrected mid-conversation to the vector Shape Tools instead.

Back to [[03-Areas/video-editing/_index|Video editing]]
