---
type: project
area: video-editing
status: needs-input
updated: 2026-10-20
source: local-folder
tags: [project, routerise, alex, frontal, brand, fusion]
---

# Frontal rebrand of the video kit

**Goal:** every visual the Editor builds for Alex follows Frontal brand kit v2.3.1, starting with video 2 ([[04-Projects/routerise-claude-10000-saas|I Gave Claude 10,000 SaaS Companies]]). Samuel, 2026-10-20: *"We would have to do this study before we can move forward on this video"*. **Done when** the kit, macros and templates below build on-brand comps and Samuel has approved a set of sample comps rendered from Resolve.

The rules: [[03-Areas/video-editing/clients/frontal-brand-v2|Frontal brand v2.3.1 for video]]. Area: [[03-Areas/video-editing/video-editing|Video editing]].

## Status

- **2026-10-20, study done (Editor).** Kit read in full (brand book, design system, tokens, logos, fonts, website screens). Every place our style uses the July look found. Ten style frames rendered for Samuel: video 2's `Docs\Frontal brand study (Editor)\`. Old rules marked superseded in the notes (list A). **Waiting on Samuel:** the questions below. Then list B is built.
- **2026-10-20, Samuel's answers:** *"For the contradiction, you need to ease everywhere, use what the brand book says"* · *"Motion, keep our pacing and one by one reveals, keep our current motion and change only the look"* (Q1) · *"We don't need those extra kits"* · *"Yes made up companies are ok"* · *"All frontal clients are cleared to show by logo"* · *"Yes install the fonts"* (Q5). Q2, Q3, Q4 and Q6 were not answered: the Editor works on the recommendations (Season for statements + Inter for running captions; circle PIP with a thin Blue-300 ring; white one-colour logos on our graphics; old orange logos left where they are and not used). Those are working defaults, not his decisions, until he confirms.
- **2026-10-20, built and proved in Resolve (Editor).** Fonts installed (Season Serif, JetBrains Mono Regular + Medium static). Generator kit `frkit.py` + shared pieces `frlib.py` in video 2's `Graphics\Frontal kit (Editor)\kits\`; BGFRONTAL is generated from BGORANGE (BGORANGE untouched). Four proof comps (chapter title, hairline list, glass stat over Alex, brand beat with pixel glow) render from nodes and match the style frames: `renders\proof\v3_sheet.jpg`. Text size rule measured: Size = px × font height / 1508. Samuel asked next for variety: *"different lists styles, different chapter styles, different lower thirds, different motion graphic styles, icons and animations so we have variety"*.
- **2026-10-20, library run (Editor).** Catalog of 23 new templates (5 chapter, 4 list, 5 lower third, 8 motion graphic, 1 icon board): `Graphics\Frontal kit (Editor)\catalog.md`. Built by a workflow at pool 3, 10 jobs, each rendered in Resolve on `zz Lab (Editor)` and self-checked. **Cost written before launch:** ~6–8 weekly points (usage card 16:30 WAT: weekly 78 %, 5-hour 8 %; expected end ~86 %; stop line 95 %). Video 2's visual build stays after the Wed 2026-10-21 23:00 reset.
- **2026-10-20, library built (Editor).** All 23 templates built and rendered by 10 builders (~1 weekly point; card 79 %). Kit fixes from the run: NeoTextMotion shine and shadow now off by default (the brand allows neither); the blue-word range now counts characters without line breaks (it spilled onto the next line); the pixel-glow grid now covers the frame (it showed a hard edge); the brand beat's line and headline pulled inside the safe area. **Review round launched:** a fresh reviewer per job checks every frame against the brand rules, a fixer applies the confirmed faults; 11 jobs at pool 3, cost written first: ~1.5–2 weekly points (card 80 %).
- **2026-10-20, library done (Editor).** Review round: 5 hard faults and ~30 visible ones fixed (cost ~1 weekly point; card 81 % after both runs). All 27 rebuilt from the current kit and rendered fresh. Note: [[03-Areas/video-editing/clients/frontal-template-library|Frontal template library]]. **Waiting on Samuel:** his review of the four sheets; and his yes to (a) copy the kit into `Visual Assets\Frontal templates (Editor)` so every Alex job can use it, (b) install BGFRONTAL into `My macros` (both are outside video 2's job folder).
- **2026-10-20, *"Yes: copy the kit to Visual Assets\Frontal templates (Editor) and install BGFRONTAL into My macros."*** Done (Editor): master kit in `Visual Assets\Frontal templates (Editor)\` (163 files; it rebuilds into itself, matches the job copy and renders in Resolve); `My macros\BGFRONTAL.setting` installed, pixel-identical to the kit's ground, BGORANGE untouched. List B items 2 (BGFRONTAL) and 4 (generator kit) are done; item 7 (sample comps) is the library, waiting on his review.

## What stays

The brand changes how things look, not how the edit works. These hold as they are: the cut method and rhythm, chapters and music on section boundaries, the PIP demo system (apart from its ring, Q3), visuals chaining back to back with breathing gaps, show the real thing (real UI, real websites, real logos when Alex names a company), hide-until-said mosaic on list items, never text over his face, node naming and layout, editable Fusion nodes only, sound design (every element gets its own sound, no repeats). Variety stays a rule too: one design repeated is still "mediocre", now with Season, Inter, Mono, Dark, white, Blue-300 and the bands instead of the orange ramp.

## What changes, construct by construct

| Was (July look) | Now (v2.3.1) | Frame |
|---|---|---|
| BGORANGE ground (`#110602`, orange light top and bottom, faint grid) | Same structure, new colours: Dark, blue ambient light top and bottom, faint Blue-300 grid. New macro **BGFRONTAL** | f1 |
| Geist ExtraBold ALL CAPS titles, two-tone white + orange line | Season Serif Regular, sentence case, one Blue-300 word at most | f1, f2 |
| "Box main" caption bar, two-tone caps, red/green tails | Statement in Season over a neutral fade to Dark, low; long panels on square glass. Red/green only as small status tags | f2, f6 |
| Numbered pills, white number badges, ghost numerals | Hairline rows, mono numbers in corner brackets, active row white, others at 64 % | f3 |
| Tool medallions (white disc, orange ring, colour logo), lit tool cards | Square logo wall, white one-colour logos, active cell bracketed (Q4) | f4 |
| Orange counters, big orange numbers | Season numbers; the section's key number on a sky band (one per section) | f5 |
| Rounded glass card, orange border, Neo Glow, bevel, light sweep, shine, drop shadow | Square glass panel to the kit's spec; the only surface with a shadow. No bevel, sweep, shine or border glow (Q1) | f6 |
| Curved white arrows, dashed orange connectors | 1 px grey lines ending in a diamond, straight or elbowed, no arrowheads | f7 |
| Section slam (scale 1.594 → 1.0 + blur), orange chapter pill | Mono eyebrow in brackets + Season title, quiet entrance (Q1) | f8 |
| Orange Frontal logo with SoftGlow / in a capsule over his head | Kit logo only, no effects, clear space; brand beat on the banner recipe with the pixel glow | f9 |
| Rounded spotlight (CornerRadius 0.12), orange Neo Highlighter | Square spotlight, Blue-200 highlighter (multiply), bracket focus | f10 |
| Down fade to `#1B0903` | Down fade to Dark `#04060C` | f2, f8 |
| Orange flaticon icons | GRAFIT icon marks in brackets once Alex sends them (A2); until then white solid glyphs in brackets | f7 |
| Accent "changes per video" | Blue-300, always | |
| Section slam, NeoAnim slide-up 20–25 f, StartBlur 25 | Depends on Q1 | |

## A. Notes marked superseded (done 2026-10-20)

[[03-Areas/video-editing/routerise-house-style|House style]] §9 · [[03-Areas/video-editing/edit-grammar/edit-grammar-shared-rules|edit grammar shared rules]] S0.3–S0.10 · [[03-Areas/video-editing/edit-grammar/edit-grammar|edit grammar]] · [[03-Areas/video-editing/sops/fusion-build|Fusion build SOP]] §2 · [[03-Areas/video-editing/ways-of-working|ways of working]] · [[03-Areas/video-editing/fusion-node-system|Fusion node system]] · [[03-Areas/video-editing/visual-vocabulary|visual vocabulary]] · [[03-Areas/video-editing/motion-gallery/motion-gallery|motion gallery]] · [[03-Areas/video-editing/clients/alex|Alex]] · [[03-Areas/video-editing/clients/routerise|Route Rise]] · the Editor's profile and memory. The old text stays as the record of the July look; each carries a dated pointer here.

## B. To build after Samuel's answers

1. **Fonts:** install Season Serif and JetBrains Mono (Q5), restart Resolve, check Fusion lists them. JetBrains Mono comes as one variable file: if Text+ shows only one weight, use the static TTFs from JetBrains' own release (OFL).
2. **BGFRONTAL macro:** a copy of `My macros\BGORANGE.setting` with the new colours. BGORANGE itself is never edited.
3. **Down fade, Glass effect, Box main:** Frontal copies of his macros (Dark fade; square glass to the kit's spec; caption strip as square glass). His originals untouched.
4. **Generator kit `frkit`** beside `pk.py` / `pillkit.py`: colours, fonts, `bracket()`, `hairline()`, `glass()`, `connector()` (line + diamond), `pixel_glow()`, `sky_band()`, `eyebrow()`, `title()` with one blue word. A new starting template in place of `gen_test_card.py` (`gen_frontal_card.py`).
5. **Focus base clip and highlighter:** square spotlight, Blue-200 highlighter.
6. **Visual engine and visual sheet** (`scripts/visual-engine/scenes/kit.css`, `gen_sheet.py`): a Frontal theme so previews match.
7. **Sample comps:** six to eight of the style frames built as real Fusion comps on a test timeline, frames exported and checked, sent to Samuel. His approval closes this project.
8. **Logos:** use only the kit's `02_Logos`. The July orange files stay where they are unless Samuel says to move them (Q6).
9. **Frontal website beats:** capture frontal.so live (the new GRAFIT site) for any website or brand beat. No old capture is reused.
10. Motion gallery and the 359 comps in `Samuel templates (Editor)`: they stay the vocabulary for structure and timing; colours and fonts are swapped at build time. No rebuild of the gallery unless Samuel asks.

Cost guess: one session for items 1–7, a few weekly points; video 2's visual build after the Wed 2026-10-21 23:00 reset.

## Questions for Samuel

1. **Motion.** The kit wants *"quiet motion: one thing moves at a time"*, short moves, nothing bouncing, graphics play once and hold. Our signature is a 20–25 f slide-up with heavy blur, per-word stagger, light sweeps, moving shines, border glows and the section slam. Recommendation: keep the pacing and the one-by-one reveals (they already move one thing at a time), shorten entrances to 10–14 f on the brand curve with light motion blur, drop the sweeps, shines, border glows and the slam's scale-blur. Or keep our motion and change only the look.
2. **Kinetic captions.** Season Serif for statements, Inter for running captions and list text (recommended), or Inter for all on-screen words?
3. **PIP.** Keep the circle with a thin Blue-300 ring, no glow or shadow (recommended), or a square PIP framed by brackets?
4. **Tool logos.** White one-colour logos on our own graphics (the kit's rule for logos in Frontal graphics), full colour only inside real UI and screenshots (recommended), or keep colour logos?
5. **Fonts.** OK to install Season Serif and JetBrains Mono for your Windows user now?
6. **Old orange logos** in `Visual Assets\Frontal Assets\` and `B2B logos (Editor)\`: move them into an `_July brand (retired)` folder, or leave them?

## For Alex (Samuel relays)

1. The kit disagrees on motion: cubic-bezier(.23, 1, .32, 1) and "no loops" (README, design system) against "ease everywhere" and "the glow may pulse slowly" (brand book p22). Which one, and does "quiet motion" cover YouTube graphics?
2. Missing parts the kit points to: GRAFIT's icon marks, `assets/gtm-logos`, `website/README.md` (motion tokens), `tokens.css`, or access to the full kit (`github.com/frontal-so/frontal-brand-kit`).
3. The kit says graphics *"show only real companies and real public events, with a source"*. Our UI demos use made-up company names for claims. OK in his videos?
4. Which of Frontal's own clients are cleared to show by logo (the kit's guardrail)?

Back to [[03-Areas/video-editing/video-editing|Video editing]]
