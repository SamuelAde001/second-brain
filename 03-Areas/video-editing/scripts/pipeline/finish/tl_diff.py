# What changed on a timeline between two tl_snapshot.py files: new markers (all are requests), then per track the removed, added, moved or trimmed items and the frame spans touched.
# usage: python tl_diff.py <before.json> <after.json> [--len <timeline frames>] [--chunk 2020]    (file only, no Resolve)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
# Last line lists the render chunks (RERENDER) the touched frames fall in. --len defaults to the after-snapshot's length.
import argparse, json, sys

ap = argparse.ArgumentParser(description="Compare two tl_snapshot.py files: markers, per-track item changes, chunks to re-render.")
ap.add_argument("before")
ap.add_argument("after")
ap.add_argument("--len", type=int, default=None, help="timeline length in frames (default: the after-snapshot's end - start)")
ap.add_argument("--chunk", type=int, default=2020, help="render chunk size in frames (default 2020)")
args = ap.parse_args()

a, b = (json.load(open(f, encoding="utf-8")) for f in (args.before, args.after))
LEN = args.len if args.len else b["end"] - b["start"]
CH = args.chunk
print("timeline", b["timeline"], "| length before", a["end"] - a["start"], "after", b["end"] - b["start"])
print("\nMARKERS (%d)" % len(b["markers"]))
for k in sorted(b["markers"], key=lambda x: int(float(x))):
    m = b["markers"][k]
    if k not in a["markers"]:
        print("  f%-6s %-7s %-30s | %s" % (k, m.get("color"), m.get("name"), (m.get("note") or "").replace("\n", " / ")))
touched = []
for tr in sorted(set(a["tracks"]) | set(b["tracks"]), key=lambda t: (t[0], int(t[1:]))):
    A = {(i["s"], i["e"], i["name"], i["in"]) for i in a["tracks"].get(tr, [])}
    B = {(i["s"], i["e"], i["name"], i["in"]) for i in b["tracks"].get(tr, [])}
    gone, new = sorted(A - B), sorted(B - A)
    if not gone and not new:
        continue
    print("\n%s: %d removed or changed, %d added or changed" % (tr, len(gone), len(new)))
    for s, e, n, i in gone:
        print("  - %5d-%5d %s (in %s)" % (s, e, n, i)); touched.append((s, e))
    for s, e, n, i in new:
        print("  + %5d-%5d %s (in %s)" % (s, e, n, i)); touched.append((s, e))
if touched:
    lo, hi = min(s for s, _ in touched), max(e for _, e in touched)
    chunks = sorted({c for s, e in touched for c in range(0, LEN, CH) if s < c + CH and e > c})
    print("\nframes touched %d-%d | chunks to re-render: %s" % (lo, hi, " ".join(map(str, chunks))))
else:
    print("\nno item changes")
