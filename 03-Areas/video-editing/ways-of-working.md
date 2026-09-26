---
type: knowledge
area: video-editing
status: active
updated: 2026-09-26
source: memory-export
tags: [conventions, agents, fusion]
---

# Ways of working — the rules for anyone editing with Samuel

From the Claude memory export for the video-editing project, last updated 2026-09-19. **This is the single most important note for the Phase 4 video-editing agent.** It is not theory: most of these rules exist because something was done wrong once and corrected.

## Node naming — strict

- **Never rename Samuel's existing Fusion nodes.**
- Every new node's name must include its node type: `Transform_D01`, `Merge_Cell_D01`, `Background_D01`.
- **Never** use abbreviations or role-only names like `XF_`, `Cell_`, `Stack_`.

## Asset generation

- Samuel pastes `.setting` file content **directly into the Fusion node graph**. Claude generates those programmatically with Python.
- **Node layout coordinates must be included** — `ViewInfo = OperatorInfo { Pos = { x, y } }` — or the flow view comes out as a stacked blob.
- **Visuals are ALWAYS built as Fusion nodes so he can edit them later.** Never an animated PNG, PNG sequence or any other raster dropped into Fusion.

## Design constraints

- Brand colour `#00ACEA`.
- **All rectangles use RectangleMask nodes** — never polygon masks for rectangles.
- Circles use **EllipseMask + Instance Ellipse** (Solid off, border on), as in his verified SIGNALS comp. (Previously: RectangleMask with `CornerRadius = 1.0`.)
- Fusion colour values in **normalised 0–1 float**.
- **Don't apply a client's brand font or colours** to things built for him — e.g. B-roll pages — unless he explicitly asks.

## Visual direction requests — the standing format

> When Samuel asks for visual ideas, the deliverable is **always a full cut sheet as an HTML page** — never a chapter-level summary in chat.

Every main sentence of VO gets its own beat with a visual assigned. Beats are detailed: the specific picture, on-screen text strings, screenshots and screen references, and motion. **He corrected this once already** — a chapter-level summary was delivered instead. Do not repeat it. See [[cut-sheets]].

## Editorial process

Phase-gated. Phases are defined upfront — **intake → cut analysis → transcript → chapter markers** — and each phase is completed fully before the next begins.

## How he collaborates

- **Pragmatic.** He wants the simplest rig that achieves the result, complexity added only when a specific problem actually appears. **He pushes back on over-engineered solutions.**
- He communicates precisely about what is missing, and expects **proactive identification of production-logistics problems**.
- For a structurally ambiguous decision — grid maths with no clean division, say — **ask one targeted clarifying question before rebuilding.** Otherwise proceed on sensible assumptions and flag them.

## Fusion build conventions — his house method

**Box with outline:** RectangleMask → Background (dark fill), plus an **Instance** of that same RectangleMask with `Solid = 0` and `BorderWidth` ~`0.00184` → a second Background in the light border colour, merged over the fill. Both Backgrounds masked by their respective rectangle. Then a **NeoLightSweep Pro** macro over the result for the shine — *"this is what gives cards the modern feel."*

**Circle with outline:** the same pattern with Ellipse + Instance Ellipse (instance has Solid off, Border on).

**Lines:** a Polygon on a Background node. Nothing more.

**Colour rule:** the accent colour varies per video. The background fill is a **darker shade of the same accent**; the border is the **lighter** one. His worked example: border `1, 0.3529, 0.1216` (`#ff5a1f`) with fill `0.1059, 0.0353, 0.0118` — accent × ~0.10. Accent for the Cold Outreach / Frontal video is **`#ff5a1f`**.

**On-screen card text** is bold white ALL CAPS. Numbered list cards use a white circle with the accent numeral to the left of the bar, plus an icon circle inside the bar.

> From now on, any visual proposed or built should use these boxes and circles.

### Node tree layout — follow this

