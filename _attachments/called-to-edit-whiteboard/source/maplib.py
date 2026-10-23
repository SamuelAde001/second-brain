"""Mind-map building blocks for the webinar whiteboard: free-placed nodes joined by drawn connectors.
Each chapter is one big canvas. Connectors are drawn by a script after layout, from the node edges."""
import json, os
from lib import icon, mark, rv, NAVY, MID, SLATE, CH, MIST

EDGES = []


def reset():
    EDGES.clear()


def edge(a, b, kind="line", arrow=True, sa=None, sb=None, bend=0.45, label=""):
    """kind: line (mist), gold (the main flow), dash (aside / demo), thick (chapter road)."""
    EDGES.append([a, b, kind, arrow, sa, sb, bend, label])


def chain(ids, kind="gold", **kw):
    for a, b in zip(ids, ids[1:]):
        edge(a, b, kind, **kw)


def node(nid, x, y, w, inner, cls="", style=""):
    ws = f"{w}px" if isinstance(w, (int, float)) else w
    return f'<div class="n {cls}" id="{nid}" style="left:{x}px;top:{y}px;width:{ws};{style}">{inner}</div>'


def topic(nid, x, y, w, num, title_, ic="", sub=""):
    """A branch head: number badge, icon, title."""
    i = icon(ic, 54) if ic else ""
    s = f'<div class="ts">{sub}</div>' if sub else ""
    return node(nid, x, y, w, f'<div class="tb">{num}</div>{i}<div><div class="tt">{title_}</div>{s}</div>', "topic")


def leaf(nid, x, y, w, head, body="", ic="", cls="", style=""):
    i = icon(ic, 42, NAVY if "gold" in cls else (MIST if "dim" in cls else CH), 2 if "gold" in cls else 1.8) if ic else ""
    b = f'<div class="lb">{body}</div>' if body else ""
    return node(nid, x, y, w, f'{i}<div class="lc"><div class="lh">{head}</div>{b}</div>', "leaf " + cls, style)


def chip(nid, x, y, text, cls="", w=None):
    ws = f"{w}px" if w else "auto"
    return f'<div class="n chip {cls}" id="{nid}" style="left:{x}px;top:{y}px;width:{ws}">{text}</div>'


def note(x, y, w, html, style=""):
    return f'<div class="note" style="left:{x}px;top:{y}px;width:{w}px;{style}">{html}</div>'


def quote_(x, y, w, text, size=56):
    return note(x, y, w, f'<div class="mq" style="font-size:{size}px">{mark(26)}<span>&ldquo;{text}&rdquo;</span></div>')


def hub(nid, x, y, num, top, big, sub=""):
    s = f'<div class="hs">{sub}</div>' if sub else ""
    return node(nid, x, y, 1000, f'<div class="hn">{num}</div><div><div class="ht">{top}</div><div class="hb">{big}</div>{s}</div>', "hub")


def demo_(nid, x, y, w, what, where=""):
    wh = f'<div class="dw">{where}</div>' if where else ""
    return node(nid, x, y, w, f'{icon("monitor-play", 54, NAVY, 2.2)}<div><div class="dl">LIVE DEMO · switch to Chrome</div><div class="dt">{what}</div>{wh}</div>', "demo")


def photo(nid, x, y, w, h, label, src=None, tilt=0, fit="cover"):
    inner = (f'<img src="{src}" style="width:100%;height:{h}px;object-fit:{fit};display:block;border-radius:6px">' if src
             else f'<div class="phx" style="height:{h}px">{icon("camera", 46, MIST)}<span>{label}</span></div>')
    cap = f'<div class="pc">{label}</div>' if src else ""
    return node(nid, x, y, w, inner + cap, "polaroid", f"transform:rotate({tilt}deg)")


