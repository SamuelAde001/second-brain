# Independent cross-check of the stage 5 prep jobs: install list, MagicZoom zones, S4 coverage, sound plan and SFX caps, S6 intro adj. Files only.
# Usage: python crosscheck.py --stage <stage dir> --comps <comps/vN> --items cut_items.json --words cut_words.json --build-list "BUILD LIST.json" --len 12100 --hook-end 1426 --timeline "<name>" [--list list.txt] [--events sfx_events.json] [--v1-count N] [--hk-folder "HK-00 intro adj" --hk-original <.setting>] [--out <dir>]
# Promoted from video 4 on 2026-10-30.
# crosscheck.py - independent cross-check of the three stage 5 prep jobs (editor-builder reviewer, 2026-10-29).
# Files only: no Resolve. Re-implements install_v2x's MZ guard + verify (union gap rule), bible 03 MZ rules,
# bible 07 sound rules, and the S6 intro adj checks, from the manifests as they are NOW.
#   -> crosscheck.json (+ crosscheck_<list name>.json for any other list) and a short summary on stdout
import argparse, json, os, sys, re, collections, subprocess
import numpy as np

ap = argparse.ArgumentParser(description="Independent cross-check of the stage 5 prep jobs (install list, MagicZoom plan, sound plan, S6 intro adj). Files only, no Resolve.")
ap.add_argument("--stage", required=True, help="folder with mz.json, mz_notes.md, sound_plan.json (crosscheck*.json is written here unless --out)")
ap.add_argument("--comps", required=True, help="the comps/<version> folder: one folder per beat, each with manifest.json")
ap.add_argument("--items", required=True, help="cut items json: [type, track, start, end, src] rows")
ap.add_argument("--words", required=True, help="cut_words.json")
ap.add_argument("--build-list", required=True, help="BUILD LIST.json")
ap.add_argument("--events", help="sfx events json (default: <stage>/sfx_events.json)")
ap.add_argument("--list", help="install list, one manifest.json per line (default: <stage>/list.txt)")
ap.add_argument("--len", type=int, required=True, help="timeline length in frames")
ap.add_argument("--hook-end", type=int, required=True, help="last frame of the hook")
ap.add_argument("--timeline", required=True, help="timeline name the sound plan must carry")
ap.add_argument("--v1-count", type=int, help="expected number of V1 clips (omit to skip the count)")
ap.add_argument("--hk-folder", help="beat folder of the S6 intro adj comp, e.g. 'HK-00 intro adj' (enables the S6 section)")
ap.add_argument("--hk-original", help="Samuel's original intro adj .setting, diffed against the installed one")
ap.add_argument("--out", help="folder for crosscheck*.json (default: --stage)")
A = ap.parse_args()
ST = A.stage
V1D = A.comps
LEN, FPS, HOOK_END = A.len, 24000 / 1001, A.hook_end
LST = A.list or os.path.join(ST, "list.txt")
EV = A.events or os.path.join(ST, "sfx_events.json")
OUTD = A.out or ST
R = {"list": os.path.basename(LST), "fail": [], "warn": [], "info": {}}
F = lambda *a: R["fail"].append(" ".join(map(str, a)))
W = lambda *a: R["warn"].append(" ".join(map(str, a)))
I = lambda k, v: R["info"].setdefault(k, []).append(v)

items = json.load(open(A.items, encoding="utf-8"))
v1 = sorted((a, b) for t, tr, a, b, *_ in items if t == "video" and tr == 1)
if (A.v1_count is not None and len(v1) != A.v1_count) or v1[-1][1] != LEN: F("V1", len(v1), v1[-1])
cuts = set(a for a, b in v1) | set(b for a, b in v1)
words = json.load(open(A.words, encoding="utf-8"))

# ---------------- (1) list ----------------
paths = [l.strip().strip('"') for l in open(LST, encoding="utf-8") if l.strip()]
R["info"]["list_paths"] = len(paths)
for p, n in collections.Counter(os.path.normcase(p) for p in paths).items():
    if n > 1: F("LIST dup path", p)
for f, n in collections.Counter(os.path.basename(os.path.dirname(p)) for p in paths).items():
    if n > 1: F("LIST dup folder", f)
