"""Find the sync offset between a camera clip and a separate mic WAV (Routerise shoots).

    python av_sync.py "<camera.MP4>" "<mic.wav>" [--window 360]

Decision tree from the Routerise cut SOP, step 1:
1. Measure the camera's scratch audio (ffmpeg volumedetect). If it carries speech
   (max above -40 dB), cross-correlate the camera audio envelope against the mic
   envelope at 100 Hz: precise to 10 ms.
2. If it's dead (the 13 Sep shoot: max -60.8 dB), fall back to motion correlation:
   a 20 Hz motion signal from the picture (mean abs inter-frame difference of a
   32x18 grey thumbnail) against the mic's 20 Hz speech envelope.
Only the first --window seconds are analysed; the offset is one constant.
Never derive the offset from file clock times (the DJI and Sony clocks drift apart).

Prints one JSON line last: {"method", "offset_s", "z"}.
offset_s > 0 means the mic started BEFORE the camera by that much, so the mic's
frame at (offset_s * fps) lines up with the camera's first frame.
Stock Python + ffmpeg only.
"""
import cmath, json, math, re, shutil, struct, subprocess, sys

FF = shutil.which("ffmpeg") or r"C:\Users\repzy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"


def run(args):
    return subprocess.run([FF, "-hide_banner", "-nostdin"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def max_volume(path, win):
    err = run(["-t", str(win), "-i", path, "-vn", "-af", "volumedetect", "-f", "null", "-"]).stderr.decode("utf-8", "ignore")
    m = re.search(r"max_volume:\s*(-?[\d.]+) dB", err)
    return float(m.group(1)) if m else -99.0


def envelope(path, win, rate, binsz=20):
    raw = run(["-t", str(win), "-i", path, "-vn", "-ac", "1", "-ar", str(rate * binsz), "-f", "s16le", "-"]).stdout
    n = len(raw) // 2
    vals = struct.unpack("<%dh" % n, raw[:n * 2])
    return [math.sqrt(sum(v * v for v in vals[k:k + binsz]) / binsz) for k in range(0, n - binsz, binsz)]


def motion(path, win, rate):
    out = run(["-hwaccel", "cuda", "-t", str(win), "-i", path, "-an", "-vf",
               f"fps={rate},scale=32x18,format=gray,tblend=all_mode=difference,signalstats,metadata=print:file=-",
               "-f", "null", "-"]).stdout.decode("utf-8", "ignore")
    return [float(l.split("=", 1)[1]) for l in out.splitlines() if "signalstats.YAVG=" in l]


def normalize(x):
    m = sum(x) / len(x)
    y = [v - m for v in x]
    sd = math.sqrt(sum(v * v for v in y) / len(y)) or 1.0
    return [v / sd for v in y]


def fft(a, inv=False):
    n = len(a); a = a[:]; j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit; bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    L = 2
    while L <= n:
        wl = cmath.exp((2j if inv else -2j) * math.pi / L); half = L >> 1
        for i in range(0, n, L):
            w = 1 + 0j
            for k in range(half):
                u = a[i + k]; v = a[i + k + half] * w
                a[i + k] = u + v; a[i + k + half] = u - v; w *= wl
        L <<= 1
    return [x / n for x in a] if inv else a


def xcorr(cam, mic):
    """Lag (samples) at which mic best matches cam; lag > 0 = mic started earlier."""
    N = 1
    while N < len(cam) + len(mic):
        N <<= 1
    A = normalize(cam) + [0.0] * (N - len(cam))
    B = normalize(mic) + [0.0] * (N - len(mic))
    FA, FB = fft([complex(x) for x in A]), fft([complex(x) for x in B])
    cr = [c.real for c in fft([FB[i] * FA[i].conjugate() for i in range(N)], inv=True)]
    bi = max(range(N), key=lambda i: cr[i])
    lag = bi if bi <= N // 2 else bi - N
    mu = sum(cr) / N
    sd = math.sqrt(sum((c - mu) ** 2 for c in cr) / N) or 1.0
    return lag, (cr[bi] - mu) / sd


def main():
    args = sys.argv[1:]
    win = 360
    if "--window" in args:
        i = args.index("--window"); win = int(args[i + 1]); del args[i:i + 2]
    cam, mic = args
    cam_max = max_volume(cam, win)
    print(f"camera audio max {cam_max:.1f} dB", flush=True)
    if cam_max > -40:
        rate = 100
        lag, z = xcorr(envelope(cam, win, rate), envelope(mic, win, rate))
        method = "camera-audio"
    else:
        rate = 20
        lag, z = xcorr(motion(cam, win, rate), envelope(mic, win, rate, 100))
        method = "motion"
    print(json.dumps({"method": method, "offset_s": round(lag / rate, 3), "z": round(z, 1)}))


if __name__ == "__main__":
    main()
