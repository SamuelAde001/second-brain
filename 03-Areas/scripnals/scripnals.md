---
type: area
area: scripnals
status: needs-input
updated: 2026-09-22
source: project-handover
tags: []
---

# Scripnals

## What this is

An AI scripting and ideation app for content creators, and one of the four branches of the HighSignals brand ([[03-Areas/highsignals/highsignals|HighSignals]]). Source: the Scripnals project-setup doc, 2026-07-23.

**The core loop:**
1. **Input** — the user records a voice note about a content idea, or types a draft directly.
2. **Processing** — AI transcribes the voice note (or takes the typed draft) and turns it into a working script, using stored context about that user's audience and content type.
3. **Output** — a refined, ready-to-use script formatted for that creator's actual content type.

**The promise:** remove the friction between having an idea and having a usable script, so recording or writing is never the bottleneck.

## Why it matters

Positioned as the daily execution tool — the last stage of the ascension model (Academy → Community → Mentorship → App). The other branches teach, support and personalise; this is where the day-to-day doing happens.

## Current status — as of 2026-09-22

Samuel, 2026-09-22: the developers are **still building it for free**; *"the app is starting to actually take good shape"* and **may be tested by people this year.** Outside his Big 3 ([[02-Me/goals/goal-ladder|Goal ladder]]).

**A dedicated Scripnals session is planned for later on 2026-09-22.** Samuel will go through exactly where the build stands and what comes next. Build status, what works today and the roadmap are all left for that session.

### Team

- **Samuel is the founder.**
- **Two developers:** one backend, one frontend. Neither is paid now. Samuel: *"I would surely pay them in equity"*. No split has been set.
- Two contract files from 2026-02-08 are on disk, both unsigned: a developer agreement "awaiting developer signature" and a development contract. Whether anything was signed later is unknown (open question 69).

### Testing plan

**Mentees first, then the waitlist** (Samuel, 2026-09-22). The mentees are in [[03-Areas/mentorship/mentorship|Mentorship]].

### Build, as far as the Brain knows

- **Spec:** the February 2026 MVP architecture — React Native (Expo) mobile, Node.js + Express, PostgreSQL, GPT-4o-mini via LangChain. Samuel says it needs updating. It describes an auditor and streak tracker, **not** the voice-to-script loop → [[03-Areas/scripnals/technical-architecture|Technical architecture]].
- **APKs:** two on disk, `HighSignals (1).apk` (2026-08-10) and `HighSignals.apk` (2026-08-26). Samuel can't say whether either is current. So Android is built. iOS is unknown.

### As of 2026-09-20

**Unknown and unverified.** The Brain holds product positioning only. No build status, no stack, no validation evidence, no roadmap, no metrics. There is a `Desktop/HighSignals/HighSignals App/` folder containing an APK and `Frontend_and_Mobile_Technical_Architecture_MVP1.pdf` that has not been inventoried — that suggests a build exists, but nothing here confirms how far it got.

## Two audiences

Both matter for every product, copy and positioning decision:

1. **Ecosystem members** — already inside Academy / Community / Mentorship, and expect Scripnals to reinforce what they learned there.
2. **Standalone creators** — have never heard of HighSignals, and need the app to sell itself on utility alone.

**Rule from the source doc:** onboarding, features and marketing copy work for a standalone creator first. The HighSignals connection is a quiet layer underneath, never the headline.

## Product filter

"Signal from the noise." Every feature either reduces friction in the creation process, or increases the odds the finished content lands. A feature that does neither gets questioned before it gets built.

## Build bias

Get the core voice-to-script loop working solidly **before** layering in audience-aware personalisation. Do not let scope balloon before the core loop is proven.

## Naming

"Script" + "Signals". Ruled out along the way: signal/frequency words (Wavelength, Tune, Beacon), transformation words (Hone, Kiln, Etch — naming conflicts), and ScriptFlow (a near-identical app already in market).

## Open questions

Marked TBD in the source doc:

- Monetisation model: subscription, freemium, one-time, or bundled with ecosystem membership? **Samuel, 2026-09-22: not decided yet.**
- Platform: iOS, Android, or both? Partly answered: the spec is React Native (Expo), which can target both, and Android APKs exist.
- Pricing relative to Academy / Community / Mentorship. **Not decided** (2026-09-22). The NGN 15,000–25,000 tiers in the survey were a draft, not a decision.
- Actual build status, and whether anyone outside the team has used it. Saved for the Scripnals session.

## Source material on disk (not imported)

`Desktop/HighSignals/HighSignals App/`, listed 2026-09-22 by filename only. Only the three architecture PDFs have been read.

- `HighSignals_PRD.md.docx` and `HighSignals app document for dev.pdf` (2026-02-02)
- `Scripnals Product Master Document.pdf` (2026-07-25). Probably the "master doc" that the survey cites for the persona split and the NGN pricing tiers ([[03-Areas/scripnals/validation|Validation]])
- The two unsigned dev contracts (2026-02-08), a domain payment invoice (2026-01-16), and design images (2026-02-17)
- The two APKs, plus an `APK/` folder and a `New folder/` (2026-09-14)
- A Google Cloud credential file. Never read, and flagged in [[00-System/security-flags|Security flags]]

## Map of content

- [[03-Areas/scripnals/technical-architecture|Technical architecture]] · [[03-Areas/scripnals/validation|Validation]]
- [[03-Areas/scripnals/scripnals-ideas|Ideas]] · [[03-Areas/scripnals/scripnals-decisions|Decisions]] · [[03-Areas/scripnals/scripnals-log|Log]] · [[03-Areas/scripnals/scripnals-goals|Goals]]

## Related areas

- [[03-Areas/highsignals/highsignals|HighSignals]] — the umbrella
- [[03-Areas/community/community|HighSignals Community]] · [[03-Areas/academy/academy|Academy]] · [[03-Areas/mentorship/mentorship|Mentorship]] — sister branches
- [[03-Areas/personal-brand/personal-brand|Personal brand]] — outside HighSignals, funnels into it
