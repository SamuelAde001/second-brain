---
type: client
area: video-editing
status: needs-input
updated: 2026-09-20
source: claude-export
tags: [client]
---

# Routerise

**Status:** active
**Contact channel:** needs-input — not stated in the source documents.
**Since:** needs-input — not stated. Earliest dated reference in the source material is 2026-09-14 (house style study established).

> **Open question — who "Routerise" actually is.** The source documents are inconsistent and this is not resolved. `routerise-alex-START-HERE.md` states, in its own project-context table: "**Client** | Alex — runs **Frontal**, a B2B agency; has worked with 250+ B2B companies" and "**My company** | Routerise" — i.e. read literally, Routerise is *Samuel's own* company/editing brand, and Alex (who runs the agency Frontal) is the client. `routerise-fusion-node-system.md` likewise labels the project "client: **Alex / Frontal**". But `routerise-cut-workflow.md` writes "Client: Routerise / Alex (Frontal)", and three separate cut sheets refer to "the Routerise dropshipping video," the *Routerise "$0–10K Profit"* video and *Routerise "How to Start an AI Ecommerce Brand in 2026"* — none of which are B2B lead-gen/Frontal content, suggesting Routerise is a channel or umbrella brand that carries more than one topic. Also: "Accent colour `#FF5A1F` for Frontal. **Accent changes per client**" implies Routerise itself may serve more than one client, of which Frontal/Alex is one. This note is filed as instructed (Routerise = client), but the actual relationship between Routerise, Alex and Frontal needs Samuel to clarify before it's treated as settled.

## What they hire me for

- Long-form talking-head YouTube tutorials with a live screen-recorded demo section. The reference project (Alex/Frontal, B2B cold outreach) runs **~7–8 minutes**.
- Longer-form content also produced under the Routerise name: *"How to Start an AI Ecommerce Brand in 2026"* (33:56 total) and a dropshipping video referred to as *"$0–10K Profit"* (33:46 total, cut sheet covers 21:39→end) and *"Claude Dropshipping Guide 2026"* (27:46).
- So the account spans at least two content lines: B2B lead-generation/cold-outreach tutorials (Alex/Frontal) and AI-ecommerce/dropshipping tutorials — both built around screen-recorded demos of AI tools plus talking-head A-roll.
- Full pipeline work: editing, Fusion graphics builds, and cut-sheet pre-production planning (shot-by-shot visual plans built before/alongside the cut). See [[03-Areas/cut-sheets|Cut sheets]].

## Brief style

