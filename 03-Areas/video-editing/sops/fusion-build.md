---
type: sop
area: video-editing
status: active
updated: 2026-10-02
source: manual
tags: [fusion, resolve, scripting, any-ai]
---

# Building a Fusion graphic by script (any AI)

How any AI acting as the Editor builds a card, pill, box or any motion graphic in one of Samuel's Fusion comps, and checks it before telling him it's done. Written 2026-10-02 after Samuel tested Gemini on *"design and build a Card animated in for me there using the standard design I have"*. Gemini's comp rendered as plain "TEST CARD" text on a flat orange frame. The same request built this way came out right first time, apart from one padding fix: [[07-Agents/video-editor/log|Editor log]] 2026-10-02 21:05.

Part of [[03-Areas/video-editing/video-editing|Video editing]].

## What went wrong in the failed test, so it isn't repeated

| Mistake | Rule |
|---|---|
| Read only the profile, ways of working and the lessons note. Skipped the Editor memory and the node-system note, so "my standard design" meant nothing to it | Step 1 below: read all five, every time |
| Built node by node with `AddTool` + `SetInput` over 15 `run_script` calls | Generate a `.setting` from a Python builder on the kit and paste it in one call (step 3) |
| Fill and border Backgrounds left at `TopLeftAlpha = 0`, so the card was invisible | Only a clear **canvas** has alpha 0. Every fill, border and ground is alpha 1 |
| Wired the ResolveFX DropShadow's `Input`, which doesn't exist, so nothing came out of it | The DropShadow's image input is **`Source`**. Macros take `MainInput1` and give `MainOutput1` |
| No BGORANGE, no Neo Glow, no Light Sweep, no Neo Anim, no animation at all | Step 2's checklist |
| Couldn't screenshot, so asked Samuel to look | Step 5: Resolve writes the frame itself. Never hand the visual check to Samuel |
| Claimed "Session 0 isolation" | Wrong. Resolve, ResolveMCP and Antigravity all run in Samuel's desktop session (checked 2026-10-02). Report what was observed, not a guessed cause |

## 1. Read first, in this order

1. [[07-Agents/video-editor/memory|Editor memory]], all of it. The entries from 2026-09-30 on hold his taste: why "mediocre" means one design repeated, the gallery-as-vocabulary rule, node arrangement as navigation.
2. [[03-Areas/video-editing/ways-of-working|Ways of working]]: the Fusion section and **Node tree layout** (the B04 v2 standard, *"ALWAYS KEEP THE NODES ORGANISED LIKE THIS"*).
3. [[03-Areas/video-editing/fusion-node-system|Fusion node system]] §3, §4 and §8: his layout, the build recipes, the colours.
4. [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]]: the paste route, macro renaming, the hangs and how to avoid them.
5. [[03-Areas/video-editing/motion-gallery/motion-gallery|Motion gallery]]: the parts to build from (medallion, status tag, border beam, fill bar…). Inspiration, never a template.

## 2. His standard look, as a checklist

- **Ground:** his `BGORANGE` macro (`My macros\BGORANGE.setting`), or the A-roll. Never a flat colour, never a tool's brand colour.
- **Card (box with outline):** a RectangleMask → dark fill Background (a gradient `#2B0E06` → `#130602` reads better than flat `#1B0903`), plus an **Instance** of the same mask with `Solid = 0`, `BorderWidth ≈ 0.00184` → orange Background (`#FF5A1F` = 1, 0.3529, 0.1216), merged over the fill. Glow on the border = **Neo Glow**, never the stock Glow.
- **Effects inline, in this order:** Neo Bevel (optional) → **NeoLightSweep** → shine (BrightnessContrast under an inclined RectangleMask) → **DropShadow** (a node, never a dark offset rectangle) → **Neo Anim**.
- **Type:** Geist. Titles and chips ALL CAPS, Bold/ExtraBold. Two-tone headline: a white line plus an orange line.
- **Logo + name** = the P01 medallion: a white disc, an orange ring with Neo Glow, the real logo inside, clipped to the circle.
- **Placement:** elements built at their final place in the frame. Neo Anim stays at Global Center 0.5/0.5 and only animates.
- **Animation:** "animated in" means the container comes in first (Neo Anim, about 16 frames), then its parts in sequence (a pop for a medallion, a rise-and-fade per text line about 3 frames apart), then one shine once it has landed. When he asks for something static, add no motion at all (2026-10-01).
- **Padding:** equal on all sides. Size the card to its content (measure the widest line), not the other way round.

## 3. Build it with a generator, never node by node