CSS = """
.n{position:absolute}
.hub{display:flex;gap:34px;align-items:center;background:#0A1F44;border:4px solid #FCDD9E;border-radius:60px;padding:46px 56px;box-shadow:0 0 0 14px rgba(252,221,158,.08)}
.hn{font-family:Gloock;font-size:230px;line-height:.8;color:#FCDD9E;letter-spacing:-.05em}
.ht{font:600 40px 'Plus Jakarta Sans';color:#fff}
.hb{font-family:Gloock;font-size:110px;line-height:.92;color:#FCDD9E;letter-spacing:-.04em}
.hs{font:500 26px/1.4 'Plus Jakarta Sans';color:#B9C3D6;margin-top:14px}
.topic{display:flex;align-items:center;gap:20px;background:#FCDD9E;color:#0A1F44;border-radius:999px;padding:20px 34px 20px 20px}
.topic svg{stroke:#0A1F44}
.tb{flex:none;width:70px;height:70px;border-radius:50%;background:#0A1F44;color:#FCDD9E;display:flex;align-items:center;justify-content:center;font:800 24px 'Plus Jakarta Sans'}
.tt{font:800 42px/1.1 'Plus Jakarta Sans';letter-spacing:-.02em}
.ts{font:600 22px 'Plus Jakarta Sans';opacity:.75;margin-top:4px}
.leaf{display:flex;gap:18px;align-items:flex-start;background:#1E3150;border-radius:24px;padding:24px 28px}
.leaf.gold{background:#FCDD9E;color:#0A1F44}
.leaf.dim{background:transparent;border:3px solid #1E3150}
.leaf.navy{background:#0A1F44;border:3px solid #1E3150}
.lc{flex:1}
.lh{font:800 30px/1.2 'Plus Jakarta Sans';letter-spacing:-.01em;color:#fff}
.leaf.gold .lh{color:#0A1F44}
.leaf.dim .lh{color:#B9C3D6}
.lb{font:500 24px/1.42 'Plus Jakarta Sans';color:#B9C3D6;margin-top:6px}
.leaf.gold .lb{color:#0A1F44;opacity:.85}
.lb b{color:#fff}.leaf.gold .lb b{color:#0A1F44}
.chip{background:#0A1F44;border:3px solid #FCDD9E;color:#fff;border-radius:999px;padding:12px 26px;font:700 26px 'Plus Jakarta Sans';white-space:nowrap}
.chip.gold{background:#FCDD9E;color:#0A1F44}
.chip.dim{border-color:#1E3150;color:#B9C3D6}
.note{position:absolute;font:500 26px/1.45 'Plus Jakarta Sans';color:#B9C3D6}
.note b{color:#fff}
.mq{display:flex;gap:18px;align-items:flex-start;font-family:Gloock;line-height:1.05;color:#FCDD9E;letter-spacing:-.03em}
.mq svg{margin-top:12px}
.demo{display:flex;align-items:center;gap:20px;background:#FCDD9E;color:#0A1F44;border-radius:22px;padding:22px 28px;border:4px dashed #0A1F44;outline:4px solid #FCDD9E}
.dl{font:800 18px 'Plus Jakarta Sans';letter-spacing:.14em}
.dt{font:800 32px/1.15 'Plus Jakarta Sans';margin-top:4px}
.dw{font:600 21px/1.3 'Plus Jakarta Sans';margin-top:6px;opacity:.85}
.polaroid{background:#fff;padding:14px 14px 18px;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.phx{border:3px dashed #B9C3D6;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;text-align:center;padding:16px;font:700 21px/1.3 'Plus Jakarta Sans';color:#4A5670;background:#EEF1F6}
.pc{font:700 21px 'Plus Jakarta Sans';color:#0A1F44;margin-top:10px;text-align:center}
.lbl{position:absolute;font:800 20px 'Plus Jakarta Sans';letter-spacing:.1em;text-transform:uppercase;color:#FCDD9E;background:#071226;padding:4px 12px;border-radius:8px;transform:translate(-50%,-50%);white-space:nowrap}
.zone{position:absolute;border:3px dashed rgba(185,195,214,.18);border-radius:60px}
.zl{position:absolute;font:800 22px 'Plus Jakarta Sans';letter-spacing:.16em;color:#B9C3D6;opacity:.6;text-transform:uppercase}
"""

