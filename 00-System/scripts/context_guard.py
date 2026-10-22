"""Context guard: keeps sessions and helper agents small.

Claude Code PostToolUse hook. Reads how big the working context is from the
last assistant turn in the transcript (input + cache write + cache read) and,
once per threshold, tells the model to checkpoint or wrap up. Auto-compact
itself is set in .claude/settings.json (autoCompactWindow); this guard makes
sure the job's state is written to the Brain before compaction, and stops
helper agents from growing past the size that made the B2B video cost ~120 %
of a week. Rule: 00-System/model-routing.md -> Session size.

Never blocks a tool call; any error exits 0 silently.
"""
import glob
import json
import os
import sys
import tempfile

MAIN_CHECKPOINT = 460_000   # auto-compact runs at 500k (settings.json)
SUB_WRAP = 300_000   # Samuel, 2026-10-22: give helpers more room (was 150k / 185k)
SUB_STOP = 350_000
TAIL_BYTES = 3_000_000


def context_size(path):
    """Context tokens of the last assistant turn in a transcript, or None."""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as f:
            f.seek(max(0, size - TAIL_BYTES))
            lines = f.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        if '"usage"' not in line:
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") != "assistant":
            continue
        u = (d.get("message") or {}).get("usage") or {}
        return ((u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)
                + (u.get("cache_read_input_tokens") or 0))
    return None


def agent_transcript(main_path, agent_id):
    base = os.path.splitext(main_path)[0]
    aid = agent_id[6:] if agent_id.startswith("agent-") else agent_id
    hits = glob.glob(os.path.join(base, "subagents", "**", f"agent-{aid}.jsonl"), recursive=True)
    return hits[0] if hits else None


def fired(key, level, ctx):
    """Fire each level once; re-arm when the context drops (after a compaction)."""
    state_dir = os.path.join(tempfile.gettempdir(), "brain-context-guard")
    os.makedirs(state_dir, exist_ok=True)
    p = os.path.join(state_dir, key + ".json")
    try:
        st = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        st = {}
    if ctx < st.get("last", 0) - 50_000:
        st = {}
    st["last"] = ctx
    new = level not in st.get("levels", [])
    if new:
        st.setdefault("levels", []).append(level)
    json.dump(st, open(p, "w", encoding="utf-8"))
    return new


def main():
    data = json.load(sys.stdin)
    tpath = data.get("transcript_path") or ""
    agent_id = data.get("agent_id") or ""
    if agent_id:
        path = agent_transcript(tpath, agent_id)
        ctx = context_size(path) if path else None
        if ctx is None:
            return
        key = f"{data.get('session_id', 'x')}-{agent_id}"
        k = ctx // 1000
        if ctx >= SUB_STOP and fired(key, "stop", ctx):
            msg = (f"Context guard: your context is {k}k tokens, past the {SUB_STOP // 1000}k cap. "
                   "Stop starting new items. Save what is done to disk, write your hand-over "
                   "(done, not done, file paths) and return it now as your final result.")
        elif ctx >= SUB_WRAP and fired(key, "wrap", ctx):
            msg = (f"Context guard: your context is {k}k tokens. Finish the item you are on, "
                   f"then wrap up; you must return before {SUB_STOP // 1000}k. Keep tool output short "
                   "(counts and paths, no dumps, no extra full-size images).")
        else:
            return
        out = {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}}
    else:
        ctx = context_size(tpath)
        if ctx is None or ctx < MAIN_CHECKPOINT:
            return
        if not fired(data.get("session_id", "x"), "checkpoint", ctx):
            return
        k = ctx // 1000
        msg = (f"Context guard: this session is at {k}k tokens; auto-compact runs at 500k. "
               "Before the next big step: write the job's RESUME block (done, next step, open "
               "decisions, Samuel's latest words) into the job note, commit, and tell Samuel the "
               "session is about to compact. If the current step is finished, end the session "
               "instead (build-state, commit, push) and name the next step for a fresh session.")
        out = {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg},
               "systemMessage": f"Context at {k}k: checkpointing before auto-compact at 500k."}
    print(json.dumps(out))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
