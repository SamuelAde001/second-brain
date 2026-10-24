---
type: knowledge
area: finances
status: active
updated: 2026-10-24
source: manual
tags: [claude, subscription, max-20x, usage-limits]
---

# Claude Max 20x: what the weekly limit really buys

Back to [[03-Areas/finances/finances|Finances]]. Feeds the 20x keep-or-drop call due 2026-11-05 ([[03-Areas/finances/plans/plan-2026-10|October plan]]).

Researched by the Money man, 2026-10-24, because Samuel asked: if one video takes 70-90 % of his current (5x) weekly usage, how many videos does 20x really give per week?

## What Anthropic says

- **"20x" is the 5-hour window only.** Max 5x = 5x Pro per session, Max 20x = 20x Pro per session, so a 20x session is 4x a 5x session.
- **The weekly limit size is not published** for either tier. The help page lists weekly limits as "Yes" for both, with no multiplier.
- Fable may use up to 50 % of the weekly limit on Max (inside the same pool, not extra). Irrelevant while the agents run on Opus 5.5.
- Claude Code weekly limits: +50 % promotion 2026-05-13 to 2026-09-13, then settled at 25 % above the old baseline from 2026-09-14.

## What people measured (20x week ÷ 5x week)

| Source | Ratio | Strength |
|---|---|---|
| GitHub issue anthropics/claude-code#99330, 2026-10-03 (one user, transcripts priced at API rates, Windows desktop app) | **~1.6x** (2x at most); session ~3.2x | After the 2026-09-14 change. One person |
| Anthropic's own 2025 hour estimates (Sonnet 140-280 h vs 240-480 h) | ~1.7x | Old, withdrawn |
| Growthcab's advice | plan on **~2x** | Opinion |
| Classmethod, August 2026 (3 accounts) | ~3.5x (3.1-3.9) | During the +50 % promotion, before the cut |
| Wokey, week of 2026-10-12 (17 Max 20x accounts) | 20x week ≈ USD 1,643 at API prices ≈ 9.7x Pro | No 5x figure yet |

No source shows 4x. The most recent measurement says ~1.6x.

## Videos per week on 20x

One video = 0.7-0.9 of a 5x week (Samuel's figure). Videos per 20x week = ratio ÷ 0.7-0.9:

| Ratio | Videos per week | Per month (~4.3 weeks) |
|---|---|---|
| 1.6x (latest measurement) | 1.8-2.3 → **2** | ~8-10 |
| 2x (safe planning number) | 2.2-2.9 → **2, sometimes 3** | ~10-12 |
| 3.5x (best case) | 3.9-5 → **4** | ~17-21 |
| 4x (if weekly matched the session) | 4.4-5.7 | — |

On 5x the same arithmetic gives 1.1-1.4 videos per week, ~5-6 a month, before any webinar, community or finance work.

**Plan on 2 videos per week.** That is the honest number until his own card proves more. Those are whole-week figures: anything else done with Claude that week comes out of the same pool.

## What 20x is really good for

- **Speed, not distance.** The 5-hour window is 4x bigger, so parallel helper agents stop hitting the 5-hour wall. A 5x week was about 7-8 full 5-hour windows (Brain: one window ≈ 13 weekly points); the GitHub measurement puts a 20x week at only ~3.6 full windows. On 20x the weekly limit is what stops you, and you can burn the whole week in under a day of full-speed running.
- Worth it in a month with more than ~5 videos, or deadlines bunched into one week. Not worth it in a month with 4 or fewer videos (already the rule, finance log 2026-10-23).

## How to get his real number

The weekly bar was **75 %** on 2026-10-24 ~15:00 WAT (resets Wed 2026-10-28 23:00 WAT), on 5x. Read the usage card right before and right after the upgrade goes through: 75 ÷ the new percentage = his real ratio (75 → ~19 % means 4x, → ~38 % means 2x, → ~47 % means 1.6x). If the bar doesn't move, check again after the first reset, when one video's cost on the new bar answers it directly. Write the reading here.

## Sources

- Anthropic help: About Claude's Max plan usage (support.claude.com, article 11014257)
- github.com/anthropics/claude-code/issues/99330
- growthcab.com/claude-max-usage-limits
- claudelimit.com/claude-max-limits
- choosely.ai/ai-radar/claude-max-limits-5x-20x-claude-code
- wokey.ai/claude-usage-limits
