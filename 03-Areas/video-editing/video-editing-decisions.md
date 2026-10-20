---
type: decision
area: video-editing
status: active
updated: 2026-09-20
source: manual
tags: []
---

# Decisions — video-editing

Append-only. Date, decision, why, alternatives rejected, who decided.

## 2026-09-25 — Revert the GPU timeout (TdrDelay) to the Windows default

- **Decision:** remove `TdrDelay` and `TdrDdiDelay` (both 10) from `HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers`, back to the Windows default of 2 s. Samuel: *"This all started when I changed that setting in the powershell, I want to return it to normal"*.
- **Why:** he links the slowdown during caching to the change.
- **Editor's objection (once):** the raised timeout was the fix for the 2026-09-23 crashes during render caching ([[03-Areas/video-editing/troubleshooting|Troubleshooting]] §7). At 2 s, heavy Fusion frames may crash Resolve again. If they do, cache heavy comps one at a time, or Render In Place.
- **Who:** Samuel. He runs the change as admin; agents don't change system settings.
- **2026-09-29 — No more editing clients, and no more Route Rise hours. 5 videos a month only through AI speed.** Samuel: *"I don't want more Route rise videos, it burns me out"* · *"NOPE, I don't want any more Video editing clients, It affects me mentally"* · *"I can try to speed up my editing efficiency with AI to get me to 5 videos per month"*. The target is 5 Route Rise videos in a month without more hours than 4 take now; the watch line is no day over 12h logged focus ([[02-Me/patterns|P2]]). A second payer is not to be raised again. The freed hours go to the [[04-Projects/called-to-edit-webinar-and-academy|webinar and live class]]. Rejected: more Route Rise volume by working longer, a second USD payer. **Who:** Samuel.

Back to [[03-Areas/video-editing/video-editing|Video editing]]

## 2026-10-13 — Video jobs run start to finish unattended, reviewed in versions

- **Decision:** the Editor runs a whole job in one unattended session (overnight), with no approval gates between steps, and Samuel reviews finished versions. Samuel: *"I want to do it all at once and have reviews in versions"*.
- **Why:** he doesn't want to sit at the PC through every step.
- **Editor's objection (once):** dropping the plan and sample gates means a wrong visual direction is found only in the morning, after the whole build. B2B *Visuals v1* was rejected whole that way. The mitigation is self-review against the edit grammar and his three finals before the version is called done.
- **Who:** Samuel.

## 2026-10-20 — Alex's videos follow Frontal brand kit v2.3.1

- **Decision:** from 2026-10-20 every visual in Alex's videos follows Frontal's brand kit v2.3.1 (Season Serif / Inter / JetBrains Mono, Dark + white + Blue-300, square shapes, quiet motion, no orange). It replaces the July orange/Geist look and the "accent changes per video" rule. Samuel: *"my client Alex just sent in the new brand guidlines of his company and brand, and they are a must follow"*, *"we just need to make sure his videos now follow the new brand guidelines including all the fonts, colors and everything there"*.
- **Why:** the client's brand changed; the kit says *"no orange anywhere from now on"*.
- **What it touches:** colours, fonts, shapes, effects and the motion style of every construct. The edit method, pacing and visual grammar stay. Rules: [[03-Areas/video-editing/clients/frontal-brand-v2|Frontal brand v2.3.1]]. Rollout and open questions: [[04-Projects/frontal-rebrand-video-kit|Frontal rebrand of the video kit]].
- **Who:** Samuel.