EDGE_JS = """
<script>
function drawEdges(){
 const E=window.EDGES||[];const svg=document.getElementById('edges');const NS='http://www.w3.org/2000/svg';
 const st={line:['#3A5072',5,''],gold:['#FCDD9E',7,''],dash:['#FCDD9E',4,'4 16'],thick:['#FCDD9E',14,'2 30'],mist:['#B9C3D6',4,'']};
 function side(r,s){return {l:[r.left,r.top+r.height/2,-1,0],r:[r.right,r.top+r.height/2,1,0],t:[r.left+r.width/2,r.top,0,-1],b:[r.left+r.width/2,r.bottom,0,1]}[s]}
 for(const [a,b,kind,arrow,sa,sb,bend,label] of E){
  const A=document.getElementById(a),B=document.getElementById(b);if(!A||!B){console.log('missing',a,b);continue}
  const ra=A.getBoundingClientRect(),rb=B.getBoundingClientRect();
  const cx=(ra.left+ra.right)/2,cy=(ra.top+ra.bottom)/2,dx=(rb.left+rb.right)/2-cx,dy=(rb.top+rb.bottom)/2-cy;
  const h=Math.abs(dx)>Math.abs(dy);
  const s1=sa||(h?(dx>0?'r':'l'):(dy>0?'b':'t')), s2=sb||(h?(dx>0?'l':'r'):(dy>0?'t':'b'));
  const p=side(ra,s1),q=side(rb,s2);let d=Math.hypot(q[0]-p[0],q[1]-p[1])*bend;if(s1==s2)d=Math.min(d,300);d=Math.min(d,600);
  const c1=[p[0]+p[2]*d,p[1]+p[3]*d],c2=[q[0]+q[2]*d,q[1]+q[3]*d];
  const [col,w,da]=st[kind]||st.line;
  const path=document.createElementNS(NS,'path');
  path.setAttribute('d',`M${p[0]} ${p[1]} C${c1[0]} ${c1[1]} ${c2[0]} ${c2[1]} ${q[0]} ${q[1]}`);
  path.setAttribute('fill','none');path.setAttribute('stroke',col);path.setAttribute('stroke-width',w);path.setAttribute('stroke-linecap','round');
  if(da)path.setAttribute('stroke-dasharray',da);svg.appendChild(path);
  if(arrow){const ang=Math.atan2(q[1]-c2[1],q[0]-c2[0]),L=12+w*2.2;
   const hd=document.createElementNS(NS,'path');
   hd.setAttribute('d',`M${q[0]-L*Math.cos(ang-0.5)} ${q[1]-L*Math.sin(ang-0.5)} L${q[0]} ${q[1]} L${q[0]-L*Math.cos(ang+0.5)} ${q[1]-L*Math.sin(ang+0.5)}`);
   hd.setAttribute('fill','none');hd.setAttribute('stroke',col);hd.setAttribute('stroke-width',Math.max(w,5));hd.setAttribute('stroke-linecap','round');hd.setAttribute('stroke-linejoin','round');svg.appendChild(hd)}
  if(label){const t=document.createElement('div');t.className='lbl';t.textContent=label;t.style.left=((p[0]+q[0])/2)+'px';t.style.top=((p[1]+q[1])/2)+'px';document.body.appendChild(t)}
 }
}
window.addEventListener('load',()=>document.fonts.ready.then(()=>{if(window.layout)layout();drawEdges();
 const out=[];document.querySelectorAll('.rv').forEach((e,i)=>{const r=e.getBoundingClientRect();out.push({i,label:e.dataset.label,x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height)})});
 const p=document.createElement('script');p.type='application/json';p.id='pos';p.textContent=JSON.stringify({w:document.body.scrollWidth,h:window.FULLH||document.body.scrollHeight,rv:out});document.head.appendChild(p);}));
</script>"""


