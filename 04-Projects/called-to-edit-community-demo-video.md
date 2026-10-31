---
type: project
area: called-to-edit
status: active
updated: 2026-10-31
source: manual
tags: [called-to-edit, community, discord, demo-video, onboarding]
---

# Called to Edit Community: phone demo video

Part of [[03-Areas/called-to-edit/called-to-edit|Called to Edit]] → [[04-Projects/called-to-edit-community-launch|Community launch]].

## The ask (Samuel, 2026-10-31)

*"A lot of people on the community don't know how to use Discord at all, and don't know how to navigate the community"*. He wants a one-on-one demo video with a voice-over, mostly on mobile, *"As easy as possible so it doesn't feel overwhelming"*, and it *"most look 1-1 replica of the community"*. It goes to members' DMs and WhatsApp, the welcome, and the email to everyone who joined and is joining.

Must cover: each channel; the 60-day challenge; sharing work and getting feedback from him; the bot; the weekly sessions (how to join, the chat there, raising your hand to be invited to speak); the voice channels.

## Plan (Brand manager writes, Editor builds; not Samuel's decisions until he confirms)

- **Format:** vertical 1080×1920, phone screen filling the frame, because it's watched on WhatsApp on phones. About 5 minutes, nine short chapters, each with a chapter card ("3 of 9 · The 60-Day Challenge") so nobody feels lost and anyone can skip to a part.
- **The look:** an HTML replica of the Discord mobile app (dark theme) filled with the real server: the real category and channel names and icons from `community_admin.py` `LAYOUT`/`ICONS`, the real pinned texts from [[04-Projects/called-to-edit-community-discord-texts|Discord texts]], the community logo as the server icon, Editors Bot's real avatar and commands. A demo member, **Chidi**, is the viewer (Member role, so no Team channels).
- **Taps:** a white touch dot shows every tap and swipe, and the part being talked about gets a soft highlight, so they can copy it on their own phone.
- **Built by:** a scripted HTML page recorded frame-exact with the Editor's `record_demo.py` (headless Chrome), voice laid over with ffmpeg, burned-in captions (many will watch on mute first).

## Script v1 (for Samuel's edits)

Spoken lines are in quotes. *What's on screen* is in italics.

**1 · Hello (0:00)**
*Samuel's photo, the Called to Edit logo, then a phone.*
"Hi, it's Samuel. Welcome to the Called to Edit Community. If you've never used Discord before, don't worry. In the next five minutes, I'll show you everything, on your phone, step by step. Pause the video any time and try it with me."

**2 · Getting around Discord (0:20)**
*Discord home: the server list on the left, the Called to Edit logo highlighted. Tap it. The channel list opens.*
"This is Discord. On the left are your servers. Tap the Called to Edit logo. This list is our community. Every line is a channel, a room for one thing."
*Highlight a # channel, then a speaker channel.*
"A hashtag means a chat room you type in. A speaker means a voice room you talk in."
*Tap a channel, it opens. Swipe right, back to the list.*
"Tap a channel to open it. Swipe right, or tap back, to come back to the list. That's it. That's most of Discord."

**3 · Start here (0:55)**
*Tap 🧭 start-here, scroll slowly.*
"Start with start-here. It tells you what each room is for, and the six rules. Read it once."
*Tap 📢 announcements.*
"Announcements is where I post news, call times and challenges. Only I post here, so turn its notifications on."
*Long-press announcements → Notification settings → All messages.*
*Tap 💬 general-chat, type "Hi, I'm Chidi, I edit on CapCut from Lagos", send.*
"Then go to general-chat and say hi. Your name, where you edit from, and what you edit. Tap the box at the bottom, type, and send."

**4 · The rooms (1:35)**
*Channel list scrolls; each category glows as it's named.*
"Here's the rest, in groups.
Community: wins, for your wins, small or big. Showcase, for your work.
Grow: resources for tutorials, opportunities for gigs, and help when you're stuck.
Then my three parts for getting clients. Personal brand, to get seen. Outreach, to reach clients. And skills, with a room for CapCut, DaVinci Resolve and Premiere Pro.
You don't need all of them today. Start with the challenge."

**5 · The 60-Day Challenge (2:10)**
*Tap ✅ accountability. A list of posts. Tap the pinned 📌 The 60-Day Challenge.*
"The 60-Day Challenge lives in accountability. Open the pinned post first. The workbook is attached there. One task a day."
*Back. Tap New Post. Type the title "Chidi's 60 days". Tap tags → 60-Day Challenge. Type "Day 1: …". Tap Post.*
"Now make your own post. Tap New Post. Call it your name's 60 days. Pick the tag 60-Day Challenge. Write your Day 1, and post."
*Open his post, type "Day 2: …" in the box at the bottom, send. A 🔥 appears.*
"Tomorrow, don't make a new post. Open your own post and write Day 2 inside it. Every day you post, you get a fire, and your streak grows. Every Sunday, the leaderboard goes up in wins."

