---
type: project
area: video-editing
status: active
updated: 2026-11-05
source: interview
tags: [ai-edit-engine, product, hyperframes, claude-code, high-ticket]
---

# AI Edit Engine (working name)

Back to [[03-Areas/video-editing/video-editing|Video editing]] · money side: [[03-Areas/finances/big-deal-options-2027|big-deal options]] → R5, R6.

## What Samuel wants (his words, 2026-11-05)
- *"I need to make it easy for them to use, possibly with a mod on their claude code that acts like a UI for their editing, and also easy for them to customize to any style in case they change their brand style etc and easy for them to review with a UI for reviewing, all in claude code, and all the permissions it needs would be granted etc"*
- *"I would test a system first to know if it's doable then build the structure"*
- *"make a list of everything needed to build this and make this work out, we would be working on this over time and see if this can be a reality"*
- Earlier the same day: no DaVinci Resolve (*"most of them don't want to go through Davinci resolve"*), HTML/CSS/JS visuals, runs on the customer's own Claude Code and Max plan, *"I won't do the editing"*, about USD 10,000 per customer.

**The shape (suggestion, from R6):** a Claude Code plugin on the customer's PC. HyperFrames renders the graphics, ffmpeg cuts and mixes, their brand style profile guides every choice, and a UI shows progress, review and style. Not a standalone app: a standalone app can't use a Max login, and paying per use would cost about USD 1,000 a video.

---

## Phase 0: the feasibility test (do this first, nothing else until it passes)

Goal: one real long-form video, edited end to end **with no Resolve**, judged against Samuel's own bar. It's the only question that matters yet.

| # | Step | Done when |
|---|---|---|
| 0.1 | Pick the test video: one finished Route Rise-style job with raws **and** Samuel's final, so there's a ground truth to compare with. Internal only, never shown or shipped | Samuel names it |
| 0.2 | Install on the PC: Node 22+, ffmpeg (already used), HyperFrames (`npx hyperframes`), and a transcriber. Pick **local Whisper** (faster-whisper / whisper.cpp) over ElevenLabs Scribe so there's no API key | `hyperframes render` makes an MP4 |
| 0.3 | **Cut pass** without Resolve: transcript with word timings → remove filler, dead air and retakes → ffmpeg cut list with audio fades. Reuse the logic of the video-edit-pass skill | Cut plays clean, no clicks, sync held |
| 0.4 | **Graphics pass**: port 5 of Samuel's core visual types to HTML/GSAP components (list, callout, lower third, screen-demo zoom with highlight, full-screen MG). Source: [[03-Areas/video-editing/edit-grammar/edit-grammar|edit grammar]] | Each matches its Resolve version in a still and in motion |
| 0.5 | **Screen-demo zooms and B-roll** on the cut, timed to words | Placed by script, not by hand |
| 0.6 | **Sound**: music bed, SFX on hits, loudness to -14 LUFS | ffmpeg loudnorm check passes |
| 0.7 | **Render** 1080p and 4K on this PC; time it | Render time written down |
| 0.8 | **Measure**: weekly-limit % used (`usage_audit.py`), wall-clock hours, Samuel's minutes, number of corrections | Numbers in this note |
| 0.9 | **Verdict**: is it as good as the Resolve version? Cheaper? | Samuel's call |

**Pass bar (suggested, Samuel to confirm):** good enough to ship after one round of fixes; costs **no more than the Resolve pipeline per video** (video 4 used ~60-65 % of a 20x week); nothing done by hand except the review.

**Known weak spots to test hard:** colour grade, audio repair (no Fairlight), subject masking (no Magic Mask), long renders, A/V sync over a 15-minute timeline.

---

## Phase 1: the engine core (after 0 passes)

