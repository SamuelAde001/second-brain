---
type: project
area: called-to-edit
status: active
updated: 2026-10-22
source: interview
tags: [called-to-edit, webinar, whiteboard, canva]
---

# Called to Edit webinar: the Canva whiteboard

Part of [[04-Projects/called-to-edit-webinar-and-academy|Called to Edit webinar → Academy]] · [[03-Areas/called-to-edit/called-to-edit|Called to Edit]]. Content source: the book `_attachments/called-to-edit-book/` (12 chapters, his reading order) and [[04-Projects/called-to-edit-webinar-teachings|Teachings]].

## The ask (Samuel, 2026-10-21, night)

Put the whole webinar on **one Canva whiteboard** in his branding. It must feel like real teaching: steps flowing into each other, diagrams, Canva icons and assets, arrows, lines, icons of people and clients. He starts on one side and zooms and scrolls through it while teaching; each zoom shows one part. Every major step, quote and emphasis is on it. **Lists are covered with sticky notes** he removes as he teaches. **Demo stops are marked**: there he opens Chrome and shows it live, then comes back. Demos he named: his outreach email, his Loom account, his old Twitter posts, his portfolio, finding clients on YouTube and Instagram. His pictures and video samples go on it; multiple photos when he tells his story; screenshots of his tweets. *"Show more and not tell."*

Corrections the same night:
- *"I said use the Canva white board, not a presentation slide"* (after a one-frame import test he saw as a Presentation).
- *"You are just putting sliders, I need like proper mapping"* (after slide-style 16:9 frames in rows went onto the whiteboard). → Build as **mind maps**: a chapter hub, branches, chained steps with arrows, diagrams, reveal stickies. No slide frames.

His choices: Canva **in his Chrome** (he keeps the window visible); old story photos come from **Google Photos in Chrome** (picture board for his OK first, then download).

## How it is built

- Source: `_attachments/called-to-edit-whiteboard/source/`. Map style: `maplib.py` (nodes, hub, topic pills, leaves, chips, demo badges, polaroid photo slots, connectors drawn by script). One file per chapter: `mapNN.py`. Build: `python build_map.py map04` → `out/<name>.svg` (text outlined, his exact fonts), preview PNG on midnight, reveal positions JSON.
- Reveal stickies: `covers.py` makes one champagne SVG per hidden part from the positions JSON (written for the old rows; point it at the map JSONs).
- Into Canva: a hidden file input + synthetic drop onto the whiteboard, then the Position panel's W/X/Y set by script (`claudePlace` in the page). One placement at a time; wait for the new element before setting values; long jobs run as a background promise and are polled (the JS call times out at 45 s).
- Canva design: "Called to Edit Webinar Whiteboard" in his account, https://www.canva.com/design/DAHYrXl8-WE/Vy9aSwga4gVcdXINoOc29g/edit. The test Presentation "test.pdf" (DAHYrWMI1dE) can be deleted.
- Old slide version (rejected, kept as content reference): `rows_a..d.py`, `build.py`.

## RESUME (2026-10-22, after Samuel's yes to the map style)

Samuel: *"Yes, this map style is right. Map every chapter like this, clear the old slide rows and put it all on the Canva whiteboard."*

- Done:
  - All 13 maps are built: `map00.py` (opening) to `map12.py` (next steps, Community, questions).
  - Each map is a hub column on the left with a contents list, branches in a two-column snake, and a gold road ending in a "Next chapter" pointer.
  - Layout is measured in the page (`maplib.assemble`), so nothing overlaps.
  - The old slide rows are deleted from the whiteboard.
  - Every map is placed on the Canva whiteboard in one column at x=0, 900 px apart. Positions: `out/placement.json` and `out/canva-plan.json`.
  - 120 reveal stickies are placed from `out/covers.json`.
- Canva refuses SVGs over 3 MB. `split_map.py` cuts big maps into bands at empty rows (map01, map08 and map09 are in bands; `out/<map>-bands.json`).
- Demo badges are on the maps:
  - 6.5: YouTube download (optional)
  - 8.4: Twitter
  - 8.5: portfolio
  - 9.4: YouTube/IG search
  - 9.8: outreach email
  - 9.10: Loom
- Photo and screenshot slots are dashed polaroids. Fill them via `source/photos.json`, then rebuild and replace that map.
- Also done: a locked Midnight `#071226` backdrop (6400 px wide, `out/backdrop.svg`) sits behind everything, and the design is renamed "Called to Edit Webinar Whiteboard".
- Next:
  - Samuel walks through it.
  - Google Photos picture board for the story photos.
  - His screenshots.
  - Canva people and client illustrations on top.

## Earlier RESUME (2026-10-21 ~23:40)

