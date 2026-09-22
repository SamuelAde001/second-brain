"""Validate the Scripnals guide library, export it for the database, and test the matching rule.

Source of truth: 03-Areas/scripnals/guides/<folder>/<id>.md (Markdown body + a flat frontmatter).
Output: 03-Areas/scripnals/guides/_export/guides.json (one object per entry) and vocab.json
(the allowed tag values with the labels the app shows). Both are generated. Never edit them by hand.

  python 00-System/scripts/build_scripnals_guides.py            validate + export
  python 00-System/scripts/build_scripnals_guides.py --check    validate, and fail if the export is stale
  python 00-System/scripts/build_scripnals_guides.py --select action=rewrite content_type=storytelling \
      tone=friendly audience=creator [--prompt out.txt]
        show which entries one request loads, their word total, and optionally write the {{guides}} text
"""
import argparse, json, pathlib, re, sys

BRAIN = pathlib.Path(__file__).resolve().parents[2]
ROOT = BRAIN / "03-Areas" / "scripnals" / "guides"
EXPORT = ROOT / "_export"

# The controlled vocabulary. Every tag value in an entry must come from here. "any" matches everything.
# These are the database enums and the request values the app sends (spec section 5).
VOCAB = {
    "actions": {
        "review_full": "Review my whole script", "improve_hook": "Improve my hook", "rewrite": "Rewrite my script",
        "shorten": "Shorten my script", "remove_fluff": "Remove fluffs", "draft_from_idea": "Draft a script from my idea",
        "review_idea": "Review my content idea", "to_bullets": "Turn my idea to bullet points",
    },
    "content_types": {
        "storytelling": "Storytelling", "listicle": "Listicles", "quick_tip": "Quick Tip",
        "contrarian": "Contrarian", "before_after": "Before and After", "pov": "POV",
    },
    "tones": {"professional": "Professional", "friendly": "Friendly", "funny": "Funny", "other": "Other"},
    "audiences": {"business": "Business owner/entrepreneur", "creator": "Content creator"},
}
# The request field that each tag field is matched against.
REQUEST_FIELD = {"actions": "action", "content_types": "content_type", "tones": "tone", "audiences": "audience"}
# Kind -> folder, in the order the entries are placed in the prompt.
KINDS = {"core": "core", "audience": "audience", "niche": "niches", "action": "actions",
         "content-type": "content-types", "format": "formats", "tone": "tones", "hook": "hooks", "cta": "ctas"}
MAX_WORDS = {"hook": 35, "cta": 30, "tone": 90}   # body words; others 250. Keep entries terse: every word is sent on every call
BUDGET = 2400          # words of guide text per call, across all loaded entries
REQUIRED = ["id", "kind", "title", "summary", *VOCAB, "priority", "version", "status", "updated", "refs"]
EXPORTED = ["id", "kind", "title", "summary", *VOCAB, "priority", "version", "status", "updated", "refs"]


def parse(path):
    text = path.read_text(encoding="utf8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise ValueError("no frontmatter")
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip() for v in val[1:-1].split(",") if v.strip()]
        meta[key.strip()] = val
    body = m.group(2).strip()
    return meta, body


