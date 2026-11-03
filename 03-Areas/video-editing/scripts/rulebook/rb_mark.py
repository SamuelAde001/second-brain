"""Mark rulebook rules approved or dismissed after Samuel's answer, and log it in the changelog.

  --approve A1.16-A1.24 A2.3     adds " · ✔ <date>" to each rule line
  --dismiss A1.5                 marks the rule " · ✖ <date>" struck through, then rb_prune.py moves it out of the rulebook
                                 into the removed-rules archive (Samuel, 2026-11-03: replaced and dismissed rules leave the book)
Ranges stay inside one section. Rules already marked are skipped. Corrections (✏) are not done here:
the Editor writes his new wording by hand, then adds " · ✏ <date>".
One changelog line per run: date · numbers · ✔ approved / ✖ dismissed.

Usage: python rb_mark.py --approve A1.16-A1.24 [--dismiss A1.5] [--date 2026-11-03]
"""
import argparse, datetime, glob, io, re

RB = r"C:/Users/repzy/Desktop/My Second brain/03-Areas/video-editing/rulebook/"
LOG = RB + "rulebook-changelog.md"
BACK = "\n\nBack to [[03-Areas/video-editing/rulebook/rulebook|Rulebook]]"


def expand(items):
    out = []
    for it in items:
        m = re.fullmatch(r"([A-K]\d{1,2})\.(\d+)(?:-(?:[A-K]\d{1,2}\.)?(\d+))?", it.upper())
        if not m:
            raise SystemExit(f"bad rule number: {it}")
        lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
        out += [f"{m.group(1)}.{n}" for n in range(lo, hi + 1)]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--approve", nargs="*", default=[])
    ap.add_argument("--dismiss", nargs="*", default=[])
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    todo = [(c, "\u2714") for c in expand(a.approve)] + [(c, "\u2716") for c in expand(a.dismiss)]
    files = {re.match(r"rb-([a-z]\d*)", f.replace("\\", "/").split("/")[-1]).group(1).upper(): f
             for f in glob.glob(RB + "rb-*.md") if re.match(r"rb-[a-z]\d", f.replace("\\", "/").split("/")[-1])}
    done = {"\u2714": [], "\u2716": []}
    for code, sym in todo:
        f = files.get(code.split(".")[0])
        if not f:
            print("no section for", code)
            continue
        s = io.open(f, encoding="utf-8").read()
        m = re.search(r"^- \*\*" + re.escape(code) + r"\*\*(.*)$", s, re.M)
        if not m:
            print("not found:", code)
            continue
        if re.search("[\u2714\u270f\u2716] 20", m.group(0)):
            print("already decided:", code)
            continue
        line = (f"- ~~**{code}**{m.group(1)}~~" if sym == "\u2716" else m.group(0)) + f" · {sym} {a.date}"
        io.open(f, "w", encoding="utf-8", newline="").write(s[:m.start()] + line + s[m.end():])
        done[sym].append(code)
    entries = [f"- {a.date} · {' '.join(v)} · {sym} {'approved' if sym == chr(0x2714) else 'dismissed'}."
               for sym, v in done.items() if v]
    if entries:
        s = io.open(LOG, encoding="utf-8").read()
        s = s.replace(BACK, "\n" + "\n".join(entries) + BACK) if BACK in s else s + "\n" + "\n".join(entries) + "\n"
        io.open(LOG, "w", encoding="utf-8", newline="").write(s)
    if done["\u2716"]:
        import os, subprocess, sys
        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "rb_prune.py"), "--date", a.date])
    print("approved:", " ".join(done["\u2714"]) or "-", "| dismissed:", " ".join(done["\u2716"]) or "-")


if __name__ == "__main__":
    main()
