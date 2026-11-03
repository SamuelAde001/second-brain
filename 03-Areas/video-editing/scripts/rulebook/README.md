---
type: sop
area: video-editing
status: active
updated: 2026-11-03
source: manual
tags: [rulebook, scripts]
---

# Rulebook scripts

The scripts that built the [[03-Areas/video-editing/rulebook/rulebook|editing rulebook]] (2026-11-03) and keep it honest. Samuel, 2026-11-03: *"don't forget to document the scripts you use"*. All are stock Python 3; `rb_images.py` also needs ffmpeg. `--work` is any scratch folder (use the session scratchpad, never the Brain). Each script's header says the same in more detail.

| Script | What it does | When to run it |
|---|---|---|
| `rb_extract.py --work <dir> [--chunks 4] [--since YYYY-MM-DD]` | Pulls every message Samuel typed out of this Brain's Claude Code transcripts (read-only), drops tool output, reminders and duplicates, keeps the editing ones by keyword, splits them into equal date chunks for helpers. Writes `samuel_all.md`, `samuel_video.md`, `samuel_video_big.md`, `chunk1..N.md`. 2026-11-03: 1,156 messages, 559 about editing. | Rebuilding the evidence; `--since` to catch only new corrections since the last pass. `rb_quotecheck.py` needs its `samuel_all.md`. |
| `rb_markers.py --out <dir>\markers_all.md` | Collects every marker note Samuel left on our timelines from the marker dumps in each job's `Docs\` (any JSON with "marker" in its name), with the spoken words and beat ids under it. 2026-11-03: 359 markers from B2B, LinkedIn and video 2. | After any marker round is dumped, and before a quote check. |
| `rb_merge.py --work <dir>` | Sorts the evidence helpers' `ev_<group>.md` files into one `sec/<CODE>.md` per rulebook section, each line tagged with its source group; CONFLICTS, VIDEOS SEEN, GAPS, IMAGE CANDIDATES get their own files. | After an evidence pass. The 2026-11-03 output is archived in `08-Archive/brain-build/rulebook-evidence-2026-11-03/`. |
| `rb_quotecheck.py --work <dir>` | Checks that every *"quote"* in the rulebook is Samuel's real words: found word for word in his messages, the markers, a Brain note or a job doc. Prints any that aren't. 2026-11-03: 800 quotes, 6 paraphrases found and fixed. | After any rulebook edit that adds a quote. |
| `rb_images.py --work <dir>` | Copies the pictures listed in `img_*.txt` manifests (`<source path> -> <name>.jpg`) into `_attachments/rulebook/` as JPGs at most 960 px wide. Sources are only read. | When a section gets a new reference picture. |
| `rb_status.py [--section A1] [--pending]` | Where Samuel's rule-by-rule review stands: per section, rules approved ✔, corrected ✏, dismissed ✖, still waiting, and questions answered. `--pending` lists the undecided numbers. | Before and after every review batch. |

## How the rulebook was built (to redo or extend it)

1. `rb_extract.py` and `rb_markers.py` into a scratch folder.
2. Evidence pass: one helper (`editor-builder`) per source group, briefed with [[03-Areas/video-editing/scripts/rulebook/briefs/evidence-brief|the evidence brief]] and [[03-Areas/video-editing/scripts/rulebook/briefs/taxonomy|the section codes]], each writing `ev_<group>.md`. On 2026-11-03: 4 groups of his messages, 5 groups of Brain notes, 1 of job folders; about 2 weekly points.
3. `rb_merge.py`.
4. Drafting pass: one helper per section group, briefed with [[03-Areas/video-editing/scripts/rulebook/briefs/drafting-brief|the drafting brief]], writing the `rb-*.md` notes and `img_<group>.txt`.
5. `rb_images.py`, `python 00-System/scripts/audit_brain.py` (links), `rb_quotecheck.py` (quotes), `rb_status.py` (counts).

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]] · [[03-Areas/video-editing/video-editing|Video editing]]
