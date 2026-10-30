# Sound plan for one timeline: music from the music plan json + SFX pins from a config, held to the bible 07 caps and levels; writes sound_plan.json for sound_place.
# Usage: python sound_plan.py --config cues.json --events sfx_events.json --music music_plan.json --out <dir> --sfx-dir <library> --assets-sfx-dir <job SFX> --len 12100 --hook-end 1426 --timeline "<name>" [--conv-dir <dir>] [--cache <json>]
# Promoted from video 4 on 2026-10-30.
"""Sound plan: the sound_place.py plan (music from the music plan json + the SFX pins below) for one timeline
(editor-builder, 2026-10-29, stage 5 job C).

Writes sound_plan.json to --out. Touches only files in --out (and the converted camera wav). No Resolve.
Video-specific creative choices (palette, pins, auto adds, quiet cues, reference video) live in the --config json;
video 4's are in examples/video4_sound_plan.json.

Re-run after any beat fix:
    python sfx_events.py --list list.txt --out sfx_events.json && python sound_plan.py --config ... (see Usage line)
Place (Editor, main session, A2+ empty): python "<K>\\final\\place_sound_locked.py" sound_plan.json

Rules (bible 07 SOUND PLAN, DECISIONS #17, Samuel's review card -> Sound):
- His #3 palette only (9 files), his #3 clip levels; UI Double Beep 03 key landing -43.1 (bible 07 section 8).
- SFX only on real visual events read from the installed manifests and comps (the events json) or from the capture
  timing the manifest records (clicks inside .mov plates). One sound per moment. Silent: shines, pushes, MagicZoom, media adj
  entrances on pages, word-by-word text, counters ticking, typing, scrolls, highlights, statements.
- Section reveals (the config's 'rev' pins only): Swoosh_03 -22.2 7 f before + ES_Low Hit 5 f before the reveal (-19.3 on a quiet cue); the open
  uses Low Hit -14.9 from source frame 1; the riser once, its start `riser.lead` f before the Low Hit of `riser.after_beat`.
- Caps: <= 3 beeps in 48 f and <= 4 in 96 f; the next beep 20+ f after a section hit; after the hook <= 7 sounds in any
  30 s (section hits aside); 36 f between two sounds inside one visual (12 f in the hook; click runs and the swoosh-then-beep
  pair aside); a shutter at most every 240 f after the hook; <= 2 data beds; files only from the palette.
- Never louder against the music than his #3 (his SFX level minus the music's level under it, measured on #3).
Pins carry a frame spec that is re-read from the comps/manifests on every run, so a fix round's retiming follows; 'was'
is the frame found when the pins were written (config was_date) and any drift is printed. Auto adds (graphic swooshes, B-roll shutters) give way to caps."""
import argparse, json, os, re, subprocess, collections, datetime, sys
import numpy as np

ap = argparse.ArgumentParser(description="Sound plan (music + SFX pins) for one timeline, checked against the bible 07 caps; writes sound_plan.json.")
ap.add_argument("--config", required=True, help="json: palette, pins, auto adds, quiet cues, reference video (see examples/video4_sound_plan.json)")
ap.add_argument("--events", required=True, help="sfx events json made by sfx_events.py")
ap.add_argument("--music", required=True, help="music plan json ({'music': [...]})")
ap.add_argument("--out", required=True, help="folder for sound_plan.json")
ap.add_argument("--sfx-dir", required=True, help="SFX library folder (the 'sfx:' root in the config)")
ap.add_argument("--assets-sfx-dir", required=True, help="the job-assets SFX folder (the 'assets:' root in the config)")
ap.add_argument("--conv-dir", help="folder for converted SFX wavs (the 'conv:' root; default <out>\\converted)")
ap.add_argument("--cache", help="music level cache json (default <out>\\meas_music.json)")
ap.add_argument("--len", type=int, required=True, help="timeline length in frames")
ap.add_argument("--hook-end", type=int, required=True, help="last frame of the hook")
ap.add_argument("--timeline", required=True, help="timeline name written into the plan")
A = ap.parse_args()
CFG = json.load(open(A.config, encoding="utf-8"))
HERE = A.out
os.makedirs(HERE, exist_ok=True)
FPS = 24000 / 1001
TIMELINE = A.timeline
END = A.len
HOOK_END = A.hook_end
MUSIC = A.music
EVENTS = A.events
CACHE = A.cache or os.path.join(HERE, "meas_music.json")
CONV = A.conv_dir or os.path.join(HERE, "converted")
_ROOTS = {"sfx:": A.sfx_dir, "assets:": A.assets_sfx_dir, "conv:": CONV}


