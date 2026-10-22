"""Native Canva build of the chapter maps: every box, text, icon and arrow becomes a real Canva element.
The map HTML is laid out by Chrome with Canva's own fonts (DM Sans, DM Serif Display: same metrics as Canva's
files, so text wraps where Canva wraps it), read back as primitives, then written as Canva clipboard JSON.
python native.py map04 [map05 ...]  ->  out/native/<name>.json (loose elements on a Midnight panel) + <name>-prims.json + plan.json"""
import importlib, json, math, os, random, re, string, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out", "native")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROF = os.path.join(os.environ.get("TEMP", HERE), "c2e-native-chrome")
sys.path.insert(0, HERE)
import maplib

FONT = {"sans": "YAD1aU3sLnI,0", "serif": "YAD1aYG82rc,0"}  # Canva's DM Sans, DM Serif Display
COMP = {"0": "1", "C": "D", "G": "H", "I": "J", "K": "L", "M": "N", "W": "X", "Y": "Z", "c": "d", "q": "r", "BC": "BD", "BG": "BH"}
EDGE_STYLE = {"line": ("#3a5072", 5, None), "gold": ("#fcdd9e", 7, None), "dash": ("#fcdd9e", 4, [3, 1]),
              "thick": ("#fcdd9e", 14, [1, 1]), "mist": ("#b9c3d6", 4, None)}
DASH = {"dashed": [3, 1], "dotted": [1, 1]}
SRC_KEY = {"kit/samuel-cutout-sm.webp": "samuel-cutout", "kit/samuel-cutout.webp": "samuel-cutout",
           "kit/called-to-edit-logo-dark.svg": "logo-dark", "kit/called-to-edit-community-dark.svg": "community-dark"}
MEDIA_DIR = os.path.join(os.environ.get("C2E_MEDIA", ""))  # high-res copies, for intrinsic sizes

NATIVE_CSS = """<style>
@font-face{font-family:'Plus Jakarta Sans';src:url(kit/fonts/dm-sans-latin-400-normal.woff2);font-weight:100 599}
@font-face{font-family:'Plus Jakarta Sans';src:url(kit/fonts/dm-sans-latin-700-normal.woff2);font-weight:600 900}
@font-face{font-family:'Gloock';src:url(kit/fonts/dm-serif-display-latin-400-normal.woff2);font-weight:100 900}
*{font-synthesis:none!important}
</style>"""

