# Offline mix check of a sound plan (no Resolve): mix loudness, true peak, limiter activity, speech on top of music + SFX per section and hit; writes mix_check.json.
# Usage: python mix_check.py --plan sound_plan.json --items cut_items.json --lav <conformed lav.wav> --len 12100 --out <dir> [--scratch <tmp>] [--cut-label "Cut v5"]
# Promoted from video 4 on 2026-10-30.
"""Offline mix check of sound_plan.json (editor-builder, 2026-10-29). No Resolve: rebuilds A1 (the lav at +6 dB per clip, the
audio items of the cut), A2 music and A3-A6 SFX at the plan's clip levels and fades, 48 kHz stereo, then measures:
- the mix: integrated loudness, true peak, LRA (ffmpeg ebur128), the master gain to -16 LUFS and the result after a
  -1.5 dBFS limiter (the final target: about -16 LUFS integrated, true peak <= -1 dBTP; DECISIONS #17);
- speech on top: BS.1770 momentary (400 ms) of the speech stem against music + SFX, per section and per SFX hit.
Assumptions (stated in the notes): the mono lav sits at 0 dB in both channels of the stereo mix (Resolve's mono-to-stereo
mapping is not verified here); Voice Isolation 44 is not modelled. Writes mix_check.json into --out; stems go to
the --scratch folder (default %TEMP%) and are removed at the end."""
import argparse, json, os, subprocess, sys, statistics
import numpy as np
from scipy.signal import lfilter

ap = argparse.ArgumentParser(description="Offline mix check of a sound plan: mix loudness, true peak, limiter activity, speech on top of music + SFX.")
ap.add_argument("--plan", required=True, help="sound_plan.json")
ap.add_argument("--items", required=True, help="cut items json: [type, track, start, end, src] rows (A1 speech = the audio track 1 rows)")
ap.add_argument("--lav", required=True, help="the conformed lav wav (the cut's source audio)")
ap.add_argument("--len", type=int, required=True, help="timeline length in frames")
ap.add_argument("--out", required=True, help="folder for mix_check.json")
ap.add_argument("--scratch", default=os.environ.get("TEMP", "."), help="folder for the temporary stems (default: %%TEMP%%)")
ap.add_argument("--lav-gain-db", type=float, default=6.0, help="gain on each A1 clip (default: %(default)s)")
ap.add_argument("--cut-label", default="Cut", help="name of the cut, for the assumptions text")
A = ap.parse_args()
HERE = A.out
os.makedirs(HERE, exist_ok=True)
TMP = A.scratch
SR, SPF = 48000, 2002                  # 48000 / (24000/1001) = 2002 samples per frame exactly
END = A.len
N = END * SPF
LAV = A.lav
ITEMS = A.items
plan = json.load(open(A.plan, encoding="utf-8"))


