---
type: project
area: video-editing
status: active
updated: 2026-09-29
source: manual
tags: [client, routerise, long-form]
---

# Route Rise — "I cancelled Apollo.io and built this Claude skill instead"

Client job through [[03-Areas/video-editing/clients/routerise|Route Rise]] (Alex, Frontal). Back to [[03-Areas/video-editing/video-editing|Video editing]].

**October order (by card dates):** **1 of 3** → [[04-Projects/routerise-ai-b2b-marketing|AI B2B Marketing]] → [[04-Projects/routerise-linkedin-training|LinkedIn Training]].

## Brief (ClickUp card, screenshot Samuel sent 2026-09-29)

- **Card title:** I cancelled Apollo.io and built this Claude skill instead (no number on the card) · READY TO EDIT · long form video · edit-assigned
- **Dates:** start Mon 2026-09-28 → **due Sat 2026-10-03, 2:15am WAT**, so it is delivered on **Fri 2026-10-02**.
- **Idea doc:** https://striped-thief-c4a.notion.site/I-cancelled-Apollo-io-and-built-this-Claude-skill-instead-3ca73bd1b02b8176adf7c4157e657949 (public link; the Notion deadline field, 2026-09-02, is stale)
- **Drive:** "4 - Cancel Apollo", https://drive.google.com/drive/folders/10V9UA7SO90S5Kre9cu0Ge2idbad1Qo2I
- **Rate:** USD 333.33 unless Samuel says otherwise ([[03-Areas/video-editing/delivered-projects|delivered projects]] rule).

## Job folder

`C:\Users\repzy\Desktop\Video edits\Routerise\I cancelled Apollo.io and built this Claude skill instead\`

- `Client raws/`: C0787.MP4 (15.25 GB, 3840×2160, 29.97 fps, 34:33; downloaded 2026-09-29), TX02_MIC018 + MIC019 (2026-09-25).
- `Screen recordings/`: Tella 4K export, "Building a Custom GTM Operating System for Sales" (23:59). Tella chapters: 00:00 The Problem with Databases · 06:40 Forward Deployed Engineers · 09:02 Defining Good Accounts · 11:05 Analyzing Account Signals · 20:43 Generating Outreach & Copy.
- `Docs/`: the idea doc (.md + .docx) and Alex's recording script, a Google Doc (about 2,250 words, opens "We built our own prospecting system…", example company Lob). The recording script differs from the Notion script; work from the footage.

## Schedule (TickTick, 📹Video editing)

| When (WAT) | Step |
|---|---|
| Tue 09-29 7:00–8:00pm | Editor: Resolve setup + sync, after Samuel's revision render |
| Wed 09-30 7:00am–1:00pm | Cut |
| Wed 09-30 7:00–9:00pm | Claude pass: sections, transcript, visual cut sheet |
| Thu 10-01 7:00am–1:00pm, 7:15–9:00pm | Visuals |
| Fri 10-02 7:00am–1:00pm | Finish visuals + sound, render started by 1:00pm (the last render took 3h55m) |
| Fri 10-02 7:00–8:30pm | Review the render, deliver (Bible study at 8:30) |

Clashes flagged to Samuel 2026-09-29: Ep 4 edit (Wed 7am–1pm), Ep 4 captions (Wed 7–9pm). Resolved the same day by the PA: Ep 4 moved to Wed and Thu 3:00–4:30pm.

**Pulled forward 2026-09-29.** Samuel: *"let's get the next project started now, cause my company wants me to be faster"*. Setup, sync and the cut ran the same evening. The Wed 7am cut block is now his review of Cut v3.

## Resolve project

Project "I cancelled Apollo.io and built this Claude skill instead" (folder Routerise), fresh, bins from the power bin. Cache at `C:\Users\repzy\Videos\CacheClip`.

- **Sync.** The camera's scratch audio is alive this shoot (max −6 dB), so the offset is camera audio against mic: **mic starts 3.32 s after the camera** (z 33), the same at minute 1 and minute 27 (no drift). MIC019 follows MIC018 with no gap (camera 1803.47 s). Tella starts at **camera 256.62 s** (z 25–35, no cuts inside it). The mic on the timeline is the 23.976-grid lossless copy in `Conformed audio/` (MD5s match the raws).
- **A-roll synced (raw).** V1 camera picture, V2 Tella, A1 both mic files at +6 dB, A2 Tella audio (disabled). Blue "Lip-sync check" markers at 1500 and 47500, green "Screen sync check" at 8000.
- **Cut v1 (Editor) - ripple silence.** Ripple Delete Silence at Samuel's #3 settings (−33.4 dB / 0 / 3 / 2, no cross fade): 458 clips, 14:30. The tool skipped the MIC019 clip on the first pass; it was run a second time on that clip alone.
- **Cut v2 (Editor) - noise clips removed.** 193 noise clips (no 50 ms window above −40 dB) plus the 124-frame camera tail past the mic end: 265 clips, 13:36. The long noise run at camera 29–32 min checked against camera audio (−46.6 dB RMS vs −34.9 dB on speech): nobody talks there.
- **Cut v3 (Editor) - retakes removed. The cut for review: 158 clips, 9:09 (13,171 frames).** 107 clips cut from per-clip transcription (every wordless clip transcribed joined to the next), last clean complete take kept, and 2 in-clip trims (c068 "but connecting and AI tools", c246 "go back into the entire system"). Sync checked on every clip after the edit.

### Calls Samuel should check in the review
- **Opener "today I'll show you".** Kept the clean scripted take ("where Apollo alone falls short for us / what we've built around it / how you can build something similar"). The later take ("why you shouldn't rely on a single tool for your…") trails off before its last word.
- **"Which clients have been a good fit?"** Kept the first take; the retake transcribed as "Which clan…", which suggests a slip.
- **Forward-deployed engineers.** Kept "The company Palantir actually invented the term." + "Palantir helped pioneer that model… around actual operations." + "companies like 11 Labs, Anthropic, OpenAI that hire engineers to build custom solutions". His earlier "OpenAI, Anthropic, 11 Labs… also hiring" was cut off mid-word.
- **Assumption line.** Kept "…otherwise you can end up writing an email with an assumption." + "That's super convincing, that's actually wrong and inaccurate."
- **The demo prompts** Alex dictates into Codex (Lob playbook, three contacts, lead magnet, waterfall enrichment) are all kept, including "Go ahead, I'm doing a demo for YouTube…". The door and "Thank you" moment after them is cut.
- **What's in the footage vs the script.** The script's middle (the review-threshold rule, saving the skill, testing on 25 accounts) wasn't recorded; the footage has a live Codex demo and a new "shared data layer" ending instead.

Scratch left in the project: bin "zz Editor per-clip transcription (Cut v2)" (291 WAVs from `Conformed audio/Per-clip WAVs (Cut v2)/`). Delete both after the cut is approved.

## Log

- 2026-09-29 — Setup, sync and cut done (Editor). Cut v3 is ready for Samuel's review. Next: his review, then sections, transcript and the visual cut sheet.
