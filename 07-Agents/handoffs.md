---
type: agent
area: system
status: active
updated: 2026-09-21
source: manual
tags: [agents, handoffs]
---

# Handoffs

Cross-domain requests between agents. One row each: **date · from · to · request · status · link to result.** Subagents do not message each other directly — a request goes through the orchestrator and is recorded here.

| Date | From | To | Request | Status | Result |
|------|------|----|---------|--------|--------|
| 2026-09-22 | finance | video-editor | Keep one row per delivered video (name, end client, date, rate, batch) so finance knows a month's income before invoice day. Samuel's instruction | **done**: backfilled May–Sep 2026 (17 rows, 15 unnamed); standing job from now | [[03-Areas/video-editing/delivered-projects\|delivered projects]] |
| 2026-09-29 | personal-life | video-editor | AI B2B Resolve setup + sync moves from Sat 7:00am to Fri 10-02 night, after Apollo is delivered, run overnight (Samuel: *"I think It can"*). Saturday has 7:00–9:00am for the cut before a wedding | open | [[04-Projects/routerise-ai-b2b-marketing\|AI B2B project]] |
| 2026-10-04 | finance | content | Samuel cut the Brand strategist's NGN 50,000 from the October budget (*"I would also cut Brand strategist out"*). Ask him whether the hire (2026-09-29 decision) is cancelled or only postponed, and update [[03-Areas/personal-brand/personal-brand-decisions|the decision]] | **done**: cancelled completely (Samuel, 2026-10-04: *"Brand manager is canceled completly, I would work on my brand with Claude instead"*) | [[03-Areas/finances/plans/plan-2026-10|October plan]] |
| 2026-10-30 | video-editor | finance | Put Gamma video 3. Claude + Gamma App MCP Will Make You Rich (USD 175) on the **October 2026** invoice even if it is delivered after 10-31. Samuel: *"even though I may not finish it before 31st, it is allowed for me to add it to my invoice"*. October total becomes USD 1,841.65 (5 × 333.33 + 175) | **done** 2026-10-30: on invoice #15 (70%, USD 1,289.16). Later the same day Route Rise rejected it (video not done); #16 replaced it without the Gamma video. Then Route Rise accepted #15 after all: #16 void, Gamma billed on #15 | [[04-Projects/routerise-gamma-claude-mcp-rich\|Gamma job]] |

Back to [[07-Agents/roster|Roster]] · Constitution: [[AGENTS]] §7.