- Done: content for all 12 chapters written (slide version); map style built and proven on **Chapter 4** (`map04.py`, preview `_attachments/called-to-edit-whiteboard/map-style-preview-ch4.png`).
- Waiting: Samuel's yes on the Chapter 4 map style.
- Next: map the other chapters in the same style (opening + 1-3, 5-12, close and Community pitch), with demo badges at 8 (Twitter, portfolio) and 9 (YouTube/Instagram search, outreach email, Loom), photo slots as polaroids on the story timeline; chapters joined by a road; clear the Canva board; place maps; covers; whiteboard background Midnight; rename the design "Called to Edit Webinar Whiteboard".
- Then: Google Photos picture board for the story (soldier 2020, Minecraft channel, first laptop, church, mentor, first client DM, going full time, Route Rise) and his screenshots (tweets that landed clients, first client DM, outreach email, portfolio, testimonial, mentor's channel views, value-first before/after, a working time-lapse). Canva illustrations of people/clients added natively on top.

## Native Canva elements (2026-10-22)

Samuel, after seeing the board: *"I like the design, but I don't like that the text and all the visual elements are pregenerated, cause I may want to highight a text, or tweek something or re arrange … Also if I zoom in too much the quality drops … I want you to do this same design but with existing canva tools so I can edit the white board and zoom in the way I want."*

- The image version stays on the board until the native one replaces it.
- His photo picks from the story board (15 photos) are copied as web copies to `source/kit/photos/` (gitignored, made from his footage folder, originals untouched); `source/photos.json` maps them. Chapter 1 and 12 map sources already use them.
- Routes weighed (Brand manager):
  1. **Canva app in development mode (recommended).** A small private Canva app run from this PC adds real text boxes, shapes, lines and his photos at exact positions, in his fonts if Canva has them. He creates the app once in Canva's developer portal and accepts its terms himself.
  2. **PDF import, then copy into the whiteboard.** Faster, but the earlier test swapped the fonts, and arrows and boxes come in as loose pieces.
- Waiting on his choice.

### RESUME checkpoint (2026-10-22, night)

Samuel: *"The arrows, the texts, the boxes, the whole visual elements must be native canav elements except medias"*. Then: *"Please do check the wording and phrasing, and the overall design, let it feel like me, let it not feel like it's AI that created it, let it be something I can flow with and actually teach as I go, let it feel natural and well detailed the way I would say it from the words"*. Then: *"ensure everything is done perfectly and ready for the webinar, I am going to bed"*.

- Route found (no Canva app needed): Canva's own clipboard format. `source/native.py` lays each map out in Chrome with DM Sans / DM Serif Display (Canva's fonts, same metrics), reads every box, text, icon, arrow and photo back, and writes Canva clipboard JSON (`out/native/<map>.json`). Pasted with a real Ctrl+V on the whiteboard. Photos are his uploads (`source/canva_media.json`).
- Canva format notes: text wraps only with `"h":"A"` and an empty `"b"` (line cache); connectors may not sit in, or point into, a group (save fails 10–30 s later), so node groups carry the anchor; a Midnight panel behind each chapter makes the paste's box exact (`out/native/plan.json`: native column at x 6500–12900, chapters stacked 900 apart).
- Fonts: Gloock and Plus Jakarta Sans need Canva Pro, so the native board uses DM Serif Display and DM Sans. He can swap later with "Change all" if he starts Pro.
- Done: wording pass on all 13 `mapNN.py` in his voice from [[04-Projects/called-to-edit-webinar-teachings-raw|raw voice notes]]; native regenerated, 13 chapters pasted and each panel locked. The old image column was not deleted: that waits on his yes (below).

## Native board done (2026-10-22)

