"""rb_issues.py - gather every open issue in the editing rulebook into one note Samuel can answer in one go.

Usage:  python rb_issues.py [--out <path>]   (default: 03-Areas/video-editing/rulebook/rulebook-open-issues.md)

An "issue" is:
  1. a question (- **Q-XX.x** ...) with no "-> Samuel:" answer yet, and
  2. a rule still waiting for review that is the Editor's own inference (marked with the bulb badge) -
     the only rules not backed by Samuel's words or his finals.
Sections are listed client overlays first (K3 Gamma, K0-K4), then book order, so the Gamma job's issues come first.
Built 2026-11-05 at Samuel's request: "Get me where all the issues are so I answer them and finalise this rule book".
Only reads the rulebook; writes the one output note.
"""
import argparse, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.normpath(os.path.join(HERE, "..", "..", "rulebook"))
MARK = re.compile(r"· [✔✏✖] 20\d\d-\d\d-\d\d")
RULE = re.compile(r"^- \*\*([A-K]\d+\.\d+)\*\*")
QN = re.compile(r"^- \*\*(Q-[A-K]\d+\.[a-z])\*\*")
ORDER = ["k3", "k0", "k1", "k2", "k4", "a1", "a2", "a3", "a4", "a5", "a6", "b1", "b2", "b3", "b4", "b5"] + \
        ["c%d" % i for i in range(1, 17)] + ["d1", "d2", "e1", "e2", "f1", "f2", "f3", "f4", "f5"]


def title(text):
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RB, "rulebook-open-issues.md"))
    a = ap.parse_args()
    files = {f.split("-")[1]: f for f in os.listdir(RB) if f.startswith("rb-") and f.split("-")[1] in ORDER}
    blocks, nq, nr, nw = [], 0, 0, 0
    for code in ORDER:
        f = files.get(code)
        if not f:
            continue
        s = io.open(os.path.join(RB, f), encoding="utf-8").read()
        qs, rs = [], []
        for line in s.splitlines():
            if QN.match(line) and "→ Samuel:" not in line:
                qs.append(line)
            elif RULE.match(line) and not MARK.search(line):
                nw += 1
                if "💡" in line.replace("carries 💡", ""):
                    rs.append(line)
        if not (qs or rs):
            continue
        nq += len(qs)
        nr += len(rs)
        link = "[[03-Areas/video-editing/rulebook/%s|%s]]" % (f[:-3], title(s))
        out = ["## %s" % link, ""]
        if qs:
            out += ["**Questions**"] + [q + "\n  - **Answer:** " for q in qs] + [""]
        if rs:
            out += ["**My inferences (keep, change or drop)**"] + [r + "\n  - **Answer:** " for r in rs] + [""]
        blocks.append("\n".join(out))
    head = ("---\ntype: sop\narea: video-editing\nstatus: needs-input\nupdated: 2026-11-05\nsource: manual\n"
            "tags: [rulebook, review]\n---\n\n# Rulebook open issues\n\n"
            "Every open issue in the [[03-Areas/video-editing/rulebook/rulebook|rulebook]], in one place "
            "(Samuel, 2026-11-05: *\"Get me where all the issues are so I answer them and finalise this rule book\"*). "
            "Made by `rb_issues.py`. **%d questions** and **%d rules that are only my inference** (💡). "
            "Gamma (K3) and the other client overlays come first.\n\n"
            "**The other %d waiting rules** come from your own words or your finals. Once these issues are answered, "
            "say *approve the rest* and they all get ✔ in one go; anything you correct later comes in as a revision and is written back.\n\n"
            "**How to answer:** in chat, e.g. `Q-K3.a 1`, `C2.14 drop`, `rest yes`, or type after **Answer:** here in Obsidian.\n\n"
            % (nq, nr, nw - nr))
    io.open(a.out, "w", encoding="utf-8", newline="\n").write(head + "\n".join(blocks) +
                                                           "\nBack to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]\n")
    print("questions %d, inferred rules %d -> %s" % (nq, nr, a.out))


if __name__ == "__main__":
    main()
