---
type: sop
area: called-to-edit
status: active
updated: 2026-10-28
source: manual
tags: [automation, community, discord, obs, recordings, drive]
---

# Meeting recorder (automation)

Samuel, 2026-10-28: *"I need to be recording meetings in the discord in video format … every main meeting is recorded and saved to drive and shared on the announcement"*; *"I don't want to have to be remembering to record everytime"*; *"I don't want other OBS Sessions to all save to google drive"*. Built the same day by the Brand manager.

## What it does

1. `00-System/scripts/meeting_recorder.py run` starts at his Windows logon (shortcut in the Startup folder, no window) and checks Discord every 15 s.
2. **A main call is live** when the 🎙️ weekly-live stage is open, or a Discord scheduled event (stage or voice) has been started. Live for 30 s, it opens OBS (or uses the open one) on the **Called to Edit Meeting** profile and scene collection, and records. It keeps the PC awake.
3. If Samuel isn't in the call from Discord on the PC 2 minutes in, the bot DMs him. If recording can't start, the bot DMs him what to do by hand.
4. **The call ends** when the stage and the event are closed for 1 minute (safety stop at 4 hours). It stops recording and switches OBS back to the profile and collection it was on before.
5. Recordings under 10 minutes are kept on the PC, not posted, and he gets a DM. Longer ones are copied to Drive as `YYYY-MM-DD <event name>.mp4`. The script reads the file's ID from Drive for desktop and checks that the link opens without a login. Each call gets a line in `06-Logs/automation/meeting-recorder.md`.
6. **The same night, into the teachings archive** (added 2026-10-28, below). While Drive uploads, `call_archive.py` transcribes the call and files the great knowledge into the archive. Then the bot posts the link, the topic and the summary in **📼 call-recordings**, and the summary in **#general-chat**. It no longer posts in #announcements: Samuel asked for a recordings channel instead.
7. **The local copy is deleted** once Drive has the whole file (cloud ID plus matching size) and the transcript is written. Samuel, 2026-10-28: *"every recording that has been uploaded, should be deleted from my computer to save space, cause I don't have space"*. The transcript is kept, since it's tiny.

## Same night: transcript, archive, summary (added 2026-10-28)

Samuel, 2026-10-28: *"I want to be able to get all my meetings on discord transcribed, filtered for what is great knowledge and saved in my teaching archives so that it can be used as content, qoutes, courasoels, by the editing bot etc"*; *"I want it the same night"*; *"the bot would send a summary of the nights session to the general group chat … we can have a channel that is for the recordings links, the topic of that session and a summary"*.

`00-System/scripts/call_archive.py`, started by the recorder:

1. **Transcribe.** faster-whisper large-v3-turbo on the RTX 3060, about 8 s for a 6-minute call. Track 3 (Main Mic alone) and track 4 (Discord alone) are transcribed separately, so each line says `Samuel` or `Member`. Older 2-track recordings come out as `Call`. Output: `C:\Users\repzy\Videos\Called to Edit Meetings\transcripts\<recording>.txt`.
2. **File.** `claude -p` (Opus, on the Max plan; the script strips any API key from its environment) runs the Brand manager on [[00-System/scripts/call_archive_prompt|the call prompt]]:
   - new teachings go into the topic notes as `### Call YYYY-MM-DD: …`, with quote times
   - a call note goes in `05-Knowledge/teachings/calls/` (quotes, clips for the Editor, carousel and post ideas, questions)
   - the summary JSON is written for Discord

   His words only, and no member names.
3. **Commit and push** only `05-Knowledge/teachings`, `01-Inbox` and the recorder log: fetch, merge `origin/main`, push, never force. If the merge conflicts, it aborts and leaves the commit local.
4. **Bot.** If anything was filed: `deploy.sh --prod` in the site folder, which rebuilds Editors Bot's knowledge from the archive.
5. **Fallback.** If Claude can't run (signed out, limits hit), Gemini (read-only, `ask_gemini.py`) writes the members' summary so the posts still go out. An `01-Inbox/call-to-file-….md` note leaves the archive filing for the next session, and Samuel gets a DM if there is no summary at all.

**Posts:** 📼 call-recordings (read-only, in LIVE) gets an embed with the topic, date, length, summary, key takeaways, questions answered and the Drive link. #general-chat gets "Missed …? Here's what we covered", the summary, and a link to that post.

**Main Mic, always** (Samuel, 2026-10-28: *"My main mic is always the one to be recorded for me"*): the preset's mic is pinned by device ID to Main Mic (High Definition Audio Device), taken from his Course rec preset, not to the Windows default.

