"""Take every replaced or dismissed rule out of the rulebook and keep it, word for word, in the removed-rules archive.

Samuel, 2026-11-03: *"The replaced rules should be replaced and removed from the rule book"*. The rulebook holds only
rules in force; what was removed goes to 08-Archive/brain-build/rulebook-removed-rules.md, one line per rule with its
section and the date, so nothing is lost and no agent reads it by accident. Rule numbers are never reused.

Removed: struck-through rule lines ("- ~~**A1.5** ...~~ · ✖ date", "- **A3.41** ~~...~~ → ..."), "Superseded:" lines,
and whole "Superseded" subsections. Lines in "Questions for Samuel" are left alone.

Usage: python rb_prune.py [--dry-run] [--date YYYY-MM-DD]
"""
import argparse, datetime, glob, io, os, re

BRAIN = r"C:/Users/repzy/Desktop/My Second brain/"
RB = BRAIN + "03-Areas/video-editing/rulebook/"
ARCH = BRAIN + "08-Archive/brain-build/rulebook-removed-rules.md"
HEAD = """---
type: log
area: video-editing
status: active
updated: {d}
source: manual
tags: [rulebook, archive]
---

# Rulebook: removed rules

Rules taken out of the [[03-Areas/video-editing/rulebook/rulebook|rulebook]] because Samuel dismissed them or a newer rule replaced them. Kept word for word for the record; **not in force, agents do not follow these.** Append-only, newest at the bottom. Written by `03-Areas/video-editing/scripts/rulebook/rb_prune.py`.
"""
STRUCK = re.compile(r"^\s*- (~~\*\*[A-K]\d{1,2}\.\d+\*\*|\*\*[A-K]\d{1,2}\.\d+\*\* ~~|~~)")
SUPER_LINE = re.compile(r"^\s*- \*?Superseded:?\*?:?", re.I)
SUPER_HEAD = re.compile(r"^#{2,3} Superseded", re.I)


def prune(text):
    out, removed, in_super, in_q = [], [], False, False
    for line in text.splitlines(keepends=True):
        if line.startswith("#"):
            in_q = line.startswith("## Questions")
            in_super = bool(SUPER_HEAD.match(line))
            if in_super:
                continue
        if in_super:
            if line.strip():
                removed.append(line.rstrip("\n"))
            continue
        if not in_q and (STRUCK.match(line) or SUPER_LINE.match(line)):
            removed.append(line.rstrip("\n"))
            continue
        out.append(line)
    return re.sub(r"\n{3,}", "\n\n", "".join(out)), removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    lines = []
    for f in sorted(glob.glob(RB + "rb-*.md")):
        code = re.match(r"rb-([a-z]\d*)", os.path.basename(f)).group(1).upper()
        s = io.open(f, encoding="utf-8").read()
        new, removed = prune(s)
        if not removed:
            continue
        print(f"{code:4} {len(removed)} removed")
        lines += [f"- [{code}] {r.strip()[2:] if r.strip().startswith('- ') else r.strip()} · removed {a.date}" for r in removed]
        if not a.dry_run:
            io.open(f, "w", encoding="utf-8", newline="").write(new)
    if lines and not a.dry_run:
        body = io.open(ARCH, encoding="utf-8").read() if os.path.exists(ARCH) else HEAD.format(d=a.date)
        body = body.rstrip("\n") + f"\n\n## {a.date}\n" + "\n".join(lines) + "\n"
        io.open(ARCH, "w", encoding="utf-8", newline="").write(body)
    print(len(lines), "lines", "(dry run)" if a.dry_run else "-> " + ARCH)


if __name__ == "__main__":
    main()
