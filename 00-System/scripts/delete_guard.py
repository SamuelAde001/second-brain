"""Delete guard: agents delete their own files without asking; any other delete asks Samuel.

Claude Code PreToolUse hook on Bash and PowerShell (.claude/settings.json). Samuel, 2026-10-22: "I don't want them
to ask me when they want to delete files created on their own" (and earlier the same day: ask only for screen
control and deletes). agy_guard.py uses classify() for Gemini, so both AIs follow the same rule.

A command that deletes (rm, rmdir, Remove-Item, del, rd, ri, erase) is allowed only when every target is agent-owned:
  - strictly inside a folder whose name carries an agent tag, e.g. "...\\Frontal kit (Editor)\\renders\\x.jpg"
    (the tagged folder itself, or anything above it, still asks);
  - inside the temp folder (%TEMP%, where each session's scratchpad lives);
  - inside the Brain's _attachments\\creative-director-breakdowns\\ (key frames the Editor's analysts made).
Never auto-allowed: paths through a folder named like a finished render, a delivery or invoices.
Anything else, a target that can't be resolved, or a command that can't be parsed: "ask". Not a delete: no output
(the normal permission rules apply). Never blocks a session on its own error: falls back to "ask" for deletes.
Every decision is appended to %TEMP%\\brain-delete-guard.log.
"""
import glob
import json
import os
import re
import shlex
import sys
import tempfile
import time

AGENT_TAGS = ("(Editor)", "(Brand manager)", "(PA)", "(Money man)", "(General Manager)")
KEEP = ("final render", "delivered", "invoices")
BRAIN = os.path.normcase(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OWNED_ROOTS = [os.path.normcase(os.path.join(BRAIN, "_attachments", "creative-director-breakdowns"))]
TEMP = os.path.normcase(os.path.realpath(tempfile.gettempdir()))
DEL_BASH = {"rm", "rmdir", "unlink", "shred"}
DEL_PS = {"remove-item", "rm", "del", "rd", "rmdir", "ri", "erase"}
CD = {"cd", "set-location", "sl", "chdir", "pushd"}
SPLIT = re.compile(r"\s*(?:&&|\|\||;|\||\n)\s*")


def _winpath(p):
    """'/c/Users/x' -> 'C:/Users/x' (Git Bash); strip quotes."""
    p = p.strip().strip('"').strip("'")
    m = re.match(r"^/([a-zA-Z])(/|$)(.*)", p)
    if m:
        p = m.group(1).upper() + ":/" + m.group(3)
    return os.path.expandvars(os.path.expanduser(p))


def _resolve(p, cwd):
    p = _winpath(p)
    if not os.path.isabs(p):
        p = os.path.join(cwd, p)
    hits = glob.glob(p) if any(c in p for c in "*?[") else []
    return [os.path.normcase(os.path.realpath(h)) for h in hits] or [os.path.normcase(os.path.realpath(p))]


def owned(path):
    """True when `path` is an agent's own file (see module doc)."""
    if path == TEMP or path.startswith(TEMP + os.sep):
        return path != TEMP
    for root in OWNED_ROOTS:
        if path.startswith(root + os.sep):
            return True
    parts = path.split(os.sep)
    if any(k in seg.lower() for seg in parts for k in KEEP):
        return False                              # finished renders and deliverables always ask
    for seg in parts[:-1]:                        # a tagged folder ABOVE the target, never the target itself
        if any(t.lower() in seg.lower() for t in AGENT_TAGS):
            return True
    return False


def _words(seg, ps):
    try:
        return shlex.split(seg, posix=not ps)
    except ValueError:
        return seg.split()


def classify(command, cwd, shell="bash"):
    """Return None (no delete), 'allow' (all targets agent-owned) or 'ask', plus the targets seen."""
    ps = shell == "powershell"
    cwd = _winpath(cwd or os.getcwd())
    targets, deletes, var = [], False, {}

    def subst(s):                                  # $S / ${S} / $env:S from earlier assignments or the environment
        return re.sub(r"\$(?:env:)?\{?([A-Za-z_]\w*)\}?",
                      lambda m: var.get(m.group(1), os.environ.get(m.group(1), m.group(0))), s)

    for seg in SPLIT.split(command or ""):
        raw = [x.strip('"').strip("'") for x in _words(seg, ps)]
        w = [subst(x) for x in raw]
        if not w:
            continue
        if not ps and all(re.match(r"^[A-Za-z_]\w*=", x) for x in w):          # S="..." P="..."
            for x in w:
                k, _, v = x.partition("=")
                var[k] = subst(v)
            continue
        if ps and len(raw) >= 3 and re.match(r"^\$[A-Za-z_]\w*$", raw[0]) and raw[1] == "=":   # $S = "..."
            var[raw[0][1:]] = w[2]
            continue
        head = w[0].lower()
        if head in CD and len(w) > 1:
            nxt = [x for x in w[1:] if not x.startswith("-")]
            if nxt:
                cwd = _winpath(nxt[0]) if os.path.isabs(_winpath(nxt[0])) else os.path.join(cwd, _winpath(nxt[0]))
            continue
        if (not ps and head in DEL_BASH) or (ps and head in DEL_PS):
            deletes = True
            args, skip = [], False
            for x in w[1:]:
                if skip:
                    skip = False
                    continue
                if ps and x.lower() in ("-path", "-literalpath"):
                    continue
                if ps and x.startswith("-") and x.lower() in ("-include", "-exclude", "-filter"):
                    skip = True
                    continue
                if x.startswith("-"):
                    continue
                if ps:
                    args.extend(a for a in x.split(",") if a)
                else:
                    args.append(x)
            if not args:
                return "ask", targets
            for a in args:
                targets += _resolve(a, cwd)
    if not deletes:
        return None, targets
    return ("allow" if targets and all(owned(t) for t in targets) else "ask"), targets


def _log(decision, cmd, targets):
    try:
        with open(os.path.join(tempfile.gettempdir(), "brain-delete-guard.log"), "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{decision}\t{cmd[:300]!r}\t{targets[:20]}\n")
    except OSError:
        pass


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    cmd = (data.get("tool_input") or {}).get("command", "")
    shell = "powershell" if tool == "PowerShell" else "bash"
    try:
        decision, targets = classify(cmd, data.get("cwd") or "", shell)
    except Exception:
        looks = re.search(r"(^|[\s;&|(])(rm|rmdir|del|rd|ri|erase|Remove-Item)\b", cmd or "", re.I)
        decision, targets = ("ask" if looks else None), []
    _log(decision or "pass", cmd or "", targets)
    if decision is None:
        return
    reason = ("Agent deleting its own files (agent-tagged folder, temp, or CD key frames)" if decision == "allow"
              else "Deleting something that is not an agent's own file: needs Samuel's yes (decision 2026-10-22)")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
