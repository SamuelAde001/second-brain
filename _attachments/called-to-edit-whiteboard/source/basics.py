"""Beginners class, Fri 2026-11-06: the 8 steps of tonight's class as clips on an editing timeline, on the same navy board
as journey.py. Order and times from 04-Projects/called-to-edit-community-beginners-class.md (Samuel's six principles,
2026-11-06, "Put this all in order of the teaching"). Outline words only: he explains them live.
Build: python native.py basics  ->  out/native/beginners-class-basics.json"""
from maplib import reset
from lib import icon

NAME = "beginners-class-basics"
W, H = 6400, 2330
NAVY, MID, SLATE, EDGE, CH, MIST, WHITE = "#0A1F44", "#071226", "#1E3150", "#2E4A78", "#FCDD9E", "#B9C3D6", "#FFFFFF"

# (time, name, icon, band, points): band = film (picture), wave (sound), done (finish)
CLIPS = [
    ("00:06", "Editing for Your Audience", "users", "film", ["Who is watching?", "Where will they watch?", "What should they feel or do?"]),
    ("00:11", "Storytelling", "book-open", "film", ["Hook", "Setup", "Payoff", "Ending"]),
    ("00:19", "Cutting", "scissors", "film", ["Split", "Delete", "Close the gap", "Keep the best take"]),
    ("00:28", "Pacing", "timer", "film", ["New information, not fast cuts", "Change the rhythm", "The boredom test"]),
    ("00:34", "Composition", "crosshair", "film", ["One focus per frame", "Eyes on the top third", "Safe zones", "Show, don't tell"]),
    ("00:41", "Sound", "mic-vocal", "wave", ["Voice first", "Music under it", "Ducking", "Check on your phone"]),
    ("00:48", "SFX", "zap", "wave", ["Whoosh", "Pop", "Impact", "Riser", "Ambience"]),
    ("00:53", "Export", "smartphone", "done", ["1080 × 1920", "Same frame rate", "Watch it on your phone"]),
]

X0, GAP = 150, 30
CW = (W - 2 * X0 - 7 * GAP) // 8
RULER, TRACK, TRACK_END = (930, 1010), 1060, 1990


def rect(x, y, w, h, fill, extra=""):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{fill};{extra}"></div>'


def band(k, x, kind):
    bx, by, bw, bh = x + 24, TRACK + 24, CW - 48, 84
    if kind == "film":  # a film strip: perforations on gold
        out = rect(bx, by, bw, bh, CH, "border-radius:14px")
        n = 8
        step = (bw - 40) / n
        out += "".join(rect(round(bx + 20 + j * step + (step - 34) / 2), by + 20, 34, 44, NAVY, "border-radius:6px") for j in range(n))
        return out
    if kind == "wave":  # a waveform: gold bars of varying height
        out = rect(bx, by, bw, bh, SLATE, "border-radius:14px")
        hs = [18, 34, 52, 30, 62, 44, 24, 56, 70, 38, 20, 48, 64, 28, 42, 58, 32, 16, 46, 60, 26, 40, 54, 22, 36]
        hs = [hs[(j + 7 * k) % len(hs)] for j in range(23)]
        bw2 = (bw - 40) / len(hs)
        return out + "".join(rect(round(bx + 20 + j * bw2 + 4), round(by + bh / 2 - h / 2), max(int(bw2 - 8), 6), h, CH, "border-radius:4px") for j, h in enumerate(hs))
    return rect(bx, by, bw, bh, CH, "border-radius:14px")  # the finish: plain gold


