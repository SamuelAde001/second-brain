---
type: knowledge
area: video-editing
status: active
updated: 2026-10-20
source: local-folder
tags: [client, alex, frontal, brand, fusion, typography, colour]
---

# Frontal brand v2.3.1: the rules for Alex's videos

**From 2026-10-20 every visual in Alex's videos follows Frontal's brand kit v2.3.1.** Samuel, 2026-10-20: *"my client Alex just sent in the new brand guidlines of his company and brand, and they are a must follow"* and *"we just need to make sure his videos now follow the new brand guidelines including all the fonts, colors and everything there"*.

It replaces the July look completely: orange `#FF5A1F`, BGORANGE, Geist, rounded pills and glowing borders. The kit's own words: *"no orange anywhere from now on"*. Finals delivered before 2026-10-20 stay as they are; the old rules remain in [[03-Areas/video-editing/routerise-house-style|house style]] §9 and the edit grammar as the record of that look.

Client: [[03-Areas/video-editing/clients/alex|Alex]]. What has to change in our kit, and the open questions: [[04-Projects/frontal-rebrand-video-kit|Frontal rebrand of the video kit]]. Part of [[03-Areas/video-editing/video-editing|Video editing]].

## The kit

`Routerise\Visual Assets\Frontal Assets\Frontal-Brand-Kit-v2.3.1\` (32 files, dated 2026-10-19): the 29-page brand book PDF, `DESIGN-SYSTEM.md`, `tokens.json`, logos (SVG + PNG), fonts, the website's glow images, three website screenshots and the colour swatches. Designed by GRAFIT for the new frontal.so; owner Alex Vacca. Read the files there for anything this note doesn't cover; never copy the kit into the Brain.

**Font licence.** Season Serif is licensed to Frontal AI LLC; contractors may use it **only for work they do for Frontal** and must not share it. So: never commit the font file to the Brain (it goes to GitHub), never send it to anyone, never use it in HighSignals, @SamuelSignals or any other client's work. Inter and JetBrains Mono are free (SIL OFL).

**Installed on this PC (checked 2026-10-20):** Inter yes (static OTFs, user fonts). Season Serif and JetBrains Mono **no**. Geist is still installed; it's no longer brand for Alex.

## 1. The five principles (the kit's own tie-breakers)

1. Dark first, lit in fluo blue. 2. Serif for the idea, sans for the detail, mono for the system. 3. Square and precise. 4. Show the real thing. 5. Quiet motion: one thing moves at a time, on purpose.

When a video case isn't covered below, decide it with these.

## 2. Colour

One accent only. Fusion values are the hex as 0–1 floats, the same way `#FF5A1F` went in as 1, 0.3529, 0.1216.

| Token | Hex | Fusion R, G, B | Use in video |
|---|---|---|---|
| Dark | `#04060C` | 0.0157, 0.0235, 0.0471 | Every ground. Fades and darkening go to this, never brown |
| White | `#FFFFFF` | 1, 1, 1 | Text on dark. Light sections (website screens, documents) |
| Blue-300 (the accent) | `#A5CCFD` | 0.6471, 0.8000, 0.9922 | One highlighted word, eyebrows, brackets, the active item, the icon |
| Blue-200 | `#CFE2FE` | 0.8118, 0.8863, 0.9961 | Highlighter over text on light screens (multiply) |
| Blue-600 cobalt | `#3B70D2` | 0.2314, 0.4392, 0.8235 | Call-to-action band only, white text large |
| Blue-700 | `#2C55A3` | 0.1725, 0.3333, 0.6392 | Blue text on white (Blue-300 is never text on white) |
| Blue-800 navy | `#1E3970` | 0.1176, 0.2235, 0.4392 | Case-study band, white text |
| Blue-900 tint | `#13254A` | 0.0745, 0.1451, 0.2902 | Quiet callouts and quotes on dark |
| Gray-900 | `#0D0F15` | 0.0510, 0.0588, 0.0824 | Subtle panels on dark |
| Connector grey | `#8C8E99` | 0.5490, 0.5569, 0.6000 | Diagram lines |
| glow-ambient | `#687CDF` @ 40 % | 0.4078, 0.4863, 0.8745 | The blue light on grounds and behind hero art |

