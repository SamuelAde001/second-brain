---
type: knowledge
area: scripnals
status: needs-input
updated: 2026-09-22
source: claude-export
tags: [validation, survey]
---

# Validation — user feedback questionnaire

From two chats: `01-Inbox/_imports/processed/shortlist/scripnals/2026-07-22-understanding-scripnals.md` and `.../2026-07-25-scripnals-app-user-feedback-questionnaire.md`.

> **Update 2026-09-22, Samuel:** the survey **was sent** and *"we had loads of responses"*. He will draft them into the Brain. Where this note says there is no evidence the survey went out, that is now superseded. The results themselves aren't in the Brain yet. The discount cap question is still open.

## What Scripnals is — confirmed correction, 2026-07-22

Samuel corrected the record directly:

> "The user doesn't only record a voice note, the user can also write down a draft of his script which then can be refined by AI to working content formats."

So the core loop has **two input paths**, not one: a voice note that gets transcribed into a draft, or a script typed directly — either is then refined by AI into a working content format tailored to that creator's specific audience and content type. This matches, and slightly sharpens, what's already in [[03-Areas/scripnals/scripnals|Scripnals]]'s "core loop" section. Scripnals sits as the daily-execution stage after Academy (skills), Community (habit/accountability) and Mentorship (personalised direction).

## The validation questionnaire — what it was for

A Fillout-platform survey drafted 2026-07-25 to test creator interest, desired features, and usefulness for the app **before** the Scripnals name was revealed to respondents — i.e. a blind concept test, run ahead of any public launch. Purpose stated by Samuel: "get to know what people would like to see in the App, if they are interested, and if it's a useful tool for creators."

**No responses or results exist in these sources.** This chat is entirely about drafting and revising the questionnaire itself — there is no evidence it was ever sent, and no response data anywhere in the source material. Anything below is the *design* of the instrument, not findings from using it.

## Final flow — confirmed by Samuel

He approved the full set of proposed edits ("Yes draft out all the changes you pointed"). The complete 12-screen order, as stated back to him and left unchallenged:

1. **Screener** *(edited)* — broadened from Instagram/TikTok only to also include YouTube Shorts: "do you currently create (or want to create) short-form video content — think TikTok, Reels, or YouTube Shorts?" Four options from "post regularly" to "No, and I don't plan to." Branching logic to skip disqualified respondents out of the rest of the survey was flagged as needing to be checked in Fillout — **not confirmed as configured**.
2. **Persona split** *(new)* — inserted right after the screener: "When someone watches your content, what's the outcome you're actually going for?" — options split roughly into lead-generation/authority vs. audience-growth vs. both vs. still deciding. This maps to a two-persona model (Expert Solopreneur/B2B vs. Content Creator/Audience Builder) referenced as coming from a separate "master doc" that is **not among these sources** — its content is not verified here, only cited secondhand.
3. **Capture habit** *(unchanged)* — how an idea gets captured today (multi-select).
4. **Hardest part of the process** *(unchanged)* — single-choice pain-point question.
5. **Concept intro / usefulness rating** *(unchanged)* — the blind pitch: AI turns spoken/typed thoughts into a polished, audience-tailored script, rated before any brand name is shown.
6. **Feature prioritization** *(edited)* — originally listed Voice Studio, AI Script Formatter, Content Calendar, Content Ideation. Swapped to: **Voice Studio, AI Script Formatter, Content Auditor** (added — described elsewhere as the core differentiator, "getting a score and specific feedback on whether my script will actually land with my audience — before I record it"). Content Calendar was cut entirely as out-of-roadmap scope creep; Content Ideation was left in as Samuel's call rather than removed outright.
7. **Magic wand — open-ended** *(unchanged)*.
8. **Pricing** *(unchanged)* — a single-question willingness-to-pay proxy (Van Westendorp-style) with a free-tier baseline. NGN pricing tiers were referenced as "already set at ₦15,000-25,000" per that same master doc — again cited secondhand, not verified in these sources.
9. **Reveal screen** *(edited)* — the original text ("HighSignals is the first mobile app designed exclusively for short-form content creators") led with HighSignals as the product name. This was flagged as contradicting a standing positioning rule attributed to Samuel elsewhere — HighSignals stays "a quiet layer underneath, never the headline" — which matches the rule already recorded in [[03-Areas/scripnals/scripnals|Scripnals]]. Rewritten to lead with **"Scripnals"** as the product, with HighSignals demoted to an optional small-print trust line ("Built by the team behind the HighSignals creator community").
10. **Waitlist email capture** *(edited)* — the original "Lifetime 50% Discount" for any email address was flagged as an uncapped permanent liability. Two capping options were drafted; **Samuel never picked between them**: (a) 50% off the first 3 months, or (b) lifetime 50% capped to the first 100 members.
11. **Traffic-source question** *(new, optional)* — added at the end to separate warm HighSignals-community respondents from cold traffic, since warm respondents would likely rate usefulness and price higher.
12. **Thank-you screen** *(edited)* — the live placeholder text "Subtitle (optional)" was still showing on the actual screen; replaced with real copy.

## Open items (needs-input)

- Whether the edits above were actually applied in Fillout and the survey sent.
- The screener/skip-logic branch for "No, and I don't plan to" — flagged twice as needing verification in Fillout, never confirmed done.
- Which waitlist-discount cap (3-months vs. first-100-members) was chosen, if either.
- The two-persona model and the ₦15,000-25,000 pricing figure are both cited from a "master doc" not present in the Brain's sources — worth locating and importing if it still exists.
- No response data of any kind — the survey's actual results are not recorded anywhere.


Back to [[03-Areas/scripnals/scripnals|Scripnals]]

---

## From the memory export (2026-09-06)

Added by the main session after the chat-export pass, from the Scripnals project memory. More current than the survey design conversation.

**Where validation actually got to:** a user-validation survey **hosted on Fillout**, with a pitch message distributed **across group chats** (WhatsApp, iMessage) targeting content-creator communities. No response data exists in any source.

**Product scope, stated:**
- **In scope:** Content Auditor.
- **Out of scope:** Content Calendar, Content Ideation.

**The key product insight:** a persona split between creators building **authority / lead generation** and creators building **audience / engagement**. This split "underpins the onboarding fork and the AI personalization logic" — it is a product-architecture decision, not just a marketing segment.

**A firm brand rule, and it is absolute:**
> HighSignals operates as a quiet background layer and **must never surface consumer-facing** — this extends to every touchpoint in the sharing flow: link previews, survey metadata, subdomains. Not just in-app UI.

**The brand leak that proved it matters:** the survey's Open Graph metadata, page title and subdomain were surfacing "HighSignals" instead of Scripnals in link-preview cards. Fix lever: Fillout's custom OG/page-title settings, or a branded redirect slug.

**Survey audit findings, all recorded as problems found:** naming inconsistencies leading with HighSignals · Content Auditor missing from the feature-prioritisation question · an **uncapped "Lifetime 50% Discount" offer carrying monetisation risk** · an unfilled placeholder on the thank-you screen · a screener wrongly excluding YouTube Shorts · a missing persona-segmentation question.

**Survey sequencing principles, learned here:**
1. Pain-point questions come **before** the concept pitch.
2. The persona split belongs immediately **after** the screener.
3. Pricing comes **before** the brand reveal.
4. Feature-prioritisation questions only list in-scope features.

**Pitch copy:** the group-chat message was judged too generic — the concrete differentiator was missing. The differentiator to lead with is **"voice note in → structured script out, fast."**

**Next steps recorded:** distribute the refined pitch, collect responses, possibly add per-group-chat attribution via redirect slugs, then further app development.