**Needs Samuel once:** the command-line Claude Code on the PC isn't signed in (*"Not logged in · Please run /login"*), and the Brain folder isn't trusted there yet. Until he opens a terminal, runs `claude` in the Brain folder, accepts the trust prompt and signs in with /login on his Max account, step 2 falls back to Gemini (summary only; archive filing waits for the next session).

## The OBS meeting preset

- **Profile "Called to Edit Meeting":** a copy of his 1080p profile. 1920×1080, 30 fps, NVENC H.264 at CQP 23 (roughly 1–2 GB an hour), hybrid MP4, so a crash still leaves a usable file. It records to `C:\Users\repzy\Videos\Called to Edit Meetings\` on the PC. None of his other profiles points at Drive.
- **Scene collection "Called to Edit Meeting":** two scenes with the same sound.
  - **Meeting**: the Discord window, the whole app fitted to the frame, cursor hidden, captured even when other windows cover it.
  - **Screen**: his whole monitor. While he screen-shares, the watcher checks every 5 s (Discord's `self_stream`) and switches to it, so Canva, Chrome and tab changes are all recorded. When he stops sharing, it switches back to Meeting (Samuel, 2026-10-28: *"If I am using canva as a screen white board or showing them other tools on chrome by screen shairing … would it affect the recording?"*). He shares his **whole screen**, so the recording matches what members see.
  - **Sound:** track 1 (what Drive plays) is everything he hears plus his mic. Track 2 is Discord's sound only plus his mic, as a backup. Since 2026-10-28, track 3 is Main Mic alone and track 4 is Discord alone, for the transcript.
- **Camera:** OBS doesn't open the Osmo. Discord shows his camera, and if OBS opened it as well, Discord would lose it. The recording is what members see in the Discord window: speakers, camera tiles, screen shares.
- `python 00-System/scripts/meeting_recorder.py setup-obs` rebuilds the preset (OBS closed). It also turned on OBS WebSocket (port 4455, password kept by OBS; the script reads it, and nobody else sees it).

His older presets, as found 2026-10-28: profiles **1080p 25 fps** and **4k 30fps** (last used: 4k + *Course rec*). Scene collections: **Course rec** (his course and tutorial recordings: Resolve, Canva, CapCut, Chrome or full screen, with the Osmo facecam and Main Mic), **Video editing fullscreen record** (screen-only scenes with no audio sources), **Untitled** (empty). None of them fits a Discord call, so the meeting preset is new and leaves them untouched.

## What has to be true on the day

- PC on, Drive for desktop running, and Discord open **on the PC** in the stage, showing the stage view. Window capture works behind other windows but not when Discord is minimised.
- Start main calls as **scheduled events** (Start event) or by opening the weekly-live stage. The event's name becomes the recording's title.
- The Drive folder `My Drive\Called to Edit\Community Call Recordings` must be shared as *Anyone with the link → Viewer*, once. Until it is, the bot DMs him instead of posting.

- **Wi-Fi drops (found 2026-10-28):** the PC's USB Wi-Fi dongle (Realtek 8812CU on the 5 GHz extender "Starlink-Ade_5GEXT") dropped 45 times in 7 days, 16 of them on 2026-10-28. 42 of the 45 say "disconnected by the driver". Samuel thinks it happens when Discord uses his speaker; not confirmed. For calls, an Ethernet cable into the PC's own network port avoids it.

## By hand

- `python 00-System/scripts/meeting_recorder.py status`: is a call live, is OBS recording, the Drive folder link.
- `… test 20`: records 20 s on the meeting preset and reports the video and audio levels.
- `… publish "<file>" "<title>"`: posts a recording made some other way.
- The watcher's own log is `%LOCALAPPDATA%\cte-meeting-recorder\recorder.log`.

## Tested 2026-10-28

- The OBS switch, recording and restore worked: 1080p30 H.264 with two AAC tracks, and the Discord window captured cleanly.
- The Drive copy and the file ID lookup worked. The public-link check correctly said "not shared yet".
- Discord lookups (events, stage, his voice state) worked.
- **Live test with Samuel, 2026-10-28, 13:19–13:26 (stage "Test session"):** recording started 30 s after the stage opened. It switched to Screen when he shared, captured Canva, and switched back to Meeting. It stopped 1 minute after the stage ended, OBS went back to 4k / Course rec, and the bot DMed him that the 6-minute recording was too short to post. His mic was clear on both tracks (peak −7 dB).
- His internet dropped for about 2 minutes mid-test. The watcher kept recording and didn't stop by mistake: Discord errors don't count as the call ending. The scene can't follow his share while the internet is down.

Back to [[03-Areas/called-to-edit/called-to-edit|Called to Edit]] · [[00-System/systems-register|systems register]]
