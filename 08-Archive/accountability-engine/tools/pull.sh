#!/usr/bin/env bash
# Auto-pull the engine at the start of every Claude Code session.
#
# Why this exists: the cloud routines (brief, midday, reckoning, weekly review)
# push to GitHub. Nothing reaches the laptop on its own — a cloud container
# cannot write to a machine that is not listening. So the laptop pulls itself,
# here, before any check-in reads a stale context/ file.
#
# Wired in as a SessionStart hook in .claude/settings.json. It prints a JSON
# systemMessage so the result is visible in the session rather than silent.
#
# It is deliberately timid. It NEVER touches work in progress:
#   - dirty tree      -> skip, say so
#   - not on main     -> skip, say so
#   - detached HEAD   -> skip, say so (see REMOTE.md)
#   - no network      -> skip, say so
# A hook that eats uncommitted work once is a hook that gets deleted.

set -u

say() { printf '{"systemMessage":"engine: %s"}\n' "$1"; exit 0; }

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$(dirname "$(readlink -f "$0")")")}" 2>/dev/null || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
[ "$branch" = "HEAD" ] && say "detached HEAD — no auto-pull (see REMOTE.md)"
[ "$branch" = "main" ] || say "on branch $branch, not main — no auto-pull"

[ -n "$(git status --porcelain 2>/dev/null)" ] && say "uncommitted changes — no auto-pull, commit or stash first"

before=$(git rev-parse HEAD)
git pull --rebase --quiet origin main >/dev/null 2>&1 || say "could not reach GitHub — working off the local copy"
after=$(git rev-parse HEAD)

if [ "$before" = "$after" ]; then
  say "already up to date"
else
  n=$(git rev-list --count "$before".."$after" 2>/dev/null || echo "?")
  say "pulled $n new commit(s) from GitHub"
fi
