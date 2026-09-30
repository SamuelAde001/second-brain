---
type: log
area: video-editing
status: active
updated: 2026-09-22
source: manual
tags: []
---

# Log — video-editing

Append-only. Newest at the bottom. Format: `- YYYY-MM-DD — what happened`.

- 2026-09-20 — Area created during the Brain build.
- 2026-09-21 — **video-editor agent skeleton built** (profile, memory, log, wrapper) — the first agent in the Brain. **Step 6 (HTML→Fusion) proven** on a duplicated timeline: an 8-node house-style card built programmatically via the Resolve MCP and rendered over the footage. See [[07-Agents/video-editor/profile|the agent]] and [[agent-plan]].
- 2026-09-21 — **Step 1 (sync) tested** in the new "Claude tests" project. DaVinci waveform sync fails on this dead-camera-audio shoot; the **motion-correlation fallback works** (+4.0 s / ~120 frames, z 7.6). ffmpeg installed. [[03-Areas/video-editing/sops/routerise-cut-workflow|SOP]] step 1 updated with the verified decision tree.
- 2026-09-22 — **[[delivered-projects]] created** — every client video delivered so far, one row per video, for the finance agent to read. 17 rows (15 `name unknown` from [[03-Areas/finances/income|Income]]'s May–Aug batch counts, 2 named — "Andy video" and "Alex video", Sep #1/#2 — recovered from the archived Accountability Engine). Open: who "Andy" is; two more archived names ("Client #1/2") not placed, to avoid double-counting August.
- 2026-09-23 — **Render-cache crash root cause found: Windows GPU timeout (TDR, 2 s default)** during heavy Fusion comps on the 12 GB RTX 3060, not the cache itself. 0:00–1:02 of *$7M Founder* cached clean; fix (TdrDelay 60 + reboot) is Samuel's. See [[03-Areas/video-editing/troubleshooting|Troubleshooting]] §7.
- 2026-09-23 — **Routerise revision delivered** that night. Samuel, 2026-09-24: *"yes it went out last night, it's a revision"*. A revision, not a new video, so no row in [[delivered-projects]] and no change to September's income. Which video it revised is not confirmed.

- 2026-09-24 — **New Route Rise job: "3. I Tried 100+ AI Tools. These 4 Are Best for Businesses"**, due Monday 2026-09-28. Documented in [[04-Projects/routerise-4-ai-tools|Route Rise #3 — 4 AI Tools]] and scheduled in TickTick (9 blocks, Thu kickoff → Mon deliver).

- 2026-09-24 — **Route Rise #3 cut by the Editor:** waveform gap pass, retakes removed, 9:34 cut with A-roll, Tella and mic frame-locked, 8 colour-coded chapters, transcript .docx. New in the [[03-Areas/video-editing/sops/routerise-cut-workflow|cut SOP]]: the frame-grid rule (conform the mic to 23.976), clock drift, per-clip transcription, teleprompter detection. Detail in [[04-Projects/routerise-4-ai-tools|the project note]].

Back to [[03-Areas/video-editing/video-editing|Video editing]]
- 2026-09-25 — **Route Rise #3 visuals v1:** style study (7M, TSB, the agency's best editor, the Route Rise guide) → [[visual-vocabulary]]. 59 rendered visuals, one per sentence after the intro, placed on *Visuals v1 (Editor)* V7 for Samuel's review. New SOP [[visual-sheet-pipeline]].
- 2026-09-25 — **PC chokes while Resolve caches: diagnosed.** RTX 3060 at 100% / 9.9 of 12 GB VRAM, background cache fires after 1 s idle, 4K H.264 sources with proxies at Original size, HDR 1000 timeline, everything on one NVMe. Checklist in [[03-Areas/video-editing/resolve-performance|Resolve performance]]; nothing applied yet.
- 2026-09-25 — **Proxies fixed most of the caching slowdown.** Samuel made proxies of the footage (checklist item 1): *"Making the video a proxy solved a lot of the cap"*. Recorded in [[03-Areas/video-editing/resolve-performance|Resolve performance]] → Results.
- 2026-09-28 — **Route Rise #3 Visuals v2 built overnight on Cut v6** (Samuel approved stills, then slept): UI demos on V2 (real Tella footage for Clay canvas / playbook form / Railway canvas, HTML-built Chrome tabs, Clay table, generator, calculators, frontal.so form, Claude, VS Code GTM OS, Wispr dictation, LinkedIn chat), motion graphics as Fusion nodes on V3 (copies of his reveal for Railway / Claude / Wispr / all four / recap; pills, waterfall, dashed lines, checklist card, thought bubble, board, 5,000 vs 25). Not done: B27 Flow video. Near-miss: Insert* rippled the cut, undone; lessons in the Editor's memory.

- 2026-09-28 — **delivered-projects row 18 added: Alex video (Sep #3).** Samuel: 3 Alex videos + 1 Andy in September, the third Alex (Route Rise #3, 4 AI Tools) going out today. Sep #3 was in the archive (started 2026-09-15) but left out of the 2026-09-22 backfill because no delivery was logged, and he was never asked. Batch now 3 delivered; the 4 AI Tools row goes in when it is sent.

- 2026-09-29 — **Three Route Rise cards for October, in order by card dates:** [[04-Projects/routerise-cancel-apollo|Cancel Apollo]] (due Sat 10-03 2:15am, deliver Fri), [[04-Projects/routerise-ai-b2b-marketing|AI B2B Marketing]] (due Wed 10-07 1:45am, deliver Tue), [[04-Projects/routerise-linkedin-training|LinkedIn Training]] (due Mon 10-12 1:30am, deliver Sat). Apollo footage + Tella downloading; the other two planned only (AI B2B mics and script saved). 25 blocks in TickTick.
- 2026-09-29 — **Apollo job: setup, sync and cut done the same evening** (pulled forward from Wed). Cut v3, 9:09, is waiting for Samuel's review, then sections, transcript and the visual cut sheet. [[04-Projects/routerise-cancel-apollo|Cancel Apollo]]. Route Rise #3 sent to the client 2026-09-29.
- 2026-09-29 — **Apollo: Samuel revised Cut v3 (9:10); sections, transcript and the visual review sheet done** the same night (Editor). Waiting on his answers to the 120-row sheet. [[04-Projects/routerise-cancel-apollo|Cancel Apollo]].
- 2026-09-29 — **Apollo visual stills v2 out for review:** 55 visuals rendered as stills in #3's shipped look, transcript rebuilt against the script (both on Samuel's correction). [[04-Projects/routerise-cancel-apollo|Cancel Apollo]].
- 2026-09-30 — **Motion gallery v1 out for review:** 39 animated pills, boxes, cards and circles in house style, mixing light and dark orange, white and grey, after Samuel rejected the Apollo stills as one design repeated. [[03-Areas/video-editing/motion-gallery/motion-gallery|Motion gallery]].
