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
- The Ep 3 page is titled "Nigerian light". "My Story" is the template's name, not the Ep 3 page (correcting the entry above).

Back to [[07-Agents/content/profile|Profile]]
