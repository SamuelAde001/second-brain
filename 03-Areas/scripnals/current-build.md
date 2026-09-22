---
type: knowledge
area: scripnals
status: active
updated: 2026-09-22
source: local-folder
tags: [build, walkthrough, audit]
---

# Current build: what the app does today

Walked screen by screen on 2026-09-22 by the main session, with Samuel watching. **This note records what the build does.** The two spec docs describe what it was meant to do. Where they disagree, this note is the fact.

## The build tested

| | |
|---|---|
| File | `Desktop/HighSignals/HighSignals App/LATEST/HighSignals.apk`, dated 2026-09-22 (Samuel: *"This is the latest version of the app"*) |
| Package ID | `com.ayomiplenty.highSignals` · versionCode 2 · versionName 1.0.0 |
| App name | Scripnals. The URL scheme is `scripnals://`, the Expo slug is `highSignals` |
| Stack, read from the bundle | Expo SDK 54, React Native with the New Architecture, expo-router, Hermes. Google Sign-In. On-device speech via `expo-speech-recognition` |
| Backend | `highsignals.onrender.com` (Render) |
| Tested on | BlueStacks, Android 9. A new test account Samuel signed up. All the answers were made-up test data |

**Every build since May 2026 carries the same version stamp** (versionCode 2, 1.0.0). Six older APKs are on disk, and only their file dates tell them apart.

## Verdict in one paragraph

The build follows the **July master doc** more than the February PRD. It has the onboarding fork, a text editor, a voice recorder, content types and the auditor. The PRD's streaks are gone. What's missing is the heart of the master doc: **there's no Script Formatter.** Nothing turns a brain-dump into a structured `[HOOK] / [VISUAL CUES] / [BODY] / [CTA]` video script. The AI does two things. It **scores** a draft and it **rewrites** it, and the rewrite comes out as a caption-style text post, not a video script.

## Screen by screen