def load():
    entries, errors = [], []
    for kind, folder in KINDS.items():
        for path in sorted((ROOT / folder).glob("*.md")):
            where = path.relative_to(ROOT).as_posix()
            try:
                meta, body = parse(path)
            except ValueError as e:
                errors.append(f"{where}: {e}"); continue
            for f in REQUIRED:
                if f not in meta:
                    errors.append(f"{where}: missing '{f}'")
            if meta.get("id") != path.stem:
                errors.append(f"{where}: id must equal the file name")
            if meta.get("kind") != kind:
                errors.append(f"{where}: kind '{meta.get('kind')}' but folder is '{folder}'")
            for f, allowed in VOCAB.items():
                vals = meta.get(f, [])
                if not isinstance(vals, list) or not vals:
                    errors.append(f"{where}: '{f}' must be a non-empty [list]"); continue
                bad = [v for v in vals if v != "any" and v not in allowed]
                if bad:
                    errors.append(f"{where}: '{f}' has unknown values {bad}")
            if str(meta.get("priority")) not in {"1", "2", "3"}:
                errors.append(f"{where}: priority must be 1, 2 or 3")
            words = len(body.split())
            if words > MAX_WORDS.get(kind, 250):
                errors.append(f"{where}: body is {words} words, limit {MAX_WORDS.get(kind, 250)}")
            if re.search(r"^#{1,6} |\*\*|`", body, re.M):
                errors.append(f"{where}: body uses Markdown headings, bold or code. Use CAPS labels and '-' lists")
            meta["priority"] = int(meta.get("priority", 3))
            meta["version"] = int(meta.get("version", 1))
            entries.append({**{k: meta.get(k) for k in EXPORTED}, "words": words, "body": body, "_file": where})
    ids = [e["id"] for e in entries]
    errors += [f"duplicate id '{i}'" for i in sorted({i for i in ids if ids.count(i) > 1})]
    for kind in ("hook", "cta"):
        titles = [e["title"] for e in entries if e["kind"] == kind]
        errors += [f"duplicate {kind} title '{t}'" for t in sorted({t for t in titles if titles.count(t) > 1})]
    return entries, errors


def matches(entry, request):
    """An entry loads when every tag field is 'any' or contains the request's value for that field."""
    for f, rf in REQUEST_FIELD.items():
        vals = entry[f]
        if "any" not in vals and request.get(rf) not in vals:
            return False
    return entry["status"] == "active"


def select(entries, request, budget=BUDGET):
    """Matching entries in prompt order. If over budget, drop priority 3, then 2, from the end."""
    order = list(KINDS)
    picked = sorted((e for e in entries if matches(e, request)), key=lambda e: (order.index(e["kind"]), e["id"]))
    dropped = []
    for p in (3, 2):
        while sum(e["words"] for e in picked) > budget and any(e["priority"] == p for e in picked):
            last = max((i for i, e in enumerate(picked) if e["priority"] == p))
            dropped.append(picked.pop(last)["id"])
    return picked, dropped


def guides_text(picked):
    return "\n\n".join(f"GUIDE: {e['title']} ({e['id']})\n{e['body']}" for e in picked)


def export_payload(entries):
    clean = [{k: v for k, v in e.items() if not k.startswith("_")} for e in entries]
    return (json.dumps(clean, ensure_ascii=False, indent=2) + "\n",
            json.dumps({"budget_words": BUDGET, "vocab": VOCAB}, ensure_ascii=False, indent=2) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="fail if the export is out of date")
    ap.add_argument("--select", nargs="*", metavar="field=value", help="simulate one request")
    ap.add_argument("--prompt", type=pathlib.Path, help="with --select: write the {{guides}} text here")
    args = ap.parse_args()

    entries, errors = load()
    if errors:
        print("\n".join(f"ERROR {e}" for e in errors)); sys.exit(1)
    by_kind = {k: sum(1 for e in entries if e["kind"] == k) for k in KINDS}
    print(f"{len(entries)} entries OK | " + " | ".join(f"{k} {n}" for k, n in by_kind.items()))

    if args.select is not None:
        request = dict(kv.split("=", 1) for kv in args.select)
        picked, dropped = select(entries, request)
        for e in picked:
            print(f"  {e['kind']:<13} {e['id']:<32} {e['words']:>4} words")
        print(f"  total {sum(e['words'] for e in picked)} words (budget {BUDGET})"
              + (f" | dropped {dropped}" if dropped else ""))
        if args.prompt:
            args.prompt.write_text(guides_text(picked) + "\n", encoding="utf8")
            print(f"  wrote {args.prompt}")
        return

    guides_json, vocab_json = export_payload(entries)
    targets = {EXPORT / "guides.json": guides_json, EXPORT / "vocab.json": vocab_json}
    if args.check:
        stale = [p.name for p, t in targets.items() if not p.exists() or p.read_text(encoding="utf8") != t]
        if stale:
            print(f"STALE {stale}: run without --check"); sys.exit(1)
        print("export is up to date"); return
    EXPORT.mkdir(exist_ok=True)
    for p, t in targets.items():
        p.write_text(t, encoding="utf8", newline="\n")
    print(f"wrote {', '.join(p.relative_to(BRAIN).as_posix() for p in targets)}")


if __name__ == "__main__":
    main()
