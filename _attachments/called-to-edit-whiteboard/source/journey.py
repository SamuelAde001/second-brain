"""The Journey of a Video Editor: the eight steps from Samuel's whiteboard (photo, 2026-11-04), word for word,
as one winding road on a navy board. Only the steps: he explains them live (Samuel, 2026-11-04: "Don't add other
details to the pathway, just the pathway, I would explain it myself").
Build: C2E_DESIGN=<id> C2E_DOC=<doc> python native.py journey  ->  out/native/journey-video-editor.json"""
import math
from maplib import reset
from lib import icon

NAME = "journey-video-editor"
W, H = 4000, 2300
NAVY, MID, SLATE, CH, MIST, WHITE = "#0A1F44", "#071226", "#1E3150", "#FCDD9E", "#B9C3D6", "#FFFFFF"

STEPS = ["Learn the Software", "Learn the Skill of Editing", "Become Visible", "Position Yourself to a Certain Client",
         "Start to Outreach", "Close Your First Clients", "Build a Bigger Network", "Offer More Than Video Editing"]

# the road climbs from bottom left to top right; valleys (odd steps) carry their label below, peaks above
START, END = (60, 1420), (3800, 640)
PINS = [(400, 1760), (880, 1330), (1370, 1700), (1850, 1200), (2330, 1540), (2790, 1020), (3230, 1300), (3530, 800)]


def bez(pts):
    """Catmull-Rom through the points, as cubic segments."""
    segs = []
    for i in range(len(pts) - 1):
        p0, p1, p2 = pts[max(i - 1, 0)], pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        segs.append((p1, c1, c2, p2))
    return segs


def at(s, t):
    (a, b, c, d), u = s, 1 - t
    return tuple(u ** 3 * a[k] + 3 * u * u * t * b[k] + 3 * u * t * t * c[k] + t ** 3 * d[k] for k in (0, 1))


def band(pts, half):
    """A closed outline 2*half wide around a sampled centre line (Canva fills shapes; it doesn't stroke open curves)."""
    left, right = [], []
    for i, p in enumerate(pts):
        q0, q1 = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        dx, dy = q1[0] - q0[0], q1[1] - q0[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * half, dx / L * half
        left.append((p[0] + nx, p[1] + ny)); right.append((p[0] - nx, p[1] - ny))
    ring = left + right[::-1]
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in ring) + "z"


def road():
    segs = bez([START] + PINS + [END])
    pts = [at(sg, k / 120) for sg in segs for k in range(120)] + [END]
    dashes, run, on, cur = [], 0.0, True, [pts[0]]
    for p, q in zip(pts, pts[1:]):
        run += math.dist(p, q)
        if on:
            cur.append(q)
        if run >= (46 if on else 38):
            if on and len(cur) > 1:
                dashes.append(band(cur, 5))
            run, on, cur = 0.0, not on, [q]
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0">'
            f'<path d="{band(pts, 98)}" fill="#33507E"/>'
            f'<path d="{band(pts, 86)}" fill="{SLATE}"/>'
            f'<path d="{"".join(dashes)}" fill="{CH}"/></svg>')


def pin(k, x, y):
    n = k + 1
    below = n % 2 == 1
    ring = (f'<svg width="224" height="224" viewBox="0 0 224 224" style="position:absolute;left:{x - 112}px;top:{y - 112}px">'
            f'<circle cx="112" cy="112" r="109" fill="{NAVY}" stroke="{CH}" stroke-width="6"/><circle cx="112" cy="112" r="84" fill="{CH}"/></svg>'
            f'<div class="n" id="p{n}" style="position:absolute;left:{x - 112}px;top:{y - 112}px;width:224px;height:224px;display:flex;align-items:center;justify-content:center">'
            f'<span style="font:400 112px/1 Gloock;color:{NAVY};margin-top:6px">{n}</span></div>')
    cw = 620
    cx = x - cw + 120 if n == 8 else min(max(x - cw / 2, 60), W - cw - 60)
    stem_top, stem_h = (y + 112, 70) if below else (y - 182, 70)
    stem = f'<div style="position:absolute;left:{x - 3}px;top:{stem_top}px;width:6px;height:{stem_h}px;background:{CH}"></div>'
    card = (f'<div class="n" id="c{n}" style="position:{'absolute' if below else 'relative'};left:{cx if below else 0}px;top:{y + 182 if below else 0}px;width:{cw}px;box-sizing:border-box;padding:34px 40px 38px;'
            f'background:{NAVY};border:4px solid #2E4A78;border-radius:28px">'
            f'<div style="font:800 26px \'Plus Jakarta Sans\';letter-spacing:.18em;color:{CH};margin-bottom:12px">STEP {n:02d}</div>'
            f'<div style="font:700 56px/1.12 \'Plus Jakarta Sans\';color:{WHITE}">{STEPS[k]}</div></div>')
    if not below:  # a column that ends at the stem, so the card sits on it whatever its height
        card = f'<div style="position:absolute;left:{cx}px;top:0;height:{y - 182}px;display:flex;flex-direction:column;justify-content:flex-end">{card}</div>'
    return stem + card + ring


def build():
    reset()
    panel = f'<div style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;background:{MID};border-radius:64px"></div>'
    title = (f'<div class="n" id="title" style="position:absolute;left:150px;top:150px;width:2000px">'
             f'<div style="font:600 84px \'Plus Jakarta Sans\';color:{WHITE}">The Journey of a</div>'
             f'<div style="font:400 250px/0.95 Gloock;color:{CH};letter-spacing:-.03em">Video Editor</div></div>')
    flag = (f'<div class="n" id="flag" style="position:absolute;left:{END[0] - 70}px;top:{END[1] - 290}px">'
            f'{icon("flag", 200, CH, 2)}</div>')
    logo = f'<img src="kit/called-to-edit-logo-dark.svg" style="position:absolute;left:{W - 540}px;top:{H - 330}px;width:380px">'
    pins = "".join(pin(k, x, y) for k, (x, y) in enumerate(PINS))
    size = f'<div class="side" style="height:{H - 220}px;padding:0;gap:0"></div>'  # sets the measured height (layout reads .side)
    return size + panel + road() + title + flag + logo + pins, W, H
