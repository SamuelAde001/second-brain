---
type: project
area: scripnals
status: active
updated: 2026-09-22
source: manual
tags: [ai, guide-library, brief, research]
---

# Guide library: brief for the research session

**Read this first in a new chat.** It holds everything needed to research and write the guide library for Script buddy, the Scripnals AI, without re-reading the whole 2026-09-22 session.

## The job

Write the reference files Script buddy uses on every call. **Samuel promised the devs the first set "before this week runs out" → by 2026-09-27** ([[03-Areas/scripnals/scripnals-log|Log]], 2026-09-22).

The spec that the files plug into is [[03-Areas/scripnals/ai-workflow|AI workflow]] (approved 2026-09-22). Read sections 7–9 of it before starting.

## How the files are used (fixed by the approved spec)

- They are plain Markdown files in the backend repo, **each under ~400 words**, because every call includes about 6 of them.
- The server picks **one file per folder** based on the user's choices. There is no search.
- The picked files go into `{{guides}}` in the master prompt, each under its file name.
- The master prompt already sets the rules, the priority order and the JSON reply format. **The guides must not contradict it.** That means:
  - no reply-format instructions
  - no scoring outside `review_full`
  - no Markdown in the output
  - never tell the model to invent facts
- The priority order: the master prompt's rules › the user's notes › the task and tone › **the guides** › the ICP and past posts.

## The files: 21 in total

| Folder | Files | Picked by |
|---|---|---|
| `master-prompt.md` | 1: **already written**, in section 8 of [[03-Areas/scripnals/ai-workflow\|AI workflow]] | always |
| `audience/` | `business.md` · `creator.md` | the ICP path |
| `content-types/` | `storytelling.md` · `listicle.md` · `quick-tip.md` · `contrarian.md` · `before-after.md` · `pov.md` | the content type in the editor |
| `actions/` | `review-full.md` (holds the scoring rubric) · `improve-hook.md` · `rewrite.md` · `shorten.md` · `remove-fluff.md` · `draft-from-idea.md` · `review-idea.md` · `to-bullets.md` | the task |
| `tone/` | `professional.md` · `friendly.md` · `funny.md` | the tone. "Other" uses the user's typed tone, with no file |
| `hooks/` | `hook-library.md` | the tasks `improve_hook`, `rewrite`, `draft_from_idea`, `review_full` |

**Suggested shape for each kind of file.** Suggestions only; Samuel decides.
- **Audience:** what this creator wants from content, what every script must do for that goal, calls to action that fit, what to avoid.
- **Content type:** what it is, when it works, the beats mapped to HOOK / BODY / VISUAL / CTA, a typical length, common mistakes.
- **Action:** what to do, what to check, what not to touch, which reply blocks to use.
- **Tone:** word choice, sentence length, energy, what to avoid.
- **Hook library:** named patterns. The names appear to users in `improve_hook`'s `pattern` field. Each gets a one-line formula and when to use it.

## Fixed inputs already decided

- **The two audience paths**, from the product master doc: *Path A, Expert Solopreneur*: lead generation and authority, with the AI focused on the ICP's pain points. *Path B, Content Creator*: community growth, virality and brand deals, with the AI focused on entertainment, storytelling arcs, emotional resonance and pacing. In the app they're "Business owner/entrepreneur" and "Content creator" ([[03-Areas/scripnals/current-build|Current build]]).
- **The rubric** for `review_full`: 5 × 20 points. Hook · Clarity · Audience fit · Pacing · Call to action (approved 2026-09-22). The guide defines what each score means.
- **The shorten default:** under 60 seconds spoken, about 150 words, unless the user says otherwise (approved).
- **Script sections:** HOOK · BODY · VISUAL · CTA.
- **Core stance**, from the master doc: Scripnals is *"not a done-for-you writer"*. It structures the creator's own thoughts.

## Source material already in the Brain (use this first)

- [[03-Areas/personal-brand/storytelling-structures|Storytelling structures]]: 6 storytelling templates (Hero's Journey, About Me, The Lesson, The Big Goal/Dream, Challenge to Victory, The Breakthrough) and 6 educational ones (Tip/Hack, Myth, Viral Video Reaction, Step-by-Step System, Common Mistake, Authority). These are the likely base for `content-types/`.
- [[03-Areas/personal-brand/script-process|Script process]]: Samuel's raw idea → script method, with an interview, hook development, the full script, a review checklist, and standing rules.
- [[03-Areas/personal-brand/script-review-checklist|Script review checklist]]: the base for `actions/review-full.md`.
- `00-System/skills/yap-session-planner/`: frameworks for unscripted talking points (story, topic, opinion, tutorial, experience). The base for `actions/to-bullets.md`.
- [[03-Areas/scripnals/validation|Validation]]: survey design, the persona split, and the differentiator "voice note in → structured script out, fast".
- The product master doc and PRD, read 2026-09-22, are summarised in [[03-Areas/scripnals/current-build|Current build]] (built vs specced).

## Research to do

- Short-form best practice on hooks, retention, pacing (spoken words per second) and CTAs, for TikTok, Reels and Shorts. Record every source.
- How each of the 6 content types is structured in practice. Map Samuel's 12 templates onto them.
- How to make "Funny" workable without inventing jokes or facts.
- **Samuel's own method outranks outside advice.** Web findings are suggestions until he confirms them (AGENTS.md rule 7).

## Questions for Samuel in that session

1. Which of his 12 templates map to which of the 6 content types?
2. What do the rubric scores mean? For example, what earns a Hook 20/20?
3. Which hook pattern names should users see?
4. Language: plain international English, or Nigerian English and Pidgin when the user writes that way?
5. How far can "Funny" go?
6. Does the 60-second / 150-word shorten default hold?

## Where to write, and what happens after

- **Canonical location:** `03-Areas/scripnals/guides/`, mirroring the repo tree above. `master-prompt.md` is copied from section 8 of [[03-Areas/scripnals/ai-workflow|AI workflow]]. If the prompt changes, change it in the spec first.
- **Suggested test before sending:** run the master prompt plus the guides on 3–4 real drafts in a Claude chat. Check the rules hold: nothing invented, a score only on a full review, the JSON is valid.
- **Send to the devs:** the `guides/` folder, zipped or shared as files. Add a line to [[03-Areas/scripnals/scripnals-log|Log]].
- **If the spec PDF has to change:** edit [[03-Areas/scripnals/ai-workflow|AI workflow]], then run `python 00-System/scripts/build_scripnals_spec.py`. Add `--figures` if the flow chart or screens changed; their sources are `03-Areas/scripnals/assets/script-buddy-flow.html` and `script-buddy-mockups.html`. The output is `03-Areas/scripnals/assets/scripnals-script-buddy-ai-workflow-v1.pdf`.
- **If the bug list changes:** edit [[03-Areas/scripnals/dev-bug-list|Bug list for the devs]].

## Style Samuel asked for in dev documents (2026-09-22)

- Few words, easy words, no worked examples.
- Diagrams: simple, left to right, high contrast. He rejected a dense three-column swimlane.
- Keep mock-ups of screens. He asked for them.

Back to [[03-Areas/scripnals/scripnals|Scripnals]]
