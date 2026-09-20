# Running the PA from the phone

The engine lives in a private GitHub repo. That is what makes it portable —
every check-in, every ledger row and every memory line is in the repo, so a
session on the phone and a session on the desktop are looking at the same state.

## Rule for every remote session

**Anything written to `context/` must be committed and pushed before the session
ends, or it never happened.**

```bash
git add -A && git commit -m "<check-in>: <date>" && git push
```

Desktop sessions: `git pull` before any check-in. If you skip the pull you will
overwrite what the phone wrote.

## The channels

**1. Scheduled routines — DELETED 2026-09-15**

Samuel deleted the brief, midday, reckoning and weekly-review routines: *"they where
constantly bugging me."* Nothing fires on its own any more. He opens a session
himself — the 9:00pm planning session and the Sunday week plan (see CLAUDE.md, Cost
discipline). The sections below about cloud sessions still apply to any session he
opens from the phone.

## Repo

`https://github.com/SamuelAde001/engine` (private). Cloud runs clone it to
`/home/user/engine`. Push from the cloud is verified working (2026-08-23).

**2. Claude Code on the phone — Samuel reaches in**

claude.ai/code in the phone browser, open this repo, then:

- `/brief` — morning brief
- `/midday` — 3pm checkpoint
- `/reckon` — evening reckoning
- `/plan-week` — lay out the week
- `/capture` — add, change or drop tasks

CLAUDE.md and everything in `context/` load automatically, so the rules hold
on the phone exactly as they do on the desktop.

## What does not change on the phone

- Tasks get ticked **only** at the evening reckoning, and only what Samuel
  confirms out loud.
- Due dates never move without asking.
- `context/mission.md` and `context/stakes.md` are never edited without asking.
- `context/memory.md` and `context/ledger.md` are append-only.
- The read lists in each skill apply on the phone too. A cloud routine that reads
  all of `context/` burns the same tokens as one at the desk, and it runs four
  times a day unattended — so it burns them whether Samuel is there or not.
- One routine, one session. The brief, midday and reckoning routines must not
  share a session; each fires clean.

## Finding TickTick in a cloud session

In cloud runs the connector tools are **deferred** — they don't appear in the tool
list until you load them. They are named `mcp__TickTick__*`, not the local UUID
names. Load them first:

`ToolSearch` with query `ticktick projects tasks`

Same for `mcp__Gmail__*`, `mcp__Google_Calendar__*`, `mcp__Google_Drive__*`.
Verified working from a cloud run on 2026-08-23.

## If TickTick is missing from a session

Say so in one line and run off `context/` alone. Mark anything taken on Samuel's
word as UNVERIFIED in the ledger. Never pretend the tasks were checked.

## The budget sheet from the cloud

The sheet is written through an Apps Script bridge whose URL and token live in
`.env` — and `.env` is gitignored, so a cloud clone does not have it. Cloud
environments also block Google Apps Script by default: it is not on the
**Trusted** allowlist, and the `/exec` URL redirects to
`script.googleusercontent.com`, so both hosts have to be allowed.

Both are fixed once, in the browser, on the environment the routines run in.
There is no settings page for it: claude.ai/code/routines → routine → pencil →
the cloud icon under **Instructions** → gear on the environment. Set network
access to **Custom** (with the default list still included) plus:

```
script.google.com
*.googleusercontent.com
```

and the three variables `SHEETS_WEBAPP_URL`, `SHEETS_TOKEN`, `SHEETS_ID`.
Full walkthrough in `tools/sheets/README.md`.

In any session, on any device, the first question is answered by:

```bash
python tools/sheets/sheets.py doctor
```

### If the bridge is down, the money is still not lost

Money batches are sent with `--queue "<label>"`. Undeliverable ones are parked
in `context/sheet-queue.jsonl` and committed with the rest of `context/`. The
next session anywhere that can reach the bridge runs
`python tools/sheets/sheets.py flush` and the sheet catches up.

So the rule on the phone is the same as at the desk: **write the ledger first,
queue the mirror, commit, push.** A cloud session never skips the ledger because
the sheet failed, and never leaves the mirror silently behind.

