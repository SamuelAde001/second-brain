---
type: sop
area: video-editing
status: approved
approved: 2026-11-05
updated: 2026-11-05
source: interview
tags: [rulebook]
section: B3
---

# B3 · Top main nodes and macros

> **Read when:** building or fixing any Fusion comp or adjustment clip (Editor, editor-builder, editor-worker), and before a review checks node choice. **Client values:** fonts, colours, corner shape and the client ground (BGFRONTAL, BGGAMMA) are in the client overlays: [[03-Areas/video-editing/clients/frontal-brand-v2|Frontal brand v2]] (K2), [[03-Areas/video-editing/clients/gamma|Gamma]] (K3). **Status:** approved by Samuel rule by rule, 2026-11-05.

## Rules

### His own tools, real nodes
- **B3.1** Build with his own macros and plugins: NeoAnim, NeoTextMotion, NeoGlow, NeoLightSweep Pro, Neo Highlighter Pro, Opacity, Arrowline, dashed line, Glass effect, Down fade, Number Counter, BGORANGE. Where his macro exists, use it. ✅ 🔁×3 *"use the tools I normally use, my macros"* (2026-09-25, 2026-09-27, 2026-10-03) · ✔ 2026-11-05
- **B3.2** Every effect is its real node: glow = NeoGlow, shadow = DropShadow, static shine = NeoLightSweep Pro, soft blur = ResolveFX Gaussian Blur, hiding blur = ResolveFX MosaicBlur. ✅ *"I always use actual nodes that can help me create those visuals"* (2026-09-25) · ✔ 2026-11-05
- **B3.3** His macros live in `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Macros\My macros\` (Box main, Down fade, shine, Glass effect, Arrowline, Moving dashed line, BGORANGE, Numbers, Number Counter, Blinking in, Screen Focus Emphasis, Opacity) and `…\Neo folder\` (Neo Anim, Neo Glow, Neo Bevel, Neo Light Sweep Pro, Neo Reflection, Neo Highlighter Pro). 🎬 · ✔ 2026-11-05
- **B3.4** Add new files only to those folders, and check his original's hash after. ✅ (2026-10-20) · ✔ 2026-11-05
- **B3.5** Reuse kits and scripts already built; build no extra kit the job doesn't need. ✅ *"We don't need those extra kits"* (2026-10-20); *"Don't, so that we don't burn tokens"* (2026-10-15) · ✔ 2026-11-05

### NeoAnim: every entrance and exit
- **B3.6** Every element comes in and goes out with NeoAnim (slide + blur + fade, Expo ease). The exit is part of the build. ✅ 🔁×4 *"always use Neo anim where something animates in and out"* (2026-10-03) · ✔ 2026-11-05
- **B3.7** One NeoAnim at the end of each node group, not keys on the group's Transforms and opacity. ✅ *"just add a neo anim at the end of the 4 nodes groups"* (2026-09-27) · ✔ 2026-11-05
- **B3.8** Place elements at their source (Transform), centred and spaced; NeoAnim stays at Global Center 0.5/0.5 and only animates. It may set size. ✅ *"don't use the neo anim to bring them down to the center"* (2026-09-27) · ✔ 2026-11-05
- **B3.9** Motion blur off on every NeoAnim (NAMotionBlur PassThrough). The soft entrance blur (StartBlur 25, or 5.5 for a crisper entry) stays. ✅ *"I don't want you to use motion blur because that makes it very hard to do"* (2026-10-28) · ✔ 2026-11-05
- **B3.10** Direction follows the element's side: Angle −90 = from below (default), −180 = from the left, 0 = from the right, 90 = drops (arrows, ticks). 🎬 · ✔ 2026-11-05
- **B3.11** StartOffset: rows 0.02-0.04, cards 0.05-0.08, pills 0.10-0.12, full-width titles 0.44. Stagger 3-5 f between elements. 🎬 · ✔ 2026-11-05
- **B3.12** Timing: entrances 16-22 f with a long ease-out, exits 10-14 f; the exit ends on the slot's last frame. Full timing rules: C2 and C14. ✅ (2026-10-03, 2026-10-15) 🎬 · ✔ 2026-11-05
- **B3.13** For a device he has built before, copy his own entrance values from his comp (e.g. his $7M bands: 25 f, Angle −270, 0.094, 5 f stagger) over any spec. ⚙️ (2026-10-08) · ✔ 2026-11-05

### NeoTextMotion: main text
- **B3.14** Main text is NeoTextMotion (the NeoMotionText fuse in the node list), word by word, each word rising from below: PosDir 0 = Up. PosDir 3 (Left) is the script default and is wrong. Split word pieces need a real space. ✅ 🔁 (2026-10-25, 84 comps failed) *"I use a lot of NeoTextMotion for Typography."* · ✔ 2026-11-05
- **B3.15** House values: preset 26, word scope, InLength 18-25 f, Delay 0.28 s (Delay is the word stagger), PosDistance 0.0464, Out off; built-in shadow 0.496 / 0.004 / 3.31. Font: client overlay. 🎬 · ✔ 2026-11-05
- **B3.16** Text keeps its built-in shine: two shines at 0.19 and 0.38, intensity ~0.335, width 0.0141. Turn it off (StShineEnable 0) on accent-coloured words: it turns them white. ✅ 🔁×2 *"my text always have shines in neotext motion so add that"* (2026-10-25; accent fix 2026-10-29) · ✔ 2026-11-05
- **B3.17** Two-tone through the Char1 range and Char1Color (accent: client overlay). Set Char1Enable 1 for an accent and 0 explicitly for none (a clone colours its last letter); set Char1ColorR explicitly. Check every range against its string by script before install. ⚙️ · ✔ 2026-11-05

### Number Counter
- **B3.18** Main numbers count up with his Number Counter (Text+ named "Count"), landing on the word; digits sit in fixed slots so the number doesn't wobble (`lib\J7.py`). When to count: C4, C10. ✅ (2026-10-25) · ✔ 2026-11-05

### MagicZoom V3: every zoom
- **B3.19** Every zoom and punch-in is MagicZoom V3 (MrAlexTech, Edit-page effect) on an adjustment clip, never a Fusion comp. ✅ 🔁×2 *"I prefer MagicZoom V3 instead of Dynamic Zoom"* (before 2026-10); *"Zoom and hold with magic zoom like we did in other videos"* (2026-10-14) · ✔ 2026-11-05
- **B3.20** His values (170 instances): zoom = 1 + depth × ramp; pivot on his face (~0.51, 0.68). On the A-roll, Standard with a Linear curve; Zoom & Hold (0.071, 0.111 punches) only on emphasis statements (B2.13, 2026-11-05); an occasional zoom-out 0.053 on a return to camera, 0.026-0.03 slow push on media and card clips. Depth and pacing: B5. 🎬 (reworded 2026-11-05 to follow B2.13; still for his review in B3) · ✔ 2026-11-05
- **B3.21** MagicZoom motion blur off (Transform1 MotionBlur 0), even though his older finals had it on. ✅ (2026-10-28) · ✔ 2026-11-05
- **B3.22** Where a zoom would snap back on plain A-roll, ease it back smoothly (mirror mode). ✅ *"this doesn't smoothly"* (2026-10-24) · ✔ 2026-11-05
- **B3.23** The punch-in pass runs over the whole video, intro included, once the visuals are final (`mz_plan.py`, `mz_inject.py`, `mzblob.py`). No MagicZoom under a full-frame visual; one per cut. ⚙️ (2026-10-09, 2026-10-16) · ✔ 2026-11-05

### Grounds
- **B3.24** Every full-frame motion graphic sits on his ground macro at the start of the main line: BGORANGE, or the client copy (client overlay). Open the macro and copy it; never rebuild it by eye. ✅ 🔁×13 *"When doing motion graphics, always use the BGORANGE macro I have saved"* (2026-09-27, 2026-09-30) · ✔ 2026-11-05
- **B3.25** BGORANGE: Background #110602; ResolveFX Grid 20×12 at Blend 0.0143; #FF5A1F glow through two Ellipse masks (W 1.034, SoftEdge 0.1) at y −0.299 and 1.254, so light comes from the top and bottom edges; Gaussian H 1.0 / V 0.4; merged at 0.181; no vignette. 🎬 · ✔ 2026-11-05
- **B3.26** A client ground is the same file with the same node names, new colours only, saved as a new file beside his (`frkit.bgfrontal_setting()`). ✅ *"install BGFRONTAL into My macros"* (2026-10-20) · ✔ 2026-11-05
- **B3.27** Set the ground's Background and blur tools to float16 to stop banding. ⚙️ · ✔ 2026-11-05

### Box chain and finishing nodes
- **B3.28** Box chain, in order: RectangleMask → fill Background → GaussianBlur 0.4 → border (Instance mask, BorderWidth ~0.0018, accent fill) → NeoLightSweep Pro → DropShadow → NeoAnim. Corner shape and colours: client overlay. 🎬 · ✔ 2026-11-05
- **B3.29** NeoLightSweep Pro is a static sheen at the box centre, on every box, never animated: width 0.07-0.11 on pills, up to 0.2 on cards; Angle −40, SoftEdge 0.055, Distance 0.0015; Intensity 0.18-0.40 (0.25 on accent fills, 0.3 on light fills; the 0.724 default washes out). Aim its inner Rectangle1 Center at the box. When: C7. ✅ *"I just add it in the box to make the box have a shiny look at the center"* (2026-09-26) · ✔ 2026-11-05
- **B3.30** NeoGlow: Gain 0.15, MasterBlur 1.5, Depth 4 (quality 3), Screen; on borders and rings only. ✅ 🔁×3 *"always use Neo glow next time I ask for Glow"* (2026-09-26) · ✔ 2026-11-05
- **B3.31** DropShadow (ResolveFX; image input is `Source`): pills strength 0.5-0.55, distance 0.008, blur 0.3; cards 0.6 / 0.012 / 0.45; big cards up to 0.62 / 0.014 / 0.5; angle 37.5. 🎬 · ✔ 2026-11-05

### His other macros
- **B3.32** Opacity: every fade and every dim goes through his Opacity macro (BrightnessContrast "Op", Gain). Inactive elements: Gain 0.42-0.62, Saturation 0-0.64, over 6-8 f. ✅ *"I have an opacity macro node I use instead"* (2026-09-26) · ✔ 2026-11-05
- **B3.33** Change a box's colour or logo with Switch nodes on the existing box. ✅ *"there are nodes called switch for that reason, correct all through the video"* (2026-10-25) · ✔ 2026-11-05
- **B3.34** Arrows: his Arrowline macro (write-on 0→1 over ~11 f, head scales in over 3 f); a straight Arrowline when he asks for straight. A card leads to its items with an Arrowline, not a dashed line. ✅ (2026-09-27, 2026-10-02) · ✔ 2026-11-05
- **B3.35** Connector lines: his Moving dashed line (dotted line) macro, curved, two points, animated with WriteOnEnd. ✅ *"I used curved dashed lines with just two points instead of 4"* (2026-09-26) · ✔ 2026-11-05
- **B3.36** Glass: his Glass effect macro (blur 0.4 below, Displace refraction −2.62, LightAngle 132.6, panel width opens on a key). "Glass background as I did" = Glass effect on the footage with a MagicMask cut-out of Alex in front (Apollo, OUR OWN PROCESS 685-754). ✅ (2026-10-03) 🎬 · ✔ 2026-11-05
- **B3.37** Down fade, for text over Alex: black at α 0.62-0.65 through a soft rect (W 1.073, H 0.619, centre y −0.119), in 8 f, out 7 f. End colour matches the ground. 🎬 💡 · ✔ 2026-11-05
- **B3.38** Neo Highlighter Pro: one stroke per line, multiply, Displace 0.01 edge, DropShadow 0.1 / 0.02 / 0.4; colour: client overlay. On a clear canvas set ApplyMode Normal, or it draws a black bar. When: C6. 🎬 · ✔ 2026-11-05
- **B3.39** MosaicBlur at PixelFrequency 200 (slider max) on the hidden content's own layer. Soft blur is Gaussian Blur. When: C7. ✅ 🔁×4 *"always increase the pixel freequency to the highest, thats how I like it"* (2026-10-15) · ✔ 2026-11-05
- **B3.40** Tile grids: his Duplicate fuse (Copies, TimeOffset), not hundreds of nodes. Outlines: PizzaBlu Outline right after the text or image, before its Transform. 🎬 · ✔ 2026-11-05
- **B3.41** Picture-in-picture: SSC PiP Pro on the Edit page, circular inset bottom-right, soft light ring, drop shadow, clip mirrored so he faces into the frame. 🎬 (2026-09-14) · ✔ 2026-11-05

### Keep comps light
- **B3.42** Comps play back smoothly on his PC at full quality: NeoBevel off, no motion blur, Switch instead of stacked copies, Duplicate for grids. Send back any comp over 1.5 MB. ✅ 🔁×2 *"it should still be very high quality visual"* (2026-10-24) · ✔ 2026-11-05
- **B3.43** NeoBevel stays off in every comp (PassThrough), turned off by script without regenerating comps. ✅ *"just disable all the neo bevel nodes in all the visuals and comps"* (2026-10-23) · ✔ 2026-11-05

### Scripting them
- **B3.44** Macro paste, inner-tool names, NeoAnim stage switches, Out quirks and Edit-page effects being invisible to the API: open [[03-Areas/video-editing/sops/fusion-build|Fusion build SOP]] and [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] before scripting any of these. ⚙️ · ✔ 2026-11-05
- **B3.54** Macros stay macros. NeoAnim, Opacity, NeoLightSweep (Pro) and NeoGlow go into a comp as the one macro node, never exploded into their inner tools (NAPosition, NABlur, ...). Lay the comp out his way (B4: one row per element, a collector column, the source along the bottom). His fix of P05-01 shows it (NeoAnim_1, Opacity_Out, NeoLightSweepPro_Sheen as macros). ✅ *"Your node structure arrangement is not how I taught you from the beginning when we did our first study of my nodes"* (2026-11-06)

## Never (strict)
- **B3.45** Never Dynamic Zoom (off on every clip). ✅ (before 2026-10) · ✔ 2026-11-05
- **B3.46** Never stock Glow, a blurred copy or a soft coloured box as a glow; never a dark offset "shadow box". ✅ *"it was creating a shadow box. It was creating things that made it look bad"* (2026-09-25) · ✔ 2026-11-05
- **B3.47** Never key opacity on a Merge Blend. ✅ *"I don't want you to ever do any opacity animation on the merge"* (2026-09-26) · ✔ 2026-11-05
- **B3.48** Never a Transform pop, overshoot or bounce. ✅ *"never use boucing animations"* (2026-10-03) · ✔ 2026-11-05
- **B3.49** Never animate a box over a box. ✅ *"Never every animate a box over a box"* (2026-10-25) · ✔ 2026-11-05
- **B3.50** Never the normal Blur node. ✅ *"always use gausian blur and not normal blur"* (2026-10-15) · ✔ 2026-11-05
- **B3.51** Never edit, rename or overwrite his macros. ✅ (2026-10-20) · ✔ 2026-11-05
- **B3.52** Never leave a MagicMask untracked: it returns the whole A-roll and hides everything under it. Samuel tracks MagicMask himself. ✅ *"I would do the magic mask myself"* (2026-10-14) · ✔ 2026-11-05
- **B3.53** No visual so heavy it lags his PC. ✅ *"this visual is too intensive on the computer"* (2026-10-24) · ✔ 2026-11-05

## Pictures
- ![[_attachments/rulebook/b3-apollo-final-macros.jpg|360]] ✅ his Apollo final: BGORANGE ground, NeoAnim cards, NeoLightSweep sheen, NeoGlow borders (Apollo, approved final)

## Questions for Samuel
- **Q-B3.a** Several of your macros never showed up in your finals: Screen Focus Emphasis (18 uses in $7M, no rule yet), `shine`, Shine box with text, Text_Infinite_Scroller, Rectangle_V3, Boxed text, the PJT text pack. → Options: (1) all allowed, use where they fit (2) tell us what Screen Focus Emphasis and `shine` are for and which to leave alone. My pick: (2). Is `shine` the moving shine in C7? → Samuel: (1), all allowed, use them where they fit (2026-11-05).

## Sources
Draws on and replaces the node parts of [[03-Areas/video-editing/fusion-node-system|Fusion node system]], [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]], [[03-Areas/video-editing/ways-of-working|Ways of working]], [[03-Areas/video-editing/samuel-review-card|Samuel's review card]], [[03-Areas/video-editing/routerise-house-style|Route Rise house style]]; how-tos stay in [[03-Areas/video-editing/sops/fusion-build|Fusion build SOP]] and [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]].

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
