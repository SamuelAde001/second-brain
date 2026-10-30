"""Where did the Claude usage go? Token audit of this Brain's Claude Code transcripts.

Reads the transcripts in %USERPROFILE%\\.claude\\projects\\C--Users-repzy-Desktop-My-Second-brain\\
(main sessions, Agent helpers, workflow helpers) and prints a short summary only:
cost by kind, what the cost is made of, helper start-up weight, cache lost to long
waits, images, and the costliest sessions with their first line.

Cost is in USD at API prices (the best proxy for the usage card; Anthropic doesn't
publish the weighting): Opus 5.5 in 4 / cache write 5 / cache read 0.2 / out 20 per 1M; Sonnet 5.5
2 / 2.5 / 0.2 / 10 (cache reads cost the same on both; claude-api reference, 2026-10-28). Helpers run on a 5-minute cache, main sessions on a 1-hour one (checked
2026-10-24), so a helper tool call that takes over 5 minutes rewrites its whole context.

Usage:
    python 00-System/scripts/usage_audit.py                  # last 7 days
    python 00-System/scripts/usage_audit.py --since 2026-10-19
    python 00-System/scripts/usage_audit.py --session 1162acdc   # one session + its helpers
    python 00-System/scripts/usage_audit.py --session fd121072 --split   # + cost per workflow, phase, helper type

Rule this feeds: 00-System/model-routing.md -> On Max 20x.
"""
import argparse
import collections
import datetime
import glob
import json
import os
import re

ROOT = os.path.expanduser(r"~/.claude/projects/C--Users-repzy-Desktop-My-Second-brain")
PRICE = {"opus": (4, 5, 0.2, 20), "sonnet": (2, 2.5, 0.2, 10), "haiku": (0.1, 0.125, 0.01, 0.5)}
GAP = 300  # seconds: the helpers' cache lifetime


def fam(model):
    m = (model or "").lower()
    return next((k for k in PRICE if k in m), "opus")


def when(d):
    try:
        return datetime.datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00")).timestamp()
    except (KeyError, ValueError, AttributeError):
        return None


def first_line(content):
    if isinstance(content, list):
        content = " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    if not isinstance(content, str):
        return ""
    return re.sub(r"<[^>]+>.*?</[^>]+>", "", content, flags=re.S).strip().replace("\n", " ")[:90]


