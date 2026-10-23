---
type: project
area: called-to-edit
status: active
updated: 2026-10-22
source: interview
tags: [called-to-edit, community, discord, flutterwave, 60-day-challenge]
---

# Called to Edit Community: launch

Part of [[03-Areas/called-to-edit/called-to-edit|Called to Edit]]. The webinar's upsell: [[04-Projects/called-to-edit-webinar-teachings|teachings]] → 10.2. Decision: [[03-Areas/called-to-edit/called-to-edit-decisions|Called to Edit decisions]], 2026-10-21.

**Deadline:** set up before the webinar, Fri 2026-10-23, 7:00pm WAT. **Challenge starts Sun 2026-11-01.**

## What Samuel has settled (2026-10-21)

- **The upsell:** the Called to Edit Community, not the Academy. NGN 5,000 a month. Open to anyone, not only webinar attendees. The Academy is announced as coming soon.
- **Payment:** Flutterwave (*"since that works"*).
- **The 60-day challenge:** *"60 days challenge is what we are going for."* Starts **2026-11-01**, *"to give people time to pay for the community"*. Everyone posts what they did each day from the workbook; he gives feedback and guides them there, until the 60 days end, *"before we know what next."*
- **Platform: Discord** (*"Discord yes"*, 2026-10-21). His reasons: *"in case someones sub finishes we can kick them out automatically, and I can have an automation there easily."*
- **No waitlist:** *"Pay now or anytime"*. The link goes out at the webinar and stays open.
- **Numbers:** *"If few people pay, we work with the few."*
- **Weekly call:** proposed, 1 hour on Wednesdays for live questions, *"but that may be stressful for me"*. He decides on 2026-10-22 with his creative director.

## Added 2026-10-22

Samuel, word for word: *"immediatly they finish the webinar, I would give them access to the community, as a paid subscription, but on a discount, instead of 5k, they would get 2k for their first month and 5k monthly after, that discount is only those who attended the webinar"*.
- **Webinar attendees:** NGN 2,000 for the first month, then NGN 5,000 a month. Everyone else: NGN 5,000 a month.
- **Discord**, set up in full: channels, lobby, rules, automations, and a payment flow that works with Discord.
- **A new website**, on brand. Only the **/community** page is built now: it is the link people get after the webinar to register. The main page waits, to save this week's tokens.
- Set-up questions put to him 2026-10-22. His answers, close to his words:

| # | Question | Samuel, 2026-10-22 |
|---|---|---|
| 1 | Proving attendance | *"The webinar people would get a secret link I would give them on the call, don't worry about a leak, I am fine with other people getting the discount"* |
| 2 | How long the NGN 2,000 lasts | *"The offer lasts until Monday"* (Mon 2026-10-26) |
| 3 | What NGN 2,000 covers | *"their first 30 days till the subscription expires, so if they pay on the 24th, their next pay would be 24th next month with the 5k"*. Access runs 30 days from the payment, not from 11-01 |
| 4 | Flutterwave fees | *"I absorb it"* |
| 5 | Renewals | *"We would prioritise more on bank cards"* (card charged automatically); people without cards pay one-off and *"renew manually with a reminder for both parties"* (member and Samuel) |
| 6 | When a month runs out | Dropped to a lobby where they *"can't message or see any messages"*, only that the sub expired and the link to resubscribe |
| 7 | Flutterwave account | *"I would try and create a new flutterwave account so we have more better flow"* |
| 8 | Refunds | *"No refunds"* |
| 9 | Linking payment to Discord | Join with Discord after paying; *"most of them don't have discord accounts so they would have to create it"* |
| 10 | Bot | He has a Discord account. *"you would make a bot for me that you use to help me oversee things there, it would be the one running things from there"* |
| 11 | Server name | **Called to Edit** |
| 12 | Channels | Proposed list approved; *"I want to have the welcome page seperate from the lobby so we don't get bugged with welcomes"* |
| 13 | Weekly call | Not decided, *"but that would surely be a possiblity"* |
| 14 | Joining after 11-01 | *"They start their own day 1"* |
| 15 | DMs | *"Yes members can DM each other"* |
| 16 | Rules | Draft approved, plus *"no fights or abuses, not scam, be kind to one another"* |
| 17 | Missed check-ins | *"I want everyone to go at their pace, not to be forced, when they see others putting the work they would want to do so also"*. No penalty, no nudge |
| 18 | Automations | Welcome DM yes · **no** daily workbook task; instead *"a reminder nugget from the teachings every morning"* · streak counter and weekly leaderboard yes · 3-day expiry reminder yes · removal yes · call reminder once a call is set |
| 19 | Team | *"No moderation for now, we would have our bot do the moderation"*. Team members get a free seat, *"like my creative director"* |
| 20 | Domain | None yet; *"I am going to buy one today"* |
| 21 | Hosting | *"A new website as we want to build on our brand, but similar setup as the netlify own"* |
| 22 | Page content | Proposed sections fine; he adds more later |
| 23 | Testimonials | *"Not yet but would be added"* |
| 24 | How-to-join | *"Once they signup, let them know the instructions"* |
| 25 | WhatsApp group | Stays open for questions, *"shut down by this month end"* (2026-10-31) |

