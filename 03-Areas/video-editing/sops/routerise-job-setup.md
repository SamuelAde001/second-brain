---
type: sop
area: video-editing
status: active
updated: 2026-09-24
source: manual
tags: [sop, routerise, setup]
---

# SOP — Routerise job setup (card → footage on a synced timeline)

**Trigger:** a new Route Rise card lands in ClickUp at READY TO EDIT. Samuel, 2026-09-24: *"Get all the things sorted till putting on the timeline and syncing audio"*. First run: [[04-Projects/routerise-4-ai-tools|Route Rise #3 — 4 AI Tools]].
**Owner:** Editor. Samuel takes over from the synced timeline ([[03-Areas/video-editing/sops/routerise-cut-workflow|cut workflow]] step 2 on).
**Ends when:** footage is local and sorted, the brief is saved offline, the Resolve project exists, and the A-roll is on V1 with the mic synced on A1.

## What a card carries

- An **idea doc** on Route Rise Media's Notion (titles, thumbnail brief, summary, full script, comments from the writer). Status/deadline fields on the Notion page go stale; the ClickUp card's dates are the real deadline.
- A **Google Drive folder** from Alex (`alex@frontal.so`), named like `3 - 4 AI Tools`. On the first job it held the A-roll (`C07xx.MP4`, ~12.5 GB), the DJI mic (`TX02_MICxxx_<date>_<time>_orig.wav`) and a Google Doc called "Screenshare" that is only a **Tella link**. The screen recording lives on Tella, not in Drive.

## Steps

1. **Folder.** `C:\Users\repzy\Desktop\Video edits\Routerise\<card title exactly>\` with `Client raws/`, `Screen recordings/`, `Docs/`, `Screenshots/`, `B-roll/`, `Music/`, `SFX/`, `Graphics/`.
2. **Drive footage.** The shared folder isn't in his Drive and the Drive connector can't list inside it. Open the folder link in the in-app browser: it's link-shared, so it lists without sign-in. Read the file IDs from the page (`[data-id]` elements). Then download with `03-Areas/video-editing/scripts/drive_download.py <id> "<out>" --threads 10`. One connection runs at ~2–3 MB/s; parallel ranges roughly double it. Small files (the WAV) are fine with a plain `curl -L "https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t"`.
3. **Tella screen recording.** Read the "Screenshare" doc with the Drive connector to get the Tella link. On the Tella page: Download → Size **4K**, 30 fps (the export is 3840×1912 for a 1920×956 story) → the export renders server-side in a couple of minutes. Poll `https://prod-stream.tella.tv/export/list?story_id=<vid_…>` from the page; when `status` is `completed` it carries a signed `downloadUrl`. Save that URL to a scratch file and run `drive_download.py @<file> "<out>" --threads 6`. Don't rely on the in-app browser's own download. Note the Tella chapters; they're Alex's section map.
4. **Notion idea doc.** The Notion connector can't see Route Rise's workspace (404). **Open it in Samuel's Chrome**, where he's signed in (his instruction, 2026-09-24). Expand every toggle (click each `[aria-expanded="false"]` button), read the page text, and save it as `Docs/Idea doc and script.md` plus a Word copy: `03-Areas/video-editing/scripts/md_to_docx.py "<md>"`. Add a short "what was actually shot" note at the bottom (files, Tella chapters, where the chapters differ from the script).
5. **Resolve project from his template.** In the Resolve project folder `Routerise`, export `Project Template` to a scratch `.drp` (`ProjectManager.ExportProject`) and import it under the card title (`ImportProject(path, name)`). The template brings the bins (Raw vids, Screen records, Music, SFX, Assets…) and 1080p 23.976.
6. **Import.** A-roll and mic into `Raw vids`; Tella MP4 into `Screen records`.
7. **Sync.** Try `MediaPool.AutoSyncAudio` on waveform first. If it returns False, run `03-Areas/video-editing/scripts/av_sync.py "<camera>" "<mic>"`. It checks the camera's scratch audio: if it's alive it cross-correlates camera audio against the mic (10 ms precision); if dead, it uses motion correlation. Offset > 0 means the mic started before the camera.
8. **Timeline.** A duplicate-safe new timeline in the job's project: A-roll on V1, mic on A1 aligned by the offset, at +6 dB ([[03-Areas/video-editing/sops/routerise-cut-workflow|cut workflow]] inputs). Screen recording stays in its bin; it goes on V2 during the cut.
9. **Log it.** Project note, [[07-Agents/video-editor/log|Editor log]], area log. Commit.

## Failure modes seen

- Tella's Download button crashed the in-app browser's page once. The export API route above is the reliable one.
- Parallel downloads share one line: two big downloads at once slow each other. Start the biggest first.
- The Notion page's own deadline field was a month stale (2026-08-25).

Back to [[03-Areas/video-editing/video-editing|Video editing]]
