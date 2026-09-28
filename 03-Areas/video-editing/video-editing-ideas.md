---
type: knowledge
area: video-editing
status: active
updated: 2026-09-29
source: manual
tags: []
---

# Ideas — video-editing

The idea bank for this area. Every idea is dated and carries a status: **raw** / **shortlisted** / **used** / **dropped**. Used ideas link to what came of them. Dropped ideas say why — that is the part that stops the same bad idea coming back.

| Date | Idea | Status | Outcome / why dropped |
|------|------|--------|-----------------------|
| 2026-09-29 | **Render → review → Frame.io → Slack automation.** Samuel stayed up through a 3h+ render to upload and message by hand. Feasibility checked, nothing built: Resolve runs a Deliver-page script at render end (gets job ID + status; example `8_slack_notification_by_render_job.py` in Resolve's Scripting/Examples). Flow he wants: render done → ntfy ping on phone + PC pop-up (Play / Approve & send / Hold) → on approve, upload to Route Rise's Frame.io (he's an invited collaborator; V4 API is OAuth-only, guest access unproven, forum reports 401s) → Slack message tagging the creative director. He is a **guest** in the client Slack and can't install apps, so the message is typed into the Slack desktop app (slack:// deep link + keystrokes), not sent via API. Open before building: Frame.io V4 or legacy, folder rule per video, channel + CD's Slack name, his usual delivery message, which renders trigger it. | raw | Samuel: build it later. |

Back to [[03-Areas/video-editing/video-editing|Video editing]]