## Cloud sessions start on a DETACHED HEAD — 2026-08-28

The cloud clone checks out a commit, not a branch. So `git push -u origin main`
pushes the stale local `main` ref and is **rejected as non-fast-forward**, while
`git pull --rebase` reports "HEAD is up to date" and hides the problem. The 28 Aug
reckoning hit this after everything was written and committed.

The rule this protects is the one that matters: **unpushed is lost.**

Check first, fix in one line:

```bash
git rev-parse --abbrev-ref HEAD          # prints "HEAD" if detached
git branch -f main HEAD && git checkout main && git push -u origin main
```

`git branch -f` is only safe because the local `main` is an ancestor of the new
commit — verify with `git merge-base --is-ancestor main HEAD` before forcing it.
Never force a branch that has commits the new HEAD does not contain.

## The laptop pulls itself — 2026-08-28

Nothing in the cloud can reach the laptop. A routine pushes to GitHub; a machine
that is not listening stays stale. Samuel found this the hard way at the 28 Aug
reckoning: *"You are meant to pull automatically and update the Laptop always."*

So the laptop pulls itself. `tools/pull.sh` runs as a **SessionStart hook**
(`.claude/settings.json`), which means every Claude Code session on any machine
starts on the latest `context/` without anyone typing `git pull`.

It is deliberately timid and never touches work in progress. It skips, and says
which, on: a dirty tree, a branch other than `main`, a detached HEAD, or no
network. A hook that eats uncommitted work once is a hook that gets deleted.

**What it does NOT cover, stated plainly:** opening `site/index.html` by
double-clicking outside a session still shows whatever was last pulled. The hook
makes the *session* current, not the *file on disk at all times*. The only real
fix for "a link that is always current" is hosting — see the note below.

## The site is built but not published — 2026-08-28

All six GitHub Pages deploys have FAILED at `actions/configure-pages`. The build
step passes every time; only publishing is broken. GitHub does not serve Pages
from a **private** repo on the free plan, and this repo must stay private.

Two ways out, decided at a brief and not at 10pm:

1. Enable Pages (Settings → Pages → Source → GitHub Actions). Only works on a
   paid plan. Verify the deploy actually goes green — do not trust the push.
2. Publish the dashboard as an Artifact, the same mechanism as the nightly
   scorecard, which already works from the phone. One fixed URL, no GitHub
   plan, no cost. Needs `tools/site/build.py` to emit a single bundled file.

**The rule this leaves behind:** a failing GitHub Action is silent. Never report
something as PUBLISHED on the strength of a successful push — check the deploy.
Same discipline as the sheet queue: a mirror that was parked is not a mirror
that was written.

## `published.sh` cannot run from a cloud session — 2026-09-02

Pages was fixed on 2 Sep (the source was set to a branch, not Actions — run 12
onward all go green), so the section above is history. A new hole took its place
and it is specific to the routines.

**The cloud environment's network policy blocks `samuelade001.github.io`.** The
agent proxy answers `403` to the CONNECT, so `bash tools/site/published.sh`
returns `HTTP 000000 — the site is not being served` from here. That reads
exactly like a dead site and it is not one: the same URL is fine from his phone
and his laptop. The reckoning that hit it had a green deploy at the same moment.

**What a cloud session must do instead, and must say plainly:**

```bash
# published.sh will 000 — that is the sandbox, not the site.
# Check the deploy through the GitHub API, which IS reachable:
#   mcp__github__actions_list  -> newest run for .github/workflows/pages.yml
#   mcp__github__actions_get   -> conclusion == "success"
```

A green deploy is **stronger than a push and weaker than a fetch.** Report it as
"deploy green, page not fetched from this session" — never as PUBLISHED, and
never as broken. The rule from 28 Aug still stands and this is its next layer:
do not report a state you did not verify, including the failure state.

**The permanent fix** is one line in the cloud environment, same dialog as the
sheets bridge (claude.ai/code/routines → routine → pencil → cloud icon → gear →
Network access: Custom): add

```
samuelade001.github.io
```

alongside `script.google.com` and `*.googleusercontent.com`. Until that is done,
every scheduled reckoning ends on an unverifiable publish step.
