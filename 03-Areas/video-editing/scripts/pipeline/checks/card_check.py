# Build-card rules the beat lint does not check (S1 S2 S4 S5 BR SQ FONT TXT BEV), read from Fusion .setting files; one line per comp, exit 1 on any FAIL.
# Usage: python card_check.py <comp.setting | folder> [...] [--exempt <name token>]
# Promoted from video 4 on 2026-10-30.
# card_check.py - the build-card rules the beat lint does not check (editor-builder, night run 2026-10-28).
# Checks (04 BUILD CARD.md): S2 motion blur off | S1 a static NeoLightSweep per box | BR corner brackets per box |
# SQ square corners | FONT Inter only | TXT NeoTextMotion rises (PosDir 0) with its shine on (M11) |
# BEV Neo Bevel switched off | S4 a growing push (comps without MediaIn) | S5 NeoAnim + Vignette (comps with MediaIn).
# Box = a top-level tool named Background_<x>Fill (frkit.box / frkit.glass naming). Heuristic: read the WARNs.
# Exempt by design: Samuel's own intro adj clip (file name holds 'samuel_intro_adj'; S6, see CONFLICTS in the card).
import argparse, re, sys, os, glob

def blocks(t):
    """Top-level tools: name -> (type, text)."""
    out, it = {}, list(re.finditer(r'\n\t\t(\w+) = ([\w.]+) \{', t))
    for i, m in enumerate(it):
        end = it[i + 1].start() if i + 1 < len(it) else len(t)
        out[m.group(1)] = (m.group(2), t[m.start():end])
    return out

def keys(btxt):
    return [float(v) for v in re.findall(r'\[\s*-?[\d.]+\s*\]\s*=\s*\{\s*(-?[\d.eE+-]+)', btxt)]

def check(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    B = blocks(t)
    R, W = {}, []
    # A MotionBlur = 1 counts only if its tool is live: NeoAnim keeps MotionBlur 1 on its inner NAMotionBlur Transform
    # and switches it off with PassThrough = true (his macro's MotionBlur On/Off buttons).
    mb = []
    for m in re.finditer(r'MotionBlur\s*=\s*Input\s*\{\s*Value\s*=\s*(?:Number\s*\{\s*Value\s*=\s*)?1\b', t):
        ip = t.rfind('Inputs = {', 0, m.start())
        ls = t.rfind('\n', 0, ip) + 1
        ind = len(t[ls:ip]) - len(t[ls:ip].lstrip('\t'))
        hs = list(re.finditer(r'\n\t{%d}(\w+) = [\w.]+ \{' % max(ind - 1, 0), t[:ip]))
        if hs and 'PassThrough = true' not in t[hs[-1].end():ip]:
            mb.append(hs[-1].group(1))
    R['S2'] = 'FAIL on: %s' % ','.join(sorted(set(mb)))[:60] if mb else 'ok'
    boxes = [n for n in B if re.match(r'Background_\w*Fill$', n)]
    sweeps = [n for n, (ty, b) in B.items() if ty == 'MacroOperator' and 'SweepControls' in b]
    R['S1'] = ('FAIL %d/%d' % (len(sweeps), len(boxes)) if len(sweeps) < len(boxes) else 'ok %d/%d' % (len(sweeps), len(boxes))) if boxes else '- %d sweeps' % len(sweeps)
    br = len([n for n in B if re.match(r'Rectangle_\w*Br0$', n)])
    R['BR'] = ('WARN %d/%d' % (br, len(boxes)) if br < len(boxes) else 'ok') if boxes else '-'
    rr = [v for v in re.findall(r'CornerRadius = Input \{ Value = ([\d.]+)', t) if float(v) > 0]
    R['SQ'] = 'FAIL r=%s' % ','.join(sorted(set(rr))) if rr else 'ok'
    fonts = sorted(set(re.findall(r'Font = Input \{ Value = "([^"]+)"', t)))
    bad = [f for f in fonts if not f.lower().startswith('inter')]
    R['FONT'] = 'FAIL ' + ','.join(bad) if bad else 'ok'
    nt = [b for ty, b in B.values() if ty == 'Fuse.NeoMotionText']
    pd = sum(1 for b in nt if re.search(r'PosDir = Input \{ Value = [1-9]', b))
    sh = sum(1 for b in nt if re.search(r'StShineEnable = Input \{ Value = 0', b))
    R['TXT'] = ('FAIL' + (' posdir!=0 x%d' % pd if pd else '') + (' shine-off x%d' % sh if sh else '') if (pd or sh) else 'ok %d' % len(nt)) if nt else '-'
    bev = [n for n, (ty, b) in B.items() if 'Bevel' in n and not re.search(r'PassThrough = true', b)]
    R['BEV'] = 'FAIL ' + ','.join(bev) if bev else 'ok'
    media = any(ty == 'MediaIn' for ty, b in B.values())
    if media and (boxes or nt or any(ty == 'TextPlus' for ty, b in B.values())):
        R['S4'] = '- overlay (footage moves by MagicZoom)'
    elif media:
        def nv(txt):
            return ('MotionBlurOn_Script' in txt, bool(re.search(r'= [\w.]*Vignette[\w.]* \{', txt)))
        na, vg = nv(t)
        if not (na and vg):  # the beat's other adj comp may carry them (one beat = one folder)
            for q in glob.glob(os.path.join(os.path.dirname(p), '*.setting')):
                if q != p:
                    a, v = nv(open(q, encoding='utf-8', errors='replace').read())
                    na, vg = na or a, vg or v
        R['S5'] = 'ok' if (na and vg) else 'FAIL neoanim=%d vignette=%d (this beat folder)' % (na, vg)
        R['S4'] = '- media (MagicZoom on the adj clip)'
    else:
        grow = False
        for n, (ty, b) in B.items():
            if ty != 'Transform':
                continue
            m = re.search(r'\bSize = Input \{\s*SourceOp = "(\w+)"', b)
            if m and m.group(1) in B:
                k = keys(B[m.group(1)][1])
                if len(k) >= 2 and k[-1] > k[0] * 1.015:
                    grow = True
        R['S4'] = 'ok' if grow else 'FAIL no push'
    return R

ap = argparse.ArgumentParser(description="Build-card rules the beat lint does not check, read from .setting files only (no Resolve). One line per comp, exit 1 on any FAIL.")
ap.add_argument("paths", nargs="+", help=".setting files or folders (searched recursively)")
ap.add_argument("--exempt", default="samuel_intro_adj", help="skip files whose name contains this (default: %(default)s)")
args = ap.parse_args()
paths = []
for a in args.paths:
    paths += sorted(glob.glob(os.path.join(a, '**', '*.setting'), recursive=True)) if os.path.isdir(a) else [a]
fails = 0
for p in paths:
    if args.exempt.lower() in os.path.basename(p).lower():
        print("-    %-60s S6: Samuel's own intro adj clip, used as he made it (not checked)" % os.path.basename(p)[:60])
        continue
    R = check(p)
    f = any(v.startswith('FAIL') for v in R.values())
    fails += f
    print('%-4s %-60s %s' % ('FAIL' if f else 'ok', os.path.basename(p)[:60], '  '.join('%s %s' % kv for kv in R.items())))
print('%d comps, %d with a FAIL' % (len(paths), fails))
sys.exit(1 if fails else 0)
