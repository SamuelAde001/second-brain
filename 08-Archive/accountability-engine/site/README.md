# Samuelsignals OS

The read surface for the engine. Everything, in one glance.

## The one rule

**`context/*.md` is the source of truth. This site is derived from it.**

Nothing under `site/data/` is ever hand-written, the same way `scorecard.html` is
never hand-written. If a number on the site is wrong, **the file is wrong** — fix
`context/`, then rebuild.

That is not a stylistic preference. It is what keeps the record honest: the days
live in committed markdown, so git's append-only history covers them, and a 40%
day cannot be quietly softened by editing a dashboard.

## Rebuild it

```bash
python tools/site/build.py
```

Stdlib only. No npm, no lockfile, no CDN, nothing to rot. The reckoning and the
morning brief both run it automatically.

## Look at it

Three ways, in increasing order of effort:

1. **Double-click `site/index.html`.** Works offline. The data ships as a plain
   script (`data/os.js`) precisely so `file://` works — `fetch()` on a local JSON
   file is blocked by CORS, and ES modules are too.
2. **Serve it** — `python -m http.server 8811 --directory site`
3. **Host it** — push to `main` and GitHub Actions publishes it to GitHub Pages.
   Enable it once: repo → Settings → Pages → Source: **GitHub Actions**.

## What is where

```
site/
  index.html            the dashboard
  pages/*.html          one page per section of his life
  assets/css/app.css    the design system
  assets/js/charts.js   hand-rolled SVG charts — no library
  assets/js/app.js      shared runtime + a small markdown renderer
  assets/js/pages/*.js  one script per page
  data/os.json          the whole state, generated
  data/os.js            the same, as a script tag (for file://)
```

## Where the data comes from

| Source | What it gives |
|---|---|
| `context/ledger.md` | the daily rows — focus, habit counts, bed times, verdicts |
| `context/ledger-notes/` | the narrative behind each day |
| `context/money-ledger.md` | every naira in and out |
| `context/habits.md` | habit names and cadences |
| `context/patterns.md` | the documented failure modes |
| `context/site.json` | goals, pots and targets — the numbers that only live in prose |
| `tools/sheets/plan.json` | every budget line item |
| `context/*.md` (raw) | rendered directly on the section pages, so the prose IS the file |

`context/site.json` is deliberately small. **If a number can be derived, it is
derived in `build.py`** — a number typed in two places is a number that will
eventually disagree with itself.

## The behaviour score

Out of 100, computed in `build.py` so the site and any other consumer agree.

| Component | Weight | Scoring |
|---|---|---|
| Verdict | 40 | SHIPPED 40 · PARTIAL 20 · MISSED 0 |
| Focus coverage | 20 | `min(logged ÷ committed, 1.0) × 20`, **capped at 10 if logged > 12h** |
| Habits | 20 | `hit ÷ set × 20` |
| Sleep | 20 | bed ≤10:30pm → 20 · ≤11:30pm → 10 · later → 0 |
| Penalty | −15 | no video live by Wednesday 7:00pm |
| Penalty | −15 | a planned savings transfer that did not move |

**The focus cap is the point.** Uncapped, 25 August scores 180% on focus and the
system hands its highest mark to the 19-hour day `body.md` calls *"an invoice."*

**Missing data rescales** rather than scoring zero — a day with no sleep figure is
not a day he slept badly, it is a day nobody asked.

## Charts

All hand-rolled SVG in `assets/js/charts.js`: line, bar, stacked bar, horizontal
bars, progress arc, sparkline, habit heatmap, lesson grid, streak strip, and a
bed-time-against-the-floor plot built specifically for this record.

Written rather than imported for three reasons: it cannot break because someone
else's CDN went down, every chart matches the design system exactly instead of
approximately, and the charts that matter here are odd shapes a generic library
fights you on.
