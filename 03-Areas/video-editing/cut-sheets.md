---
type: knowledge
area: video-editing
status: needs-input
source: claude-export
updated: 2026-09-20
tags: [cut-sheets, pre-production]
---

# Cut sheets — pre-production and visual-direction planning

A cut sheet is Samuel's shot-by-shot visual plan for a video, built before or alongside the cut. Definition in the source's own words (the Routerise "$0–10K Profit" doc):

> "Shot-by-shot visual plan for Sections 27–44 of the Routerise dropshipping video, built against the client's actual asset folder. Every line of VO has a picture assigned, plus text-on-screen / zoom / list / cut-point callouts."

It's delivered as a standalone HTML artifact (published via a `claude.ai/code/artifact/<id>` link) with a local copy kept alongside the project's assets — e.g. `Assets/$0-10K Cut Sheet - 21m39 to End.html`, `New folder/AI Ecom Brand - Cut Sheet.html`, `Docs/Cut Sheet - Visual Direction.html`.

**Two uses, seen across the three examples:** (1) forward planning — map every VO line to a picture before touching the timeline ($0–10K, AI-ecom); (2) a **visual-direction pass** on a video already cut — audit it against an approved reference style and flag what's wrong (Claude Dropshipping).

**A caveat on the sources.** All three source documents are companion/verification notes *about* a cut sheet built as a separate HTML file, and none of those HTML files are among the sources. They record the underlying asset facts, conflicts and to-do lists behind each sheet, not its beat-by-beat content.

## The fields

From the AI-ecom doc: "every VO line gets a picture, plus text-on-screen / zoom / list-build / cut-back-to-A-roll callouts." So each beat carries:

- **Picture** — plain prose describing exactly what's on screen, shot by shot.
- **On-screen text** — the literal text or graphic.
- **Motion** — expressed as a zoom or a list-build.
- **Cut-back-to-A-roll callout** — an explicit instruction for when to return to A-roll. The house-style footer on the $0–10K sheet makes this a standing requirement: "explicit calls for when to return to A-roll".

`status: needs-input` on this note is mostly about this section: the field list is reconstructed from a one-line description in a companion note, not from a cut sheet itself. Samuel can confirm or correct it in a minute; until then it should not be treated as the definitive schema.

## VO-to-beat timing is keyed to the subtitle file, not the raw footage

From the AI-ecom cut-sheet doc: **"`Subtitle 1updated.srt` is the edit timeline — 1,329 cues, ends 33:56. All cut-sheet timecodes key to this file."** The raw client-delivered MP4 (45:28, camera and screen record laid side by side in one letterboxed frame) is explicitly flagged as *not* mapping to that SRT. So every beat's timestamp is the SRT cue time, not a timecode from any underlying source video — those get their own separate "key marks" when referenced for a specific shot.

## The three examples

### 1. Routerise "$0–10K Profit" — back-half cut sheet (21:39 → 33:46)

Covers Sections 27–44 (beats numbered by script section). "Verified asset facts" locks down screen-recording specs before cutting begins, e.g. both client screen records are 3456×2234 @ 60fps macOS retina captures — so Samuel (on Windows) records his own browser inserts in Chrome F11 full screen "so no window chrome betrays the OS." Source clips get internal key timestamps, e.g. `arcads screen.mp4` (7:42): "0:10–0:55 actor-spec prompt · 1:25 generation widget · 1:40 'Authorization complete' OAuth page…"

**Open conflicts** flagged before cutting: the client says "Higgsfield" on camera at ~25:32 but all available footage is Arcads — resolved as "crop/blur every Arcads string; no tool UI on the word itself." A **still-needed-from-client** list is ranked (real "check the campaign" reply, Ads Manager with all columns on, the generated morning report, community screen capture, which ad downloader, end-card videos).

**Editor's house style footer:** "no complex Fusion work (deadline-constrained); explicit calls for when to return to A-roll; real-world B-roll sourced from YouTube and TikTok only — no stock libraries."

### 2. "How to Start an AI Ecommerce Brand in 2026" — full cut sheet (00:00 → 33:56)

205 timestamped beats, 85 verified links. **Script-vs-VO conflicts** — the rule is to cut to what's spoken, not what's written: written script says a $50/day ad budget, VO says "$50–$100/day"; written script says paste a custom connector URL, VO says browse connectors and search "Facebook Ads." A **blur list** covers PII visible in screen recordings (email/phone, credit card, business address, store URL).

**Structural spine** — compound clips built once early and reused verbatim later, "what makes the video feel authored": an "identical-stores 3×3 grid" (00:08 → reused 33:05), a "Reddit quote block" appearing four times (06:44 → 07:50 → 25:26 → 32:47, shortest last). **No-B-roll zones** are called out deliberately (e.g. 22:55–23:40, the whole mid-CTA: "one insert only, single slow push in underneath").

### 3. "Claude Dropshipping Guide 2026" — visual direction pass (00:00 → 27:46)

Not built from zero: a **gap-analysis of an already-cut video** (`cut footage.mp4`, 641 A-roll cuts) against an approved reference cut of the same creator's style (the AI Ecommerce Brand video above). Deliverable: 63 beats plus a 24-item shot list.

It defines a **16-component reference style vocabulary** to check the cut against — chapter chip, keyword caption (white caps, one word cyan), additive equation, pill chain, side-panel card, calculation card, full-frame comparison card, ticked recap chips, screen-rec with circular webcam PIP, progressive cyan highlight, white quote callout, 9:16 clip with mirrored blur sides, ad-script layout, thought pill over B-roll, big number callout, community plug block. Palette: cyan `#35C6E8`, green `#3ED07E`, red `#E5473C`, teal panel `#0C3A47 → #061E27`, white.

**Seven structural gaps** found against that vocabulary: no circular A-roll PIP on any screen recording; nothing punched in (Claude output and Google Docs sit at native scale in a 4K frame, unreadable); frames held too long (one stretch of 108s on a motionless doc page), and others.

**Method worth reusing:** frames sampled every 2s from both videos with ffmpeg, tiled into 6×4 contact sheets and read visually; the reference video's own subtitle track used to map its visual choices to its spoken lines.

## A recurring pattern: beats collapse into recording sessions

Across the sheets, the shot list is organised by **physical shoot**, not by beat order — every screen capture in one sitting, every desk take in another, phone captures last once the edit shows which cutaways survive. Capture specs are written into the sheet itself (terminal font bumped two sizes, notifications off, bookmarks bar hidden, 1440p+ at 60fps; clap at the top of every take for waveform sync).

## `routerise-alex-START-HERE.md` — checked, not folded in here

A condensed project-briefing and house-style recap ("Read this first when starting a new video for Alex") covering delivery spec, the ten structural rules, track layout, the PIP system, the plugin list, Fusion build conventions and Resolve-stability warnings. No cut-sheet process content. Its facts are already in [[routerise-house-style]] and [[fusion-node-system]], and its project-context table is quoted in [[clients/routerise]].

## needs-input

- Confirm the beat field list above — it is reconstructed from a single descriptive line, not from an actual cut sheet.
- The beat-by-beat HTML content of the three cut sheets (`$0-10K Cut Sheet - 21m39 to End.html`, `AI Ecom Brand - Cut Sheet.html`, `Cut Sheet - Visual Direction.html`) is not among the sources — only the companion notes.
- Which ad downloader to use for the $0–10K video (§29) — listed as still needed from the client, unresolved.

Back to [[03-Areas/video-editing/_index|Video editing]]
