---
type: knowledge
area: video-editing
status: active
updated: 2026-09-20
source: interview
tags: [agents, automation]
---

# The video editing agent — target design

Samuel's own brief, 2026-09-20. **Not built yet — the agent has started nothing.** This note exists so the Phase 4 build has his actual intent in front of it, in his own terms.

> **"The video editing agent is my most important agent in this whole second brain."**

## The mission, and why

**Get the agent doing 60–80% of the editing work**, while Samuel fine-tunes the rest.

The reason is not convenience. It is time: he needs hours back **to start his own brand and build his own business**. Client editing currently consumes them. That makes this agent the lever for everything else in the vault.

## The pipeline he wants, step by step

### 1. Cut the video in DaVinci Resolve, from the script
The agent goes into Resolve and cuts the video based on the script Samuel gives it. **The client does not always stick to the script** — the agent has to work out what to do from the script rather than assume the video follows it.

### 2. Sectionalise
Split the cut into the video's major sections. This must be right before anything else proceeds.

### 3. Transcribe
Turn the cut video into a document showing every section, to refer to during the edit. **Uses the existing transcription skill** — possibly tweaked.

### 4. Ideate the visuals — including the intro
From the transcript, ideate the visual for **every sentence**. A storyboard, effectively. **The existing ideation skill does this** and can be tweaked.

**The intro is ideated here but edited by Samuel.** He handles the intro himself — *"the intro is one of the major places that I want to put in a lot of my creative work"* — but he wants the agent's ideation for it **before** he edits it, so he works from the idea.

### 5. Visualise the storyboard in HTML/CSS
Build the proposed visuals as actual animated HTML/CSS — the motion graphics, the screen recordings, all of it — so Samuel can see and approve the visual before it is built for real.

### 6. Convert approved visuals into Fusion comps on the timeline
Once he is happy with the HTML, find a way to turn it into Fusion compositions on the timeline, where he can work on it properly and tweak.

### 7. Standing job: DaVinci Resolve expert
The agent is **a professional in DaVinci Resolve** and helps with bugs and anything Resolve-related, continuously — not just inside this pipeline.

## Skills, one per job

The agent carries a skill per part of the work: cutting, transcription, ideation, and so on. Two already exist and get reused rather than rebuilt:
- `subtitle-transcript-formatter` — step 3
- `video-edit-pass` — the two-phase editorial pass
- Ideation — an existing skill he named; identify exactly which one at build time

## Reference material

> The agent should refer back to **the last project in the video editing project** — what was done there, and fine-tune from it.

## How this gets built

Samuel's instruction: **not in one pass, and not tonight.** A dedicated session on the video-editing agent, fine-tuning the process heavily. This note is the starting brief for that session, not the finished design.

## Open before building

- Which existing skill is "the ideation skill" — confirm by name.
- How the agent drives Resolve: the DaVinci Resolve MCP is connected, so the cut in step 1 and the comps in step 6 are scriptable. Needs a real test on a copy of a timeline.
- **Rule already on file:** duplicate the timeline before any agent touches it ([[ways-of-working]]).

Related: [[workflow]] · [[ways-of-working]] · [[fusion-recipes]] · [[cut-sheets]]. Back to [[03-Areas/video-editing/video-editing|Video editing]]
