---
type: knowledge
area: video-editing
status: active
updated: 2026-09-20
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

Related: [[fusion-node-system]] · [[fusion-recipes]] · [[routerise-house-style]] · [[cut-sheets]]. Back to [[03-Areas/video-editing/video-editing|Video editing]]
