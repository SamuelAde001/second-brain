"""Build the Called to Edit logo kit as outlined SVGs from glyphs.pdf (Chrome print of glyphs.html)."""
import math, os, re, sys
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "kit")
os.makedirs(OUT, exist_ok=True)

NAVY, MID, CHAMP, BRONZE, WHITE = "#0A1F44", "#071226", "#FCDD9E", "#8A5E17", "#FFFFFF"

NUM = re.compile(r"[MLHVCZ]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?")


def mat_apply(m, x, y):
    a, b, c, d, e, f = m
    return a * x + c * y + e, b * x + d * y + f


def compose(m1, m2):
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return (a1*a2 + c1*b2, b1*a2 + d1*b2, a1*c2 + c1*d2, b1*c2 + d1*d2, a1*e2 + c1*f2 + e1, b1*e2 + d1*f2 + f1)


def flatten(dstr, m):
    """Absolute M/L/H/V/C/Z path -> list of segments in page coords."""
    toks = NUM.findall(dstr)
    segs, i, cur, cmd, start = [], 0, (0.0, 0.0), None, (0.0, 0.0)
    while i < len(toks):
        t = toks[i]
        if t in "MLHVCZ":
            cmd = t
            i += 1
            if cmd == "Z":
                segs.append(("Z",))
                cur = start
            continue
        if cmd in ("M", "L"):
            p = (float(toks[i]), float(toks[i + 1])); i += 2
            segs.append((cmd, mat_apply(m, *p)))
            if cmd == "M":
                start = p
                cmd = "L"
            cur = p
        elif cmd == "H":
            p = (float(toks[i]), cur[1]); i += 1
            segs.append(("L", mat_apply(m, *p))); cur = p
        elif cmd == "V":
            p = (cur[0], float(toks[i])); i += 1
            segs.append(("L", mat_apply(m, *p))); cur = p
        elif cmd == "C":
            ps = [(float(toks[i + k]), float(toks[i + k + 1])) for k in (0, 2, 4)]; i += 6
            segs.append(("C",) + tuple(mat_apply(m, *q) for q in ps)); cur = ps[2]
        else:
            raise ValueError(cmd)
    return segs


def xform(segs, m):
    out = []
    for s in segs:
        if s[0] == "Z":
            out.append(s)
        else:
            out.append((s[0],) + tuple(mat_apply(m, *p) for p in s[1:]))
    return out


def d_of(segs):
    parts = []
    for s in segs:
        if s[0] == "Z":
            parts.append("Z")
        else:
            parts.append(s[0] + " ".join(f"{x:.2f} {y:.2f}" for x, y in s[1:]))
    return "".join(parts)


def bbox(items):
    xs, ys = [], []
    for it in items:
        cur = None
        for s in it["segs"]:
            if s[0] in ("M", "L"):
                cur = s[1]; xs.append(cur[0]); ys.append(cur[1])
            elif s[0] == "C":
                p0 = cur
                p1, p2, p3 = s[1:]
                for k in range(21):
                    t = k / 20
                    x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t*t*p2[0] + t**3*p3[0]
                    y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t*t*p2[1] + t**3*p3[1]
                    xs.append(x); ys.append(y)
                cur = p3
    return min(xs), min(ys), max(xs), max(ys)


def page_items(page):
    svg = page.get_svg_image(text_as_path=True)
    I = (1, 0, 0, 1, 0, 0)
    defs = {k: [(I, d)] for k, d in re.findall(r'<path id="(font_[\d_]+)" d="([^"]*)"', svg)}
    for k, inner in re.findall(r'<g id="(font_[\d_]+)">(.*?)</g>', svg, re.S):
        defs[k] = [(tuple(float(v) for v in mt.split(",")), d) for mt, d in re.findall(r'<path transform="matrix\(([^)]*)\)" d="([^"]*)"', inner)]
    body = svg[svg.find("</defs>"):]
    items = []
    for txt, ref, mt, fill in re.findall(r'<use data-text="([^"]*)" xlink:href="#([^"]+)" transform="matrix\(([^)]*)\)" fill="([^"]+)"', body):
        m = tuple(float(v) for v in mt.split(","))
        segs = []
        for mi, d in defs[ref]:
            segs += flatten(d, compose(m, mi))
        items.append({"text": txt, "segs": segs, "fill": fill.lower(), "origin": (m[4], m[5]), "size": abs(m[3])})
    for mt, d, fill in re.findall(r'<path transform="matrix\(([^)]*)\)" d="([^"]*)" fill="([^"]+)"', body):
        m = tuple(float(v) for v in mt.split(","))
        items.append({"text": "marker", "segs": flatten(d, m), "fill": fill.lower(), "origin": (m[4], m[5]), "size": 0})
    return [it for it in items if it["segs"]]


def moved(items, m):
    return [dict(it, segs=xform(it["segs"], m)) for it in items]