- Secondary text = white at 64 %. Lines and dividers = white at 12 % (black 10 % on light).
- Glow cells: gradient `#E6EEFF` → `#B9D4FD` → `#8DB3F2` (top-left to bottom-right), 1.5 px inner line white 55 %, halo `#9EC7FF` at 75 % blurred. Only in the pixel glow (§6).
- **Extended palette** (teal, green, yellow, red, pink, violet; hexes in `DESIGN-SYSTEM.md` §3) is for data, status and tags only: charts, small status chips. **Never** for headlines, logos or hero art. On dark, text from step 300 or lighter; tags = step 900 fill with step 200 text. So a red "negative" is a small red tag, never a red headline tail.
- **Charts:** series in the fixed order on dark: Blue-300, Yellow-500, Violet-500, Pink-500, Red-200, Teal-400, Green-500, Gray-400. Six series at most, labels on the bars, no 3D, no gradients, 1 px gridlines.
- **Bands** (full-frame colour moments): sky = Blue-300 with Dark text, **one per section**, for the key number; navy for a case study; cobalt for the call to action; tint for a quote. Never two coloured bands in a row. Never Blue-300 text on sky or cobalt.

## 3. Type

| Role | Font | Rules |
|---|---|---|
| Headlines, titles, big numbers, quotes | **Season Serif Regular** | Sentence case. One weight: never bold, never italic, never ALL CAPS. One word may be Blue-300 ("Frontal **Five**"). Tracking −3 % (CharacterSpacing 0.97) at display size, −1.5 % (0.985) smaller. Line height 90–100 % at display size |
| Everything people read: supporting lines, captions, list items, card text | **Inter** Regular; Semi Bold for emphasis | Tracking −1.5 to −2 % (0.98–0.985), line height 130–140 % |
| Eyebrows, labels, lower thirds, tags, data labels, buttons | **JetBrains Mono**, ALL CAPS | Short. Tracking +2 % (1.02), +4 % (1.04) at the smallest size |

