---
type: knowledge
area: video-editing
status: active
updated: 2026-10-08
source: local-folder
tags: [grammar, style, samuel, constructs, index]
---

# Edit grammar: how Samuel shows a talking-head video

What the Editor learned by studying Samuel's three finished Route Rise timelines on 2026-10-07: every visual on the timeline, the words under it, his comps and their exact settings. Built for the AI B2B Marketing job ([[04-Projects/routerise-ai-b2b-marketing|job note]]), reusable on every job. Back to [[03-Areas/video-editing/video-editing|Video editing]].

**Use this instead of re-studying his videos.** Samuel, 2026-10-08: *"Hope all the things you learned in the study sessions would all be used to help in the new session without it learning again from the old videos"*. Start every visual plan here. Open one of his comps or a still of his finals only when building that exact construct, to copy its nodes and settings. Re-study only when he finishes a new video (then add it here).

## The notes

| Note | What's in it |
|---|---|
| [[03-Areas/video-editing/edit-grammar/edit-grammar-apollo\|Apollo]] | Visual types with counts and durations, which spoken line gets which visual, rhythm, the construct library (template comp → settings), signature moves |
| [[03-Areas/video-editing/edit-grammar/edit-grammar-ai4\|4 AI Tools]] | The same for "I Tried 100+ AI Tools" (Cut v6), plus what could not be read |
| [[03-Areas/video-editing/edit-grammar/edit-grammar-tsb\|Taking a Step Back]] | The same for TSB, plus shared constants and what he never does |
| [[03-Areas/video-editing/edit-grammar/edit-grammar-shared-rules\|Shared rules in numbers]] | S0.1–S0.6 (entrance, UI spotlight and zoom, premium chain, two-tone titles, captions, BGORANGE) and the K1–K20 constructs, each copied from one of his comps |

Also: [[03-Areas/video-editing/routerise-house-style|House style]] §11b (pacing measured on his finals: a visual for about three quarters of the talk, a new element every 4–6 s, 2–6 s A-roll breaths, every visual ends on the next visual or a cut, no slivers), [[03-Areas/video-editing/ways-of-working|ways of working]] (his rules from corrections), [[03-Areas/video-editing/motion-gallery/motion-gallery|motion gallery]] (approved designs to remix).

## His material, in one shared place

`C:\Users\repzy\Desktop\Video edits\Routerise\Visual Assets\Samuel templates (Editor)\` (copied 2026-10-08, originals untouched):
- `comps from Apollo, 4 AI Tools, TSB\`: 359 comps exported from his three finals, named `<video>_V<track>_<frame>_1` (`apollo_`, `ai4_`, `tsb_`). The construct libraries in the notes above name them.
- `finals stills\ai4\`, `apollo\`, `tsb\`: stills of his finals (file name = mm ss.ss), for calibrating a review.
- `HIS_NEOANIM_ADJ.setting` (his Neo Anim entrance on an adjustment clip), `HIS_BOXMAIN.setting` (with wiring json).
- `magiczoom_instances.json`: his 170 MagicZoom V3 instances, decoded.
- His $7M Founder comps (pyramid, tier walk): `Routerise\Claude Files\Style Study - Cold Outreach\raw\comps\`.

## MagicZoom V3, decoded (2026-10-07)

From his 170 instances: zoom size = 1 + depth × an eased ramp, speed always 2 s, cubic ease, pivot on his face (B2B: 0.51, 0.68). On plain A-roll: mostly Zoom & Hold at depth 0.071 (about 98 f), 0.111 punches on short emphatic lines, slow Standard pushes (0.071–0.111) on long stretches, now and then an inverted zoom-out (0.053) on a return to camera. Media and card clips carry a 0.026–0.03 slow push. The punch-in pass goes on V2 wherever the A-roll shows, after the visuals are final. Tools: the B2B job's `Graphics\Visuals v1\kits\drt\mz_plan.py` (plans and injects into a .drt), `mz_inject.py`, `mzblob.py`.

## How the B2B video was built with it (2026-10-07/08)

Grammar → a build list of 20 constructs, each from one of his comps → builders per folder → install on adjustment clips → frame review from timeline stills against his finals, with adversarial verifiers → fix rounds. Samuel's markers are part of the brief: read them first, on the timeline he wrote them on. The machinery and its pitfalls: [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] (bottom sections) and the job note.
