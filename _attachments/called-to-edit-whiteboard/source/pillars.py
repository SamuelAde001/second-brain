"""The 5 things that get you clients (Samuel, 2026-11-04: "Outreach Visibility, Competence, Recommendation, Networking"),
as five pillars holding up "Clients", on the same navy board as journey.py. Only his five words.
Build: C2E_DESIGN=<id> C2E_DOC=<doc> python native.py pillars  ->  out/native/five-things-clients.json"""
from maplib import reset

NAME = "five-things-clients"
W, H = 4000, 2300
NAVY, MID, SLATE, EDGE, CH, WHITE = "#0A1F44", "#071226", "#1E3150", "#33507E", "#FCDD9E", "#FFFFFF"
THINGS = ["Outreach", "Visibility", "Competence", "Recommendation", "Networking"]

CW, GAP = 560, 100
X0 = (W - (5 * CW + 4 * GAP)) // 2
L, R = X0 - 60, W - X0 + 60
ROOF_TOP, ROOF_BASE, ARCH = 700, 990, (1000, 1070)
CAP, SHAFT, BASE = (1090, 1140), (1140, 1860), (1860, 1910)


def rect(x, y, w, h, fill, extra=""):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{fill};{extra}"></div>'


def column(k):
    x = X0 + k * (CW + GAP)
    flutes = "".join(rect(x + 70 + j * 84, SHAFT[0] + 300, 14, 300, NAVY) for j in range(6))
    label = (f'<div class="n" id="c{k}" style="position:absolute;left:{x}px;top:{SHAFT[0]}px;width:{CW}px;height:{SHAFT[1] - SHAFT[0]}px;'
             f'display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:50px 0 70px;box-sizing:border-box">'
             f'<span style="font:400 190px/1 Gloock;color:{CH}">{k + 1}</span>'
             f'<span style="font:700 60px/1.1 \'Plus Jakarta Sans\';color:{WHITE}">{THINGS[k]}</span></div>')
    return (rect(x - 24, CAP[0], CW + 48, CAP[1] - CAP[0], CH) + rect(x, SHAFT[0], CW, SHAFT[1] - SHAFT[0], SLATE)
            + flutes + rect(x - 24, BASE[0], CW + 48, BASE[1] - BASE[0], CH) + label)


def build():
    reset()
    size = f'<div class="side" style="height:{H - 220}px;padding:0;gap:0"></div>'  # sets the measured height
    panel = rect(0, 0, W, H, MID, "border-radius:64px")
    title = (f'<div class="n" id="title" style="position:absolute;left:150px;top:150px;width:2400px">'
             f'<div style="font:600 84px \'Plus Jakarta Sans\';color:{WHITE}">The 5 things that</div>'
             f'<div style="font:400 250px/0.95 Gloock;color:{CH};letter-spacing:-.03em">Get You Clients</div></div>')
    roof = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0">'
            f'<path d="M{L} {ROOF_BASE}L{W // 2} {ROOF_TOP}L{R} {ROOF_BASE}z" fill="{CH}"/></svg>')
    roof_word = (f'<div class="n" id="roof" style="position:absolute;left:{W // 2 - 500}px;top:{ROOF_BASE - 150}px;width:1000px;text-align:center">'
                 f'<span style="font:800 64px \'Plus Jakarta Sans\';letter-spacing:.3em;color:{NAVY}">CLIENTS</span></div>')
    arch = rect(L, ARCH[0], R - L, ARCH[1] - ARCH[0], EDGE)
    steps = rect(L, 1930, R - L, 60, EDGE) + rect(L - 70, 1990, R - L + 140, 60, SLATE)
    logo = f'<img src="kit/called-to-edit-logo-dark.svg" style="position:absolute;left:{W - 540}px;top:150px;width:380px">'
    cols = "".join(column(k) for k in range(5))
    return size + panel + title + logo + roof + roof_word + arch + cols + steps, W, H