needs-input — no source document describes how Alex/Routerise actually briefs Samuel for a new video (what arrives, how complete it is, what's missing). The closest material is the **cut sheets** Samuel himself builds against "the client's actual asset folder" (see [[03-Areas/cut-sheets|Cut sheets]]), which imply the client hands over raw footage/screen recordings plus a written script, and Samuel has to reconcile it — see "Quirks" below.

## Preferences

- **Pacing / style:** cuts only, no transitions ever (confirmed zero dissolves/wipes across 503 clips in the reference project). A-roll cut to a ~2.4 s median, holding up to 11 s when a point earns it, machine-gunning sub-second cuts for emphasis. Full detail in [[03-Areas/routerise-house-style|Routerise house style]].
- **Zooms:** **MagicZoom V3, never Dynamic Zoom.** Samuel's own words on this account: *"I prefer MagicZoom V3 instead of Dynamic Zoom, I use it for slow zooms, and quick punch ins and the speed and depth of the zoom differs in different contexts."*
- **Captions/typography:** word-by-word animated text (NeoTextMotion / NeoAnim), ALL CAPS bold for chips and titles. Brand font is **Geist** (Alex's brand font — confirmed by Samuel, replacing the ad-hoc Open Sans seen in the first reference cut). Full detail in [[03-Areas/routerise-house-style|Routerise house style]].
- **Music:** Epidemic Sound tracks, one track per script section/chapter, changing on the exact section boundary; level set once per track (−25 to −42 dB), never automated per clip.
- **Graphics must be built as native Fusion nodes, not raster.** Dated rule from the TSB project: *"graphics are always nodes… No PNG sequences or rasterised graphics standing in for a visual"* — raster/PNG-sequence fallbacks from Samuel's compiler tooling were explicitly rejected as unacceptable output and had to be rebuilt as real node trees. (See [[03-Areas/tsb-graphics-pipeline|Tsb graphics pipeline]] — note that document does not itself confirm it is Routerise work; flagged there.)
- **B-roll sourcing:** real-world B-roll from **YouTube and TikTok only — no stock libraries** (stated house style on two separate cut sheets).
- **Show over tell**, with explicit calls for when to cut back to A-roll (recurring instruction across cut sheets).
- **Accent colour is per-client/per-brand**, not fixed: `#FF5A1F` for Frontal specifically; fill = accent × ~0.10, border = the accent itself.

## Things they always ask for

- Editable graphics (nodes, not rasters/PNG sequences) — TSB project rule.
- Cut-sheet-style pre-production: every VO line mapped to a picture, with explicit zoom/text-on-screen/cut-back-to-A-roll callouts, before or alongside the edit.
- Privacy handling: specific timestamps get blurred/cropped for PII (email, phone, credit card, business address, store URLs) — seen in the AI Ecommerce Brand 2026 cut sheet's blur list.
- Screen recordings that don't betray the client's OS: client shoots on **macOS** (screen recordings at 3456×2234 @ 60fps retina); Samuel edits on **Windows**, so any of his own browser-based inserts must be recorded in **Chrome, F11 full screen**, so no window chrome gives away the OS mismatch.

## Things they hate

- Raster/PNG-sequence graphics standing in for a "real" (editable) visual — explicitly called out as not acceptable.
- Dynamic Zoom (MagicZoom V3 is the standing substitute).
- Transitions of any kind on A-roll.

## Rates and terms

- Rate: needs-input — not stated anywhere in the source documents.
- Turnaround: needs-input — not stated.
- Revision rules: needs-input — not stated.
- Invoicing and payment: needs-input — not stated.

## Quirks

- **Alex sometimes names a tool on camera that doesn't match the footage actually supplied.** Happened at least twice: he says "Higgsfield" on camera in one video while all available footage is Arcads (flagged in the $0–10K cut sheet as needing crop/blur of every Arcads string so the tool name on-screen never contradicts the VO); the same mismatch (Higgsfield vs. Arcads) recurs in the AI Ecommerce Brand 2026 cut sheet, noted there as *"Same trap as the last project"* — confirm which tool the footage actually shows before cutting, every time.
- **Written script and spoken VO diverge**, and the rule is to cut to the VO, not the script — e.g. the AI Ecommerce Brand 2026 script says a $50/day ad budget, VO says "$50–$100/day"; script says paste a custom connector URL, VO says browse connectors and search "Facebook Ads."
- **On-screen numbers get rounded in VO** — e.g. margin figures shown on screen as $64.99/$8.00/$6.00/$2.18/$16.18/$48.81/~75% get rounded to "$2," "$16," "$48" when spoken; the cut sheet rule is to show the file's real numbers, because a later VO callback (32:14) depends on the exact $48.81 figure. Same pattern on the $0–10K video: break-even shown on screen is $59, not the $32–$38 that appears in the written script — use $59.
- **Footage often arrives incomplete.** Every cut sheet reviewed ends with a ranked "still needed from client" list (e.g. real UGC ad renders, Ads Manager screen capture with all columns on, community-platform screen capture, specific end-card videos) — getting a cut sheet approved does not mean the footage to execute it exists yet.
- **Some assets are explicitly unverified and need confirming before use** — e.g. `mcp.facebook.com/ads` flagged in Alex's own script as unverified; must be confirmed before showing it "connect" on screen.
- **Mic setup varies shoot to shoot without being a fixed rule.** Two separate lavalier files (`TX02_MIC012`, `TX02_MIC013`) turned up in one project's timeline — confirmed by Samuel to be "just whatever audio Alex supplied," not a deliberate two-mic convention.
- **Camera audio is occasionally unusable.** On the 13 Sep shoot the camera's scratch audio was dead (flat noise floor at −62 dBFS, no speech), which breaks waveform sync entirely and forces a fallback motion-correlation sync method — see [[03-Areas/sops/routerise-cut-workflow|Routerise cut workflow]].
- **Deadline pressure can override the usual Fusion-heavy approach** — the $0–10K back-half cut sheet explicitly notes "no complex Fusion work (deadline-constrained)" as a house-style adjustment for that specific cut.

## Work history

Dates are not stated in the source documents except where noted; do not infer an order beyond what's given.

- 2026-09-14 — house style study conducted against the reference project *"$7M Founder: How I Use Claude for Cold Outreach (B2B sales)"* (Alex/Frontal) — [[03-Areas/routerise-house-style|Routerise house style]], [[03-Areas/fusion-node-system|Fusion node system]]
- date not stated — SOP for the cut workflow (sync → silence removal → transcribe → remove bad takes) established and written down, dated only as "Established 14 Sep 2026" — [[03-Areas/sops/routerise-cut-workflow|Routerise cut workflow]]
- 2026-09-19 — TSB graphics-pipeline work (Timeline 2, 3:06–10:40): native-Fusion rebuild of `lego2` and `accounts`, plus the wider raster→native-node conversion effort. **Client attribution for this document is itself unconfirmed** — see [[03-Areas/tsb-graphics-pipeline|Tsb graphics pipeline]]
- date not stated — cut sheet built for *Routerise "$0–10K Profit"* (back half, 21:39→33:46) — see [[03-Areas/cut-sheets|Cut sheets]]
- date not stated — cut sheet built for *Routerise "How to Start an AI Ecommerce Brand in 2026"* (full video, 00:00→33:56) — see [[03-Areas/cut-sheets|Cut sheets]]
- date not stated — visual-direction/gap-analysis pass on *"Claude Dropshipping Guide 2026"* against an approved reference cut of the same creator/style — see [[03-Areas/cut-sheets|Cut sheets]]

## Revisions log

No revision requests are recorded in the source documents. needs-input if Samuel wants this tracked going forward.

Back to [[03-Areas/video-editing/_index|Video editing]]