for p in paths:
    if not os.path.isfile(p): F("LIST missing file", p)
    if os.path.normcase(os.path.dirname(os.path.dirname(p))) != os.path.normcase(V1D): F("LIST outside --comps", p)
inlist = {os.path.basename(os.path.dirname(p)) for p in paths}
for f in sorted(os.listdir(V1D)):
    if not os.path.isdir(os.path.join(V1D, f)): continue
    m = os.path.join(V1D, f, "manifest.json")
    if not os.path.isfile(m):
        (W if f.startswith("_") else F)("LIST folder without manifest", f); continue
    n = len(json.load(open(m, encoding="utf-8")))
    if n and f not in inlist: (W if f.startswith("_") or (f == A.hk_folder and "no_" + A.hk_folder.split()[0] in LST) else F)("LIST folder with ops not listed", f, n)
    if not n and f in inlist: W("LIST empty manifest listed", f)
    if not n and f not in inlist: I("empty_unlisted", f)
bl = json.load(open(A.build_list, encoding="utf-8"))
blb = sorted({b for u in bl["units"] for b in u.get("beats", [])})
R["info"]["buildlist_beats"] = len(blb)
R["info"]["buildlist_beats_not_listed"] = [b for b in blb if b not in inlist]

ops, mt = [], {}
for p in paths:
    if not os.path.isfile(p): continue
    f = os.path.basename(os.path.dirname(p)); mt[f] = os.path.getmtime(p)
    for i, o in enumerate(json.load(open(p, encoding="utf-8"))):
        a = int(o["start"]); ops.append(dict(o, folder=f, i=i, a=a, b=a + int(o["D"]), tr=int(o["track"])))
R["info"]["ops"] = len(ops)
for o in ops:
    if not (2 <= o["tr"] <= 6) or o["a"] < 0 or o["b"] > LEN or o["b"] - o["a"] < 6: F("OP range", o["folder"], o["tr"], o["a"], o["b"])
    for k in ("setting", "path", "file"):
        if o.get(k) and not os.path.isfile(o[k]): F("OP file missing", o["folder"], o[k])
newer = [f for f, t in mt.items() if t > min(os.path.getmtime(x) for x in (os.path.join(ST, "mz.json"), os.path.join(ST, "sound_plan.json"), EV))]
R["info"]["manifests_newer_than_stage5_plans"] = sorted(newer)

# ---------------- (2) MagicZoom ----------------
MODES = {"zoom_hold": (1, 0.071), "standard": (0, 0.071), "punch": (1, 0.111), "mirror": (3, 0.071)}
mz = json.load(open(os.path.join(ST, "mz.json"), encoding="utf-8"))
zs = sorted(mz, key=lambda z: int(z["start"]))
isvis = lambda o: o["tr"] == 2 or not o.get("adj")                     # what install_v2x's guard refuses under a zone
zstarts = {int(z["start"]) for z in zs}
opedges = {o["a"] for o in ops} | {o["b"] for o in ops}
vstarts = sorted({o["a"] for o in ops if isvis(o)})
for k, z in enumerate(zs):
    a, b, m = int(z["start"]), int(z["end"]), z["mode"]
    if m not in MODES: F("MZ unknown mode", z); continue
    D, dep = b - a, float(z.get("depth", MODES[m][1])); tag = "MZ %d-%d %s %.3f (%d f)" % (a, b, m, dep, D)
    if not (0 <= a < b <= LEN): F(tag, "out of range")
    if a < 28: F(tag, "inside S6 0-28")
    if [round(x, 3) for x in z.get("center", [])] != [0.507, 0.62]: W(tag, "center", z.get("center"))
    hit = [(o["folder"], o["tr"], o["a"], o["b"]) for o in ops if isvis(o) and o["a"] < b and o["b"] > a]
    if hit: F(tag, "over a visual", hit[:3])
    if D < 24: F(tag, "under 24 f")
    if m == "punch" and not 25 <= D <= 45: F(tag, "punch outside 25-45 f")
    if m == "zoom_hold" and D < 43: F(tag, "zoom_hold under 43 f (bible 03 rule 2; ramp is 24 f)")
    if m == "zoom_hold" and D > 190: W(tag, "zoom_hold over 190 f")
    under = sorted({o["folder"] for o in ops if o["tr"] >= 3 and o.get("adj") and o["a"] < b and o["b"] > a})
    if m == "standard" and not under and not (D >= 170 and dep in (0.071, 0.111)) and not (D < 43 and dep <= 0.03):   # 24-42 f: rule 2 names no mode; Standard at the bible 03 depth-by-length
        W(tag, "standard on plain A-roll outside bible 03 rule 2 (>=170 f at 0.071/0.111; 43-190 f -> zoom_hold)")
    if m == "standard" and under and dep > 0.048: W(tag, "standard under overlay deeper than 0.048", under)
    if k and int(zs[k - 1]["end"]) > a: F(tag, "overlaps previous zone")
    if k and zs[k - 1]["mode"] == "punch" and m == "punch": F(tag, "two punches in a row")
    for e, wh in ((a, "start"), (b, "end")):
        if e not in cuts and e not in opedges and e not in (0, LEN): W(tag, wh, "edge on no V1 cut and no visual edge")
        mid = [w["w"] for w in words if w["f"] < e < w["e"]]
        if mid: I("mz_edges_mid_word", [e, mid[0], "visual edge" if e in opedges else ("V1 cut" if e in cuts else "neither")])
    if not [w for w in words if a <= w["f"] < b]: F(tag, "no word starts inside")
    if b < LEN and b not in zstarts:
        nxt = min([x for x in list(zstarts) + vstarts if x >= b] or [LEN])
        if 0 < nxt - b < 6: F(tag, "1-5 f of unzoomed A-roll after the zone, before", nxt)
        elif nxt > b and b not in cuts: F(tag, "ends mid-shot onto plain A-roll (snap; mirror or chain)")
        elif nxt > b: I("mz_end_on_V1_cut_to_unzoomed", b)