EXTRACT_JS = r"""<script>
window.addEventListener('load',()=>document.fonts.ready.then(()=>setTimeout(()=>{
 const BG=[7,18,38];
 const P=c=>{if(!c)return null;const m=c.match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(/[\s,\/]+/).filter(Boolean).map(parseFloat);return [p[0],p[1],p[2],p.length>3?p[3]:1]};
 const HEX=c=>'#'+c.slice(0,3).map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join('');
 const OP=el=>{let o=1;for(let e=el;e&&e.nodeType===1&&e!==document.documentElement;e=e.parentElement){o*=parseFloat(getComputedStyle(e).opacity)}return o};
 const UNDER=el=>{for(let e=el;e&&e.nodeType===1&&e!==document.body;e=e.parentElement){const c=P(getComputedStyle(e).backgroundColor);if(c&&c[3]>0.5)return c.slice(0,3)}return BG};
 const COL=(c,el,bgEl)=>{const p=P(c);if(!p||p[3]===0)return null;const a=p[3]*OP(el),u=UNDER(bgEl);return HEX(p.slice(0,3).map((v,i)=>v*a+u[i]*(1-a)))};
 const ROT=el=>{let a=0;for(let e=el;e&&e.nodeType===1&&e!==document.body;e=e.parentElement){const t=getComputedStyle(e).transform;if(t&&t!=='none'){const m=t.match(/matrix\(([^)]+)\)/);if(m){const v=m[1].split(',').map(parseFloat);a+=Math.atan2(v[1],v[0])*180/Math.PI}}}return Math.round(a*100)/100};
 const SIZE=el=>{const r=el.getBoundingClientRect();return [el.offsetWidth!=null?el.offsetWidth:r.width,el.offsetHeight!=null?el.offsetHeight:r.height]};
 const GEO=(el,l,t,w,h)=>{const r=el.getBoundingClientRect();const [W,H]=SIZE(el);const a=ROT(el);let dx=l+w/2-W/2,dy=t+h/2-H/2;
  if(a){const s=Math.sin(a*Math.PI/180),c=Math.cos(a*Math.PI/180);[dx,dy]=[dx*c-dy*s,dx*s+dy*c]}
  return {x:r.left+r.width/2+dx-w/2,y:r.top+r.height/2+dy-h/2,w,h,r:a}};
 const GK=new Map();const G=el=>{const n=el.closest('.n,.note');if(!n)return null;if(!GK.has(n))GK.set(n,'g'+GK.size);return GK.get(n)};
 const out=[];
 const RAD=(cs,w,h)=>Math.min(Math.max(...['borderTopLeftRadius','borderTopRightRadius','borderBottomRightRadius','borderBottomLeftRadius'].map(k=>parseFloat(cs[k])||0)),Math.min(w,h)/2);
 const LHN={};const lhNormal=fam=>{if(!(fam in LHN)){const s=document.createElement('span');s.style.cssText=`font-family:${fam};font-size:100px;line-height:normal;position:absolute;left:0;top:0;white-space:nowrap`;s.textContent='Hg';document.body.appendChild(s);LHN[fam]=s.getBoundingClientRect().height/100;s.remove()}return LHN[fam]};
 const ST=(el,container)=>{const cs=getComputedStyle(el);const fam=/Gloock|Serif/.test(cs.fontFamily)?'serif':'sans';const size=parseFloat(cs.fontSize);
  const lh=cs.lineHeight==='normal'?lhNormal(cs.fontFamily):parseFloat(cs.lineHeight)/size;const ls=cs.letterSpacing==='normal'?0:parseFloat(cs.letterSpacing)/size;
  return {font:fam,bold:fam==='sans'&&parseFloat(cs.fontWeight)>=600,size:Math.round(size*100)/100,color:COL(cs.color,el,container)||'#ffffff',lh:Math.round(lh*1000)/1000,ls:Math.round(ls*1000)/1000,up:cs.textTransform==='uppercase'}};
 function collect(nodes,container,paras){for(const ch of nodes){
   if(ch.nodeType===3){let t=ch.textContent.replace(/\s+/g,' ');if(!t)continue;const s=ST(ch.parentElement,container);if(s.up)t=t.toUpperCase();paras[paras.length-1].push({t,s})}
   else if(ch.nodeType===1){const tag=ch.tagName.toLowerCase();if(tag==='br'){paras.push([]);continue}if(tag==='svg'||tag==='img'||tag==='script')continue;
    const d=getComputedStyle(ch).display;if(d==='none')continue;if(d==='inline')collect(ch.childNodes,container,paras)}}}
 const hasText=paras=>paras.some(p=>p.some(r=>r.t.trim()));
 const isInlineNode=n=>n.nodeType===3||(n.nodeType===1&&n.tagName.toLowerCase()!=='svg'&&n.tagName.toLowerCase()!=='img'&&(n.tagName.toLowerCase()==='br'||getComputedStyle(n).display==='inline'));
 function texts(el,cs){
  const flex=/flex|grid/.test(cs.display);const kids=[...el.childNodes];const hasBlock=kids.some(n=>n.nodeType===1&&!isInlineNode(n)&&n.tagName.toLowerCase()!=='svg'&&n.tagName.toLowerCase()!=='img');
  const seqs=[];let cur=[];for(const n of kids){if(isInlineNode(n))cur.push(n);else{if(cur.length)seqs.push(cur);cur=[]}}if(cur.length)seqs.push(cur);
  const align=cs.textAlign==='center'?'center':(/right|end/.test(cs.textAlign)?'end':'start');
  for(const seq of seqs){const paras=[[]];collect(seq,el,paras);if(!hasText(paras))continue;let geo;
   if(!flex&&!hasBlock&&seqs.length===1){const [W,H]=SIZE(el);const bl=parseFloat(cs.borderLeftWidth)+parseFloat(cs.paddingLeft),bt=parseFloat(cs.borderTopWidth)+parseFloat(cs.paddingTop),br=parseFloat(cs.borderRightWidth)+parseFloat(cs.paddingRight),bb=parseFloat(cs.borderBottomWidth)+parseFloat(cs.paddingBottom);geo=GEO(el,bl,bt,W-bl-br,H-bt-bb)}
   else{const rg=document.createRange();rg.setStartBefore(seq[0]);rg.setEndAfter(seq[seq.length-1]);const rs=[...rg.getClientRects()].filter(r=>r.width>0);if(!rs.length)continue;
    const x0=Math.min(...rs.map(r=>r.left)),y0=Math.min(...rs.map(r=>r.top)),x1=Math.max(...rs.map(r=>r.right)),y1=Math.max(...rs.map(r=>r.bottom));geo={x:x0,y:y0,w:x1-x0,h:y1-y0,r:ROT(el)}}
   out.push({t:'text',...geo,align,nowrap:cs.whiteSpace==='nowrap',paras,g:G(el)})}}
 function boxes(el,cs){const [W,H]=SIZE(el);if(!W||!H)return;const g=G(el);const R=RAD(cs,W,H);const nid=el.classList.contains('n')&&el.id?el.id:null;
  const sh=cs.boxShadow;if(sh&&sh!=='none'){const m=sh.match(/(rgba?\([^)]+\))\s+(-?[\d.]+)px\s+(-?[\d.]+)px\s+([\d.]+)px\s+([\d.]+)px/);if(m&&+m[2]===0&&+m[3]===0&&+m[4]===0&&+m[5]>0){const s=+m[5];out.push({t:'box',...GEO(el,-s,-s,W+2*s,H+2*s),fill:COL(m[1],el,el.parentElement),rad:R+s,g})}}
  const ow=parseFloat(cs.outlineWidth)||0;if(cs.outlineStyle!=='none'&&ow>0){const e=ow+(parseFloat(cs.outlineOffset)||0);out.push({t:'box',...GEO(el,-e,-e,W+2*e,H+2*e),stroke:COL(cs.outlineColor,el,el.parentElement),sw:ow,dash:cs.outlineStyle,rad:R+e,g})}
  const bg=P(cs.backgroundColor);const fill=bg&&bg[3]>0.01?COL(cs.backgroundColor,el,el.parentElement):null;
  const sd=['Top','Right','Bottom','Left'].map(s=>({w:parseFloat(cs['border'+s+'Width'])||0,c:cs['border'+s+'Color'],st:cs['border'+s+'Style']}));
  const vis=sd.filter(s=>s.w>0&&s.st!=='none'&&P(s.c)&&P(s.c)[3]>0);const uni=vis.length===4&&vis.every(s=>s.w===vis[0].w&&s.c===vis[0].c&&s.st===vis[0].st);
  if(fill||uni)out.push({t:'box',...GEO(el,0,0,W,H),fill,stroke:uni?COL(vis[0].c,el,el.parentElement):null,sw:uni?vis[0].w:0,dash:uni?vis[0].st:null,rad:R,g,nid});
  if(!uni)sd.forEach((s,i)=>{if(!(s.w>0&&s.st!=='none'))return;const c=COL(s.c,el,el.parentElement);if(!c)return;const q=[[0,0,W,s.w],[W-s.w,0,s.w,H],[0,H-s.w,W,s.w],[0,0,s.w,H]][i];out.push({t:'box',...GEO(el,...q),fill:c,rad:0,g})})}
 function icon(svg){const r=svg.getBoundingClientRect();if(!r.width)return;const vb=svg.viewBox&&svg.viewBox.baseVal&&svg.viewBox.baseVal.width?svg.viewBox.baseVal:{width:r.width,height:r.height};const paths=[];
  for(const ch of svg.querySelectorAll('path,circle,ellipse,line,polyline,polygon,rect')){const cs=getComputedStyle(ch);const A=n=>parseFloat(ch.getAttribute(n)||0);let d='';const tg=ch.tagName.toLowerCase();
   if(tg==='path')d=ch.getAttribute('d');
   else if(tg==='circle'){const cx=A('cx'),cy=A('cy'),q=A('r');d=`M${cx-q} ${cy}a${q} ${q} 0 1 0 ${2*q} 0a${q} ${q} 0 1 0 ${-2*q} 0z`}
   else if(tg==='ellipse'){const cx=A('cx'),cy=A('cy'),rx=A('rx'),ry=A('ry');d=`M${cx-rx} ${cy}a${rx} ${ry} 0 1 0 ${2*rx} 0a${rx} ${ry} 0 1 0 ${-2*rx} 0z`}
   else if(tg==='line')d=`M${A('x1')} ${A('y1')}L${A('x2')} ${A('y2')}`;
   else if(tg==='polyline'||tg==='polygon'){const p=(ch.getAttribute('points')||'').trim().split(/[\s,]+/).map(parseFloat);d='M'+p[0]+' '+p[1];for(let i=2;i<p.length;i+=2)d+='L'+p[i]+' '+p[i+1];if(tg==='polygon')d+='z'}
   else if(tg==='rect'){const x=A('x'),y=A('y'),w=A('width'),h=A('height');const q=Math.min(A('rx')||A('ry'),w/2,h/2);d=q?`M${x+q} ${y}H${x+w-q}A${q} ${q} 0 0 1 ${x+w} ${y+q}V${y+h-q}A${q} ${q} 0 0 1 ${x+w-q} ${y+h}H${x+q}A${q} ${q} 0 0 1 ${x} ${y+h-q}V${y+q}A${q} ${q} 0 0 1 ${x+q} ${y}z`:`M${x} ${y}H${x+w}V${y+h}H${x}z`}
   if(!d)continue;paths.push({d,fill:cs.fill==='none'?null:COL(cs.fill,svg,svg.parentElement),stroke:cs.stroke==='none'?null:COL(cs.stroke,svg,svg.parentElement),sw:parseFloat(cs.strokeWidth)||0})}
  const w=parseFloat(svg.getAttribute('width'))||r.width,h=parseFloat(svg.getAttribute('height'))||r.height;
  out.push({t:'icon',x:r.left+r.width/2-w/2,y:r.top+r.height/2-h/2,w,h,r:ROT(svg),vw:vb.width,vh:vb.height,paths,g:G(svg)})}
 for(const el of document.body.querySelectorAll('*')){
  if(el.closest('#edges'))continue;const tg=el.tagName.toLowerCase();if(tg==='script'||tg==='style')continue;
  if(el.closest('svg')&&tg!=='svg')continue;if(tg==='svg'&&el.parentElement.closest('svg'))continue;
  if(!el.getClientRects().length)continue;const cs=getComputedStyle(el);if(cs.visibility==='hidden'||OP(el)<0.02)continue;
  if(tg==='svg'){icon(el);continue}
  if(tg==='img'){const [W,H]=SIZE(el);out.push({t:'img',...GEO(el,0,0,W,H),src:el.getAttribute('src'),fit:cs.objectFit,g:G(el)});continue}
  boxes(el,cs);if(cs.display!=='inline')texts(el,cs)}
 const rv=[...document.querySelectorAll('.rv')].map(e=>{const r=e.getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height,label:e.dataset.label}});
 const SIDE=(r,s)=>({l:[r.left,r.top+r.height/2,-1,0],r:[r.right,r.top+r.height/2,1,0],t:[r.left+r.width/2,r.top,0,-1],b:[r.left+r.width/2,r.bottom,0,1]}[s]);
 const edges=[];for(const [a,b,kind,arrow,sa,sb,bend,label] of (window.EDGES||[])){const A=document.getElementById(a),B=document.getElementById(b);if(!A||!B)continue;
  const ra=A.getBoundingClientRect(),rb=B.getBoundingClientRect();const cx=(ra.left+ra.right)/2,cy=(ra.top+ra.bottom)/2,dx=(rb.left+rb.right)/2-cx,dy=(rb.top+rb.bottom)/2-cy;const hz=Math.abs(dx)>Math.abs(dy);
  const s1=sa||(hz?(dx>0?'r':'l'):(dy>0?'b':'t')),s2=sb||(hz?(dx>0?'l':'r'):(dy>0?'t':'b'));const p=SIDE(ra,s1),q=SIDE(rb,s2);let d=Math.hypot(q[0]-p[0],q[1]-p[1])*bend;if(s1==s2)d=Math.min(d,300);d=Math.min(d,600);
  edges.push({a,b,kind,arrow,s1,s2,p:[p[0],p[1]],q:[q[0],q[1]],c1:[p[0]+p[2]*d,p[1]+p[3]*d],c2:[q[0]+q[2]*d,q[1]+q[3]*d]})}
 const s=document.createElement('script');s.type='application/json';s.id='native';
 s.textContent=JSON.stringify({w:document.body.scrollWidth,h:window.FULLH||document.body.scrollHeight,els:out,rv,edges}).replace(/</g,'\\u003c');document.head.appendChild(s);
},300)));
</script>"""


