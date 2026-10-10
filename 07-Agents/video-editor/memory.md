---
type: agent
area: video-editing
status: active
updated: 2026-10-10
source: interview
tags: [agent, memory]
---

# video-editor — memory

Append-only. What this agent has learned by doing. Newest at the bottom. Facts here were verified in action, not assumed (AGENTS.md rule 6).

**How to read it:** the digest below holds every standing lesson up to 2026-10-09 in one line each, with the date of its full entry. The full entries were moved verbatim to [[07-Agents/video-editor/memory-2026-09-21-to-10-09|memory, 2026-09-21 to 10-09]] on 2026-10-10 (General Manager, Brain tidy). Open an entry there only when the work touches it. Visual rules live in [[03-Areas/video-editing/ways-of-working|ways of working]], Resolve and Fusion scripting in [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]], his finals' grammar in [[03-Areas/video-editing/edit-grammar/edit-grammar|edit grammar]]. New entries go at the bottom, after the digest.

---

## Digest, up to 2026-10-09

### Working with Samuel
- **Resolve is shared with his own edits.** While he edits, do everything possible outside Resolve, batch the Resolve steps into one block that runs after his go, save his open project as he left it and load it back after. If the open project isn't this job's, ask before switching (10-08, 10-09).
- **Scripts, not screen control** (10-07: *"Avoid using computer use when you don't need it"*). A GUI step only when he asks for it or OKs it; narrate each step (09-25).
- **When Resolve crashes, relaunch it, reload project and timeline, report what was lost.** Don't wait to be told (10-07).
- **His markers are part of the brief.** Read every marker on the timeline he left them on, at the start of every round, and track each to done. The text is in the marker's name field (10-03, 10-08).
- **Ask short either/or questions with defaults**; he answers fast (10-08).
- **Usage is a budget.** Ask before a big fan-out once the weekly cap is past ~20 %. Run builders a few at a time. Skeptic verifiers are the expensive part; verify by eye from stills where the fault is obvious (10-08, 10-09).
- **Decide, don't flag.** Flags and markers are clutter to him; keep them for content that exists nowhere else (09-25).
- **Don't add motion he didn't ask for** (10-01).
- **Replaced visuals are disabled, not deleted**, after a backup timeline; tell him which ones so he can delete them (10-03).
- **Long sessions die.** Keep the plan, the workflow script and a resume note in the job's Docs folder and the Brain from the start; install each builder's output as soon as it lands (10-07).
- **Reuse the study.** Plan from the edit grammar and `Routerise\Visual Assets\Samuel templates (Editor)\`; re-study only a new finished video (10-08).
- **Jobs run in ClickUp card-date order.** Confirm "next" against the board. A due time after midnight means deliver the evening before, nothing after 10pm (09-29).
- **An open flag in delivered-projects is a question for the next session.** Confirm the month's video count with him before the invoice on the 29th (09-28). Don't force a reconciliation between sources that disagree; record both and flag (09-22).

### Cutting
- **His method:** duplicate the synced raw, delete the Tella audio, Ripple Delete Silence; threshold from the red preview (#3: −33.4 dB, pre 0, post 3, min 2). Never rebuild a cut clip by clip (09-25).
- **Order:** silence → noise → retakes → uhms → transcript check. Last clean complete take, inside clips as well as across them. Short wordless clips between sentences are noise (09-25).
- **Judge retakes from per-clip transcripts**, never the whole-file transcript (09-25, 10-06).
- **Before handing over:** diff the raw transcript against the kept source ranges; the script's hook line must be in the cut (09-25).
- **The transcript is checked against the client's script every time**; note where the footage leaves it (09-29). A last clean take with a different number than the script: keep it, flag the number (10-06). Alex saying "remove this" on camera: cut it, note it (10-06).
- **Demos keep a short silent hold after each prompt; the Tella goes only over real UI** (09-29).
- **Diff his final against mine on every job he finishes himself** (09-25, 09-29).
- **Sync:** Alex's camera audio is usually dead; motion sync, trust `av_sync.py`, ear-check the first placement. Cut with a metadata-free lossless mic copy at the timeline rate. Drift ~129 ppm on a 28-minute take (09-21, 09-24).

### Visuals (full rules: ways of working)
- **"Mediocre" means one design repeated.** Same font and palette, many ways of using them. The motion gallery is a vocabulary to remix, never templates (09-30).
- **Show the thing, not a pill naming it.** Pills are for nouns and lists (10-02). A list he says on the orange screen = title + numbered pills lit on his words (10-03).
- **"Build a UI demo" means build it from scratch.** Never base a visual on Alex's footage or visuals unless Samuel names them (10-02). Made-up company names for claims, real logos only for real tools (10-02). Check a company's stack against the footage before naming it (10-01).
- **Node layout is navigation:** the B04 v2 layout is the standard for every comp; check the node view before saying done (10-02).
- **"Glow" means Neo Glow** (09-26). Effects are real nodes, never faked (09-25).
- **His constructs go on adjustment clips, not base clips** (10-07, his instruction; replaces the 10-03 base-clip workaround after crashes).
- **Pacing:** every visual ends where the next starts or on the next cut; measure end alignment, not only density. Plan a website or logo beat for every named company; Frontal logos allowed (10-07).
- **Check from the timeline:** export frames at the middle and end−30 of each comp. Never leave a card empty; lay out rows from measured widths; glyphs in their own Text+ (09-30, 10-07).
- **When he points at his own element, lift it from his comp with its settings.** Read his newest edits in the job before designing (10-03).
- **UI mockups fill the frame**, fill whole rows (~0.3 s a row), no highlight boxes (09-27). Real UI from his Chrome for logged-in pages, Google Images for product shots (09-27). No fast zooms on UI (10-03).
- **AI B-roll from Omni Flash in Flow.** Cut to a full-screen rebuild when the B-roll's screen has to say something (10-03).
- **A visual review is rendered stills, never a text sheet** (09-29).

### Machine and files
- **Render cache:** he reviews from the cache, not a render. Never bulk-toggle Fusion output cache on a cached timeline. Check C: free space first (35–40 GB for a whole video) (10-09).
- **C: is the only local disk; G: is Google Drive.** Never put cache, proxies or footage on G: (09-28).
- **Never Ctrl+Z after a script action**: Resolve's undo includes it (09-25).
- **New Resolve project:** never copy `Project Template`; `CreateProject` fresh and drag in the "Folder structure template" power bin (09-24).
- **Paths:** the curly apostrophe in a job path is mangled by the MCP transport (10-07); Git Bash `/c/...` paths break Windows Python, use `C:/...` (10-09).
- **YouTube pulls get re-encoded** to edit-ready .mov (libx264; `h264_nvenc` fails on this driver) before handing over (10-09).
- **Where Route Rise material lives:** idea docs on public `*.notion.site`, footage in link-shared Drive folders (read in the in-app browser), screen recordings on Tella (09-24, 09-25, 09-29). His visual references: `Routerise\Visual Assets\Visual Inspo\` and the #3 `Docs\Visual study\best-editor\` (09-30).
- **Folders granted:** `Desktop\Video edits\Ad showcase\` (write, 10-09).

---

## Entries from 2026-10-10

- **2026-10-10 — A revision round on a cached timeline goes in place.** Samuel caches the whole video before reviewing, so a duplicate (or a .drt re-import) costs him a full re-cache. Back up once, then swap comps on the existing clips with `kits\inst\inplace.py` (stage, export, `adjconv.py`, `ImportFusionComp`). New ranges with no adjustment-clip host get a base clip; tell him which. Rules from his 61 markers: [[03-Areas/video-editing/ways-of-working|ways of working]] → Revision rules. Hangs and their fixes: [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] (2026-10-10).
- **2026-10-10 — Pause background tasks while scripting, restart Resolve to cache.** `DisableBackgroundTasksForCurrentResolveSession()` first thing in every scripted session (background caching + page/timeline switches hung Resolve five times). When the work is done, restart Resolve without it and leave the timeline on the Edit page so it caches. Don't switch projects by script on this machine while it's busy: loading Apollo froze it.
- **2026-10-10 — Weigh every builder comp.** A 10-token motion graphic came back at 2.6 MB with 73 Neo macros; one token chain duplicated brought it to 0.5 MB. Ask for file size and tool count in every report; send back anything heavier than the old crash comp (1.5 MB).
- **2026-10-10 — Backslashes don't survive the shell.** The Bash tool halves `\\` inside heredocs, so Windows paths written through it turned `\r`, `\b`, `\a` into control characters in three Brain notes. Write Brain text with the Write tool (or build paths with `chr(92)`), and scan for control characters after any scripted edit.
- **2026-10-10 (evening) — Finals: H.264 MP4, never the render cache, rendered in chunks.** Samuel: *"don't use render cache as a final render, my client would pick on it"* and *"Not proRess, use H.264, proRess would be good large"*. Resolve 21.1's `SetRenderSettings({"VideoQuality": ...})` returns False for every value and codec, so H.264 NVIDIA renders at its automatic quality (~14-16 Mbps at 1080p; his "H.264 Master" preset gives the same). Render the timeline in ~3,000-frame chunks (a power cut loses one chunk), then `join_chunks.py` in the job's final-render folder concats them with `-c copy` and muxes one full-length WAV. Speed on the B2B final: 6-12 fps, chunks 4-10 min.
- **2026-10-10 — Chrome downloads while Samuel is away.** His Chrome asks where to save each file, and computer use can only get Chrome read-only, so the dialog can't be clicked. The file still lands in `Downloads\<guid>.tmp` at full size within seconds; copy it out and use it. Flow's 1080p upscale took under 2 minutes. While Resolve renders, Claude in Chrome screenshots time out (GPU busy): use `find` / `read_page` / `get_page_text` instead.
