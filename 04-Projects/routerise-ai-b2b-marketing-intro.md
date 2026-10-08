---
type: project
area: video-editing
status: active
updated: 2026-10-08
source: manual
tags: [client, routerise, intro, hook]
---

# Route Rise — AI B2B Marketing: the intro (hook)

Part of [[04-Projects/routerise-ai-b2b-marketing|the AI B2B Marketing job]]. Back to [[03-Areas/video-editing/video-editing|Video editing]].

Samuel, 2026-10-08: *"I want you to start the intro, but not in this session, in another session with the same intensity that you gave this one ... you did a good Job here and I belive you can handle the intro also"*. This overrides "every intro is Samuel's" for this job only ([[00-System/decisions|decision]], 2026-10-08). A second session finishes the rest of the edits at the same time ([[04-Projects/routerise-ai-b2b-marketing|job note]] → RESUME).

## What the intro is

- **Frames 0–2494** of the approved cut (1:44 at 23.976 fps), 32 A-roll clips on V1. Every timeline (*Visuals v1* … *Visuals v3 adj 5*) has **nothing on V2+ before 2495**: it is plain A-roll. Visuals after it start at 2495 (the section slam + the chapter lower third *WHAT WE TELL EVERY NEW CLIENT*).
- **The words, frame by frame:** job `Docs\Editor working files (2026-10-08)\hook_words_0-2494.txt` (from `words_v5.json`, an ASR transcript: "odd bound(s)" = outbound, "lens" = lands). Alex's recording script (`Docs\Editor working files (2026-10-06)\script.txt`, the hook section) settles the real words and carries **his on-screen plan** for the hook. Read it first.
- **What Alex says, in beats:** pipeline flat for months → the usual fixes (more cold email, another SDR, a new AI tool, LinkedIn ads, LinkedIn content) and nothing moved → most buyers pick their favourite vendor before they talk to sales, and that vendor wins about 80% of the time → getting B2B tech companies in front of those buyers first is what Frontal does, with more than 250 of them, and Frontal runs the same process for itself ("we eat our own dog food") → in 2026 that's the minimum: buyers avoid irrelevant outreach, cold email alone barely gets replies → this training: exactly what Frontal would do if you signed tomorrow, step by step from kickoff to the end of the first quarter, with real numbers, the tools and where AI does the work → Ivan, head of ABM, runs ads on the same account list as outbound, so buyers know you before the first email lands → almost nobody on YouTube talks about it, because ads and outbound sit in two teams that never talk → step 4: the signal mistake almost every company makes.
- **Facts to keep straight:** "250+ B2B companies" only as written (Alex's production note); no music under the voice (his note; Samuel's sound plan puts music on its own track); logos allowed (Samuel settled it with Alex, 2026-10-07); sales-call people anonymous. The 80% claim also gets the 6sense pie at 3484 (built 2026-10-08): if the intro shows 80%, make it a different device or a deliberate echo, never the same pie twice.

## Samuel's bar for an intro

- **Start from [[03-Areas/video-editing/edit-grammar/edit-grammar|Edit grammar]]** (the study of his three finals: triggers, rhythm, constructs with exact settings, MagicZoom). Do not re-study his videos; open a template or a still only to copy the construct you are building. His comps and finals stills are also in `Routerise\Visual Assets\Samuel templates (Editor)\` (shared copy).

- His finished hooks are the reference: Apollo (0:00–0:41), 4 AI Tools, Taking a Step Back. Their comps are in the job's `Graphics\Visuals v1\comps\his\templates\` (`apollo_*`, `ai4_*`, `tsb_*` at low frame numbers); stills in the old scratchpad `qa3\his_finals\` (copy what you need into the job folder, the scratchpad is temporary); his $7M Founder comps in `Routerise\Claude Files\Style Study - Cold Outreach\raw\comps\`.
- [[03-Areas/video-editing/ways-of-working|Ways of working]]: "Premium means the hook's look" (two-tone Geist ExtraBold titles with glow, glass pills with an orange border, orange numbered circles, ghost numerals, orange icons, curved white arrows…), node layout rules, UI demo rules, motion rules. [[03-Areas/video-editing/routerise-house-style|House style]] §11b (pacing). [[03-Areas/video-editing/motion-gallery/motion-gallery|Motion gallery]] (a vocabulary to remix, never templates). The B2B build list and grammar (job `Docs\Build list v3 (2026-10-07).md`, `Docs\Grammar - Samuel's last three timelines (2026-10-07).md`).
- An intro is denser than the body: a visual every few seconds, real things on screen (the tools named, the people, the 80% stat with its source, Frontal's site, Ivan), his premium chain on every graphic, every element landing on its word.

## How to build it (same machinery as the body)

1. **Plan:** a visual per sentence, from his hooks' grammar and Alex's on-screen plan. **Show Samuel a rendered-stills storyboard (one still per visual) and get his go before building** (the profile's storyboard gate). Ask choices with defaults; he answers fast.
2. **Build** in its own folders: `Graphics\Visuals v1\comps\intro\H0_intro\` and `renders\intro\H0_intro\`, with a `manifest.json` in the v3 op format. Keep it **out of `comps\v3\`** until Samuel approves: the other session's `kits\inst\round_install.py` applies every `comps\v3\*\manifest.json`.
3. **Install** on your own duplicate timeline (e.g. *Intro build (Editor)*, duplicated from the newest *Visuals v3 adj N*), never on *Visuals v3 adj 2* (the other session's working timeline) or an *adj N*. Paste with `kits\ext_kit.py` / `kits\apply_manifest.py <manifest> "<your timeline>"`, convert comps to adjustment clips with `kits\drt\export_drt.py` → `convert.py` → `import_drt.py`, gate with `kits\inst\identity.py` and `rawbreaks.py`, stills with `kits\inst\stills_safe.py`, chain with `kits\qa_v3.py chain`.
4. **Review** from timeline stills against his finals, with adversarial verifiers; fix; repeat until clean.
5. **Hand over:** when Samuel approves, copy the folder into `comps\v3\H0_intro\` and tell the edits session (or Samuel) so the next main install picks it up.

## Shared Resolve: take the lock

Two sessions drive one Resolve. Before any Resolve step that writes, renders stills, switches timelines or projects: `python kits\inst\resolve_lock.py acquire intro` (it waits while the other session holds it); afterwards `python kits\inst\resolve_lock.py release intro`. If the open project isn't this job's, ask Samuel before switching.

## Lessons from the body build (2026-10-07/08), all in the Brain

- [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] (bottom sections): identity gate after every paste, `sync_plan` before re-applying, raw line breaks in Lua strings, `Char1Enable` for two-tone, 24 fps Flow clips on the 23.976 timeline, MagicMask must be tracked in the GUI or it hides everything above it, Resolve's slow shutdown, Chrome's Save As for Flow downloads.
- [[07-Agents/video-editor/memory|Editor memory]] (2026-10-08): markers are part of the brief, parallel builders burn the 5-hour window fast (run 3–5 at a time, check usage before a fan-out), ask before switching his Resolve project.
- Flow (Omni Flash, ~12 credits a clip) in his Chrome is allowed for this job (Samuel, 2026-10-08); downloads open a Save As dialog he clicks.