pun = [z for z in zs if z["mode"] == "punch"]
if len(pun) * 4 > len(zs): F("MZ punches over 1 in 4", len(pun), len(zs))
R["info"]["mz"] = {"zones": len(zs), "modes": dict(collections.Counter("%s %.3f" % (z["mode"], float(z.get("depth", MODES[z["mode"]][1]))) for z in zs))}

# named words in mz_notes (lands on)
notes = open(os.path.join(ST, "mz_notes.md"), encoding="utf-8").read()
for a, b, mode, wd, wf in re.findall(r"^\| (\d+)-(\d+) \| \d+ \| (\w+) \| [\d.]+ \| '([^']+)' (\d+) \|", notes, re.M):
    a, b, wf = int(a), int(b), int(wf); first = re.sub(r"[^\w']", "", wd.split()[0].lower())
    hit = [w for w in words if abs(w["f"] - wf) <= 1 and re.sub(r"[^\w']", "", w["w"].lower()) == first]
    if not hit: F("MZ named word not in cut_words", a, b, wd, wf)
    if not a <= wf < b: F("MZ named word outside its zone", a, b, wd, wf)
    if mode in ("punch", "zoom_hold") and wf - a > 26: W("MZ named word after the 1 s ramp", a, b, mode, wd, wf - a)

# installer verify, union over V2+ (ops + zones on V2)
vis = sorted([(o["a"], o["b"], o["tr"]) for o in ops] + [(int(z["start"]), int(z["end"]), 2) for z in zs])
e = None
for a, b, k in vis:
    if e is not None and 0 < a - e < 6: F("VERIFY sliver gap", e, a)
    e = b if e is None else max(e, b)
for a, b, k in vis:
    if b - a < 6: F("VERIFY sliver item", a, b, k)
for k in set(v[2] for v in vis):
    t = sorted(v for v in vis if v[2] == k)
    for x, y in zip(t, t[1:]):
        if y[0] < x[1]: F("VERIFY overlap track", k, x, y)
    if k == 2:
        for x, y in zip(t, t[1:]):
            if 0 < y[0] - x[1] < 6: W("V2 per-track 1-5 f gap (covered above)", x, y)

# ---------------- (3) S4 coverage ----------------
cls = np.zeros(LEN, int)                         # 0 bare A-roll, 1 A-roll under adj overlay only, 2 visual
for o in ops:
    if isvis(o): cls[o["a"]:o["b"]] = 2
