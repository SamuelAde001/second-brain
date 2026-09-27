# gen.py: focus spec (timeline frames, frame-normalised u,v with v down) -> per-clip Fusion keys (JSON)
# Coordinates are what the viewer shows under Samuel's inspector framing of the Tella clips.
import json, sys, math
import data

# Adjustment-clip mode: the comp sees the composited 1920x1080 frame, so frame coords map 1:1
VX, VY, VW, VH = 0, 0, 1920, 1080
SW, SH = 1920, 1080
R = 1.0                             # comp frames per timeline frame
DIM = 0.62                          # black overlay opacity outside the focus

def src_norm(u, v):
    return ((VX + u * VW) / SW, 1 - (VY + v * VH) / SH)

# visible window and screen area in source-normalised coords
WX0, WX1 = VX / SW, (VX + VW) / SW
WY0, WY1 = 1 - (VY + VH) / SH, 1 - VY / SH
SX0, SX1 = 0.0, 1.0
SY0, SY1 = 0.0, 1.0   # never above the framing top (keeps menu bar + browser chrome hidden)
V = ((WX0 + WX1) / 2, (WY0 + WY1) / 2)

BIAS = (0.045, 0.035)   # land the focus a little up-left of centre, clear of the camera PIP (bottom right)

def zoom_center(Z, pu, pv):
    k = min(1.0, max(0.0, (Z - 1) / 0.3)) / Z
    pu, pv = pu + BIAS[0] * k, pv + BIAS[1] * k
    px, py = src_norm(pu, pv)
    cx = V[0] - Z * (px - 0.5)
    cy = V[1] - Z * (py - 0.5)
    # keep the screen area covering the visible window
    cx = min(cx, WX0 - Z * (SX0 - 0.5)); cx = max(cx, WX1 - Z * (SX1 - 0.5))
    cy = min(cy, WY0 - Z * (SY0 - 0.5)); cy = max(cy, WY1 - Z * (SY1 - 0.5))
    return cx, cy

def rect_src(r):
    u0, v0, u1, v1 = r
    cx, cy = src_norm((u0 + u1) / 2, (v0 + v1) / 2)
    return cx, cy, (u1 - u0) * VW / SW, (v1 - v0) * VH / SH

def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * t

class Track:
    """States: (frame, dur, Z, (pu,pv), rect or None). Transition runs over [frame, frame+dur]."""
    def __init__(self, states):
        self.s = sorted(states, key=lambda x: x[0])
    def at(self, f):
        prev = (None, 0, 1.0, (0.5, 0.5), None)
        cur = prev
        for st in self.s:
            if f < st[0]:
                break
            prev, cur = cur, st
        if cur[0] is None:
            return 1.0, (0.5, 0.5), None, 0.0
        t = ease((f - cur[0]) / cur[1]) if cur[1] else 1.0
        Z = lerp(prev[2], cur[2], t)
        pa, pb = prev[3], cur[3]
        pa = pa(f) if callable(pa) else pa
        pb = pb(f) if callable(pb) else pb
        P = (lerp(pa[0], pb[0], t), lerp(pa[1], pb[1], t))
        ra, rb = prev[4], cur[4]
        da, db = (1.0 if ra else 0.0), (1.0 if rb else 0.0)
        if ra is None: ra = rb
        if rb is None: rb = ra
        rect = None
        if ra is not None:
            ra, rb = (ra(f) if callable(ra) else ra), (rb(f) if callable(rb) else rb)
            rect = tuple(lerp(a, b, t) for a, b in zip(ra, rb))
        return Z, P, rect, lerp(da, db, t)

def plan(track, blurs, clips):
    """clips: [(start, end)] timeline frames. blurs: [(f0, f1, rect or fn)]. Returns per-clip key dicts."""
    out = []
    for a, b in clips:
        rows = []
        for f in range(a, b + 1):          # +1: a key on the clip's last frame edge
            Z, P, rect, dim = track.at(f)
            cx, cy = zoom_center(Z, *P)
            rr = rect_src(rect) if rect else (0.5, 0.5, 0.2, 0.2)
            bl = [0.0, 0.5, 0.5, 0.1, 0.02]
            for f0, f1, br in blurs:
                if f0 <= f < f1:
                    r = br(f) if callable(br) else br
                    bl = [1.0, *rect_src(r)]
            rows.append((f, [round(Z, 5), round(cx, 5), round(cy, 5), round(dim * DIM, 4),
                             *[round(x, 5) for x in rr], *[round(x, 5) for x in bl]]))
        # does the clip need anything at all?
        ident = [1.0, None, None, 0.0]
        busy = any(r[0] != 1.0 or r[3] > 0 for _, r in rows) or any(r[8] > 0 for _, r in rows)
        if not busy:
            continue
        names = ["Z", "CX", "CY", "DIM", "RX", "RY", "RW", "RH", "BON", "BX", "BY", "BW", "BH"]
        keys = {n: [] for n in names}
        for i, n in enumerate(names):
            last = None
            for j, (f, r) in enumerate(rows):
                v = r[i]
                nxt = rows[j + 1][1][i] if j + 1 < len(rows) else v
                prv = rows[j - 1][1][i] if j > 0 else None
                if j == 0 or j == len(rows) - 1 or v != prv or v != nxt:
                    keys[n].append((round((f - a) * R, 3), v))
            # collapse constant
            if all(k[1] == keys[n][0][1] for k in keys[n]):
                keys[n] = [keys[n][0]]
        out.append({"start": a, "end": b, "blur": any(r[8] > 0 for _, r in rows), "keys": keys})
    return out

class Scroll:
    """Content that scrolls vertically: positions measured at a reference frame follow the tracked offset."""
    def __init__(self, path):
        d = json.load(open(path))
        self.d = {int(k): v for k, v in d.items()}
        self.lo, self.hi = min(self.d), max(self.d)
    def dv(self, f):
        return self.d[min(max(f, self.lo), self.hi)]
    def rect(self, ref, r):
        return lambda f: (r[0], r[1] + self.dv(f) - self.dv(ref), r[2], r[3] + self.dv(f) - self.dv(ref))
    def point(self, ref, r, dy=0.0):
        cu, cv = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2 + dy
        return lambda f: (cu, cv + self.dv(f) - self.dv(ref))

def clips_in(f0, f1):
    return [(a, b) for a, b, s in data.V4 if a >= f0 and b <= f1]
