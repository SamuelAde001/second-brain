import re, glob, os
def norm(s): return re.sub(r"[^a-z0-9]+"," ",s.lower().replace("’","'")).strip()
corpus=[open("samuel_all.md",encoding="utf-8").read(), open("markers_all.md",encoding="utf-8").read()]
B="C:/Users/repzy/Desktop/My Second brain/"
for f in glob.glob(B+"**/*.md",recursive=True):
    if "/rulebook/" in f.replace("\\","/") or "_imports" in f: continue
    try: corpus.append(open(f,encoding="utf-8").read())
    except: pass
for f in glob.glob("C:/Users/repzy/Desktop/Video edits/Routerise/*/Docs/**/*.md",recursive=True):
    try: corpus.append(open(f,encoding="utf-8").read())
    except: pass
C=norm(" ".join(corpus))
tot=bad=0; out=[]
for f in sorted(glob.glob(B+"03-Areas/video-editing/rulebook/rb-*.md")):
    for q in re.findall(r'\*"([^"*]{6,})"\*', open(f,encoding="utf-8").read()):
        tot+=1; n=norm(q)
        parts=[p for p in re.split(r"\s*(?:\.\.\.|…)\s*", q) if len(norm(p))>3]
        if all(norm(p) in C for p in parts): continue
        bad+=1; out.append(f"{os.path.basename(f)}: {q}")
print(tot,"quotes,",bad,"not found verbatim"); print("\n".join(out))
