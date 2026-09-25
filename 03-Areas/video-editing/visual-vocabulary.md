---
type: knowledge
area: video-editing
status: active
updated: 2026-09-25
source: local-folder
tags: [visuals, house-style, routerise, fusion]
---

# Visual vocabulary: how Samuel's visuals look, and why Claude's were called mediocre

Studied 2026-09-25 for Route Rise #3, on Samuel's instruction (*"cross-check how I used to edit… study the finals"*). Sources: the finals of *$7M Founder* (`v2.mp4`, 7:30) and *Taking a Step Back from Claude* (`v2.1.mp4`, 10:41), TSB Timeline 2's node trees, a video by Route Rise's best editor, and the Route Rise editing guide. Contact sheets and stills: `Routerise\3. I Tried 100+ AI Tools…\Docs\Visual study\`. Companion notes: [[routerise-house-style]], [[fusion-node-system]], [[ways-of-working]].

## 1. What makes a visual Samuel's

1. **Show the real thing.** Real UI (screen recordings, website screenshots rebuilt or zoomed), real logos, real footage (AI B-roll, YouTube clips framed in the YouTube page, the A-roll itself). Abstract metaphors only when nothing real can show it.
2. **Few words.** Chips of 1–4 words. Two-tone headlines (white + accent) only on key statements. Never a sentence of explanatory text on a card.
3. **Big and bold.** Graphics fill the frame or a whole side of it. Not small cards parked in a corner.
4. **Depth from real effect nodes**, stacked: NeoBevel (edge light), NeoLightSweep Pro (shine pass), NeoGlow (glow on accent strokes, icons, text), DropShadow, NeoReflection (floor reflection under hero objects), 3D (Extrude3D / Renderer3D, perspective tilt), GaussianBlur backgrounds (depth of field), Vignette, ResolveFX Grid on the ground. Measured on TSB Timeline 2: his comps carry these nodes. Claude's carried almost only plain `Blur` nodes.
5. **Layers.** Foreground chip overlapping a card, card over a blurred real UI, the A-roll shrunk into a bordered card with graphics around it, a hand passing in front (MagicMask).
6. **Colour carries meaning.** Green = signal, good, verified. Red = noise, problem, broken. Brand accent (Frontal `#FF5A1F`) is the thread. Box fills vary: frosted glass, translucent orange gradient, near-black, white/light UI cards, desaturated red wash for a negative beat.
7. **Grounds.** Full-frame graphics sit on a warm near-black with a radial accent glow (usually from below), a faint grid, and a vignette. Or on a blurred, dimmed real screenshot. Never flat black.
8. **Motion.** NeoAnim slide-up (20–25 f, heavy start blur, per-word stagger, motion blur), splines, never linear. Something always moves: slow push, drift, a light sweep after landing, counters rolling.
9. **A-roll breathes.** 3–6 s stretches of plain A-roll between visuals, carried by MagicZoom punch-ins.

## 2. His list styles

| List | Where seen |
|---|---|
| A-roll card at the top, orange gradient pills stacked below, big ghost numeral in each pill, dashed connector | 7M 0:18, TSB 0:15 |
| Numbered chip lower-left on the A-roll; the upcoming item blurred, revealed on the word | 7M 0:39, 1:44 |
| Two numbered cards floating either side of him | 7M 0:13 |
| Tool pill with number + logo at the bottom, over that tool's own UI | 7M 2:05 (1 CLAUDE), 2:16 (2 APIFY), 2:37 (3 ORIGAMI) |
| Tall translucent card beside him; items with icons build one by one | 7M 6:43 (TIER 1) |
| Mac-window card (traffic lights) holding a mini flow (LEADS → CALLS → REVENUE), curved arrow | TSB 0:12 |
| Icon source → department pills with branching arrows | TSB 0:57 |
| Recap chips at the bottom (green FUNNEL SYSTEM / TIER SYSTEM) | 7M 1:57 |

## 3. Why the TSB visuals were called mediocre

Samuel's creative director called the Claude-built visuals *"very mediocre… shallow… didn't have depth"*. Samuel, 2026-09-25: Claude faked glows and built shadow boxes instead of using NeoGlow and the DropShadow node. Diffing Claude's original `.comp` files against the timeline confirmed it: **zero** NeoLightSweep, NeoGlow, NeoReflection, NeoBevel or DropShadow in Claude's comps. Every one in those comps now was added by Samuel. From the frames, the rest of the gap:
- small cards in the top-right corner with tiny text, where his fill a side of the frame;
- abstract metaphors (seesaw, gauge, coins, dopamine meter) where he shows a real thing;
- the same brown card again and again; his mix fills and colours;
- full-frame panels of paragraph text;
- flat 2D; his use perspective, reflection, 3D.

## 4. Route Rise's best editor (reference video, Nate Herk, "Anthropic's CEO: How to Build a 1 Person Business with Claude")

44 stills in `Visual study\best-editor\`. What to take from it:
- **Glass cards** with a dark-to-accent gradient fill, a bright rim light along the top edge, gradient icons, and numbered diamond badges.
- **3D perspective rows** of cards with a slow camera drift. The not-yet-spoken card is pixelated (signposting).
- **Sonar rings and a radial glow** on a near-black ground. Orbits of avatars or icons around a hub.
- **Colour meaning:** red card = the wrong way, accent card = the right way, side by side.
- **A-roll + list:** chips or logos popping in a row along the bottom. Small icon cards stacking top-left with status dots.
- **Node graphs** with curved connectors for workflows. Flow chips with arrows (step → step) along the bottom of the A-roll.
- **Real pages rebuilt around real content.** The YouTube watch page with the actual video inside it, a site with its logo strip, a dock of app icons.
- **Counters and bars inside glass cards** (16 → 19 → 23), with a hand-drawn arrow and a handwritten note.
- **B-roll** darkened, with one or two words over it.

## 5. Route Rise editing guide (Module 1, agency training)

Source: the agency's Notion training (Module 1 "Route Rise Media Editing style", read 2026-09-25). *"We may not follow all"* (Samuel), but consider it every time.
- **Frequency:** a change about every 3 s (cut, move, text, B-roll, animation), constant for the whole video, the back end included. Only the mix changes.
- **Mix:** fast pacing = 50% B-roll + text, 40% animation, 10% zooms. Slow pacing = 40% / 30% / 30%. Fast pacing at the start of a topic, a hook, a new list.
- **B-roll shows, animation explains.** Animate only what B-roll can't show. Treat viewers like kids: simple, literal.
- **Retention devices:** signposting with blur (upcoming items blurred), progress bars / visual timelines, zoom + text on key words, moving B-roll + text.
- **Never:** keyboard-typing SFX, loud repetitive SFX, light-leak transitions, jump zooms, static animations or static text, the same animation or the same song twice (adapt it), a song over 90 s, surface-level B-roll, quality dropping off later in the video, long gaps without stimulus, uhms left in.
- **B-roll:** custom/movie over stock. Vignette + a slight glow on all B-roll. No slow-mo stock of people talking. Show repeated B-roll differently (e.g. as a polaroid).
- **Text:** client colours for emphasis, size and weight to separate title and subtitle, something always moving behind or under text.
- **Music** changes with the subject, smoothly. **SFX** subtle, to make visuals feel real.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
