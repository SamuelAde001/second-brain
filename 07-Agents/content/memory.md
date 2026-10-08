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

## 2026-10-04 — Building web pages for him

- He wants **conversion first, mobile first, light pages**: most of his audience is on phones and slow data. No video on a landing page; WebP at ~640px for phones.
- The **content is the selling point, not his face**: *"I need them to see the roadmap and what they would learn"*. Lead with the career outcome.
- His photo library: `C:\Users\repzy\Pictures\My pictures\Photos-1-001\` (76 JPGs). Best brand shot: `Potrait photo.jpg` (blue blazer, marble wall). `Pictures\Babe` is his girlfriend: never opened.
- ffmpeg `drawtext` fails here (fontconfig missing); make contact sheets without labels and check picks by filename. EXIF rotation means raw dimensions can look swapped.
- scroll-craft engine: `data-sc-kinetic` strips inner spans (a gold phrase loses its colour). A middle pinned act's last cue must hold (one value) or the stage slides off empty.
- The in-app browser pane only advances CSS transitions while a screenshot is being taken; half-faded blocks in `javascript_tool` reads are not a page bug.
- **Mobile first never means desktop second** (Samuel, 2026-10-04: *"some would open on their computers"*). Check every page at ~1920px too: keep content inside the page width, never a full-bleed photo with tiny copy at the far edge. He dislikes long pinned scroll sections and generic timelines; wants scannable cards with icons.

## 2026-10-04 — Publishing the landing page
- Netlify CLI is installed globally and logged in to his account. Publish with `sh deploy.sh "msg"` in `Desktop\landing-page\` (site id `abf350bc-…`, `--dir site`). He drags whole folders by mistake; never ask him to drag again.
- Apps Script editor: set code with `monaco.editor.getModels()[0].setValue(...)` via javascript, using `String.raw` so regex backslashes survive. The OAuth "Allow" stays his click.
- `curl -L -X POST` to an Apps Script `/exec` returns 411 after the 302; the row is still written. Check the Sheet, not curl's reply.
- Never put a honeypot field named like a real field (`company`) in his forms: Android autofill fills it and the form fails silently on phones.
- He wants the Sheet readable at a glance: one list plus an overview, brand colours, no raw tabs. Phone numbers must stay text (leading 0).
- Apps Script editor via Chrome: the Run function picker would not change by click; making `setup()` call the job once, then reverting, worked. Clicking at fixed coordinates in the editor can hit links in dialogs; click the editor by its ref.

## 2026-10-06 — The webinar payment funnel

- **Never trust the redirect alone.** Bank-transfer payers leave for their bank app and often never come back to `welcome.html`. Flutterwave's webhook is the truth; the redirect is a bonus.
- **Flutterwave payment links prefill** with `?email=&firstname=&lastname=` (checked 2026-10-06; `first_name` does not work). The checkout shows his business name, contentinfluence.
- Flutterwave emails him "New successful transaction" (from noreply@flutterwavego.com): name, method, Transaction ID (`Rave-Pages…`, the same as the redirect's `tx_ref`). No customer email in it. **Settlement emails carry his bank account number: never copy them into the Brain.**
- **Apps Script web apps run the deployed version, not the saved code.** After any change: run `setup` in the editor (permissions), then Deploy → Manage deployments → New version. A `try {} catch {}` that swallows errors hid the calendar failure for a day: write failures into a cell instead.
- **Calendar guests:** `CalendarApp` `addGuest` sends no email. The Calendar API `patch` with `sendUpdates: "all"` can notify every guest each time one is added, so with 100 payers, don't use it. Send our own confirmation email instead.
- **Test page changes without touching his live Sheet:** serve a copy of `site/` with `config.sheet` pointed at a local logger (the 2026-10-06 `serve.py` pattern), and use `?test=1` on the live page.
- The 400/411 after a POST to the Apps Script `/exec` is the redirect hop. The script already ran on the 302.
- **Nobody is added to the WhatsApp group by the system.** `welcome.html` opens the invite when a payer returns; bank-transfer payers usually don't, so they rely on the confirmation email. Samuel reads "not added" as broken: check the Sheet row and Sent mail first, then send the row's Follow up link.
- **Flutterwave emails "Unsuccessful Webhook Delivery" for any hook that gets a 302**, which Apps Script always gives, even when the hook landed. Check the Payments tab before believing it. Fix: the `/flw` Netlify relay answers 200 (live 2026-10-06).
- **Don't put payers' names or emails in Brain notes**: the Brain is pushed to GitHub. Say "4th payer" and point to the Sheet.

## 2026-10-07 — Making flyers and cutouts
- **Pinterest search needs a login**: logged out it shows a wall. Use his Chrome (he's logged in there); the in-app browser can't search it.
- **Cutouts: `rembg` is installed** (Python 3.14, `isnet-general-use` model in `%USERPROFILE%\.rembg\models\`). `remove(img, session=new_session("isnet-general-use"), post_process_mask=True)` gave a clean cut of his portrait, hair included. Runs locally; his photos never leave the PC.
- **Export designs to PNG with headless Chrome**: `chrome.exe --headless=new --user-data-dir=<scratchpad> --window-size=1080,1350 --force-device-scale-factor=2 --virtual-time-budget=10000 --screenshot=<out.png> file:///…?export`. Google Fonts load fine.
- Pinterest's best-performing webinar flyers are busy templates; the ones that stand out are editorial magazine covers (big serif masthead, head over it, little text). That's the Called to Edit flyer direction.

