"""After a Community call: transcribe it, file the great knowledge into the teachings archive, write the members' summary.

Called by meeting_recorder.py the same night as the call (Samuel, 2026-10-28: *"I want it the same night"*).
  1. transcribe   faster-whisper large-v3-turbo on the GPU. On recordings with 4 audio tracks, track 3 (his mic)
                  and track 4 (Discord, everyone else) are transcribed apart, so lines say Samuel or Member.
  2. file         `claude -p` runs the Brand manager on call_archive_prompt.md: new teachings into the topic notes,
                  a call note in 05-Knowledge/teachings/calls/, and summary JSON for Discord.
  3. commit       only the teachings folder and the recorder log, then fetch, merge origin/main, push (never force).
  4. bot          rebuild Editors Bot's knowledge and deploy the site to production.

  python call_archive.py run FILE "Title"        all four steps (prints the summary JSON)
  python call_archive.py transcribe FILE         step 1 only
"""

import glob
import json
import os
import site
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

BRAIN = Path(__file__).resolve().parents[2]
PROMPT = Path(__file__).with_name("call_archive_prompt.md")
TEACHINGS = BRAIN / "05-Knowledge" / "teachings"
RECORDER_LOG = BRAIN / "06-Logs" / "automation" / "meeting-recorder.md"
TRANSCRIPTS = Path(r"C:\Users\repzy\Videos\Called to Edit Meetings\transcripts")  # small text, kept
WORK = Path(os.environ["LOCALAPPDATA"]) / "cte-meeting-recorder"
SITE_DIR = Path(r"C:\Users\repzy\Desktop\called-to-edit-site")
GIT_BASH = Path(r"C:\Program Files\Git\bin\bash.exe")

MODEL = "large-v3-turbo"
FILTER_MODEL = "opus"     # judgement on his teaching; Max 20x
FILTER_TIMEOUT = 60 * 60  # seconds


def ts(sec):
    h, rem = divmod(int(sec), 3600)
    return f"{h}:{rem // 60:02d}:{rem % 60:02d}"


def audio_tracks(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return len([l for l in r.stdout.split() if l.strip()])


def _pcm(path, track):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", f"0:a:{track}", "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def _model():
    for p in site.getsitepackages() + [site.getusersitepackages()]:  # pip's CUDA libraries for ctranslate2
        for b in glob.glob(os.path.join(p, "nvidia", "*", "bin")):
            os.add_dll_directory(b)
            os.environ["PATH"] = b + os.pathsep + os.environ["PATH"]
    from faster_whisper import WhisperModel
    try:
        return WhisperModel(MODEL, device="cuda", compute_type="float16")
    except Exception:
        return WhisperModel(MODEL, device="cpu", compute_type="int8")


def transcribe(path):
    """Writes <stem>.txt in TRANSCRIPTS and returns its path."""
    path = Path(path)
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    out = TRANSCRIPTS / f"{path.stem}.txt"
    n = audio_tracks(path)
    plan = [(2, "Samuel"), (3, "Member")] if n >= 4 else [(1 if n >= 2 else 0, "Call")]
    model = _model()
    lines = []
    for track, who in plan:
        segs, _ = model.transcribe(_pcm(path, track), language="en", vad_filter=True,
                                   vad_parameters={"min_silence_duration_ms": 700}, condition_on_previous_text=False,
                                   initial_prompt="Called to Edit, video editing, CapCut, DaVinci Resolve, clients, outreach, portfolio.")
        for s in segs:
            text = s.text.strip()
            if text:
                lines.append((s.start, who, text))
    lines.sort()
    out.write_text("".join(f"[{ts(t)}] {who}: {text}\n" for t, who, text in lines), encoding="utf-8")
    return out, len(lines)


def file_into_archive(transcript, title, when, length):
    """Runs the Brand manager headless. Returns the summary dict, or None."""
    WORK.mkdir(parents=True, exist_ok=True)
    summary_json = WORK / f"summary-{when:%Y-%m-%d-%H%M}.json"
    summary_json.unlink(missing_ok=True)
    body = PROMPT.read_text(encoding="utf-8").split("\n---\n", 1)[1]
    for k, v in {"title": title, "date": f"{when:%Y-%m-%d}", "length": length, "transcript": str(transcript),
                 "summary_json": str(summary_json)}.items():
        body = body.replace("{" + k + "}", v)
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}  # bill the Max plan, never the API
    claude = subprocess.run(["where", "claude.cmd"], capture_output=True, text=True).stdout.split()
    exe = claude[0] if claude else "claude"
    # the prompt goes in on stdin: a multi-line argument doesn't survive claude.cmd
    r = subprocess.run([exe, "-p", "--model", FILTER_MODEL, "--permission-mode", "acceptEdits",
                        "--allowedTools", "Read,Write,Edit,Glob,Grep", "--add-dir", str(WORK), "--add-dir", str(TRANSCRIPTS)],
                       input=body, cwd=str(BRAIN), env=env, capture_output=True, text=True, encoding="utf-8",
                       timeout=FILTER_TIMEOUT, creationflags=0x08000000)  # no window
    (WORK / "last-filter.log").write_text((r.stdout or "") + "\n--- stderr ---\n" + (r.stderr or ""), encoding="utf-8")
    try:
        return json.loads(summary_json.read_text(encoding="utf-8"))
    except Exception:
        return None


