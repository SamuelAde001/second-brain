# sound_plan.json + mix_check.json + the sfx events json -> sound_notes.md (every SFX, per-file counts, checks run, changes against the plan, open points).
# Usage: python sound_notes.py --plan sound_plan.json --mix mix_check.json --events sfx_events.json --notes notes.json --len 12100 --hook-end 1426 --out <dir>
# Promoted from video 4 on 2026-10-30.
"""sound_plan.json + mix_check.json + sfx events json -> sound_notes.md (editor-builder, 2026-10-29). Touches only sound_notes.md.
The video-specific wording (title, bullets, 'changed against the plan', 'open' list) comes from the --notes json
(video 4's: examples/video4_sound_notes.json); {tokens} in it are filled from the plan and the mix check."""
import json, os, collections, datetime, argparse

ap = argparse.ArgumentParser(description="sound_plan.json + mix_check.json + sfx events json -> sound_notes.md")
ap.add_argument("--plan", required=True, help="sound_plan.json")
ap.add_argument("--mix", required=True, help="mix_check.json")
ap.add_argument("--events", required=True, help="sfx events json made by sfx_events.py")
ap.add_argument("--notes", required=True, help="json with the video's wording (see examples/video4_sound_notes.json)")
ap.add_argument("--len", type=int, required=True, help="timeline length in frames")
ap.add_argument("--hook-end", type=int, required=True, help="last frame of the hook")
ap.add_argument("--out", required=True, help="folder for sound_notes.md")
A = ap.parse_args()
P = json.load(open(A.plan, encoding="utf-8"))
M = json.load(open(A.mix, encoding="utf-8"))
EV = json.load(open(A.events, encoding="utf-8"))
N = json.load(open(A.notes, encoding="utf-8"))


def T(s, **kw):
    for k, v in kw.items():
        s = s.replace("{" + k + "}", str(v))
    return s


