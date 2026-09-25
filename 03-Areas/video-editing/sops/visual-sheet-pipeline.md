---
type: sop
area: video-editing
status: active
updated: 2026-09-25
source: manual
tags: [sop, visuals, cut-sheet, storyboard, resolve]
---

# Visual sheet pipeline: a rendered visual for every sentence

How the Editor turns a finished cut into a visual per sentence, rendered as videos and placed on a duplicate timeline for Samuel to judge in context. First run: Route Rise #3, 2026-09-25 (59 visuals, [[04-Projects/routerise-4-ai-tools|project note]]). This is steps 4–5 of [[07-Agents/video-editor/profile|the Editor's pipeline]] (ideate per sentence, preview). Step 6 (approved visuals rebuilt as Fusion comps) comes after Samuel's review. The engine lives in `03-Areas/video-editing/scripts/visual-engine/`: copy it into the job's `Graphics\Visuals vN\` folder.

Read first: [[03-Areas/video-editing/visual-vocabulary|visual vocabulary]] (his look, list styles, the TSB critique, the agency guide) and [[ways-of-working]] (effects are real nodes; the intro is his).

## 1. Study before designing
- If the style is in question, contact-sheet the reference finals (ffmpeg `fps=1,scale=384:216,drawtext,tile=6x5`) and read them. Don't re-read what [[03-Areas/video-editing/visual-vocabulary|visual vocabulary]] already records.
- Contact-sheet the client's screen recording (`fps=1/4`, crop the screen side) to know what real UI exists. Pull full-res frames of the UI you'll rebuild into `_assets/tella/`.
- YouTube reference videos: play them in Samuel's Chrome (the in-app browser gets ads; embeds fail with error 153). Build contact sheets in the page (seek the `<video>`, `drawImage` into a canvas grid, screenshot). Save stills: draw frames to a canvas, pack them into one HTML file, download it once (one download, no multi-download prompt), and split it into JPGs with Python.

## 2. Timings
- Duplicate the working cut (`DuplicateTimeline`; it can time out at 10 s but still finishes; check by name). Run `CreateSubtitlesFromAudio()` on the duplicate (also times out, finishes about 20 s later). Read cues with `GetItemListInTrack("subtitle",1)`: `GetStart()` minus the timeline start, and `GetName()`. Disable the subtitle track afterwards.
- Map which stretches are screen recording from the enabled/disabled runs on the Tella track.
- `beats.py`: one beat per main sentence (join very short ones), kind `intro` (ideas only, never placed) / `visual` / `aroll` / `screen`, frames from the cues. Each visual has picture, on-screen text, depth → nodes, ground, motion, SFX.
- **Close gaps:** a visual runs up to the next beat, or the next screen stretch, when it starts within 8 frames. Otherwise two full-frame visuals flash the A-roll for 1–3 frames between them.

## 3. Build scenes
- One `scenes/src/<scene>.js` per beat. `scenes/build.py` wraps each in HTML with kit.css, kit.js, lib.js, tracker.js and parts.js.
- Time words with `T(frame)` (timeline frame → scene seconds), so a reveal lands on its word.
- Every effect must map to a Fusion node: `.bevel` NeoBevel, `sweep()` NeoLightSweep Pro, `.glow-*` NeoGlow, `.shadow` DropShadow, `.reflect` NeoReflection, 3D via CSS perspective (Transform3D/ImagePlane3D). No fake shadow boxes.
- Vary the grounds and box fills: warm dark with radial glow, light, cream, navy-violet, red wash, blurred real screenshot, blurred A-roll.
- A-roll inside a graphic: map the beat's frames through V1 (`GetLeftOffset(True)` is in timeline frames; source seconds = (leftOffset + frame − clip start) / 23.976) into `_assets/aroll/map.json`, then `aroll.py <beat>`. The scene uses `arollImg()`.
- **Never declare top-level `const R`, `T`, `A`, `F` or `W` in a scene.** They shadow the engine's globals and the render comes out empty.
- Invented example data only where nothing real exists, and never invented stats. Real numbers only from the footage.

## 4. Render and check
- `python render.py B07 --still` (a frame at 80%), `python check.py out.jpg B07 B08 …` (tiles stills; overlays composited on an A-roll frame). Look, fix, then `python render.py <ids>` (3 tabs in parallel, about 6 fps per tab).
- Overlays → ProRes 4444 with alpha (Resolve reads the alpha as Straight). Full frame → H.264 CRF 12.
- Verify every render's frame count against its beat with ffprobe `-count_frames`.

## 5. Place
- Bin `Fusion Comps and Adjustments / Claude visuals vN (Editor)`, new video track named `Claude visuals vN`, clip colour Apricot.
- `AppendToTimeline` with `recordFrame = timeline start + beat start`. **`endFrame` is exclusive: pass the full frame count.**
- A file re-rendered with a new length keeps its old duration in the media pool. Delete the media pool item, re-import, re-append.
- Check afterwards: every V7 clip's start/duration against beats.py, and the other tracks' item counts unchanged. Save the project.

## 6. Hand over
- `gen_sheet.py` builds the sheet (every beat, a thumbnail at 85%, the nodes behind each effect, the intro ideas, open items). Publish it as a private artifact and copy it to the job's `Docs`.
- Thumbnails of overlay `.mov`s: `select=eq(n\,N),setpts=PTS-STARTPTS` before `overlay`, or ffmpeg composites nothing.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
