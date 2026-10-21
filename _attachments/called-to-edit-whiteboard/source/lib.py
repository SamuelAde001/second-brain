"""Building blocks for the Called to Edit webinar whiteboard. Each frame is 1920 x 1080."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, GAP = 1920, 1080, 420
NAVY, MID, SLATE, CH, BRONZE, MIST = "#0A1F44", "#071226", "#1E3150", "#FCDD9E", "#8A5E17", "#B9C3D6"

_icon_cache = {}


def icon(name, size=56, color=CH, sw=1.8):
    if name not in _icon_cache:
        fp = os.path.join(HERE, "kit", "icons", name + ".svg")
        if not os.path.exists(fp):  # Lucide (ISC licence), pinned version
            import urllib.request
            urllib.request.urlretrieve(f"https://cdn.jsdelivr.net/npm/lucide-static@0.460.0/icons/{name}.svg", fp)
        s = open(fp, encoding="utf-8").read()
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        s = re.sub(r"<svg[^>]*>", lambda m: re.sub(r'\s(class|width|height|stroke|stroke-width)="[^"]*"', "", m.group(0)), s, count=1)
        _icon_cache[name] = s.strip()
    s = _icon_cache[name]
    return s.replace("<svg", f'<svg width="{size}" height="{size}" stroke="{color}" stroke-width="{sw}" style="flex:none"', 1)


MARK = f'<svg width="20" height="23" viewBox="0 0 14 16" style="flex:none"><path d="M0 0H14V9.6L7 16L0 9.6Z" fill="{CH}"/></svg>'


def mark(size=20, color=CH):
    return f'<svg width="{size}" height="{size*16/14:.0f}" viewBox="0 0 14 16" style="flex:none"><path d="M0 0H14V9.6L7 16L0 9.6Z" fill="{color}"/></svg>'


def lab(text):
    return f'<div class="lab">{MARK}<span>{text}</span></div>'


def title(top, big, size=120):
    return f'<div class="ttl"><div class="tl">{top}</div><div class="bw" style="font-size:{size}px">{big}</div></div>'


def card(ic, head, body="", style="", cls=""):
    i = icon(ic, 52) if ic else ""
    b = f'<div class="cb">{body}</div>' if body else ""
    return f'<div class="card {cls}" style="{style}">{i}<div class="ct">{head}</div>{b}</div>'


def ph(label, style="", src=None, fit="cover", pos="center"):
    """Photo or screenshot slot. With src it shows the image; without, a labelled placeholder."""
    if src:
        return f'<div class="phi" style="{style}"><img src="{src}" style="object-fit:{fit};object-position:{pos}"></div>'
    return f'<div class="ph" style="{style}">{icon("camera", 44, MIST)}<span>{label}</span></div>'


def demo(what, where="", style=""):
    w = f'<div class="dw">{where}</div>' if where else ""
    return (f'<div class="demo" style="{style}">{icon("monitor-play", 54, NAVY, 2.2)}'
            f'<div><div class="dl">LIVE DEMO · switch to Chrome</div><div class="dt">{what}</div>{w}</div></div>')


def journey(text, style=""):
    return f'<div class="jr" style="{style}"><div class="jl">{mark(16)}<span>FROM MY JOURNEY</span></div><div class="jt">{text}</div></div>'


def remember(text, style="", head="Remember"):
    return f'<div class="rem" style="{style}"><div class="rl">{mark(16, NAVY)}<span>{head.upper()}</span></div><div class="rt">{text}</div></div>'


def doit(text, style=""):
    return f'<div class="doit" style="{style}"><div class="rl">{icon("list-checks", 30, CH, 2)}<span>DO THIS</span></div><div class="rt">{text}</div></div>'


def quote(text, size=64, style=""):
    return f'<div class="qt" style="font-size:{size}px;{style}">&ldquo;{text}&rdquo;</div>'


def rv(inner, label, style="", tag="div"):
    """A part covered by a reveal sticky. label is the teaser written on the sticky."""
    return f'<{tag} class="rv" data-label="{label}" style="{style}">{inner}</{tag}>'


def arrow(x1, y1, x2, y2, color=CH, w=6, head=True, dash=False):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx1, hy1 = x2 - 30 * math.cos(a - 0.45), y2 - 30 * math.sin(a - 0.45)
    hx2, hy2 = x2 - 30 * math.cos(a + 0.45), y2 - 30 * math.sin(a + 0.45)
    d = ' stroke-dasharray="4 18"' if dash else ""
    h = f'<path d="M{hx1:.0f} {hy1:.0f} L{x2} {y2} L{hx2:.0f} {hy2:.0f}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>' if head else ""
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"{d}/>{h}'


def svg(inner, style="position:absolute;left:0;top:0", w=W, h=H):
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="{style};overflow:visible">{inner}</svg>'


def frame(fid, label, body, cls=""):
    return (f'<section class="frame {cls}" data-id="{fid}">{lab(label)}{body}'
            f'<div class="fid">{fid}</div></section>')


def opener(n, top, big, sub, q, extra=""):
    return (f'<section class="frame op" data-id="{n}.0">'
            f'<img class="oplogo" src="kit/called-to-edit-logo-dark.svg">'
            f'<div class="opn">{n}</div>'
            f'<div class="opt">{lab("Chapter " + str(n))}<div class="tl" style="font-size:52px">{top}</div>'
            f'<div class="bw" style="font-size:150px">{big}</div><div class="ops">{sub}</div></div>'
            f'<div class="opq">{mark(26)}<span>&ldquo;{q}&rdquo;</span></div>{extra}'
            f'<div class="fid">{n}.0</div></section>')


CSS = open(os.path.join(HERE, "board.css"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "board.css")) else ""


def page(frames, name):
    n = len(frames)
    width = n * W + (n - 1) * GAP
    placed = []
    for i, f in enumerate(frames):
        left = i * (W + GAP)
        placed.append(f.replace('<section class="frame', f'<section style="left:{left}px" class="frame', 1))
    arrows = "".join(
        svg(arrow(i * (W + GAP) + W + 70, H // 2, (i + 1) * (W + GAP) - 70, H // 2, w=8),
            style="position:absolute;left:0;top:0", w=width, h=H) for i in range(n - 1))
    pos_js = """<script>
window.addEventListener('load',()=>{document.fonts.ready.then(()=>{const out=[];
document.querySelectorAll('.rv').forEach((e,i)=>{const r=e.getBoundingClientRect();out.push({i,label:e.dataset.label,x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height)})});
const p=document.createElement('script');p.type='application/json';p.id='pos';p.textContent=JSON.stringify({w:document.body.scrollWidth,h:%d,rv:out});document.head.appendChild(p);});});
</script>""" % H
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{name}</title>
<link href="https://fonts.googleapis.com/css2?family=Gloock&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="board.css">
<style>@page{{size:{width}px {H}px;margin:0}} body{{width:{width}px;height:{H}px}}</style>{pos_js}</head>
<body>{arrows}{"".join(placed)}</body></html>"""
