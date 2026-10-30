# Pre-install check of ALL beat manifests (install_v2x-style rules): rewrites list.txt, list_no_<prefix>.txt and timeline_check.json; reads only, never touches a beat folder.
# usage: python timeline_check.py --job <job folder> --len <timeline frames> --plan <visual plan dir> [--kits <kits dir>] [--comps <comps dir>] [--out <dir>] [--drop-prefix HK-00]    (file only, no Resolve)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
r"""timeline_check.py - list.txt + an install_v2x-style check of ALL manifests (editor-builder, video 4 stage 5 job A, 2026-10-29).
  python timeline_check.py            re-run any time (after the fix round): rewrites list.txt, list_no_HK-00.txt and
                                       timeline_check.json in the --out folder (keeps the hand-written "conflicts" and "hk00" blocks).
                                       Reads only; never touches a beat folder.
Rules copied from kits\install_v1.py install() and kits\install_v2x.py build()/verify():
  op media|comp; file exists (relative = against the kit); track 2..6; D > 0, start >= 0, start + D <= 12100;
  no overlap on a track (all manifests together); no sliver (an item < 6 f); verify's gap rule = the UNION of all
  V2+ items: no 1-5 f hole between covered spans (butt or >= 6 f), plus the same per track; mz keys = mz_media
  merge_element's (depth, typ, pivot, invert, motion_blur), only on adj comps, motion_blur off (S2);
  S5 size guard on every mz adj comp (adj_guard.check, install prints it). Extra (install would fail or render wrong):
  media video src_in + D <= the file's frames, comp D <= the transparent base clip, Loader files exist, stems unique."""
import argparse, os, sys, json, re, subprocess, time
from collections import Counter
sys.dont_write_bytecode = True                           # never leave __pycache__ in the kits dir

ap = argparse.ArgumentParser(description="Check every beat manifest against install_v2x's rules; write list.txt, list_no_<prefix>.txt, timeline_check.json.")
ap.add_argument("--job", help="job folder (gives the default --kits, --comps, --out)")
ap.add_argument("--kits", help="kits dir (default <job>\\Graphics\\Frontal kit (Editor)\\kits)")
ap.add_argument("--comps", help="comps dir with <beat>\\manifest.json (default <kit>\\comps\\v1)")
ap.add_argument("--plan", required=True, help="visual plan folder holding BUILD LIST.json and beats.json (video 4: Docs\\Visual plan v2 (Editor))")
ap.add_argument("--len", type=int, required=True, help="timeline length in frames (video 4: 12100)")
ap.add_argument("--out", help="folder for list.txt, list_no_<prefix>.txt, timeline_check.json (default <job>\\Docs\\finish)")
ap.add_argument("--drop-prefix", default="HK-00", help="manifest folders starting with this go to the second list (default HK-00, the intro adj)")
ap.add_argument("--ffprobe", default=(r"C:\Users\repzy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
                                      r"\ffmpeg-9.0.1-full_build\bin\ffprobe.exe"), help="ffprobe.exe (default: the winget ffmpeg 9.0.1)")
ap.add_argument("--base", default=r"C:\Users\repzy\Desktop\Video edits\Routerise\Visual Assets\Assets\Fusion base 1080 transparent.mov",
                help="the transparent base clip every comp sits on")
args = ap.parse_args()
if not (args.job or args.kits):
    ap.error("give --job or --kits")
if not (args.job or args.out):
    ap.error("give --job or --out")
KITS = os.path.abspath(args.kits or os.path.join(args.job, "Graphics", "Frontal kit (Editor)", "kits"))
K = os.path.dirname(KITS); V = os.path.abspath(args.comps or os.path.join(K, "comps", "v1"))
HERE = os.path.abspath(args.out or os.path.join(args.job, "Docs", "finish"))
os.makedirs(HERE, exist_ok=True)
PL = os.path.abspath(args.plan)
sys.path.insert(0, KITS)
import adj_guard as AG  # noqa: E402
FFP = args.ffprobe
BASE = args.base
TL, TRACKS, STILL = args.len, range(2, 7), (".png", ".jpg", ".jpeg", ".tif", ".tiff")
MZK = {"depth", "typ", "pivot", "invert", "motion_blur"}
OUTJ = os.path.join(HERE, "timeline_check.json")
DROP = args.drop_prefix


def ab(p): return p if os.path.isabs(p) else os.path.join(K, p.replace("/", "\\"))
def src(o): return o.get("setting") or o.get("path") or ""
def end(o): return int(o["start"]) + int(o["D"])
def tag(o): return "%s op%d V%d %d-%d" % (o["folder"], o["i"], int(o["track"]), int(o["start"]), end(o))


