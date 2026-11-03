---
type: sop
area: video-editing
status: draft
approved:
updated: 2026-11-03
source: interview
tags: [rulebook]
section: A1
---

# A1 · Download and sorting

> **Read when:** a new job card lands, before the first download (Editor, setup step; also when clearing disk space). **Client values:** where each client's footage and script arrive: [[03-Areas/video-editing/clients/routerise|Route Rise]], [[03-Areas/video-editing/clients/alex|Alex]], [[03-Areas/video-editing/clients/gamma|Gamma]]. **Status:** draft, not yet approved by Samuel.

## Rules
### Start of a job
- **A1.1** A job starts when a Route Rise card reaches READY TO EDIT in ClickUp. The Editor does phase 1 alone: download, sort, project, sync, cut, sections, transcript. Then stop and wait for Samuel's cut review. 🔁 (5 times: 2026-09-24, 10-12, 10-19, 10-26, 10-30) ✅ *"download the footage, cut it and as we normally do and wait till I revise the cuts"* (2026-10-30)
- **A1.2** Get the script first, before anything else. ✅ (2026-09-20)
- **A1.3** Document the job, plan it and schedule it to hit the deadline. Record the card in the job note: title, status, start and due dates, idea doc link, footage folder, camera file IDs. ✅ *"document it, plan it, schedule it, let's hit the deadline"* (2026-09-24)
- **A1.4** The ClickUp card dates are the real deadline. The Notion idea doc's status and deadline fields go stale (one was a month old). Do the maths against Route Rise's 5-day cap, Sunday excluded: he doesn't work Sundays. 🏢 ⚙️
- **A1.5** A due time after midnight (e.g. Sat 2:15am) means deliver the evening before, nothing after 10pm. 💡
- **A1.6** Several jobs at once: run them in card-date order (start, then due), not the order he pastes links. Confirm "next" on the board before downloading; ask for the board view if a card is missing. Download and prep only the next job; plan and schedule the others, download them only when he asks. ✅ *"Don't download the other 2 so we don't take up space yet"* (2026-09-29)
- **A1.7** If he is rendering or using Resolve, prep the folder and downloads but don't open Resolve. ✅ *"prep the folder don't use Davinci Yet, I am rendering a revision"* (2026-09-29)
- **A1.8** Ask Samuel when the script doc refuses access, before switching his open Resolve project, and when the frame rate is unclear. ⚙️ (2026-10-30)