## Build plan (Brand manager's design, 2026-10-22; not Samuel's decisions unless quoted above)

- **Site:** a new Netlify site from `C:\Users\repzy\Desktop\called-to-edit-site\`, set up like the webinar page (`site/`, `netlify/functions/`, `deploy.sh`). Pages: `/community` (NGN 5,000), the secret offer link (NGN 2,000 until Mon 2026-10-26 23:59 WAT, taken as the end of Monday), `/community/join` (after paying: how to make a Discord account, then Join with Discord). The server sets the price, never the page.
- **Payment:** Flutterwave hosted checkout, opened by a function, card first. The payment is verified with Flutterwave's API on return; the webhook catches transfer payers who never come back. A card payment keeps Flutterwave's card token, and a scheduled function charges NGN 5,000 on day 30. A failed charge, or a transfer payer, gets reminders on day 27 and day 30: the member by email and Discord DM, Samuel by Discord DM.
- **Join:** Discord login (OAuth). The bot adds them to the server with the **Member** role. No public invite link, so nobody gets in without paying.
- **Expired:** the Member role is swapped for **Expired**, which sees one read-only channel with the resubscribe link.
- **Team:** a **Team** role, free, no expiry.
- **Running it:** no always-on server. Netlify functions (checkout, verify, webhook, Discord login) and scheduled functions (daily: nugget, renewals, expiry, streaks; weekly: leaderboard). Members are stored in Netlify Blobs.
- **Moderation:** Discord's built-in AutoMod (slurs, scam links, spam, mass mentions), logging to a private mod-log channel.
- **Admin from here:** there is no official Discord MCP. A local script, `community_admin.py`, drives the bot (build channels and roles, post, read, give Team seats). The bot token lives only in a secrets file outside the Brain and in Netlify's environment, never in the Brain (AGENTS.md §6).
- **Channels:** welcome (read-only; join messages and the bot's welcomes land here, apart from chat) · rules · announcements · start-here · workbook · introduce-yourself · general (the chat) · daily-check-in (forum, one thread per member, own day count) · wins · portfolio-and-profile · outreach · niche · questions · davinci-help · gear · weekly-call (stage) · call-recordings · off-topic · team only: mod-log, payments-log · Expired only: subscription-expired.

### Built 2026-10-22 (Brand manager)

- **Live:** https://calledtoeditcommunity.netlify.app/community · offer: `/community/webinar` · renew: `/community/renew` · after paying: `/community/join` · account (auto-renew on/off): `/community/account`. Home `/` sends to `/community` until the main site exists.
- **Code:** `C:\Users\repzy\Desktop\called-to-edit-site\` (`site/`, `netlify/functions/`, `netlify/lib/`), published with `sh deploy.sh "what changed"`. Functions: checkout, verify, claim, flw (webhook), discord login and callback, account. Scheduled: streaks 6:00am, nugget 7:00am, renewals 7:05am WAT daily; leaderboard Sundays 6:00pm WAT.
- **Webinar relay:** `calledtoedit.netlify.app/flw` now forwards any `cte-` payment to the community site, so a community payment on the current Flutterwave account never lands in the webinar Sheet (tested 2026-10-22).
- **Texts:** [[04-Projects/called-to-edit-community-discord-texts|Discord texts]] (rules, welcome, start-here, workbook, expired, check-in guide, 64 nuggets in his words).
- **Checked:** pages at 375 px (no sideways scroll; offer price and countdown right), checkout answers without keys, the Blobs store works, the relay routes `cte-`. **Not checked yet:** a real payment, the Discord join, the scheduled jobs (they need the keys and the server).

### Discord set up, 2026-10-22 evening (Brand manager, in Samuel's Chrome)

Samuel: *"I want you to build the discord community for me and set everything up for me on my browser as I am very tired"*, then *"Make sure all channel names have Icons to make them look cooler"*.
- **Server** "Called to Edit" (id 1562930392863080470), made by the Brand manager in his Discord. **Bot app** "Called to Edit" (client id 1562931510364082336): Public Bot off, install link None, redirect `https://calledtoeditcommunity.netlify.app/api/discord/callback`. The Brand manager ticked the Developer Terms box on his ask; Samuel did the "I am human" check, pasted the token and client secret into `community.json` himself (Notepad, via `community_admin.py edit-secrets`) and clicked Authorise in his Discord app.
- **Built by `community_admin.py build` + `post-texts`:** roles Team, Member, Expired; 9 categories, 23 channels, each named icon・name (e.g. 📜・rules); Community mode; AutoMod (Kindness, Scams, Spam, Mention spam → 🛡️・mod-log); server icon and bot avatar = community logo; bot renamed from Discord's default "Editors Bot" to "Called to Edit"; Discord's empty starter channels removed; rules, welcome, start-here, workbook (PDF), expired texts pinned; example check-in pinned in the forum.
- **Website:** Discord keys and server ids on Netlify, redeployed; the Discord login link forwards correctly.
- **Flutterwave key in, 2026-10-22 night** (Samuel pasted it; current account, so the webinar relay forwards community webhooks). Checkout tested: the webinar link opens a real Flutterwave page at NGN 2,000. **Still open:** one real test payment through Join with Discord, the domain, team seats.

