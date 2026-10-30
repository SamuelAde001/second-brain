---
type: sop
area: video-editing
status: active
updated: 2026-10-30
source: manual
tags: [pipeline, scripts, audio, sound]
---

# Pipeline audio scripts (promoted from video 4)

Reusable sound-plan and loudness scripts for the Editor, promoted from video 4's one-off scripts on 2026-10-30. None of them starts or drives Resolve. Back to [[03-Areas/video-editing/video-editing|Video editing]] · sibling: [[03-Areas/video-editing/scripts/pipeline/checks/README|check scripts]].

Run with plain `python` (numpy and scipy are in the user site, so not `-I`; ffmpeg on PATH). Chain after any beat fix: `sfx_events` -> `sound_plan` -> `mix_check` -> `sound_notes`; on a render: `loudness`, then `master`. Video 4's creative choices (palette, pins, auto adds, quiet cues, notes wording) are JSON files in `examples\`: copy and edit them for the next video.

| Script | What it makes or checks | Inputs | Example command |
|---|---|---|---|
| `sfx_events.py` | Every visual event (pop, reveal, count, cut-in, click...) of the installed timeline, in timeline frames, read from the manifests and `.setting` files. Writes `sfx_events.json`. | install list | `python sfx_events.py --list list.txt --out sfx_events.json` |
| `sound_plan.py` | `sound_plan.json` for sound_place: music plus SFX pins resolved from the events, held to the bible 07 caps and the reference video's levels; lists problems, clamps, drift. | `--config` cues json, events json, music plan json, SFX library and job SFX folders | `python sound_plan.py --config examples\video4_sound_plan.json --events sfx_events.json --music music_v4.json --out <dir> --sfx-dir <Sound effects> --assets-sfx-dir <Visual Assets\SFX> --len 12100 --hook-end 1426 --timeline "<name>"` |
| `mix_check.py` | Offline mix of the plan (lav at +6 dB, music, SFX): loudness, true peak, limiter activity, speech minus bed per section and per SFX hit. Writes `mix_check.json`. About 30 s. | `sound_plan.json`, cut items, conformed lav wav | `python mix_check.py --plan sound_plan.json --items cut_items.json --lav lav.wav --len 12100 --out <dir> --cut-label "Cut v5"` |
| `sound_notes.py` | `sound_notes.md`: every SFX, per-file counts, checks run, changes against the plan, open points. | plan, mix check, events json, `--notes` wording json | `python sound_notes.py --plan sound_plan.json --mix mix_check.json --events sfx_events.json --notes examples\video4_sound_notes.json --len 12100 --hook-end 1426 --out <dir>` |
| `loudness.py` | Integrated LUFS, true peak, LRA of a render; `--fix` writes a two-pass -16 LUFS / -1 dBTP copy (video copied). Also imported by `master.py`. | one render | `python loudness.py render.mp4 [--fix out.mp4]` |
| `master.py` | Masters a render to -16 LUFS / under -1 dBTP (gain + oversampled limiter, delay removed) and checks sync at 3 points; exit 1 on failure. | render, output path | `python master.py render.mp4 mastered.mp4` |
| `music_scan.py` | Every song in the libraries: duration, p90 level, body span, per-0.1 s level curve. Writes `music_scan.json`. Slow on a full library. | one or more music folders | `python music_scan.py --music-dir <library> --out <dir>` |
| `palette_check.py` | The SFX palette files exist and decode: duration, peak, loudest 100 ms. Writes `palette_check.json`. | `--palette` json, SFX folders | `python palette_check.py --palette examples\video4_palette.json --sfx-dir <Sound effects> --assets-sfx-dir <Visual Assets\SFX> --out <dir>` |
| `speech_levels.py` | Speech vs bed levels (p5..p90, per-minute bed p10 and speech p80) of lav files and delivered mixes. Writes `speech_levels.json`. | `--sources` json of name -> wav or glob | `python speech_levels.py --sources examples\video4_speech_levels.json --out <dir>` |

Config roots: `sfx:` = `--sfx-dir`, `assets:` = `--assets-sfx-dir`, `conv:` = `--conv-dir` (converted wavs, default `<out>\converted`). `--len` is the timeline length in frames, `--hook-end` the last hook frame.

Examples: `examples\video4_sound_plan.json`, `video4_sound_notes.json`, `video4_palette.json`, `video4_speech_levels.json`.
