---
type: project
area: personal-brand
status: active
updated: 2026-10-06
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
- **Page:** hero (his blazer photo on the marble, three planes) → "where you're stuck" (pinned, three lines) → for you if → **the roadmap** (peak: a gold line draws through 7 stops as you scroll) → host + real counts → what you get + price + countdown to 7:00pm WAT 2026-10-23 → FAQ → form. Phone price dock with the button between the hero and the form. No video; first phone screen about 70 KB of images.
- **Flow:** form → row in the Sheet (Registrations, with utm tags) → Flutterwave link → `welcome.html?status=successful` shows the WhatsApp button and a calendar link, and logs a Payments row; cancelled shows a retry. Every "Get my seat" tap logs to Taps.
- **Verified** in the in-app browser at 375×812 and 1440×900: hero fits above the fold, pinned act holds, route lights stop by stop, form validation, both welcome states, no console errors. **Not verified:** a real phone, a real Flutterwave payment, the Sheet endpoint (needs his deploy).
- **Live 2026-10-04 at https://calledtoedit.netlify.app**, with all three links in (Flutterwave `calledtoeditwebinar`, the WhatsApp invite, the Sheet). The Sheet is "Called to Edit · Registrations" in Samuel's Drive. Its script project is "Called to Edit sheet endpoint", deployed as a web app (run as Samuel, access Anyone), and he authorized it himself. A test row from the live page landed (Registrations and Taps tabs created). **Not yet done:** his own test payment on his phone.
- **Fixes 2026-10-04 after Samuel's phone test** (*"The "Get my seat" button is not working on my phone"*, *"The Sheet looks all scattered and not organised"*):
  - Removed the hidden anti-spam field (`name="company"`): phone autofill can fill it, and the form then quietly stopped. A phone-size test on the live site went form → Sheet → Flutterwave checkout.
  - Sheet rebuilt (script version 4): **Overview** (signed up, paid, not paid yet, money in NGN, seats left, sources, buttons) + **Sign-ups** (navy and gold header, readable dates, a Paid tick box that turns the row green, Flutterwave ref). Taps sit in a hidden tab; the old Registrations/Payments/Sheet1 tabs are gone. Numbers are stored as text, so phone numbers keep their leading 0 (his own first row lost it before the fix). A test "paid" return ticked the row and the Overview counted NGN 5,000; test rows then removed.
- **Publishing changes:** the Netlify CLI is logged in on the PC (Samuel authorized 2026-10-04, *"I need it to auto update on netlify in case we have a change"*). `sh deploy.sh "what changed"` in the build folder publishes `site/` only. No Git repo; the folder is the source.
- *(Superseded 2026-10-04, kept for history)* **Waiting on Samuel** (`SETUP.md`): Netlify account and drag-drop (site name `calledtoedit`), the Apps Script web-app URL, the Flutterwave payment link (redirect to `/welcome.html`), the WhatsApp group invite link, and his brand colours if he wants them changed. Each goes into `site\config.js`.
- **Risk he should know:** the WhatsApp link shows to anyone who opens `welcome.html?status=successful`. Match group members against Flutterwave's transaction list.
- Not used: the `doctor` playwright step (verification ran in the in-app browser instead, no install), kie.ai (no generation).

## Revision 2026-10-04 (Samuel's review)

Samuel, on the first build: *"Because I told you prioritize mobile doesn't mean that desktop like mine should look bad"* · the stuck part had *"too much space ... more straight to the point, not too much animations"* · roadmap *"looks medicre and generic ... make them love to read it with visuals icons"* · remove "Not for you if" and the three steps beside the form · *"they must pay first before they join the whatsapp actually"*.