1. **Project folder layout**, the same for every customer: `raw/`, `samples/`, `style/`, `assets/`, `work/`, `review/`, `final/`.
2. **Style profile**, one folder per brand, so a style change is a file edit, not a rebuild:
   - `brand.json`: colours, fonts, logo, safe areas, caption style, pacing numbers
   - `rulebook.md`: their rules in plain words (the shape of Samuel's [[03-Areas/video-editing/rulebook/rulebook|rulebook]], not its content)
   - `components/`: their HTML graphics kit
   - `samples/`: reference videos it learns from
3. **Style-study skill** (`/learn-style`): reads 3-5 sample videos (frames, cut rhythm, graphic types, captions, music) and writes a first style profile for the human to approve. **This is the selling point. It's the hardest part.**
4. **Pipeline as skills**, one per stage, each with a scripted check before the next stage: ingest → transcript → cut → visual plan → graphics → B-roll and assets → sound → assemble → QC → render.
5. **Asset finder**: their own library first, then licensed sources only (stock APIs with clear licences). **No YouTube or TikTok rips in a product** (the Route Rise practice can't ship). Browser access for screen captures of their own product.
6. **QC lint scripts**: from the Route Rise checks (flash frames, gaps, loudness, safe areas, spelling in graphics, A/V sync).
7. **Revision loop**: review notes → a fix list → the agent fixes only the noted beats → re-render only those sections.
8. **Cost control**: script-first, Sonnet helpers for exact-spec work, a token budget per video, a stop before the weekly limit (lessons in [[00-System/model-routing|model routing]]).

## Phase 2: the UI (inside Claude Code)

| UI | What it does |
|---|---|
| **Dashboard** | Current project, stage, progress, time left, usage this week |
| **Review** | Video player, click a moment → type a note → notes become the fix list; approve or send back per section; before/after |
| **Style editor** | Change colours, fonts, logo, pacing, rules; live preview of each graphic component; save as a new style version |
| **New project** | Drop raws, pick a style, press Start |

**Decision needed:** Claude desktop app **mods** (panels beside the chat) only work in the desktop app. A **local web page** (the preview-gate idea, already used on video jobs) works in any Claude Code, terminal included. Suggestion: build the UI as a local page first, then wrap it in a mod for desktop-app users. Check what mods can do with the plugin-authoring skill before building.

## Phase 3: packaging and install

1. **Claude Code plugin**: skills, subagents, hooks, slash commands (`/new-video`, `/learn-style`, `/review`, `/render`), the UI.
2. **One-command installer** for Windows (and Mac later?): Node, ffmpeg, Whisper model, fonts, HyperFrames, health check.
3. **Permissions shipped with it**: a project `settings.json` that allows exactly what the engine needs inside its own folder (files, ffmpeg, node, the browser for captures). The customer approves it once at install. Anything outside the folder stays an ask.
4. **Updates**: private plugin marketplace (a private Git repo per customer), versions pinned so an update never breaks a live project.
5. **`/doctor`**: checks versions, disk, GPU, Claude login, usage left; tells them what to fix.

## Phase 4: legal and business checks

- [ ] Anthropic terms: the customer running Claude Code on their own plan for their own business work. Read the current Consumer Terms and Usage Policy; for companies, check whether a Team or Enterprise seat is the right plan.
- [ ] HyperFrames: Apache-2.0, keep the licence and notice.
- [ ] video-use licence is unclear: check it, or write our own cut logic.
- [ ] Fonts, music, SFX: only licensed, redistributable files, or the customer's own.
- [ ] Strip every Route Rise / Frontal / Gamma asset; check the Route Rise terms on building and selling tools.
- [ ] Contract: style study, build, pilots, guarantee, support term, what "done" means, liability cap.
- [ ] Data: footage never leaves the customer's PC except to the model; say so in the contract.

## Phase 5: proof and selling

1. A demo video: folder → `/new-video` → review UI → MP4, with a side-by-side against the human edit.
2. A case study with numbers: hours saved, cost per video, corrections.
3. A one-page offer: USD 1,500 style study (credited) → build → 3 pilot videos → 60 days support → USD 500-1,000 a month maintenance; about USD 10,000 total; 50/30/20; refund of the build stage if the pilots miss the agreed bar.
4. Outreach list: 50 B2B / SaaS / AI companies posting weekly long-form, plus small video agencies. Each pitch carries a re-edit of their own public video.
5. Pilot customer 1 at a discount, in exchange for the case study.

## Phase 6: support

Maintenance plan, a break-fix list for when Claude Code, HyperFrames or Node update, a usage report each month, a style update included each quarter.

---

## Project plan (draft dates, tokens permitting)

Offer and brand: [[04-Projects/ai-edit-engine-offer-and-brand|Housecut offer and brand]]. Dates move with Route Rise work and the weekly limit; every phase ends with a go/no-go from Samuel.

| Phase | Dates (draft) | Output | Go/no-go |
|---|---|---|---|
| 0. Feasibility test | 2026-11-09 → 2026-11-22 | One video, no Resolve, measured | Passes the bar → go on. Fails → sell R5 (the Resolve system) or drop it |
| 1. Engine core | 2026-11-23 → 2026-12-20 | Style profile, `/learn-style`, pipeline skills, QC, revision loop; tested on a **second, different style** | It copies a style it wasn't built on |
| 2. Studio UI | 2027-01-04 → 2027-01-24 | Dashboard, review, style editor, new project | A non-editor runs a video alone |
| 3. Packaging | 2027-01-25 → 2027-02-07 | Plugin, installer, permissions, `/doctor`, private marketplace | Clean install on a second PC |
| 4. Legal checks | alongside 1-3 | Checklist above cleared, contract drafted | All boxes ticked |
| 5. Pilot customer | 2027-02-08 → 2027-03-21 | Paid pilot (USD 3,000-5,000), case study | Customer would post the videos |
| 6. Launch | from 2027-03-22 | Housecut page, outreach to 50, first full Build at USD 9,500 | First full-price deal signed |

Christmas week 2026-12-21 → 2027-01-03 is left free. The first full-price deal lands in **Q2 2027** at the earliest, so this isn't January money.

## Open decisions for Samuel
1. Which video for the test (0.1).
2. Mod-only UI, or local web page first (Phase 2).
3. Windows only, or Mac too (most founders use Mac).
4. The pass bar for Phase 0.
5. When: tokens come from the same 20x week as Route Rise work.

## Log
- 2026-11-05: note created from Samuel's ask; build list written (General Manager). Nothing built.