def fpath(s):
    for k, r in _ROOTS.items():
        if s.startswith(k):
            return os.path.join(r, s[len(k):])
    return s


# kind: (file, his #3 clip dB, length f, source frame)
PAL = {k: (fpath(v[0]), v[1], v[2], v[3]) for k, v in CFG["palette"].items()}
CAM = PAL["camera"][0] if "camera" in PAL else None
CAM_MP4 = fpath(CFG["camera_source"]) if CFG.get("camera_source") else None
RR3, V2CACHE = CFG["reference"]["plan"], CFG["reference"]["cache"]   # read only: video 3's plan and video 2's per-frame song levels
BEEPS = ("beep", "beep3", "arp", "arp2", "multi")
SECTION = ("lowhit0", "lowhit", "lowhitQ", "swooshR", "riser")
PEAK = CFG["peak"]
QUIET_CUES = tuple(CFG["quiet_cues"])   # bible 07 section 4: Low Hit -19.3 under these
RISER = CFG.get("riser")
EXPECT = CFG.get("expect") or {}

ev = json.load(open(EVENTS, encoding="utf-8"))
E = ev["events"]
LIST = ev["list"] if os.path.isabs(ev["list"]) else os.path.join(os.path.dirname(os.path.abspath(EVENTS)), ev["list"])
MUS = json.load(open(MUSIC, encoding="utf-8"))["music"]
OPS = collections.defaultdict(list)
for p in [l.strip() for l in open(LIST, encoding="utf-8") if l.strip()]:
    for o in json.load(open(p, encoding="utf-8")):
        OPS[os.path.basename(os.path.dirname(p))].append(o)
stale = [os.path.basename(os.path.dirname(p)) for p in (l.strip() for l in open(LIST, encoding="utf-8")) if p
         and os.path.getmtime(p) > os.path.getmtime(EVENTS)]

# ------------------------------------------------------------------------------------------------ frame specs
def cut(beat, i=0):
    """the beat's i-th V2 cut (its first op start when it has nothing on V2: a V3+ overlay)."""
    s = sorted({o["start"] for o in OPS[beat] if o["track"] == 2}) or sorted({o["start"] for o in OPS[beat]})
    return s[i] if len(s) > i else None


def evf(beat, rx, which="f", off=0, kind=None, last=False):
    xs = [e for e in E if e["beat"] == beat and re.search(rx, e["elem"]) and (kind is None or e["kind"] == kind)]
    if not xs:
        return None
    e = xs[-1] if last else xs[0]
    if which == "land":
        v = e.get("land") if e["kind"] != "count" else e["f"] + (e.get("dur") or 0)
        v = e["f"] if v is None else v
    else:
        v = e["f"]
    return int(round(v + off))


def why(beat, rx):
    for o in OPS[beat]:
        m = re.search(rx, o.get("why", ""))
        if m:
            return int(m.group(1))
    return None


# (beat, kind, spec, was, event) ; spec = ("cut", off) | ("ev", rx, which, off[, kind, last]) | ("why", rx) | ("rev", spec)
# "rev" = a section reveal at the spec frame R: Swoosh_03 -22.2 at R-7 + Low Hit at R-5.
PINS = [(b, k, tuple(s), w, what) for b, k, s, w, what in CFG["pins"]]
# auto adds: real events that get a sound only when the caps allow (they give way, pins never do)
AUTO = [(b, k, tuple(s), w, what) for b, k, s, w, what in CFG["auto"]]


def resolve(beat, spec):
    t = spec[0]
    if t == "cut":
        c = cut(beat)
        return None if c is None else c + spec[1]
    if t == "ev":
        return evf(beat, spec[1], spec[2], *(spec[3:] if len(spec) > 3 else ()))
    if t == "why":
        return why(beat, spec[1])
    raise ValueError(spec)


def music_at(f):
    return next((m for m in MUS if m["rec"] <= f < m["end"]), None)


