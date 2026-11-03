---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: C11
---

# C11 · 3D elements

> **Read when:** a beat needs a laptop, a logo ring, a hologram, a 3D icon or tile, or any depth (visual plan, intro builds, beat reviews). **Client values:** whether 3D is allowed in charts and the client's ring colour: [[03-Areas/video-editing/rulebook/rb-k2-alex-frontal|K2 Alex / Frontal]], [[03-Areas/video-editing/rulebook/rb-k3-gamma|K3 Gamma]]. **Status:** draft, not yet approved by Samuel.

## Rules
### When to use 3D
- **C11.1** Use 3D where it earns it: laptops, hero objects, logo rings, the tier pyramid. Everything else stays flat. ✅ *"making things look 3D when needed"* (2026-10-20)
- **C11.2** No tilted or rotated flat cards. ✅ *"I don't like the rotation"* (2026-09-30) · 🎬 no 3D tilt in the Apollo graphics → Q-C11.a
- **C11.3** Real 3D, not faked: real meshes (the FBX laptop, an FBX tier pyramid), Extrude3D shapes and real lights; never painted shading or faked perspective. ✅ *"let's create the box with shape 3D and the light and the extrude, not making sides"* (2026-08-14)
- **C11.4** Hero objects get depth: a NeoReflection floor reflection under them, perspective. Glossy 3D tiles with a reflection are approved vocabulary. 🎬 (TSB) · ✅ (gallery C04, 2026-09-30)

### The 3D laptop
- **C11.5** Laptop beats copy his TSB laptop: a big real 3D MacBook (`macbookpro.fbx`), the whole laptop on screen (lid and deck) at a 3/4 angle, the UI playing on its screen, a smooth entrance (his spin: Y-rotation −62 → 18 over 43 f), then a smooth push into the screen to full frame with a clean transition. ✅ *"look at how I did laptop visuals in the last intro, this looks very bad for an intro"* (2026-10-15) 🔁3 (2026-10-14, 10-15, 10-16)
- **C11.6** It must read as 3D: not a flat laptop sliding in, not a lid rising from the bottom edge. The content sits inside the screen. ✅ *"it felt like a 2D laptop that was coming in... it should feel inside of the laptop"* (2026-10-15)
- **C11.7** The screen fits the lid: inside it, with a black bezel and a thin silver rim, never wider than the lid, no white gap or light band, and still fitted through the push-in. ✅ *"The top has a large white gap, that's not how a laptop screen looks"* (2026-10-16) 🔁2 · approved after the fix: *"Laptop looks right now, carry on."* (2026-10-16)
- **C11.8** Approved extras on the LinkedIn intro: the laptop big and in front of the speaker in the middle, a flat platform logo above the lid that animates in with it "like a small crown", dynamic typography at his side. ✅ (2026-10-14)
- **C11.9** Fitting a screen taken from a template rig: render the lid and the screen alone and compare their corners; fix z-fighting with a separate render pass, never by floating the screen off the lid; scale the screen and the camera path about the same point. ⚙️ (2026-10-16)

### Rings, holograms, 3D icons
- **C11.10** Icon rings around the speaker: icons shrunk with a 3D Transform, 10 per ring 36° apart (radius ≈ 0.28), pivots at the ring centre, the second ring on its own axis, Camera3D framing the background with his cutout in the middle, a line per ring in the client's colour with Neo Glow, MagicMask so tiles and title pass behind him. ✅ (2026-09-26) · 🎬 AI4 hook: 20 real app-icon tiles on ImagePlane3D (Scale 0.075), rings drop Y 0.618 → 0.087 over f4-28, group Z-rotation 8 → −8 over 99 f
- **C11.11** Rings move at a steady speed and tilt gradually around the speaker. Set the rig up; Samuel animates the spin. ✅ *"Don't add the rotate animation, I would do it, just set everything"* (2026-09-26) → Q-C11.b
- **C11.12** Hologram: a screenshot in DVE 3D (X 20°, Y 28.2°, Z −8.3°) planar-tracked above his laptop, MagicMask on his hand, Neo Glow, a LumaKeyer screen-light merge. 🎬 (TSB)
- **C11.13** A 3D icon or box: sRectangle (the vector Shape tool) → Extrude3D (Depth > 0, Bevel Depth > 0, Front Bevel on, Back off, smoothing up) with Phong materials on face and bevel; the logo as its own ImagePlane3D just proud of the face, with cast and receive shadow. ✅ (2026-08-14)
- **C11.14** Ruled out: Shape3D Cube (no corner rounding); a raster mask into Extrude3D (won't feed). A custom OBJ mesh only if the Extrude3D bevel looks faceted. ⚙️

### The rig
- **C11.15** Standard rig: ImagePlane3D + Camera3D + AmbientLight + 2 DirectionalLight + 2 SpotLight → Merge3D, two Renderer3D outputs (the object, and one through Opacity → GaussianBlur for a real floor reflection). 🎬 (7M)
- **C11.16** A static hero reflection mirrors the geometry (Merge3D under a Transform3D at Scale Y −1, one render pass). The camera-mirror method only for moving cameras (it costs a second Renderer3D every frame). 💡
- **C11.17** Shape3D torus line thickness = `SurfaceTorusInputs.Section`. ⚙️ Rig recipes in full: [[03-Areas/video-editing/fusion-recipes|Fusion recipes]] and [[03-Areas/video-editing/fusion-node-system|Fusion node system]] (Recipe 8).

## Never
- **C11.18** Flat cards tilted or rotated to fake depth. ❌ (2026-09-30)
- **C11.19** A laptop that reads as 2D, or a screen that overhangs the lid or leaves a gap. ❌ (2026-10-15, 2026-10-16)
- **C11.20** UI covering the whole laptop before the push-in. ❌ *"you are covering the whole laptop, I want to see the linkedin animation on the laptop"* (2026-10-15)

## Pictures
- (no picture yet: the approved LinkedIn intro laptop after the 2026-10-16 fix, beside his TSB laptop frame)

## Questions for Samuel
- **Q-C11.a** The creative director likes a slight side angle on cards (2026-10-22); you said "I don't like the rotation" (2026-09-30). → Options: (1) flat cards always. (2) A slight angle allowed on hero card rows only. My pick: (1) until you say otherwise.
- **Q-C11.b** Ring spin. On 2026-09-26 you said you animate it yourself. Agents now deliver finished visuals. → Options: (1) agents animate it like your AI4 hook (steady spin, gradual tilt) and flag it for you. (2) Agents set up only. My pick: (1).
- **Q-C11.c** Phones and 3D cameras: no source has a rule yet. What do you want for a phone mockup or a 3D camera move?

## Sources
Draws on and replaces the 3D rules in [[03-Areas/video-editing/ways-of-working|Ways of working]], [[03-Areas/video-editing/visual-vocabulary|Visual vocabulary]], [[03-Areas/video-editing/fusion-recipes|Fusion recipes]], [[03-Areas/video-editing/fusion-node-system|Fusion node system]], [[03-Areas/video-editing/edit-grammar/edit-grammar-tsb|Edit grammar TSB]] and [[03-Areas/video-editing/edit-grammar/edit-grammar-ai4|Edit grammar AI4]], plus his LinkedIn intro markers.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
