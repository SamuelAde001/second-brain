---
type: knowledge
area: video-editing
status: needs-input
updated: 2026-10-20
source: local-folder
tags: [routerise, alex, frontal, brand, fusion, templates]
---

# Frontal template library (Fusion)

Samuel, 2026-10-20: *"come up with new design templates and styles that we can use in the videos, to give it more variety and style, so we don't use the same things over and over again"*. Built by the Editor the same day on the Frontal kit, rendered in Resolve, reviewed twice. **Waiting on Samuel's review** of the sheets before any template goes into a video.

Rules: [[03-Areas/video-editing/clients/frontal-brand-v2|Frontal brand v2.3.1 for video]]. Project: [[04-Projects/frontal-rebrand-video-kit|Frontal rebrand of the video kit]]. Area: [[03-Areas/video-editing/video-editing|Video editing]].

## Where it lives

**Master: `Routerise\Visual Assets\Frontal templates (Editor)\`** (Samuel, 2026-10-20: *"Yes: copy the kit to Visual Assets\Frontal templates (Editor) and install BGFRONTAL into My macros."*). Each Alex job copies it into its own `Graphics\Frontal kit (Editor)\` and works there; kit fixes go back to the master. Video 2's working copy is the original. Its `README.md` says how to use it. Outside the Brain: Season Serif is Frontal's licence and never enters the Brain or GitHub.
- **BGFRONTAL is installed in `My macros`** beside BGORANGE (2026-10-20): the same nodes under the same names, recoloured; it renders pixel-identical to the ground in every template. Made by `frkit.bgfrontal_setting()`; BGORANGE was only read (hash unchanged). It may need a Resolve restart to show in the macro list.
- `kits\frkit.py`: brand tokens, calibrated text, brackets, hairlines, boxes, glass, connector, pixel glow, bands, logo, icons, BGFRONTAL (generated from his BGORANGE, which stays untouched), his NeoAnim and NeoTextMotion re-skinned, `write()`.
- `kits\frlib.py`: 13 geometric glyphs, three icon tiles (bracket, panel, sky), scrim, eased wipe (draw-ons, bars, band slides).
- `catalog.md`: every template with its look and motion. `proof.py` + `lib\J1.py`..`J10.py`: the generators. `rebuild_all.py`: rebuilds everything and renders each last frame.
- `kits\lab.py` renders any `.setting` on the scratch timeline `zz Lab (Editor)`; no other timeline is touched.

## The 27 templates

| Kind | IDs |
|---|---|
| Chapters | CH01 centred title · CH02 big number · CH03 sky band · CH04 progress rail · CH05 glass over A-roll |
| Lists | LI01 hairline rows · LI02 card grid · LI03 one at a time · LI04 glass checklist over A-roll · LI05 before/after columns |
| Lower thirds | LT01 bracket name · LT02 rule + label · LT03 glass bar · LT04 tool chip · LT05 source tag |
| Motion graphics | MG01 glass stat · MG02 counter · MG03 bar chart · MG04 flow diagram · MG05 quote · MG06 logo wall · MG07 UI frame + spotlight · MG08 number compare · MG09 vertical timeline |
| Brand + icons | OUT01 brand beat (pixel glow, logo, button) · IC01 icon and logo board |

Motion is his (Samuel: *"keep our current motion and change only the look"*): NeoAnim slide-ins one by one, NeoTextMotion word reveals, eased draw-ons. Variety comes from entry direction (left, right, drop), sharp or blurred starts, draw-ons, band slides, counters and a slow glow pulse.

## What the build taught (for any later builder)

- Season leading: the kit default (LineSpacing 0.78) is tight for two or three lines; use 0.85–0.92.
- A blue word in NeoTextMotion: the colour range counts characters without line breaks (fixed in frkit 2026-10-20).
- NeoTextMotion's shine and shadow are off by default now (the brand allows neither).
- `text_width()` is close but not exact: Fusion draws mono about 5 % narrower and Inter and Season about 1–3 % wider. Measure tight fits from a render.
- The connector grey at full strength reads as white ~55 %: right for diagrams, too loud for a progress rail (white 12–20 % hairlines instead).
- Inside a card, the panel and each item get their own reveal, about 6 f apart; never one reveal for the whole card.
- Counters: a Text+ with a Lua expression driven by an eased spline, digits in fixed slots so the number doesn't wobble (`lib\J7.py`).
- In the A-roll at 600 frames into *Cut v5*, Alex's face sits at about x 880–1100, y 190–500, and his hands reach x 400–1250 low in frame: lower thirds stay left of x ~700.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
