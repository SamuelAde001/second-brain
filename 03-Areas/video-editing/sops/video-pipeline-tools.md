---
type: sop
area: video-editing
status: active
updated: 2026-10-28
source: manual
tags: [pipeline, lint, preview-gate, render-queue, resolve, helpers]
---

# Video pipeline tools: beat lint, preview gate, render queue

The three scripts the zero-revision pipeline needs (Samuel, 2026-10-28: *"If we can do a great quality Job that never needs my correction nor the creative directors corrections, that is the biggest token saver"*). The pipeline itself, steps 1-8, is in [[00-System/model-routing|model routing]] → Audit 2026-10-28; this note is how to run its tools. The rules they check are on [[03-Areas/video-editing/samuel-review-card|Samuel's review card]]. Part of [[03-Areas/video-editing/video-editing|Video editing]].

## Where they live

- **Canonical:** `03-Areas/video-editing/scripts/pipeline/` in the Brain: `beat_lint.py`, `preview_page.py`, `render_queue.py`, and `fusion_setting.py` (reads a .setting into Python; the lint uses it).
- **Copies beside `lab.py`** in the master kit `Routerise\Visual Assets\Frontal templates (Editor)\kits\`, so a job kit copied from the master has them. After changing a Brain copy, copy the four files over the kit copies. Never edit a kit copy.
- The queue hand-off version of `lab.py` is `kits\lab_with_queue_2026-10-28.py` in the master kit (new file; the master `lab.py` stays as it was). When a job's kit is set up, copy it over the job kit's `lab.py`. Video 2's kit is never changed: it is delivered and kept as the reference.

## Step 3: beat lint (no AI, no Resolve)

Run by the worker on its own beats before it reports done, and by the Editor on a whole section before any reviewer.

```
python beat_lint.py --words "<Docs>\...\words_cut.json" --beats "<Docs>\<plan>\beats.json" [--section hook] [--out <report.json>] "<kits>\..\comps\<run>"
python beat_lint.py --why <report.json> <BEAT>        one beat's findings, for the worker that fixes it
python beat_lint.py ... --by-type <folders>           adds a table per comp type (chart, page/UI, lower third, list, counter, card)
python beat_lint.py --words <w.json> --setting <comp.setting> --start <timeline f> --D <n> [--beat ID]    one comp before it has a manifest
```

- Input: every `manifest.json` under the folder (its `comp` ops and .setting files), the job's word timings (timeline frames of the cut) and the plan's `beats.json` (section, kind, Alex's line). Media ops are not linted.
- Output: one line per beat, `ok` / `FAIL` / `-` (nothing to check) per rule, element and unmatched counts; the details go to the report json. Exit 1 on any FAIL. About 0.03 s a beat (142 beats in 4.4 s).
- **What each rule checks** (thresholds from video 4's `Docs\CD rules from video 2 (2026-10-26).md`):
  - **P1** each element (NeoAnim, NeoMotionText, counter, fade) is readable 0-3 f after its word, widened to -1..+5 f for Whisper's error; never before the word. A counter is judged on the count's end against the end of the spoken number. No two separate elements enter on the same frame. An element's word is the first word of its text heard in the op ±1 s, or a cue in the manifest op: `"cues": {"NeoAnim_Logo": "Stripe"}`. Give cues for logos, icons and boxes: with no text and no cue an element is counted as unmatched, not checked.
  - **P2** a number said in the beat and shown at 72 px or more on its own is a counter; a counter is never on one line with same-size words (a number inside a sentence is plain text). Axis ticks, 0 and ordinals 1-9 are skipped.
  - **P3** every NeoMotionText has PosDir 0 (Up) and Scope 1 (word); a static Text+ of 3+ words at 56 px or more fails.
  - **P5** no tool named strike/cancel/crossout, no thin red bar across a text.
  - **C3** the last element is landed 36 f before the cut (or the start of an exit animator). Wipes, line draws and pushes are not elements. An op that butts into the next op of the same beat on its track is judged at the end of the sequence.
  - **C6** text over undarkened A-roll (an adj comp or a comp with no ground of its own and no op under it) sits at y ≥ 900 px and the text group is centred (|x − 960| ≤ 120). A darkened statement layout is not a lower third.
  - **C7** text height on the frame: ≥ 56 px over footage, ≥ 40 px on a ground or a page, ≥ 36 px in a UI rebuild.
  - **C9** every number on screen is heard in the beat (±1 s) or elsewhere in the video. The lint hears Whisper, not the audio: **listen to every C9 fail before changing anything.** Its one fail on video 2 is P4-14's "700", which Whisper heard as 1,700; the creative director heard 700 (note #15).
- Known limits: px comes from Size and the kit's font heights (Inter 1.210, JetBrains Mono 1.320, Season 1.229) times the first downstream Transform/Merge Size; text width is estimated. Motion feel, lighting (C1), darkness (C2), density (C4), centre (C5) and taste stay with the Opus filmstrip review (step 4).

## Step 8: render queue (one script owns Resolve)

Start it once per job before helpers build; it runs until stopped (Ctrl+C) or `--idle-exit` seconds with nothing to do. Run it in the background or in its own terminal.

```
python render_queue.py run --kits "<job>\Graphics\Frontal kit (Editor)\kits" --project "<job project name start>" [--batch 6] [--frame-budget 2010] [--mem-gb 16]
python render_queue.py status --kits <kits>
python render_queue.py clip --kits <kits> --manifest <beat>\manifest.json --out <dir> [--pad 12] [--res 960x540]
python render_queue.py submit --kits <kits> <request.json>
python render_queue.py wait --kits <kits> <id> ...
```

- **Helpers keep calling `lab.py render ...` as before.** While the queue runs, lab.py drops the job in `kits\_queue\requests\` instead of waiting on the lock, then waits for its done file and prints the same json. Add `--nowait` to get `{"queued", "done"}` back at once and keep building; read the done file later. `--direct` bypasses the queue (only when the queue is stopped on purpose).
- Each request gets `kits\_queue\done\<id>.json` (ok, files, errors, secs, tries). The queue log is `kits\_queue\queue.log`.
- It renders up to `--batch` requests per pass in one worker process, holding lab's lock as `render-queue`; an install run (`kit-pipe`) holding the lock makes it wait.
- **A hang:** each Resolve step has a budget; past it the worker is killed, Resolve is restarted (`restart_resolve.py`, `--force` when Windows still says it responds, because a timed-out script keeps running inside Resolve), the project reopened (`open_job.py --name`), and the request retried once. A request that hangs twice gets a failed done file: look at the comp.
- **Memory:** between batches it restarts Resolve with `--force` after 2010 rendered frames or when Resolve uses more than `--mem-gb` (video 2 v7: one 4K pass crashed at ~3000 f, 2010-f chunks with a restart each rendered clean; memory climbed 6 → 19.5 GB over a long lab session on 2026-10-25).
- Clip requests (`kind: clip`, or `manifest` + `clip`) lay the whole beat on `zz Lab (Editor)` over the cut's A-roll with its sound, pad frames either side, and render one small H.264 mp4 from Deliver.

## Step 7: Samuel's preview gate

One page per section, only motion-graphic beats (plan kinds `motion-graphic`, `overlay`, `aroll-fx` whose manifest has a comp). Screen recordings, captures, UI demos and B-roll are left out.

```
python preview_page.py build --beats <beats.json> --section <sec> --comps <comps dir> --docs "<job>\Docs" --kits <kits> --render
python preview_page.py build ... --from-render <full timeline render.mp4>     beats already on a rendered timeline
python preview_page.py read "<path>\preview_<sec>_notes.json"
```

- Writes `<job>\Docs\Preview <sec> (Editor)\preview_<sec>.html` and `clips\<beat>_<hash>.mp4`. The hash covers the manifest and its .setting files, so a rebuilt beat gets a new clip and an unchanged one is never rendered again.
- Samuel opens the page, plays each clip (Space under the mouse), presses **Approve** or **Note** and types what to change, then **Save notes**: `preview_<sec>_notes.json`, into the folder he picks (Chrome/Edge) or Downloads. The page also keeps his marks in the browser while he works.
- The Editor reads it with `read`, puts each note on the review card the same session, turns notes into fix specs, and only approved beats go on the timeline.

## Tested on video 2, 2026-10-28

Video 2 is read only (delivered): every test works on copies in its `Docs\Pipeline tools test (Editor)\`.
- Lint on copies of the 141 installed beats (185 comps) by type: `Lint v7c (Editor)\`. Hook section, first run: `Lint first run (Editor)\`.
- Queue mechanics in `--fake` mode: batches, a hung request killed and retried once then failed, lab.py hand-off with and without `--nowait`.
- Preview page for the hook from the v7 4K render (`--from-render`): 5 beats, 5 clips, `Preview hook first run (Editor)\preview_hook.html`.
- Not yet: a live queue run in Resolve. It goes in a scratch project, never in video 2's project or timelines.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
