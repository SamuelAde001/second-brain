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
Back to [[03-Areas/video-editing/video-editing|Video editing]]