def frames(p):
    r = subprocess.run([FFP, "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=r_frame_rate,nb_read_packets", "-of", "csv=p=0", p],
                       capture_output=True, text=True).stdout.strip().split(",")
    return r[0], int(r[1]) if len(r) > 1 and r[1].isdigit() else -1


mans, ops, empty = [], [], []
for d in sorted(os.listdir(V)):
    m = os.path.join(V, d, "manifest.json")
    if d.startswith("_") or not os.path.isfile(m):
        continue
    L = json.load(open(m, encoding="utf-8"))
    if L == []:
        empty.append(d); continue
    mans.append(m)
    for i, o in enumerate(L):
        ops.append(dict(o, folder=d, i=i))
hk00 = [m for m in mans if os.path.basename(os.path.dirname(m)).startswith(DROP)]
open(os.path.join(HERE, "list.txt"), "w", encoding="utf-8").write("\n".join(mans) + "\n")
open(os.path.join(HERE, "list_no_%s.txt" % DROP), "w", encoding="utf-8").write("\n".join(m for m in mans if m not in hk00) + "\n")

old = json.load(open(OUTJ, encoding="utf-8")) if os.path.exists(OUTJ) else {}
R = {"made": time.strftime("%Y-%m-%d %H:%M"),
     "by": "pipeline\\finish\\timeline_check.py (re-run after the fix round, it rewrites everything but 'conflicts' and 'hk00')",
     "rules": __doc__.split("Rules copied from ")[1].strip(),
     "conflicts": old.get("conflicts", []), "hk00": old.get("hk00", {}),
     "manifests": len(mans), "ops": len(ops),
     "by_track": dict(sorted(Counter("V%d" % int(o["track"]) for o in ops).items())),
     "media": sum(o["op"] == "media" for o in ops), "comps": sum(o["op"] == "comp" for o in ops),
     "adj": sum(bool(o.get("adj")) for o in ops), "mz_on_adj": sum(bool(o.get("mz")) for o in ops),
     "skipped_empty_manifests": empty,
     "lists": {"list.txt": len(mans), "list_no_%s.txt" % DROP: len(mans) - len(hk00)}}
bad = []
for o in ops:
    p = ab(src(o)); e = []
    if o["op"] not in ("media", "comp"): e.append("unknown op")
    if not os.path.exists(p): e.append("missing file " + p)
    if int(o["track"]) not in TRACKS: e.append("track")
    if int(o["D"]) <= 0 or int(o["start"]) < 0 or end(o) > TL: e.append("range")
    if 0 < int(o["D"]) < 6: e.append("sliver D %d" % int(o["D"]))
    if o["op"] == "comp" and not isinstance(o.get("fonts", []), list): e.append("fonts not a list")
    if o.get("mz") is not None:
        z = o["mz"]
        if not (o["op"] == "comp" and o.get("adj")): e.append("mz on a non-adj op (install ignores it)")
        if set(z) - MZK: e.append("mz keys %s" % sorted(set(z) - MZK))
        if z.get("motion_blur"): e.append("mz motion_blur on (S2)")
    if e:
        bad.append({"op": tag(o), "problems": e})
R["op_problems"] = bad

over, tgap = [], []
for t in TRACKS:
    L = sorted([o for o in ops if int(o["track"]) == t], key=lambda o: (int(o["start"]), end(o)))
    for x in range(len(L)):
        for y in range(x + 1, len(L)):
            if int(L[y]["start"]) < end(L[x]):
                over.append({"track": t, "a": tag(L[x]), "b": tag(L[y]), "frames": end(L[x]) - int(L[y]["start"])})
        if x + 1 < len(L) and 0 < int(L[x + 1]["start"]) - end(L[x]) < 6:
            tgap.append({"track": t, "a": tag(L[x]), "b": tag(L[x + 1]), "gap": int(L[x + 1]["start"]) - end(L[x])})
ug, e_, last = [], None, None
for o in sorted(ops, key=lambda o: (int(o["start"]), end(o), int(o["track"]))):
    if e_ is not None and 0 < int(o["start"]) - e_ < 6:
        ug.append({"a": tag(last), "b": tag(o), "gap": int(o["start"]) - e_})
    if e_ is None or end(o) > e_:
        e_, last = end(o), o
R["overlaps"], R["gaps_per_track"], R["gaps_union_verify_rule"] = over, tgap, ug

# extra install risks
fr_base = frames(BASE)
longest = max((o for o in ops if o["op"] == "comp"), key=lambda o: int(o["D"]))
med = []
for o in ops:
    p = ab(src(o))
    if o["op"] != "media" or p.lower().endswith(STILL) or not os.path.exists(p):
        continue
    fr, n = frames(p); need = int(o.get("src_in", 0)) + int(o["D"])
    if n < need or (fr != "24000/1001" and n - need < 2):
        med.append({"op": tag(o), "file": os.path.basename(p), "fps": fr, "frames": n, "src_in+D": need})
