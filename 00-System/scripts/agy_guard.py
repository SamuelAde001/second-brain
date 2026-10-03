"""Antigravity (Gemini) hooks: the same guard rails Claude Code runs under, so both AIs are equal.

Wired in .agents/hooks.json (read by the Antigravity app and agy in this Brain):

    python 00-System/scripts/agy_guard.py pre-tool     # PreToolUse: deny secrets, ask before destructive commands
    python 00-System/scripts/agy_guard.py first-turn   # PreInvocation: the session-start sync, once per conversation

pre-tool mirrors .claude/settings.json -> permissions.deny and permissions.ask. It only ever blocks or asks;
it never grants anything: every other call gets "ask", which defers to Antigravity's own permission
setting (tested 2026-10-02: an empty reply is treated as deny).
Edit both files together (00-System/relay.md -> Same rules, both AIs).
first-turn runs session_start_sync.py on the first model call of a conversation (Antigravity has no
SessionStart event) and injects its note, naming any commits Claude made since Gemini's last.
Hook contract: %USERPROFILE%/.gemini/antigravity-cli/builtin/skills/agy-customizations/docs/hooks.md.
Never blocks a session: on any error it falls back to "ask" (pre-tool) or {} (first-turn) and exits 0.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# .claude/settings.json -> permissions.deny (reads of secrets; the API key variable).
DENY = [
    r"brain-secrets",
    r"(^|[\\/])\.env($|[\s\"'])",
    r"\.key($|[\s\"'])",
    r"(^|[\\/])credentials[^\\/]*\.json",
    r"(^|[\\/])token[^\\/]*\.json",
    r"ANTHROPIC_API_KEY",
]
# .claude/settings.json -> permissions.ask (deleting, process/system, scheduled tasks, installs, history rewrites).
ASK = [
    r"\bRemove-Item\b", r"(^|[\s;&|(])(rm|del|rd|rmdir)\s", r"\bClear-Content\b",
    r"\bStop-Process\b", r"\bStop-Service\b", r"\bRestart-Computer\b", r"\bStop-Computer\b",
    r"\bSet-ExecutionPolicy\b", r"\bFormat-Volume\b", r"(^|[\s;&|(])reg\s",
    r"\bschtasks\b", r"\b(Un)?Register-ScheduledTask\b", r"\bwinget\b",
    r"\bgit\s+(reset|clean|rebase)\b", r"\bgit\s+push\s+(.*\s)?(--force|-f)\b", r"\bgit\s+push\s+(.*\s)?\+",
]


def pre_tool(payload):
    call = payload.get("toolCall") or {}
    args = json.dumps(call.get("args") or {})
    for pat in DENY:
        if re.search(pat, args, re.I):
            return {"decision": "deny",
                    "reason": "Blocked by the Brain's guard: secrets are never read by an AI (AGENTS.md section 6)."}
    if call.get("name") == "run_command":
        cmd = str((call.get("args") or {}).get("CommandLine", ""))
        for pat in ASK:
            if re.search(pat, cmd, re.I):
                return {"decision": "force_ask",
                        "reason": "Deletes, system changes, installs and history rewrites need Samuel's yes (AGENTS.md section 5)."}
    # "allow" lets safe commands proceed automatically without prompting the user.
    return {"decision": "allow"}


def first_turn(payload):
    conv = payload.get("conversationId") or ""
    mark = os.path.join(tempfile.gettempdir(), "brain-agy-synced", conv or "none")
    if os.path.exists(mark):
        return {}
    os.makedirs(os.path.dirname(mark), exist_ok=True)
    open(mark, "w").close()
    r = subprocess.run([sys.executable, os.path.join(BRAIN, "00-System", "scripts", "session_start_sync.py"),
                        "--for", "gemini"], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=45)
    note = (r.stdout or "").strip()
    try:
        note = json.loads(note).get("systemMessage", note)
    except json.JSONDecodeError:
        pass
    if not note:
        return {}
    return {"injectSteps": [{"ephemeralMessage": "Session start (AGENTS.md section 12). " + note}]}


def main():
    out = {}
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        mode = sys.argv[1] if len(sys.argv) > 1 else ""
        if mode == "pre-tool":
            out = pre_tool(payload)
        elif mode == "first-turn":
            out = first_turn(payload)
    except Exception:  # never block a session
        out = {"decision": "ask"} if sys.argv[1:2] == ["pre-tool"] else {}
    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main()
