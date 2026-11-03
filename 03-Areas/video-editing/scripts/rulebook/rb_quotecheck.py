"""Check that every quote in the rulebook is Samuel's real words.

Every *"..."* in rulebook/rb-*.md must appear word for word (case and punctuation ignored, "..." gaps
allowed) in at least one source: his messages (samuel_all.md from rb_extract.py), the marker list
(markers_all.md from rb_markers.py), any Brain note outside the rulebook, or a job folder's Docs .md file.
Prints the quotes it could not find. Run after every rulebook edit that adds a quote.

Usage: python rb_quotecheck.py --work <folder with samuel_all.md and markers_all.md>
"""
import argparse, glob, os, re

BRAIN = r"C:/Users/repzy/Desktop/My Second brain/"
JOBS = r"C:/Users/repzy/Desktop/Video edits/Routerise/*/Docs/**/*.md"


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower().replace("\u2019", "'")).strip()


def read(f):
    try:
        return open(f, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError):
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    corpus = [read(os.path.join(a.work, "samuel_all.md")), read(os.path.join(a.work, "markers_all.md"))]
    if not corpus[0]:
        print("WARNING: samuel_all.md missing; run rb_extract.py first")
    for f in glob.glob(BRAIN + "**/*.md", recursive=True):
        p = f.replace("\\", "/")
        if "/rulebook/" not in p and "_imports" not in p:
            corpus.append(read(f))
    corpus += [read(f) for f in glob.glob(JOBS, recursive=True)]
    C = norm(" ".join(corpus))
    total = bad = 0
    for f in sorted(glob.glob(BRAIN + "03-Areas/video-editing/rulebook/rb-*.md")):
        for q in re.findall(r'\*"([^"*]{6,})"\*', read(f)):
            total += 1
            parts = [p for p in re.split(r"\s*(?:\.\.\.|\u2026)\s*", q) if len(norm(p)) > 3]
            if not all(norm(p) in C for p in parts):
                bad += 1
                print(f"NOT FOUND  {os.path.basename(f)}: {q}")
    print(f"{total} quotes, {bad} not found word for word")


if __name__ == "__main__":
    main()
