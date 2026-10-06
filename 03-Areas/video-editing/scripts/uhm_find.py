"""Find uhms, breaths, long pauses and in-clip repeats inside the clips of a cut (cut SOP step 6).

Reads the filler-aware word times from uhm_transcribe.py and the per-clip WAVs, and writes
trims as timeline frame ranges to remove, cut points snapped to the quietest 10 ms.

    python uhm_find.py <working_dir> <wav_folder>

<working_dir> holds v2_clips.json (clip list: start, dur), v3_cut_list.json (clips already
removed), whisper_words.json, and optional manual_trims.json {"c142": [[from_s, to_s]], ...}.
Writes trims.json [{clip, kind, a, b, tl_in, tl_out, text}] (a/b clip frames, b exclusive;
tl_in/tl_out timeline frames on the cut before any trim, tl_out inclusive) and prints a review.
"""
import json, os, re, subprocess, sys, shutil, glob
import numpy as np

FPS = 24000 / 1001
FFMPEG = shutil.which("ffmpeg") or (glob.glob(os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe")) or ["ffmpeg"])[0]
FILLERS = {"uh", "um", "umm", "uhm", "uhh", "ah", "er", "erm", "hmm", "mm", "mhm"}
MIN_TRIM = 3          # frames; anything shorter isn't worth a cut
PAUSE = 0.70          # s between words before a pause gets shortened
KEEP_PAUSE = (0.15, 0.12)  # s kept after the previous word / before the next
# A head/tail/pause trim must be quiet: at most 25% of its 10 ms windows within 12 dB of the
# clip's speech level, and its peak 8 dB under it. Louder means a word Whisper missed: skip it.
LOUD_DB, LOUD_SHARE, PEAK_DB = 12, 0.25, 8

def env(path):
    """10 ms RMS in dB."""
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    n = len(x) // 160
    r = np.sqrt((x[:n * 160].reshape(n, 160) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(r)

def quietest(e, t0, t1):
    """Time (s) of the quietest 10 ms window in [t0, t1]."""
    i0, i1 = max(0, int(t0 * 100)), min(len(e), int(t1 * 100) + 1)
    if i1 <= i0:
        return max(0.0, t0)
    return (i0 + int(np.argmin(e[i0:i1]))) / 100

def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())

def main():
    wd, wavs = sys.argv[1], sys.argv[2]
    clips = json.load(open(os.path.join(wd, "v2_clips.json")))
    cut = set(json.load(open(os.path.join(wd, "v3_cut_list.json"))))
    W = json.load(open(os.path.join(wd, "whisper_words.json"), encoding="utf-8"))
    mp = os.path.join(wd, "manual_trims.json")
    manual = json.load(open(mp)) if os.path.exists(mp) else {}
    trims, T = [], 0
    for i, c in enumerate(clips):
        if i in cut:
            continue
        name, D = "c%03d" % i, c["dur"]
        dur_s = D / FPS
        words = [w for w in W.get(name, []) if w[1] > w[0]]
        e = env(os.path.join(wavs, name + ".wav"))
        real = [w for w in words if norm(w[2]) not in FILLERS and norm(w[2])]
        out = []  # (kind, from_s, to_s, text)
        if real:
            s0, e1 = real[0][0], real[-1][1]
            head = [w[2] for w in words if w[1] <= s0 + 0.01 and norm(w[2]) in FILLERS]
            if head or s0 > 0.30:
                out.append(("head-filler" if head else "head", 0.0, quietest(e, s0 - 0.20, s0 + 0.02), " ".join(head)))
            tail = [w[2] for w in words if w[0] >= e1 - 0.01 and norm(w[2]) in FILLERS]
            if tail or dur_s - e1 > 0.40:
                out.append(("tail-filler" if tail else "tail", quietest(e, e1, e1 + 0.20), dur_s, " ".join(tail)))
            # fillers and long pauses between real words
            for k in range(1, len(real)):
                p, n = real[k - 1], real[k]
                mids = [w[2] for w in words if w[0] >= p[1] - 0.01 and w[1] <= n[0] + 0.01 and norm(w[2]) in FILLERS]
                if mids:
                    out.append(("mid-filler", quietest(e, p[1] - 0.03, p[1] + 0.12), quietest(e, n[0] - 0.12, n[0] + 0.02), " ".join(mids)))
                elif n[0] - p[1] > PAUSE:
                    out.append(("pause", quietest(e, p[1] + KEEP_PAUSE[0] - 0.05, p[1] + KEEP_PAUSE[0] + 0.05),
                                quietest(e, n[0] - KEEP_PAUSE[1] - 0.05, n[0] - KEEP_PAUSE[1] + 0.05),
                                f"{p[2]} … {n[2]}"))
            # repeats inside the clip, for review only (decided by hand into manual_trims.json)
            toks = [norm(w[2]) for w in real]
            for k in range(len(toks)):
                for L in (3, 2):
                    if k + 2 * L <= len(toks) and toks[k:k + L] == toks[k + L:k + 2 * L]:
                        print(f"  REPEAT {name}: {' '.join(w[2] for w in real[max(0, k - 2):k + 2 * L + 2])}")
                        break
        for a_s, b_s in manual.get(name, []):
            out.append(("manual", a_s, min(b_s, dur_s), ""))
        med = float(np.median(e[e > np.percentile(e, 50)]))
        for kind, a_s, b_s, txt in out:
            a, b = int(round(a_s * FPS)), int(round(b_s * FPS))
            a, b = max(0, a), min(D, b)
            r = e[int(a / FPS * 100):int(b / FPS * 100)]
            if kind in ("head", "tail", "pause") and len(r) and (
                    (r > med - LOUD_DB).mean() > LOUD_SHARE or r.max() > med - PEAK_DB):
                print(f"  SKIP loud {kind} {name} {a}-{b}: {' '.join(w[2] for w in real)[:60]}")
                continue
            if b - a >= MIN_TRIM and b - a < D:
                trims.append({"clip": name, "kind": kind, "a": a, "b": b, "tl_in": T + a, "tl_out": T + b - 1,
                              "text": txt, "words": " ".join(w[2] for w in real)[:90]})
        T += D
    # merge overlapping trims inside a clip
    trims.sort(key=lambda t: t["tl_in"])
    merged = []
    for t in trims:
        if merged and t["tl_in"] <= merged[-1]["tl_out"] + 1:
            m = merged[-1]
            m["tl_out"] = max(m["tl_out"], t["tl_out"]); m["b"] = max(m["b"], t["b"]); m["kind"] += "+" + t["kind"]
        else:
            merged.append(t)
    json.dump(merged, open(os.path.join(wd, "trims.json"), "w"), indent=0)
    kinds = {}
    for t in merged:
        k = t["kind"].split("+")[0]; kinds[k] = kinds.get(k, 0) + 1
    tot = sum(t["tl_out"] - t["tl_in"] + 1 for t in merged)
    print(len(merged), "trims", kinds, tot, "frames", round(tot / FPS, 1), "s; timeline", T)

if __name__ == "__main__":
    main()
