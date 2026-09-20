---
type: decision
area: system
status: active
updated: 2026-09-20
source: manual
tags: [decisions, system]
---

# Structural decisions

Decisions about the vault itself: its structure, rules, agents and automations. Area-level decisions live in that area's `decisions.md`. Append-only.

---

## 2026-09-20 — Vault lives at `C:\Users\repzy\Desktop\My Second brain`
**Decided:** the vault stays at its existing Desktop path rather than moving to `C:\SecondBrain` as the build spec assumed.
**Why:** Obsidian is already pointed at it, and the path is outside OneDrive and Dropbox, which was the actual requirement.
**Alternatives rejected:** moving it, which would break the existing Obsidian vault registration for no gain.
**Who decided:** Samuel (Phase 0 gate).

## 2026-09-20 — GitHub is the sync spine, not a paid sync service
**Decided:** the private GitHub repo is both the backup and the PC-to-phone sync path. The PC commits and pushes; Android pulls and pushes through the Obsidian Git community plugin.
**Why:** Obsidian Sync costs money Samuel is not spending on this. The vault is text-only and small, and the phone only writes to `01-Inbox/`, which keeps conflicts rare.
**Alternatives rejected:** Obsidian Sync Standard (paid). Syncthing (free, but two systems to maintain and no off-machine backup by itself) — kept as the documented fallback if the Git plugin proves flaky.
**Cost accepted:** a GitHub personal access token must live in the phone plugin's settings. It never goes in a note or the repo.
**Who decided:** Samuel (Phase 0 gate).

## 2026-09-20 — Contentinfluence is history, not an area
**Decided:** Contentinfluence gets imported into `03-Areas/personal-brand/` as a past attempt at personal-brand coaching — what it was, why it failed — not as its own area.
**Why:** it is a dead brand. The lessons matter; the structure does not.
**Who decided:** Samuel (Phase 0 gate).

## 2026-09-20 — No church area
**Decided:** the church / AAC media work gets no area. Files stay where they are on disk.
**Why:** there is not enough of it to manage. If church editing work ever needs tracking, it becomes a client note under video-editing.
**Who decided:** Samuel (Phase 0 gate).

## 2026-09-20 — HighSignals is the community; the personal brand is Samuel himself
**Decided:** `03-Areas/personal-brand/` is Samuel's own brand — him, Instagram handle @SamuelSignals. `03-Areas/community/` is HighSignals. The build spec had these conflated and called HighSignals the personal brand; it is wrong and the correction stands.
**Why:** Samuel said so plainly. Getting this wrong would have mislabelled every note, goal and content decision in two areas.
**Who decided:** Samuel, 2026-09-20.
**Follow-up:** the Phase 3 interview must settle where Called to Edit Academy, the mentorship program and the book sit relative to the brand and the community.

## 2026-09-20 — CORRECTION to the entry above: HighSignals is the umbrella brand
**Decided:** HighSignals is the whole brand. It contains four branches: HighSignals Community, HighSignals Academy, Mentorship, and the Scripnals app. Samuel's personal brand (@SamuelSignals) is a **separate brand outside HighSignals** whose job is to funnel people into it.
**Why:** Samuel stated it directly. The entry above, recorded earlier the same day, captured only half of the correction — that HighSignals is not his personal brand — and wrongly concluded it was just the community.
**What changed in the vault:** new area `03-Areas/highsignals/` holds brand-level strategy. Community, Academy, Mentorship and Scripnals stay as top-level areas, each linking up to it. AGENTS.md §1 and §2 updated. `03-Areas/community/_index.md` conflict section replaced with the resolution.
**Alternatives rejected:** nesting the four branches inside `highsignals/` (deeper paths, longer cross-links); leaving the tree flat with no umbrella (brand-level strategy would have had nowhere to live).
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — Calibration: notes keep source detail verbatim
**Decided:** extracted notes preserve specifics — full topic banks, exact fixed lines, rejected alternatives, the reasoning behind a rule — rather than summarising them away.
**Why:** Samuel reviewed three sample notes at the Phase 2 calibration gate and confirmed the depth. The test is whether an agent can act from a note without coming back to him.
**Cost accepted:** longer notes, more context per read.
**Who decided:** Samuel, 2026-09-20.

## 2026-09-20 — Git permission rule added
**Decided:** `.claude/settings.json` allows `git add`, `commit`, `push`, `status`, `log`, `diff`, `ls-remote`, and denies reads of `.env`, `*.key`, `credentials*.json`, `token*.json`.
**Why:** Samuel did not want to run every push by hand. Pushing to his own private repo is the one outward action this build needs repeatedly.
**Who decided:** Samuel, 2026-09-20.

