# Put MagicZoom V3 ON a media adjustment clip itself (S5), editing a .drt file in memory or on disk, never Resolve; also importable (merge_element / mz_hex).
# usage: python mz_media.py <in.drt> <out.drt> <ops.json> [--kits <kits dir> | --job <job folder> | --drt <kits\drt dir>] [--off N] [--motion-blur]    (file only, no Resolve)
# Promoted from video 4 (Night run 2026-10-28) on 2026-10-30.
r"""mz_media.py - put MagicZoom V3 ON the media adjustment clip itself (S5), the way Samuel's own clips carry it
(editor-builder A3, 2026-10-28). File-only: edits a .drt (in memory or on disk), never Resolve.

Why: all 100 of his comp-carrying MagicZoom clips (magiczoom_instances.json x his 359 exported comps) are his media clip
C1 (NeoAnim + Vignette comp) with MagicZoom on the SAME adjustment clip: Standard (Type 0), depth 0.026-0.037 on 85 of
them. install_v2x.py only adds MagicZoom-only clips on V2 (and refuses one over a visual), so S5 needs this step.

How: an adjustment clip element keeps its Fusion page comp in <CompositionBA> and its Edit-page Fusion effects in
<Sm2TiCompositionTable><FieldsBlob> (key FusionEffectFiltersBA). A converted media element (convert.adj_from) has a short
FieldsBlob with no effect; this swaps in the MagicZoom FieldsBlob that mz_inject builds for an MZ-only clip (same TSB
template, same <In> 86313, same FusionStartFrameOffset), re-ranged to the clip's D. The comp is not touched.

In install_v2x.py (after the step-4 convert loop, before step 5), with `off` from that function:
    mzm = <load this file with importlib>
    for o in ops:
        if o["op"] == "comp" and o.get("adj") and o.get("mz"):
            r_ = mzm.merge_element(d, int(o["track"]), int(o["start"]) + off, int(o["D"]), **o["mz"])
            assert r_ == "ok", (o["folder"], o["start"], r_)
  manifest op: {"op": "comp", "adj": true, ..., "mz": {"depth": 0.03, "typ": 0, "pivot": [0.5, 0.5]}}

Standalone on a file:
  python mz_media.py <in.drt> <out.drt> <ops.json> [--kits <kits dir> | --job <job folder> | --drt <kits\drt dir>] [--off N] [--motion-blur]
  ops.json: [{"track": 3, "start": 1234, "D": 95, "depth": 0.03, "typ": 0, "pivot": [0.5, 0.5]}]   start = timeline frame
  --off N is added to every start to get the .drt <Start>; default = the first V1 <Start>.
MotionBlur on MagicZoom's Transform1 is set to 0 unless motion_blur=True / --motion-blur (S2).
Each merge is read back: the comp still has NAPosition + Vignette; the new blob decodes as MagicZoomV3 with
RenderRange {0, D-1}, the asked Type and Scale, MotionBlur 0. Tested 2026-10-28 on a copy of the LinkedIn v6 .drt
(3 media clips, decode ok). NOT yet proven in Resolve: import once on a scratch timeline and render frames 0/mid/end."""
import json, os, re, sys
sys.dont_write_bytecode = True
EL = r"<Sm2TiVideoClip DbId=.*?</Sm2TiVideoClip>"
FB = r"(<Sm2TiCompositionTable[^>]*>\s*<FieldsBlob>)([0-9a-f]+)(</FieldsBlob>)"


def mz_hex(D, typ=0, depth=0.03, pivot=(0.5, 0.5), invert=False, motion_blur=False):
    import mz_inject as M
    from mzblob import set_comp, join
    t = M.mz_tools(D, typ=typ, scale=depth, invert=invert, pivot=tuple(pivot))
    on, off = "MotionBlur = Input { Value = 1, }", "MotionBlur = Input { Value = 0, }"
    assert t.count(on) + t.count(off) == 1, "live Transform1 MotionBlur not found exactly once"
    t = t.replace(off, on) if motion_blur else t.replace(on, off)    # works with or without the mz_inject S2 patch
    return set_comp(M._STATE, join(M._range(M.T_HEAD, D), t))