def page(body, w, h, name, band=None):
    """band=(a, b): print only rows a..b of the map (for files Canva would refuse as too big)."""
    ph, extra = h, ""
    if band:
        ph = band[1] - band[0]
        extra = (f"<style>html{{height:{ph}px!important;overflow:hidden}}</style>"
                 f"<script>window.addEventListener('load',()=>document.fonts.ready.then(()=>setTimeout(()=>{{document.body.style.transform='translateY(-{band[0]}px)'}},50)));</script>")
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{name}</title>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="board.css"><style>{CSS}
@page{{size:{w}px {ph}px;margin:0}} html,body{{width:{w}px;height:{h}px;overflow:hidden;background:transparent}}
#edges{{position:absolute;left:0;top:0}}</style>
<script>window.EDGES={json.dumps(EDGES)};</script>{LAYOUT_JS}{EDGE_JS}{extra}</head>
<body><svg id="edges" width="{w}" height="{h}" viewBox="0 0 {w} {h}"></svg>{body}</body></html>"""


# ---- whole-chapter layout: hub column on the left, branches in a two-column snake, heights measured in the page ----
WHITE = os.environ.get("C2E_THEME") == "white"  # white board: more room around each branch for scribbles
COLX, COLW = ([1450, 3850] if WHITE else [1300, 3360]), 1800
RG = 450 if WHITE else 150

CSS += """
.side{position:absolute;left:60px;top:100px;width:1060px;display:flex;flex-direction:column;gap:70px}
.side .n,.side .note,.flow .n,.flow .note,.flow .flow{position:relative!important;left:auto!important;top:auto!important}
.br{position:absolute;width:1800px}
.flow{position:absolute;display:flex}
.toc{display:flex;flex-direction:column;gap:14px}
.toc div{display:flex;gap:18px;align-items:center;font:700 27px 'Plus Jakarta Sans';color:#fff}
.toc span{flex:none;width:76px;font:800 22px 'Plus Jakarta Sans';color:#FCDD9E}
.nx{display:flex;align-items:center;gap:26px;border:4px dashed #FCDD9E;border-radius:999px;padding:26px 44px;color:#FCDD9E}
.nx .a{font:800 22px 'Plus Jakarta Sans';letter-spacing:.16em}
.nx .b{font:800 40px 'Plus Jakarta Sans';color:#fff}
.big{font-family:Gloock;color:#FCDD9E;line-height:1;letter-spacing:-.03em}
"""

LAYOUT_JS = """
<script>
function layout(){
 const COLX=%s,Y0=110,RG=%s,ZP=70;const brs=[...document.querySelectorAll('.br')];
 const hts=brs.map(b=>{let m=0;for(const c of b.children)m=Math.max(m,c.offsetTop+c.offsetHeight);return m});
 let y=Y0;
 for(let r=0;r*2<brs.length;r++){
  const idx=[2*r,2*r+1].filter(i=>i<brs.length);const h=Math.max(...idx.map(i=>hts[i]));
  for(const i of idx){const c=r%%2==0?i%%2:1-i%%2;brs[i].style.left=COLX[c]+'px';brs[i].style.top=y+'px';
   if(!brs[i].classList.contains('nz')){const z=document.createElement('div');z.className='zone';
    z.style.cssText=`left:${COLX[c]-ZP}px;top:${y-ZP}px;width:${1800+2*ZP}px;height:${hts[i]+2*ZP}px`;document.body.insertBefore(z,document.body.firstChild)}}
  y+=h+RG+2*ZP}
 const side=document.querySelector('.side');window.FULLH=Math.ceil(Math.max(y,side?side.offsetTop+side.offsetHeight+120:0));
}
</script>""" % (json.dumps(COLX), RG)


def flow(x, y, w, items, gap=30, d="column", style=""):
    ws = f"width:{w}px;" if w else ""
    return f'<div class="flow" style="left:{x}px;top:{y}px;{ws}flex-direction:{d};gap:{gap}px;{style}">{"".join(items)}</div>'


def toc(rows):
    return '<div class="toc">' + "".join(f'<div><span>{n}</span>{t}</div>' for n, t in rows) + "</div>"


def nextnode(nid, label, title_):
    return node(nid, 0, 0, 1800, f'{icon("arrow-down", 64, CH, 2.4)}<div><div class="a">{label}</div><div class="b">{title_}</div></div>', "nx")


def assemble(num, top, big, sub, quote_text, branches, toc_rows, nxt=None, side_extra=""):
    """branches: HTML strings, coords relative to the branch origin, each with topic id t1, t2… in teaching order.
    nxt: (label, title) for the pointer to the next chapter, placed as the last stop on the road."""
    items = list(branches)
    if nxt:
        items.append(nextnode(f"t{len(items) + 1}", *nxt))
    side = (f'<div class="side">{hub("hub", 0, 0, num, top, big, sub)}'
            f'{quote_(0, 0, 1000, quote_text, 54)}'
            f'{toc(toc_rows)}{side_extra}</div>')
    edge("hub", "t1", "gold", sa="r", sb="l", bend=0.35)
    for i in range(len(items) - 1):
        r1, c1 = i // 2, (i % 2 if (i // 2) % 2 == 0 else 1 - i % 2)
        r2, c2 = (i + 1) // 2, ((i + 1) % 2 if ((i + 1) // 2) % 2 == 0 else 1 - (i + 1) % 2)
        if r1 == r2:
            sa, sb = ("r", "l") if c2 > c1 else ("l", "r")
            bend = 0.3
        else:
            sa = sb = "r" if c1 == 1 else "l"
            bend = 0.5
        edge(f"t{i+1}", f"t{i+2}", "gold", sa=sa, sb=sb, bend=bend)
    body = side + "".join(f'<div class="br{" nz" if nxt and k == len(items) - 1 else ""}">{h}</div>' for k, h in enumerate(items))
    return body


CSS += """
.bub{background:#1E3150;border-radius:30px 30px 30px 6px;padding:22px 30px;font:500 27px/1.42 'Plus Jakarta Sans';color:#fff}
.bub.me{background:#FCDD9E;color:#0A1F44;border-radius:30px 30px 6px 30px}
.who{font:800 18px 'Plus Jakarta Sans';letter-spacing:.14em;opacity:.7;margin-bottom:6px;text-transform:uppercase}
.mock{background:#F4F6FA;color:#0A1F44;border-radius:20px;padding:30px 34px;font:500 25px/1.45 'Plus Jakarta Sans'}
.mock .mh{font:800 20px 'Plus Jakarta Sans';letter-spacing:.12em;color:#4A5670;text-transform:uppercase;margin-bottom:12px}
.mock b{color:#0A1F44}
.kv{display:grid;grid-template-columns:260px 1fr;gap:10px 24px}
.kv div:nth-child(odd){font-weight:800;color:#4A5670}
.lab2{font:800 20px 'Plus Jakarta Sans';letter-spacing:.14em;color:#FCDD9E;text-transform:uppercase}
.spk{border-radius:50%;background:#FCDD9E;color:#0A1F44;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font:800 34px/1.1 'Plus Jakarta Sans'}
"""


def L(nid, head, body="", ic="", cls="", w="auto", style=""):
    """A leaf for flows: width auto unless given."""
    return leaf(nid, 0, 0, w, head, body, ic, cls, style)


def big(text, size=90, color=CH):
    return f'<span class="big" style="font-size:{size}px;color:{color}">{text}</span>'


def lab2(text):
    return f'<div class="lab2">{text}</div>'


def bub(nid, text, me=False, who="", w="auto", style=""):
    wh = f'<div class="who">{who}</div>' if who else ""
    return node(nid, 0, 0, w, wh + text, "bub" + (" me" if me else ""), style)


def steps(p, items, kind="gold", d="column", gap=56, w="auto", reveal=None, num=False):
    """A chain of leaves joined by arrows. items: (head, body, ic, cls). reveal: labels (or None) per item."""
    out = []
    for k, it in enumerate(items):
        head, body, ic, cls = (list(it) + ["", "", ""])[:4]
        if num:
            head = f'<span style="font-family:Gloock;color:{NAVY if "gold" in cls else CH};font-size:44px;margin-right:14px">{k+1}</span>' + head
        h = L(f"{p}{k}", head, body, ic, cls, w, "flex:1" if d == "row" else "")
        lab_ = reveal[k] if reveal else None
        out.append(rv(h, lab_, "flex:1;display:flex" if d == "row" else "") if lab_ else h)
    for k in range(len(items) - 1):
        edge(f"{p}{k}", f"{p}{k+1}", kind, sa="b" if d == "column" else "r", sb="t" if d == "column" else "l", bend=0.3)
    return out


def row(items, gap=30, style=""):
    return flow(0, 0, None, items, gap, "row", "align-items:stretch;" + style)


def col(items, gap=30, w=None, style=""):
    return flow(0, 0, w, items, gap, "column", style)


def B(k, num, title_, ic, items, sub="", first=None, gap=44, tw=1800):
    """One branch: topic pill at the origin, a column of content below. first: id the topic points into."""
    if first and not (items and items[0].startswith('<div class="note"')):  # a heading sits in between: the line would cross it
        edge(f"t{k}", first, "line", sa="b", sb="t", bend=0.35)
    return topic(f"t{k}", 0, 0, tw, num, title_, ic, sub) + flow(0, 170, 1800, items, gap)
