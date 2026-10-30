# Loudness of a render (integrated LUFS, true peak, LRA), and a two-pass -16 LUFS / -1 dBTP copy with --fix (DECISIONS #55).
# Usage: python loudness.py <in.mp4> [--fix <out.mp4>]
# Promoted from video 4 on 2026-10-30.
# Loudness of a render, and a -16 LUFS / -1 dBTP copy (Editor, 2026-10-29, DECISIONS #55).
#   python loudness.py <in.mp4>                 -> integrated LUFS, true peak, LRA (ffmpeg loudnorm measure pass)
#   python loudness.py <in.mp4> --fix <out.mp4> -> two-pass linear loudnorm to -16 LUFS / -1 dBTP; video stream copied,
#                                                  audio AAC 320k 48 kHz; then measures <out.mp4> again
import argparse, json, re, subprocess, sys

I, TP, LRA = -16.0, -1.0, 11.0


def measure(f):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", f, "-vn", "-af",
                          "loudnorm=I=%s:TP=%s:LRA=%s:print_format=json" % (I, TP, LRA), "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S)[-1])
    return m


def main():
    ap = argparse.ArgumentParser(description="Loudness of a render (ffmpeg loudnorm measure pass); --fix writes a -16 LUFS / -1 dBTP copy.")
    ap.add_argument("input", help="render to measure (mp4 / wav)")
    ap.add_argument("--fix", metavar="OUT", help="write a two-pass linear loudnorm copy (-16 LUFS / -1 dBTP; video copied, audio AAC 320k 48 kHz) and measure it")
    a = ap.parse_args()
    m = measure(a.input)
    print("in : %s LUFS, true peak %s dBTP, LRA %s LU" % (m["input_i"], m["input_tp"], m["input_lra"]))
    if a.fix:
        out = a.fix
        af = ("loudnorm=I=%s:TP=%s:LRA=%s:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true"
              % (I, TP, LRA, m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.input, "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", af,
                        "-ar", "48000", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", out], check=True)
        n = measure(out)
        print("out: %s LUFS, true peak %s dBTP, LRA %s LU -> %s" % (n["input_i"], n["input_tp"], n["input_lra"], out))
        if n.get("normalization_type") == "dynamic":
            print("note: loudnorm fell back to dynamic mode on the measure pass")


if __name__ == "__main__":
    main()
