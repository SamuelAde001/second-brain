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
