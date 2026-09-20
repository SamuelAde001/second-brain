---
type: knowledge
area: personal-brand
status: active
updated: 2026-09-20
source: memory-export
tags: [gear, production, luts]
---

# Recording setup and post workflow

From the Claude memory export for the Content Creation project, 2026-09-06. The settings behind his own content — the cinematic, narrated, shot-in-his-room format described in [[brand-context]]. **Read before shooting or grading.**

## Camera

**DJI Osmo Pocket 4** (standard, not the 4P):
- Fixed 20mm-equivalent f/2.0 lens. Single fixed lens only.
- **D-Log** colour profile. **ISO floor 400** — there is no ISO 100 and no D-Log 2 on this body.

**B-roll settings, locked:**

| Setting | Value |
|---------|-------|
| Resolution / rate | 4K, 25fps |
| Profile | D-Log |
| Shutter | 1/50s |
| ISO | 400 native, max ~1600 in the dark |
| White balance | Manual ~5400K, matched to the softbox |
| Texture | −1 |
| Noise reduction | 0 |
| Anti-flicker | 50Hz |

## Microphone

**DJI Mic Mini**, paired **directly to the Pocket 4** via the camera's own touchscreen: Control Center → Wireless Microphone. **The Mimo app does not connect to the Mic Mini** — a dead end worth not rediscovering.

- Mic on the chest, **6–8 inches from the mouth**.
- Target peaks **−12dB to −6dB**.

## Voiceover workflow

Record video on the Pocket 4 with the Mic Mini live, then **extract the audio in Resolve**. No separate recorder.

## Fairlight chain

High-pass ~80–100Hz → noise reduction → light compression → **loudness normalise to ~−16 LUFS** for social.

## Colour and LUTs

- D-Log LUT workflow in Resolve. **PowerGrade** for reusable node trees with live exposure adjustment. **33-point `.cube`** export for Mimo compatibility.
- **CST IN/OUT nodes already bake the D-Log conversion — do not also enable Mimo's "Color Recovery"**, or the footage double-converts.
- **"Generate LUT" in Resolve is reached by right-clicking the clip thumbnail in the timeline strip**, not from inside the node editor.
- **One LUT across an entire series** builds a recognisable visual brand. Resist switching.
- **Contact shadow is non-negotiable** for composite shots to look grounded.

**LUT sources** — free: The Looks Lab, LumaKit Studio. Paid, Pocket 4 / Mimo compatible: The Film Alliance, Editors Keys.

## Planning tools

Excel workbooks built with `openpyxl` for shoot lists, archive trackers and formula-driven checklists.

Related: [[brand-context]] · [[03-Areas/video-editing/toolchain|Toolchain]] · [[03-Areas/video-editing/troubleshooting|Troubleshooting]]. Back to [[03-Areas/personal-brand/_index|Personal brand]]
