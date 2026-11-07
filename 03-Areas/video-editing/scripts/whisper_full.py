"""Whole-file Whisper on the GPU: segments with word times, for mapping footage to a script
(rulebook A1.21) and for studying a reference video's speech.

    python whisper_full.py <media file> <out.json> [--model small.en]

- ffmpeg decodes the audio (faster-whisper's own decoder breaks on PyAV 19 here).
- Default model: mobiuslabsgmbh/faster-whisper-large-v3-turbo (cached locally, 1.6 GB).
  small.en is not fully cached on this PC (2026-11-06): pulling it over a busy line stalls
  for many minutes, so the script runs with HF_HUB_OFFLINE=1 and uses only cached models.
- The pip nvidia-cublas/cudnn DLL folders are added the same way uhm_transcribe.py does.
Output: [{"s": start, "e": end, "t": text, "w": [[start, end, word], ...]}, ...] in seconds.
Built 2026-11-06 (Lewis, The Art of Winning on YouTube).
"""
import glob, json, os, site, subprocess, sys

os.environ.setdefault("HF_HUB_OFFLINE", "1")
for p in site.getsitepackages() + [site.getusersitepackages()]:
    for b in glob.glob(os.path.join(p, "nvidia", "*", "bin")):
        os.add_dll_directory(b)
        os.environ["PATH"] = b + os.pathsep + os.environ["PATH"]

import numpy as np
from faster_whisper import WhisperModel


def main():
    args = sys.argv[1:]
    model = "mobiuslabsgmbh/faster-whisper-large-v3-turbo"
    if "--model" in args:
        i = args.index("--model"); model = args[i + 1]; del args[i:i + 2]
    media, out = args
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", media, "-map", "0:a:0", "-ac", "1",
                          "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.float32)
    m = WhisperModel(model, device="cuda", compute_type="float16")
    segs, _ = m.transcribe(audio, language="en", vad_filter=True, word_timestamps=True,
                           beam_size=5, condition_on_previous_text=False)
    res = [{"s": round(s.start, 2), "e": round(s.end, 2), "t": s.text.strip(),
            "w": [[round(w.start, 2), round(w.end, 2), w.word] for w in (s.words or [])]} for s in segs]
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False)
    print(len(res), "segments,", round(len(audio) / 16000 / 60, 1), "min")


if __name__ == "__main__":
    main()
