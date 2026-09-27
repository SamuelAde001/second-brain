# track.py f0 f1 u0 u1 v0 v1 out.json -> vertical scroll of the content in a column, per timeline frame
# dv[f] = how far (in v units, down positive) content has moved since frame f0.
import sys, json, subprocess
import data

f0, f1 = int(sys.argv[1]), int(sys.argv[2])
u0, u1, v0, v1 = map(float, sys.argv[3:7])
out = sys.argv[7]
H, W = 540, 960
x, y, w, h = data.VIEW
cx0, cx1 = int(u0 * W), int(u1 * W)
cw = cx1 - cx0
r0, r1 = int(v0 * H), int(v1 * H)

def frames(a, b, s):
    vf = f"crop={w}:{h}:{x}:{y},scale={W}:{H},crop={cw}:{H}:{cx0}:0,format=gray"
    p = subprocess.run([data.FF, '-hide_banner', '-loglevel', 'error', '-ss', f'{s:.4f}', '-i', data.TELLA,
                        '-frames:v', str(b - a), '-r', '24000/1001', '-vf', vf, '-f', 'rawvideo', '-'],
                       capture_output=True)
    raw = p.stdout
    n = len(raw) // (cw * H)
    profs = []
    for i in range(n):
        fr = raw[i * cw * H:(i + 1) * cw * H]
        profs.append([sum(fr[r * cw:(r + 1) * cw]) / cw for r in range(H)])
    while len(profs) < b - a:
        profs.append(profs[-1])
    return profs

def best_lag(p, q, lmax):
    # content moved by L: p[y] ~ q[y - L]
    best, bl = None, 0
    for L in range(-lmax, lmax + 1):
        lo, hi = max(r0, r0 + L), min(r1, r1 + L)
        if hi - lo < 60:
            continue
        s = 0.0
        for yy in range(lo, hi):
            s += abs(p[yy] - q[yy - L])
        s /= (hi - lo)
        if best is None or s < best - 1e-9:
            best, bl = s, L
    return bl, best

res = {}
acc = 0
prev = None
for a, b, s in data.V4:
    if b <= f0 or a >= f1:
        continue
    aa, bb = max(a, f0), min(b, f1)
    ps = frames(aa, bb, s + (aa - a) / data.FPS)
    for i, p in enumerate(ps):
        f = aa + i
        if prev is not None:
            l0 = sum(abs(p[yy] - prev[yy]) for yy in range(r0, r1)) / (r1 - r0)
            if l0 > 0.4:
                L, sc = best_lag(p, prev, 300 if i == 0 else 60)
                acc += L
        res[f] = round(acc / H, 4)
        prev = p
json.dump(res, open(out, 'w'))
ks = sorted(res)
chg = [(f, res[f]) for j, f in enumerate(ks) if j == 0 or res[f] != res[ks[j - 1]]]
print(len(res), "changes:", chg[:80])