### The job folder
- **A1.9** One folder per card: `C:\Users\repzy\Desktop\Video edits\Routerise\<card title exactly>\` with `Client raws\`, `Screen recordings\`, `Docs\`, `Screenshots\`, `B-roll\`, `Music\`, `SFX\`, `Graphics\`. Add `Conformed audio\` when the mic is conformed (A2). ✅ *"create a new folder on routerise and sort it there"* (2026-09-24)
- **A1.10** Use a straight apostrophe (') in folder names. The curly one (’) breaks the Resolve MCP transport. 🔁 (2026-10-07, 2026-10-12) ⚙️
- **A1.11** Finished camera downloads go to `Client raws\`; a second camera to `Client raws\B-cam\`. ✅ *"once it's done move it to the actual right folder"* (2026-10-30)
- **A1.12** Everything the Editor makes carries "(Editor)" in its name: folders, docs, timelines (`Docs\Visual plan v1 (Editor)`, `Visuals v1 (Editor)`). New files only; never overwrite his. ⚙️
- **A1.13** Keep the job's live state in `Docs\RUN STATE.md` (a ">>> NOW" line plus a dated log). ⚙️
- **A1.14** Client template kits: copy the master kit into the job's `Graphics\<kit> (Editor)\` and work there; kit fixes go back to the master (client overlay names the kit). ✅ (2026-10-20)
- **A1.15** Music and SFX come from the library: `Routerise\Visual Assets\Music\`, `Routerise\Visual Assets\SFX\`, `C:\Users\repzy\Downloads\sounds\Sound effects\` (D1, D2). ⚙️

### The brief and the script
- **A1.16** Save the brief offline in the job: `Docs\Idea doc and script.md` plus a Word copy (`md_to_docx.py`). Expand every toggle; open sub-pages and images too. ✅ *"we need to get that as a doc in the folder so I can access it offline"* (2026-09-24)
- **A1.17** Route Rise's Notion is not visible to the Notion connector (404). Open the page in Samuel's Chrome, where he is signed in, or its public `notion.site` copy. ✅ (2026-09-24)
- **A1.18** Read the scriptwriter's comments on the idea doc: they hold the references (e.g. which real posts to show). ✅ *"In the comments here on this notion page draft, you would see some of the refrences"* (2026-10-13)
- **A1.19** Read the client's recording script in full. It can carry an on-screen plan per section, the source of every number and production notes (client overlay). 🏢
- **A1.20** Add a "what was actually shot" note to the doc: files, screen-recording chapters, and where the footage leaves the script. ⚙️
- **A1.21** Two scripts on one card (e.g. ClickUp doc and a Drive "Script" doc): run a whole-mic Whisper while the camera file downloads, match it against every script (3-gram coverage: 168/200 vs 9/74 sentences) and cut against the one he read. ✅ *"how similar is it to the final script the client wrote for the video?"* (2026-10-06) 🔁 (3 jobs) ⚙️
- **A1.22** Cut from the footage, not the script. The presenter freestyles; whole scripted parts can be missing or replaced. Key cut sheets to the cut timeline, not the written script. ⚙️
- **A1.23** Script doc refuses access even in his Chrome: read the links from the card description, ask him for the script, and cut from the footage meanwhile. ⚙️ (2026-10-30)
- **A1.24** Google Docs in a Drive folder export directly: `docs.google.com/document/d/<id>/export?format=docx` (or `txt`). ⚙️

### Downloading footage
- **A1.25** Drive: the connector can't list a link-shared folder. List it in the in-app browser (file IDs on `[data-id]`), then download with `03-Areas/video-editing/scripts/drive_download.py <id> "<out>" --threads 10`; small files (the WAV) with plain `curl`. ⚙️
- **A1.26** Very large files (40 GB+): 4 threads at most; 10 parallel ranges tripped Drive's "Quota exceeded". Start the biggest download first; two big ones at once slow each other. ⚙️
- **A1.27** Watch long downloads. When the network drops, resume (`drive_download.py` resumes from its `.part`). When the file lands, move it into the right folder and delete your own `.part` leftovers. ✅ *"take note the download can stop due to network you just have to resume it"* (2026-10-30)
- **A1.28** "Quota exceeded" comes back as a ~2 KB HTML body: check one range's body before trusting a stall. It usually clears within 24 h (probe every 30 min), or Samuel copies the file into his own Drive. ⚙️
- **A1.29** Screen recordings from Tella: the link sits in the one-line "Screenshare" doc. Use the export API and take the 4K export (3840×1912, 30 fps). Note the chapters (the presenter's section map) and which stretches are real demo versus teleprompter. ⚙️ (details: [[03-Areas/video-editing/sops/routerise-job-setup|job setup SOP]] step 3)
- **A1.30** Download only what this episode needs. Check every camera clip belongs to this episode: one Drive drop held another episode's A-cam and B-cam. Ignore duplicate and pre-roll mic files. ⚙️ (2026-10-30)
- **A1.31** Check every download by decoding it (ffprobe, decode at several points) before use. A suspect file: MediaInfo, play the spot in VLC, try a proxy; if two decoders break at the same point, re-download. ✅ *"redownloading the file has worked."* (2026-08-11)
- **A1.32** Samuel's Chrome asks "Save as" on every download, and the file still lands in `Downloads\<guid>.tmp` at full size: copy it out. ⚙️
- **A1.33** Give Windows programs `C:/Users/...` paths, never Git Bash `/c/...` (files landed in `C:\c\...`). ⚙️
- **A1.34** Web pulls (YouTube etc.) are re-encoded to an edit-ready `.mov` before he gets them (spec in C9). ✅ *"A lot of the videos are glitching and saying media offline in Davinci"* (2026-10-09)
- **A1.35** Client B-roll on request: pick from Drive thumbnails, check 4 to 6 frames per clip, skip non-work footage, download fast and ping him when done. Leave the files unsorted and unrenamed. ✅ *"find me B-rolls that show him working ... download them for me fast, ping me when you are done"* (2026-10-02)

### Check before cutting
- **A1.36** Before cutting, write down the verified asset facts (screen-recording specs, key timestamps) and a ranked "still needed from client" list. Footage often arrives incomplete; an approved cut sheet does not mean the footage exists. 💡
- **A1.37** Check the tool on screen is the tool he names. Alex said Higgsfield on camera while all footage was Arcads, twice. Crop or blur the wrong name so the screen never contradicts the voice. 🏢 💡
- **A1.38** Confirm any unverified asset (a URL flagged in the script) before showing it. 💡

### Disk space and deleting
- **A1.39** Check free space on C: before downloads, extractions and renders. One job is about 15 GB of raws plus 35 to 40 GB of render cache. Ask him to free 30 GB+ before a heavy ProRes wave (a full C: killed one). ✅ "save space" (2026-09-29)
- **A1.40** C: is the only local disk. G: is Google Drive. ⚙️
- **A1.41** Delete draft renders only on his yes; keep finals. Clearing a job's cache is his call. ✅ (2026-10-28)
- **A1.42** Clearing the Routerise raws: keep the last 3 videos, clear the rest. ✅ *"we won't touch the last 3 videos, just clear the folder completly"* (2026-10-31)
- **A1.43** During unattended runs, never delete with the shell (it prompts him and stalls). Remove your own temp files from Python, only inside the job folder or the scratchpad. ⚙️

### Training
- **A1.44** Every method that works goes into the SOP and the scripts: the job is the Editor's training. 🔁 (2026-09-21, 2026-09-24) ✅ *"What every methods succeeds, we would add to SOP"* (2026-09-21)

## Never
- **A1.45** Never modify, move or rename downloaded client raws. Make lossless copies when a conform is needed. ✅ 🏢 (2026-09-24)
- **A1.46** Never delete anything Samuel made. ✅
- **A1.47** Never use footage from another episode, even when it sits in the same Drive drop. ⚙️
- **A1.48** Never take Tella's 1920×956 stream (too soft) or press the in-app browser's Tella Download button (it crashed the page). ⚙️
- **A1.49** Never trigger blob downloads in Samuel's Chrome: the "Save as" dialog stays in front and blocks every click in Resolve. ⚙️
- **A1.50** Never hand over raw 4K VP9 web downloads. ✅ (2026-10-09)
- **A1.51** Never put cache, proxies or footage on G:. ⚙️
- **A1.52** Never copy a client's brand kit into the Brain; read it where it lives. 💡

## Pictures
- (no picture yet: a screenshot of a correctly sorted job folder would help)

## Questions for Samuel
- **Q-A1.a** Raws clean-up (2026-10-31): "keep the last 3 videos" was said for one clean-up. → Options: (1) standing rule for every clean-up (2) one-off. My pick: (1).
- **Q-A1.b** Folder name: the SOP says "card title exactly", but the job folders carry a number ("2. I Gave Claude…", and two different jobs are both "3."). → Options: (1) copy the card title as it is, number included (2) add our own running number per client. My pick: (1), with straight apostrophes (A1.10).
- **Q-A1.c** A1.5 (deliver the evening before, nothing after 10pm) was inferred, never said by you. → Options: (1) keep (2) drop. My pick: (1).

## Sources
Replaces or draws on [[03-Areas/video-editing/sops/routerise-job-setup|Route Rise job setup]], [[03-Areas/video-editing/workflow|Workflow]], [[03-Areas/video-editing/troubleshooting|Troubleshooting]], [[03-Areas/video-editing/cut-sheets|Cut sheets]], [[03-Areas/video-editing/clients/routerise|Route Rise]], [[03-Areas/video-editing/ways-of-working|Ways of working]], [[07-Agents/video-editor/memory|Editor memory]] and the job notes.

Back to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]
