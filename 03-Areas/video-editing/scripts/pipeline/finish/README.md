---
type: knowledge
area: video-editing
status: active
updated: 2026-10-30
source: manual
tags: [pipeline, finish, resolve, scripts]
---

# Finish scripts (install, check, render, master)

Promoted from video 4 (Night run 2026-10-28) on 2026-10-30; every job path, project, timeline, version tag and beat list is now an argument. Area: [[03-Areas/video-editing/video-editing|Video editing]]. Sibling: `..\render_queue.py`.

Shared arguments: `--job <job folder>` gives `--kits` (default `<job>\Graphics\Frontal kit (Editor)\kits`) and `--out` (default `<job>\Docs\finish`). Resolve scripts take the kit's lock (`lab.py`): run them with the render queue stopped. `J` below is the job folder.

| script | what it does | needs Resolve | example command |
|---|---|---|---|
| `finish.sh` | The whole chain: stop queue, install changed beats, snapshot check, A1 voice keep, chunked render, master, phone parts | y | `bash finish.sh --job "J" --project "4. The Cold" --base "Visuals v1 (Editor)" --new "Visuals v3 (Editor)" --beats IN-07,WN-08 --res 1080 --snapshot tl_after.json --cut "Cut v5 (Editor) - sections" [--from-render] [--dry-run]` |
| `install_loop.py` | Full install of the visuals onto a new timeline with crash retries (restart Resolve, reopen project, re-run) | y | `python install_loop.py --job "J" --timeline "Visuals v1 (Editor)" --src-timeline "Cut v5 (Editor) - sections" --list list.txt --mz mz.json` |
| `install_changed.py` | `seed`: copy base install records for the changed beats; `build`: install only those beats onto a copy of Samuel's timeline (his is never touched) | build y, seed n | `python install_changed.py build --beats IN-07,WN-08 --job "J" --timeline "Visuals v3 (Editor)" --src-timeline "Visuals v1 (Editor)" --ver v3 --replace` |
| `tl_snapshot.py` | Read-only JSON snapshot of a timeline: markers and every item per track | y | `python tl_snapshot.py tl_after.json --timeline "Visuals v1 (Editor)" --job "J"` |
| `tl_diff.py` | Compare two snapshots: new markers, removed/added items per track, render chunks to redo | n | `python tl_diff.py tl_before.json tl_after.json [--len 12100 --chunk 2020]` |
| `a1_voice.py` | Compare A1 Voice Isolation of the cut and the visuals timeline; `--keep` copies the cut's to the visuals one | y | `python a1_voice.py --timeline "Visuals v3 (Editor)" --src-timeline "Cut v5 (Editor) - sections" --keep --job "J"` |
| `render_review.py` | Deliver render of a timeline in chunks (H.264 1080p) holding the lock; `--chunk 99999` = one pass | y | `python render_review.py "Visuals v3 (Editor)" "J\Renders\v3 1080p (Editor)" --job "J" --name v3_1080 --from 0 --to 2020` |
| `render_frames.py` | Review frames (12/50/88 % of each beat, chunk joins, A-roll) and labelled contact sheets from a render | n | `python render_frames.py v3_1080.mp4 frames --job "J" --timeline "Visuals v1 (Editor)" --inst "Visuals v3 (Editor)" --len 12100 [--beats EN-04] [--off 2020]` |
| `timeline_check.py` | Check every beat manifest against install_v2x's rules; writes `list.txt`, `list_no_HK-00.txt`, `timeline_check.json` | n | `python timeline_check.py --job "J" --len 12100 --plan "J\Docs\Visual plan v2 (Editor)" --out "J\Docs\finish"` |
| `mz_build.py` | Build and check the A-roll MagicZoom plan (`mz.json`, `mz_notes.md`) from a zones file; `--check` re-checks after a fix round | n | `python mz_build.py --zones zones.json --items cut_items.json --words cut_words.json --len 12100 --out out --job "J" --full IN-07,IN-08 --v1-count 159 [--check]` |
| `mz_media.py` | Put MagicZoom on media adjustment clips inside a `.drt` (file edit; also importable: `merge_element`, `mz_hex`) | n | `python mz_media.py in.drt out.drt ops.json --job "J" [--off N] [--motion-blur]` |
| `render_chunks.sh` | Chunked final render: 2020-f chunks, Resolve restart before each, join, seam audio; resumable, `RERENDER` redoes chunks. Runs `resolve_guard.py preflight` first. finish.sh's render step | y | `JOB="J" LEN=12100 TL="Visuals v3 (Editor)" VER=v3 RES=1080 bash render_chunks.sh` |
| `kill_demo_chrome.py` | List (`--list`) or stop the headless Chrome `record_demo.py` leaves on a DevTools port | n | `python kill_demo_chrome.py --list` then `python kill_demo_chrome.py 9411` |

- `mz_build.py --zones` is a JSON list of `[start, end, mode, depth, stressed word, why]`; video 4's 35 zones were the `Z` list in its script (kept in its `mz.json`).
- Not promoted (video 4 one-offs): `sfx_fix_v3.py` and the v3c patch render + splice. `finish.sh` step 5 needs `master.py` (+ `loudness.py`) beside it or `--master <path>`; step 4 calls the kit's `build_v1.sh` (`--build <path>` to use another): that file still hard-codes video 4's job (JOB, LOG, RDIR, LEN) and calls the old `render_review.py` without `--kits`, so copy and fix it for the next job.
- Tested 2026-10-30 without Resolve: file-only scripts match the originals on video 4's files; Resolve scripts compile and print `--help` only.
