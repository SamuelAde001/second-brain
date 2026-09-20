#!/usr/bin/env python3
"""
Split a Claude account export (conversations.json) into one markdown file per
conversation and write a triage CSV for Samuel to trim before any model reads them.

Standard library only. Reads nothing into a model's context: this is the
"script first" rule in AGENTS.md §5.10 doing its job.

Usage (from the vault root):
    python 00-System/scripts/split_conversations.py

Inputs:
    01-Inbox/_imports/claude-export/conversations-000.zip   (or extracted/conversations.json)

Outputs:
    01-Inbox/_imports/processed/conversations/<date>-<slug>.md
    01-Inbox/_imports/processed/triage.csv
"""

import csv
import json
import os
import re
import sys
import zipfile
from collections import Counter

VAULT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXPORT_DIR = os.path.join(VAULT, "01-Inbox", "_imports", "claude-export")
OUT_DIR = os.path.join(VAULT, "01-Inbox", "_imports", "processed", "conversations")
TRIAGE = os.path.join(VAULT, "01-Inbox", "_imports", "processed", "triage.csv")

# Area keywords. Order matters only for reporting; scoring picks the best match.
# Keep these lowercase. Add to them rather than rewriting — the matches get
# reviewed by Samuel anyway, so a wrong guess costs nothing but a glance.
AREA_KEYWORDS = {
    "video-editing": [
        "resolve", "davinci", "fusion", "timeline", "render", "export settings",
        "lut", "colour grade", "color grade", "b-roll", "broll", "cut sheet",
        "subtitle", "caption", "transition", "keyframe", "node", "obs",
        "client edit", "rough cut", "footage", "codec", "h.264", "h.265",
        "multicam", "edit pass", "routerise", "comfort cuts", "osmo", "dji",
    ],
    "personal-brand": [
        "instagram", "reel", "hook", "script", "storytelling", "content pillar",
        "posting", "talking head", "yap", "caption copy", "followers",
        "engagement", "viral", "thumbnail", "samuelsignals", "docuseries",
        "called to create", "guiding while riding",
    ],
    "highsignals": ["highsignals", "high signals", "ecosystem", "ascension", "signal from the noise"],
    "academy": ["course", "curriculum", "lesson", "module", "teach", "student", "called to edit", "academy"],
    "community": ["community", "members", "accountability tracker", "group review", "live session"],
    "mentorship": ["mentorship", "mentee", "mentor", "one-on-one", "1-on-1"],
    "scripnals": ["scripnals", "app build", "voice note to script", "mvp", "apk", "onboarding flow"],
    "finances": [
        "budget", "naira", "ngn", "usd", "invoice", "retainer", "income",
        "savings", "cleva", "expense", "runway", "pricing", "rate card", "paid",
    ],
    "relationships": ["family", "friend", "wife", "girlfriend", "relationship", "birthday", "check in on"],
    "study": [
        "hvdc", "dielectric", "busbar", "transmission line", "power system",
        "instrumentation", "eee 804", "term paper", "ieee format", "tutorial question",
        "postgraduate", "lecturer",
    ],
    "me": [
        "habit", "routine", "morning", "discipline", "accountability", "gym",
        "fitness", "sleep", "goal", "mission", "stakes", "ledger", "reckoning",
        "enforcer", "ticktick",
    ],
    "system": ["second brain", "obsidian", "vault", "claude code", "agents.md", "mcp", "skill", "subagent"],
}

DROP_HINTS = [
    "test", "hello", "hi claude", "untitled", "quick question",
]


def slugify(text, maxlen=60):
    text = re.sub(r"[^\w\s-]", "", (text or "").lower()).strip()
    text = re.sub(r"[\s_]+", "-", text)
    return (text[:maxlen].strip("-") or "untitled")


def message_text(msg):
    """Claude's export puts text either on `text` or inside `content` blocks."""
    t = msg.get("text") or ""
    if not t:
        parts = []
        for block in msg.get("content") or []:
            if isinstance(block, dict) and block.get("text"):
                parts.append(block["text"])
        t = "\n".join(parts)
    return t