def merge_element(d, tr, s0, D, depth=0.03, typ=0, pivot=(0.5, 0.5), invert=False, motion_blur=False):
    """d = drt_inject.Drt (edited in place); s0 = the element's .drt <Start>. Returns "ok" or the reason it refused."""
    from mzblob import get_comp, split
    from qblob import parse_map, split_comp
    a0, b0 = d.video_tracks()[tr - 1]
    blk = d.s[a0:b0]
    hit = None
    for m in re.finditer(EL, blk, re.S):
        if int(re.search(r"<Start>(\d+)</Start>", m.group(0)).group(1)) == s0:
            hit = m; break
    if not hit:
        return "NOT FOUND"
    e = hit.group(0)
    if "<PrettyType>Adjustment Clip</PrettyType>" not in e or int(re.search(r"<Duration>(\d+)</Duration>", e).group(1)) != D:
        return "NOT ADJ OR WRONG D"
    hx = re.search(r"<CompositionBA>([0-9a-f]+)</CompositionBA>", e)
    tools = split_comp(dict(parse_map(hx.group(1))[1])["0_data"][1])[1] if hx else ""
    if not (re.search(r"NAPosition\w* = Transform", tools) and "resolvefx.Vignette" in tools):
        return "COMP IS NOT NeoAnim+Vignette"
    fb = re.search(FB, e)
    if not fb:
        return "NO COMPOSITION TABLE"
    try:
        hd0, _ = split(get_comp(fb.group(2))[0])
        if "MagicZoom" in hd0:
            return "ALREADY HAS MZ"
    except Exception:
        pass                                     # no effect blob yet: the normal case
    new = mz_hex(D, typ=typ, depth=depth, pivot=pivot, invert=invert, motion_blur=motion_blur)
    e2 = e[:fb.start(2)] + new + e[fb.end(2):]
    hd, tl = split(get_comp(new)[0])             # read back
    k = tl.rfind("Transform1 = Transform {"); t1 = tl[k:k + 900]
    k2 = tl.rfind("AnimSize = LUTLookup {"); an = tl[k2:k2 + 1400]
    ok = ("MagicZoomV3" in hd and "RenderRange = { 0, %d }" % (D - 1) in hd
          and "Type = Input { Value = %d, }" % typ in t1
          and "Scale = Input { Value = %g, }" % depth in an
          and ("MotionBlur = Input { Value = %d, }" % (1 if motion_blur else 0)) in t1)
    if not ok:
        return "READBACK FAIL"
    d.s = d.s[:a0] + blk[:hit.start()] + e2 + blk[hit.end():] + d.s[b0:]
    return "ok"


def main(a):
    import argparse
    ap = argparse.ArgumentParser(description="Put MagicZoom V3 on media adjustment clips in a .drt (file only).")
    ap.add_argument("src", help="input .drt")
    ap.add_argument("dst", help="output .drt")
    ap.add_argument("ops", help="ops.json: [{track, start, D, depth, typ, pivot}]")
    ap.add_argument("--job", help="job folder (gives the default --kits)")
    ap.add_argument("--kits", help="kits dir (default <job>/Graphics/Frontal kit (Editor)/kits); its drt folder holds drt_inject, mz_inject, mzblob, qblob")
    ap.add_argument("--drt", help="the kits drt folder itself (overrides --kits)")
    ap.add_argument("--off", type=int, default=None, help="added to every start to get the .drt <Start>; default = the first V1 <Start>")
    ap.add_argument("--motion-blur", action="store_true", help="leave MotionBlur on MagicZoom's Transform1 on (default off, S2)")
    args = ap.parse_args(a)
    if not (args.drt or args.kits or args.job):
        ap.error("give --drt, --kits or --job")
    kd = os.path.abspath(args.drt or os.path.join(args.kits or os.path.join(args.job, "Graphics", "Frontal kit (Editor)", "kits"), "drt"))
    src, dst, opsf = args.src, args.dst, args.ops
    sys.path.insert(0, kd)
    from drt_inject import Drt
    ops = json.load(open(opsf, encoding="utf-8"))
    d = Drt(src)
    v1a, v1b = d.video_tracks()[0]
    off = args.off if args.off is not None else int(re.search(r"<Start>(\d+)</Start>", d.s[v1a:v1b]).group(1))
    res = []
    for o in ops:
        r = merge_element(d, int(o["track"]), int(o["start"]) + off, int(o["D"]), depth=float(o.get("depth", 0.03)),
                          typ=int(o.get("typ", 0)), pivot=o.get("pivot", (0.5, 0.5)), invert=bool(o.get("invert")),
                          motion_blur=args.motion_blur)
        res.append([o["track"], o["start"], o["D"], r])
    bad = [x for x in res if x[3] != "ok"]
    d.save(dst)
    print("off", off, "merged", len(res) - len(bad), "of", len(res), "problems", bad[:20])
    print("saved", dst)
    return 0 if not bad else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
