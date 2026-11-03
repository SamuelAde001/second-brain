---
type: sop
area: video-editing
status: active
updated: 2026-11-03
source: manual
tags: [rulebook, scripts]
---

# Drafting brief: rulebook sections

Samuel Adebayo edits talking-head YouTube videos in DaVinci Resolve + Fusion for the agency Route Rise (end clients: Alex of Frontal, Gamma, more later). We are writing his editing rulebook: the number-one rule for every Route Rise edit, for him and for every Claude agent. He will review and approve it section by section. It must be easy for him to read and edit in Obsidian, and cheap for an agent to read (an agent opens only the sections its step needs).

Ten research helpers already pulled ~2,900 evidence lines from every source (his chat messages, 359 timeline markers, the Brain's house notes, edit grammar measured from his finals, the creative director's breakdowns and corrections, every job note, the Editor's memory). The evidence for each section is in `sec/<CODE>.md` in this folder; every line starts with its source group, e.g. `[T4]` = his own messages, `[J]` = his timeline markers and job folders, `[N1]` house rules, `[N2]` edit grammar from his finals, `[N3]` SOPs, `[N4]` job notes, `[N5]` Editor memory. `sec/CONFLICTS.md` lists disagreements (grep it for your codes). `sec/IMAGE_CANDIDATES.md` lists images. `taxonomy.md` lists every code.

## Your job

For each section code in your task, read its whole `sec/<CODE>.md`, the CONFLICTS lines for it, and write ONE section note. Deduplicate hard: ten sources say the same thing in different words; one rule each. Lose nothing that matters: every distinct correction Samuel gave must survive as a rule (or be marked superseded).

### Which source wins
1. Samuel's own words (KIND ruled / scolded / liked) — the LATEST date wins when he changed his mind. Repeated corrections are the most important rules; mark them.
2. The creative director (KIND creative-director). Samuel's order (2026-10-22): his corrections and markers > creative director standard > older house notes > client brand kit.
3. What is in his approved finals (approved-final).
4. Route Rise rules, then working methods, then inferred.
If two of his own rulings conflict and the later one does not clearly replace the earlier, do not choose: write it as an open question.

### Client-specific values
Fonts, colours, corner shape (Alex square + corner brackets, Gamma rounded), logos and brand-kit rules go ONLY in the K2/K3 client notes. In every other section, write the rule client-neutral and point to the overlay, e.g. "accent colour (client overlay)".

### Scope of a section note
Rules about the craft and the process. Exact numbers stay (frames, seconds, dB, node settings, script paths). Long technical how-tos (API quirks, script internals) do NOT go in: link the existing Brain note instead ([[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]], etc.), with one line on when to open it.

## File format (follow exactly)

Path: `C:\Users\repzy\Desktop\My Second brain\03-Areas\video-editing\rulebook\rb-<code lowercase>-<kebab-name>.md` (e.g. `rb-c6-highlighting.md`). Write with the Write tool (not the shell: backslashes break).

```
---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: C6
---

# C6 · Highlighting and brightness areas

> **Read when:** <which job step / which agent needs this>. **Client values:** <overlay link or "none">. **Status:** draft, not yet approved by Samuel.

## Rules
### <subheading>
- **C6.1** <rule, one or two lines, imperative> ✅ *"<his words, ≤20 words>"* (2026-10-25)
- **C6.2** <rule> 🎬
...

## Never
- **C6.20** <banned thing> ❌ *"<his words>"* (date)

## Pictures
- ![[_attachments/rulebook/<file>.jpg|360]] ✅/❌ <what it shows, video> 

## Questions for Samuel
- **Q-C6.a** <the conflict or gap, both sides with dates> → Options: (1) … (2) … My pick: …

## Sources
One line: which Brain notes this section replaces or draws on, as wikilinks with full paths and aliases.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
```

Badges after each rule: ✅ Samuel said it · 🔁 he said it more than once (add the count) · 🎬 in his approved finals · 🎯 creative director · 🏢 Route Rise · ⚙️ our working method · 💡 inferred, needs his yes.

Number rules continuously through the note (C6.1, C6.2 …) with subheadings grouping them. Keep a note under ~220 lines; if a section is bigger, keep the rules terse rather than splitting. Plain English, short sentences, no filler. Samuel must be able to read it on his own.

Pictures: pick at most 4 per section from `sec/IMAGE_CANDIDATES.md` (only ones that exist; check with Glob). For each one you use, append a line to `img_<your group>.txt` in this folder: `<full source path> -> <target file name>.jpg`. Use target names `<code>-<short-slug>.jpg`. A script will downscale and copy them into `_attachments/rulebook/`. If no candidate fits, write `- (no picture yet: <what picture would help>)`.

## Return

Max 120 words: the files written, rules per section, the number of open questions, the one question per section that matters most.


Back to [[03-Areas/video-editing/scripts/rulebook/README|Rulebook scripts]]