def clip(k):
    t, name, ic, kind, pts = CLIPS[k]
    x = X0 + k * (CW + GAP)
    body = rect(x, TRACK, CW, TRACK_END - TRACK, NAVY, f"border:4px solid {EDGE};border-radius:28px;box-sizing:border-box")
    tick = rect(x, RULER[0], 6, RULER[1] - RULER[0] + 20, CH)
    stamp = (f'<div class="n" id="t{k}" style="position:absolute;left:{x + (60 if k == 0 else 22)}px;top:{RULER[0] + 16}px">'
             f'<span style="font:800 40px \'Plus Jakarta Sans\';letter-spacing:.06em;color:{CH}">{t}</span></div>')
    bullets = "".join(
        f'<div style="display:flex;align-items:flex-start;gap:22px"><div style="flex:none;width:16px;height:16px;margin-top:18px;background:{CH};border-radius:3px"></div>'
        f'<span style="font:400 50px/1.2 \'Plus Jakarta Sans\';color:{MIST}">{p}</span></div>' for p in pts)
    text = (f'<div class="n" id="c{k}" style="position:absolute;left:{x + 48}px;top:{TRACK + 150}px;width:{CW - 96}px;display:flex;flex-direction:column">'
            f'<div style="display:flex;align-items:center;justify-content:space-between">'
            f'<span style="font:400 150px/1 Gloock;color:{CH}">{k + 1}</span></div>'
            f'<div style="font:700 60px/1.1 \'Plus Jakarta Sans\';color:{WHITE};margin:34px 0 44px">{name}</div>'
            f'<div style="display:flex;flex-direction:column;gap:22px">{bullets}</div></div>')
    return tick + body + band(k, x, kind) + stamp + text


def build():
    reset()
    size = f'<div class="side" style="height:{H - 220}px;padding:0;gap:0"></div>'  # sets the measured height
    panel = rect(0, 0, W, H, MID, "border-radius:64px")
    title = (f'<div class="n" id="title" style="position:absolute;left:150px;top:150px;width:4200px">'
             f'<div style="font:600 84px \'Plus Jakarta Sans\';color:{WHITE}">Beginners Class</div>'
             f'<div style="font:400 250px/0.95 Gloock;color:{CH};letter-spacing:-.03em">The Basics of Every Edit</div></div>')
    rule = (f'<div class="n" id="rule" style="position:absolute;left:150px;top:640px;width:5200px">'
            f'<span style="font:400 64px/1.2 \'Plus Jakarta Sans\';color:{MIST}">Every cut, sound, text and B-roll must help the viewer </span>'
            f'<span style="font:700 64px/1.2 \'Plus Jakarta Sans\';color:{CH}">understand</span>'
            f'<span style="font:400 64px/1.2 \'Plus Jakarta Sans\';color:{MIST}"> or </span>'
            f'<span style="font:700 64px/1.2 \'Plus Jakarta Sans\';color:{CH}">feel</span>'
            f'<span style="font:400 64px/1.2 \'Plus Jakarta Sans\';color:{MIST}">.</span></div>')
    logo = f'<img src="kit/called-to-edit-logo-dark.svg" style="position:absolute;left:{W - 540}px;top:150px;width:380px">'
    ruler = rect(X0, RULER[0], W - 2 * X0, RULER[1] - RULER[0], NAVY, "border-radius:12px")
    ticks = "".join(rect(X0 + 40 + j * 48, RULER[1] - 22, 4, 22, EDGE) for j in range((W - 2 * X0 - 80) // 48))
    clips = "".join(clip(k) for k in range(8))
    px = X0 + 10  # the playhead, parked at the start
    playhead = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0">'
                f'<path d="M{px - 34} {RULER[0] - 40}H{px + 34}V{RULER[0] + 10}L{px} {RULER[0] + 50}L{px - 34} {RULER[0] + 10}z" fill="{WHITE}"/>'
                f'<path d="M{px - 4} {RULER[0] + 40}H{px + 4}V{TRACK_END + 30}H{px - 4}z" fill="{WHITE}"/></svg>')
    homework = (f'<div class="n" id="hw" style="position:absolute;left:150px;top:{TRACK_END + 110}px;width:5600px;display:flex;align-items:center;gap:36px">'
                f'<span style="font:800 40px \'Plus Jakarta Sans\';letter-spacing:.06em;color:{CH}">00:55</span>'
                f'<span style="font:700 60px \'Plus Jakarta Sans\';color:{WHITE}">Homework: your first full edit</span>'
                f'<span style="font:400 60px \'Plus Jakarta Sans\';color:{MIST}">· post it in #feedback · Q&amp;A</span></div>')
    return size + panel + title + rule + logo + ruler + ticks + clips + playhead + homework, W, H
