---
type: knowledge
area: scripnals
status: active
updated: 2026-09-22
source: manual
tags: [ai, guide-library, script-buddy, dev-handover]
---

# Script buddy guide library

**v2 · 2026-09-22 · approved by Samuel.** Due to the devs 2026-09-27. **A living library:** it will be improved as better conventions and rules come up (Samuel, 2026-09-22).

The reference text Script buddy reads on every call: how to keep the user's voice, how a short script is built, what each task, content type, tone and audience needs, notes on niches and filming formats, and named hooks and calls to action.

**These are advice for the AI, not rules for the user** (Samuel, 2026-09-22). The AI uses them to suggest better things. Structures, hooks, calls to action, visuals and on-screen text are all suggestions the user can ignore. The master prompt says the same. Spec: [[03-Areas/scripnals/ai-workflow|AI workflow]], section 7. Research and sources: [[03-Areas/scripnals/guide-library-research|Guide library research]].

## What is in it: 51 entries

| Folder | Kind | Entries | Loads when |
|---|---|---|---|
| `core/` | core | 3: keep their voice (opens with "these guides are advice") · scripting standards · what the platforms reward | always (platform rules: not on remove fluffs or bullets) |
| `audience/` | audience | 2: business · creator | the ICP path |
| `niches/` | niche | 1: `niche-notes`, 10 niches in one note. The AI picks the one that fits the ICP answers | create and review tasks |
| `actions/` | action | 8, one per task. `action-review-full` holds the scoring rubric | the task |
| `content-types/` | content-type | 6, each with 4–6 structures built on Samuel's templates | the content type |
| `formats/` | format | 1: `format-notes`, 7 filming styles in one note. The AI reads the style from the draft, else assumes talking to camera | create and review tasks |
| `tones/` | tone | 3. "Other" loads none and uses the typed tone | the tone |
| `hooks/` | hook | 18 named patterns. The title is what users see in `improve_hook` | hook-related tasks + the content type |
| `ctas/` | cta | 9 named calls to action | review, rewrite, draft + the audience |

## How one entry is built

One Markdown file per entry. The file name is the entry's `id`. The top block holds the tags. The body is the text the AI reads: short plain lines, CAPS labels, `-` lists, no bold or headings.

| Field | Meaning |
|---|---|
| `id` · `kind` · `title` · `summary` | Unique name · folder kind · display name · one line on what it is for |
| `actions` · `content_types` · `tones` · `audiences` | The request values it applies to, or `any` |
| `priority` | 1 = always keep · 2 = drop if over budget · 3 = drop first |
| `version` · `status` · `updated` | Only `active` entries load |
| `refs` | Source codes in [[03-Areas/scripnals/guide-library-research\|the research note]] |

`type`, `area`, `source` and `tags` are Brain fields. They are not exported. Guide files carry no backlinks, because their body goes straight into the prompt; this note is their link to the area.

## The matching rule

**An entry loads when every tag field is `any` or contains the request's value.** One rule, no search engine. A value with no entry (tone "Other") simply matches only `any`.

Entries go into `{{guides}}` in this order: core → audience → niche note → action → content type → format note → tone → hooks → calls to action. Each starts with a line `GUIDE: <title> (<id>)`.

**Written to be token-light** (Samuel, 2026-09-22): terse lines, no repeats of rules the master prompt already enforces. Word caps per entry: 250, tones 90, hooks 35, calls to action 30. The script refuses anything longer.

**Budget: 2,400 words** (about 3,200 tokens). Over it, drop priority 3 (the niche and format notes), then 2, from the end. Today the largest request (`review_full`, storytelling) loads about 2,050 words (about 2,700 tokens), so nothing is dropped.

## For the devs

- **Load `_export/guides.json` at server start** and filter in memory. 51 entries is small. `_export/vocab.json` has every allowed value with the label the app shows.
- A database is optional. If you want one: one table, one row per entry, the four tag fields as text arrays, and this filter:

```sql
WHERE status = 'active'
  AND ('any' = ANY(actions)       OR :action       = ANY(actions))
  AND ('any' = ANY(content_types) OR :content_type = ANY(content_types))
  AND ('any' = ANY(tones)         OR :tone         = ANY(tones))
  AND ('any' = ANY(audiences)     OR :audience     = ANY(audiences))
```

- `00-System/scripts/build_scripnals_guides.py` is the reference: `select()` is the matching rule and the budget, `guides_text()` builds `{{guides}}`.

## For Samuel: editing

1. Edit or add a `.md` file. Keep tag values from `vocab.json`.
2. Run `python 00-System/scripts/build_scripnals_guides.py`. It checks every file and rewrites the export.
3. See what one request loads: add `--select action=rewrite content_type=storytelling tone=friendly audience=creator`. Add `--prompt out.txt` to get the exact guide text for a test in Claude chat.
4. `--check` before committing.

## How it grows

- **Change an entry:** edit it and raise its `version` by 1.
- **Add an entry:** a new file in the right folder, tags from `vocab.json`, inside the word cap.
- **Retire an entry:** set `status: paused`. It stops loading but stays on record.
- Run the script, `--check`, commit with a line on what changed and why. Then send the devs the new `guides.json`.
- **Server side:** swapping `guides.json` and restarting is all an update needs. No app release, no code change.
- A new rule from outside research stays a suggestion until Samuel confirms it. Add its source to [[03-Areas/scripnals/guide-library-research|the research note]].

## Before sending (2026-09-27)

- [ ] Samuel reads the core, action and content-type entries (17 files). Those carry the product.
- [x] Samuel confirmed the review score bands and the 18 hook names (2026-09-22).
- [ ] Test: the master prompt plus `--prompt` output on 3–4 real drafts in Claude chat. Check nothing is invented, the score only appears on a full review, the JSON is valid, and **the result still sounds like the person who wrote the draft.**
- [ ] Send `_export/guides.json`, `_export/vocab.json` and this note. Line in [[03-Areas/scripnals/scripnals-log|Log]].

Back to [[03-Areas/scripnals/scripnals|Scripnals]]
