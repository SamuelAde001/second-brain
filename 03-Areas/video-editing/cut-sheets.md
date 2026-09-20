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

**Two uses, seen across the four examples:** (1) forward planning — map every VO line to a picture before touching the timeline (the $0–10K, AI-ecom, and Butler reel examples below); (2) a **visual-direction pass** on a video that's already been cut — audit it against an approved reference style and flag what's wrong (the Claude Dropshipping example).

**A caveat on the sources for this note:** three of the four source documents (the $0–10K, AI-ecom and dropshipping ones) are companion/verification notes *about* a cut sheet built as a separate HTML file — none of those HTML files are among the sources. They record the underlying asset facts, conflicts and to-do lists behind the sheet, not its beat-by-beat content. Only the **Butler reel** source is the actual, complete cut-sheet document, and it's the clearest evidence for the field-level structure below.

## The beat, field by field (from the Butler reel cut sheet)

Each beat carries: a number and its place in the line ("01 — list item 1 of 3"), the VO line quoted verbatim, capability chips (e.g. `Screen record` `Desktop` `Ref clip`), then five description fields:

- **The picture** — plain prose describing exactly what's on screen, shot by shot. Example (beat 1): *"Your own terminal, full frame. You type `/mcp`, hit enter, and the connected-server list draws down the screen... Hard cut to your actual desktop: those same five app icons in the dock, and your cursor clicks Gmail so the real inbox opens."*
- **On screen** — the literal on-screen text/graphic, quoted or spelled out as a chip/card (e.g. a chip row `GMAIL` `CALENDAR` `DRIVE` `NOTION` `TICKTICK`; a colour-coded card set `ALLOW` (green) `ASK` (amber) `DENY` (red) landing on the word "rules").
- **Motion** — camera/graphic movement in specific, executable terms, e.g. *"Static split until the action fires, then the screen half punches in 10% on the calendar row at the exact frame the event moves."*
- **Capture** — the literal recording setup: tool, resolution, frame rate, device. E.g. *"OBS Studio, display capture, 2560×1440 or higher at 60fps... Bump the terminal font two sizes before you record."* Or for a hero take: *"Pocket 4 for the face, DJI Mic Mini for the voice, OBS for the screen, all rolling at once. Clap once at the top of the take so you've got a sync point for the waveforms in Resolve."*
- **Source** — where the footage comes from, marked by a dot colour: **blue = self-shot**, **amber = third-party reference clip** (handle + URL, credited). Rule attached to third-party clips: keep each under ~2 seconds, keep the creator's handle visible in frame, never use a downloader that burns its own watermark in.

The long-form Routerise cut sheets use the same core fields under slightly different names. From the AI-ecom doc: "every VO line gets a picture, plus text-on-screen / zoom / list-build / cut-back-to-A-roll callouts." So: picture, on-screen text, motion (expressed as a zoom or a list-build), and an explicit **cut-back-to-A-roll callout** — a field the short-form Butler reel doesn't need, since it has no A-roll to return to.

## VO-to-beat timing is keyed to the subtitle file, not the raw footage

From the AI-ecom cut-sheet doc: **"`Subtitle 1updated.srt` is the edit timeline — 1,329 cues, ends 33:56. All cut-sheet timecodes key to this file."** The raw client-delivered MP4 (45:28, camera and screen record laid side by side in one letterboxed frame) is explicitly flagged as *not* mapping to that SRT. So every beat's timestamp is the SRT cue time, not a timecode from any of the underlying source videos — those get their own separate timestamps ("key marks") when referenced for a specific shot.

## The four examples

### 1. Routerise "$0–10K Profit" — back-half cut sheet (21:39 → 33:46)

Covers Sections 27–44 (beats numbered by script section). "Verified asset facts" locks down screen-recording specs before cutting begins, e.g.: both client screen records are 3456×2234 @ 60fps macOS retina captures — so Samuel (on Windows) records his own browser inserts in Chrome F11 full screen "so no window chrome betrays the OS." Source clips get marked with internal key timestamps, e.g. `arcads screen.mp4` (7:42): "0:10–0:55 actor-spec prompt · 1:25 generation widget · 1:40 'Authorization complete' OAuth page..."

**Open conflicts** flagged before cutting: the client says "Higgsfield" on camera at ~25:32 but all available footage is Arcads — resolved as "crop/blur every Arcads string; no tool UI on the word itself." A **still-needed-from-client** list is ranked (real "check the campaign" reply, Ads Manager with all columns on, the generated morning report, community screen capture, which ad downloader, end-card videos). Editor's house style footer: "no complex Fusion work (deadline-constrained); explicit calls for when to return to A-roll; real-world B-roll sourced from YouTube and TikTok only — no stock libraries."

### 2. "How to Start an AI Ecommerce Brand in 2026" — full cut sheet (00:00 → 33:56)

205 timestamped beats, 85 verified links. **Script-vs-VO conflicts** — the rule is to cut to what's spoken, not what's written: written script says a $50/day ad budget, VO says "$50–$100/day"; written script says paste a custom connector URL, VO says browse connectors and search "Facebook Ads." A **blur list** covers PII visible in screen recordings (email/phone, credit card, business address, store URL).

**Structural spine** — compound clips built once early and reused verbatim later, "what makes the video feel authored": e.g. an "identical-stores 3×3 grid" (00:08 → reused 33:05), a "Reddit quote block" that appears four times (06:44 → 07:50 → 25:26 → 32:47, shortest last). **No-B-roll zones** are called out deliberately (e.g. 22:55–23:40, the whole mid-CTA: "one insert only, single slow push in underneath").

