---
type: project
area: personal-brand
status: active
updated: 2026-10-04
source: manual
tags: [called-to-edit, landing-page, scroll-craft, build, handoff]
---

# Called to Edit landing page: build handoff

Build state for the page whose copy is in [[04-Projects/called-to-edit-landing-page-copy|landing page copy]]. Look and voice: [[03-Areas/personal-brand/brand-guide|Brand guide]]. Area: [[03-Areas/personal-brand/personal-brand|Personal brand]]. Parent: [[04-Projects/called-to-edit-webinar-and-academy|Called to Edit webinar → Academy]].

## Decision (Samuel, 2026-10-04)

Use the **scroll-craft** skill (github.com/nateherkai/scroll-craft, MIT) to build the page, in a **new Opus session**, so the build is handled better and faster. Build session to be started by Samuel.

## State at handoff

- The Claude plugin install failed on Windows (marketplace cache `EPERM` rename error). Samuel downloaded the repo instead. **Not installed as a plugin; used by reading the skill directly.**
- Skill location: `C:\Users\repzy\Downloads\scroll-craft-main\scroll-craft-main\plugins\nateherk-design\skills\scroll-craft\` (note the nested folder). Entry point: `SKILL.md`. Read it, then its `references/`.
- Build folder (empty, made 2026-10-04): `C:\Users\repzy\Desktop\landing-page\`. Outside the Brain on purpose. Needs a directory grant in the session before writing there.
- `doctor.mjs` run from the build folder: Node v24.12.0 ok, ffmpeg full build ok (WinGet Gyan, 588 filters, libwebp present), Chrome ok. **Missing:** `playwright-core` (run `npm i playwright-core` in the build folder before the verify step) and `KIE_AI_API_KEY` (optional, only for generated imagery; none set, so no generation without Samuel's say-so).
- Doctor script was read in full before running: no network calls, no writes.

## Built 2026-10-04 (Brand manager, this session)

- **Folder:** `C:\Users\repzy\Desktop\landing-page\`. Upload only `site\` (468 KB: `index.html`, `welcome.html`, `config.js`, the scroll-craft engine copy, 5 images). Also there: `BRIEF.md` (scroll-craft brief, self-authored under his "use your judgment"), `SETUP.md` (his go-live steps), `apps-script.gs` (Google Sheet endpoint), `FINGERPRINTS.md`.
- **Page:** hero (his blazer photo on the marble, three planes) → "where you're stuck" (pinned, three lines) → for you if → **the roadmap** (peak: a gold line draws through 7 stops as you scroll) → host + real counts → what you get + price + countdown to 7:00pm WAT 2026-10-25 → FAQ → form. Phone price dock with the button between the hero and the form. No video; first phone screen about 70 KB of images.
- **Flow:** form → row in the Sheet (Registrations, with utm tags) → Flutterwave link → `welcome.html?status=successful` shows the WhatsApp button and a calendar link, and logs a Payments row; cancelled shows a retry. Every "Get my seat" tap logs to Taps.
- **Verified** in the in-app browser at 375×812 and 1440×900: hero fits above the fold, pinned act holds, route lights stop by stop, form validation, both welcome states, no console errors. **Not verified:** a real phone, a real Flutterwave payment, the Sheet endpoint (needs his deploy).
- **Waiting on Samuel** (`SETUP.md`): Netlify account and drag-drop (site name `calledtoedit`), the Apps Script web-app URL, the Flutterwave payment link (redirect to `/welcome.html`), the WhatsApp group invite link, and his brand colours if he wants them changed. Each goes into `site\config.js`.
- **Risk he should know:** the WhatsApp link shows to anyone who opens `welcome.html?status=successful`. Match group members against Flutterwave's transaction list.
- Not used: the `doctor` playwright step (verification ran in the in-app browser instead, no install), kie.ai (no generation).

## Next step: Step 0, the brief (done 2026-10-04, see above)

The skill needs a brief before building. Pre-filled from the Brain: audience, journey, one CTA (**Get my seat**), look (navy marble, gold serif, cream), mobile first. **Four questions still open for Samuel** (or he may say "use your judgment", which the skill treats as creative delegation: author the brief, flag assumptions, build):

1. Footage he already has: hero photo or video of himself, the marble room, Resolve screen recordings. With none, the page is type and motion only.
2. How far from premium-minimal: editorial, cinematic (like Life of a Video Editor), or bold.
3. The one moment a visitor should remember after scrolling.
4. Weight: many visitors are on mobile data, so light and fast, or heavy video is acceptable.

## Rules for the build

- Copy items marked `[confirm]` stay flagged. No invented proof, counts or testimonials. No income promises (*plan*, *skill*, *clients*; never *guaranteed*).
- The button goes to the Paystack payment page; needs the fields from task A3 in [[04-Projects/called-to-edit-prep-tasks|Prep tasks]]. Add a simple count of button taps.
- Brand colours and fonts are *approximate* until Samuel confirms them against his Resolve project ([[03-Areas/personal-brand/brand-guide|Brand guide]], Open).
- Never edit the skill's engine per project. Never put third-party code inside the Brain.
