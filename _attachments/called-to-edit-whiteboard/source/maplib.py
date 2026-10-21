"""Mind-map building blocks for the webinar whiteboard: free-placed nodes joined by drawn connectors.
Each chapter is one big canvas. Connectors are drawn by a script after layout, from the node edges."""
import json
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
    return f'<div class="n {cls}" id="{nid}" style="left:{x}px;top:{y}px;width:{w}px;{style}">{inner}</div>'


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
.tt{font:800 36px/1.1 'Plus Jakarta Sans';letter-spacing:-.02em}
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
  const p=side(ra,s1),q=side(rb,s2);const d=Math.hypot(q[0]-p[0],q[1]-p[1])*bend;
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
window.addEventListener('load',()=>document.fonts.ready.then(()=>{drawEdges();
 const out=[];document.querySelectorAll('.rv').forEach((e,i)=>{const r=e.getBoundingClientRect();out.push({i,label:e.dataset.label,x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height)})});
 const p=document.createElement('script');p.type='application/json';p.id='pos';p.textContent=JSON.stringify({w:document.body.scrollWidth,h:document.body.scrollHeight,rv:out});document.head.appendChild(p);}));
</script>"""


def page(body, w, h, name):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{name}</title>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="board.css"><style>{CSS}
@page{{size:{w}px {h}px;margin:0}} html,body{{width:{w}px;height:{h}px;overflow:hidden;background:transparent}}
#edges{{position:absolute;left:0;top:0}}</style>
<script>window.EDGES={json.dumps(EDGES)};</script>{EDGE_JS}</head>
<body><svg id="edges" width="{w}" height="{h}" viewBox="0 0 {w} {h}"></svg>{body}</body></html>"""
