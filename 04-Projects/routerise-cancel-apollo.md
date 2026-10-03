---
type: project
area: video-editing
status: active
updated: 2026-09-30
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

### Samuel's revision of Cut v3 (2026-09-29): 178 clips, 9:10 (13,194 frames)
He edited Cut v3 in place. Diffed by mic source range against Cut v2/v3 (`Docs\Cut v3 revised by Samuel (2026-09-29).xml`):
- **No clip restored, none removed.** All four review calls stood.
- **28 trims inside kept clips.** In the talk they're 1–5 frames at heads and tails. In the Codex demo they're 5–31 frames, the pauses inside the dictated prompts.
- **8 silent stretches put back in the demo** (294 frames, 1.7–2.4 s each) so Codex's answers show on screen before the next prompt.
- **Screen recording only over the demo:** V2 emptied. The Tella now sits on **V3 from 5:45.55 to 7:42.67** (43 clips, sync unchanged). Everywhere else the Tella screen is Alex's teleprompter.
- Two blue markers at 4:10 and 5:45 (the build and the demo start).

## Sections, transcript, visual review (Editor, 2026-09-29)
Timeline **Visuals v1 (Editor)** = duplicate of his revised Cut v3, with a subtitle track (disabled), clip colours on V1/V3/A1 and a duration marker per section. His Cut v3 is untouched.

| # | Section | Starts | Colour |
|---|---|---|---|
| 1 | Hook and intro | 0:00 | Yellow |
| 2 | Where Apollo falls short | 0:39.7 | Blue |
| 3 | Frontal's GTM OS and skills | 2:05.8 | Green |
| 4 | Forward-deployed engineers | 2:57.9 | Purple |
| 5 | Mid-video CTA: Frontal | 3:55.8 | Pink |
| 6 | Step 1: define a good account | 4:10.2 | Teal |
| 7 | Step 2: connect the tools (the Lob example) | 4:51.2 | Tan |
| 8 | Codex demo (screen recording) | 5:45.6 | Brown |
| 9 | A shared data layer | 7:42.7 | Lime |
| 10 | Outro and CTA | 8:58.8 | Violet |