- The kit's scale in px (web): Display 64 / 56 / 48, Headline 40 / 32 / 28, Title 24 / 20, Body 20 / 18 / 16 / 15 / 13, Mono 15 / 13 / 11. Decks *"scale the whole set up together and keep the ratios"*: do the same in video.
- **Sizes used in the approved-look style frames at 1920×1080** (to confirm on the first Fusion comp): chapter title 132 px, statement over A-roll 96 px, section headline 84–96 px, key number 190–330 px, body 32–48 px, mono eyebrow 26 px, mono labels 19–24 px. ~~Fusion Text+ Size ≈ px ÷ 1920~~ (wrong). **Measured 2026-10-20 in Resolve:** Fusion sizes text by the font's full height (hhea ascender − descender), so Size = px × font height ÷ 1508, with font height Season Serif 1.229, Inter 1.210, JetBrains Mono 1.320. Same for Text+ and his NeoTextMotion; within 1 % on all four fonts (`kits\frkit.py` → `FONT_H`).
- "Putting it together" (the kit's screen recipe): mono eyebrow in Blue-300 → Season headline, one colour → Inter supporting line at white 64 %. One idea per screen.

## 4. Shape

- **Square corners everywhere.** No pills, no capsules, no rounded boxes or cards. `radius-full` only for round avatars (people's photos) and radio buttons.
- **Thin corner brackets** frame labels, buttons, icons and the active item (the kit's `BracketFrame`, 6 px brackets on the web; ~14–22 px arms, 2–3 px thick at 1080).
- 1 px hairlines (2 px at 1080) for dividers and cell borders. **No drop shadows on cards.**
- **Glass** is the only surface with a shadow: fill white 6 % (or Dark 72 % for text-heavy panels over busy footage), 20 px background blur with 140 % saturation, 1 px Blue-300 edge at 20 %, 1 px white 14 % top highlight, shadow 0 / 16 / 40 black 35 %. Square.
- **Diagrams:** objects joined by 1 px `#8C8E99` lines ending in a 6 px diamond. **No arrowheads, no curves**; the objects carry the colour.
- **Icons:** GRAFIT's small solid glyphs, white on dark, always inside corner brackets. We don't have that set yet (see the project note).

## 5. Logo

- Always the **full logo** (pixel icon + wordmark); the icon may stand alone. Never the wordmark alone.
- White wordmark on dark (`frontal-logo-on-dark.svg`, the default), black on light. The icon is always Blue-300.
- **Never** recolour (including the old orange), stretch, rotate, outline, or add shadows, glows or effects. **Never type "Frontal" in a font** in place of the logo.
- Clear space: half the logo's height on every side. Minimum 80 px wide (icon alone 16 px).
- Not where it loses contrast: no logo on a sky (Blue-300) band, the icon disappears.
- **Every Frontal logo file we used before 2026-10-20 is the July orange one** (`Visual Assets\Frontal Assets\frontal-logo-on-dark.png` etc., `Visual Assets\B2B logos (Editor)\frontal-*.png`; their pixels are `#F04000`-ish). Use only the kit's `02_Logos`.

## 6. Glow, grounds and imagery

- **The fluo blue glow** (`PixelGlow`): the pixel icon's seven cells lit, inside a fading grid, blue halo and ambient light. The brand's hero art: **one per composition**, usually left of the headline. Never recolour the cells, light other cells or put text on them.
- **Website hero glow:** `04_Glow` images, at 20 % opacity, blurred ~91 px, behind hero shots.
- **Ground for motion graphics** (our replacement for BGORANGE): Dark, a faint Blue-300 grid (~7–8 %, faded out at the edges), blue ambient light from the top and bottom edges. Same structure as his BGORANGE macro, new colours. Social cards in the kit use a 48 px grid in Blue-300 at 8 %.
- **Imagery:** real product screens, real people, illustrations that explain a mechanism. **No stock photos, no 3D blobs, no purple gradients.** Client logos in Frontal's own graphics are white and one colour.
- **Made-up companies in demos are fine** and **every Frontal client may be shown by logo** (Samuel, 2026-10-20: *"Yes made up companies are ok"*, *"All frontal clients are cleared to show by logo"*). The kit's "real companies only" and "cleared clients only" lines don't bind his videos.
- **No extra kit parts needed** (Samuel, 2026-10-20: *"We don't need those extra kits"*): we make our own icons in the brand's style instead of waiting for GRAFIT's set.

## 7. Motion

- **Quiet motion:** one thing moves at a time, on purpose. Nothing bounces.
- Animated graphics **play once and hold their final frame**: no loops, no replays (Alex, 2026-10-15, in the kit).
- **The kit disagreed with itself on the curve** (README: `cubic-bezier(.23, 1, .32, 1)` and no loops; brand book p22: *"Easing: ease, everywhere"*, *"The glow may pulse slowly"*). **Settled by Samuel, 2026-10-20: the brand book wins.** *"For the contradiction, you need to ease everywhere, use what the brand book says"*. So: the CSS `ease` curve (cubic-bezier .25, .1, .25, 1) on every move we keyframe ourselves, nothing bounces, and the pixel glow may pulse slowly.
- **Our motion stays; only the look changes.** Samuel, 2026-10-20: *"Motion, keep our pacing and one by one reveals, keep our current motion and change only the look"*. NeoAnim entrances, timing constants, staggers, section slams and shine passes stay as in [[03-Areas/video-editing/routerise-house-style|house style]] §10 and the edit grammar; what they move is now on-brand. The kit's 140–200 ms numbers are for website UI, not our graphics.

## 8. Formats in the kit that touch video

- Slides 1920×1080: title slides dark with the glow; content dark or light with an eyebrow and a 56–64 px headline, at most three points; one sky slide per section for the key number; case studies on navy. Closest to our full-screen motion graphics.
- Banner recipe: glow left, headline right with one blue word, a muted line under it, logo top right. Our brand beat uses it.
- Frontal Five (newsletter sub-brand) has its own frosted arrow; never mix it with the pixel glow. Not in the kit we were sent.

## 9. Style frames

Ten frames of our constructs redrawn in this brand, with the real fonts and Alex's frame from video 2, rendered 2026-10-20 for Samuel: video 2's job folder → `Docs\Frontal brand study (Editor)\` (`review_sheet_1.png`, `review_sheet_2.png`, `frames\f1–f10.png`, source `frames.html`). Ground + chapter title, key line over A-roll, list reveal, tool logo wall, sky key number, glass stat beside Alex, diagram, chapter lower third, brand beat, website beat.

Back to [[03-Areas/video-editing/clients/alex|Alex]] · [[03-Areas/video-editing/video-editing|Video editing]]