guard = [tag(o) for o in ops if o.get("adj") and o.get("mz") and os.path.exists(ab(src(o)))
         and AG.check(open(ab(src(o)), encoding="utf-8", errors="replace").read()) == "MISSING"]
lmiss, few, stems = [], [], {}
for o in ops:
    p = ab(src(o))
    if not os.path.exists(p):
        continue
    stems.setdefault(os.path.basename(p).lower(), set()).add(os.path.normcase(p))
    if o["op"] != "comp":
        continue
    t = open(p, encoding="utf-8", errors="replace").read()
    for f in set(re.findall(r'(?<![A-Za-z])Filename = "([^"]+)"', t)):
        if not os.path.exists(f.replace("\\\\", "\\")):
            lmiss.append({"op": tag(o), "file": f})
    top = re.findall(r"^\t\t(\w+) = ([\w.]+) \{", t, re.M)
    n = [x for x, ty in top if not (ty.endswith("Spline") or ty.endswith("Path") or ty.startswith("Publish")
                                    or ty.startswith("LUT") or ty == "Note")]
    if len(n) <= 2 and not any(ty in ("MacroOperator", "GroupOperator") for _, ty in top):
        few.append({"op": tag(o), "tools": n})   # verify fails 'EMPTY COMP' when the placed comp has <= 4 tools
R["checks"] = {
    "S5_size_guard_missing": guard,
    "media_short_or_zero_headroom": med,
    "base_clip": {"file": os.path.basename(BASE), "fps": fr_base[0], "frames": fr_base[1], "longest_comp": tag(longest),
                  "ok": fr_base[1] >= int(longest["D"])},
    "loader_files_missing": lmiss,
    "same_file_name_two_paths": [k for k, v in stems.items() if len(v) > 1],
    "comps_with_2_or_fewer_real_tools": few}

# beats
BL = json.load(open(os.path.join(PL, "BUILD LIST.json"), encoding="utf-8"))
beats = {b["id"]: b for b in json.load(open(os.path.join(PL, "beats.json"), encoding="utf-8"))}
blb = [b for u in BL["units"] for b in u["beats"]]
have = {o["folder"] for o in ops}
noops = []
for b in blb:
    if b in have:
        continue
    s0, e0 = beats[b]["start"], beats[b]["end"]
    cov = sorted({tag(o) for o in ops if int(o["start"]) < e0 and end(o) > s0})
    noops.append({"beat": b, "plan": [s0, e0], "kind": beats[b]["kind"], "manifest": "[]" if b in empty else "none",
                  "covered_by": cov, "covered": bool(cov)})
R["build_list_beats_without_ops"] = noops
R["folders_not_in_build_list"] = sorted(have - set(blb))
R["plan_beats_not_in_build_list"] = {"count": sum(1 for b in beats if b not in blb),
                                     "kinds": dict(Counter(beats[b]["kind"] for b in beats if b not in blb))}

# MagicZoom (A-roll pass): install_v2x asserts no zone over any V2 item or a non-adj V3+ item; zones sit on V2
blk = [0] * TL
for o in ops:
    if int(o["track"]) == 2 or not o.get("adj"):
        for f in range(int(o["start"]), min(end(o), TL)):
            blk[f] = 1
win, f = [], 0
while f < TL:
    if blk[f]:
        f += 1; continue
    g = f
    while g < TL and not blk[g]:
        g += 1
    win.append([f, g]); f = g
R["magiczoom_free_windows"] = {
    "rule": "mz.json is not written yet (A-roll pass). install_v2x puts every zone on V2 and asserts it covers no V2 item "
            "and no non-adj V3+ item, so a zone [start, end) sits inside one window. Its edges butt the window edge or stay "
            ">= 6 f from every V2+ item edge (verify's union gap rule); no zone under 6 f. Plan v2: no MagicZoom in 0-28.",
    "frames_free": sum(b - a for a, b in win), "count": len(win), "windows": win}
json.dump(R, open(OUTJ, "w", encoding="utf-8"), indent=1)
print("manifests", len(mans), "ops", len(ops), "| problems", len(bad), "overlaps", len(over), "gaps track/union", len(tgap), len(ug),
      "| media risk", len(med), "guard missing", len(guard), "loader missing", len(lmiss), "few-tool", len(few),
      "same-name", len(R["checks"]["same_file_name_two_paths"]), "base ok", R["checks"]["base_clip"]["ok"],
      "| no-op beats", [(x["beat"], x["covered"]) for x in noops], "| not in BL", R["folders_not_in_build_list"],
      "| mz windows", len(win), R["magiczoom_free_windows"]["frames_free"], "f")
