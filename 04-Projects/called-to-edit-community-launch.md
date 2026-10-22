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
- Set-up questions put to him 2026-10-22; his answers go below.

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