- **One horizontal merge spine, left → right on a single row.** Every Merge sits on that row.
- Each element's generator stack (Rectangle/Ellipse → Background, Text+, imported PNG) sits **directly above** the Merge where it enters the spine, feeding down into it.
- The effects chain runs **inline on the spine in order** — NeoBevel, NeoLightSweep, DropShadow, NeoAnim — never hung off to the side.
- Source footage (Adjustment Clip / MediaIn) enters at the **bottom right** and merges into the final Merge before `MediaOut1`, which sits far right.
- Third-party macros in use: **NeoLightSweep Pro, NeoBevel, NeoAnim, NeoTextMotion, MosaicBlur.**

## Effects are real nodes, never faked — Samuel, 2026-09-25

On *Taking a Step Back from Claude*, Claude built its own glows and "shadow boxes" instead of using the effect nodes, and Samuel had to correct it. His words: *"I have a plugin called Neo Glow, which is well what I use for glows. It didn't use that… instead of it to use shadows, the actual drop shadow node, it was creating a shadow box."* And: *"I always use actual nodes that can help me create those visuals so light sweep glow node actual drop shadow um reflection."*

- **Glow = NeoGlow.** Never a blurred copy or a soft coloured box standing in for a glow.
- **Shadow = the DropShadow node.** Never a dark offset rectangle behind a card.
- **Shine = NeoLightSweep Pro. Bevel = NeoBevel. Reflection = a real reflection** (the Renderer3D/Opacity/GaussianBlur rig in [[fusion-node-system]] §3, or a flipped, faded copy only where that is his method).
- An HTML preview may imitate these looks, but every effect in it must map one-to-one to the node that will make it in Fusion. The cut sheet names that node.
- **Not sure which node makes a look? Ask him.** Don't invent a workaround.

## Box builds — Samuel's corrections, 2026-09-26

From his review of the first Claude box on Route Rise #3 (he liked the design; these are how he builds it):

- **NeoLightSweep Pro is a static shine**, placed so the box looks shiny at its centre. It never animates. *"I don't use lightsweep to actually sweep shine, I just add it in the box to make the box have a shiny look at the center."*
- **A moving shine = a BrightnessContrast node masked by a slightly inclined RectangleMask**, swiped across the box as it finishes animating in, on top of the static light sweep.
- **Opacity animation uses his Opacity macro** (`My macros\Opacity.setting`, a BrightnessContrast called `Op` with a Gain control). *"I don't want you to ever do any opacity animation on the merge."* Never key Merge Blend.
- **No Underlay** on generated builds. Instead, **each box's node structure sits far from every other node group** (its own area of the flow).
- **Boxes are squares** when he says "box".
- **Dashed/dotted lines use his "Moving dashed line" setup** (`My macros\Moving dashed line.setting`): transparent Background → Paint with a PolylineStroke (CircleBrush 0.0111, Spacing driven by a Shake 1–2, Smoothness 25) along a polyline, masked by the same polyline as a PolylineMask border (0.0019, Solid off). Animate it on with the stroke's `WriteOnEnd`.
- **Hiding a reveal** (logo, name, anything to be revealed later): MosaicBlur (ResolveFX) on that content's own layer only.
- Keep only the text he asks for. No invented sub-lines ("BY ANTHROPIC" was cut).

### How he finished the four-box visual (Route Rise #3, Composition2) — study, 2026-09-26

Read from his final comp (parsed from a saved copy) and frames. Build this way next time:

