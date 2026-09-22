---
type: knowledge
area: scripnals
status: needs-input
updated: 2026-09-22
source: local-folder
tags: [architecture, stack]
---

# Technical architecture — MVP spec (February 2026)

What the devs were given to build. Read 2026-09-22, with Samuel's go-ahead, from three PDFs in `Desktop/HighSignals/HighSignals App/` (files dated 2026-02-09):

- `HighSignals Backend Technical Architecture MVP.pdf` — the main spec
- `Frontend_and_Mobile_Technical_Architecture_MVP1.pdf` — the frontend spec
- `Frontend_and_Mobile_Technical_Architecture_MVP2.pdf` — a shorter version of MVP1 with a request-flow diagram. Nothing new.

The docs were written while the app was still called **HighSignals**. The Scripnals name came in July 2026.

**Samuel, 2026-09-22:** *"the MVP architecture might need some changes, I haven't updated it since a while."* So this is the plan as written in February. It is **not** a description of what the current build does. Whether the APK follows it is unknown.

## Stack, as specified

| Layer | Choice |
|---|---|
| Mobile | React Native (Expo), TypeScript, React Navigation, Zustand (state), Axios, Expo SecureStore |
| Web / admin (optional) | Next.js (App Router), TypeScript, Tailwind CSS |
| API | Node.js + Express, REST. Zod validates every request |
| Database | PostgreSQL |
| Cache / timers | Redis (sessions, the 24-hour streak countdown) |
| Auth | Google OAuth via Passport.js, then a JWT on every request |
| AI | OpenAI GPT-4o-mini through LangChain.js. Picked for low cost per call and structured JSON output |
| Background | A worker that runs the streak check every hour |

**The rule the whole spec rests on:** clients only talk to the Node.js API. They never touch a model or the database directly. All AI runs on the server, for security, cost control and consistent personalisation.

## Data model

- **users** — id, email, password_hash, google_id, created_at
- **icp_profiles** (one per user) — niche, pain_points, dreams, content_pillars (jsonb)
- **posts** (many per user) — content, status (idea / draft / published), score, feedback (jsonb), published_at
- **streaks** (one per user) — current_count, longest_count, freezes_available, last_activity

## The two flows it builds

1. **AI audit.** The user submits a draft. The backend loads their ICP profile and builds a prompt from an auditor role, the ICP context and the post. It sends that through LangChain and gets back a score plus tips as JSON. User input never goes straight to the model.
2. **Streaks.** Publishing a post bumps the streak. Every hour, a check finds anyone who hasn't posted in over 24 hours. If they have a freeze, one is used. If not, the streak resets.

## Endpoints (proposed)

`POST /auth/google` · `GET /auth/google/callback` · `POST /auth/logout` · `GET /users/me` · `GET|PUT /icp` · `POST /posts` · `PUT /posts/:id` · `POST /posts/:id/audit` · `POST /posts/:id/publish` · `GET /posts` · `GET /streak` · `POST /streak/freeze`

AI calls retry automatically. If the model is down, the user sees "try again later" and the app keeps running.

## Where the spec and the current product disagree

My reading, not a decision. For the Scripnals session.

- **The core loop isn't in it.** Since July, Scripnals has been pitched as voice note (or typed draft) → AI script, formatted for the creator's content type ([[03-Areas/scripnals/scripnals|Scripnals]], [[03-Areas/scripnals/validation|Validation]]). The February spec has no audio upload, no transcription, no script-generation endpoint and no content-type formatting. What it specifies is an **auditor plus a streak tracker**.
- **The Content Auditor does match.** `POST /posts/:id/audit` is the auditor that the memory export lists as in scope and calls the core differentiator.
- **Streaks appear nowhere in the Scripnals positioning.** They are either a feature that was dropped or one nobody wrote down.
- **The spec runs against the recorded build bias.** The Scripnals note says to get the voice-to-script loop solid before adding audience personalisation. The spec builds the personalisation (ICP profiles) and leaves out the voice loop entirely.
- The frontend doc names "LangChain / LangCast". I don't recognise LangCast as a framework, so check with the devs whether it's a typo.

Back to [[03-Areas/scripnals/scripnals|Scripnals]]
