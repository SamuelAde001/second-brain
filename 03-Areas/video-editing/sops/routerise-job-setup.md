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
5. **A fresh Resolve project, never a copy of the template.** Samuel, 2026-09-24: *"Don't copy the template… it keeps the date created same as the day the template was created… create a new project and copy the bin in power bin called Folder structure"*. In the Resolve project folder `Routerise`, run `ProjectManager.CreateProject("<card title>")`. His new-project defaults already match the old template (1080p, 23.976, DaVinci YRGB). Set `perfCacheClipsLocation` to `C:\Users\repzy\Videos\CacheClip`. Then bring in the bins from the **"Folder structure template"** power bin. The scripting API can't reach power bins, so this is a GUI step:
   - Media page → Power Bins panel (bottom-left; drag its divider up to see it) → click "Folder structure template".
   - Click inside the browser, press Ctrl+A, and drag the 13 folders onto **Master** under Bins.
   - Confirm with the API that Master holds: AI Vids, Assets, Chat GPTweb images, Client's B-rolls, Fusion Comps and Adjustments, Musics, Raw vids, Screen records, Screenshots, SFX, Shorts B-rolls, Visual Inspo, Youtube B-rolls.
6. **Import.** A-roll and mic into `Raw vids`; Tella MP4 into `Screen records`.
7. **Sync.** If the camera's scratch audio has speech, `MediaPool.AutoSyncAudio` on waveform works. Otherwise (both shoots so far: max −61 dB), run `03-Areas/video-editing/scripts/av_sync.py "<camera>" "<mic>"`. It checks the camera's scratch audio: if it's alive it cross-correlates camera audio against the mic (10 ms precision); if it's dead it uses motion correlation. A positive offset means the mic started before the camera; a negative one means after. Confirm the offset on a second stretch where he's talking to camera.
8. **Timeline.** `CreateEmptyTimeline("A-roll synced (raw)")`.
   - Camera **picture only** (`mediaType 1`) on V1 at the timeline start, so the dead scratch audio never lands on the timeline.
   - Mic (`mediaType 2`) on A1 at `recordFrame = start + round(seconds_mic_started_after_camera × 23.976)`.
   - Link them with `SetClipsLinked([v, a], True)`, then `SetProperty("AudioVolume", 6.0)` on the mic ([[03-Areas/video-editing/sops/routerise-cut-workflow|cut workflow]] inputs).
   - Add two blue "Lip-sync check" markers, one near the start and one near the end, for Samuel to eyeball.
   - **Sync the screen recording too** (Samuel, 2026-09-24: *"you haven't synced the screen recording to the video also"*). Tella's export has clean audio from his laptop, so cross-correlate the Tella audio envelope against the mic (`av_sync.envelope` + `xcorr`, 20 Hz for the whole length, then 100 Hz on a 90 s stretch). Sweep 120 s windows along Tella first to catch cuts in the story; high-z windows must all give the same offset. Place Tella at `camera time = mic offset in Tella + mic offset after camera`: picture on V2 ("Screen rec (Tella)"), its audio on A2 ("Tella audio (ref)"), linked, **A2 disabled**. Add a green "Screen sync check" marker.
9. **Log it.** Project note, [[07-Agents/video-editor/log|Editor log]], area log. Commit.

## Failure modes seen

- Tella's Download button crashed the in-app browser's page once. The export API route above is the reliable one.
- Parallel downloads share one line: two big downloads at once slow each other. Start the biggest first.
- The Notion page's own deadline field was a month stale (2026-08-25).
- **Motion sync is only as good as the stretch you measure.** On the 4 AI Tools shoot, 150-second windows at 0–8 min and 20–28 min all read −9.80 to −9.95 s (z 7–15). Windows at 10–18 min gave garbage (z 3–5, offsets from −20 to +46 s) because he isn't talking there. Measure where he talks to camera and ignore low-z windows.
- `ProjectManager.DeleteProject` returned False on a project that wasn't loaded. Leave a clearly named leftover for Samuel to delete by hand.
- Right after `AppendToTimeline`, a screenshot of the timeline can lag behind the API. Trust `GetStart`/`GetEnd`, or press Shift+Z and look again.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