def scale_about(s, tx, ty):
    return (s, 0, 0, s, tx, ty)


pdf = pymupdf.open(os.path.join(HERE, "glyphs.pdf"))
pages = [page_items(p) for p in pdf]
word, kick = pages[0], pages[1]
tags = dict(zip(["academy", "webinar", "mentorship", "community"], pages[2:6]))
ring = pages[6]

W = word[0]["size"]                      # Gloock size in pt (300)
base_y = word[0]["origin"][1]
E = [it for it in word if it["text"] == "E"]
ex0, ecap, ex1, _ = bbox(E)
wx0, wy0, wx1, wy1 = bbox(word)
K = kick[0]["size"]
kx0, kcap, kx1, kbase_bottom = bbox(kick)
k_base = kick[0]["origin"][1]

# Stacked lockup: kicker tucked into the top of the E (his Life of a Video Editor build).
OVERLAP = 0.035 * W
kick_st = moved(kick, (1, 0, 0, 1, (ex0 - 0.004 * W) - kx0, (wy0 - 0.014 * W) - k_base))
GAP = 0.014 * W                           # knockout gap around the kicker where it overlaps the gold

# One-line lockup: "Called" over "to", left of the word, top aligned to the cap.
called = [it for it in kick if it["text"] in "Called"][:6]
to = [it for it in kick if it["text"] in ("t", "o")][-2:]
s_h = 0.9
cx0, ccap, cx1, _ = bbox(called)
tx0, _, tx1, _ = bbox(to)
line1 = moved(called, (s_h, 0, 0, s_h, 0, 0))
c1x0, c1cap, c1x1, _ = bbox(line1)
line1 = moved(line1, (1, 0, 0, 1, -c1x0, ecap - c1cap))
k_base1 = ecap - c1cap + k_base * s_h
line2 = moved(to, (s_h, 0, 0, s_h, 0, 0))
l2x0, _, _, _ = bbox(line2)
line2 = moved(line2, (1, 0, 0, 1, -l2x0, k_base1 + 1.02 * K * s_h - k_base * s_h))
blk_w = max(bbox(line1)[2], bbox(line2)[2])
word_h = moved(word, (1, 0, 0, 1, blk_w + 0.07 * W - ex0, 0))
oneline = line1 + line2 + word_h


def tag_items(name):
    t = tags[name]
    tx0_, tcap, tx1_, tbot = bbox(t)
    s = (0.125 * W) / tags[name][0]["size"]
    t2 = moved(t, (s, 0, 0, s, 0, 0))
    a0, acap, a1, _ = bbox(t2)
    return moved(t2, (1, 0, 0, 1, wx1 + 0.02 * W - a0, ecap - acap))


ROLE = {"#ffffff": "kick", "#fcdd9e": "word", "#ff0000": "tag", "#00ff00": "ring"}
COLOURWAYS = {
    "dark": {"kick": WHITE, "word": CHAMP, "tag": CHAMP},
    "light": {"kick": BRONZE, "word": NAVY, "tag": BRONZE},
    "white": {"kick": WHITE, "word": WHITE, "tag": WHITE},
    "navy": {"kick": NAVY, "word": NAVY, "tag": NAVY},
    "champagne": {"kick": CHAMP, "word": CHAMP, "tag": CHAMP},
}


def render(items, colours, knock=None, pad=0.0, bg=None, title="Called to Edit"):
    x0, y0, x1, y1 = bbox(items)
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    w, h = x1 - x0, y1 - y0
    sh = (1, 0, 0, 1, -x0, -y0)
    items = moved(items, sh)
    groups = {}
    for it in items:
        groups.setdefault(ROLE.get(it["fill"], "word"), []).append(d_of(it["segs"]))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">', f"<title>{title}</title>"]
    if bg:
        out.append(f'<rect width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>')
    word_attr = ""
    if knock is not None and "kick" in groups:
        kd = "".join(groups["kick"])
        out.append(f'<defs><mask id="ko" maskUnits="userSpaceOnUse" x="0" y="0" width="{w:.2f}" height="{h:.2f}"><rect width="{w:.2f}" height="{h:.2f}" fill="#fff"/><path d="{kd}" fill="#000" stroke="#000" stroke-width="{2*knock:.2f}" stroke-linejoin="round"/></mask></defs>')
        word_attr = ' mask="url(#ko)"'
    for role in ("word", "tag", "ring", "kick"):
        if role in groups:
            attr = word_attr if role == "word" else ""
            out.append(f'<path fill="{colours.get(role, CHAMP)}"{attr} d="{"".join(groups[role])}"/>')
    out.append("</svg>")
    return "\n".join(out), (w, h)


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


