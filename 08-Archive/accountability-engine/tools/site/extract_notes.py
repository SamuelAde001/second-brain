#!/usr/bin/env python3
"""One-time migration: lift static prose out of the page scripts into context/site.json.

Samuel's rule, 2026-09-02: "Nothing should be hard coded... it should just be an
update to the data and the frontend reads from the data."

The callouts and chart notes on every page were written as JavaScript string
literals. That meant changing a sentence -- a figure that moved, a rule that died --
required editing code. This lifts every STATIC one into `site.json` under `notes`,
keyed by page and id, and rewrites the call site to `notesFor('<page>', '<id>')`.

Calls that interpolate live values are LEFT WHERE THEY ARE. They are not hardcoded
facts; they are templates over data, and moving them would break them. The run
prints how many of each.

Re-running is safe: already-migrated call sites no longer match.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PAGES = REPO / "site" / "assets" / "js" / "pages"
SITE = REPO / "context" / "site.json"

OPENERS = "([{"
CLOSERS = ")]}"
QUOTES = "'\"`"
BACKSLASH = chr(92)


def split_args(src):
    """Split a call's argument list on top-level commas, respecting nesting."""
    args, depth, buf, i, quote = [], 0, [], 0, None
    while i < len(src):
        ch = src[i]
        if quote:
            buf.append(ch)
            if ch == BACKSLASH and i + 1 < len(src):
                buf.append(src[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in QUOTES:
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if ch in OPENERS:
            depth += 1
        elif ch in CLOSERS:
            depth -= 1
        if ch == "," and depth == 0:
            args.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    if "".join(buf).strip():
        args.append("".join(buf))
    return [a.strip() for a in args]


def read_literal(expr):
    """If expr is exactly one quoted JS string, return its value; else None."""
    expr = expr.strip()
    if len(expr) < 2 or expr[0] not in "'\"" or expr[-1] != expr[0]:
        return None
    quote = expr[0]
    body, i, out = expr[1:-1], 0, []
    while i < len(body):
        ch = body[i]
        if ch == quote:
            return None  # unescaped closing quote inside: not a single literal
        if ch == BACKSLASH and i + 1 < len(body):
            nxt = body[i + 1]
            if nxt in ("n", "t"):
                out.append("\n" if nxt == "n" else "\t")
            elif nxt == "u":
                # keep JS unicode escapes verbatim; they render fine as text
                out.append(body[i:i + 2])
            else:
                out.append(nxt)
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def static_string(expr):
    """Return the string if expr is a literal or a chain of literals joined by +."""
    parts, buf, depth, quote, i = [], [], 0, None, 0
    while i < len(expr):
        ch = expr[i]
        if quote:
            buf.append(ch)
            if ch == BACKSLASH and i + 1 < len(expr):
                buf.append(expr[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in QUOTES:
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if ch in OPENERS:
            depth += 1
        elif ch in CLOSERS:
            depth -= 1
        if ch == "+" and depth == 0:
            parts.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    parts.append("".join(buf))

    out = []
    for part in parts:
        value = read_literal(part)
        if value is None:
            return None
        out.append(value)
    return "".join(out)


def find_calls(text):
    """Yield (start, end, name, args) for every callout( / note( call."""
    for m in re.finditer(r"\b(callout|note)\(", text):
        i = m.end() - 1
        depth, quote = 0, None
        while i < len(text):
            ch = text[i]
            if quote:
                if ch == BACKSLASH:
                    i += 2
                    continue
                if ch == quote:
                    quote = None
                i += 1
                continue
            if ch in QUOTES:
                quote = ch
                i += 1
                continue
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    yield m.start(), i + 1, m.group(1), split_args(text[m.end():i])
                    break
            i += 1


def main():
    site = json.loads(SITE.read_text(encoding="utf-8"))
    notes = site.setdefault("notes", {})
    moved = left = 0

    for path in sorted(PAGES.glob("*.js")):
        page = path.stem
        text = path.read_text(encoding="utf-8")
        page_notes, edits = {}, []

        for start, end, name, args in find_calls(text):
            entry = None
            if name == "callout" and len(args) >= 3:
                kind = static_string(args[0])
                icon = static_string(args[1])
                paras = [static_string(a) for a in args[2:]]
                if kind is not None and icon is not None and all(p is not None for p in paras):
                    entry = {"type": "callout", "kind": kind, "icon": icon, "paras": paras}
            elif name == "note" and len(args) == 1:
                body = static_string(args[0])
                if body is not None:
                    entry = {"type": "note", "html": body}

            if entry is None:
                left += 1
                continue

            nid = "n%d" % (len(page_notes) + 1)
            page_notes[nid] = entry
            edits.append((start, end, "notesFor('%s', '%s')" % (page, nid)))
            moved += 1

        if not edits:
            continue
        for start, end, repl in sorted(edits, key=lambda e: -e[0]):
            text = text[:start] + repl + text[end:]
        path.write_text(text, encoding="utf-8")
        notes[page] = page_notes
        print("  %-16s moved %d" % (path.name, len(page_notes)))

    SITE.write_text(json.dumps(site, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nmoved %d into context/site.json - left %d in code (they read live data)"
          % (moved, left))


if __name__ == "__main__":
    main()