### Reworked 2026-10-22 night: a growth community, fewer channels, Editors Bot

After Samuel's correction (decision of the same date in [[03-Areas/called-to-edit/called-to-edit-decisions|Called to Edit decisions]]):
- **Server, 12 member channels** (was 20), each icon・name: START HERE 🧭 start-here (what it is, how to use it, rules; Discord's rules channel) · 📢 announcements · 👋 welcome (join messages + introductions) — COMMUNITY 💬 general (morning nugget) · 🏆 wins (Sunday leaderboard) · ✅ accountability (forum, tags 60-Day Challenge / Weekly goals / Daily log; the challenge is one pinned post with the workbook) · 🤖 ask-editors-bot — GROW 🎞️ feedback (forum, tags incl. Client work) · 📚 resources (forum: tutorials, editing hacks, templates, tools, call replays) · 💼 opportunities · 🆘 help — LIVE 🎙️ weekly-live (stage). Team-only 💳 payments-log, 🛡️ mod-log; Expired-only 🔒 subscription-expired. Removed: rules, workbook, daily-nugget, introduce-yourself, leaderboard, portfolio-and-profile, outreach, niche, davinci-help, gear, call-recordings, off-topic. Streaks now count posts in your own accountability post.
- **Editors Bot** (renamed from "Called to Edit"): slash commands /ask, /review, /niche (AI answering from the webinar teachings: **Gemini since 2026-10-23**, Samuel: *"let's swtich to Gemini and see how it works"*, after the Anthropic Console payment verification kept failing; every answer is public in the channel, with the question quoted above it, Samuel 2026-10-22), /nugget, /streak, /subscription, /call, /help. Served by `netlify/functions/interactions.mjs` (Discord's Interactions Endpoint; no always-on bot). Knowledge = the teachings note minus production notes, rebuilt by `community_admin.py knowledge` on every deploy. Persona in `netlify/lib/brain.mjs`. Models, free tier, tried in order when one is out of quota (429), busy (503) or slow (10 s cap each, 24 s total): `gemini-3.8-flash`, `gemini-3.6-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite` (env `BOT_MODELS`; key `gemini_api_key` → Netlify `GEMINI_API_KEY`). Free-tier prompts may be used by Google to improve its products. Was Haiku 5.5 for a day (2026-10-22), 25 AI questions per member per day. Live-call reminder an hour before (`call-reminder.mjs`, from `community_admin.py call <day> <HH:MM>`). Checked: endpoint accepted by Discord, /help answers in the server. **Not live yet:** /ask, /review, /niche wait for an Anthropic API key; mentions (@Editors Bot) would need an always-on host, so the bot works through slash commands.
- **Website** rewritten around the community: weekly live calls, accountability, feedback, resources and hacks, opportunities, Editors Bot; the 60-Day Challenge as one "running now" section; FAQ on joining any time, live calls and the bot.

- **Hero, 2026-10-22** (Samuel: *"I want the heading to be Called to Edit Community / We help editors build their career and land clients ... just phrase it better but let it center around what Called to edit is about"*): heading **Called to Edit Community**, line under it **We help video editors build a real career and land clients, together.**

### Needs Samuel
- **Weekly live call set 2026-10-23:** Wednesdays, 8:00pm WAT (Samuel: *"Weekly live calls would be 8pm Wednesdays, may change later"*). /call shows it; the bot posts a reminder an hour before. Change with `community_admin.py call <day> <HH:MM>`, then push-env and deploy.
- **Editors Bot tested 2026-10-23 off Discord** (the site's own brain code, key from the secrets file): /ask, /niche and a cracked-software question all answered well from the teachings, in 17-18 s, refusing the cracked software. gemini-3.8-flash and 3.1-flash-lite were returning 503 (high demand) at the time; 3.6-flash and 3.5-flash-lite answered. **Live check passed 2026-10-23:** Samuel ran /ask in #ask-editors-bot and Editors Bot answered.
1. Discord: create the server "Called to Edit" (bots can't create servers), then the bot application in Discord's developer portal, with the Brand manager in Chrome. He pastes the token into the secrets file himself.
2. Flutterwave: a new account goes through KYC review, which can take days. Launch on the current account and switch later, unless the new one is approved in time.
3. Buy the domain; it gets connected to the new Netlify site.
4. Times for the morning nugget (proposed 7:00am WAT) and the leaderboard (proposed Sunday 6:00pm WAT).
5. Discord usernames of the team members who get a free seat.

## Research (2026-10-21, on his ask)

**Platforms**
| Option | Fits Nigerians paying in naira? | Auto-remove when the month runs out? | Notes |
|---|---|---|---|
| **Discord + Flutterwave + our own automation** | yes: Flutterwave link in NGN, bank transfer or card | yes, with a bot (below) | channels per day or topic, threads for feedback, voice and stage calls. Discord's own Server Subscriptions aren't confirmed for Nigeria (no official list found), so payment can't go through Discord itself |
| **Whop** (popular for paid Discords) | weak: checkout in USD; many Nigerian naira cards fail or are capped abroad | yes, built in | Nigeria isn't on Whop's sanctioned list; payout options vary by country ([Whop](https://docs.whop.com/manage-your-business/manage-payouts/payout-methods)) |
| **Telegram + a bot (e.g. Subbflow)** | yes: Paystack, built for Nigerian creators | yes, built in | Paystack, not Flutterwave; Telegram is less suited to daily posts with feedback threads ([Subbflow](https://hunted.space/product/subbflow)) |
| **WhatsApp Community** | yes | no: removal by hand | where his audience already is: WhatsApp is used by over 95% of Nigerian internet users ([Statista](https://www.statista.com/statistics/1176101/leading-social-media-platforms-nigeria/)). A daily-post challenge for many people gets lost in one chat |
| **Skool, Circle** | weak: USD, Stripe | yes | priced in USD for him too |

**The one risk with Discord:** no Nigerian Discord user figure was found, and his audience lives on WhatsApp. Many beginners, phone editors especially, won't have used Discord. It needs a short "how to join and post" video and a pinned guide on day one.

**How the automation can work** (a sketch, not built):
1. **A free lobby.** Anyone can join the server and sees only *welcome* and *how to pay*.
2. **They pay on the Flutterwave link** (NGN 5,000), which asks for their **Discord username**.
3. **Flutterwave's webhook** reaches the Apps Script behind the webinar Sheet. It has been live through a relay since 2026-10-06 ([[04-Projects/called-to-edit-landing-page-build|build note]]). The webhook is one URL for the whole account, so the script must tell a community payment from a webinar seat (both are NGN 5,000) by the payment link. The script then gives that member the **Member** role through Discord's API (a bot with Manage Roles) and logs the expiry date.
4. **A daily trigger** reminds members 3 days before expiry with the renewal link, and **removes the Member role** when it lapses. That drops them back to the lobby, which is softer than a kick. A kick is also possible.
5. **Renewal by one-off payment**, not card auto-debit. Flutterwave payment plans charge the card again each month ([Flutterwave](https://developer.flutterwave.com/docs/recurring-payments/payment-plans)), but no source confirmed they work with bank transfer, and his webinar payers mostly paid by bank transfer.
6. **Anyone who pays before 2026-11-01 gets access counted from 11-01**, so the first month covers Nov 1–30 and the 60 days need two payments (November, December).

Discord's add-role and remove-role calls need a bot token in a script property, never in the Brain (AGENTS.md §6). Make and Activepieces also have ready "add / remove guild member role" actions if code isn't wanted.

## Waitlist or pay now

**Settled 2026-10-21: pay now or anytime, no waitlist** (his words above). The reasoning given before he chose, kept for the record:
- The end of the webinar is when they want it most. A free waitlist is a second ask later, and people drop off between "interested" and paying.
- The 11-01 start is already a deadline: *"doors close 31 Oct, challenge starts 1 Nov."* By 10-31 he knows the real number, which is what a waitlist would tell him.
- He already has a working Flutterwave setup.
- For people who can't pay yet: a free "tell me when" list for a later intake, so nobody who's interested is lost.
- What a waitlist would buy: time to finish setting up. But he wants the community ready before the webinar anyway.

## Open

- Bot and server set-up (Discord settled).
- The weekly Wednesday call: yes or no, decided 2026-10-22 with his creative director.
- Someone who joins after 11-01 (*"anytime"*): do they start the challenge at day 1 on their own, or join the group at its current day?
- The 60-day plan and workbook (10.1): to be built by the Brand manager from the teachings.
  - **Built 2026-10-21, draft for Samuel's review:** `_attachments/called-to-edit-workbook/Called-to-Edit-Workbook-Your-First-60-Days.pdf`. 60 days in four phases (direction, learn on real videos, real people's work, first client), a check-in every 7 days. The day-by-day order is the Brand manager's proposal from the book, not yet confirmed by Samuel. **Confirmed 2026-10-21** after the cut-down to 73 pages (Samuel: *"Yes, the workbook is good."*).
- Who on the team moderates.

Samuel will give the build instructions in a new session (2026-10-21).

Back to [[03-Areas/called-to-edit/called-to-edit|Called to Edit]]
