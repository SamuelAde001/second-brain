---
type: knowledge
area: video-editing
status: active
updated: 2026-09-27
source: manual
tags: [scripts, resolve, fusion, ui-demo]
---

# UI focus: zoom, darken, highlight on adjustment clips

First run: Route Rise #3, 2026-09-27, timeline *UI demos v2 (Editor)*. Rules: [[03-Areas/video-editing/ways-of-working|ways of working]] → "UI demos and screen recordings".

- `data.py`: the Tella file and the V4 clip map (timeline frame ↔ Tella second). Rewrite it per job.
- `quad.py out.jpg f1 f2…` / `tq.py out.jpg t1 t2…`: frames (timeline frame or Tella second), framed like the timeline, with a 5%/10% grid for measuring focus boxes in frame fractions (u, v, v down).
- `track.py f0 f1 u0 u1 v0 v1 out.json`: vertical scroll tracker (row-profile match), so a focus box stays on content while the page scrolls (`gen.Scroll`).
- `spec.py` / `spec2.py`: the focus states per stretch. `(frame, ease, zoom, focus point, box)`: the zoom target and highlighted box, keyed on the spoken word.
- `gen.py`: turns states into per-frame keys (zoom clamped so the frame never shows past the image edge, a slight bias away from the camera PIP bottom right).
- `build3.py` + `datacomp.py`: writes the keys into a Note inside a small `.comp`, because the Resolve sandbox can't read files. The comp is imported onto a scratch clip (`ImportFusionComp` fails on adjustment clips), the Note text is read back, and the nodes are built by API in the adjustment clip's comp: MediaIn → Merge_Dim (black Background masked by an inverted Rectangle_Focus) → Transform_Zoom → MediaOut.
- `snap.ps1`: grab the Edit-page viewer to check a frame.

Gotchas: connect `MediaOut1` **after** `comp.Unlock()`, or the Edit page keeps rendering the old comp. Adjustment clips go on the patched destination track (move the patch in the GUI), with every other track locked while `InsertGeneratorIntoTimeline` runs.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
