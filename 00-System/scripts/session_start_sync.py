"""Session-start sync: bring the PC's Brain up to date with GitHub.

Run at the start of every session by both AIs: Claude Code's SessionStart hook (.claude/settings.json)
and, with --for gemini, Antigravity's first-turn hook (.agents/hooks.json via agy_guard.py). It:
  1. fetches origin,
  2. fast-forwards local main to origin/main (only when on main, only fast-forward,
     so nothing is ever merged, rebased or overwritten here),
  3. lists claude/* branches from cloud sessions that main hasn't merged yet,
  4. names the commits the other AI made since this AI's last one (00-System/relay.md).

Merging those branches is the session's job, with review (portability.md ->
Cloud sessions and the PC). This script never merges, deletes or resets.
It always exits 0, so a failed sync never blocks a session. It says what failed instead.
"""
import argparse
import json
import os
import subprocess

BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def git(*args, timeout=25):
    r = subprocess.run(["git", "-C", BRAIN, *args], capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--for", dest="for_ai", choices=["claude", "gemini"], default="claude")
    for_ai = ap.parse_args().for_ai
    notes = []
    try:
        code, out = git("fetch", "--prune", "origin")
        if code != 0:
            notes.append(f"Brain sync: fetch failed, working from the local copy. ({out.splitlines()[-1] if out else 'no output'})")
        else:
            _, branch = git("rev-parse", "--abbrev-ref", "HEAD")
            _, behind = git("rev-list", "--count", "HEAD..origin/main")
            behind = int(behind) if behind.isdigit() else 0
            if branch != "main":
                notes.append(f"Brain sync: on branch '{branch}', not main. No pull done.")
            elif behind:
                code, out = git("merge", "--ff-only", "origin/main")
                if code == 0:
                    notes.append(f"Brain sync: pulled {behind} new commit(s) from GitHub.")
                else:
                    notes.append(f"Brain sync: {behind} commit(s) on GitHub could NOT be pulled (local changes in the way, or main has diverged). Show Samuel; do not force. ({out.splitlines()[-1] if out else ''})")
            else:
                notes.append("Brain sync: up to date with GitHub.")

            _, unmerged = git("branch", "-r", "--no-merged", "main")
            cloud = [b.strip() for b in unmerged.splitlines() if b.strip().startswith("origin/claude/")]
            if cloud:
                notes.append("Unmerged cloud-session branches (review and merge per portability.md): " + ", ".join(cloud))

            # Work the other AI did since this one's last commit (00-System/relay.md -> Switching).
            me, other = ("Gemini", "Claude") if for_ai == "gemini" else ("Claude", "Gemini")
            _, last_mine = git("log", "-1", "--format=%H", "-i", f"--grep=Co-Authored-By: {me}",
                               *([r"--grep=^\[gemini\]"] if me == "Gemini" else []))
            if last_mine:
                _, log = git("log", f"{last_mine}..HEAD", "--format=%h %s%x1f%b%x1e")
                theirs = []
                for entry in log.split(""):
                    head, _, body = entry.strip().partition("")
                    subject = head.split(" ", 1)[-1]
                    if (f"co-authored-by: {other.lower()}" in body.lower()
                            or (other == "Gemini" and subject.startswith("[gemini]"))):
                        theirs.append(head)
                if theirs:
                    notes.append(f"{other} made {len(theirs)} commit(s) since {me}'s last: read them and the newest "
                                 "relay-log entry before carrying on (00-System/relay.md -> Switching). "
                                 + " | ".join(theirs[:5]))
    except Exception as e:  # never block a session
        notes.append(f"Brain sync: skipped ({e.__class__.__name__}: {e}).")

    msg = " ".join(notes)
    print(json.dumps({
        "systemMessage": msg,
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": msg},
    }))


if __name__ == "__main__":
    main()
