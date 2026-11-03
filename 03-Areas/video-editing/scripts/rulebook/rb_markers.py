"""Collect every marker note Samuel left on our timelines from the marker dumps in the Route Rise job folders.

Reads every JSON under <job>\\Docs\\ whose file name contains "marker" (the dumps the Editor makes at each
revision round) and writes one markdown list: colour, note, the spoken words under it, the beat ids.
Lip-sync check markers are skipped. Duplicates inside one job are dropped.

Usage: python rb_markers.py --out <folder>\\markers_all.md [--root "C:\\Users\\repzy\\Desktop\\Video edits\\Routerise"]
Read-only on the job folders.
"""
import argparse, glob, json, os

SKIP = {"Lip-sync check", "Eyeball lip sync here"}


def walk(o, job, seen, out):
    if isinstance(o, dict):
        txt = " | ".join(x for x in [o.get("name") or "", o.get("note") or o.get("text") or ""] if x and x not in SKIP)
        if txt and "color" in o and (job, txt[:200]) not in seen:
            seen.add((job, txt[:200]))
            beats = ",".join(sorted({u.get("beat", "") for u in o.get("under", []) if isinstance(u, dict) and u.get("beat")}))
            words = o.get("words", "")
            out.append(f"- [{o.get('color')}] {txt}" + (f'  — says: "{words}"' if words else "") + (f"  (beat {beats})" if beats else ""))
        for v in o.values():
            walk(v, job, seen, out)
    elif isinstance(o, list):
        for v in o:
            walk(v, job, seen, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--root", default=r"C:\Users\repzy\Desktop\Video edits\Routerise")
    a = ap.parse_args()
    lines, seen = [], set()
    for f in sorted(glob.glob(os.path.join(a.root, "*", "Docs", "**", "*.json"), recursive=True)):
        if "marker" not in os.path.basename(f).lower():
            continue
        job = os.path.relpath(f, a.root).split(os.sep)[0]
        lines.append(f"\n## {os.path.relpath(f, a.root)}")
        n0 = len(lines)
        try:
            walk(json.load(open(f, encoding="utf-8")), job, seen, lines)
        except (ValueError, OSError) as e:
            lines.append(f"ERR {e}")
        print(f"{len(lines) - n0:4}  {os.path.relpath(f, a.root)}")
    open(a.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(sum(1 for l in lines if l.startswith("- [")), "markers ->", a.out)


if __name__ == "__main__":
    main()
