---
type: knowledge
area: video-editing
status: active
updated: 2026-09-25
source: manual
tags: [resolve, performance, hardware, cache]
---

# Resolve performance: why the PC crawls while Resolve caches

Samuel, 2026-09-25: *"My computer gets painfully slow nowadays when Davinci resolve is Caching."* He wants Resolve smooth and the rest of the PC usable at the same time. Everything below was measured on his PC that day by script. Nothing has been changed yet: it's a checklist for him.

## The PC (measured 2026-09-25)

| Part | What it is | Note |
|---|---|---|
| CPU | Intel i5-13400F, 10 cores / 16 threads | **"F" = no integrated graphics, so no Intel QuickSync.** All decode lands on the one NVIDIA card. |
| RAM | 32 GB DDR5-4800 (2×16) | Not the bottleneck. Resolve used 6.8 GB. |
| GPU | RTX 3060, 12 GB, PCIe 4.0 x16, driver 595.79 | **100% busy, 9.9 of 12 GB VRAM used** while caching. This is the choke point. |
| Disk | One 1 TB NVMe (SanDisk Extreme), C: only | OS, apps, client raws, render cache all on one drive. 163 GB free (82% full). |
| Other | Parsec Virtual Display Adapter installed | An extra display adapter costs VRAM. |
| Windows | High performance plan · pagefile auto (56 GB) · `TdrDelay` 10 · HAGS not set | 3 NVIDIA driver resets (`nvlddmkm`) in the last 2 days. |

## Resolve settings found (Route Rise #3 project)

- Timeline 1920×1080 at 23.976. Sources: **4K H.264 8-bit 29.97** (client raws, 352 clips on Cut v6) and **3840×1912 H.264 30 fps** (Tella, 161 clips). Frame rate mismatch: every clip gets converted to 23.976.
- Colour management: DaVinci Wide Gamut, **timeline working luminance HDR 1000**, for a Rec.709 SDR YouTube delivery.
- Render cache **Smart**, codec DNxHD SQ, **background caching starts after 1 second idle**.
- Optimized media on, DNxHR SQ at **Original** resolution. Proxy resolution **Original**. Both at original size defeat their purpose.
- Cache folder `C:\Users\repzy\Videos\CacheClip` (19.3 GB), on C:. Automatic cache deletion off.
- Preferences: CUDA, one GPU mapped, hardware decode on, Resolve memory 51%, Fusion 42%.
- Resolve runs at **Normal** priority, same as every other app.

## Why the whole PC chokes

Windows can't share one GPU fairly. Resolve's background cache fills the RTX 3060 to 100%, and the desktop, Chrome and every other app draw on that same card, so the whole PC stutters. Three settings make it worse:
1. **Caching starts after 1 second of idle.** Switching to Chrome counts as idle, so the cache starts exactly when he's doing something else.
2. **Resolve decodes 4K long-GOP H.264 for every cached frame**, and the CPU has no QuickSync to share the load.
3. **HDR 1000 working luminance plus Fusion comps** make each frame heavier than a 1080p SDR job needs.

`TdrDelay` 10 (set after the 2026-09-23 crashes, see [[03-Areas/video-editing/troubleshooting|Troubleshooting]] §7) lets a heavy Fusion frame hold the GPU up to 10 seconds. That stops the crashes, but the screen can freeze while it happens.

## The checklist, in order of impact

### In Resolve (free, today)
1. **Proxies at Half or Quarter size** for every 4K clip: Project Settings → Master Settings → Optimized Media and Render Cache → Proxy resolution Half, format DNxHR LB. Generate for the client raws and the Tella recording. Playback → Proxy Handling → Prefer Proxies. Deliver uses the originals automatically.
2. **Turn Optimized Media off** (or set it to Half). Don't run both at Original size.
3. **Background caching: raise it from 1 to 15–30 seconds**, or switch Render Cache to **User** and cache only Fusion comps and heavy clips on demand (right-click → Render Cache Fusion Output / Render Cache Color Output).
4. **Render Cache → None when working in another app**, back to Smart/User when you return. Assign a keyboard shortcut to it.
5. **Timeline working luminance: SDR 100** (or plain DaVinci YRGB) for Routerise talking-head jobs. It changes how grades look, so set it at project start, not mid-grade. His call: colour isn't the Editor's.
6. **Pre-render finished Fusion comps** (Render in Place) so they stop costing GPU every time.
7. **Turn off Resolve 21's background jobs you don't need** (transcription and audio-classification analysis, IntelliSearch). Preferences are searchable: search "background".
8. **Delete unused cache** after each job (Playback → Delete Render Cache → Unused), and turn on automatic cache deletion by age.
9. Keep the Fusion memory limit near 30–40% (it's 42%).

### In Windows (Samuel does these, as admin)
10. **Start Resolve at Below Normal priority** so the CPU serves other apps first. A shortcut targeting `cmd /c start "" /belownormal "C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"`.
11. **Defender exclusions** for `C:\Users\repzy\Videos\CacheClip`, the proxy folder and `Resolve.exe`. Every cache file is scanned as it's written.
12. **Turn Hardware-accelerated GPU scheduling on** (Settings → Display → Graphics → Default graphics settings), reboot, test. It often keeps the desktop smoother when one app saturates the GPU. Revert if Resolve gets less stable.
13. **Trim startup apps:** Steam, Discord, BlueStacks Services, Canva agent, Adobe Acrobat Synchronizer, Fathom, Parsec (unless used), Logitech Download Assistant, Proton VPN (unless needed at boot).
14. **Pause Google Drive sync** while editing if it syncs anything in the video folders.
15. **NVIDIA App:** turn off Instant Replay / overlay recording if on. Use the **Studio** driver, not Game Ready.
16. **Keep at least 20% of C: free.** An SSD slows down as it fills. It's at 18% now.

### Hardware (ranked)
17. **A second NVMe SSD (1–2 TB)** for cache, proxies and active client footage. This is the biggest upgrade for the "whole PC chokes" symptom: Resolve's disk traffic moves off the drive Windows runs from. Check the motherboard for a free M.2 slot first.
18. The GPU is the real ceiling. With proxies and sensible caching, a 3060 12 GB is enough for 1080p Routerise deliveries. Upgrade only if Fusion-heavy jobs keep freezing it.
19. 64 GB RAM only matters for very heavy Fusion. Not now.

## Side note
Client raws are 29.97, the timeline is 23.976. Resolve drops frames to convert, which can make motion judder. Confirm the Routerise delivery spec is 23.976 before the next job.

Back to [[03-Areas/video-editing/video-editing|Video editing]]
