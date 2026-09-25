"""Find the leftover noise clips after Ripple Delete Silence.

Ripple Delete Silence leaves small clips of room noise, breaths and clicks behind.
This measures the mic level inside every A1 clip of an exported timeline and sorts
them into noise (safe to ripple-delete), ambiguous (colour for Samuel) and speech.

Usage:
    python noise_clips.py <timeline.xml (FCP7)> <mic.wav> [--noise-db -40] [--fps 23.976]

Stock Python + ffmpeg. The XML's clip <in>/<out> are in timeline frames, so
source seconds = in / timeline fps (checked against GetSourceStartTime on Route Rise #3).

Rules (Route Rise #3, 2026-09-25; raw mic, before the +6 dB clip gain):
  noise     = no 50 ms window above --noise-db (speech body never drops below -36 dB)
  ambiguous = 12 frames or shorter AND has a window above --noise-db (word, breath or click?)
  speech    = everything else
Prints the start frames of each group; noise starts go into Timeline.DeleteClips(..., True)
together with the V1/V2 items at the same span.
"""
import argparse, os, subprocess, tempfile, xml.etree.ElementTree as ET


def rms_windows(wav):
    # file= takes a relative name: a Windows drive colon breaks the filter string
    with tempfile.TemporaryDirectory() as d:
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", wav, "-af",
               "pan=mono|c0=c0,aresample=8000,asetnsamples=n=400:p=0,astats=metadata=1:reset=1,"
               "ametadata=print:key=lavfi.astats.Overall.RMS_level:file=rms.txt", "-f", "null", "-"]
        subprocess.run(cmd, cwd=d, check=True)
        out = open(os.path.join(d, "rms.txt")).read()
    v = []
    for line in out.splitlines():
        if "RMS_level=" in line:
            x = line.split("=")[1].strip()
            v.append(-120.0 if "inf" in x else float(x))
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xml"); ap.add_argument("wav")
    ap.add_argument("--noise-db", type=float, default=-40.0)
    ap.add_argument("--fps", type=float, default=24000 / 1001)
    a = ap.parse_args()
    v = rms_windows(a.wav)
    if not v:
        raise SystemExit("no RMS values read from ffmpeg")
    seq = ET.parse(a.xml).getroot().find(".//sequence")
    clips = seq.findall("media/audio/track")[0].findall("clipitem")
    groups = {"noise": [], "ambiguous": [], "speech": []}
    for c in clips:
        st, en, i, o = [int(c.find(k).text) for k in ("start", "end", "in", "out")]
        w0 = int(i / a.fps / 0.05)
        w = v[w0:max(w0 + 1, int(o / a.fps / 0.05) + 1)]
        loud = sum(1 for x in w if x > a.noise_db)
        g = "noise" if loud == 0 else ("ambiguous" if en - st <= 12 else "speech")
        groups[g].append((st, en - st, round(max(w), 1)))
    for g, rows in groups.items():
        print(f"{g}: {len(rows)} clips, {sum(r[1] for r in rows)} frames")
        if g != "speech":
            print("  starts:", [r[0] for r in rows])


if __name__ == "__main__":
    main()