for o in ops:
    if not isvis(o): seg = cls[o["a"]:o["b"]]; seg[seg == 0] = 1
zc = np.zeros(LEN, bool)
for z in zs: zc[int(z["start"]):int(z["end"])] = True
plain = cls < 2
R["info"]["S4"] = {"plain_frames": int(plain.sum()), "covered": int((plain & zc).sum()), "bare": int((cls == 0).sum()), "under_overlay": int((cls == 1).sum())}
un = plain & ~zc
f = 0
while f < LEN:
    if un[f]:
        g = f
        while g < LEN and un[g]: g += 1
        if g - f >= 24:
            ov = sorted({o["folder"] for o in ops if not isvis(o) and o["a"] < g and o["b"] > f})
            I("S4_unzoned_plain_ge24", [f, g, g - f, ov])
        else: I("S4_unzoned_plain_lt24", [f, g])
        f = g
    else: f += 1
# non-adj V3+ overlays over A-roll (installer refuses a zone there): A-roll under them can't move
for o in ops:
    if o["tr"] >= 3 and not o.get("adj"):
        v2 = np.zeros(LEN, bool)
        for q in ops:
            if q["tr"] == 2: v2[q["a"]:q["b"]] = True
        bare = int((~v2[o["a"]:o["b"]]).sum())
        if bare: I("S4_A-roll_under_non-adj_overlay", [o["folder"], o["tr"], o["a"], o["b"], bare])
# S5: every V2 media item under a V4 adj that carries MZ
for o in [o for o in ops if o["op"] == "media"]:
    cov = sum(max(0, min(o["b"], q["b"]) - max(o["a"], q["a"])) for q in ops if q.get("adj") and q.get("mz"))
    if cov < 0.9 * (o["b"] - o["a"]): F("S5 media without MZ adj", o["folder"], o["a"], o["b"], cov)

# ---------------- (4) sound ----------------
sp = json.load(open(os.path.join(ST, "sound_plan.json"), encoding="utf-8"))
if sp.get("timeline") != A.timeline: F("SOUND timeline", sp.get("timeline"))
mus = sorted(sp["music"], key=lambda m: m["rec"]); sfx = sorted(sp["sfx"], key=lambda s: s["rec"])
dur = {}
for p in sorted({m["path"] for m in mus} | {s["path"] for s in sfx}):
    if not os.path.isfile(p): F("SOUND missing file", p); continue
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True)
    try: dur[p] = float(r.stdout.strip())
    except ValueError: F("SOUND undecodable", p)
if mus and mus[0]["rec"] != 0: F("MUSIC does not start at 0")
for x, y in zip(mus, mus[1:]):
    if y["rec"] != x["end"]: F("MUSIC gap/overlap", x["end"], y["rec"])
if mus and mus[-1]["end"] != LEN: F("MUSIC ends at", mus[-1]["end"])
for p, n in collections.Counter(m["path"] for m in mus).items():
    if n > 1: F("MUSIC song twice", os.path.basename(p))
for k, m in enumerate(mus):
    D = m["end"] - m["rec"]; nm = os.path.basename(m["path"])
    if D < 216: W("MUSIC piece under 9 s", nm, D)
    if not -42 <= m["vol"] <= -25: W("MUSIC level outside -42..-25", nm, m["vol"])
    if m["path"] in dur and m["src_s"] + D / FPS > dur[m["path"]] + 0.01: F("MUSIC past file end", nm, m["src_s"], D, dur[m["path"]])
    if m["rec"] and m["rec"] not in cuts: W("MUSIC change not on a V1 cut", m["rec"], nm)
    fi, fo = m.get("fade_in", 0), m.get("fade_out", 0)
    if (m["rec"] == 0 and fi) or (m["rec"] and fi != 6) or fo != (48 if k == len(mus) - 1 else 12): W("MUSIC fades", m["rec"], nm, fi, fo)
