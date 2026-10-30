---
type: sop
area: video-editing
status: active
updated: 2026-10-30
source: manual
tags: [pipeline, scripts, checks]
---

# Pipeline checks (promoted from video 4)

Reusable file-only checks and plan makers for the Editor, promoted from video 4's one-off scripts on 2026-10-30. None of them starts or drives Resolve. Back to [[03-Areas/video-editing/video-editing|Video editing]] · sibling: [[03-Areas/video-editing/scripts/pipeline/audio/README|audio scripts]].

Run with plain `python` (not `-I`: numpy and scipy live in the user site). `--help` lists every argument. Video 4's values for the config files are in `examples\`: copy one, change the values, pass it with `--config` / `--anchors`.

| Script | What it checks or makes | Inputs | Example command |
|---|---|---|---|
| `accent_scan.py` | Every accent (non-white) NeoTextMotion node carries `StShineEnable 0` (DECISIONS #52). Prints counts and hits. | install list (one `manifest.json` path per line) | `python accent_scan.py --list list.txt` |
| `card_check.py` | Build-card rules the beat lint skips (S1 S2 S4 S5 BR SQ FONT TXT BEV), one line per comp; exit 1 on any FAIL. Samuel's own intro adj clip is exempt. | `.setting` files or folders | `python card_check.py <kit>\comps\v1` |
| `crosscheck.py` | Independent stage 5 cross-check: install list, MagicZoom zones (`mz.json`), S4 coverage, sound plan and SFX caps, S6 intro adj. Writes `crosscheck*.json`. | stage folder (`mz.json`, `mz_notes.md`, `sound_plan.json`), comps folder, cut items, `cut_words.json`, `BUILD LIST.json`, sfx events json, install list | `python crosscheck.py --stage <stage5> --comps <kit>\comps\v1 --items cut_items.json --words cut_words.json --build-list "BUILD LIST.json" --events sfx_events.json --list list.txt --len 12100 --hook-end 1426 --timeline "<name>" --v1-count 159 --hk-folder "HK-00 intro adj"` |
| `regress.py` | Frame-by-frame diff of two renders at 320x180; each changed span marked `expected` (inside a touched beat) or `UNEXPECTED`. Needs ffmpeg (cuda decode). | render A, render B, touched beats, folder with `installed_<beat>.json` | `python regress.py a.mp4 b.mp4 HK-03d,IN-05 --inst <kit>\renders\v2\INST\<timeline>` |
| `plan_check.py` | Visual plan: coverage per part, holes, overlaps, A-roll slivers, starts and edges against the words and cuts, seams, schema, capture ids. `--json` for the full result. | `plan.json` config, sections folder, `cut_words.json`, `sentences.json`, cut xml, `captures.json` | `python plan_check.py --config plan.json --sections-dir sections --words cut_words.json --sents sentences.json --xml cut.xml --captures captures.json` |
| `make_plan_docs.py` | Merges the section files into `beats.json` and one readable HTML plan (summary, coloured sections, hero stills). Imports `plan_check.py` beside it. | same as `plan_check.py` plus `sections.json` (colours, titles) | `python make_plan_docs.py <plan_check args> --sections-json sections.json --out <plan folder>` |
| `boundary_check.py` | Plan assembly check: holes, overlaps, group seams, plain A-roll under 12 f between visuals, visual starts off a word or cut, edges inside a word. | sections folder (or `beats.json` with `--merged`), `cut_words.json`, cut items | `python boundary_check.py --sections-dir sections --words cut_words.json --items cut_items.json --len 12100` |
| `make_build_list.py` | `beats.json` into `BUILD LIST.json`: look-anchor units, design units, 2-4 beat spec units (DP split). | `beats.json`, captures json, anchors json | `python make_build_list.py --beats beats.json --captures captures_v2.json --anchors anchors.json --out "BUILD LIST.json"` |

Cut items json = rows of `[type, track, start, end, src]`; `--len` is the timeline length in frames; `--hook-end` the last hook frame.

Examples: `examples\video4_plan.json` (plan_check, make_plan_docs), `examples\video4_anchors.json` (make_build_list).

Tested 2026-10-30 against the original video 4 scripts on video 4's real inputs: identical output (regress: v1 vs v2 1080p watch copies, 12100 frames).
