import json, glob, os, re, sys
src = r"C:/Users/repzy/.claude/projects/C--Users-repzy-Desktop-My-Second-brain"
out = []
seen = set()
for f in glob.glob(src + "/*.jsonl"):
    sid = os.path.basename(f)[:8]
    with open(f, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try: d = json.loads(line)
            except: continue
            if d.get("type") != "user" or d.get("isMeta") or d.get("isSidechain"): continue
            if d.get("isCompactSummary"): continue
            c = d.get("message", {}).get("content")
            texts = []
            if isinstance(c, str): texts = [c]
            elif isinstance(c, list):
                texts = [b.get("text","") for b in c if isinstance(b, dict) and b.get("type") == "text"]
            t = "\n".join(texts)
            t = re.sub(r"<system-reminder>.*?</system-reminder>", "", t, flags=re.S)
            t = re.sub(r"<(command-[a-z-]+|local-command-[a-z]+|task-notification|side-sessions-event|ci-monitor-event)>.*?</\1>", "", t, flags=re.S)
            t = t.strip()
            if not t or t.startswith("This session is being continued") or t.startswith("[Request interrupted"): continue
            if t.startswith("Caveat:"): continue
            key = t[:300]
            if key in seen: continue
            seen.add(key)
            out.append((d.get("timestamp",""), sid, t))
out.sort()
with open("samuel_all.md", "w", encoding="utf-8") as o:
    for ts, sid, t in out:
        o.write(f"\n### {ts[:16]} {sid}\n{t}\n")
print(len(out), os.path.getsize("samuel_all.md"))