- **Desktop hero:** now a composed spread inside the page width: copy left, framed portrait right (gold offset frame, name tag overlapping it, three parallax planes). Phone hero unchanged.
- **Stuck:** no longer pinned. One screen: headline, three questions as icon cards, the "business side" line.
- **Roadmap:** three phases (Get started 1–3, Get clients 4–5, Get paid and grow 6–7; the grouping is the Brand manager's, the content is his outline), each stop a card with an icon, the stop name and bullets taken from his outline. Desktop: a central road with cards alternating sides. Phone: road on the left. The road still fills and stops light up as you scroll. Finish card with the button.
- **Payment first, then WhatsApp:** form → Flutterwave → `welcome.html` logs the payment and **opens the WhatsApp group automatically** after about 2 seconds (button kept as a fallback). Nobody gets the group link without Flutterwave sending them back as paid.
- Verified in the in-app browser at 1920×960 and 375×812.

## Funnel fix 2026-10-06 (Brand manager)

Samuel, 2026-10-06: *"someone paid but his name didn't show up"* · paid people *"not being added to the google calendar guest automatically"* · *"I am getting registrations, but not much payment"* · *"I need a way to follow up people that have shown interest but haven't paid"* · *"Nigerians love transfers a lot ... I really don't want to loose people"* · *"Look at everything in this funnel to make it as easy as possible and less friction"*.

**What was wrong (checked against the Sheet, his Gmail and his Calendar, 2026-10-06 ~11:30 WAT):**
- 18 sign-ups, 3 paid (Flutterwave's emails confirm all 3; 2 of the 3 by bank transfer). The Sheet only heard about a payment when the buyer's browser came back to `welcome.html`. One transfer payer never came back, so the Sheet missed him and Samuel added him by hand. Transfer payers leave for their bank app and often don't return.
- The calendar event "Called to Edit Live Webinar" (Fri 23 Oct, 7pm) had **0 guests**. The guest code added on 2026-10-05 sat behind that same browser return and swallowed its own errors, and a payer on 2026-10-06 still wasn't added, so the deployed web app wasn't running it, or it failed silently.
- Checkout friction: after our form, Flutterwave's page asked for name and email again, under the business name **contentinfluence**, with no mention of Called to Edit until "Details".
- Overview: wrong date ("Sun 25 Oct"), paid count only from ticks, sources almost all "direct" because links were pasted without tags, test taps from the build still counted.
- Not known yet: card failures or abandoned checkouts. They live in Flutterwave's dashboard (Chrome wasn't connected, so not read).

**Live on the page (published 2026-10-06 with `deploy.sh`, tested locally at 375 and 1440 px, then checked live):**
- Flutterwave opens with **email, first and last name filled in** (`?email=&firstname=&lastname=` works on payment links; checked).
- Form is name, email, **one WhatsApp number** (phone + checkbox removed). Email typo fix (gmial.com → gmail.com). Details refill after a failed payment.
- Copy says **bank transfer, card or USSD** and names contentinfluence, so nobody is spooked.
- `welcome.html`: cancelled, failed and pending each get their own message, a Bank Transfer tip, a retry with details filled in; no more "no money was taken" claim. It tells the Sheet when someone left the payment.
- `pay.html` (`/pay?e=&n=`): the follow-up link, straight into a prefilled checkout.
- `funnel.js`: source from the short-link tag, else the in-app browser (Instagram, TikTok, Facebook), else the referring site; kept 14 days. One view per visit. `?test=1` marks a tester's phone.
- `site/_redirects`: short links `/ig /story /dm /tt /wa /status /group /x /fb /yt /li /tg /email /p/<name>` (full table in `SETUP-sheet-v5.md`).

**Written, not live until Samuel does `SETUP-sheet-v5.md` (Sheet script version 5, `apps-script.gs`, 30+ checks passed in a Node mock):**
- **Flutterwave webhook** → the Sheet: every payment, paid or failed, even when the buyer never returns. Amount must be NGN 5,000+. Duplicates ignored. Key in the URL (Apps Script can't read Flutterwave's header).
- **Sign-ups**, one row per email: Status (Paid / Not paid yet / Left the payment page / Payment failed: reason), Paid, Paid at, Paid by (Bank transfer, Card, USSD, Returned from Flutterwave, Ticked by hand), On calendar, **Follow up** (a WhatsApp link with the message for their status), Followed up tick, Notes, Source, ref, Emails sent. **Payments** tab: every event with Flutterwave's failure reason.
- **Calendar:** payers added quietly with CalendarApp every 10 minutes and on each payment. Not the Calendar API with notifications, which can email every guest each time one is added. Guests can't see each other.
- **Overview:** paid, money in, after fees (NGN 4,892.50 each, from Flutterwave's emails), seats left, unpaid with failed/left/followed-up, the funnel (opened → tapped → form → paid), sources with paid %, how people paid, payment problems by reason.
- **Two email switches, off:** a confirmation to each payer (Meet link + WhatsApp group) and one reminder to unpaid sign-ups after 3 hours. Waiting on Samuel's yes.
- Old v4 copies: `Desktop\landing-page\old\`.
- **Deployed 2026-10-06 ~12:15 WAT** (Brand manager in Chrome, Samuel clicked Allow): code pasted, `setup` run, the deployment the page uses (`AKfycbyOSsZ0…`) moved from Version 4 (4 Oct) to the new version; endpoint answers "version 5". **Why the calendar never worked:** the 5 Oct calendar code went out as a *second* deployment with a different URL that nothing calls; the page's URL stayed on Version 4. That second deployment (Version 5 of 5 Oct, `AKfycbzyLvT4…`) is still active and unused. Archive it when convenient.
- After `setup`: 19 people migrated, 3 payers on the calendar event (no email sent), event set so guests can't see each other or invite others, WhatsApp group added to its description. Samuel 2026-10-06: *"yes to both emails"*: both switches ticked. Sales page: the "contentinfluence / No refunds" line removed on his word (*"it doesn't show on the flutterwave Dashboard"*); No refunds stays in the FAQ.
- **Webhook saved 2026-10-06** by Samuel (Settings → Webhooks, V3 live): URL checked exact, all preferences on. Not yet proven end to end: no payment since. Test = **Resend webhook** on a paid transaction (Samuel's click), or the next real payment; the Overview line then reads Connected.
- **Emails sent 12:20 WAT:** 3 confirmations, 12 reminders. The 5 newest sign-ups get theirs when they pass 3 hours.
- **Flutterwave transactions, 1 Aug–6 Oct (read 2026-10-06):** 3 successful, all **bank transfer**; 1 cancelled card attempt, Samuel's own test. No failed, pending or abandoned payments. So unpaid sign-ups never started a payment: the leak is between the form and the checkout, not card failures. Follow-up is the lever.
- Samuel clicked Resend webhook on Paul Akoji's payment: *"no hook data found"*. Expected: that payment (09:02) came before any webhook URL existed, so Flutterwave never made a hook for it. No faked test sent: it would mark the webhook Connected without Flutterwave having reached the Sheet. Proof waits for the next real payment.
- **Emails rewritten 2026-10-06, live 15:22 WAT (deployment version 7, same URL).** Samuel: *"I need it to feel more personalised and kind"*, then *"I love them"*, with subjects carrying *"Video editing Webinar"* so people remember what it is. Sender now "Samuel Adebayo", signed "Samuel"; first name fixed (DAVID → David). Reminder subject "<First>, your seat for the Video editing Webinar is still waiting", middle line changes for card failed / left the payment page / not started, offers a reply. Confirmation subject "<First>, you're in! Video editing Webinar, 23 October", asks them to bring or reply with their one question. Both invite replies: Samuel answers them in Gmail. All 19 current people had already got the old wording (once each); the new one applies from the next sign-up or payment.
- **First payment through the webhook, 2026-10-06 15:27 WAT** (4th payer). Three card tries failed (Incorrect PIN ×2, PIN Tries Exceeded), then a bank transfer went through. The webhook landed all four events: row marked Paid (Bank transfer), on the calendar 15:27, confirmation email with the WhatsApp group link sent 15:27. Proven end to end; the Overview reads Connected.
- **Samuel, 2026-10-06:** *"I got an email of an unsuccesful webhook, and also ... the person wasn't automatically added to the whatsapp group chat like the rest"*. Nobody is ever added: `welcome.html` opens the group link when the payer comes back to it. The earlier payers came back; this one paid in the bank app and never did, so the confirmation email was the only route in. For a payer who hasn't joined: the row's Follow up WhatsApp link.
- **"Unsuccessful Webhook Delivery" emails (15:35, 15:53, 15:55 WAT) were false.** Apps Script answers every POST with a 302; Flutterwave counts anything but 200 as failed and retries (the Sheet drops the duplicates). **Fix live 2026-10-06** (Samuel: *"Go ahead with the updates"*): Netlify Function relay `netlify/functions/flw.mjs` at `https://calledtoedit.netlify.app/flw` passes the hook and its `?key=` on unchanged and answers 200 (502 if the Sheet didn't take it, so Flutterwave retries). `deploy.sh` now uploads `--functions netlify/functions` too. Live test: wrong key → 200 (the Sheet writes nothing on a wrong key), GET → 405, page 200. **Waiting on Samuel:** in Flutterwave Settings → Webhooks, replace the `https://script.google.com/macros/s/AKfycbyOSsZ0…/exec` part of the URL with `https://calledtoedit.netlify.app/flw`, keeping `?key=…` as it is.
- **Flutterwave webhook URL switched to the relay, 2026-10-06 ~16:00 WAT** by the Brand manager in Samuel's Chrome on his go (*"please do it yourself, I give you the permission"*): only the part before `?key=` replaced (key never read out), saved ("Setting updated successfully"), still there after reload; all six preferences on. Proof: the next real payment shows on the Payments tab and no "Unsuccessful Webhook Delivery" email follows.

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

## 2026-10-07 — Sign-ups silently lost since the 6 Oct page update

Samuel, 2026-10-07: *"I am getting people responiding to the last video I posted, but most of them are not signing up or converting into payments"*.

- **Sheet at 14:00 WAT:** 21 people, 5 paid (NGN 25,000 in, NGN 24,463 after fees), 95 seats left, 16 not paid (3 followed up). The last form sign-up was **Tue 6 Oct 11:42**. Since then: no form rows, no views (Views tab empty), only two people who reached Flutterwave without a form row (one paid by transfer, one card failure), caught by the webhook.
- **Cause, proven:** the 6 Oct `funnel.js` sends a field named `sid` with every event. Google's Apps Script front end answers any POST carrying `sid` with **400** and never runs the script (curl: with `sid` → 400, nothing written; same body with `visit` or nothing → 302, row written). So every view, tap, form sign-up and page-reported payment since ~11:41 on 6 Oct was dropped. Those people got no reminder email and have no Follow up link. Anyone who filled the form but never opened checkout is unrecoverable. Webhook payments were unaffected (server to server, no `sid`).
- **Fix, local, not yet published:** `funnel.js` sends `visit` instead of `sid`; the three pages load `funnel.js?v=2`. Tested from a local copy with `?test=1`: view and tap landed in the Tests tab. The Session column stays blank until the Sheet script reads `p.visit` (needs a new deployment version; optional). Publishing waits on Samuel's yes.
- **2026-10-07, after Samuel's *"fix the everything pleease"*:** `funnel.js` also re-sends a visitor's saved sign-up once (`recovered=1`) when they come back, so people lost 6–7 Oct who return on the same phone land in the Sheet. Publishing with `deploy.sh` was blocked by Claude Code's auto-mode safety check, so it is **not live**: Samuel runs `deploy.sh` himself or approves it. Still to do after that: the Sheet script reads `visit` (otherwise "Tapped Get my seat" reads 0), and a post-publish check that a `?test=1` view lands.
- **Where lost sign-ups can still be found:** Flutterwave pending or abandoned transactions since 6 Oct 11:41 (name and email, prefilled from the form; the webhook only reports paid and failed charges, both already in the Sheet); the visitor's own phone (the re-send above); his Instagram comments and DMs on the video. Not recoverable: Google refused the requests before the script ran, so there are no logs, and Netlify never saw form data.
- **Fix live 2026-10-07 ~14:26 WAT** on Samuel's *"Deploy the fix"*: `funnel.js?v=2` sends `visit`, plus the one-time re-send. Checked on the live site with `?test=1`: view and registration landed in Tests; a real visitor's view landed in Views straight after.
- **Guard:** `deploy.sh` now runs `check-sheet.js` first. It loads `site/funnel.js` in a fake browser, posts exactly what the page would send (as a test) and stops the publish unless the Sheet answers 302. Checked: the fixed page passes; the old `sid` version fails with 400.
- **Not done (Claude Code's auto-mode check blocked the live script edit):** the Sheet script reading `visit` (`apps-script.gs` lines 68–69 already changed locally). Until it's in a new deployment version, the Session column is blank and "Tapped Get my seat" on the Overview reads 0. Flutterwave was logged out in Chrome, so pending/abandoned transactions since 6 Oct are unread.
