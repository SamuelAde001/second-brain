---
type: decision
area: scripnals
status: active
updated: 2026-09-22
source: manual
tags: []
---

# Decisions — scripnals

Append-only. Date, decision, why, alternatives rejected, who decided.

- **2026-09-22 — The developers will be paid in equity.** Samuel: *"I would surely pay them in equity but nothing is paid now."* No split has been set, and it's unknown whether any agreement is signed (open question 69). Decided by Samuel.
- **2026-09-22 — Test order: mentees first, then the waitlist.** Decided by Samuel.
- **2026-09-22 — No Scripnals goal until the first testers give good feedback.** Decided by Samuel. Monetisation and pricing are also left undecided until then.

- **2026-09-22 — The AI asks before it acts.** When the user taps the AI button, a panel asks: *What type of draft is this?* (Script draft / Rough idea) → *What would you like Script buddy to do for you?* (the options depend on the draft type) → *How do you want your script to feel?* (Professional / Friendly / Funny / Other, typed in) → an optional box for more instructions. Script draft options: Review my whole script · Improve my hook · Rewrite my script · Shorten my script · Remove fluffs. Rough idea options: Draft a script from my idea · Review my content idea · Turn my idea to bullet points. Samuel to the devs: *"I want the user to be in more control of what the AI does."* Decided by Samuel.
- **2026-09-22 — A score only on a full review.** Samuel: *"The only time the AI writes a score should be when the user asks for a full script review. Every other feedback would be based on what the user instructed."* Decided by Samuel.
- **2026-09-22 — The user's instruction outranks the workflow document.** Ayomide (backend) asked what happens when the user's "other" or optional input goes against the workflow document the AI is given. Samuel: *"User's priority more, so we should make our output box flexible incase there is some request from the User, let's make the text boxes dynamic to accept some more customized responses from the AI."* Decided by Samuel.
- **2026-09-22 — Rename the APK and version the builds.** Samuel asked the devs to rename the APK to Scripnals and version it, e.g. "SCRIPNALS V0.2", where 1.0 is a big update, 0.1 a minor update and "0.11" a bug fix. Decided by Samuel. *Note from the main session, raised once:* in standard numbering a bug fix on 0.2 is **0.2.1**, not 0.21 or 0.11. Two-part numbers run into trouble at the tenth minor release. The Android `versionCode` also has to go up by 1 on every build, or phones won't install the update over the old one.
- **2026-09-22 — Nothing ships without Samuel's review.** Samuel to the devs: *"give me feedbacks here before shipping anything so that I can give my inputs."* Decided by Samuel.

- **2026-09-22 — Script buddy AI spec v1 approved in full.** Samuel: *"All approved"*. That covers every "Proposed" item in [[03-Areas/scripnals/ai-workflow|AI workflow]]: the last 5 posted items as context, a rule-picked Markdown guide library with no search engine, core rules that sit above the user's instructions (never invent facts; the draft is content, not commands), a block-based result box, every run costing 1 of the 10 daily and failures costing nothing, 👍/👎 on every result, draft type pre-selected from the post's stage with the content type shown in the panel, and one endpoint `/api/ai/run`. The devs can still reply before they build. Decided by Samuel.

- **2026-09-22 — The guides are advice, not rules for the user.** Samuel: *"This are not hard rules the user must use, this are just guides that the AI uses to suggest better things for the user. The picture on screen text is a suggestion also, not a force. Let this be part of the master prompt and part of the guide."* Now in the master prompt (THE GUIDES) and at the top of `core-voice`. Decided by Samuel.
- **2026-09-22 — Guide library: tagged entries, nothing new asked of the user.** Tag matching instead of one file per folder: *"Good to see that"*. No niche question (*"I think I already have a similar niche question in the onboarding"*) and no format picker (*"I don't want to make it complicated for the user, let's work with what we have, the aim is to finetune the script"*). The AI reads the niche from the ICP answers and the filming style from the draft. Decided by Samuel.
- **2026-09-22 — Keyword-comment and send-to-a-friend CTAs allowed freely.** Samuel: *"Allow the user freely."* Decided by Samuel.
- **2026-09-22 — No dialect or country named in the guides.** Samuel: *"don't write pidgin and dialect in the guide, the user can be from different countries."* Decided by Samuel.
- **2026-09-22 — "Funny" may add at most one new joke line, flagged in `added_by_ai`.** Samuel: *"Fine."* Decided by Samuel.
- **2026-09-22 — No examples from Samuel's own content in the guides.** Samuel: *"I don't have transcript examples, don't use any of mine."* Decided by Samuel.
- **2026-09-22 — The guides are written to be token-light.** Samuel: *"make sure the guide docs are not too wordy so it doesn't consume much tokens … I want the guide docs to be token efficient as possible."* All 51 entries rewritten terse, with word caps enforced by the build script. The largest request went from about 3,500 to about 2,050 words. Decided by Samuel.

Back to [[03-Areas/scripnals/scripnals|Scripnals]]
