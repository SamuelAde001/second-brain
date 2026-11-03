"""Bucket every evidence line from ev_*.md into one file per section code."""
import glob, re, os, collections

here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, "sec"), exist_ok=True)
code_re = re.compile(r"^##\s+([A-FKX]\d{0,2})\b", re.I)
special = {"CONFLICTS", "VIDEOS SEEN", "GAPS", "IMAGE CANDIDATES"}
buckets = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(here, "ev_*.md"))):
    grp = os.path.basename(f)[3:-3]
    cur = "X"
    for line in open(f, encoding="utf-8", errors="replace"):
        s = line.rstrip("\n")
        if s.startswith("## "):
            h = s[3:].strip().upper()
            sp = next((k for k in special if h.startswith(k)), None)
            m = code_re.match(s)
            cur = sp if sp else (m.group(1).upper() if m else "X")
            continue
        if s.strip() and not s.startswith("# "):
            buckets[cur].append(f"[{grp}] {s}")
for k, lines in buckets.items():
    name = k.replace(" ", "_")
    with open(os.path.join(here, "sec", f"{name}.md"), "w", encoding="utf-8") as o:
        o.write("\n".join(lines) + "\n")
for k in sorted(buckets, key=lambda x: (len(x) > 3, x)):
    n = sum(1 for l in buckets[k] if "RULE:" in l)
    print(f"{k:18} {n:4} rules  {sum(map(len, buckets[k])):7} chars")