stacked = word + kick_st
manifest = []
for cw, col in COLOURWAYS.items():
    svg, wh = render(stacked, col, knock=GAP)
    write(f"called-to-edit-logo-{cw}.svg", svg); manifest.append((f"called-to-edit-logo-{cw}.svg", wh))
    svg, wh = render(oneline, col)
    write(f"called-to-edit-logo-oneline-{cw}.svg", svg); manifest.append((f"called-to-edit-logo-oneline-{cw}.svg", wh))
for name in tags:
    for cw in ("dark", "light"):
        svg, wh = render(stacked + tag_items(name), COLOURWAYS[cw], knock=GAP, title=f"Called to Edit {name.title()}")
        write(f"called-to-edit-{name}-{cw}.svg", svg); manifest.append((f"called-to-edit-{name}-{cw}.svg", wh))


def fit(items, box_w, cx, cy):
    x0, y0, x1, y1 = bbox(items)
    s = box_w / (x1 - x0)
    it2 = moved(items, (s, 0, 0, s, 0, 0))
    a0, b0, a1, b1 = bbox(it2)
    return moved(it2, (1, 0, 0, 1, cx - (a0 + a1) / 2, cy - (b0 + b1) / 2))


def icon(items, shape_fill, glyph_fill, shape="circle", box_w=620, dy=0, extra=""):
    it = fit(items, box_w, 500, 500 + dy)
    d = "".join(d_of(i["segs"]) for i in it)
    shp = '<circle cx="500" cy="500" r="500"' if shape == "circle" else '<rect width="1000" height="1000" rx="200"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000" role="img" aria-label="Called to Edit">'
            f'<title>Called to Edit</title>{shp} fill="{shape_fill}"/>{extra}<path fill="{glyph_fill}" d="{d}"/></svg>')


write("called-to-edit-avatar-champagne.svg", icon(word, CHAMP, NAVY))
write("called-to-edit-avatar-navy.svg", icon(word, NAVY, CHAMP))
write("called-to-edit-icon-champagne.svg", icon(E, CHAMP, NAVY, shape="square", box_w=430))
write("called-to-edit-icon-navy.svg", icon(E, NAVY, CHAMP, shape="square", box_w=430))

# Seal: ring text on a circle around the stacked logo.
R = 372.0
rx0, rcap, rx1, rbot = bbox(ring)
r_base = ring[0]["origin"][1]
run = sorted(ring, key=lambda it: it["origin"][0])
x_start = run[0]["origin"][0]
total = (rx1 - x_start) + 0.95 * ring[0]["size"]
s = (2 * math.pi * R) / total
glyphs = []
for it in run:
    ox = it["origin"][0]
    theta = math.pi + ((ox - x_start) * s) / R
    px, py = 500 + R * math.cos(theta), 500 + R * math.sin(theta)
    tx_, ty_ = -math.sin(theta), math.cos(theta)
    ux, uy = math.cos(theta), math.sin(theta)
    # local (lx, ly) relative to glyph origin, scaled: P + lx*t + ly*(-u)
    m = (s * tx_, s * ty_, s * -ux, s * -uy, 0, 0)
    loc = xform(it["segs"], (1, 0, 0, 1, -ox, -r_base))
    seg2 = xform(loc, m)
    seg2 = xform(seg2, (1, 0, 0, 1, px, py))
    glyphs.append(d_of(seg2))
inner, _ = render(fit(stacked, 430, 500, 512), COLOURWAYS["dark"], knock=GAP * 430 / (wx1 - wx0))
inner_paths = inner[inner.find("<defs>") if "<defs>" in inner else inner.find("<path"):inner.rfind("</svg>")]
seal = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000" role="img" aria-label="Called to Edit Academy seal"><title>Called to Edit Academy seal</title>'
        f'<circle cx="500" cy="500" r="496" fill="{NAVY}" stroke="{CHAMP}" stroke-width="8"/>'
        f'<circle cx="500" cy="500" r="452" fill="none" stroke="{CHAMP}" stroke-opacity=".4" stroke-width="3"/>'
        f'<circle cx="500" cy="500" r="300" fill="none" stroke="{CHAMP}" stroke-opacity=".4" stroke-width="3"/>'
        f'<path fill="{CHAMP}" d="{"".join(glyphs)}"/>')
# the inner logo was rendered in its own box: place it with a nested svg
iw, ih = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', inner).groups()
iw, ih = float(iw), float(ih)
seal += f'<svg x="{500 - iw/2:.2f}" y="{500 - ih/2 + 8:.2f}" width="{iw:.2f}" height="{ih:.2f}" viewBox="0 0 {iw:.2f} {ih:.2f}">{inner_paths}</svg></svg>'
write("called-to-edit-seal.svg", seal)

for n, (w, h) in manifest[:2]:
    print(n, round(w), round(h))
print("files:", len(os.listdir(OUT)))
print("W", W, "capTop", round(ecap, 1), "base", base_y, "E left", round(ex0, 1), "word box", [round(v, 1) for v in (wx0, wy0, wx1, wy1)])
