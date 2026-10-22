---
type: project
area: called-to-edit
status: active
updated: 2026-10-21
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
- In progress: wording pass on all 13 `mapNN.py` in his voice from [[04-Projects/called-to-edit-webinar-teachings-raw|raw voice notes]]; then regenerate native, paste the 13 chapters, lock each panel, delete the old image column, commit.
