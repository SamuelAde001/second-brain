---
type: knowledge
area: video-editing
status: active
updated: 2026-09-30
source: interview
tags: [visuals, motion-graphics, house-style, routerise, gallery]
---

# Motion gallery: pills, boxes, cards and circles

Our own library of motion-graphic components, in Route Rise house style, to pick from on every video. Built 2026-09-30 after Samuel rejected the Apollo visual stills.

> Samuel, 2026-09-30: *"You tend to use the same Design every time, the same color ratio, yes we have a color we use but, mix it up, use light and dark orange and white, and sometimes grey"* · *"Everything looks mediocre and Shallow"* · *"Let's create our own inspiration Galerry of different types of Boxes, Cards, circles, pills, that we can use from"* · *"All for motion grahpics"* · *"the finished videos of the last 3 are okay, just that we need more better and different types"*.

**Open it:** run `python 03-Areas/video-editing/motion-gallery/build_gallery.py`, then open `motion-gallery.html` in the same folder. The built page is gitignored, because it embeds the reference frames and A-roll stills. The sources in `src/` are the record.

## Rules it follows

- **Same font, same colours, more ways of using them.** Geist only. Dark orange `#FF5A1F` (deep `#BE4117`, `#591E0B`), light orange `#FD9457` (cream `#FFE9DC`), white, grey. Ground `#1B0903`. From [[03-Areas/video-editing/routerise-house-style|Routerise house style]].
- **Colour recipes rotate; the ground doesn't.** Solid orange, white paper, light orange, grey glass, outline: no two neighbouring designs share a recipe. The ground is the A-roll or BGORANGE, nothing else. Samuel, 2026-09-30: *"The background must be BGorange"*, *"I want a consistent background"*.
- **The approved baseline is the last 3 finals:** *$7M Founder*, *Taking a Step Back from Claude*, *4 AI Tools* (Route Rise #3). Orange number pills, orange-ringed hub circles, dark list cards, the 4-tools tiles, the top stepper, two-tone headlines, highlighter marks. The gallery shows them in a strip and adds types that aren't there yet.
- **Big, few words, depth, and something always moving.** [[03-Areas/video-editing/visual-vocabulary|Visual vocabulary]] still applies.
- Every design can be rebuilt in Fusion from real nodes (rectangle and ellipse masks, NeoBevel, NeoGlow, NeoLightSweep, DropShadow, 3D). Each card on the page carries a one-line Fusion note.
- **Sample copy only.** Text and numbers on the page are placeholders to judge the look, never facts for a client video.

## Sources studied

- `Routerise\Visual Assets\Visual Inspo\`: 125 frames. Andy Stauring's dropshipping videos and Nate Herk's AI-agency videos, both Route Rise clients.
- The agency's best editor: 44 stills in `3. I Tried 100+ AI Tools…\Docs\Visual study\best-editor\`.
- The last 3 finals: 270 frames picked where the picture changes sharply, which catches graphic reveals.
- Web, 2026 motion trends: liquid-glass callouts, hand-drawn strokes, grain, kinetic type, border-beam outlines, Dynamic Island morphs, bento grids, orbit animations ([Videobolt trends 2026](https://blog.videobolt.net/post/top-motion-graphics-trends-2026), [Liquid Glass UI element](https://videobolt.net/author/kalinichev/liquid-glass-ui-element-2), Dribbble searches for dynamic island, orbit, progress ring, neon badge, bento grid).

## The designs (v1, all proposed)

| Code | Design | Recipe | Ground | From |
|---|---|---|---|---|
| P01 | Medallion pills, zigzag list | grey glass + white medallion | A-roll | Inspo #3 |
| P02 | Pill with a status tag hanging off it | white / deep orange + grey tag | warm dark | Inspo #14 |
| P03 | Ghost-numeral chapter pill | deep orange | A-roll | Inspo #40, #58 |
| P04 | Corner-badge pills (? ! ✓) | cream | A-roll | Inspo #1, #11, best editor 31 |
| P05 | Dynamic Island notification | black + orange | A-roll | web |
| P06 | Liquid-glass logo pill | clear glass | A-roll | web trend, Inspo #29 |
| P07 | Border-beam pill | graphite + orange light | grey | Inspo #113, web |
| P08 | CAN / CANNOT verdict pair | white vs deep orange | A-roll | Inspo #98 |
| P09 | Stat pill with segment bar | grey glass + light orange | A-roll | Inspo #81, best editor 44 |
| P10 | Search pill that types | white | cream | Inspo #32 |
| P11 | Flow chips that break | grey → orange | A-roll | best editor 35 |
| P12 | Toggle switch | white on full orange | orange | web |
| P13 | Pill with a header tab | white + orange tab | A-roll | Inspo #72 |
| B01 | Checklist box, upcoming rows blurred | grey glass + orange rim | warm dark | Inspo #10, best editor 38 |
| B02 | Window compare, theirs vs yours | graphite, white | grey | Inspo #61 |
| B03 | Bento grid of results | orange, white, light orange, grey | warm dark | web |
| B04 | Chat that builds bubble by bubble | white, orange, grey | cream | Inspo #52, #122 |
| B05 | Tabbed box, steps 1–4 | grey glass + orange tab | warm dark | Inspo #100, #101 |
| B06 | Receipt that prints, then a stamp | white paper | light orange | web |
| B07 | Leaderboard that re-sorts | graphite + orange | grey | web |
| B08 | Quote box with marker highlight | cream | warm dark | best editor 6 |
| C01 | Tilted glass pair with number badges | grey glass | warm dark | Inspo #6 |
| C02 | Fanned deck of cards | grey + cream front | A-roll | Inspo #73, #85 |
| C03 | Counter card + hand-drawn arrow | graphite + light orange | grey | best editor 26, 27 |
| C04 | Glossy 3D tiles with reflection | white vs orange | grey | Inspo #103, #104 |
| C05 | Milestone flags on an orange horizon | cream + orange | grey | Inspo #74, #75 |
| C06 | Wrong vs right cards | grey vs orange | warm dark | best editor 13, Inspo #125 |
| C07 | Profile card with buying signals | white | cream | 7M 1:07 (approved) |
| C08 | Notification stack | light glass | A-roll | web, Inspo #23 |
| O01 | Hub ring with labels around it | orange ring | grey | Inspo #86, #87 |
| O02 | Sonar hub with pills on the rings | white + light orange | grey | Inspo #56, #57, best editor 12 |
| O03 | Orbit system | orange planet + glass | warm dark | best editor 19, Inspo #41, web |
| O04 | Big-numeral circle with pills | outline + graphite | warm dark | best editor 1 |
| O05 | Progress ring | orange on cream | cream | web |
| O06 | Avatar row, YOU in the middle | grey + white | A-roll | Inspo #45 |
| O07 | Venn, the overlap is the answer | white on full orange | orange | web |
| O08 | Rotating seal stamp | deep orange + light orange | warm dark | web |
| O09 | Hand-drawn marker circle | orange marker | A-roll | web, best editor 27 |
| O10 | Social buttons, like / save / send | grey glass + orange | A-roll | Inspo #20 |

## Grounds (settled 2026-09-30)

v1 tried grey, cream and full-orange grounds. Samuel moved every one back to BGORANGE (*"Love this but The background must be BGorange"*, on 13 designs). v2 rebuilds BGORANGE from the macro itself; see [[03-Areas/video-editing/routerise-house-style|house style §9]].

## Samuel's verdicts

Round 1, 2026-09-30, pasted from the page's "Copy my review". Full notes are in `src/verdicts.js`.

- **Approved (16):** P01, P02 (*"Just don't use that background wave"*: removed), P03, P04, P08, P11, P13, B01, B05, C06, C08, O03, O04, O06, O09, O10.
- **Dropped (3):** P12 toggle, B06 receipt, O08 rotating seal.
- **Changed in v2 (19):**
  - BGORANGE only (*"Love this but The background must be BGorange"*): P07, P10, B02, B04, B07, C03, C04, C05, C07, O01, O02, O05, O07.
  - P05: *"make it appear from the buttom instead if it's on screen, but we can use this in different other places"*. It now rises from the bottom over the A-roll, and the top version stays an option.
  - P09: *"I prefer a bar that fills up instead of the dots"*.
  - B03: *"Make it one card, not multiple"*.
  - B08: *"Would prefer quotes to be on a picture/video of the person quoting it"*. It now sits on the speaker's footage, with a real line from Alex's Apollo script.
  - C01: *"I don't normally use this kind of in Animation, and I don't like the rotation"*. Now flat, with no 3D.
  - C02: *"I always prefer this smaller, too big on the screen right now"*. About a third smaller.
- **Not reviewed:** P06.

Round 2 (v2) is waiting on his marks. An approved design gets rebuilt as a visual-engine scene and a Fusion comp when a video needs it.

## Build notes

- Same API as the visual-engine kit (`el`, `W`, `A`, `F`, `neo`, `pop`, `sweep`, `count`, `typeText`), bound per stage, so a design ports into a render scene by dropping the `S.` prefix. Engine: `src/gallery-engine.js`; one file per family: `pills.js`, `boxes.js`, `cards.js`, `circles.js`.
- Reference ids: `I<n>` is the nth file of `Visual Inspo` sorted by name, `B<n>` the nth still of `best-editor`, `M7-67` a frame of the $7M Founder final. The build script turns them into thumbnails.
- QA: `python build_gallery.py --stills --t=3.8 --only=P01,B02` renders `?only=CODE&t=T` with headless Chrome into `_cache/stills/`. Headless Chrome won't go narrower than 512 px, so phone layout can't be checked this way.
- A flex container drops the space between a text node and a `<span>`. Wrap mixed text (`tt()` output) in one span, or words run together.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