- **Kit:** `Routerise\3. I Tried 100+ AI Tools…\Graphics\Visuals v2\pk.py` + `pillkit.py`. `bgorange()`, `background()`, `loader()`, `macro()` (a fresh Neo macro with renamed inner tools), `copy_his()` (his own NeoAnim / Light Sweep / NeoTextMotion, renamed), `spline()`, `ease()`, `xypath()`, `arrow()` (his Arrowline), `pill()`.
- **Starting templates (copy one, then change it):**
  - One card: [[03-Areas/video-editing/scripts/fusion-box/gen_test_card.py|gen_test_card.py]] (Brain). BGORANGE, card, medallion, eyebrow, two-tone headline, sweep, shine, shadow, Neo Anim, the full layout. Change `LINES`, the geometry and the timing.
  - A card with rows, pills and arrows: the Apollo job's `Graphics\Visuals v3\build_B04.py`.
  - A row of logo pills: the Apollo job's `Graphics\Visuals v3\build_I1_medallions.py`.
- **Layout comes from the generator, not from tidying afterwards:** a main line at the bottom (BGORANGE → one Merge per group → MediaOut1). A container gets its own line above it (canvas → fill → border → one Merge per sub-group → effects → animation). Repeated elements go one row each, into a collector column over their own clear canvas, and join their line **once**. Generators sit straight above their Merge.
- **Name every node `Type_Role`** (`Background_CardFill`, `Merge_TextRow0`). Never rename his nodes.
- **The generator must assert before writing:** unique names (a duplicate name makes a self-link that hangs Resolve), no link loops, no two nodes on the same position. `gen_test_card.py` has the checks.

## 4. Load it into his comp

1. Don't overwrite his work. Add a new comp version on the clip (`item.AddFusionComp()`), so the old one stays for comparison, unless he asked for nodes inside an existing comp.
2. `item.LoadFusionCompByName("Composition N")`. `resolve.Fusion().CurrentComp` only follows after a page round trip (Edit → Fusion). **Tell Samuel before switching pages.** Check that `CurrentComp`'s tool list is the new empty one (just `MediaOut1`).
3. Clipboard paste: `Set-Clipboard -Value ([IO.File]::ReadAllText(path))` in PowerShell, then `comp.Paste()` in `run_script`. One call, no `comp.Lock()`.
4. Wire what a paste drops: every link into and out of a macro (`ConnectInput("MainInput1", tool)`, `ConnectInput("Foreground", macro)`). The generator writes this list (`*_wiring.json`).
5. Re-set every pasted Loader's `Clip` (`SetInput("Clip","")`, then the path again), or it renders empty.
6. Move `MediaOut1` beside the last Merge (`FlowView.SetPos`), connect it **last**, then `FlowView.Select()` to clear the selection. Selected nodes draw their on-screen controls over the viewer.
7. Save the project (`ProjectManager.SaveProject()`).

## 5. Check it yourself before saying it's done

Look at real frames from Resolve: **the container landing, each part arriving, the finished hold, the shine**. For a 120-frame card that's about frames 3, 8, 12, 17, 24, 42 and 100. Contact-sheet them with ffmpeg and look.

- **Route A, no page switch (proven from Claude Code):** set `comp.CurrentTime = n`, then capture his Fusion viewer with `scripts/fusion_view.ps1 -Crop x,y,w,h` (window fractions). From Claude Code it runs inside `run_script_unsafe` as a `subprocess` call, one call for all frames. It uses PrintWindow, so it needs a process on his desktop: from Antigravity's terminal both it and `CopyFromScreen` failed ("The handle is invalid"). Try it through Resolve's `run_script_unsafe`. If it fails there too, use route B.
- **Route B, works from any AI (proven 2026-10-02):** Resolve writes the frame itself. Tell Samuel first, then `resolve.OpenPage("color")`, set the timeline playhead (`tl.SetCurrentTimecode`, at 24 fps for 23.976), `project.ExportCurrentFrameAsStill(r"<scratch>\f060.png")` → True, and `OpenPage("fusion")` again at the end. It shows the clip's **active** comp version.
- **What to check on the frames:** everything visible (alpha), nothing touching an edge, even padding, text inside the card, the order of arrival, the end state matching the request.
- **Check the nodes too:** list each top-level tool's `GetPosTable` position and flag any link between two of them longer than about 4 grid units. Skip macro inner tools: they show in `GetToolList` but not in the flow. A long link usually means `MediaOut1` was left where the comp put it.
- Fix what the frames show, re-check, and only then report. Send Samuel the contact sheet with the report.

## 6. Log it

One entry in [[07-Agents/video-editor/log|the Editor log]]: which comp and version, what was built, the builder's path, the frames checked, what was fixed. Commit and push.