cands, notes_drift, unresolved = [], [], []
for pri, table in ((1, PINS), (0, AUTO)):
    for beat, kind, spec, was, what in table:
        f = resolve(beat, spec)
        if f is None:
            unresolved.append("%s %s %s: no frame (kept %d)" % (beat, kind, spec, was)); f = was
        elif f != was:
            notes_drift.append("%s %s: %d -> %d" % (beat, kind, was, f))
        span = [(o["start"], o["start"] + o["D"]) for o in OPS[beat]]
        if span and not any(a - 40 <= f <= b for a, b in span):
            unresolved.append("%s %s at %d is outside the beat's ops %s" % (beat, kind, f, span))
        if kind == "rev":
            m = music_at(f)
            lk = "lowhitQ" if m and any(q in m["cue"] for q in QUIET_CUES) else "lowhit"
            cands.append(dict(f=f - 7, kind="swooshR", beat=beat, what=what + " (swoosh peaks on the reveal %d)" % f, pri=pri))
            cands.append(dict(f=f - 5, kind=lk, beat=beat, what=what + " (Low Hit peaks on the reveal %d)" % f, pri=pri))
            if RISER and beat == RISER["after_beat"]:
                cands.append(dict(f=f - 5 - RISER["lead"], kind="riser", beat=RISER["beat"], what=RISER["what"], pri=pri))
        else:
            cands.append(dict(f=f, kind=kind, beat=beat, what=what, pri=pri))
cands.sort(key=lambda c: (c["f"], -c["pri"]))

# ------------------------------------------------------------------------------------------------ caps
def beeps_in(chosen, a, b):
    return sum(1 for c in chosen if c["kind"] in BEEPS and a <= c["f"] < b)


def check(c, chosen):
    """reasons this candidate breaks a cap, given the sounds already chosen (empty = ok)."""
    r, f = [], c["f"]
    if c["kind"] in BEEPS:
        if any(beeps_in(chosen + [c], a, a + 48) > 3 for a in range(f - 47, f + 1)):
            r.append("beep cap 3 in 2 s")
        if any(beeps_in(chosen + [c], a, a + 96) > 4 for a in range(f - 95, f + 1)):
            r.append("beep cap 4 in 4 s")
        if any(s["kind"] in ("lowhit", "lowhitQ", "lowhit0") and 0 <= f - s["f"] < 20 for s in chosen):
            r.append("within 20 f after a section hit")
    if f >= HOOK_END and c["kind"] not in SECTION:
        for a in range(f - 719, f + 1):
            n = sum(1 for s in chosen + [c] if s["kind"] not in SECTION and a <= s["f"] < a + 720)
            if n > 7:
                r.append("7 in 30 s after the hook"); break
    gap = 12 if f < HOOK_END else 36
    for s in chosen:
        if s["beat"] != c["beat"] or s is c:
            continue
        a1, a2 = sorted((s, c), key=lambda x: x["f"])
        pair = {s["kind"], c["kind"]} <= {"click"} or (a1["kind"] in ("swoosh", "swooshL") and a2["kind"] in BEEPS + ("click",)
                                                         and 0 <= a2["f"] - a1["f"] <= 30)
        if abs(f - s["f"]) < gap and not pair and not ({s["kind"], c["kind"]} & set(SECTION)):
            r.append("%d f from %s in the same visual" % (abs(f - s["f"]), s["kind"]))
    if c["kind"] == "camera" and f >= HOOK_END and any(s["kind"] == "camera" and abs(f - s["f"]) < 240 and s["f"] >= HOOK_END - 240
                                                       for s in chosen):
        r.append("shutter within 240 f")
    if c["kind"] == "data" and sum(1 for s in chosen if s["kind"] == "data") >= 2:
        r.append("data beds > 2")
    if c["kind"] == "riser" and any(s["kind"] == "riser" for s in chosen):
        r.append("riser twice")
    if f + 1 > END:
        r.append("past the end")
    return r


chosen, gave_way, pin_fails = [], [], []
for c in [c for c in cands if c["pri"] == 1]:
    chosen.append(c)
for c in chosen:
    rest = [s for s in chosen if s is not c and s["f"] <= c["f"]]
    bad = check(c, rest)
    if bad:
        pin_fails.append("%d %s %s: %s" % (c["f"], c["kind"], c["beat"], "; ".join(bad)))
for c in [c for c in cands if c["pri"] == 0]:
    bad = check(c, chosen)
    # an auto add must also leave every later sound inside its caps
    if not bad:
        trial = sorted(chosen + [c], key=lambda s: s["f"])
        bad = ["pushes %d %s over: %s" % (s["f"], s["kind"], check(s, [t for t in trial if t is not s and t["f"] <= s["f"]])[0])
               for s in trial if s["f"] > c["f"] and check(s, [t for t in trial if t is not s and t["f"] <= s["f"]])
               and not check(s, [t for t in chosen if t is not s and t["f"] <= s["f"]])][:1]
    if bad:
        gave_way.append("%d %s %s: %s" % (c["f"], c["kind"], c["beat"], "; ".join(bad)))
    else:
        chosen.append(c)