def dec(path, ss=0.0, n=None, ch=2):
    cmd = ["ffmpeg", "-v", "error", "-ss", "%.6f" % ss, "-i", path] + (["-t", "%.6f" % (n / SR + 0.05)] if n else []) + \
          ["-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, ch)
    return x[:n] if n else x


def db2g(d):
    return 10 ** (d / 20)


def fade(x, fi, fo):
    x = x.copy()
    if fi:
        k = min(len(x), fi * SPF); x[:k] *= np.linspace(0, 1, k)[:, None]
    if fo:
        k = min(len(x), fo * SPF); x[-k:] *= np.linspace(1, 0, k)[:, None]
    return x


speech = np.zeros((N, 2), np.float32)
lav = dec(LAV, ch=1)[:, 0]
for typ, tr, a, b, src in json.load(open(ITEMS, encoding="utf-8")):
    if typ != "audio" or tr != 1:
        continue
    seg = lav[src * SPF: (src + b - a) * SPF] * db2g(A.lav_gain_db)
    speech[a * SPF: a * SPF + len(seg)] += seg[:, None]
music = np.zeros((N, 2), np.float32)
for m in plan["music"]:
    n = (m["end"] - m["rec"]) * SPF
    x = dec(m["path"], m["src_s"], n)
    x = fade(x, m.get("fade_in", 0), m.get("fade_out", 0)) * db2g(m["vol"])
    music[m["rec"] * SPF: m["rec"] * SPF + len(x)] += x
sfx = np.zeros((N, 2), np.float32)
cache = {}
for s in plan["sfx"]:
    if s["path"] not in cache:
        cache[s["path"]] = dec(s["path"])
    x = cache[s["path"]][s["src"] * SPF: (s["src"] + s["len"]) * SPF] * db2g(s["vol"])
    a = s["rec"] * SPF
    x = x[:N - a]
    sfx[a: a + len(x)] += x
mix = speech + music + sfx

# ------------------------------------------------------------------------------------------------ BS.1770 momentary
B1 = ([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585])
B2 = ([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621])


def momentary(x):
    """400 ms K-weighted loudness every 100 ms (LUFS)."""
    y = lfilter(*B2, lfilter(*B1, x.astype(np.float64), axis=0), axis=0)
    p = (y ** 2).sum(1)
    hop, win = SR // 10, SR * 4 // 10
    c = np.concatenate([[0], np.cumsum(p)])
    idx = np.arange(0, len(p) - win, hop)
    return -0.691 + 10 * np.log10((c[idx + win] - c[idx]) / win + 1e-15)


Ms, Mm, Mx, Mb = momentary(speech), momentary(music), momentary(sfx), momentary(music + sfx)
blk = lambda f: int(f / (24000 / 1001) * 10)            # frame -> momentary block index (block i covers i*0.1 .. i*0.1+0.4 s)


def ebur(path_or_raw, af=""):
    cmd = ["ffmpeg", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", path_or_raw, "-af",
           (af + "," if af else "") + "ebur128=peak=true", "-f", "null", "-"]
    e = subprocess.run(cmd, capture_output=True, text=True).stderr.splitlines()
    out = {}
    for l in e:
        t = l.strip()
        if t.startswith("I:"): out["I"] = float(t.split()[1])
        elif t.startswith("LRA:"): out["LRA"] = float(t.split()[1])
        elif t.startswith("Peak:"): out["TP"] = float(t.split()[1])
    return out


raw = os.path.join(TMP, "mix_check.f32")
mix.astype(np.float32).tofile(raw)
pre = ebur(raw)
sp_raw = os.path.join(TMP, "speech_check.f32")
speech.astype(np.float32).tofile(sp_raw)
sp = ebur(sp_raw)
G = round(-16.0 - pre["I"], 1)
# how hard a -1.5 dBFS limiter works after the gain: sample peak per 10 ms block of the gained mix
pk = np.abs(mix[: (N // 480) * 480]).max(1).reshape(-1, 480).max(1) * db2g(G)
over_db = 20 * np.log10(pk[pk > db2g(-1.5)] / db2g(-1.5))
lim = {"blocks_10ms_over": int(len(over_db)), "share_of_time": round(float(len(over_db) / len(pk)), 4),
       "gain_reduction_db_p50": round(float(np.median(over_db)), 1) if len(over_db) else 0.0,
       "gain_reduction_db_max": round(float(over_db.max()), 1) if len(over_db) else 0.0,
       "over_3db_blocks": int((over_db > 3).sum())}
post = ebur(raw, "volume=%.1fdB,alimiter=limit=%.4f:level=false:attack=1:release=50" % (G, db2g(-1.5)))
nolim = ebur(raw, "volume=%.1fdB" % G)
for p in (raw, sp_raw):
    os.remove(p)                         # own temp files only (DECISIONS #18: delete inside python, never with the shell)

# speech on top: blocks where Alex speaks (speech momentary within 12 LU of its own median when active)
act = Ms > (np.median(Ms[Ms > -60]) - 12)
gap = (Ms - Mb)[act]
sections = []
for m in plan["music"]:
    a, b = blk(m["rec"]), blk(m["end"]) - 4
    sel = act[a:b]
    if sel.sum() < 5:
        continue
    g = (Ms[a:b] - Mm[a:b])[sel]
    sections.append({"cue": m["cue"][3:-4], "rec": m["rec"], "end": m["end"], "speech_minus_music_median": round(float(np.median(g)), 1),
                     "p5": round(float(np.percentile(g, 5)), 1)})
hits = []
for s in plan["sfx"]:
    a, b = blk(s["rec"]), max(blk(s["rec"]) + 1, blk(s["rec"] + s["len"]) - 3)
    sx = float(Mx[a:b].max())
    w = slice(max(0, a - 10), b + 10)
    spk = Ms[w][act[w]]
    sp_l = float(np.median(spk)) if len(spk) >= 3 else None
    hits.append({"rec": s["rec"], "beat": s["beat"], "file": os.path.basename(s["path"]), "vol": s["vol"], "sfx_M": round(sx, 1),
                 "speech_M": None if sp_l is None else round(sp_l, 1), "music_M": round(float(np.median(Mm[a:b])), 1),
                 "over_speech": None if sp_l is None else round(sx - sp_l, 1)})
over = [h for h in hits if h["over_speech"] is not None and h["over_speech"] > 0]
res = {"assumptions": ["mono lav at 0 dB in both channels (Resolve mono->stereo not verified)", "Voice Isolation 44 not modelled",
                       "A1 = %s audio items (lav %+g dB), no clip fades" % (A.cut_label, A.lav_gain_db)],
       "speech_alone": sp, "mix_at_plan_levels": pre, "master_gain_to_-16": G, "after_gain_no_limiter": nolim,
       "after_gain_and_limiter_-1.5dBFS": post, "limiter_activity": lim,
       "speech_minus_bed": {"median": round(float(np.median(gap)), 1), "p5": round(float(np.percentile(gap, 5)), 1),
                            "p1": round(float(np.percentile(gap, 1)), 1), "share_below_0": round(float((gap < 0).mean()), 4)},
       "sections": sections, "sfx_hits": hits, "sfx_over_speech": over}
json.dump(res, open(os.path.join(HERE, "mix_check.json"), "w", encoding="utf-8"), indent=1)
print("speech alone", sp, "| mix at plan levels", pre)
print("gain to -16:", G, "dB | no limiter", nolim, "| + limiter -1.5 dBFS", post, "| limiter", lim)
print("sfx above the music bed (momentary):", sum(1 for h in hits if h["sfx_M"] > h["music_M"]), "of", len(hits))
print("speech - (music+sfx) momentary while he speaks: median %.1f p5 %.1f p1 %.1f, below 0: %.2f %%" % (
    res["speech_minus_bed"]["median"], res["speech_minus_bed"]["p5"], res["speech_minus_bed"]["p1"], 100 * res["speech_minus_bed"]["share_below_0"]))
print("sections (speech - music median / p5):", [(x["cue"][:10], x["speech_minus_music_median"], x["p5"]) for x in sections])
print("sfx louder than speech around them:", len(over), [(h["rec"], h["file"][:14], h["over_speech"]) for h in over])
print("loudest sfx vs speech:", sorted([(h["over_speech"], h["rec"], h["file"][:14]) for h in hits if h["over_speech"] is not None])[-6:])
print("->", os.path.join(HERE, "mix_check.json"))
