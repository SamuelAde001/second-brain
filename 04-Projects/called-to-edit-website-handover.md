---
type: project
area: called-to-edit
status: active
updated: 2026-10-26
source: project-handover
tags: [website, calledtoedit, handover, gemini]
---

# calledtoedit.com: handover to Gemini

Samuel, 2026-10-26: *"Handover everything concerning the website brand building to Gemini, I would continue from there … all adjustments would be made there"*. Written by Claude Code (Brand manager) at the moment the redesign went live. The project's history, brief and decisions: [[04-Projects/called-to-edit-website|calledtoedit.com project]]. Area: [[03-Areas/called-to-edit/called-to-edit|Called to Edit]].

## Where it stands

- **Live:** https://calledtoedit.com (production deploy 2026-10-26 ~22:20 WAT, site commit d4a2ff2). Preview link for drafts: https://preview--calledtoeditcommunity.netlify.app.
- **Samuel likes the design.** He wants: **copy changes** (he'll list them), **smaller cards**, **fewer unnecessary gaps**. These are the first jobs. He'll send them page by page. Do them, deploy to the preview, screenshot, then go live on his OK.
- He is short on credits. Keep the work small: edit the CSS and copy. Don't rebuild anything.

## The build, exactly

**Code:** `C:\Users\repzy\Desktop\called-to-edit-site\` (a local git repo, no remote). Commit there with `git -c user.name=Samuel -c user.email=repzysam@gmail.com commit`.
- **Astro 7** static site, multi-page. `astro.config`: `build.format: 'file'` (pages build as `webinar.html` and are served at `/webinar` with no redirect hop), `trailingSlash: 'never'`, `publicDir: ./site`, `outDir: ./dist`.
- **Read first:**
  - `docs/DIRECTION.md` is the design build document. Section 0 has Samuel's settled choices; section 5 has the hard rules and greps.
  - `docs/COPY-CHECK.md` lists which facts are allowed in the copy.
  - `docs/COMPONENTS.md` and `docs/components/{chrome,dialog,blocks}.md` cover every component.
- **Design system:** the scroll-craft skill. Its engine is vendored unchanged in `src/vendor/scrollcraft/` and driven by `data-sc-*` attributes (pin, flow, parallax, in, tilt, spotlight; progress in `--sc-p`).
  - Grammar "The edit bay".
  - Signature "the playhead lands": the rail under the header, where a marker flies to the i of the outro logo.
  - Peak "the room opens": the webinar screen grows edge to edge.
  - The skill itself is at `C:\Users\repzy\Downloads\scroll-craft-main\scroll-craft-main\plugins\nateherk-design\skills\scroll-craft\`.
- **Where to change things:**
  - **Prices, offers, dates, contact:** `src/data/site.ts` only. It is the single source.
  - **Form text:** `src/data/forms.ts`.
  - **Page copy:** `src/pages/*.astro`, plus `src/components/{home,community,offers,about,legal}/`.
  - **Spacing and card size:**
    - tokens in `src/styles/system-tokens.css` (`--space-section`, `--space-block`, `--gap`, type sizes `--t-*`);
    - section padding in `src/styles/system.css` (`.section`);
    - cards (bento tiles, price slates, clip cards) in `src/styles/blocks.css`;
    - offer pages in `src/components/offers/offers.css`;
    - the home hero in `src/components/home/ScreeningRoom.astro`.
  - **Header, menu, rail, footer, outro:** `src/styles/chrome.css`.
  - **The pop-up:** a native `<dialog>`, styled in `src/styles/dialog.css`.
  - **Scripts:** `src/scripts/` (`site.ts` boots everything).
- **Images:**
  - `src/assets/` (webinar stills with names blurred, photos, covers) go through `<Picture>`, which builds the srcsets.
  - Videos are in `site/media/`: the home hero loop (muted, no audio track) and the community and academy clips, which have captions.
  - The free guide is at `site/guides/called-to-edit-choose-your-niche.pdf`.
  - The asset scripts and notes are in `scripts/assets/` (see its README).
- **Checks before every deploy:**
  - `npm run build`.
  - `node scripts/budget.mjs` (page-weight budgets; it must say "All pages within budget").
  - The hard-rule greps from DIRECTION section 5: no em or en dashes; no "Call to Edit"; no attendee counts or "booked a seat"; never name Route Rise or USD rates; no invented results or testimonials.
- **Deploy:**
  - Draft: `sh deploy.sh "message"` goes to the stable preview link.
  - Production: `sh deploy.sh --prod "message"`, **only on Samuel's OK**.
  - `deploy.sh` also rebuilds Editors Bot's knowledge from the Brain (`community_admin.py nuggets` and `knowledge`), so run it from a shell where Python and the `netlify` CLI work.
  - Netlify site `calledtoeditcommunity`, id `20664735-e47b-402f-9450-6fab7ce27ebc`. The custom domain and HTTPS are on, and the Netlify badge is off.

## Payments (don't change without a parity test)

- **Provider:** Flutterwave, Samuel's existing account. Checkout shows the name "contentinfluence" until Flutterwave changes it. A support message is drafted in the project note (not sent; his call).
- **Community, NGN 5,000 a month:**
  - `/community` holds the join dialog, which POSTs JSON to `/api/checkout` (`netlify/functions/checkout.mjs`). **The price is decided on the server, never by the page.**
  - Offer price: NGN 2,000 for a first payment through `/community/webinar` until `2026-10-30T23:59 WAT` (mirrored in `site.ts → community`).
  - Flutterwave sends the buyer back to the join page, which calls `verify.mjs`.
  - `flw-webhook.mjs` catches bank-transfer payers. It only counts a payment after checking with Flutterwave's API, and only tx_refs starting `cte-`.
  - `renewals.mjs` runs daily at 7:05am WAT: a reminder 3 days before the end, a saved-card charge on the last day, then Member becomes Expired.
  - `account.mjs` serves the account page (auto-renew on/off).
  - Discord login and role: `discord-login.mjs` and `discord-callback.mjs`.
  - `/community/join` and `/community/account` are the old live pages (kept). `/community/`, `/community/webinar` and `/community/renew` rewrite to `community.html` (see `site/_redirects`).
- **Shared code:** `netlify/lib/lib.mjs`. It holds members in Netlify Blobs, tokens and the Google Sheet sync. **Never edit it casually.**
- **Parity test:** `node scripts/community-parity.mjs`, or add `--new-origin https://preview--calledtoeditcommunity.netlify.app` to test the deployed preview. It compares the new join form's checkout request with the old page's, byte for byte, and never pays. Run it after any change to `/community` or the dialog. It passed 57/57 on 2026-10-26.
- **Secrets:**
  - They live in `%USERPROFILE%\.brain-secrets\community.json`: Flutterwave secret key, Discord bot token and client secret.
  - No agent opens that file. `python 00-System/scripts/community_admin.py push-env` puts them on Netlify as environment variables.
  - Only these names appear in code: `FLW_SECRET_KEY`, `DISCORD_*`, `GEMINI_API_KEY`.
- **Masterclass (the 2026-10-23 webinar recording), NGN 10,000, sold since 2026-10-27:** button opens the `masterclass` dialog (type `buy`) → `netlify/functions/masterclass.mjs` (POST, price set on the server, tx_ref `mc-`) → Flutterwave → `/thanks/masterclass` → `masterclass-verify.mjs` checks the payment and returns the video link from the Netlify env var `MASTERCLASS_URL` (Samuel's Drive link; until set, the page says the link comes by email within 24 hours). Paid records: Blobs store `community`, keys `mc:<tx_ref>`. The Community webhook ignores `mc-`.
- **Not paid online yet:** webinar seats, e-book, Academy, Mentorship.
  - Their buttons open the pop-up and collect a lead (first name and email) into Netlify Blobs store `leads` via `lead.mjs`.
  - Mentorship applications also DM Samuel on Discord.
  - The webinar button says "Tell me the next date" until `webinars.next.paymentUrl` is set in `site.ts`; then it becomes "Book my seat".
  - Read leads with `netlify blobs:list leads --site <id>` and `netlify blobs:get`.

## Email

- Google Workspace (Business Starter): samuel@calledtoedit.com, with aliases hello@ (the site's contact) and dmarc@.
- SPF, DKIM and DMARC are on, in the Netlify DNS zone. First charge 2026-11-09.

## Samuel's settled choices (don't reopen)

- Feel: *"Apple premium clean, with motions added in, and all in my brand but looks good and still easy to load"*.
- Logo: the vertical (stacked) one.
- Home: a main VSL area showing a muted webinar loop with no play button until the real VSL exists.
- Webinar shots show the full screen: faces visible, names blurred.
- Forms: no form on the page. A button opens the pop-up, which asks for first name and email for the guide.
- Never: "78 people booked a seat", Route Rise, or his USD rates.
- About keeps the military story.
- Instagram @samuelsignals01. WhatsApp 08156417120.

## Open, waiting on Samuel

- His copy changes, smaller cards, fewer gaps (first job).
- A test on his own phone, in Chrome and the Instagram in-app browser, as far as the Flutterwave page without paying.
- A seat payment link once a webinar date is set.
- A Fusion screenshot, the DaVinci syllabus, and testimonials (with consent).
- His OK on the new privacy and terms text.

**Phase 2 (later):**
- Paid checkouts for the other offers.
- A Leads Sheet and MailerLite.
- Moving the old landing-page webinar relay (`Desktop\landing-page\netlify\functions\flw.mjs`) and the Discord interactions endpoint onto calledtoedit.com.
- 301 redirects for the old links.
- After shipping, append the fingerprint row to `Desktop\landing-page\FINGERPRINTS.md`.
