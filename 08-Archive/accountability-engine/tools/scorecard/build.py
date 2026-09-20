#!/usr/bin/env python3
"""Build scorecard.html from a small JSON day-file plus the frozen template.

The reckoning writes ONLY context/scorecard-day.json (~30 lines) and runs this.
Nothing in this repo should ever read or rewrite scorecard.html by hand — the
whole point is that the expensive 450-line file is generated, not typed.

    python tools/scorecard/build.py

Then publish scorecard.html to the FIXED artifact URL in the reckon skill.
"""
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DAY = ROOT / "context" / "scorecard-day.json"
TEMPLATE = ROOT / "tools" / "scorecard" / "template.html"
OUT = ROOT / "scorecard.html"

NAIRA = "&#8358;"


def esc(text):
    """Escape, then allow the handful of typographic entities the card uses."""
    out = html.escape(str(text), quote=False)
    for src, ent in (
        ("₦", NAIRA), ("·", "&middot;"), ("—", "&mdash;"),
        ("–", "&ndash;"), ("→", "&rarr;"), ("“", "&ldquo;"),
        ("”", "&rdquo;"), ("’", "&rsquo;"),
    ):
        out = out.replace(src, ent)
    return out


def rows(items):
    """A list of {what, detail, state, tag} -> the .row markup."""
    out = []
    for it in items:
        state = it.get("state", "null")
        tag = it.get("tag") or state.title()
        detail = f'\n          <span>{esc(it["detail"])}</span>' if it.get("detail") else ""
        out.append(
            f'      <div class="row is-{state}">\n'
            f'        <div class="what">\n'
            f'          <b>{esc(it["what"])}</b>{detail}\n'
            f'        </div>\n'
            f'        <span class="tag t-{state}">{esc(tag)}</span>\n'
            f'      </div>'
        )
    return "\n".join(out)


def section(title, items):
    if not items:
        return ""
    return (
        f'\n  <section>\n    <h2>{esc(title)}</h2>\n'
        f'    <div class="rows">\n{rows(items)}\n    </div>\n  </section>\n'
    )


def build(day):
    p = []
    p.append('<div class="card">\n')

    p.append('  <div class="band">\n'
             '    <span class="mark">Reckoning Scorecard</span>\n'
             f'    <span class="date">{esc(day["date"])}</span>\n')
    if day.get("sub"):
        p.append(f'    <span class="sub">{esc(day["sub"])}</span>\n')
    p.append('  </div>\n')

    score = esc(day.get("score", "0"))
    of = esc(day.get("score_of", ""))
    small = f'<small>{of}</small>' if of else ""
    p.append('\n  <div class="verdict">\n'
             f'    <div class="score">{score}{small}</div>\n'
             '    <div class="verdict-meta">\n'
             f'      <span class="stamp {day.get("verdict_class", "open")}">'
             f'{esc(day.get("verdict", "Open"))}</span>\n')
    for line in day.get("ratios", []):
        p.append(f'      <span class="ratio">{esc(line)}</span>\n')
    p.append('    </div>\n  </div>\n')

    p.append(section(day.get("committed_title", "Committed today"), day.get("committed", [])))

    habits = day.get("habits", [])
    if habits:
        hit = sum(1 for h in habits if h.get("state") == "pass")
        p.append(f'\n  <section>\n    <h2>Habits &mdash; {hit} of {len(habits)}</h2>\n'
                 '    <div class="habits">\n')
        for h in habits:
            p.append(f'      <span class="habit h-{h.get("state", "null")}">'
                     f'<span class="dot"></span>{esc(h["name"])}</span>\n')
        p.append('    </div>\n  </section>\n')

    p.append(section(day.get("red_title", "Red marks"), day.get("red", [])))

    cells = day.get("cells", [])
    if cells:
        p.append('\n  <div class="grid">\n')
        for c in cells:
            vclass = f' {c["vclass"]}' if c.get("vclass") else ""
            note = f'\n      <div class="n">{esc(c["n"])}</div>' if c.get("n") else ""
            p.append(f'    <div class="cell">\n'
                     f'      <div class="k">{esc(c["k"])}</div>\n'
                     f'      <div class="v{vclass}">{esc(c["v"])}</div>{note}\n'
                     f'    </div>\n')
        p.append('  </div>\n')

    p.append('\n  <div class="foot">\n')
    if day.get("quote"):
        p.append(f'    <p class="rule-quote"><em>From stakes.md:</em> '
                 f'{esc(day["quote"])}</p>\n')
    p.append('    <div class="send">Screenshot this &mdash; send it &mdash; every night</div>\n'
             '  </div>\n\n</div>\n')

    p.append('\n<p class="note">\n'
             '  This is the card the evening reckoning builds. It goes to the same link every\n'
             '  night, so the bookmark never changes. Nothing on it is assumed &mdash; every line\n'
             '  was confirmed out loud at the 9pm reckoning, and a red mark stays red on a day\n'
             '  that went well.\n</p>\n')
    return "".join(p)


def main():
    if not DAY.exists():
        sys.exit(f"no day file at {DAY} — write it first, then rerun")
    day = json.loads(DAY.read_text(encoding="utf-8"))
    for required in ("date", "verdict"):
        if not day.get(required):
            sys.exit(f'scorecard-day.json is missing "{required}"')
    page = TEMPLATE.read_text(encoding="utf-8").replace("<!--__BODY__-->", build(day))
    OUT.write_text(page, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.name} ({len(page)} bytes) for {day['date']} — {day['verdict']}")


if __name__ == "__main__":
    main()