def chrome_dom(url):
    r = subprocess.run([CHROME, "--headless=new", f"--user-data-dir={PROF}", "--allow-file-access-from-files",
                        "--virtual-time-budget=30000", "--run-all-compositor-stages-before-draw", "--dump-dom", url],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout


def extract(modname):
    m = importlib.import_module(modname)
    photos = json.load(open(os.path.join(HERE, "photos.json"), encoding="utf-8"))
    if hasattr(m, "P"):
        m.P.update(photos)
    body, w, _ = m.build()
    html = maplib.page(body, w, 40000, m.NAME)
    html = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>', "", html)
    html = html.replace("</head>", NATIVE_CSS + EXTRACT_JS + "</head>", 1)
    hp = os.path.join(HERE, m.NAME + "-native.html")
    open(hp, "w", encoding="utf-8").write(html)
    dom = chrome_dom("file:///" + hp.replace("\\", "/"))
    mm = re.search(r'<script type="application/json" id="native">(.*?)</script>', dom, re.S)
    if not mm:
        raise SystemExit(f"{m.NAME}: no extraction output")
    return m.NAME, json.loads(mm.group(1))


# ---------------- Canva elements ----------------

def rid():
    return "LB" + "".join(random.choice(string.ascii_letters + string.digits) for _ in range(14))


def r2(v):
    return round(v, 2)


def rich(paras):
    """paras: [{'align', 'runs': [{'t', 's': style}]}] -> Canva rich text (cumulative style changes)."""
    A, bl, ents, pos, run = [], [], [], 0, {}
    for p in paras:
        pt = "".join(r["t"] for r in p["runs"])
        A.append(pt + "\n"); bl.append(len(pt) + 1)
        for i, r in enumerate(p["runs"]):
            s = r["s"]
            S = {"0": "none", "C": FONT[s["font"]], "G": f'{s["size"]}px', "I": "bold" if s.get("bold") else "normal", "K": "normal",
                 "M": s["color"].lower(), "W": f'{s.get("ls", 0)}em', "Y": f'{s.get("lh", 1.3)}em', "BC": "0em", "BG": "none"}
            if i == 0:
                S["c"], S["q"] = p.get("align", "start"), "normal"
            d = {k: v for k, v in S.items() if run.get(k) != v}
            run.update(d)
            if d:
                ents.append([pos, d])
            pos += len(r["t"])
        pos += 1
    ents.append([pos, {COMP[k]: True for k in run}])
    merged = []
    for p_, d in ents:
        if merged and merged[-1][0] == p_:
            merged[-1][1].update(d)
        else:
            merged.append([p_, d])
    C = [d for _, d in merged]
    D = [merged[0][0]] + [merged[i][0] - merged[i - 1][0] for i in range(1, len(merged))]
    return {"A": A, "B": [pos], "C": C, "D": D}, bl


def clean_paras(paras, align):
    """Whitespace like CSS: collapse, trim paragraph ends, merge same-style runs; drop empty paragraphs at the ends."""
    res = []
    for runs in paras:
        rr = []
        for r in runs:
            t = r["t"]
            if rr and rr[-1]["t"].endswith(" ") and t.startswith(" "):
                t = t[1:]
            if not t:
                continue
            if rr and rr[-1]["s"] == r["s"]:
                rr[-1]["t"] += t
            else:
                rr.append({"t": t, "s": r["s"]})
        if rr:
            rr[0]["t"] = rr[0]["t"].lstrip()
            rr[-1]["t"] = rr[-1]["t"].rstrip()
            rr = [r for r in rr if r["t"]]
        res.append({"align": align, "runs": rr})
    while res and not res[0]["runs"]:
        res.pop(0)
    while res and not res[-1]["runs"]:
        res.pop()
    for p in res:  # an empty middle paragraph (double <br>) still needs a style: borrow the previous one
        if not p["runs"]:
            prev = next((q for q in res if q["runs"]), None)
            p["runs"] = [{"t": "", "s": prev["runs"][-1]["s"]}] if prev else []
    return [p for p in res if p["runs"]]


def text_el(e):
    paras = clean_paras(e["paras"], e["align"])
    if not paras:
        return None
    for p in paras:
        for r in p["runs"]:
            r["s"] = {k: v for k, v in r["s"].items() if k != "up"}
    rt, _ = rich(paras)
    slack = 2 if not e.get("nowrap") else 6
    x = e["x"] - (slack / 2 if e["align"] == "center" else (slack if e["align"] == "end" else 0))
    # "h": "A" = fixed width, Canva wraps at D; "B" = auto width (one line per paragraph).
    # "b" is Canva's cached line breaks: left empty so Canva lays the text out itself.
    lines = [max(r["s"]["size"] * r["s"].get("lh", 1.3) for r in p["runs"]) for p in paras]
    wrapped = not e.get("nowrap") and e["h"] > sum(lines) + 0.4 * min(lines)
    el = {"A": r2(e["y"]), "B": r2(x), "D": r2(e["w"] + slack), "C": r2(e["h"]), "A?": "K", "_": rid(),
          "a": {"C": rt}, "b": {}, "d": "A", "h": "A" if wrapped else "B"}
    if e.get("r"):
        el["E"] = e["r"]
    return el


def empty_frame(w, h):
    return [{"A": {"C": {"A": ["\n"], "B": [1], "C": [{"C": FONT["sans"], "G": "16px", "I": "normal", "K": "normal", "M": "#000000", "c": "center", "q": "normal"},
                                                        {"D": True, "H": True, "J": True, "L": True, "N": True, "d": True, "r": True}], "D": [0, 1]}},
             "B": {}, "D": {"D": w, "C": h}, "E": [4], "F": "B"}]


def shape(x, y, w, h, paths, vw=None, vh=None, rot=0, anchor=None):
    vw, vh = vw or w, vh or h
    el = {"A": r2(y), "B": r2(x), "D": r2(w), "C": r2(h), "A?": "J", "_": rid(), "a": {"D": r2(vw), "C": r2(vh)}, "b": paths,
          "c": {"A": {"D": r2(vw), "C": r2(vh)}, "B": r2(vw), "C": r2(vh), "D": "A", "E": "A"}, "e": {}, "f": empty_frame(r2(vw), r2(vh)),
          "h": {"A?": "H", "A": r2(w)}}
    if rot:
        el["E"] = rot
    if anchor:
        el["W"] = anchor
    return el


def box_el(e, anchor=None):
    w, h = e["w"], e["h"]
    path = {"A": f"M0 0H{r2(w)}V{r2(h)}H0z", "B": {"C": e["fill"]} if e.get("fill") else {}}
    if e.get("stroke") and e.get("sw"):
        st = {"A": r2(e["sw"]), "B": e["stroke"]}
        if e.get("dash") in DASH:
            st["C"] = DASH[e["dash"]]
        path["C"] = st
    if e.get("rad"):
        path["D"] = r2(e["rad"])
    if not e.get("fill") and "C" not in path:
        return None
    return shape(e["x"], e["y"], w, h, [path], rot=e.get("r") or 0, anchor=anchor)


def icon_el(e):
    k = e["w"] / e["vw"]
    paths = []
    for p in e["paths"]:
        q = {"A": p["d"], "B": {"C": p["fill"]} if p.get("fill") else {}}
        if p.get("stroke") and p.get("sw"):
            q["C"] = {"A": r2(p["sw"] * k), "B": p["stroke"]}  # round ends: no "f"
        if q["B"] or "C" in q:
            paths.append(q)
    if not paths:
        return None
    return shape(e["x"], e["y"], e["w"], e["h"], paths, e["vw"], e["vh"], e.get("r") or 0)


MEDIA = json.load(open(os.path.join(HERE, "canva_media.json"), encoding="utf-8"))
SIZES = {}


def media_size(key):
    if key not in SIZES:
        from PIL import Image
        f = next((os.path.join(MEDIA_DIR, key + ext) for ext in (".jpg", ".png") if os.path.exists(os.path.join(MEDIA_DIR, key + ext))), None)
        SIZES[key] = Image.open(f).size if f else None
    return SIZES[key]


def img_el(e):
    src = e["src"]
    key = SRC_KEY.get(src) or os.path.splitext(os.path.basename(src))[0]
    if key not in MEDIA:
        print("  no media for", src); return None
    iw, ih = media_size(key) or (e["w"], e["h"])
    x, y, w, h = e["x"], e["y"], e["w"], e["h"]
    if e.get("fit") == "contain":
        s = min(w / iw, h / ih); nw, nh = iw * s, ih * s
        x, y, w, h = x + (w - nw) / 2, y + (h - nh) / 2, nw, nh
    s = max(w / iw, h / ih); dw, dh = iw * s, ih * s
    B = {"D": r2(dw), "C": r2(dh)}
    if abs(dh - h) > 0.01: B["A"] = r2(-(dh - h) / 2)
    if abs(dw - w) > 0.01: B["B"] = r2(-(dw - w) / 2)
    el = {"A": r2(y), "B": r2(x), "D": r2(w), "C": r2(h), "A?": "I", "_": rid(), "a": {"B": {"A": {"A?": "d", "A": MEDIA[key], "B": 1}, "B": B}}}
    if e.get("r"):
        el["E"] = e["r"]
    return el


def sticky_el(x, y, w, h, label):
    fx = lambda v: r2(v * w / 240)
    curl = (f"M0 {r2(h-8)}H{r2(w)}L{r2(w-10)} {r2(h)}C{r2(w-10)} {r2(h)} {fx(152)} {r2(h-6)} {fx(144)} {r2(h-6)}H{fx(96)}"
            f"C{fx(88)} {r2(h-6)} 10 {r2(h)} 10 {r2(h)}L0 {r2(h-8)}V0H{r2(w)}V{r2(h-8)}H1V{r2(h-9)}H{r2(w-1)}V1H1V{r2(h-8)}")
    size = max(26, min(64, h * 0.22, w * 0.09))
    rt, _ = rich([{"align": "center", "runs": [{"t": label, "s": {"font": "sans", "bold": True, "size": round(size), "color": "#0a1f44", "lh": 1.2}}]}])
    return {"A": r2(y), "B": r2(x), "D": r2(w), "C": r2(h), "A?": "J", "_": rid(), "a": {"D": r2(w), "C": r2(h)},
            "b": [{"A": f"M0 0H{r2(w)}V{r2(h-8)}H0Z", "B": {"A": False, "C": "#fcdd9e"}},
                  {"A": curl, "B": {"A": False, "C": "#394c60", "D": 0.9, "F": True}}],
            "c": {"A": {"A": 80, "B": 96, "D": 48, "C": 80}, "B": 48, "C": 80, "D": "A", "E": "A"},
            "f": [{"A": {"C": rt}, "B": {"A": [2]}, "D": {"D": r2(w), "C": r2(h - 44)}, "E": [16], "F": "B"},
                  {"A": {"C": {"A": ["Samuel Adebayo\n"], "B": [15], "C": [{"G": "14px"}, {"H": True}], "D": [0, 15]}}, "B": {}, "D": {"A": r2(h - 44), "D": r2(w), "C": 36}, "E": [0, 16], "F": "A"}],
            "h": {"A?": "H", "A": 240}}


FRAC = {"l": (0.5, 0), "r": (0.5, 1), "t": (0, 0.5), "b": (1, 0.5)}


def conn_el(ed, anchors):
    col, sw, dash = EDGE_STYLE.get(ed["kind"], EDGE_STYLE["line"])
    (px, py), (qx, qy) = ed["p"], ed["q"]
    # one-bulge curve from the drawn cubic: twice the cubic midpoint's offset from the chord
    mx = (px + 3 * ed["c1"][0] + 3 * ed["c2"][0] + qx) / 8; my = (py + 3 * ed["c1"][1] + 3 * ed["c2"][1] + qy) / 8
    L = math.hypot(qx - px, qy - py) or 1
    nx, ny = -(qy - py) / L, (qx - px) / L
    dev = (mx - (px + qx) / 2) * nx + (my - (py + qy) / 2) * ny
    parallel = {ed["s1"], ed["s2"]} in ({"l", "r"}, {"t", "b"}) and ed["s1"] != ed["s2"]
    across = abs(qy - py) if ed["s1"] in "lr" else abs(qx - px)
    if parallel and abs(dev) < 8 and across > 40:
        curve = {"A?": "A", "C": 40}          # S-bend -> elbow with round corners
    elif abs(dev) < 4:
        curve = None                          # straight
    else:
        curve = {"A?": "D", "A": r2(2 * dev)}
    el = {"A": r2(min(py, qy)), "B": r2(min(px, qx)), "D": r2(abs(qx - px)) or 1, "C": r2(abs(qy - py)) or 1, "A?": "U", "_": rid(), "a": sw,
          "b": {"C": {"A": r2(py), "B": r2(px)}}, "c": {"C": {"A": r2(qy), "B": r2(qx)}}, "d": col}
    if ed["a"] in anchors:
        fy, fx = FRAC[ed["s1"]]; el["b"]["B"] = {"A": anchors[ed["a"]], "B": fy, "C": fx, "D": "A"}
    if ed["b"] in anchors:
        fy, fx = FRAC[ed["s2"]]; el["c"]["B"] = {"A": anchors[ed["b"]], "B": fy, "C": fx, "D": "A"}
    if ed.get("arrow"):
        el["c"]["A"] = "B"
    if curve:
        el["i"] = curve
    if dash:
        el["e"] = dash
    return el


def bbox(el):
    return el["B"], el["A"], el["B"] + el["D"], el["A"] + el["C"]


def group(children, lift_anchor=False):
    if lift_anchor:  # a connector may not point inside a group: the group takes its box's anchor
        anchor = next((c["W"] for c in children if "W" in c), None)
        children = [{k: v for k, v in c.items() if k != "W"} for c in children]
    xs = [bbox(c) for c in children]
    x0, y0 = min(b[0] for b in xs), min(b[1] for b in xs)
    x1, y1 = max(b[2] for b in xs), max(b[3] for b in xs)
    kids = []
    for c in children:
        c = dict(c); c["A"] = r2(c["A"] - y0); c["B"] = r2(c["B"] - x0)
        if c["A?"] == "U":  # line points are absolute in the clipboard: shift them too
            for end in ("b", "c"):
                c[end] = json.loads(json.dumps(c[end])); c[end]["C"]["A"] = r2(c[end]["C"]["A"] - y0); c[end]["C"]["B"] = r2(c[end]["C"]["B"] - x0)
        kids.append(c)
    g = {"A": r2(y0), "B": r2(x0), "D": r2(x1 - x0), "C": r2(y1 - y0), "A?": "H", "_": rid(), "b": r2(x1 - x0), "a": r2(y1 - y0), "c": kids}
    if lift_anchor and anchor:
        g["W"] = anchor
    return g


BACK = ("#071226", 500, 450)  # Midnight panel behind each chapter: colour, side margin, top/bottom margin (half the 900 gap)


def convert(name, data, wrap=False):
    ns = "CTE" + re.sub(r"[^A-Za-z0-9]", "", name)
    anchors, groups, order, loose = {}, {}, [], []
    stats = {}
    for e in data["els"]:
        t = e["t"]
        if t == "box":
            a = None
            if e.get("nid") and e["nid"] not in anchors:
                anchors[e["nid"]] = f"{ns}-{len(anchors) + 1}"
                a = {ns: anchors[e["nid"]]}
            el = box_el(e, a)
        elif t == "text":
            el = text_el(e)
        elif t == "icon":
            el = icon_el(e)
        elif t == "img":
            el = img_el(e)
        else:
            el = None
        if not el:
            continue
        stats[t] = stats.get(t, 0) + 1
        g = e.get("g")
        if g:
            if g not in groups:
                groups[g] = []; order.append(("g", g))
            groups[g].append(el)
        else:
            order.append(("e", el))
    conns = [conn_el(ed, anchors) for ed in data["edges"]]
    stats["edges"] = len(conns)
    top = []
    zones = [el for kind, el in order if kind == "e" and el["A?"] == "J" and not el["b"][0]["B"]]  # outline-only shapes first
    body = []
    for kind, v in order:
        if kind == "g":
            ch = groups[v]
            body.append(group(ch, lift_anchor=True) if len(ch) > 1 else ch[0])
        elif v not in zones:
            body.append(v)
    stick = [sticky_el(r["x"], r["y"], r["w"], r["h"], r["label"]) for r in data["rv"] if r["w"] > 0]
    stats["stickies"] = len(stick)
    col, mx, my = BACK
    back = shape(-mx, -my, data["w"] + 2 * mx, data["h"] + 2 * my, [{"A": f"M0 0H{data['w'] + 2 * mx}V{data['h'] + 2 * my}H0z", "B": {"C": col}}])
    top = [back] + zones + conns + body + stick  # the panel is the paste's bounding box, so placement is exact
    els = [group(top)] if wrap else top
    payload = {"a": 5, "h": "www.canva.com", "c": "DAHYrXl8-WE", "i": "Vy9aSwga4gVcdXINoOc29g", "b": 1792625136638,
               "n": {"A": {}}, "p": False, "A?": "B", "A": els, "B": -1, "C": -1}
    return payload, stats


COL_X, GAP = 7000, 900  # native column: left edge of the maps, gap between chapters (old image column is at x=0)


def plan(sizes):
    """Chapters stacked down the column. Canva centres a paste on the cursor, so each entry gives the panel's centre."""
    out, y = [], 0
    for name, w, h in sizes:
        _, mx, my = BACK
        out.append({"name": name, "x": COL_X, "y": y, "w": w, "h": h, "panel": [COL_X - mx, y - my, w + 2 * mx, h + 2 * my],
                    "centre": [COL_X + w / 2, y + h / 2]})
        y += h + GAP
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for a in sys.argv[1:]:
        name, data = extract(a)
        json.dump(data, open(os.path.join(OUT, name + "-prims.json"), "w", encoding="utf-8"))
        payload, stats = convert(name, data)
        s = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8").write(s)
        print(f"{name}: {data['w']}x{data['h']}  {len(s)//1024} KB  {stats}")
    sizes = []
    for f in sorted(os.listdir(OUT)):
        if re.fullmatch(r"map\d\d-[a-z]+-prims\.json", f):
            d = json.load(open(os.path.join(OUT, f), encoding="utf-8"))
            sizes.append((f[:-11], d["w"], d["h"]))
    json.dump(plan(sizes), open(os.path.join(OUT, "plan.json"), "w"), indent=1)