ev = json.load(open(EV, encoding="utf-8"))
evops = {(e["beat"], e["track"], e["start"], e["D"]) for e in ev["ops"]}
curops = {(o["folder"], o["tr"], o["a"], o["b"] - o["a"]) for o in ops}
R["info"]["events_ops_stale"] = sorted(set(x[0] for x in evops ^ curops))
evb = collections.defaultdict(list)
for e in ev["events"]:
    evb[e["beat"]].append(int(round(e["f"])))
    if e.get("land") is not None: evb[e["beat"]].append(int(round(e["land"])))
    if e["kind"] == "count": evb[e["beat"]].append(int(round(e["f"] + (e.get("dur") or 0))))
allev = sorted(x for v in evb.values() for x in v)
SECTION, BEEPS = ("lowhit0", "lowhit", "lowhitQ", "swooshR", "riser"), ("beep", "beep3", "arp", "arp2", "multi")
# where each kind lands relative to its rec (bible 07 table: Low Hit 5 f before the reveal, Swoosh 7 f before it with the
# Low Hit or 1 f before a graphic entrance; shutter peak +9 measured, placed 10 f before the cut; riser starts 35 f before
# the Low Hit); everything else lands on its rec
OFF = {"swooshR": (7,), "swoosh": (0, 1, 7), "swooshL": (0, 1, 7), "camera": (9, 10), "lowhit": (5,), "lowhitQ": (5,), "lowhit0": (0,)}
pertr = collections.defaultdict(list)
lowhits = [s["rec"] for s in sfx if s["kind"].startswith("lowhit")]
for s in sfx:
    a = s["rec"]; n = s.get("len") or int(round(s.get("dur", 1.0) * FPS)); src = int(s.get("src", 0)); b_ = s.get("beat", "")
    pertr[s["tr"]].append((a, a + n))
    if a < 0 or a + n > LEN: F("SFX out of range", a, b_)
    if not 3 <= s["tr"] <= 8: W("SFX track", a, s["tr"])
    if s["path"] in dur and (src + n) / FPS > dur[s["path"]] + 0.01: F("SFX past file end", a, os.path.basename(s["path"]))
    beatops = [o for o in ops if o["folder"] == b_]
    if not beatops: F("SFX beat not in list", a, b_, s["kind"]); continue
    whyf = [int(x) for o in beatops for x in re.findall(r"(?<![\d.,$])(\d{3,5})(?!\d|%|[.,]\d)", o.get("why", "")) if o["a"] - 2 <= int(x) <= o["b"] + 2]
    cand = sorted(set(evb.get(b_, []) + [o["a"] for o in beatops] + [o["b"] for o in beatops] + whyf))
    if s["kind"] == "riser":
        land = a + 35; d = min([abs(land - h) for h in lowhits] or [999]); src_ = "Low Hit"
    else:
        lands = [a + k for k in OFF.get(s["kind"], (0,))]; d = min(abs(l - c) for l in lands for c in cand); land = lands[0]; src_ = "event"
    if d > 2:
        d_any = min(abs(l - c) for l in ([land] if s["kind"] == "riser" else lands) for c in allev)
        (W if d_any <= 2 else F)("SFX not within 2 f of its beat's %s" % src_, a, b_, s["kind"], "off %d (any beat %d)" % (d, d_any), s.get("event", "")[:80])
    if not any(o["a"] - 2 <= land < o["b"] + 2 for o in beatops) and s["kind"] != "riser": F("SFX lands outside its beat's visual", a, land, b_, s["kind"])
    if land < LEN and cls[land] == 0 and not any(abs(land - o["a"]) <= 2 for o in ops): W("SFX lands on bare A-roll", a, b_, s["kind"])
for t, v in pertr.items():
    v.sort()
    for x, y in zip(v, v[1:]):
        if y[0] < x[1]: F("SFX overlap on track", t, x, y)
for x, y in zip(sfx, sfx[1:]):
    if y["rec"] - x["rec"] <= 6: I("SFX_pairs_le6f", [x["rec"], x["kind"], x["beat"], x["tr"], y["rec"], y["kind"], y["beat"], y["tr"]])
recs = [(s["rec"], s["kind"], s["beat"]) for s in sfx]
bp = [r for r, k, _ in recs if k in BEEPS]
for a in range(0, LEN):
    if sum(1 for r in bp if a <= r < a + 48) > 3: F("SFX >3 beeps in 48 f at", a); break
for a in range(0, LEN):
    if sum(1 for r in bp if a <= r < a + 96) > 4: F("SFX >4 beeps in 96 f at", a); break