1. **Welcome.** An animated gauge shows "CONTENT SCORE 98", with *"Publish with Confidence. The only mobile AI that audits your content before you post."* Continue with Google / Continue with Email. The screen never shows the name Scripnals. ![[scripnals-2026-09-22-01-welcome.png]]
2. **Email auth.** Login / Sign Up tabs, email and password, Remember me, Forgot Password (there's a reset-password endpoint), and Google.
3. **Onboarding fork.** *"Which defines your goal of creating content?"* → **Business owner/entrepreneur** ("I sell a product or service") or **Content creator** ("I build an audience and community"). ![[scripnals-2026-09-22-02-onboarding-fork.png]]
4. **Onboarding questions, 7 steps with a progress bar.**
   - *Business path, walked live:* What do you do? (one sentence) · Describe your dream client · What is the #1 problem you solve for them? · What is their dream outcome after you solve this problem? · What is your personal story or expertise in this area? · Demographics of your dream client · Anything else about your audience? (optional)
   - *Creator path, from the bundle strings, not walked:* What is the main topic you post about? · Who is your dream follower? · Why do people follow you / What is the main reason people follow you? · What is your ultimate goal for growing this audience? · What is your unique backstory or journey? · How do you want people to feel after seeing your post?
5. **ICP Profile.** Shows the raw answers under Positioning, Audience & Value and Authority, and can be edited. **No AI touches it.** There's no summary and no generated content pillars (the PRD asked for both). ![[scripnals-2026-09-22-03-icp-profile.png]]
6. **Dashboard.** "Welcome back, <name>", the date, two big cards (**Write Script**, rich text, and **Record Idea**, voice to text), a "Dashboard insight" line and Recent posts. The insight line is fixed text keyed to state ("Your ICP is still missing…", "You are set up…", "Your content pipeline is active…"). It isn't AI. ![[scripnals-2026-09-22-04-dashboard.png]]
7. **Script editor.** Title and a rich-text body, with a toolbar of H1–H3, bold/italic/underline/strike, checklist, bullets, numbers, divider, colour, undo and redo. A mic button, a **Content type** picker and a floating **AI** button. It autosaves.
8. **Content types:** Storytelling · Listicles · Quick Tip · Contrarian · Before and After · POV. ![[scripnals-2026-09-22-05-content-types.png]]
9. **AI Feedback, the auditor.** A score gauge (the test draft got **62/100**) and three tips. The footer reads **"10/10 Daily Trials Remaining"**, with a button **Generate Upgraded Version**. ![[scripnals-2026-09-22-06-ai-feedback.png]]
10. **Revamped Script.** The rewritten draft, with Discard or Insert. **Insert adds the rewrite below the original instead of replacing it.** ![[scripnals-2026-09-22-07-revamped-script.png]] ![[scripnals-2026-09-22-08-revamp-inserted.png]]
11. **Save As:** Idea ("save as a rough idea") or Scripting ("move to the scripting stage").
12. **Content List.** A pipeline with the filters **All · Idea · Scripting · Filming · Editing · Posted**, plus search, a filter button, a favourite star, and a status dropdown on each card. Delete, with a confirm. ![[scripnals-2026-09-22-09-content-list.png]]
13. **Voice recorder.** A bottom sheet reading "Start speaking to transcribe…", a mic button and Insert. Leaving mid-recording gives *Keep recording / Save draft / Discard*. It resumes an unfinished recording ("You have an unfinished recorded idea…"). ![[scripnals-2026-09-22-10-voice-recorder.png]]
14. **Profile.** Dark mode, Edit Profile (with avatar upload), ICP Profile, View Content, **Send Feedback**, Log Out. ![[scripnals-2026-09-22-11-profile.png]]

## The AI, as built

Two server endpoints, both called from the editor:

| Endpoint | What it does in the app | What went in (test) | What came out |
|---|---|---|---|
| `POST /api/ai/analyze/` | Score and 3 tips | A rambling 3-sentence draft, content type Quick Tip, a business ICP for fitness coaches | 62/100. Tips: stronger hook in the first 2 seconds · add visual cues / on-screen text / B-roll · add a clear CTA |
| `POST /api/ai/revamp/` | "Upgraded version" | The same draft | A Markdown text post: heading with emoji, a 3-step numbered list, closing line, "Repost ♻️ … follow for more" |

What I saw, not what the devs have confirmed:

- **The tips were generic.** None of them mentioned the ICP (fitness coaches, lead generation), the content type, or a specific line of the draft. The PRD example ("Cut the first sentence", "Replace 'synergy' with 'teamwork'") is the specificity it was meant to have. Whether the ICP even reaches the prompt is unknown. Ask the devs for the prompt.
- **The rewrite added content the creator never said.** The third step, "Automate: schedule your content to post daily", wasn't in the draft. The master doc says Scripnals is *"not a done-for-you writer"* and structures *"the creator's own organic thoughts."*
- **The rewrite is a caption, not a script.** No hook label, no visual cues, no spoken-script pacing. The reposting CTA fits a LinkedIn or Instagram caption, not a Reel.
- **Raw Markdown shows in the preview** (`###`, `**`). After Insert it renders as formatting, but `***` leaves a stray `*`.
- **Transcription happens on the phone, not the server.** Android uses Google's speech service, iOS uses Apple's. It's free and live, but accuracy depends on the phone and its language settings.
- **The daily limit is 10** "trials". Whether a score, a rewrite or both use one up wasn't confirmed; the counter still read 10/10 after one score.

## Built vs specced

| Feature | Feb PRD | Jul master doc | Build |
|---|---|---|---|
| Google and email auth | ✓ | — | ✓ |
| Onboarding fork (solopreneur vs creator) | — | ✓ | ✓ |
| ICP questions | ✓ 5–7 | ✓ per path | ✓ 7 per path |
| AI-generated ICP summary / content pillars | ✓ | — | ✗ stored raw |
| Rich text editor | ✓ drafting | ✓ | ✓ |
| Voice capture with live transcription | — | ✓ | ✓ built, **untested on a real phone** |
| Content types | — | implied | ✓ 6 types |
| **Script Formatter** (`[HOOK]` `[VISUAL CUES]` `[BODY]` `[CTA]`) | — | ✓ **core** | ✗ **missing** |
| Auditor: score 0–100 | ✓ | ✓ | ✓ |
| Auditor: specific feedback | ✓ 3 bullets | ✓ flags hooks, jargon, pacing | ✓ 3 bullets, generic |
| Auto-improve | ✓ "better write-ups" | ✓ 1-click | ✓ "Generate Upgraded Version" |
| AI post suggestions / ideas | ✓ | — | ✗ |
| Streaks, freezes, push reminders | ✓ | — | ✗ |
| Content pipeline | ✓ 5 states | — | ✓ Idea → Scripting → Filming → Editing → Posted |
| Free tier, limited scripts | — | ✓ | ✓ 10 per day, no paywall |
| In-app feedback | — | — | ✓ |
| Notifications | ✓ push | — | ✗ bell icon does nothing |

## Problems found

**Fix before any tester sees it:**
1. **The package ID `com.ayomiplenty.highSignals` is permanent once the app is published on the Play Store.** It puts "HighSignals" in the public store URL, which breaks the rule that HighSignals never surfaces to consumers ([[03-Areas/scripnals/validation|Validation]]). It also sits in what looks like one developer's own namespace. Change it before the first store upload. Connected to open question 69, who owns the code.
2. **No versioning.** Every build is 1.0.0 / code 2. Testers' bug reports can't be tied to a build.
3. **The voice recorder hangs on "Listening…" with no error** if the phone has no speech service (tested on BlueStacks, which has no Google app). A real phone may be fine. It needs a timeout and an error message either way.
4. **The backend is on Render.** If that's the free tier, it sleeps when idle, and the first request after a quiet spell takes 30–60 seconds. To a tester that looks like a broken app.

**Small bugs:**
5. You can skip onboarding with Back. It lands on the welcome screen, and the next launch opens the dashboard with no ICP.
6. The last onboarding question says "optional", but Complete Setup stays disabled until you type something, so only Skip works.
7. Business path Q2 ("Describe your dream client") and Q6 ("Demographics of your dream client") overlap.
8. A card's status changed in the dropdown doesn't update in the Content List until you refresh. The dashboard updates straight away.
9. The status dropdown's heading reads "Status Update Modal", which is a developer placeholder.
10. The notification bell does nothing.
11. It says "Welcome back" on a brand-new account's first visit.
12. The welcome screen never says "Scripnals".

## Not tested yet

- Voice capture on a real phone (Samuel's Android).
- The creator onboarding path, walked live.
- Google Sign-In, Forgot Password, Edit Profile and avatar, Send Feedback, dark mode, search and filters.
- What happens after 10 AI uses in a day.
- Behaviour when offline or when the backend is asleep.

## Questions for the devs

1. Send the exact prompts behind `analyze` and `revamp`. Does the ICP go in? Does the content type?
2. Which model and provider are behind them, and what does one call cost?
3. What counts against the 10 daily trials?
4. Is Render on a free or a paid plan?
5. Who owns the `ayomiplenty` namespace, the Expo/EAS project and the Google Cloud/Firebase project?

Back to [[03-Areas/scripnals/scripnals|Scripnals]] · See also [[03-Areas/scripnals/technical-architecture|Technical architecture]]