- **Transcript:** `Docs\Transcript - Cut v3 revised (2026-09-29).docx`: ALL CAPS, one colour per section, the 8 Codex prompts boxed. **Rebuilt against Alex's script** (Samuel's correction): "a bad fit", "isn't working", "the run returned five signals", "they're hiring in roles", "for your business", "walkthrough"; 3 script-check notes where the footage leaves the script (mid-CTA pitch, the missing middle, the new ending); 3 lines still to check by ear.
- **Visual stills v2** (replaces the text-only v1 sheet, Samuel's correction): https://claude.ai/artifact/QW3cUPRKZFhcniqem7c7T8 (private, version 2), copy at `Docs\Visual stills v2 (2026-09-29).html`. 55 visuals + 4 intro ideas, each rendered as a still in the look that shipped on #3 (`Graphics\Visuals v1\kit.py` = the #3 stills2 kit), 14 plain A-roll lines between them. Real UI from Alex's Tella: Apollo's Find companies page with his filters (V01, V02, V07) and the Codex run (V36, V38-V47, circle of Alex + focus boxes). A build board DEFINE / CONNECT / CHECK / OUTREACH carries the build section. Build files: `vis.py` (one entry per visual, `python vis.py V12` re-renders one), `frames.py`, `review_v2.py`, `grounds\`, `vis\`. Logos in `Graphics\Logos\`.
- **What real UI exists:** Tella 0:00–0:30 is Apollo (Companies page loading, "My lists"). The Codex app runs from Tella 12:15 to the end. The rest is the teleprompter. The typed bubble in Codex is his dictated prompt word for word, so use it to settle transcript doubts ("which play", not "which player").
- **Flags for Samuel:** the Codex result at 6:50 shows three real Lob employees' names and LinkedIn links (emails masked): blur or leave? The last prompt (7:24–7:42, CTA and waterfall enrichment) never shows its result; the recording ends while he dictates.
- Scratch left on *Visuals v1 (Editor)*: an empty Fusion comp with one Note on the first V1 clip (the cue export; `DeleteFusionCompByName` returned False). Harmless; delete it with the other scratch.

## Visual review v3 (Editor, 2026-09-30)

Samuel rejected the v2 stills as *"mediocre and shallow"*: the same design and colour ratio on every beat. After the [[03-Areas/video-editing/motion-gallery/motion-gallery|Motion gallery]] was approved, he asked for a new visual review for this video: *"be creative and let it look good and professional, not stale like the last one"*.

- **Page:** `Docs\Visual review v3 (2026-09-30).html`, built by `motion-gallery/build_review.py`. Every sentence of his Cut v3 in order. Each visual animates in time with the words, with a live caption, approve/change/drop, a comment box, and Copy my review back to chat.
- **40 new animated visuals** (`Graphics\Visuals v3\scenes-1..3.js`): 4 intro ideas (I1–I4), 34 motion graphics on BGORANGE or the A-roll, and 2 text beats on the Down fade. **Q01** is new: Alex's own line *"You don't have to build your own contact database to build your own workflow"* as a quote on his footage.
- **Motifs:** the GTM OS core (I1, I4, V11, V12, V33, V50, V51) and the build board DEFINE / CONNECT / CHECK / OUTREACH (V27, V29, V33, V34).
- **Kept as planned** (shown as stills): the real Apollo and Codex screens V01, V02, V07, V23, V36, V38–V47; the #3 reuses V25, V26, V54, V55. V10 is a Flow AI video (prompt on its card).
- **Still open:** blur or keep the three real Lob contacts' names (V43), and the last prompt's result never appears on the recording (V47).

## Log

- 2026-09-29 — Setup, sync and cut done (Editor). Cut v3 is ready for Samuel's review. Next: his review, then sections, transcript and the visual cut sheet.
- 2026-09-29 — Checkpoint (Editor): Samuel revised Cut v3 himself (178 clips, 9:10). Duplicate *Visuals v1 (Editor)* made, subtitled, 10 sections coloured with duration markers; transcript `Docs\Transcript - Cut v3 revised (2026-09-29).docx`. Next: the visual review sheet.
- 2026-09-29 — Samuel revised Cut v3 (9:10): 28 trims, 8 silent demo stretches back, Tella only over the demo. Editor: sections (10, coloured on *Visuals v1 (Editor)*), transcript docx, visual review sheet (120 rows). Next: Samuel answers the sheet, then the visuals build (Thu).
- 2026-09-29 — Samuel: the transcript had to use the script, and the visual review has to be the actual visuals, learned from #3's final. Transcript rebuilt against the script; 55 visuals rendered as stills after a study of #3's delivered video (v2.2.mp4, one frame per 3 s). Next: his answers on the stills, then the Fusion builds.
- 2026-09-30 — Motion gallery approved in full. Visual review v3 built: 40 animated visuals remixed from the gallery and timed to the words. Next: Samuel's marks and comments, then the Fusion builds of what he approves (Thu 10-01 visuals block).
- 2026-10-01 — Editor: four logo pills (Apollo, LinkedIn, LeadMagic, AI Ark) added to Samuel's I1 hub comp (V2 28–177 on *Visuals v1 (Editor)*), fed into his empty `Merge7`. Builder: `Graphics\Visuals v3\build_I1_pills.py`.
- 2026-10-01 — Editor: hook pills rebuilt on Samuel's review as five static P01 medallion pills: Apollo, AI Ark, LinkedIn, LeadMagic (all four checked against the Codex demo and the script) and Codex (his pick for the 5th). The v1 pills were deleted. Builder: `Graphics\Visuals v3\build_I1_medallions.py`.
- 2026-10-02 — Editor: B03 real Apollo demo in the red marker (177–334): Alex's own Apollo session from the Tella, fullscreen, cut so the company list lands on "a list of companies", with a cursor-following zoom (max 1.32) on a V5 adjustment clip. Waiting on Samuel's look.
- 2026-10-02 — Editor: B03 demo rebuilt from scratch on Samuel's correction (no Tella): an HTML Apollo Find companies page rendered to `Graphics\Visuals v3\B03 Apollo demo\Apollo demo B03 (Editor).mov` on V2 177–334, the 201–500 click generating the list, cursor-following zoom on the V5 adjustment clip. Waiting on his look.
- 2026-10-02 — Editor: B04 visual in the red marker (V2 334–464): I2 rebuilt as a Fusion comp with a detailed Apollo results card (the B03 demo's companies), dim on "know", three question pills on know / good fit / why. Builder `Graphics\Visuals v3uild_B04.py`. Waiting on his look.
- 2026-10-02 — Correction (Editor): the builder path in the entry above lost a character to an escape; it is `Graphics\Visuals v3\build_B04.py`.
- 2026-10-02 — Editor: GTM OS demo built from scratch on Samuel's ask (*"a real screen showing the OS UI in work… that I can import in the timeline myself"*): the Codex app rebuilt full screen (layout measured off Alex's Tella, none of his footage used), project `frontal-gtm-os`, the account-research skill run on lob.com: prompt typed, six OS steps (SKILL.md, client context, `gtm.py intel`, signal engine, Exa search, wedge agent), then the verdict with reasons and what's missing. Wording comes from the real runs (the #3 Claude Code demo and this Tella). 20 s, 1920×1080 ProRes 422 HQ at 23.976: `Graphics\Visuals v3\GTM OS demo\GTM OS demo (Editor).mov`. Not placed; Samuel places it himself. Fits B34–B36.
- 2026-10-02 — Correction (Editor): Samuel rejected the Codex-layout GTM OS demo in the entry above (*"Generate a UI that shows the GTM OS, not a cursur page, stop copying from alex visuals… make it dark mode also"*). v2 replaces it at the same path, `Graphics\Visuals v3\GTM OS demo\GTM OS demo (Editor).mov`: an original dark GTM OS app running account-research on lob.com, 22 s, no cursor. v1 moved to `GTM OS demo1 Codex (rejected)\`.
- 2026-10-02 — Correction (Editor): in the entry above, the path to the rejected v1 lost a character to an escape. The folder is `Graphics\Visuals v3\GTM OS demo\v1 Codex (rejected)\`.
- 2026-10-02 10:30 — Checkpoint (Editor), Samuel's review of marker 2 (*Visuals v1 (Editor)* red marker 952–3017, V01–V10). Plan per his notes: V01+V02 = my own Apollo Find companies demo (952–1307: three filters on his words, 191K → 23.4K → 5,038, list scrolled, send-email hover, the twins Quillstream/Brightfold ticked, cursor across employees / industry / country); V03 = twin cards from left and right on an adjustment clip over Alex (1307–1558), no "same on paper" text, no email card; V03 email part = Claude writing one email for both (1558–1749); V04 = question pills on Alex, no header pill, animated out (1844–2013); V05 = full-screen call recording, team B-roll, campaign notes, then the pills that can't reach the tool (2074–2247); V06 = COMMON CONTEXT alone (2247–2361); V07 = my Apollo demo, research → enrichment → Integrations, on through "connect it to AI tools" (2413–2511); V08 = Claude ↔ Apollo dashed line, TEAM KNOWLEDGE box greys out, then context connects to Claude (2511–2727), no circle, no small tags; V10 = Flow video in his browser (2883–3017). V09 not reviewed: left as A-roll. Adjustment clips go on empty V7 (patch move needed). Built so far: `Graphics\Visuals v3\M2 demos\` — `apollo2.html` (#v01, #v07), `claude_email.html`, `render2.py`, `sheet.py`; renders `V01-V02 Apollo demo (Editor).mov` and `V07 Apollo demo (Editor).mov` (started in the background; check they exist). Company names in the demos are fictional. Next: check the email stills (`sheet_v03e.jpg`), render it, zoom adjustment clips from the `*_path.json` cursor paths, V05 shots, the Fusion comps, placement, Flow.
- 2026-10-02 12:45 — Marker 2 built on *Visuals v1 (Editor)* from Samuel's review (Editor). Timeline length unchanged (13,194); only V2, V3 and V7 touched, all inside 952–3017.
  - **V01+V02** 952–1307: V2 `V01-V02 Apollo demo (Editor).mov` (my Apollo Find companies page, `M2 demos\apollo2.html#v01`): Employees 101-200 → Computer software → United States on his words (191K → 23.4K → 5,038), list scrolls, Send email hover, the twins Quillstream and Brightfold ticked, cursor across their employees / industry / country. V7 adjustment clip `Transform_Zoom` follows the cursor (1.0–1.34).
  - **V03** 1307–1558: V3 transparent base + Fusion comp (`M2 comps\build_V03.py`): the two twin cards slide in from the left and right over Alex, same facts; A's tags HIRING SALES TEAM / NEEDS PIPELINE on its words while B dims, then B's SALES TEAM IN PLACE / PROCESS WORKS. **Email part** 1558–1749: V2 `V03 email demo (Editor).mov` (Claude writing one email to both because they match the same filters) + V7 zoom.
  - **V04** 1890–2013: V3 base + comp (`build_V04.py`): three question pills (cream / orange / graphite, ? badges), pop on each question, pop out at the end. No header pill.
  - **V05** 2074–2247: V2 full-screen shots — call recording (my call-recorder screen with Alex's B-roll C0144 as his tile, 2074–2096), team (IMG_2402 cropped 16:9, 2096–2126), Notion campaign notes (2126–2165); then V2 base + comp (`build_V05.py`) 2165–2247: CALLS / TEAM'S HEADS / CAMPAIGN NOTES lines stall short of THE TOOL, which greys out with an X.
  - **V06** 2247–2361: V3 base + comp (`build_V06.py`): COMMON CONTEXT alone, NeoTextMotion two-tone + Neo Glow on his Down fade (end colour changed from his blue to the deep orange).
  - **V07** 2413–2511: V2 `V07 Apollo demo (Editor).mov` (Research with AI → Enrichment → Integrations, Claude's Connect) + V7 zoom; Apollo stays on through "connect it to AI tools".
  - **V08** 2511–2727: V2 base + comp (`build_V08.py`): Apollo and Claude tiles joined by his dashed line, TEAM KNOWLEDGE box shows and greys out, relights on "give it that context" and its line connects to Claude.
  - **V10** 2883–3017: generated in his Flow (project "Oct 02 - 12:36", 2 takes, 8 s, 720p). Download waits on his yes.
  - V09 (not reviewed) left as A-roll. The overlays sit on transparent base clips, not adjustment clips: the Fusion page won't open an API-inserted adjustment clip ([[03-Areas/video-editing/resolve-automation-lessons|lessons]]).
- 2026-10-03 — Editor: Samuel's ten blue marker notes on 952–3017 built on *Visuals v1 (Editor)*. Builders and settings are in the job's `Graphics\Visuals v3\M2 fixes\` (`m3kit.py`, `build_zooms.py`, `build_pills.py`, `build_VC.py`, `build_VG.py`, `build_glass.py`). Overlays sit on transparent base clips that read the layers below. Everything goes in and out with his Neo Anim. Timeline length unchanged (13,194).
  - **952–1063** Apollo demo re-rendered at 111 f and slower (`M2 demos\V01b Apollo demo 111f (Editor).mov`, ReplaceClip on the V2 item): United States filter, list lands at 5,038 on "5,000 companies", cursor over the three filters. Smooth eased zoom on V8 (`Z01`).
  - **1063–1190** Alex + Renat strategy-session B-roll on V2 (src 113 s, zoom 1.22, Renat pointing at Alex's screen) + V3 pills that type on: WHICH ONE SHOULD WE CONTACT? / WHAT SHOULD WE SAY TO THEM? (`VB`).
  - **1190–1558** two frosted-glass company cards on V3 (`VC`): QUILLSTREAM from the left, BRIGHTFOLD from the right, rows on employees / industry / country, shine on "similar in a database", A grows to HIRING SALES TEAM / NEEDS PIPELINE while B dims, then B grows to SALES TEAM IN PLACE / PROCESS WORKS while A dims, both out by 1556. The old V03 base clip was replaced.
  - **1894–2015** three question pills on V3 (`VD`), typing on per question, earlier ones dim. The old V2 V04 clip (rendered as an orange wash) is disabled.
  - **2166–2247** glass panel INTO THE WORKFLOW on V3 (`VE`): calls / team's heads / campaign notes outside an empty WORKFLOW box, AI TOOL greys out with a cross on "isn't going to use it". The old V2 V05 pill clip is disabled.
  - **2413–2511** smooth zoom + Brightness Contrast focus on Research, then Enrichment, then the Claude card, on V8 (`Z07`). The old V3 cursor-follow adjustment clip is disabled.
  - **2511–2727** lower third on V3 (`VG`): Down fade, real Apollo + Claude logos in medallion pills, dashed link, TEAM KNOWLEDGE box greyed then lit with an arc into Claude, DECISION RULES box on "make decisions"; boxes shine. The old V2 V08 clip is disabled.
  - **2727–2769** Flow B-roll from his browser (project "Oct 02 - 12:36", "Sales manager typing on laptop", 1080p): `B-roll\Flow - sales manager updating laptop (2727).mp4`, frames 120–163, V2; pool item in *AI Vids*.
  - **2769–2883** glass panel THE NEXT LIST on V3 (`VI`): AGENCIES UNDER 10 STAFF gets a BAD FIT stamp, arrow into the list, the two AGENCY rows struck through and faded.
  - **2883–3017** strategy-session B-roll on V2 (src 264 s, zoom 1.5, pan −150): Alex and Renat discussing.
  - Check renders: `Graphics\Visuals v3\_qa\M2_fixes_fA–fD.jpg`. Disabled leftovers to delete when he's happy: V7 952 and V3 2413 adjustment clips, V2 base clips at 1894, 2166 and 2511.
