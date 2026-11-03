"""Sort the evidence helpers' findings into one file per rulebook section.

Reads every ev_<group>.md in --work (written by the evidence helpers, headings "## <CODE> <name>", one
"- RULE: ..." line per finding) and writes sec/<CODE>.md, each line prefixed with its group, e.g. "[T4]".
CONFLICTS, VIDEOS SEEN, GAPS and IMAGE CANDIDATES get their own files. Prints rules and size per section.

Usage: python rb_merge.py --work <folder>
"""
import argparse, collections, glob, os, re

CODE = re.compile(r"^##\s+([A-FKX]\d{0,2})\b", re.I)
SPECIAL = ("CONFLICTS", "VIDEOS SEEN", "GAPS", "IMAGE CANDIDATES")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    sec = os.path.join(a.work, "sec")
    os.makedirs(sec, exist_ok=True)
    buckets = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(a.work, "ev_*.md"))):
        grp, cur = os.path.basename(f)[3:-3], "X"
        for line in open(f, encoding="utf-8", errors="replace"):
            s = line.rstrip("\n")
            if s.startswith("## "):
                h = s[3:].strip().upper()
                sp = next((k for k in SPECIAL if h.startswith(k)), None)
                m = CODE.match(s)
                cur = sp or (m.group(1).upper() if m else "X")
            elif s.strip() and not s.startswith("# "):
                buckets[cur].append(f"[{grp}] {s}")
    for k, lines in buckets.items():
        open(os.path.join(sec, k.replace(" ", "_") + ".md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    for k in sorted(buckets, key=lambda x: (len(x) > 3, x)):
        print(f"{k:18} {sum('RULE:' in l for l in buckets[k]):4} rules  {sum(map(len, buckets[k])):7} chars")


if __name__ == "__main__":
    main()
