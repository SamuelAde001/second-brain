"""Pull Samuel's own messages out of the Claude Code transcripts, keep the editing ones, split them by date.

Writes into --work:
  samuel_all.md         every message he typed (deduped, oldest first)
  samuel_video.md       the ones that mention editing (keyword filter), under 6,000 chars each
  samuel_video_big.md   the long ones (voice notes, pastes) over 6,000 chars
  chunk1..N.md          editing messages + editor voice notes, split into N equal date ranges

Usage: python rb_extract.py --work <folder> [--chunks 4] [--since 2026-11-03]
Read-only on the transcripts (AGENTS.md §10, relay grant).
"""
import argparse, glob, json, os, re

SRC = os.path.expandvars(r"%USERPROFILE%/.claude/projects/C--Users-repzy-Desktop-My-Second-brain")
KW = re.compile(r"resolve|fusion|timeline|visual|edit|render|clip|node|comp\b|comps|font|colou?r|zoom|b-?roll|sfx|sound|music|"
                r"transition|animation|motion|routerise|route rise|alex|frontal|gamma|marker|intro|cut|subtitle|transcript|glow|"
                r"blur|highlight|pill|box|card|screen ?record|tella|graphic|text|keyframe|adjustment|editor|video|frame|"
                r"creative director|ifeoma|reference|style|cache|drive", re.I)
EDITOR_BIG = ["editor", "Editor", "linkedin video", "visuals of this video", "visual cuts"]


def messages(since):
    out, seen = [], set()
    for f in glob.glob(SRC + "/*.jsonl"):
        sid = os.path.basename(f)[:8]
        for line in open(f, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") != "user" or d.get("isMeta") or d.get("isSidechain") or d.get("isCompactSummary"):
                continue
            c = d.get("message", {}).get("content")
            if isinstance(c, str):
                texts = [c]
            elif isinstance(c, list):
                texts = [b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text"]
            else:
                continue
            t = re.sub(r"<system-reminder>.*?</system-reminder>", "", "\n".join(texts), flags=re.S)
            t = re.sub(r"<(command-[a-z-]+|local-command-[a-z]+|task-notification|side-sessions-event|ci-monitor-event)>.*?</\1>",
                       "", t, flags=re.S).strip()
            if not t or t.startswith(("This session is being continued", "[Request interrupted", "Caveat:")):
                continue
            ts = d.get("timestamp", "")
            if since and ts[:10] < since:
                continue
            if t[:300] in seen:
                continue
            seen.add(t[:300])
            out.append((ts, sid, t))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--chunks", type=int, default=4)
    ap.add_argument("--since", default="", help="only messages on or after this date (YYYY-MM-DD)")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    blocks = [f"### {ts[:16]} {sid}\n{t}\n" for ts, sid, t in messages(a.since)]
    w = lambda name, bs: open(os.path.join(a.work, name), "w", encoding="utf-8").write("\n".join(bs))
    w("samuel_all.md", blocks)
    video = [b for b in blocks if KW.search(b)]
    small = [b for b in video if len(b) <= 6000]
    big = [b for b in video if len(b) > 6000]
    w("samuel_video.md", small)
    w("samuel_video_big.md", big)
    keep = sorted(small + [b for b in big if any(k in b[:200] for k in EDITOR_BIG)], key=lambda b: b[4:20])
    per, cur, size, k = sum(map(len, keep)) / max(a.chunks, 1), [], 0, 1
    for b in keep:
        cur.append(b)
        size += len(b)
        if size >= per and k < a.chunks:
            w(f"chunk{k}.md", cur)
            cur, size, k = [], 0, k + 1
    w(f"chunk{k}.md", cur)
    print(f"{len(blocks)} messages, {len(video)} about editing, {len(big)} long, {k} chunks -> {a.work}")


if __name__ == "__main__":
    main()
