"""v2 kit: product name under the logo, round-dot versions, product avatars. Runs build_kit (v1) first, then overwrites/adds."""
import os, sys
sys.argv = [sys.argv[0], os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit")]
import build_kit as K

W, kick, tags, pages = K.W, K.kick, K.tags, K.pages
word_m, word_d = K.word, pages[7]
bbox, moved, render, write, icon = K.bbox, K.moved, K.render, K.write, K.icon
NAVY, CHAMP, BRONZE, WHITE = K.NAVY, K.CHAMP, K.BRONZE, K.WHITE

for cw in K.COLOURWAYS.values():      # the product name takes the kicker's colour
    cw["tag"] = cw["kick"]


def stack_for(wd):
    x0, y0, x1, y1 = bbox(wd)
    ex0 = bbox([it for it in wd if it["text"] == "E"])[0]
    ks = moved(kick, (1, 0, 0, 1, (ex0 - 0.004 * W) - K.kx0, (y0 - 0.014 * W) - K.k_base))
    return wd + ks


def oneline_for(wd):
    return K.line1 + K.line2 + moved(wd, (1, 0, 0, 1, K.blk_w + 0.07 * W - K.ex0, 0))


def tag_under(name, wd, h=0.105, gap=0.085):
    """Product name in caps under the word, letters spread to the word's exact width."""
    t = tags[name]
    _, tcap, _, tbot = bbox(t)
    s = (h * W) / (tbot - tcap)
    gl = sorted(moved(t, (s, 0, 0, s, 0, 0)), key=lambda it: it["origin"][0])
    x0, _, x1, y1 = bbox(wd)
    target = x1 - x0
    boxes = [bbox([g]) for g in gl]
    natural = boxes[-1][2] - boxes[0][0]
    if natural > target:
        f = target / natural
        gl = sorted(moved(gl, (f, 0, 0, f, 0, 0)), key=lambda it: it["origin"][0])
        boxes = [bbox([g]) for g in gl]
    widths = [b[2] - b[0] for b in boxes]
    space = (target - sum(widths)) / (len(gl) - 1)
    cap = min(b[1] for b in boxes)
    out, x = [], x0
    for g, b, wd_ in zip(gl, boxes, widths):
        out += moved([g], (1, 0, 0, 1, x - b[0], (y1 + gap * W) - cap))
        x += wd_ + space
    return out


made = []
st_m, st_d = stack_for(word_m), stack_for(word_d)
for name in tags:
    for cw in ("dark", "light", "white"):
        svg, _ = render(st_m + tag_under(name, word_m), K.COLOURWAYS[cw], title=f"Called to Edit {name.title()}")
        write(f"called-to-edit-{name}-{cw}.svg", svg); made.append(f"{name}-{cw}")
    # product profile picture: Edit + name, navy on champagne
    it = K.fit(word_m + tag_under(name, word_m, h=0.2, gap=0.1), 600, 500, 500)
    d = "".join(K.d_of(i["segs"]) for i in it)
    write(f"called-to-edit-avatar-{name}.svg",
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000" role="img" aria-label="Called to Edit {name.title()}"><title>Called to Edit {name.title()}</title><circle cx="500" cy="500" r="500" fill="{CHAMP}"/><path fill="{NAVY}" d="{d}"/></svg>')
    made.append(f"avatar-{name}")

for cw, col in K.COLOURWAYS.items():
    svg, _ = render(st_d, col, title="Called to Edit")
    write(f"called-to-edit-logo-{cw}-dot.svg", svg); made.append(f"logo-{cw}-dot")
for cw in ("dark", "light"):
    svg, _ = render(oneline_for(word_d), K.COLOURWAYS[cw])
    write(f"called-to-edit-logo-oneline-{cw}-dot.svg", svg); made.append(f"logo-oneline-{cw}-dot")
write("called-to-edit-avatar-champagne-dot.svg", icon(word_d, CHAMP, NAVY))
write("called-to-edit-avatar-navy-dot.svg", icon(word_d, NAVY, CHAMP))
print("v2 files:", len(made) + 2, "kit total:", len(os.listdir(K.OUT)))