chosen.sort(key=lambda c: c["f"])

# ------------------------------------------------------------------------------------------------ levels against the music (#3)
meas = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
if os.path.exists(V2CACHE):
    for k, v in json.load(open(V2CACHE, encoding="utf-8")).items():
        meas.setdefault(k, v)


def median_db(p, a, b):
    """median 1 s power-averaged level (dB) of file p between source seconds a and b (video 2's method, cached per file)."""
    k = "%s|%d" % (os.path.basename(p), os.path.getsize(p))
    if k not in meas:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", "11025", "-f", "f32le", "-"], capture_output=True).stdout
        x = np.frombuffer(raw, np.float32).astype(np.float64)
        hop = 11025 / FPS
        meas[k] = [round(10 * np.log10(np.mean(x[int(i * hop):int(i * hop) + int(hop)] ** 2) + 1e-12), 1) for i in range(int(len(x) / hop))]
    db = np.array(meas[k])
    sm = 10 * np.log10(np.convolve(10 ** (db / 10), np.ones(24) / 24, "same") + 1e-12)
    return float(np.median(sm[int(a * FPS):max(int(a * FPS) + 1, int(b * FPS))]))


rr3 = json.load(open(RR3, encoding="utf-8"))
t3 = [t for t in rr3["timelines"] if t["name"] == CFG["reference"]["timeline"]][0]
m3 = [{"rec": a["s"], "end": a["e"], "path": a["path"], "src_s": a["src"] / FPS, "vol": a["AudioVolume"]}
      for a in t3["audio"] if a["tr"] == 2 and a["enabled"]]
for m in m3 + MUS:
    m["eff"] = m["vol"] + median_db(m["path"], m["src_s"], m["src_s"] + (m["end"] - m["rec"]) / FPS)
NAME = lambda p: os.path.splitext(os.path.basename(p))[0].replace("_pcm", "")
rel3 = collections.defaultdict(list)
for a in t3["audio"]:
    if a["tr"] >= 3 and a["enabled"]:
        nm3 = os.path.splitext(a["name"])[0]
        k3 = next((k for k, v in PAL.items() if NAME(v[0]) == nm3), None)
        mm = next((m for m in m3 if m["rec"] <= a["s"] + (PEAK.get(k3, 2) if k3 else 2) < m["end"]), None)
        if mm:
            rel3[nm3].append(a["AudioVolume"] - mm["eff"])
json.dump(meas, open(CACHE, "w", encoding="utf-8"))
REL_MAX = {k: max(v) for k, v in rel3.items()}

