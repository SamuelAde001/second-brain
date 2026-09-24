---
type: agent
area: personal-brand
status: active
updated: 2026-09-22
source: manual
tags: [agent, memory]
---

# content — memory

Append-only. What this agent has learned by doing. Newest at the bottom. Facts here were verified in action, not assumed (AGENTS.md rule 6).

---

## 2026-09-22 — What the Brain held when it was built

- **Voice and script method are deep:** [[brand-context]] (pillars, audience feelings, six non-negotiables, positioning, boundaries), [[script-process]], [[script-review-checklist]], [[storytelling-structures]] (including five named techniques), and 30 raw stories in [[03-Areas/personal-brand/personal-brand-ideas|ideas]], none used yet.
- **Production is thin.** For [[03-Areas/personal-brand/series/life-of-a-video-editor|The Life of a Video Editor]] the Brain knows the time per episode (about 4h30) and where ideas come from. It doesn't know the episode structure, length, how B-roll is planned, or any view counts.
- **Numbers are sparse.** Followers: 460 IG / 550 TikTok on 2026-08-26, 671 / 673 on 2026-09-20. No post-level data. Nothing connects to Instagram or TikTok.
- **Two connectors could automate the numbers** (MCP registry, checked 2026-09-22): **Metricool** (connects his own IG and TikTok accounts; analytics, best time to post, scheduling) and **vidIQ** (research for YouTube, Instagram and TikTok; already connected to his claude.ai account, not to Claude Code). Neither is tested. Connecting either needs his yes.

## 2026-09-24 — He drafts scripts in Notion

- Samuel: *"I did it in Notion because Notion formats better and is easier to use"*, and he will connect his Notion page to the Brain later. Until then drafts arrive as screenshots. The Notion connector is installed but not yet authorised.
- His draft 1 of Ep 3 dropped the strongest stake from his own interview (lost international trial tasks). Check drafts against the outline for beats that went missing, not just for wording.

## 2026-09-24 — B-roll notes are blue

- Samuel: *"Every B-roll should differentiate itself from the script by being colored in Blue"*. In Notion, every `{b-roll}` note sits at the end of its line, wrapped in blue text (`<span color="blue">…</span>`). Script text stays default colour.
- His scripts live in Notion under Samuel Signals → My personal brand → Samuel Signals Instagram → Content Calendar. Ep 3 is the page "My Story". Pages carry a long template above `## Script`; fetch output is ~70k characters, so extract the script part with a script, don't read it whole.

## 2026-09-24 — His footage folder and how to read it

- All personal-brand footage: `C:\Users\repzy\Desktop\Video edits\My videos\Instagram Samuel Signals\` (~111 GB). B-roll lives in `B-roll archive\`, sorted by his Master Shot Library codes (`Document\HighSignals_Broll_Shot_List.xlsx`). New Osmo dumps land loose in the archive root.
- Identify clips by script: ffprobe plus 3 frames each (15/50/85 %), tiled with ffmpeg (`hstack` + `tile`) into 20-clip contact sheets, about 9 images for 164 clips. Pillow isn't installed. Colour-flat footage reads fine.
- When he's talking into his mic on camera, it's a voice-over recording (Samuel, 2026-09-24). File it under `Voice over videos`. Clips of his girlfriend go to `Girlfriend` and are never used in content or indexed.
- Moving clips can break media links in Resolve projects that use them. Warn before any move.

## 2026-09-24 — Starting a new script page in Notion

- Database: Instagram Content Calendar, data source `collection://30d8d1c1-7bb7-8030-8a7a-000bcb336370`. Story template **My Story** (id `38e8d1c1-7bb7-80ea-aa99-d6e7eed56c3b`, the default). Its script section ends the page: `## Script`, then red `## Hook / Context / Struggle / Pivot / Resolution / CTA`, each with empty blocks. Replace that tail with `update_content`; don't read the ~70k-char guide above it. Set Status `Script`, Content pillar `My stories`, Post Type `Series` for this series.
- On 2026-09-24 the database holds both a page "Nigerian light" (its text is the Ep 3 script with b-roll notes) and a page "My Story", which shares its name with the template. Check which one is Ep 3 before editing either.

## 2026-09-24 — Cutting a voice-over and B-roll in Resolve by script

- **Transcribe with Resolve itself:** `MediaPoolItem.TranscribeAudio()` (open the Media page first; the first call returned False), then `GetTranscription()` gives words with timecodes. On a multi-take voice-over the word timings are loose, and some repeats get merged into one.
- **What worked:** pick takes, render the cut to a WAV with ffmpeg (`aselect`), import it and transcribe *that*. The second transcript showed duplicate takes and dead pauses the first one hid. Three passes got the cut clean.
- **Stills are held for 5 s** on `AppendToTimeline`, whatever `endFrame` says. For photos and titles, render exact-length ProRes 4444 alpha clips with ffmpeg instead.
- **`InsertFusionTitleIntoTimeline` ripple-inserts** at the playhead on the current track and shifts every track. With the tracks locked it returns None. Undo it with `DeleteClips([item], True)`.
- `AppendToTimeline` from 29.97 source into a 23.976 timeline can come out 1 frame short. Check the length and lengthen `endFrame` until there are no gaps, or the track underneath flashes through.

## 2026-09-24 — Voice-over cuts: waveform first, then mistakes (correction from Samuel)

- Samuel: *"Your voice over cuts where bad, I told you to use the waveform to cut out the gaps, never cut with the transcription, and then after that, remove the mistakes. That is the process"*. The v1 Ep 3 cut used transcript timings and left gasps and bad cuts.
- **The process for every voice-over, his own or a client's:** follow [[03-Areas/video-editing/sops/routerise-cut-workflow|the cut workflow SOP]], steps 2-4. (1) Strip gaps from the waveform only. (2) Transcribe after that. (3) Remove mistakes and repeated takes as **whole clips**, so every cut still lands on a waveform gap. The transcript only says which clip holds what; it never sets a cut point.
- **His own VO (Osmo + Mic Mini at home):** the room noise moves between about −41 and −28 dB peak (a generator or fan), so the client setting of −38 dB strips almost nothing. Breaths and gasps sit at −35 to −20. A −22 dB peak threshold per frame works: 3-frame minimum gap, 1 frame pre head, 2 frames post tail. Short runs that never reach −12 dB are breaths or clicks and get dropped.
- He adds the B-roll himself when he says so. On 2026-09-24 he asked for the VO cut only.
- **What worked on Ep 3 v3 (2026-09-24):**
  1. Per-frame peak levels (`astats`, one window per timeline frame). Strip gaps at −22 dB. Drop short runs under −12 dB as breaths.
  2. Transcribe **each waveform clip on its own** (one WAV per clip, `TranscribeAudio` on each). A single transcript of the whole file drifts when you map words back to clips.
  3. Keep whole clips: usually the last complete take, or a take said in one clip.
  4. Check with a subtitle track on the cut timeline plus its FCP7 XML export: every subtitle should read clean, with no edits inside a line except intended joins (Samuel: *"Make use more of the subtitle track and XML timing, with the waveform parts"*).
- **Tight starts, no mouth smacks** (Samuel: *"The cuts must be tight, at the beginnings and avoid my mouth smackings"*). At 5 ms resolution, a smack is a spike of 5-15 ms with at least 30 ms of quiet (below −40 dB) before the word. Start the clip 5 ms before the first sustained sound (6 windows averaging above −28 dB), always after the last smack. End it about 60 ms after the last sustained sound, before any isolated click. Nasal starts ("N…") sit at about −38 dB: check that they stay inside.


Back to [[07-Agents/content/profile|Profile]]