def gemini_summary(transcript, title, when):
    """Fallback when Claude can't run (signed out, limits): Gemini, read-only, writes only the members' summary.
    Filing into the archive then waits for the next session (an inbox note says so)."""
    task = WORK / "gemini-task.md"
    task.write_text(
        f"Read the transcript of the Called to Edit Community call \"{title}\" ({when:%Y-%m-%d}) at `{transcript}` "
        "(Whisper, machine-made; lines `[h:mm:ss] Speaker: text`, Samuel = Samuel's mic). Write a summary for members "
        "who missed it, from what Samuel actually said, nothing invented, no member names. Answer with ONLY this JSON, "
        'no code fence: {"topic": "<3-8 words>", "summary": "<3-5 sentences, second person where it fits>", '
        '"takeaways": ["<5-8 short points>"], "questions": ["<question> → <his answer in one line>"], "filed": 0}. '
        'If the call holds no teaching, say so in the summary and leave the lists empty.', encoding="utf-8")
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("ask_gemini.py")), "--file", str(task)],
                       capture_output=True, text=True, encoding="utf-8", timeout=1800, creationflags=0x08000000)
    out = r.stdout or ""
    try:
        return json.loads(out[out.index("{"):out.rindex("}") + 1])
    except ValueError:
        (WORK / "last-gemini.log").write_text(out + "\n--- stderr ---\n" + (r.stderr or ""), encoding="utf-8")
        return None


def inbox_note(transcript, title, when):
    """Tells the next session to file this call into the archive."""
    note = BRAIN / "01-Inbox" / f"call-to-file-{when:%Y-%m-%d-%H%M}.md"
    note.write_text(
        f"---\ntype: log\narea: called-to-edit\nstatus: needs-input\nupdated: {datetime.now():%Y-%m-%d}\n"
        f"source: local-folder\ntags: [community-call, teachings]\n---\n\n# Call to file: {title} ({when:%Y-%m-%d})\n\n"
        f"The same-night filing didn't run, so this call isn't in the teachings archive yet. Brand manager: run "
        f"`00-System/scripts/call_archive_prompt.md` on the transcript `{transcript}`, then commit and redeploy the bot "
        f"(`call_archive.py` steps 3-4). Back to [[03-Areas/called-to-edit/called-to-edit|Called to Edit]].\n", encoding="utf-8")
    return note


def git(*args):
    return subprocess.run(["git", *args], cwd=str(BRAIN), capture_output=True, text=True, encoding="utf-8")


def commit_and_push(title, when):
    paths = ["05-Knowledge/teachings", "06-Logs/automation/meeting-recorder.md", "01-Inbox"]
    git("add", "--", *paths)
    if not git("diff", "--cached", "--quiet", "--", *paths).returncode:
        return "nothing to commit"
    msg = (f"Brand manager: call {when:%Y-%m-%d} ({title}) filed into the teachings archive\n\n"
           "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    r = git("commit", "-m", msg, "--", *paths)
    if r.returncode:
        return "commit failed: " + (r.stderr or r.stdout)[-200:]
    git("fetch", "origin")
    m = git("merge", "--no-edit", "origin/main")
    if m.returncode:
        git("merge", "--abort")
        return "committed, not pushed (merge with GitHub needs a person)"
    p = git("push", "origin", "HEAD:main")
    return "committed and pushed" if not p.returncode else "committed, push failed"


def redeploy_bot(when):
    if not GIT_BASH.exists():
        return "no Git Bash, bot not redeployed"
    r = subprocess.run([str(GIT_BASH), "-lc", f"cd '{SITE_DIR.as_posix()}' && sh deploy.sh --prod 'Editors Bot knowledge: call {when:%Y-%m-%d}'"],
                       capture_output=True, text=True, encoding="utf-8", timeout=1800, creationflags=0x08000000)
    (WORK / "last-deploy.log").write_text((r.stdout or "")[-4000:] + "\n--- stderr ---\n" + (r.stderr or "")[-4000:], encoding="utf-8")
    return "bot knowledge deployed" if not r.returncode else "deploy failed (see last-deploy.log)"


def run(path, title, when=None, length="", log=print):
    """All four steps. Returns (summary-or-None, transcript path, notes)."""
    path = Path(path)
    when = when or datetime.fromtimestamp(path.stat().st_mtime)
    t0 = time.time()
    transcript, n = transcribe(path)
    log(f"Transcribed {n} lines in {int(time.time() - t0)} s: {transcript}")
    summary = file_into_archive(transcript, title, when, length)
    log(f"Archive filing: {'done, ' + str(summary.get('filed')) + ' items' if summary else 'FAILED (see last-filter.log)'}")
    notes = []
    if not summary:
        summary = gemini_summary(transcript, title, when)
        inbox_note(transcript, title, when)
        notes.append("Claude filing failed: summary by Gemini, archive filing left in 01-Inbox for next session"
                     if summary else "Claude and Gemini both failed: no summary, filing left in 01-Inbox")
        if summary:
            summary["filed"] = 0
            summary["by"] = "gemini"
    notes.append(commit_and_push(title, when))
    if summary and summary.get("filed"):
        notes.append(redeploy_bot(when))
    log("; ".join(notes))
    return summary, transcript, notes


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a[:1] == ["transcribe"] and len(a) > 1:
        print(transcribe(a[1]))
    elif a[:1] == ["run"] and len(a) > 1:
        s, t, notes = run(a[1], a[2] if len(a) > 2 else "Community call")
        print(json.dumps(s, indent=2, ensure_ascii=False))
    else:
        sys.exit(__doc__)