if CAM and CAM_MP4 and not os.path.exists(CAM):
    os.makedirs(CONV, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", CAM_MP4, "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", CAM], check=True)

sfx, clamped = [], []
for c in chosen:
    p, vol, n, src = PAL[c["kind"]]
    n = max(3, min(n, END - c["f"]))
    mm = next((m for m in MUS if m["rec"] <= c["f"] + PEAK.get(c["kind"], 2) < m["end"]), None)
    nm = NAME(p)
    if mm and nm in REL_MAX and vol - mm["eff"] > REL_MAX[nm] + 1e-6:
        clamped.append("%d %s %s %.1f -> %.1f (under %s, music eff %.1f dB)" % (c["f"], c["beat"], nm, vol, REL_MAX[nm] + mm["eff"],
                                                                               mm["cue"][3:-4], mm["eff"]))
        vol = REL_MAX[nm] + mm["eff"]
    sfx.append({"path": p, "rec": c["f"], "len": n, "vol": round(vol, 1), "src": src, "kind": c["kind"], "beat": c["beat"],
                "event": c["what"], "cue": mm["cue"][3:-4] if mm else None, "auto": c["pri"] == 0})
busy = {t: -1 for t in (3, 4, 5, 6)}
for s in sfx:
    order = (6, 5, 4, 3) if s["kind"] in ("data", "lowhit", "lowhitQ", "lowhit0", "riser") else (3, 4, 5, 6)
    free = [t for t in order if busy[t] <= s["rec"]]
    s["tr"] = free[0]; busy[free[0]] = s["rec"] + s["len"]

# ------------------------------------------------------------------------------------------------ validate (merge_plan checks)
probs = []
dur = {}
for p in {s["path"] for s in sfx} | {m["path"] for m in MUS}:
    if not os.path.exists(p):
        probs.append("missing " + p); continue
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout
    dur[p] = float(o.strip() or 0)
    if dur[p] <= 0:
        probs.append("does not decode " + p)
for s in sfx:
    if (s["src"] + s["len"]) / FPS > dur.get(s["path"], 0) + 1e-3:
        probs.append("%d %s: in+len %.3f s > file %.3f s" % (s["rec"], NAME(s["path"]), (s["src"] + s["len"]) / FPS, dur.get(s["path"], 0)))
    if s["rec"] + s["len"] > END:
        probs.append("%d past the end" % s["rec"])
for t in (3, 4, 5, 6):
    tr = sorted((s for s in sfx if s["tr"] == t), key=lambda s: s["rec"])
    for a, b in zip(tr, tr[1:]):
        if a["rec"] + a["len"] > b["rec"]:
            probs.append("overlap on A%d at %d" % (t, b["rec"]))
for m in MUS:
    if m["src_s"] + (m["end"] - m["rec"]) / FPS > dur.get(m["path"], 0) + 1e-3:
        probs.append("music %s runs past its file" % m["cue"])
mu = sorted(MUS, key=lambda m: m["rec"])
if mu[0]["rec"] != 0 or mu[-1]["end"] != END or any(a["end"] != b["rec"] for a, b in zip(mu, mu[1:])):
    probs.append("music not contiguous 0-%d" % END)
if len({m["path"] for m in MUS}) != len(MUS):
    probs.append("a song plays twice")
pal_files = {v[0] for v in PAL.values()}
if any(s["path"] not in pal_files for s in sfx):
    probs.append("file outside the palette")
lowhits = [s for s in sfx if s["kind"].startswith("lowhit")]
_nr, _nd = sum(s["kind"] == "riser" for s in sfx), sum(s["kind"] == "data" for s in sfx)
if (("section_hits" in EXPECT and len(lowhits) != EXPECT["section_hits"]) or ("risers" in EXPECT and _nr != EXPECT["risers"])
        or ("max_data" in EXPECT and _nd > EXPECT["max_data"])):
    probs.append("section hits %d (want %s), risers %d, data %d" % (len(lowhits), EXPECT.get("section_hits", "any"), _nr, _nd))
probs += ["PIN CAP: " + x for x in pin_fails] + ["UNRESOLVED: " + x for x in unresolved]

plan = {"timeline": TIMELINE, "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "by": CFG.get("by", "sound_plan.py"), "music_source": MUSIC,
        "music": [{k: m[k] for k in ("path", "rec", "end", "src_s", "vol", "fade_in", "fade_out", "section", "cue", "lufs")} for m in MUS],
        "sfx": [{k: s[k] for k in ("path", "rec", "len", "src", "vol", "tr", "kind", "beat", "event", "cue", "auto")} for s in sfx],
        "a1": {"note": "not placed by sound_place.py: lav +6 dB per clip as delivered, Voice Isolation 44 on A1 (DECISIONS #17)"},
        "checks": {"problems": probs, "clamped": clamped, "gave_way": gave_way, "drift": notes_drift, "stale_manifests": stale}}
json.dump(plan, open(os.path.join(HERE, "sound_plan.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

cnt = collections.Counter(NAME(s["path"]) for s in sfx)
mins = [sum(1 for s in sfx if m * 1438 <= s["rec"] < (m + 1) * 1438) for m in range(-(-END // 1438))]
print("sfx", len(sfx), "(pins %d, auto %d)" % (sum(not s["auto"] for s in sfx), sum(s["auto"] for s in sfx)),
      "| hook", sum(s["rec"] < HOOK_END for s in sfx), "| per min", mins, "| a minute %.1f" % (len(sfx) / (END / FPS / 60)))
print("files", dict(cnt))
print("problems", len(probs)); [print("  ", p) for p in probs]
print("clamped", len(clamped)); [print("  ", c) for c in clamped]
print("gave way", len(gave_way)); [print("  ", g) for g in gave_way]
print("drift from", CFG.get("was_date", "plan time"), notes_drift, "| stale manifests (newer than %s)" % os.path.basename(EVENTS), stale)
print("REL_MAX (#3, SFX dB minus music eff)", {k: round(v, 1) for k, v in REL_MAX.items()})
print("->", os.path.join(HERE, "sound_plan.json"))