- **Each family of elements merges onto its own transparent Background canvas**, then that canvas joins the main line. The four boxes chain onto one canvas (Merge7 → 8 → 9 → 10), the two pills onto another, his card onto a third. This makes it easy to see which is which, and each group can be moved or shined as one.
- **The background (grid/glow) stays separate from the content.** All the content (card + lines + boxes) goes through one Transform on a PolyPath (a slow move over frames 0–33), and only then merges onto the static background. It works like a camera move.
- **One shine across the whole row:** a single BrightnessContrast + inclined RectangleMask (width 0.022, height 0.81, angle −18) on the boxes' canvas, moved by a PolyPath across the full frame over frames 36–60. Not one shine per box.
- **NeoLightSweep Pro width is narrow, about 0.07** (the default 0.2 washes the box).
- **Connector lines have two points and are curved.** They all start from one point on the top of his card and fan out to each box. They're drawn on fast (about 6.5 frames). There are no right-angle paths.
- **Timing is quick:** each box moves in about 8 frames and the boxes are about 3.75 frames apart, so the whole row is in within about 20 frames.
- **The box drop shadows were removed**, since the box glow is enough. The drop shadow on his pills is small and tight (distance 0.008, blur 0.31).
- **Pills (chips):** RectangleMask (CornerRadius 0.34) → accent Background → GaussianBlur 0.4 → Merge masked by the fill, plus an Instance border in the lighter tint #FD9457, then NeoBevel → NeoLightSweep → DropShadow → **NeoAnim** (slide + blur in). The text is **NeoTextMotion** (Geist SemiBold). The title is NeoTextMotion Geist ExtraBold, with the number in the accent colour.
- **The layout tells the story of the segment:** title ("4 TOOLS") → the two questions the section answers → the four tools → Alex at the bottom, with every line coming out of him.

## The intro is Samuel's — 2026-09-25

*"Every intro is Samuel."* Visual ideas for the intro still go on the cut sheet, as inspiration for him. **Nothing is placed on the timeline before the intro ends.** Visuals start on the first sentence after it.

## Animation and tidiness

- **Always use splines to smooth keyframes.** Timing must feel smooth, never linear.
- Each segment of a node tree must be **well separated and spaced**, and **labelled with an Underlay**.

## The visual toolkit for finishing an edit — stated 2026-09-18

The kinds of visual he uses, and the rule attached to each:

| Visual | Rule |
|--------|------|
| Website screenshots | Placed where needed |
| Fusion animations | For statements that need visualising |
| YouTube B-roll | Claude can't download it — **leave a marker saying what to use** |
| Steady zoom-ins on A-roll | Via adjustment clips |
| HTML mockups | To demonstrate things on screen; screen-recorded in OBS. He records it himself if Claude can't |
| Text on screen | **Only on important statements** |
| AI B-roll | Generated in Flow — Claude supplies the prompt plus a marker |

- **Icons come from his Assets folder.** Placeholders only if that isn't possible.
- **Visuals written in cut guides are often unrealistic** — follow the style already used in the edited part of the video instead.
- **Duplicate the timeline before any agent starts editing it.**
- **Prioritise speed and credit efficiency:** reuse and copy-paste existing comps, adjustment clips and nodes rather than rebuilding.
- **Visualise with illustrations first — "show, not tell."** He expects dense, varied visuals matching the density of his own edit. *Reusing templates with swapped text was explicitly rejected as useless.*

## Time and delivery rules — confirmed 2026-09-22

From the Accountability Engine's `body.md` (2026-08-26 to 2026-09-02), checked one by one with Samuel on 2026-09-22. Only what he confirmed is here.

- **Edit in 55-minute chunks with 5-minute breaks.** His numbers — the engine's were 50 and 10.
- **Plan the day the night before.** Tomorrow is planned by 9:30pm ([[daily-routine]]).
- **Every client day has a MUST-CLOSE and a STRETCH.** MUST-CLOSE: the day fails if it does not close. STRETCH: tomorrow's first item, pulled forward if today runs ahead.
- **Route Rise's 5-day cap.** The clock starts the day he opens the project. **Route Rise counts Sunday inside the five days; Samuel does not work Sunday, so when a Sunday falls inside, he has 4 working days.**
- **Revisions become top priority.** *"Revisions happen and can't be controlled, but they become top priority."*
- **Ship day starts like any other day** — no early start. The engine's 5:00am ship-day start is dropped.

The engine's evidence behind these: the job is about 30 hours of work, and the day that closed Client #2 in about eight hours was the one built into timed chunks the night before ([[patterns|P5]]).

Related: [[fusion-node-system]] · [[fusion-recipes]] · [[routerise-house-style]] · [[cut-sheets]]. Back to [[03-Areas/video-editing/video-editing|Video editing]]
