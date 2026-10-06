"""Filler-aware word-timed transcription of per-clip WAVs (the uhm pass, cut SOP step 6).

Resolve's transcription drops "uh"/"um". faster-whisper keeps them when the initial
prompt is itself full of fillers. Writes one JSON: {clip_name: [[start_s, end_s, word], ...]}.

    python uhm_transcribe.py <wav_folder> <out.json> [name1 name2 ...]

Model: small.en on the CPU (int8), installed 2026-10-06 with Samuel's yes.
"""
import glob, json, os, shutil, subprocess, sys, time
import numpy as np
from faster_whisper import WhisperModel

# faster-whisper's own decoder breaks with PyAV 19 (metadata_errors), so decode with ffmpeg.
FFMPEG = shutil.which("ffmpeg") or (glob.glob(os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe")) or ["ffmpeg"])[0]

def load(path):
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

PROMPT = "Umm, so, uh, I mean, like, uh, you know. Hmm, so we, um, we start with the, uh, the list."

def main():
    folder, out = sys.argv[1], sys.argv[2]
    names = sys.argv[3:] or sorted(f[:-4] for f in os.listdir(folder) if f.endswith(".wav"))
    done = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    t0 = time.time()
    for n, name in enumerate(names):
        if name in done:
            continue
        segs, _ = model.transcribe(load(os.path.join(folder, name + ".wav")), language="en",
                                   word_timestamps=True, initial_prompt=PROMPT,
                                   vad_filter=False, condition_on_previous_text=False)
        done[name] = [[round(w.start, 3), round(w.end, 3), w.word.strip()] for s in segs for w in s.words]
        if n % 20 == 0:
            json.dump(done, open(out, "w", encoding="utf-8"))
            print(f"{n+1}/{len(names)} {time.time()-t0:.0f}s", flush=True)
    json.dump(done, open(out, "w", encoding="utf-8"))
    print("done", len(done))

if __name__ == "__main__":
    main()
