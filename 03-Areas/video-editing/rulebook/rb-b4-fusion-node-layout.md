---
type: sop
area: video-editing
status: approved
approved: 2026-11-05
updated: 2026-11-05
source: interview
tags: [rulebook]
section: B4
---

# B4 · Fusion node layout

> **Read when:** building, generating or editing any Fusion comp or .setting file, and when reviewing a comp before it goes to Samuel. **Client values:** corner shape of boxes (client overlay). **Status:** approved by Samuel, 2026-11-05 (issues answered one by one, the rest approved in one go).

## Rules

### Why it matters
- **B4.1** The node tree is part of the deliverable. He fixes small things himself in Fusion, so a messy tree is a fault even when the picture is right. 🔁 ×7 (2026-09-26 to 2026-10-31) ✅ *"I prioritise node arrangement as it helps me navigate"* (2026-10-02); *"it helps me to make corrections without having to prompt you"* (2026-10-14) · ✔ 2026-11-05

### The B04 v2 layout (every comp)
- **B4.2** Main line along the bottom, left to right: background nodes at the start (BGORANGE / BGFRONTAL, or the adjustment clip's MediaIn) → one Merge per group (Merge_Card, Merge_Arrows, Merge_Pills …) → MediaOut1 at the far bottom right. ✅ *"Better node arrangement, ALWAYS KEEP THE NODES ORGANISED LIKE THIS"* (2026-10-02). Reference build: Apollo `Graphics\Visuals v3\build_B04.py`. · ✔ 2026-11-05
- **B4.3** Each group of similar nodes (rows, pills, arrows, logos, cards) is collected over its own clear canvas Background and joins the main line **once**. 🔁 ×2 ✅ *"Similar nodes on the same node line connected to a BG canvas"* (2026-09-26, 2026-10-02) · ✔ 2026-11-05
- **B4.4** Repeated elements: one row per element, evenly spaced, each a left-to-right chain ending in its placement Transform. Their collector Merges stand in one vertical column on the right, the clear canvas at the top; the bottom Merge feeds the main line. ✅ *"Next time arrange this kind of nodes like this"* (2026-10-01) · ✔ 2026-11-05
- **B4.5** A container (card, panel) gets its own line above the main line: canvas → fill → border → one Merge per sub-group → effects inline → animation Transform → down into its main-line Merge. Loose parts of a container sit on one line over their own clear canvas. ✅ (2026-10-02) · ✔ 2026-11-05
- **B4.6** Generators sit straight above the Merge they feed. ✅ · ✔ 2026-11-05
- **B4.7** Effects inline, in this order: NeoBevel (switched off, B2.24) → NeoLightSweep → shine (Brightness Contrast under an inclined RectangleMask) → DropShadow (a node, never a dark offset rectangle) → NeoAnim → collector. A Brightness Contrast that sits the graphic into the plate goes late, near the collector. 🎬 ✅ · ✔ 2026-11-05
- **B4.8** Separate families: the background (grid, glow) stays on its own and static; all content goes through one Transform for a camera-like move before merging onto the background. 🎬 (Route Rise #3 four-box, 2026-09-26) · ✔ 2026-11-05
- **B4.9** A speaker cut-out (MagicMask) sits at the very bottom by the output. The input feeds both MagicMask1 and the base Merge; the masked speaker merges back on top of the finished graphics, always last. 🎬 (7M) · ✔ 2026-11-05
- **B4.10** Every repeated card gets its own mask and its own canvas. ✅ *"I want every Mask and canvas to be stand alone"* (2026-08-14) · ✔ 2026-11-05
- **B4.11** The same icon repeated: one icon node feeding one Transform per copy. ✅ *"one person Icon connected to multiple transforms for each circle"* (2026-09-27) · ✔ 2026-11-05

### Adding to his comp
- **B4.12** New merges go on his main line in one straight row, between his last Merge and MediaOut1. Feed into his own nodes (e.g. his empty Merge7) rather than restructure his tree. After pasting, line the new group up with his anchor nodes. ✅ *"Nice arrangement, keep always doing this"* (2026-09-27) · ✔ 2026-11-05
- **B4.13** His node-tree screenshots (`node-graphs-SAMUEL/`, 14 images) beat anything rebuilt from comp coordinates. ✅ (2026-09-20) · ✔ 2026-11-05

### Spacing and tidiness
- **B4.14** Compact: groups separate, short straight links, no long diagonals, no two nodes on one spot, but close enough that he never scrolls or drags to find a group. ✅ *"still put them close together enough that I don't need to scroll too much"* (2026-10-14; replaces "far away from other nodes", 2026-09-26) · ✔ 2026-11-05
- **B4.15** No stray or dead nodes. Delete them, or gather them in one compact block beside the tree and tell him where. ✅ *"Please delete wrong nodes, or put them all inside one group, so I can easily delete it"* (2026-09-27) · ✔ 2026-11-05
- **B4.16** Generated .setting files carry node positions (`ViewInfo = OperatorInfo { Pos = { x, y } }`), or they paste as a stacked blob. ✅ · ✔ 2026-11-05

### Naming
- **B4.17** Every new node's name starts with its type, then its role: `Type_Role_D##` (e.g. `Background_LeadCard_Fill_D01`, `Merge_Cell_D01`, `Transform_D01`). 🔁 ×3 ✅ · ✔ 2026-11-05
- **B4.18** Names are unique and there are no link loops: a duplicate name makes a self-link that hangs Resolve. ⚙️ (2026-10-02) · ✔ 2026-11-05

### Node craft
- **B4.19** Position, scale and rotation go on a Transform (Loader → Transform → Merge) or the element's own Center. Every Merge keeps Center 0.5/0.5, Size 1, Angle 0. When the foreground is smaller than the frame, offset = 0.5 + dx_px / fg_width_px. ✅ *"NEVER EVER Reposition anything with a Merge node."* (2026-09-27) · ✔ 2026-11-05
- **B4.20** Centre and space elements at their source inputs, never with NeoAnim. ✅ *"don't use the neo anim to bring them down to the center, centralise them and space them well"* (2026-09-27) · ✔ 2026-11-05
- **B4.21** Keyframes use splines, never linear. One exception: the constant slow push over a whole motion graphic (Size 1.000 → 1.036) is linear, so it never slows to a stop mid-shot (Q-B4.a, 2026-11-05). ✅ · ✏ 2026-11-05
- **B4.22** Rectangles are RectangleMask; circles are EllipseMask + an Instance (Solid off, border on); lines are a Polygon on a Background. Box with outline: RectangleMask → dark Background, plus an Instance of the mask (Solid 0, BorderWidth ~0.00184) → light-border Background merged over, then NeoLightSweep Pro. Corner shape: client overlay. ✅ *"this is what gives cards the modern feel."* · ✔ 2026-11-05
- **B4.23** Fusion colours are normalised 0-1 floats. ✅ · ✔ 2026-11-05

### Check before it goes to him
- **B4.24** Check the layout of every comp before handover: list each top-level tool's position, flag any link longer than ~4 grid units (skip macro insides), move MediaOut1 beside the last Merge and connect it last, clear the selection, then look at the node view. 🔁 ×2 ✅ *"you have completly abandoned the way I told you to arrange fusion nodes"* (2026-10-28, 2026-10-31). How: [[03-Areas/video-editing/sops/fusion-build|Fusion build SOP]] §3-5. · ✔ 2026-11-05
- **B4.25** Check the picture in the viewer too. ✅ *"always check your work with the view"* (2026-09-27) · ✔ 2026-11-05
- **B4.26** Don't keep switching to the Fusion page on his screen; say what you are doing as you go. ✅ *"why do you keep going to the fusion page?"* (2026-09-27) · ✔ 2026-11-05

## Never (strict)
- **B4.27** Never wire every element straight into the main line. 🔁 ✅ *"you are connecting them all to the main line"* (2026-10-02) · ✔ 2026-11-05
- **B4.28** Never reposition with a Merge. ✅ (2026-09-27) · ✔ 2026-11-05
- **B4.29** Never rename his existing nodes; never role-only or abbreviated names (XF_, Cell_, Stack_). 🔁 ✅ · ✔ 2026-11-05
- **B4.30** Never share one mask or canvas across a batch (long fan-out links). ✅ (2026-08-14) · ✔ 2026-11-05
- **B4.31** Never add Underlays to generated builds. ✅ *"No need to add an underlay"* (2026-09-26; replaces Underlay labels) · ✔ 2026-11-05
- **B4.32** Never group leftovers by script (a 139-tool Group hung Resolve); park them with `SetPos`. ⚙️ (2026-09-27) · ✔ 2026-11-05

## Pictures
- (no picture yet: the Apollo B04 v2 node view he approved on 2026-10-02, and one of his `node-graphs-SAMUEL` screenshots)

## Questions for Samuel
- **Q-B4.a** Splines vs linear. Your rule: always splines, never linear (before 2026-09-19). Our video 4 bible: the slow push over a whole motion graphic is linear, Size 1.000 → 1.036 (2026-10-28). → Options: (1) splines everywhere, the push eases in and out (2) linear allowed only for that constant push. My pick: (2), a constant drift should not slow to a stop mid-beat. → Samuel: (2), linear only for that constant push (2026-11-05). B4.21 updated.

## Sources
Replaces the node rules in [[03-Areas/video-editing/ways-of-working|Ways of working]] (Node naming, Node tree layout, Never position with a Merge, Animation and tidiness), and draws on [[03-Areas/video-editing/fusion-node-system|Fusion node system]] §3, [[03-Areas/video-editing/fusion-recipes|Fusion recipes]], [[03-Areas/video-editing/sops/fusion-build|Fusion build SOP]], [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] (open for paste and SetPos details).

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
