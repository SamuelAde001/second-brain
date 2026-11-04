---
type: sop
area: video-editing
status: approved
approved: 2026-11-04
updated: 2026-11-03
source: interview
tags: [rulebook]
section: A5
---

# A5 · Transcription and the transcript doc

> **Read when:** after the silence pass and sections, building or rebuilding the transcript doc, and before planning visuals (Editor, end of phase 1 and after Samuel's re-cut). **Client values:** none (each client's names and brand words go on the job's fix list). **Status:** approved by Samuel rule by rule, 2026-11-04.

## Rules
### When
- **A5.1** Always transcribe, **after Samuel's review and re-cut**, so the transcript matches every word he added or removed. It is the reference for the rest of the edit. ✅ *"till the cuts and the transcription as usual"* (2026-10-19) · *"Transcript should be done after my review and recut so it gets things accurately in case a word was added or removed"* (2026-11-04) · ✏ 2026-11-04
- **A5.2** Transcribe his final cut, never the raw. ⚙️ (follows A5.1) · ✔ 2026-11-04
- **A5.3** The visual stage starts from the transcript: transcribe, watch the whole video, then plan. ✅ *"you transcribe the video, then you take your time and go through the whole video"* (2026-10-20) · ✔ 2026-11-04
- **A5.4** When he re-cuts, re-time the words and sentences to his live cut before planning visuals. If beat frames came from an old cut, re-transcribe the latest render. An old word map drifted 15 to 69 frames. ⚙️ (2026-10-26) · ✔ 2026-11-04
- **A5.5** Key every cut-sheet and beat timecode to the cut timeline (or its subtitle file), never to the raw footage or the written script. ⚙️ · ✔ 2026-11-04

### The doc, "like I always do"
- **A5.6** A Word `.docx` in ALL CAPS, one section per chapter, each section heading filled with its section colour (A4). ✅ *"transcribe the cut video into a document like I always do"* (2026-09-24) 🎬 (2026-09-06) · ✔ 2026-11-04
- **A5.7** A red NOTE at every switch between A-roll and screen. ⚙️ · ✔ 2026-11-04
- **A5.8** Prompts that are typed or dictated on screen sit in a purple box. ⚙️ · ✔ 2026-11-04
- **A5.9** NOTEs also mark: where the footage leaves the script, numbers to check, the client's production notes and "remove this" lines, and anything to check by ear. ⚙️ · ✔ 2026-11-04
- **A5.10** Build it with `03-Areas/video-editing/scripts/transcript_docx.py`, one section per colour run; to rebuild, parse the previous doc back into a spec. Name it `Transcript - Cut vN sections (YYYY-MM-DD).docx` in `Docs\`. ⚙️ · ✔ 2026-11-04
- **A5.11** Beside the doc, keep timeline-frame text files per cut: `sentences.txt` (start frame, tab, sentence), `cut_words.json`, `sections.json`. Agents read these, not the doc. ⚙️ · ✔ 2026-11-04
- **A5.12** Subtitle-based transcripts follow the [[00-System/skills/subtitle-transcript-formatter/subtitle-transcript-formatter|subtitle-transcript-formatter]] skill. ⚙️ · ✔ 2026-11-04

### Getting the words right
- **A5.13** Use the client's script to guide the transcript, every time. Where the footage follows the script, the script settles the words. Where it leaves the script, say so in a NOTE. ✅ *"Did you use the script to guide in the transcript?"* (2026-09-29) · ✔ 2026-11-04
- **A5.14** Fix mishearings from the script and context with a fix list per job: "an 8-N" = n8n, "clawed / Cloud / Clod" = Claude, "Gemma" = Gamma, "a benefit" = "a bad fit". 🔁 (2026-09-29, 10-22, 10-30) ⚙️ · ✔ 2026-11-04
- **A5.15** A prompt typed on screen settles a doubtful line word for word. ⚙️ · ✔ 2026-11-04
- **A5.16** Check every number against the audio, not the transcript (he said 700, the screen said 1,700). Whisper also splits thousands ("1" ",043"), so a failed number check means: listen first. Where the transcript is unsure, on-screen wording follows the script. 🎯 (2026-10-26) · ✔ 2026-11-04
- **A5.17** Show the number he said on camera, even when the file or source has a more exact figure. ✅ *"No, show the number he said"* (2026-11-04) · ✏ 2026-11-04

### Tools
- **A5.18** Use word-level Whisper (`03-Areas/video-editing/scripts/uhm_transcribe.py`) for fillers and word times. Resolve's transcription strips fillers (1 "ah" in 3,351 words) and inflates word end times. ⚙️ · ✔ 2026-11-04
- **A5.19** Resolve's transcription and subtitle calls (polling, rates, GUI-only export, menu fallback): open [[03-Areas/video-editing/resolve-automation-lessons|Resolve automation lessons]] and [[03-Areas/video-editing/sops/routerise-cut-workflow|cut workflow]] step 3 before scripting them. ⚙️ · ✔ 2026-11-04

## Never (strict)
- **A5.20** Never hunt "um"s with Resolve's transcript. ⚙️ · ✔ 2026-11-04
- **A5.21** Never put a number on screen from the transcript alone. 🎯 (2026-10-26) · ✔ 2026-11-04
- **A5.22** Never sleep inside a Resolve `run_script` call while waiting for a transcription: it blocks Resolve. ⚙️ · ✔ 2026-11-04

## Pictures
- (no picture yet: one page of an approved transcript doc showing coloured headings, a red NOTE and a prompt box would help)

## Questions for Samuel
- **Q-A5.a** Order: on 2026-09-29 you set "cut, you review and approve, then sections, transcript, visual cut sheet". Since 2026-10-12, sections and transcript are done in phase 1 before your review (the Gamma transcript, 2026-10-30), then re-timed to your re-cut. → Options: (1) transcript in phase 1, rebuild the doc after your re-cut (2) only after you approve the cut. My pick: (1); your later words "till the cuts and the transcription as usual" (2026-10-19) point there. → Samuel: (2), after his review and re-cut (2026-11-04). A5.1, A3.5 and A1.1 updated.
- **Q-A5.b** After your re-cut: rebuild the whole Word doc, or only re-time the text files agents use (A5.11)? → Options: (1) both (2) text files only, doc on request. My pick: (1). → Samuel: (1) both: the Word doc and the text files (2026-11-04).

## Sources
Replaces or draws on [[03-Areas/video-editing/sops/routerise-cut-workflow|Route Rise cut workflow]], [[03-Areas/video-editing/sops/visual-sheet-pipeline|Visual sheet pipeline]], [[03-Areas/video-editing/workflow|Workflow]], [[03-Areas/video-editing/toolchain|Toolchain]], [[03-Areas/video-editing/cut-sheets|Cut sheets]], [[03-Areas/video-editing/routerise-house-style|Route Rise house style]], [[07-Agents/video-editor/memory|Editor memory]] and the job notes.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
