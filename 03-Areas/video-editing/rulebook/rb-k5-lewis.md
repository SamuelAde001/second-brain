---
type: sop
area: video-editing
status: needs-input
updated: 2026-11-07
source: interview
tags: [rulebook, lewis, routerise]
section: K5
---

# K5 · Lewis Mountstephens (client overlay)

> **Read when:** any step of a Lewis job that touches the look: planning, every build, every review. **Client values:** this note. **Status:** built 2026-11-07 from Samuel's 44 verdicts on the reference study and his premium list (*"anything I have approved here stays for this client lewis"*). The rules carry his words; the wording of the overlay itself waits for his ✔.

## Rules
### Who and what
- **K5.1** Lewis Mountstephens is the **CEO of Route Rise**, Samuel's boss, and this is his own channel. Every Lewis video is top priority and must be premium. ✅ *"he is my Boss and CEO so this video needs to blow his mind, it needs to be good"* (2026-11-07)
- **K5.2** His agency style, not his last video's: Lewis wants what Route Rise does for its top clients. ✅ Lewis (Slack, 2026-11-06): *"no forget last video … i wanna replicate everything we do for our top clients"*
- **K5.3** The guide for every Lewis video is his Long-Form SOP (Notion, saved in the job's `Docs\Lewis Long-Form SOP.md`). ✅ *"Let's use this as guide for his videos"* (2026-11-07)
- **K5.4** Footage: DJI Osmo, 4K HEVC 29.97 fps, stereo 48 kHz, one camera, no separate mic file. The 2026-10-26 set is red-lit (red wall). Grade with the Osmo Pocket 3 plugin for vibrance (SOP). ⚙️ (2026-11-07)

### The reference
- **K5.5** The reference is the Frame.io edit v1_4 (Lewis's niche-down video, 20:25), studied 2026-11-07: [[04-Projects/routerise-lewis-art-of-winning-youtube|job note]], `Docs\Reference study - v1_4 (Editor).md` and the second-by-second log. The copy is in the job's `Visual Inspo\Reference (Frame.io v1_4) (Editor)\`. Its grammar is kept (below); its light pages, red/green coding and FX on A-roll are not. *"I want my video to look different a bit but better"* (2026-11-07)

### Colours
- **K5.6** Black, gold and white. White text, gold `#FBD62D` for keywords, one near-black background for every animation. ✅ Lewis (Slack): *"use black, gold, and white text for colours"*; SOP.
- **K5.7** Red and green only on a positive or negative element, never as decoration or section colour. Everything else is in Lewis's colours. ✅ *"Use red and green only for possitive and negative elements specifically,the rest should use Lewis actual collors"* (D2, F4, 2026-11-07)
- **K5.8** Glow shifts a colour, so use variants: pick the fill shade so the glowing result reads as `#FBD62D`, and use a darker gold only for shadows and glow tints. Never a second gold. ✅ *"The glow makes the color change slightly so use varients"* (D5, 2026-11-07)
- **K5.9** Before building, check one graded A-roll frame beside a gold graphic: the red-lit set against black/gold is a strong contrast. ⚙️ (F6, 2026-11-07)

### Font
- **K5.10** Coolvetica Bold, heavy, ALL CAPS for primary text; Coolvetica Light, lowercase with a capital first letter, for secondary text. ✅ *"Use Lewis SOP instead"* (D1, 2026-11-07)

### Text: one NeoTextMotion
- **K5.11** All text is NeoTextMotion. No Text+. One NeoTextMotion per text block, never several when one can do the work: mixed weights, the gold keyword and a different size go in its **Character Styling** ranges (4 ranges: colour, size, font per range), not in a second node. ✅ *"don't be creating text + or even multiple neo text motion when one can do the work"* (2026-11-07) (B6, B13, B14)
- **K5.12** Use its built-in looks, not extra nodes: a little **shine** (StShine), **drop shadow** (StShadow) and **glow** (StGlow) on the text itself. ✅ *"All text should use one neo text motion with a bit of shine and dropshadow, and glow, neo text motion has all those elements built in use it"* (2026-11-07). Shine values from [[03-Areas/video-editing/rulebook/rb-b3-main-nodes-and-macros|B3.16]].
- **K5.13** Use its animation types to the full, chosen per moment: word-by-word slide up (Scope = word, PosDir Up, B3.14) for captions and punch lines; letter blur-in for sentences; **Counter** (CtrFrom/CtrTo, prefix/suffix, decimals, thousands separator, digit slide) for every number; Write On, Scramble and Box Reveal where they fit the meaning. ✅ *"it has different types of animation, use that well"*; *"it has a numbers animation now, use that for numbers"* (B10); *"with word by word slide up as we do"* (D3) (2026-11-07)
- **K5.14** Text shine comes from NeoTextMotion's own shine; every other element uses his normal `shine` macro. ✅ *"Use neo text motion to do the shine … but use my normal shine for other elements"* (B7, 2026-11-07)

### Motion
- **K5.15** Every entrance and exit is NeoAnim, including pops: the small-overshoot pop on big shapes is NeoAnim's size with an overshooting curve, not separate Transform keys. ✅ *"Always use neo anim for entrances, it has all the things you need, don't use individual nodes"* (B2); *"Use neo anim it has that feature"* (B11) (2026-11-07). Staggered by 4-5 frames. Rest of the NeoAnim rules: [[03-Areas/video-editing/rulebook/rb-b3-main-nodes-and-macros|B3.6-B3.9]].
- **K5.16** Camera moves on a large canvas animate the board, never the background: the background stays still. Every comp ends in one Transform with a subtle zoom-in that runs through the whole comp, so no moment is static. ✅ *"the background stays a bit still, the at the end of the comp add a transform that zooms in graudally all through out the animation, just subtle zoom in, so no time is static"* (B3, B4, 2026-11-07)
- **K5.17** Zooms and punch-ins only on adjustment clips, never on the A-roll itself. Punch-ins (hard) and zooms (animated, his style) are both allowed. ✅ *"You can do punch ins, but also zoom in is my style, and never do it on the A-roll itself, use adjustment clips always"* (A5, 2026-11-07)
- **K5.18** Spoiler blur is always mosaic blur: labels sit mosaic-blurred until he says them, then sharpen on the word. ✅ *"Always use mosaic blur, for me"* (B5, 2026-11-07)
- **K5.19** Glow is NeoGlow, never Soft Glow. ✅ *"Use neo Glow, not soft glow"* (B9, 2026-11-07). Values: [[03-Areas/video-editing/rulebook/rb-b3-main-nodes-and-macros|B3.30]].
- **K5.20** Desaturate everything except the point; big glowing verdict words in NeoTextMotion; pixel-to-sharp tile entrances; hand-drawn arrows that draw on. ✅ kept: B8, B12, B14, C7 (2026-11-07)

### Structure and pacing
- **K5.21** Hook: claim, a proof on every sentence, then a "later in the video" teaser of later comps sped up under mosaic blur. ✅ *"The later comps would be a video sped up, and mosaic blur on t[he …]"* (A1, 2026-11-07; his note was cut off, read as "on top")
- **K5.22** A roadmap card, then a recurring tracker per part, built once as one macro with inputs, using his comps and nodes. Recurring boards are built once and reused at the same size every return. ✅ *"Make sure you use the right fusion comps, and my nodes, with a premium feel, neo text motion for all texts"* (A2); kept C5, D4, F1, F2 (2026-11-07)
- **K5.23** Visual cover per section to plan against: about 77% in the hook falling to about 55% in the last part, 20-25% in the outro. Hard cuts between A-roll and graphics. Very tight cut: retakes out, almost no pauses over 0.35 s. ✅ kept A3, A4, A6, B1 (2026-11-07)
- **K5.24** Real proof is the backbone: recreated real UI, one real proof per named thing on its word, cursor/typing/clicks on real UI, his own world as proof, a generic "Your Channel" stand-in. Diagrams are few, each with lots of motion. ✅ kept C1-C4, C6, B13 (2026-11-07)
- **K5.25** Mockery as a device stays (C9 kept). ⚠ F8, also kept, proposed dropping the clown-wig mockery: Q-K5.b.
- **K5.26** Light sound design: his SFX library on the big moments only, low music bed. ✅ kept E1 (2026-11-07)

### Premium (Samuel's list, 2026-11-07)
- **K5.27** NeoLightSweep Pro on every box for the glossy feel (static sheen, values in [[03-Areas/video-editing/rulebook/rb-b3-main-nodes-and-macros|B3.29]]). ✅ *"Neolightsweep on any box, just to give that glossy feel"*
- **K5.28** Neo Bevel when needed, sparingly, so the PC is not overworked. ✅ *"Neo bevel when needed, use sparringly so it doesn't overwork the PC"* ⚠ B3.42-B3.43 and B2.24 say NeoBevel stays off in every comp: Q-K5.a.
- **K5.29** Shines only when needed, not on every element. ✅ *"Shines, only when needed, not on every element"*
- **K5.30** Glass once in a while where needed (his `Glass effect` macro). ✅ *"Glass could be also use once a while where needed"*
- **K5.31** Icons are solid (filled), never outline. ✅ *"Icons should be solid"*
- **K5.32** Good design: hierarchy, alignment, spacing, contrast, and creative ideas inside his styles. ✅ *"Be a good designer, add design aesthetics, use good design principles * Be creative with your designs"*

### Nodes
- **K5.33** Use his tools, plugins and macros before building anything: NeoTextMotion, NeoAnim, NeoGlow above all; then the `Neo folder` (Light Sweep Pro, Bevel, Highlighter Pro, Inner Shadow …) and `My macros` (Box main, Down fade, shine, Glass effect, Arrowline, Number Counter, Screen Focus Emphasis …). Never build what a plugin already does. ✅ *"don't forget to use my tools plugins and macros espectially neo text motion, neo anim, neo glow, don't just build everything when there is a plugin for it"* (2026-11-07)
- **K5.34** Nodes arranged vertically, his way: [[03-Areas/video-editing/rulebook/rb-b4-fusion-node-layout|B4]]. ✅ *"make sure that the nodes are arranged vertically the way I do it"* (2026-11-07)

## Never (strict)
- **K5.35** Never FX on the A-roll (reference used it twice). ❌ B15 rejected (2026-11-07)
- **K5.36** Never a light page: one near-black background for every animation, right or wrong. ❌ C8 rejected (2026-11-07); SOP.
- **K5.37** Never Text+, never Soft Glow, never a zoom keyed on the A-roll clip itself. ❌ (K5.11, K5.17, K5.19)

## Questions for Samuel
- **Q-K5.a** Neo Bevel. The rulebook says off in every comp (B3.43, *"just disable all the neo bevel nodes in all the visuals and comps"*, 2026-10-23). Now: *"Neo bevel when needed, use sparringly"*. → Options: (1) for Lewis, on for 1-2 hero elements per comp at most, off everywhere else; (2) keep it off as B3.43 says. My pick: (1).
- **Q-K5.b** Mockery. You kept C9 (mockery as a device) and F8, which proposed dropping the clown wig. → Options: (1) keep mockery, but in the black/gold look, no clown wig; (2) keep the clown wig too. My pick: (1).
- **Q-K5.c** Rate for Lewis's videos. Needs-input (K1.2).

## Sources
Samuel's verdicts on [[04-Projects/routerise-lewis-art-of-winning-youtube|the Art of Winning job]]'s reference study (artifact `verdicts` collection, 2026-11-07) and his message of 2026-11-07; Lewis's Long-Form SOP and Slack note (job `Docs\`). NeoTextMotion's controls read from his installed fuse (2026-11-07).

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