## 2026-10-07 — His taste in flyers (v1 rejected)
- Samuel on v1 (Playfair serif masthead, Montserrat, a Resolve-timeline details strip): *"looks good but could be better"*, *"not a fan of the fonts used"*, *"I don't like the timeline looking details"*, *"We need better heirachy"*. Clever editor motifs don't win him; clear hierarchy does.
- His Pinterest picks (sheet in `landing-page\flyer\inspiration\`): giant heavy condensed title, person cut out on the right overlapping it, clean sans text, details in a divided labelled row, a badge for urgency, navy premium mood. He wants the main event details **and 3 benefits** on a flyer.
- Show him options as one numbered contact-sheet image: the preview pane blocks hot-linked Pinterest images.
- 2026-10-07: his Instagram handle on designs is **@samuelsignals01** (Samuel's correction to v3). He liked v2's direction; disliked a plain pill "Get your seat" button.
- 2026-10-07: on 9:16 designs he wants the frame **filled top to bottom**; no empty bands for story safe zones. Backgrounds stay in his navy (a cream version was rejected: *"stick to my normal color for BG"*).
- 2026-10-07: **cutouts need soft edges**: use rembg with `alpha_matting=True, alpha_matting_foreground_threshold=235, alpha_matting_background_threshold=20, alpha_matting_erode_size=12` (16 s on 2240×3982). No 1px outline on the subject; he called it "too harsh". Flyers stay **4:5** unless he asks (he dropped 9:16 the same day).

## 2026-10-07 — Apps Script field names
- **Never send a field named `sid` to an Apps Script web app.** Google's front end returns 400 and the script never runs; the browser shows nothing wrong. It killed every landing-page sign-up from 6 Oct ~11:41 for a day. After any change to what the page sends, check that a `?test=1` view lands in the Tests tab before calling it done.
- `deploy.sh` runs `check-sheet.js` before publishing: it posts the page's real fields to the Sheet as a test and blocks the publish unless it gets 302. Don't remove it.
- Claude Code's auto-mode check blocks publishing his site and editing the live Sheet script unless Samuel says so in his own words for that change ("Deploy the fix" covered the page only). Ask for each live change by name.
- **Apps Script deploy dialog:** after picking "New version", the version listbox can stay over the Description field; a click there picks an old version (it deployed Version 6 by mistake on 2026-10-07). Skip the description, check the Version box reads "New version", then Deploy, then confirm the result says the new version number.
- **Flutterwave Customers** (dashboard → Customers) lists people who opened checkout even without a transaction: the place to find lost sign-ups. Transactions list URL takes `?from=YYYY-MM-DD 00:00:00&to=…` and no status to show every status.

## 2026-10-08 — Notion content calendar
- His content database in Notion is *Instagram Content Calendar* (Samuel Signals → My personal brand → Samuel Signals Instagram → Content Calendar), data source `collection://30d8d1c1-7bb7-8030-8a7a-000bcb336370`. Status is the only state field: Idea · Script · Recording · Editing · Done · Dropped. "Content pillar" doubles as the series (My stories, Called to create, Storytelling).
- `ALTER COLUMN … SET SELECT(...)` keeps existing values when option names match: count rows per option before and after anyway.
- In `update-view`, `CLEAR FILTER` does not remove quick filters that have a preset value; those still filter the view. Use `CLEAR QUICK FILTER` too, then read the returned `simpleFilters`.
