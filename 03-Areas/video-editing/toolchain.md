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

## Hardware note

Bluetooth audio trouble was traced to a counterfeit CSR8510 adapter. A TP-Link UB500 dongle was the fix, sourced locally in Abuja.

Related: [[client-acquisition]]. Back to [[03-Areas/video-editing/_index|Video editing]]