hits = [r for r, k, _ in recs if k.startswith("lowhit")]
for r in bp:
    if any(0 <= r - h < 20 for h in hits): F("SFX beep within 20 f after a Low Hit", r)
body = [r for r, k, _ in recs if r >= HOOK_END and k not in SECTION]
for a in range(HOOK_END, LEN):
    n = sum(1 for r in body if a <= r < a + 720)
    if n > 7: F("SFX >7 sounds in 30 s from", a, n); break
cam = [r for r, k, _ in recs if k == "camera" and r >= HOOK_END - 240]
for x, y in zip(cam, cam[1:]):
    if y >= HOOK_END and y - x < 240: F("SFX shutters under 240 f apart", x, y)
byb = collections.defaultdict(list)
for r, k, b_ in recs: byb[b_].append((r, k))
for b_, v in byb.items():
    for (r1, k1), (r2, k2) in zip(v, v[1:]):
        g = 12 if r2 < HOOK_END else 36
        if r2 - r1 < g and not (k1 == k2 == "click") and not (k1.startswith("swoosh") and k2 in BEEPS) and not (k1 in SECTION or k2 in SECTION):
            W("SFX same-visual spacing", b_, r1, k1, r2, k2)
R["info"]["sfx"] = {"total": len(sfx), "hook": sum(1 for s in sfx if s["rec"] < HOOK_END), "files": len({os.path.basename(s["path"]) for s in sfx}),
                    "per_min": round(len(sfx) / (LEN / FPS / 60), 1), "music": len(mus)}

# ---------------- (5) HK-00 ----------------
hk = os.path.join(V1D, A.hk_folder, "manifest.json") if A.hk_folder else ""
if hk and os.path.isfile(hk):
    o0 = json.load(open(hk, encoding="utf-8"))
    if len(o0) != 1: F("HK-00 ops", len(o0))
    o = o0[0]
    for k, v in (("op", "comp"), ("adj", True), ("D", 28), ("start", 0)):
        if o.get(k) != v: F("HK-00", k, o.get(k))
    t = open(o["setting"], encoding="utf-8").read() if os.path.isfile(o["setting"]) else ""
    if not t: F("HK-00 setting missing", o["setting"])
    mb = re.findall(r"MotionBlur = Input \{ Value = (\d+)", t)
    if not mb or any(x != "0" for x in mb): F("HK-00 MotionBlur", mb)
    pv = re.findall(r"Pivot = Input \{ Value = \{ ([\d.]+), ([\d.]+)", t)
    R["info"]["HK-00"] = {"track": o["track"], "MotionBlur": mb, "pivot": pv, "fonts": o.get("fonts")}
    org = A.hk_original or ""
    if org and os.path.isfile(org):
        ot = open(org, encoding="utf-8").read()
        R["info"]["HK-00"]["original_MotionBlur_pivot"] = [re.findall(r"MotionBlur = Input \{ Value = (\d+)", ot), re.findall(r"Pivot = Input \{ Value = \{ ([\d.]+), ([\d.]+)", ot)]
        dl = [i for i, (x, y) in enumerate(zip(ot.splitlines(), t.splitlines())) if x != y]
        R["info"]["HK-00"]["lines_changed_vs_original"] = len(dl) + abs(len(ot.splitlines()) - len(t.splitlines()))
intro = [(o["folder"], o["i"], o["tr"], o["a"], o["b"]) for o in ops if "intro_adj" in os.path.basename(o.get("setting", ""))]
R["info"]["intro_adj_ops_in_list"] = intro
if len(intro) > 1: F("S6 intro adj installed %d times (stacks the 1.594 zoom and the blur)" % len(intro), intro)

json.dump(R, open(os.path.join(OUTD, "crosscheck%s.json" % ("" if os.path.basename(LST) == "list.txt" else "_" + os.path.splitext(os.path.basename(LST))[0])), "w", encoding="utf-8"), indent=1)
print(R["list"], "fail", len(R["fail"]), "warn", len(R["warn"]))
for x in R["fail"]: print(" F", x[:230])
for x in R["warn"][:40]: print(" W", x[:230])
for k, v in R["info"].items(): print(" I", k, json.dumps(v)[:400])