def match_area(title, body):
    """Score every area by keyword hits; title hits count triple."""
    title_l = (title or "").lower()
    body_l = body.lower()
    scores = Counter()
    for area, words in AREA_KEYWORDS.items():
        for w in words:
            if w in title_l:
                scores[area] += 3
            scores[area] += body_l.count(w)
    if not scores:
        return "", 0
    area, score = scores.most_common(1)[0]
    return (area, score) if score else ("", 0)


def load_conversations():
    zip_path = os.path.join(EXPORT_DIR, "conversations-000.zip")
    json_path = os.path.join(EXPORT_DIR, "extracted", "conversations.json")
    if os.path.exists(json_path):
        with open(json_path, encoding="utf-8") as fh:
            return json.load(fh)
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path) as z:
            return json.loads(z.read("conversations.json").decode("utf-8"))
    sys.exit(f"No conversations export found in {EXPORT_DIR}")


def main():
    convos = load_conversations()
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []

    for convo in convos:
        title = convo.get("name") or "(untitled)"
        created = (convo.get("created_at") or "")[:10]
        msgs = convo.get("chat_messages") or []

        lines = [f"# {title}", "", f"- Created: {created}", f"- Messages: {len(msgs)}",
                 f"- Export uuid: {convo.get('uuid','')}", "", "---", ""]
        body_parts = []
        for m in msgs:
            who = "Samuel" if m.get("sender") == "human" else "Claude"
            text = message_text(m)
            body_parts.append(text)
            lines.append(f"## {who} — {(m.get('created_at') or '')[:19]}")
            lines.append("")
            lines.append(text)
            lines.append("")

        body = "\n".join(body_parts)
        chars = len(body)
        area, score = match_area(title, body)

        fname = f"{created}-{slugify(title)}.md"
        path = os.path.join(OUT_DIR, fname)
        # Collisions: same title, same day. Suffix rather than overwrite.
        n = 2
        while os.path.exists(path):
            path = os.path.join(OUT_DIR, f"{created}-{slugify(title)}-{n}.md")
            n += 1
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines))

        # Suggestion, not a decision. Samuel trims the CSV.
        title_l = title.lower()
        if chars < 2000 or len(msgs) <= 2:
            suggest, why = "drop", "too short to hold anything durable"
        elif any(h in title_l for h in DROP_HINTS):
            suggest, why = "drop", "title suggests a throwaway"
        elif not area:
            suggest, why = "drop", "no area match"
        elif area in ("study",):
            suggest, why = "drop", "academic coursework, not vault knowledge"
        elif chars > 20000:
            suggest, why = "keep", "large and area-matched"
        else:
            suggest, why = "keep", "area-matched"

        rows.append({
            "keep_or_drop": suggest,
            "title": title,
            "date": created,
            "messages": len(msgs),
            "chars": chars,
            "est_tokens": chars // 4,
            "matched_area": area,
            "match_score": score,
            "why_suggested": why,
            "file": os.path.basename(path),
        })

    rows.sort(key=lambda r: (r["keep_or_drop"], -r["chars"]))
    os.makedirs(os.path.dirname(TRIAGE), exist_ok=True)
    with open(TRIAGE, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    keep = [r for r in rows if r["keep_or_drop"] == "keep"]
    drop = [r for r in rows if r["keep_or_drop"] == "drop"]
    print(f"conversations split : {len(rows)}  -> {OUT_DIR}")
    print(f"triage written      : {TRIAGE}")
    print(f"suggested keep      : {len(keep)}  ({sum(r['est_tokens'] for r in keep):,} est tokens)")
    print(f"suggested drop      : {len(drop)}  ({sum(r['est_tokens'] for r in drop):,} est tokens)")
    print()
    by_area = Counter(r["matched_area"] or "(none)" for r in keep)
    print("kept, by matched area:")
    for a, c in by_area.most_common():
        t = sum(r["est_tokens"] for r in keep if (r["matched_area"] or "(none)") == a)
        print(f"  {a:<16} {c:>3} conversations  {t:>8,} est tokens")


if __name__ == "__main__":
    main()
