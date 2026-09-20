---
type: knowledge
area: video-editing
status: active
updated: 2026-09-20
source: memory-export
tags: [tools, resolve, obs]
---

# Toolchain

Samuel's production stack and the tooling around it. From the Claude memory export, `/topics/video-editing-toolchain.md`, last updated 2026-09-20 — the most current record of what he actually uses.

## Core stack

**DaVinci Resolve · Fusion · OBS · DJI Osmo Pocket 4 · DJI Mic Mini.** The memory notes "strong, established fluency" across all of it — an agent should not explain the basics of these tools to him.

- **Windows 11 PC. Android phone. Claude Pro plan.**

## DaVinci Resolve

Worked through in depth: H.264/H.265 generation loss, export settings, Fusion node graphs, multicam editing, LUTs.

## OBS Studio

4K recording profiles · scene collections vs. profiles · window-capture troubleshooting with WGC and BitBlt.

## DJI

DJI Mic Mini for production — he has worked through all transmitter settings in DJI Mimo, and corrected several documentation inaccuracies while doing it.

## Bespoke tooling

- Comfortable building custom tooling in Claude.
- Built animated screen-recording demo HTML files to use as **B-roll in client edits**.
- Worked on font tooling for editing.

## The editing clock

A recurring habit worth knowing, because it changes how to answer him:

> A standalone HTML "editing clock" / pace widget, kept open beside Resolve to hold a deadline pace — planned playhead position vs. actual, in WAT (UTC+1).

**He calls it his "timer".** When he asks for "a timer" to finish a video, this is what he means — not a countdown. He asked for it to be packaged as a reusable skill, `edit-clock`, which now exists.

## The machine

From the video-editing project memory, 2026-09-06:

- **Core i5 13th Gen, NVIDIA GeForce RTX 3060 (12GB VRAM).** DaVinci Resolve 21.
- Scripting: **Python** (ElementTree, file parsing, Fusion `.setting` generation), **Node.js** (`docx` for Word generation), and the **DaVinci Resolve Python console API**.
- File formats in regular use: FCP7 XML · SRT · EDL · `.setting` · `.drfx` · `.prproj` · FBX · OBJ.
- External tools: **LibreOffice headless** (docx → PDF verification), **pandoc** (docx → markdown), **Demucs / UVR5** (vocal isolation), **WhisperX** (forced alignment).
- 3D asset sources: **Sketchfab, CGTrader** — game-ready models, Metallic/Roughness PBR workflow.

## How client footage arrives

Client videos are typically **a single OBS capture combining A-roll talking head and screen recording**. And the fact that shapes every edit: **the presenter freestyles significantly from the provided script.** That is why the cut sheets key to the subtitle file rather than the script ([[cut-sheets]]).

## Hardware note

Bluetooth audio trouble was traced to a counterfeit CSR8510 adapter. A TP-Link UB500 dongle was the fix, sourced locally in Abuja.

Related: [[client-acquisition]]. Back to [[03-Areas/video-editing/video-editing|Video editing]]

## Current state, 2026-09-06

- **A new client has been taken on** — different presenter, generally a different visual style from Routerise, but the same two-phase `video-edit-pass` workflow applies. The Brain has no client note for them; if this is Mshel (invoice DSG-2026-001, [[03-Areas/finances/invoicing|Invoicing]]), that needs confirming.
- Completed a full two-phase editorial pass on a Routerise video: "The Only Claude Dropshipping Guide You'll Ever Need in 2026" — phase 1 cut-marker scripts via the Resolve Python console with diffing across timeline versions; phase 2 a chaptered ALL-CAPS docx transcript, chapter marker EDL and marker scripts.
- Active Fusion work: a 30-day calendar hero asset, e-commerce dashboard widgets, 3D text shadow composites, icon arc animations.
- **The "people web" build**, for the line *"WHAT HAPPENS WHEN A MILLION PEOPLE GET HANDED THE SAME SHORTCUT AT THE SAME TIME?"* — 30 illustrated figures standing in for a million. Rig: illustration → `ImagePlane3D` at varied X/Y/Z with animated opacity appearing at random → one `Merge3D` → animated `Camera3D` moving from inside the web to outside → `Renderer3D`. Figures in shades of `#35C6E8`. 97 frames, every appearance and the camera move finishing at frame 51, camera move kept smooth.

**On the horizon:** expanding a personal Fusion node-recipe library so future sessions can regenerate specific designs from a natural-language description — which is what [[fusion-recipes]] is now for.

