---
type: log
area: system
status: needs-input
updated: 2026-09-27
source: manual
tags: [inbox, git, needs-pc]
---

# 2026-09-27 — cloud session git sync note (needs PC)

This morning's brief routine found the container's local `main` branch pointing at a stale, unrelated history (last commit 2026-09-23, no common ancestor with `origin/main`) — `git merge --ff-only origin/main` failed with "refusing to merge unrelated histories". Worked around it by leaving `main` alone and reading from a detached checkout of `origin/main` instead (no writes, no risk to Samuel's data — `origin/main` is unaffected). The stale local branch itself is a throwaway container artifact, but flagging it since `git checkout -B main origin/main` to fix it was blocked by the auto-mode permission classifier as "irreversible local destruction," so it needs a human (or a session with that permission) to clean up. Also still open from the SessionStart hook: `origin/claude/entertainment-recommendations-2xppuq` is an unmerged cloud-session branch to review per `00-System/portability.md` → Cloud sessions and the PC.