### 3. "Claude Dropshipping Guide 2026" — visual direction pass (00:00 → 27:46)

A different kind of cut sheet: not built from zero, but a **gap-analysis of an already-cut video** (`cut footage.mp4`, 641 A-roll cuts) against an approved reference cut of the same creator's style (the AI Ecommerce Brand 2026 video above). Deliverable: 63 beats plus a 24-item shot list.

It defines a **16-component reference style vocabulary** to check the cut against — chapter chip, keyword caption (white caps, one word cyan), additive equation, pill chain, side-panel card, calculation card, full-frame comparison card, ticked recap chips, screen-rec with circular webcam PIP, progressive cyan highlight, white quote callout, 9:16 clip with mirrored blur sides, ad-script layout, thought pill over B-roll, big number callout, community plug block. Palette: cyan `#35C6E8`, green `#3ED07E`, red `#E5473C`, teal panel `#0C3A47 → #061E27`, white.

**Seven structural gaps** found against that vocabulary, e.g.: no circular A-roll PIP on any screen recording; nothing punched in (Claude output and Google Docs sit at native scale in a 4K frame, unreadable); frames held too long (one stretch of 108s on a motionless doc page). **Method:** frames sampled every 2s from both videos with ffmpeg, tiled into 6×4 contact sheets and read visually; the reference's own subtitle track was used to map its visual choices to its spoken lines.

### 4. Butler reel cut sheet — "Build Your Own AI Butler" (Comfort Cuts project)

Vertical short-form (IG Reel / TikTok), 8 beats, 7 of 8 self-shot, 4 optional third-party cutaways. Confirmed against the file: it covers MCP app access (beat 1, `/mcp` listing Gmail/Calendar/Drive/Notion/TickTick), long-term memory (beat 2, a `.md` memory file plus a cold-chat recall test), permission rules (beat 3, allow/ask/deny), ElevenLabs voice (beat 4), the hero split-screen take of a spoken command executing (beat 5), running through Claude Code (beat 6, typing `claude`, the startup banner, tool calls streaming), the no-code objection handled (beat 7), and the CTA "Comment 'BUTLER'" (beat 8).

**Real visuals only, confirmed by the file's own standfirst:** *"Everything here is a real screen, a real file, or a real post — nothing is stock, and nothing is an abstract 'AI brain' graphic."*

**Accent colour, confirmed unresolved by the file:** *"Accent colour isn't set for this video... Suggested here: a cool blue-cyan, so the graphics sit inside the terminal palette rather than fighting it."* Not a decision — a suggestion pending Samuel's input.

**Also flagged, unresolved:** *"The script starts mid-list. Beats 1–3 ('Access to your apps…', 'Long-term memory.', 'And clear rules…') read as items in a three-part list whose setup line is missing. I've cut them as a numbered 1 / 2 / 3 sequence on screen so they hold together on their own — if there's an opening line before these, send it and I'll add the beat."*

**Shot list, organised into three recording sessions** (a recurring cut-sheet pattern — collapsing many beats into as few physical shoots as possible):
- **Session 1 — screen, one sitting:** the `/mcp` list, desktop + Gmail, memory file + cold-chat recall, settings.json rules + allow/ask terminal test, ElevenLabs agents page + voice playback, `claude` startup + tool calls, the self-writing config demo. Setup: terminal font two sizes up, notifications off, bookmarks bar hidden, 1440p+ at 60fps.
- **Session 2 — desk, Pocket 4:** the hero split-screen take with mic, the handheld slide to the monitor, hands lifting off the keyboard, over-shoulder on the phone. Room light low so the monitor is the brightest thing in frame; clap at the top of every take with a matching screen recording.
- **Session 3 — phone:** comment typed and posted, DM reply landing, reference reels played full-screen and recorded (recorded last, once the edit shows which cutaways survived).

A sourcing table closes the doc, naming every capture tool and reference (OBS Studio, phone recorders, the connectors directory page, the Claude Code permissions reference, ElevenLabs, yt-dlp / 4K Video Downloader, and the five credited reels/accounts).

## `routerise-alex-START-HERE.md` — checked, not folded in here

This source is a condensed project-briefing and house-style recap ("Read this first when starting a new video for Alex") covering delivery spec, the ten structural rules, track layout, the PIP system, the plugin list, Fusion build conventions and Resolve-stability warnings. It contains no cut-sheet process content — nothing about mapping VO to beats or building a shot list. Its facts are already captured in [[routerise-house-style]] and [[fusion-node-system]], and its project-context table (client/company/accent framing) is already quoted in [[clients/routerise]]. Nothing further was pulled from it into this note.

## needs-input

- Whether Butler reel beats 1–3 need an opening/setup line before the numbered list — flagged in the source as unresolved, pending Samuel sending it.
- Accent colour for the Butler reel — not set; the source suggests a cool blue-cyan but this is explicitly a suggestion, not a decision.
- The actual beat-by-beat HTML content of the three Routerise cut sheets (`$0-10K Cut Sheet - 21m39 to End.html`, `AI Ecom Brand - Cut Sheet.html`, `Cut Sheet - Visual Direction.html`) is not among the sources — only the companion notes summarising each are.
- Which ad downloader to use for the $0–10K video (§29 in that cut sheet) — listed there as still needed from the client, not resolved in the source.

Back to [[03-Areas/video-editing/_index|Video editing]]