**6 · Share your work, get my feedback (2:55)**
*Tap 🎞️ feedback. Tap New Post. The template from the pinned post fills in.*
"Want feedback from me? Go to feedback and tap New Post. Say what it is, who it's for, and what you want feedback on: the hook, the pacing, the message."
*Tap +, pick a video from the gallery, pick the tag Edit, Post. A reply from Samuel appears in the post.*
"Tap the plus to add your video or a screenshot, pick a tag, and post. I'll reply right inside your post. And when you post, give someone else feedback too."
*Tap 🎬 showcase.*
"Finished something you're proud of? Share it in showcase."

**7 · Editors Bot (3:35)**
*Tap 🤖 ask-editors-bot. Type "/". The command list pops up. Tap /ask. Type "How do I find my first client?". Send. Editors Bot answers.*
"Editors Bot has learned my teachings. Go to ask-editors-bot and type a slash. Tap ask, type your question, and send. It answers in seconds."
*Show /streak, /call, /subscription in the list.*
"Slash streak shows your streak. Slash call shows the next live call. Slash subscription shows when your access ends."

**8 · The weekly live call (4:05)**
*An announcement card: "Live call, Wednesday 8pm". The bot's reminder.*
"Every Wednesday at 8pm, we have a live call. The bot reminds you an hour before."
*Tap 🎙️ weekly-live → Join. Samuel shows as a speaker, Chidi in the audience.*
"When it starts, tap weekly-live and join. You'll come in as a listener, so nobody hears you. Relax."
*Tap the chat bubble. Type a question, send.*
"Got a question? Tap the chat bubble, type it, and send."
*Tap the hand. "Request to speak". Samuel invites; a pop-up: "Samuel invited you to speak" → Accept. Unmute.*
"Want to talk? Tap the hand to raise it. When I invite you, tap accept, then unmute your mic. Done talking? Tap the hand again, or leave quietly."
*Tap 📼 call-recordings.*
"Missed a call? The recording and a summary go up in call-recordings."

**9 · Voice rooms (4:45)**
*Tap ☕ lounge → Join Voice. Mute and leave buttons glow.*
"Lounge, work-gist and edit-showcase are open voice rooms. Hop in to chat with other editors, any time. Tap join. This is your mic, tap to mute. This red button leaves."

**10 · You're ready (5:05)**
*Three ticks: say hi · post Day 1 · come on Wednesday. The Called to Edit logo.*
"So: say hi in general-chat, post your Day 1 in accountability, and come on Wednesday. Stuck? Ask in help. I'll see you inside."

## Settled (Samuel, 2026-10-31)

- **Voice:** *"Mine, AI guide first"*: built with an AI guide voice, then he records the final script and his voice goes in.
- **Look:** from real screenshots of his phone (*"What if I connect my phone to my PC and it displays so you can take screenshots"*), then *"Do it for me"*: the Brand manager drove his phone.
- **PC version:** asked whether to do one *"cause of PC users"*. The Brand manager's suggestion (not yet his decision): a ~90-second PC add-on after the phone video is approved, covering only what differs.
- **Requests to Speak on #weekly-live:** *"Yes, turn it on"* (see Log).
- **Where it goes first:** #start-here. He told a member in #general-chat on 2026-10-31: *"I would be dropping a video in the start here page about how to navigate the app"*.

## Build folder

