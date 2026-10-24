"""PC background sync: keep GitHub (and so the phone) level with the PC's Brain, all day.

Run every 10 minutes by the Windows task "Brain - git sync" (pythonw, hidden), so the phone's
Obsidian Git plugin always pulls the latest, and phone notes reach the PC without a session.
Each run, only on main and only when no merge or rebase is in progress:
  1. fetches origin,
  2. brings in phone/cloud commits: fast-forward when it can, otherwise a normal merge
     (never rebase, never force, AGENTS.md rule 4). A merge that conflicts or would touch
     uncommitted files is aborted and left for the next session to show Samuel,
  3. pushes commits the PC has that GitHub doesn't.
It never commits. Uncommitted edits (an agent mid-job, Samuel typing in Obsidian) wait for
the session that owns them (AGENTS.md section 12). Log: %LOCALAPPDATA%\\Brain\\git-sync.log,
outside the Brain so it never makes a change to commit. 00-System/phone-sync.md -> The PC side.
"""
import datetime
import os
import subprocess

BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = os.path.join(os.environ.get("LOCALAPPDATA", BRAIN), "Brain", "git-sync.log")
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def git(*args, timeout=60):
    r = subprocess.run(["git", "-C", BRAIN, *args], capture_output=True, text=True,
                       timeout=timeout, creationflags=NO_WINDOW)
    return r.returncode, (r.stdout + r.stderr).strip()


def log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    lines = []
    if os.path.exists(LOG):
        with open(LOG, encoding="utf-8") as f:
            lines = f.readlines()[-499:]  # keep the last 500 lines
    lines.append(f"{datetime.datetime.now():%Y-%m-%d %H:%M} {msg}\n")
    with open(LOG, "w", encoding="utf-8") as f:
        f.writelines(lines)


def sync():
    gitdir = os.path.join(BRAIN, ".git")
    if any(os.path.exists(os.path.join(gitdir, p)) for p in
           ("MERGE_HEAD", "REBASE_HEAD", "rebase-merge", "rebase-apply", "index.lock")):
        return "skipped: git busy (merge, rebase or another git command in progress)"
    _, branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        return f"skipped: on '{branch}', not main"
    code, out = git("fetch", "--prune", "origin")
    if code != 0:
        return f"fetch failed: {out.splitlines()[-1] if out else 'no output'}"

    notes = []
    _, behind = git("rev-list", "--count", "HEAD..origin/main")
    _, ahead = git("rev-list", "--count", "origin/main..HEAD")
    behind, ahead = int(behind or 0), int(ahead or 0)
    if behind:
        if not ahead:
            code, out = git("merge", "--ff-only", "origin/main")
        else:
            code, out = git("merge", "--no-edit", "-m", "Merge GitHub main (phone/cloud) into PC main", "origin/main")
        if code != 0:
            if os.path.exists(os.path.join(gitdir, "MERGE_HEAD")):
                git("merge", "--abort")
            return f"pull of {behind} commit(s) FAILED, left for the next session: {out.splitlines()[-1] if out else ''}"
        notes.append(f"pulled {behind}")
    _, ahead = git("rev-list", "--count", "origin/main..HEAD")
    if int(ahead or 0):
        code, out = git("push", "origin", "main")
        notes.append(f"pushed {ahead}" if code == 0 else f"push FAILED: {out.splitlines()[-1] if out else ''}")
    return ", ".join(notes)


def main():
    try:
        msg = sync()
    except Exception as e:  # a background job must never pop up an error
        msg = f"error: {e.__class__.__name__}: {e}"
    if msg:  # quiet when there was nothing to do
        log(msg)


if __name__ == "__main__":
    main()
