---
type: log
area: scripnals
status: active
updated: 2026-09-22
source: manual
tags: []
---

# Log — scripnals

Append-only. Newest at the bottom. Format: `- YYYY-MM-DD — what happened`.

- 2026-09-20 — Area created during the Brain build.
- 2026-09-22 — Samuel: devs still building for free; the app is taking good shape and may be tested by people this year. Outside the Big 3.
- 2026-09-22 — Phase 3 interview, short version. Samuel is the founder. Two devs (backend, frontend), unpaid, equity intended. Test order: mentees, then waitlist. The survey was sent and got many responses; Samuel will draft them in. Monetisation undecided, and no goal until tester feedback comes in. The Feb 2026 architecture PDFs were read → [[03-Areas/scripnals/technical-architecture|Technical architecture]]. The full build walkthrough is deferred to a dedicated Scripnals session later today.
- 2026-09-22 — Scripnals session. Samuel supplied the latest APK (`LATEST/HighSignals.apk`), which was installed on BlueStacks and walked screen by screen with a test account → [[03-Areas/scripnals/current-build|Current build]]. The PRD and Product Master Document were read with his go-ahead. Headline: the build follows the master doc's onboarding fork and voice capture, but has no Script Formatter, and the AI scoring and rewrite are generic.

- 2026-09-22 — Samuel's requests to the devs in their chat (07:07–10:07 WAT), **none done yet**, per Samuel. **Fixes:** after an update, send people back to login (he got "Post not found" until he logged out and in) · rename the APK to Scripnals and add version numbers · a new logo with more padding (Samuel sends it 2026-09-23; his Canva subscription had lapsed) · auto-scroll the live transcript as the person talks · a taller, gold waveform · a 3-2-1 countdown to cover the delay before transcription starts · editing a saved script reopens the full Scripting page (AI button, voice, content type) and **updates** the script instead of creating a new one, with the button reading "Update" · too much empty space at the top of the home screen (tagged to Alisha Prescious). Then *"I want us to focus on the AI now"*: the AI panel, score only on full review, user instruction first (→ [[03-Areas/scripnals/scripnals-decisions|Decisions]]). He told the devs he'd send *"a document where the AI gets all it's references from on how to format the scripts"* **before this week runs out**, and that he's *"sharing this version with my mentor and other advisors this week"*.
- 2026-09-22 — Checked against [[03-Areas/scripnals/current-build|Current build]]: his requests already cover versioning (problem 2) and part of the naming. Not yet raised with the devs: the permanent package ID (1), the voice recorder hanging silently (3), Render cold starts (4), and small bugs 5–12.

- 2026-09-22 — AI spec v1 approved (→ [[03-Areas/scripnals/ai-workflow|AI workflow]]). Samuel is sending the walkthrough bugs to the devs as a direct message: problems 1–12 in [[03-Areas/scripnals/current-build|Current build]], plus the AI output issues.

- 2026-09-22 — The AI spec was reworked at Samuel's request: a left-to-right flow chart (App → Server → App lanes, chosen over a vertical chart and a three-column swimlane), UI mock-ups of the panel and the results, **the master prompt added** (the system prompt that uses all the context), no examples, fewer and simpler words. Sources are in `03-Areas/scripnals/assets/`, images in `_attachments/scripnals/`.

Back to [[03-Areas/scripnals/scripnals|Scripnals]]
