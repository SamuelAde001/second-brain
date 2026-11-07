"""Script-aligned take picker: for each script sentence, find every take in the raws, pick the last complete one."""
import json, re, sys
NUM={"1":"one","2":"two","3":"three","4":"four","5":"five","10":"ten","13":"thirteen","40":"forty"}
def toks(text):
    text=text.replace("$12M","12 million dollars").replace("$1M","1 million").replace("$0","0").replace("3Cs","three c's").replace("3 C's","three c's")
    out=[]
    for w in re.findall(r"[A-Za-z0-9']+",text.lower()):
        w=NUM.get(w,w).replace("'","")
        if w in ("um","uh","erm"): continue
        out.append(w)
    return out
def script_lines(md):
    s=open(md,encoding='utf-8').read()
    s=s[s.index("### Hook"):s.index("## What was actually shot")]
    lines=[];sec=None
    for raw in s.split("\n"):
        raw=raw.strip()
        if not raw: continue
        if raw.startswith("###"): sec=raw.strip("# ").strip(); continue
        if raw.startswith("["): continue
        for sent in re.split(r"(?<=[.?!])\s+",raw):
            t=toks(sent)
            if len(t)>=3: lines.append({"sec":sec,"text":sent,"t":t})
    return lines
def raw_words(files):
    W=[]
    for f in files:
        name=re.search(r"(00\d\d)",f).group(1)
        for seg in json.load(open(f,encoding='utf-8')):
            for s,e,w in seg["w"]:
                for t in toks(w):
                    W.append((name,s,e,t,w.strip()))
    return W
def align(L,W,i,maxskip=4):
    j=i; m=0; last=None; first=None; k=0
    while k<len(L) and j<len(W):
        hit=None
        for d in range(0,maxskip+1):
            if j+d<len(W) and W[j+d][3]==L[k] and W[j+d][0]==W[i][0]: hit=j+d; break
        if hit is None:
            k+=1; continue
        if first is None: first=hit
        m+=1; last=hit; j=hit+1; k+=1
    return m,first,last
def find_takes(L,W,lo):
    takes=[]; n=len(L); head=L[:3]
    i=lo
    while i<len(W):
        if W[i][3]==head[0] or (len(head)>1 and W[i][3]==head[1]):
            m,f,l=align(L,W,i)
            if f is not None and m/n>=0.5:
                # a restart inside the span (head words again) starts a later, cleaner take
                best=(f,l,m)
                for q in range(f+1,l):
                    if W[q][3]==L[0] and q+1<len(W) and W[q+1][3]==(L[1] if n>1 else L[0]):
                        m2,f2,l2=align(L,W,q)
                        if f2 is not None and m2/n>=0.8: best=(f2,l2,m2)
                f,l,m=best
                exp=n*0.42
                takes.append({"i":f,"j":l,"cov":round(m/n,2),"long":(W[l][2]-W[f][1])>2.5*exp+3})
                i=l+1 if l>i else i+1; continue
        i+=1
    return takes
if __name__=="__main__":
    md, out, *files = sys.argv[1:]
    L=script_lines(md); W=raw_words(files)
    lo=0; res=[]
    for ln in L:
        tk=find_takes(ln["t"],W,max(0,lo-50))
        # only takes within the next ~6 minutes of speech to keep order
        if tk:
            base=W[tk[0]["i"]]
            tk=[t for t in tk if W[t["i"]][0]==base[0] and W[t["i"]][1]-base[1]<360] or tk[:1]
        good=[t for t in tk if t["cov"]>=0.8]
        pick=(good or sorted(tk,key=lambda t:t["cov"]))[-1] if tk else None
        r={"sec":ln["sec"],"text":ln["text"],"takes":len(tk)}
        if pick:
            a,b=W[pick["i"]],W[pick["j"]]
            r.update(file=a[0],s=round(a[1],2),e=round(b[2],2),cov=pick["cov"],long=pick["long"],
                     spoken=" ".join(w[4] for w in W[pick["i"]:pick["j"]+1]))
            lo=pick["j"]+1
        res.append(r)
    json.dump(res,open(out,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
    found=[r for r in res if "file" in r]
    print("lines",len(res),"found",len(found),"low cov",sum(1 for r in found if r["cov"]<0.8),"missing",len(res)-len(found))
    print("kept speech %.1f min"%(sum(r["e"]-r["s"] for r in found)/60))