def scan(path):
    r = dict(cost=0.0, turns=0, first_ctx=0, cw=0, cr=0, out=0, lost=0, images=0, sonnet=0, topic="",
             c_cr=0.0, c_cw=0.0, c_out=0.0, c_lost=0.0, c_sonnet=0.0)
    seen, last_t = set(), None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message") or {}
            if d.get("type") == "user":
                c = m.get("content")
                if not r["topic"]:
                    r["topic"] = first_line(c)
                if isinstance(c, list):
                    for b in c:
                        if isinstance(b, dict) and b.get("type") == "tool_result" and isinstance(b.get("content"), list):
                            r["images"] += sum(1 for x in b["content"] if isinstance(x, dict) and x.get("type") == "image")
                continue
            u = m.get("usage")
            if d.get("type") != "assistant" or not u or m.get("id") in seen:
                continue
            seen.add(m.get("id"))
            p = PRICE[fam(m.get("model"))]
            i, cw = u.get("input_tokens") or 0, u.get("cache_creation_input_tokens") or 0
            cr, o = u.get("cache_read_input_tokens") or 0, u.get("output_tokens") or 0
            r["cost"] += (i * p[0] + cw * p[1] + cr * p[2] + o * p[3]) / 1e6
            r["cw"] += cw; r["cr"] += cr; r["out"] += o
            r["c_cw"] += cw * p[1] / 1e6; r["c_cr"] += cr * p[2] / 1e6; r["c_out"] += o * p[3] / 1e6
            if fam(m.get("model")) == "sonnet":
                r["sonnet"] += 1
                r["c_sonnet"] += (i * p[0] + cw * p[1] + cr * p[2] + o * p[3]) / 1e6
            t = when(d)
            if r["turns"] == 0:
                r["first_ctx"] = i + cw + cr
            elif cw > 30_000 and last_t and t and t - last_t > GAP:
                r["lost"] += cw
                r["c_lost"] += cw * p[1] / 1e6
            r["turns"] += 1
            last_t = t or last_t
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD (default: 7 days ago)")
    ap.add_argument("--session", help="first characters of a main session id")
    ap.add_argument("--split", action="store_true", help="cost per workflow, per phase and per helper type")
    a = ap.parse_args()
    since = (datetime.datetime.fromisoformat(a.since) if a.since
             else datetime.datetime.now() - datetime.timedelta(days=7)).timestamp()
    groups = collections.defaultdict(list)
    for path in glob.glob(os.path.join(ROOT, "**", "*.jsonl"), recursive=True):
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if a.session and not rel.startswith(a.session):
            continue
        if not a.session and os.path.getmtime(path) < since:
            continue
        kind = "workflow helpers" if "/workflows/" in rel else "agent helpers" if "/subagents/" in rel else "main sessions"
        r = scan(path)
        r["rel"] = rel
        r["wf"] = rel.split("/workflows/")[1].split("/")[0] if "/workflows/" in rel else ""
        try:
            with open(path[:-6] + ".meta.json", encoding="utf-8") as f:
                meta = json.load(f)
        except (OSError, ValueError):
            meta = {}
        r["phase"] = meta.get("workflowPhase") or "-"
        r["type"] = meta.get("agentType") or "-"
        if r["turns"]:
            groups[kind].append(r)
    total = sum(r["cost"] for rs in groups.values() for r in rs) or 1
    print(f"Total: {total:,.0f} cost units (USD at API prices)")
    for kind, rs in sorted(groups.items()):
        c = sum(r["cost"] for r in rs)
        cr = sum(r["c_cr"] for r in rs)
        cw = sum(r["c_cw"] for r in rs)
        out = sum(r["c_out"] for r in rs)
        lost = sum(r["c_lost"] for r in rs)
        turns = sum(r["turns"] for r in rs)
        print(f"\n{kind}: {len(rs)}, {turns} turns, {c:,.0f} ({c / total:.0%})"
              f"  | re-reading context {cr:,.0f} · writing cache {cw:,.0f} · output {out:,.0f}"
              f"  | Sonnet turns {sum(r['sonnet'] for r in rs)}  | images read {sum(r['images'] for r in rs)}")
        if kind != "main sessions":
            starts = sorted(r["first_ctx"] for r in rs)
            start_cost = sum(r["turns"] * r["first_ctx"] for r in rs) * 0.2 / 1e6
            print(f"  start-up context median {starts[len(starts) // 2]:,} tokens, re-read every turn: ~{start_cost:,.0f} ({start_cost / c:.0%})")
            print(f"  cache rewritten after a wait over 5 min: ~{lost:,.0f} ({lost / c:.0%})")
    if a.split:
        hs = [r for k, rs in groups.items() if k != "main sessions" for r in rs]
        for title, key in (("workflow", "wf"), ("phase", "phase"), ("helper type", "type")):
            agg = collections.defaultdict(lambda: [0.0, 0, 0, 0, 0.0])
            for r in hs:
                g = agg[r[key] or "(agent helper)"]
                g[0] += r["cost"]; g[1] += 1; g[2] += r["turns"]; g[3] += r["sonnet"]; g[4] += r["c_sonnet"]
            print(f"\nBy {title} (cost, % of all, helpers, turns, Sonnet share of turns / of cost):")
            for name, (c, n, t, sn, cs) in sorted(agg.items(), key=lambda x: -x[1][0])[:25]:
                print(f"  {name[:28]:28} {c:7,.0f} {c / total:4.0%} {n:4} {t:6}  S {sn / max(t, 1):4.0%} / {cs / max(c, 1e-9):4.0%}")
    mains = sorted(groups.get("main sessions", []), key=lambda r: -r["cost"])[:10]
    if mains:
        print("\nCostliest main sessions (own cost + helpers):")
        helpers = [r for k, rs in groups.items() if k != "main sessions" for r in rs]
        for r in mains:
            sid = r["rel"][:-6]
            h = sum(x["cost"] for x in helpers if x["rel"].startswith(sid + "/"))
            print(f"  {sid[:8]} {r['cost']:6,.0f} + {h:6,.0f}  {r['topic']}")


if __name__ == "__main__":
    main()
