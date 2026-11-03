"""Where Samuel's rule-by-rule review stands: rules approved, corrected, dismissed and still waiting, per section.

A decided rule carries its mark at the end of its line (written by the Editor when Samuel answers):
  ✔ YYYY-MM-DD   approved as written
  ✏ YYYY-MM-DD   corrected (the line holds his new wording)
  ✖ YYYY-MM-DD   dismissed (moved to 08-Archive/brain-build/rulebook-removed-rules.md and counted from there)
Open questions are counted until they carry "→ Samuel:".

Usage: python rb_status.py [--section A1] [--pending]   (--pending lists the undecided rule numbers)
"""
import argparse, glob, os, re

RB = r"C:/Users/repzy/Desktop/My Second brain/03-Areas/video-editing/rulebook/"
ARCH = r"C:/Users/repzy/Desktop/My Second brain/08-Archive/brain-build/rulebook-removed-rules.md"
RULE = re.compile(r"^\s*- (?:~~)?\*\*([A-K]\d{1,2}\.\d+)\*\*")
QUES = re.compile(r"^\s*- \*\*(Q-[A-K]\d{1,2}\.[a-z])\*\*")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section")
    ap.add_argument("--pending", action="store_true")
    a = ap.parse_args()
    tot = [0] * 6
    try:
        arch = open(ARCH, encoding="utf-8").read().splitlines()
    except OSError:
        arch = []
    for f in sorted(glob.glob(RB + "rb-*.md"), key=lambda p: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p)]):
        code = re.match(r"rb-([a-z]\d*)", os.path.basename(f)).group(1).upper()
        if a.section and code != a.section.upper():
            continue
        n = [0] * 6
        pend, qpend = [], []
        for line in open(f, encoding="utf-8"):
            m, q = RULE.match(line), QUES.match(line)
            if m:
                n[0] += 1
                k = 1 if "\u2714 20" in line else 2 if "\u270f 20" in line else 3 if "\u2716 20" in line else 0
                if k:
                    n[k] += 1
                else:
                    pend.append(m.group(1))
            elif q:
                n[4] += 1
                if "\u2192 Samuel:" in line:
                    n[5] += 1
                else:
                    qpend.append(q.group(1))
        gone = sum(1 for l in arch if l.startswith(f"- [{code}]") and "\u2716 20" in l)
        n[0] += gone
        n[3] += gone
        if not n[0] and not n[4]:
            continue
        tot = [x + y for x, y in zip(tot, n)]
        left = n[0] - sum(n[1:4])
        print(f"{code:4} rules {n[0]:3}  approved {n[1]:3}  corrected {n[2]:3}  dismissed {n[3]:3}  waiting {left:3}   questions {n[5]}/{n[4]} answered")
        if a.pending and (pend or qpend):
            print("     waiting:", " ".join(pend + qpend))
    print(f"ALL  rules {tot[0]}  approved {tot[1]}  corrected {tot[2]}  dismissed {tot[3]}  "
          f"waiting {tot[0] - sum(tot[1:4])}   questions {tot[5]}/{tot[4]} answered")


if __name__ == "__main__":
    main()