FPS = 24000 / 1001
S, MU, C = P["sfx"], P["music"], P["checks"]
nm = lambda p: os.path.splitext(os.path.basename(p))[0].replace("_pcm", "")
tc = lambda f: "%d:%02d.%02d" % (f // 24 // 60, f // 24 % 60, f % 24)
BEEP = tuple(N["beep_names"])
bf = sorted(s["rec"] for s in S if nm(s["path"]) in BEEP)
max2 = max(sum(1 for x in bf if a <= x < a + 48) for a in bf)
max4 = max(sum(1 for x in bf if a <= x < a + 96) for a in bf)
mins = [sum(1 for s in S if m * 1438 <= s["rec"] < (m + 1) * 1438) for m in range(-(-A.len // 1438))]
beats_all = {o["beat"] for o in EV["ops"]}
beats_snd = {s["beat"] for s in S}
lands = [e for e in EV["events"] if e["kind"] in ("pop", "count", "reveal", "cutin", "whoosh", "light")]
lit = sum(1 for e in lands if any(abs(s["rec"] - e["f"]) <= 6 for s in S))
lim = M["after_gain_and_limiter_-1.5dBFS"]
L = []
w = L.append
os.makedirs(A.out, exist_ok=True)
w(T(N["title"], generated=P["generated"][:16].replace("T", " ")))
w("")
w(T(N["plan_line"], timeline=P["timeline"]))
w("")
w(N["chain"])
w("")
w(N["place"])
w("")
w("## Summary")
w(T(N["music_bullet"], pieces=len(MU)))
w(T(N["sfx_bullet"], n=len(S), n_files=len({s["path"] for s in S}), per_min="%.1f" % (len(S) / (A.len / FPS / 60)),
    hook_end=A.hook_end, hook=sum(s["rec"] < A.hook_end for s in S), mins=mins))
w(N["reveals_bullet"])
w(N["silent_bullet"])
_h = max((h for h in M["sfx_hits"] if h["over_speech"] is not None), key=lambda h: h["over_speech"])
w(T(N["speech_bullet"], median="%.1f" % M["speech_minus_bed"]["median"], p5="%.1f" % M["speech_minus_bed"]["p5"],
    p1="%.1f" % M["speech_minus_bed"]["p1"], close_file=os.path.splitext(_h["file"])[0], close_rec=_h["rec"],
    close_over="%.1f" % _h["over_speech"], cue_min=min(x["speech_minus_music_median"] for x in M["sections"]),
    cue_max=max(x["speech_minus_music_median"] for x in M["sections"])))
w(T(N["loudness_bullet"], lufs="%.1f" % M["mix_at_plan_levels"]["I"], tp="%.1f" % M["mix_at_plan_levels"]["TP"],
    speech_lufs="%.1f" % M["speech_alone"]["I"], gain="%.1f" % M["master_gain_to_-16"], lim_lufs="%.1f" % lim["I"], lim_tp="%.1f" % lim["TP"],
    lim_share="%.2f" % (100 * M["limiter_activity"]["share_of_time"]), lim_p50="%.1f" % M["limiter_activity"]["gain_reduction_db_p50"],
    lim_max="%.1f" % M["limiter_activity"]["gain_reduction_db_max"]))
w(N["a1_bullet"])
w("")
w("## Every SFX")
w("Frame = timeline frame from 0 (sound_place adds the timeline start). Gain = the clip's AudioVolume in dB. 'auto' = added on a real event because the caps allowed it.")
w("")
w("| # | Frame | Time | Tr | File | Gain dB | Len f | Beat | Event | Music under |")
w("|---|---|---|---|---|---|---|---|---|---|")
for i, s in enumerate(S, 1):
    w("| %d | %d | %s | A%d | %s%s | %.1f | %d | %s | %s%s | %s |" % (i, s["rec"], tc(s["rec"]), s["tr"], nm(s["path"]),
      " (src f%d)" % s["src"] if s["src"] else "", s["vol"], s["len"], s["beat"], s["event"], " (auto)" if s["auto"] else "", s["cue"] or ""))
w("")
w("## Per file")
w("| File | Count | Gains dB |")
w("|---|---|---|")
for f, n in collections.Counter(nm(s["path"]) for s in S).most_common():
    g = sorted({s["vol"] for s in S if nm(s["path"]) == f})
    w("| %s | %d | %s |" % (f, n, ", ".join("%.1f" % x for x in g)))
w("")
w("## Checks run (all by script) and their result")
w(T(N["validation_line"], data_beds=sum(nm(s["path"]).startswith(N["data_prefix"]) for s in S), problems=len(C["problems"])))
w("- Caps (bible 07): max %d beeps inside 2 s (cap 3), %d inside 4 s (cap 4); no beep within 20 f after a Low Hit; after the hook at most 7 sounds in any 30 s (section hits aside); 36 f between sounds inside one visual in the body (12 f in the hook; click runs and his swoosh-then-beep pair aside); shutters 240 f apart after the hook. Pins breaking a cap: **%d**." % (
    max2, max4, sum(1 for p in C["problems"] if p.startswith("PIN CAP"))))
w("- Events: every pin's frame is re-read from the installed comps (`%s`, %d events from %d ops in %d manifests) or from the capture timing in the manifest note; drift since %s: %s; manifests newer than the events file: %s." % (
    os.path.basename(A.events), len(EV["events"]), len(EV["ops"]), len(beats_all), N.get("was_date", "plan time"), C["drift"] or "none", C["stale_manifests"] or "none"))
w("- Share with a sound: %d of %d beats; %d of %d entrances/landings/lights within 6 f of a sound (%.0f %%; bible: about a third of reveals)." % (
    len(beats_snd & beats_all), len(beats_all), lit, len(lands), 100 * lit / max(1, len(lands))))
w("- Levels against the music: each SFX kept at or under his #3 level relative to the song under it (his SFX dB minus the measured song level on #3). Lowered: %d." % len(C["clamped"]))
for c in C["clamped"]:
    w("  - %s" % c)
w("- Gave way to the caps (auto adds not placed): %d." % len(C["gave_way"]))
for g in C["gave_way"]:
    w("  - %s" % g)
w("- Offline mix (`mix_check.py`): assumptions: %s." % "; ".join(M["assumptions"]))
w("")
w("## Changed against plan v2's per-beat SFX lines (beats.json)")
for x in N["changed"]:
    w("- " + x)
w("")
w("## Open")
w(T(N["open"][0], density="%.1f" % (len(S) / (A.len / FPS / 60))))
w(T(N["open"][1], gain="%.1f" % M["master_gain_to_-16"], gain3="%.1f" % (M["master_gain_to_-16"] + 3)))
w(N["open"][2])
w(N["open"][3])
w(N["open"][4])
w(N["open"][5])
w("")
open(os.path.join(A.out, "sound_notes.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("notes", len(L), "lines | sfx", len(S), "| max beeps 2s/4s", max2, max4, "| beats with sound", len(beats_snd & beats_all), "/", len(beats_all),
      "| landings with sound %d/%d" % (lit, len(lands)))