`C:\Users\repzy\Desktop\Called to Edit\Videos\Community demo video (Brand manager)\`
- `reference screenshots\`: 34 full-size screens from his Pixel 8a (Discord 351.11, Android 17): channel list, general-chat, start-here, long-press menu and notification settings, accountability + challenge post + New Post + tags, feedback + guidelines + tags, ask-editors-bot + `/` list + /ask field + an answer, weekly-live sheet + stage chat + audience view with raised hand + raised-hands list, lounge preview + voice settings + in-call view. Holds members' real names and messages: reference only, never in the video (demo members instead).
- `phone_driver.py`: the adb helper used (snap, ui, tap). Phone mirroring: scrcpy v5.0.1 in `%LOCALAPPDATA%\Programs\scrcpy\` (Samuel's yes, 2026-10-31). His USB cable dropped mid-session; wireless debugging carried on with full-size screenshots.

## How it's built (Brand manager, 2026-10-31)

All in the build folder's `build\`:
- `script.txt`: **script v2** (the spoken words; supersedes v1 below). 10 chapters, ~5:15 with the AI voice. `[[...]]` cues sit before the word they fire on. Both live calls: Sundays and Wednesdays, 8pm.
- `voice.py`: one Microsoft neural TTS clip per line (`en-NG-AbeoNeural`, free, edge-tts), word timings, cues placed on their words → `voice.wav` + `timeline.js`. `--chapters 1-3` builds part of it.
- `demo.html` + `style.css` + `screens.js` + `engine.js`: the Discord replica (Android dp sizes and colours taken from his screenshots) in a 1080×1920 Called to Edit frame (navy, Gloock, Plus Jakarta Sans), with a touch dot, zoom-ins, karaoke captions, step cards and a step pill. `demo.html?t=42` jumps to 42 s. `__check()` in a browser lists any selector the script uses that doesn't exist.
- Recorded frame-exact with the Editor's `record_demo.py` (`shot_preview.json`, 30 fps), served by `serve.py` (no cache, port 8765), voice muxed with ffmpeg (loudnorm −16 LUFS).
- **Samuel's voice:** he reads `Script to record.txt` (build folder root; generated from `script.txt`, so re-make it after any script change). The Editor cuts his mistakes first (waveform-first, [[03-Areas/video-editing/sops/routerise-cut-workflow|cut workflow]] steps 2-4). Then `python voice_samuel.py "<his cut take>"` transcribes it on the CPU with faster-whisper (`medium.en`; CUDA's cuBLAS isn't installed here, and audio is decoded by ffmpeg because faster-whisper's own loader breaks on the installed PyAV), matches each word to the script, cuts his take line by line (pauses capped at 0.6 s, chapter-card gaps added) and writes `voice.wav` + `timeline.js`. Set `duration` in `shot_full.json` to the total it prints, record, mux. Tested 2026-10-31 on the AI track: 95 % of words matched, cues within a median 0.1 s of the AI timing.

**Preview v1 (chapters 1-3, 1:28):** `renders\Community demo PREVIEW ch1-3 v1.mp4`, sent 2026-10-31; Samuel: *"Yes, build the rest"*.

**Full v1 (AI guide voice, 5:15, 1080×1920, 53 MB):** `renders\Community demo v1 (AI guide voice).mp4`, sent 2026-10-31. Checked on 26 frames: in sync; one soft spot in chapter 6 ("and post" ~1.5 s early), fixed in `script.txt` for the next take. `screens2.js` + `style2.css` hold chapters 4-10. Next: Samuel records `Script to record.txt`; no background music yet.

## What the screenshots changed in the plan

- Discord's current phone app has no bottom tabs: server icons on the left, channel list on the right, his profile bar at the bottom. Forums open with a "Post Guidelines" sheet before the New Post form; tags are picked from a sheet with a Save button.
- Stage bottom bar for the audience: music, raise hand (Request to Speak), raised-hands list, chat, leave (Disconnect Quietly). The host invites from the raised-hands list (mic icon = Invite to Speak).
- Voice room preview: mic toggle, Join Voice, chat. In call: camera, mic, screen share, soundboard, red leave.
- In LIVE, call-recordings sits above weekly-live.

## Open for Samuel

- His edits to the script.
- Which day the call is: the Brain says Wednesday 8pm WAT (2026-10-23), but Discord has a scheduled event "Sunday Live Call" for Sun 2026-11-01 at 20:00.

## Log

- 2026-10-31 (Brand manager): project opened, plan and script v1 written from the community launch note, the Discord texts and `community_admin.py`.
- 2026-10-31 (Brand manager): downloaded scrcpy (his yes), took 34 reference screenshots driving his phone over adb. Nothing posted or sent; "/" typed in #ask-editors-bot then cleared. Joined the empty ☕ lounge muted for about 20 seconds, then left and put his mic back on. Joined #weekly-live **without starting the Stage** (no notification, no @everyone) to capture the audience view; raised and dismissed his own hand; he disconnected himself.
- 2026-10-31 (Brand manager): found the "Requests to Speak" switch on #weekly-live showing "Requests Disabled". Checked the API: Member and Team already had Request to Speak from their roles, so members could raise a hand; the switch reads @everyone only. On Samuel's *"Yes, turn it on"*, @everyone's overwrite on the stage now allows Request to Speak (View still denied), live and in `community_admin.py` build so a rebuild keeps it.

## RESUME (2026-10-31, ~12:15 WAT, Editor)

- **Done:** full v1 with the AI guide voice (`renders\Community demo v1 (AI guide voice).mp4`, 5:15, 50 MB; it didn't reach his phone: the upload limit is 30 MB, so phone copies must be under 30 MB). Script v2 in `build\script.txt` (chapter 6 gallery cue moved earlier after v1).
- **Samuel's latest words (2026-10-31):** sent his voice-over `C:\Users\repzy\Downloads\Mobile Devices\Oct 31 at 12-05.m4a` (8:52, phone AAC 48 kbps; copy at `voice\samuel_raw.m4a`): *"there where a lot of mistakes and pauses, and noises, cut out the mistakes, remove the background noise, make my voice sound better and clarer and cut out the gaps as I don't want the video to have too much gaps, I didn't record the chapter numbers so keep gaps there, make it short and well understandable"*.
- **Next step (Editor):** in `voice\`: (1) silence-detect clips on the waveform; (2) faster-whisper word pass (CPU, keep disfluencies); (3) retakes = last clean complete take, decide, don't flag; drop noise/breath/uh clips; cut gaps short (~0.25-0.4 s); (4) denoise + voice polish (high-pass, noise reduction, EQ, de-ess, compression, loudnorm −16 LUFS); (5) re-transcribe the cut and check it against the script; (6) `build\voice_samuel.py <cut wav>` (adds the chapter-card gaps), set `shot_full.json` duration, record, mux; (7) phone copy under 30 MB, send, log.
- **Open:** background music (none yet); PC add-on (suggestion only); the video goes first to #start-here (he promised members).