- **With covers:** "Called to Edit Webinar Whiteboard" (Canva design DAHYrXl8-WE; in Canva Trash since 2026-10-22, see One board, five columns). All 13 chapters in the right-hand column as native Canva text, boxes, arrows and icons; only photos are media. Each chapter's Midnight panel is locked, everything on it stays editable. 120 reveal stickies on top.
- **Without covers:** "Called to Edit Webinar Whiteboard (no covers)" (DAHYsWQt71Y). Samuel, 2026-10-22: *"Once you are done, create a copy of everything exactly the way it is but without the Sticky notes covers so I can check everything, and see if I prefer that version without the sticky note covers"*. Made with Canva's Make a copy, then all 120 covers deleted one by one. Nothing else changed.
- Sweep fixes: inline "?" stickies under 80 px lost their author line and got padding (`sticky_el` in `native.py`; Canva drops the whole paste when a sticky's text box goes negative). Chapter 11's six "Editor" chips: the icon sat on the word, so the word is now its own box beside the icon (`map11.py`).
- Swapping covers one at a time in Canva: shift-clicking inside the current selection's box is ignored, so delete one sticky at a time.
- ~~Waiting on Samuel's yes to delete (both boards): the old image column, the build test cluster about 100,000 px above the board, the test Presentation (DAHYrWMI1dE).~~ Done 2026-10-22, see below.
- **Empty slots for his material (13):** Ch 1: his Minecraft YouTube channel, one of his first editing tweets. Ch 6: the original edit and his recreation (clips). Ch 8: phone recording him at work or a timeline post, two posts that landed clients, his Framer portfolio site. Ch 9: a working time-lapse, a value-first before and after (clips). Ch 11: views on his mentor's channel, a client testimonial.
- Fonts stay DM Serif Display / DM Sans until he has Canva Pro (then "Change all" to Gloock / Plus Jakarta Sans).

## One board, five columns (2026-10-22)

Samuel: *"So, delete every other thing except the one without the cover notes, and zoom everything out and increase them in the same way, cause, I noticed if I put it on fullscreen I can't zoom in fully"*.

- **The only board now:** "Called to Edit Webinar Whiteboard (no covers)", https://www.canva.com/design/DAHYsWQt71Y/EdMBKz4SuXqjqRLLxZN-1A/edit. Overview: `_attachments/called-to-edit-whiteboard/board-five-columns.jpg`.
- **Deleted:** the board with covers (DAHYrXl8-WE) and the test Presentation (DAHYrWMI1dE) are in Canva Trash, restorable for 30 days. On the surviving board: the old image column, its backdrop and the build test cluster.
- **Why fullscreen couldn't zoom in:** "Present full screen" opens at fit (the whole board on screen) and zooms in at most about 10× from there. One column of 13 chapters is about 75,000 px tall and 6,400 px wide, so fit was tiny: the max was about 7.6% of real size with the clutter, 16% without. Scaling everything up by the same amount changes nothing, because fit and the 10× cap scale with it. Only the board's shape counts: the closer to the screen's shape, the deeper the zoom.
- **Fix:** the 13 chapters are now in five columns, read top to bottom, then left to right: ch 0–1 · 2–5 · 6–8 · 9 · 10–12. Columns are 6,400 px wide, touching, tops aligned (checked to 0 px); every chapter panel is locked again; nothing inside a chapter moved relative to its panel. Fullscreen now opens at 6.4% and zooms to 63.5% of real size, so one branch fills about half the screen. The editor itself still zooms to 500%.
- Moving a multi-selection in Canva: the Position panel shows "--" and arrow keys don't nudge. Drag from inside the block (dragging its edge resizes the whole block), then zoom to ~20% and ~130% at the junction and drag a few px; Canva snaps the edge exactly.

## White version (2026-10-23)

Samuel: *"I want you to turn my recreate the canva board to white theme, I want to see how it looks, so no blue dark background over everything, remove that, and let all the elements sit on the native white board, change the colors of the elements to be visible on the whiteboard background, make sure there are spaces around each section in case I want to scribble something for them"*; *"The design is okay as it is, just do this"*.

- **New board:** "Called to Edit Webinar Whiteboard (white)" (Canva design DAHY0B1pmtg), https://www.canva.com/design/DAHY0B1pmtg/544bxD08zceSLdFwVik-IQ/edit. The dark no-covers board is untouched, so he can compare. Overview: `_attachments/called-to-edit-whiteboard/board-white.jpg`.
- Built from the map sources with `C2E_THEME=white python native.py map00 … map12` → `out/native-white/` (plus `plan.json`). No chapter panels and no reveal covers. Same five columns, with 1,500 px of white space between chapters. Inside each chapter there is more room: 600 px between the two branch columns and 450 px between rows. Any edits he made by hand on the dark board are not in the white one.
- Colours on white:
  - Navy hub, navy cards and gold pills stay as they are.
  - Gold text becomes bronze (#8A5E17).
  - The slate cards become light grey-blue (#E9EEF6).
  - Gold lines become deep gold (#B8821F); grey lines become #7D8BA3.
  - Anything sitting on a navy box keeps its dark-theme colours.
- Logos: the light-background Called to Edit and Community logos are uploaded to his Canva (`logo-light` MAHY0C9SWTQ, `community-light` MAHY0CL5mno in `source/canva_media.json`).
- Canva setting: "Open links in Desktop App" was on, so every Canva link hung on "Redirecting…". It was turned off on Samuel's yes (2026-10-23).
- Pasting a chapter right after a file upload, or straight after a big paste, sometimes doesn't take. Check that the clipboard holds the payload, then paste again.
