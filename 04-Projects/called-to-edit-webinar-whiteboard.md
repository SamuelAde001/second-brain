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
- Canva design: "Untitled design - Whiteboard" in his account, https://www.canva.com/design/DAHYrXl8-WE/Vy9aSwga4gVcdXINoOc29g/edit. It currently holds the **rejected slide rows** (rows 0-9): delete them before placing maps. The test Presentation "test.pdf" (DAHYrWMI1dE) can be deleted.
- Old slide version (rejected, kept as content reference): `rows_a..d.py`, `build.py`.

## RESUME (2026-10-21 ~23:40)

- Done: content for all 12 chapters written (slide version); map style built and proven on **Chapter 4** (`map04.py`, preview `_attachments/called-to-edit-whiteboard/map-style-preview-ch4.png`).
- Waiting: Samuel's yes on the Chapter 4 map style.
- Next: map the other chapters in the same style (opening + 1-3, 5-12, close and Community pitch), with demo badges at 8 (Twitter, portfolio) and 9 (YouTube/Instagram search, outreach email, Loom), photo slots as polaroids on the story timeline; chapters joined by a road; clear the Canva board; place maps; covers; whiteboard background Midnight; rename the design "Called to Edit Webinar Whiteboard".
- Then: Google Photos picture board for the story (soldier 2020, Minecraft channel, first laptop, church, mentor, first client DM, going full time, Route Rise) and his screenshots (tweets that landed clients, first client DM, outreach email, portfolio, testimonial, mentor's channel views, value-first before/after, a working time-lapse). Canva illustrations of people/clients added natively on top.
