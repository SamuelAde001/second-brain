"""Records the Called to Edit Community's main calls on its own, saves them to Drive and posts them.

Runs quietly from Windows logon (scheduled task "Called to Edit meeting recorder"). Every 15 s it asks
Discord whether a main call is live: the weekly-live stage is open, or a scheduled event is active. When
one starts it opens OBS on the meeting preset (profile + scene collection "Called to Edit Meeting"),
records, and switches OBS back to whatever it was on before. When the call ends it copies the file into
Drive, waits until Drive has it, and has the bot post the link in #announcements and pin it.

The bot token is read from %USERPROFILE%\\.brain-secrets\\community.json and the OBS WebSocket password
from OBS's own config, by this script only. Neither is ever printed or written anywhere.

  python meeting_recorder.py setup-obs     create the meeting preset and turn on OBS WebSocket (OBS closed)
  python meeting_recorder.py status        what the recorder sees right now
  python meeting_recorder.py test 20       record 20 s on the meeting preset, check the file, restore OBS
  python meeting_recorder.py run           the watcher (the scheduled task runs this with pythonw)
  python meeting_recorder.py install       create the logon task and start it
  python meeting_recorder.py publish FILE "Title"   post a finished recording by hand
"""

import ctypes
import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import uuid
from datetime import datetime
from pathlib import Path

import requests

BRAIN = Path(__file__).resolve().parents[2]
SECRETS = Path(os.environ["USERPROFILE"]) / ".brain-secrets" / "community.json"
DISCORD_CFG = Path(r"C:\Users\repzy\Desktop\called-to-edit-site\discord-config.json")  # ids only
API = "https://discord.com/api/v10"

OBS_EXE = Path(r"C:\Program Files\obs-studio\bin\64bit\obs64.exe")
OBS_DIR = Path(os.environ["APPDATA"]) / "obs-studio"
WS_CONFIG = OBS_DIR / "plugin_config" / "obs-websocket" / "config.json"
PRESET = "Called to Edit Meeting"            # profile name and scene collection name
PRESET_DIR = "Called_to_Edit_Meeting"        # profile folder and collection file stem
BASE_PROFILE = "1080p_25_fps"                # copied, then changed

LOCAL_DIR = Path(r"C:\Users\repzy\Videos\Called to Edit Meetings")   # OBS writes here, never to Drive
DRIVE_PARENT = Path(r"G:\My Drive\Called to Edit")
DRIVE_DIR = DRIVE_PARENT / "Community Call Recordings"
DRIVEFS = Path(os.environ["LOCALAPPDATA"]) / "Google" / "DriveFS"

WORK = Path(os.environ["LOCALAPPDATA"]) / "cte-meeting-recorder"
STATE = WORK / "state.json"
LOG = WORK / "recorder.log"
BRAIN_LOG = BRAIN / "06-Logs" / "automation" / "meeting-recorder.md"

# Mic: the Windows default input, which is what Discord uses on "Default" (Main Mic on 2026-10-28).
POLL = 15            # seconds between Discord checks
SHARE_POLL = 5       # seconds between screen-share checks while recording
START_AFTER = 2      # live on this many checks in a row before recording
STOP_AFTER = 4       # not live on this many checks in a row before stopping (1 min)
MAX_HOURS = 4        # safety stop
MIN_POST_MIN = 10    # shorter recordings are kept but not posted
LOCK_PORT = 47655    # one watcher at a time


# ---------- small helpers ----------

def log(msg):
    WORK.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    if sys.stdout:
        try:
            print(line, flush=True)
        except Exception:
            pass


def brain_log(line):
    BRAIN_LOG.parent.mkdir(parents=True, exist_ok=True)
    if not BRAIN_LOG.exists():
        BRAIN_LOG.write_text(
            "---\ntype: log\narea: called-to-edit\nstatus: active\nupdated: 2026-10-28\nsource: manual\n"
            "tags: [automation, community, recordings]\n---\n\n# Meeting recorder log\n\n"
            "Append-only. One line per recorded call, written by `00-System/scripts/meeting_recorder.py`. "
            "Back to [[03-Areas/called-to-edit/called-to-edit|Called to Edit]].\n\n",
            encoding="utf-8")
    with BRAIN_LOG.open("a", encoding="utf-8") as f:
        f.write(f"- {datetime.now():%Y-%m-%d %H:%M} — {line}\n")


def load_state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(s):
    WORK.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=2), encoding="utf-8")


def keep_awake(on):
    ES_CONTINUOUS, ES_SYSTEM, ES_DISPLAY = 0x80000000, 0x1, 0x2
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ((ES_SYSTEM | ES_DISPLAY) if on else 0))


def duration_s(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def nice_len(sec):
    h, m = divmod(int(sec // 60), 60)
    return f"{h} h {m:02d} min" if h else f"{m} min"


# ---------- Discord ----------

def _token():
    s = json.loads(SECRETS.read_text(encoding="utf-8"))
    return s["discord_bot_token"].strip()


def dc(method, path, body=None, ok=(200, 201, 204)):
    """One Discord call. Returns (status, json-or-None). Never raises for HTTP errors."""
    for _ in range(4):
        r = requests.request(method, API + path, json=body, timeout=30,
                             headers={"Authorization": "Bot " + _token()})
        if r.status_code == 429:
            time.sleep(float(r.json().get("retry_after", 1)) + 0.2)
            continue
        return r.status_code, (r.json() if r.content else None)
    return 429, None


def cfg():
    return json.loads(DISCORD_CFG.read_text(encoding="utf-8"))


def call_live():
    """Returns (live, title, channel_id). Live = the weekly-live stage is open, or an event is active."""
    c = cfg()
    g, stage = c["guild"], c["channels"]["live"]
    st, events = dc("GET", f"/guilds/{g}/scheduled-events")
    if st == 200:
        for e in events or []:
            if e.get("status") == 2 and e.get("entity_type") in (1, 2):  # active, stage or voice
                return True, e["name"].strip(), e.get("channel_id")
    elif st >= 500 or st == 429:
        raise ConnectionError(f"Discord {st}")
    st, inst = dc("GET", f"/stage-instances/{stage}")
    if st == 200 and inst:
        return True, (inst.get("topic") or "Weekly Live").strip(), stage
    if st not in (200, 404):
        raise ConnectionError(f"Discord {st}")
    return False, None, None


def owner_id():
    st, gd = dc("GET", f"/guilds/{cfg()['guild']}")
    return gd["owner_id"] if st == 200 else None


_owner = None


def samuel_voice():
    """Samuel's voice state ({} when he's in no call): channel_id, self_stream (screen-sharing), ..."""
    global _owner
    _owner = _owner or owner_id()
    if not _owner:
        return None
    st, vs = dc("GET", f"/guilds/{cfg()['guild']}/voice-states/{_owner}")
    return vs if st == 200 and vs else ({} if st == 404 else None)


def samuel_in(channel_id):
    vs = samuel_voice()
    return None if vs is None else vs.get("channel_id") == channel_id


def dm_samuel(text):
    uid = owner_id()
    if not uid:
        log("DM failed: no owner id")
        return
    st, ch = dc("POST", "/users/@me/channels", {"recipient_id": uid})
    if st in (200, 201):
        st, _ = dc("POST", f"/channels/{ch['id']}/messages", {"content": text, "allowed_mentions": {"parse": []}})
    log(f"DM to Samuel ({st}): {text[:80]}")


def post_announcement(text):
    ch = cfg()["channels"]["announcements"]
    st, msg = dc("POST", f"/channels/{ch}/messages", {"content": text, "allowed_mentions": {"parse": []}})
    if st not in (200, 201):
        raise RuntimeError(f"announcement post failed: {st} {msg}")
    pst, _ = dc("PUT", f"/channels/{ch}/messages/pins/{msg['id']}")
    if pst not in (200, 204):
        pst, _ = dc("PUT", f"/channels/{ch}/pins/{msg['id']}")
    log(f"Posted in #announcements, pin {pst}")
    return msg["id"]


# ---------- OBS ----------

def ws_password():
    return json.loads(WS_CONFIG.read_text(encoding="utf-8")).get("server_password", "")


def obs_running():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq obs64.exe", "/NH"], capture_output=True, text=True)
    return "obs64.exe" in r.stdout


def obs_client(wait=0):
    import obsws_python as obs
    end = time.time() + wait
    while True:
        try:
            return obs.ReqClient(host="localhost", port=4455, password=ws_password(), timeout=10)
        except Exception:
            if time.time() > end:
                raise
            time.sleep(2)


def last_obs_preset():
    """The profile and collection OBS was last on, from user.ini (read before launching it ourselves)."""
    prof = coll = None
    for f in (OBS_DIR / "user.ini", OBS_DIR / "global.ini"):
        if f.exists():
            for line in f.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
                if line.startswith("Profile=") and not prof:
                    prof = line.split("=", 1)[1]
                if line.startswith("SceneCollection=") and not coll:
                    coll = line.split("=", 1)[1]
    return prof, coll


def obs_open_on_preset():
    """Make OBS run on the meeting preset. Returns (client, previous_profile, previous_collection)."""
    if obs_running():
        cl = obs_client(wait=10)
        if cl.get_record_status().output_active:
            raise RuntimeError("OBS is already recording something else")
        prev_p = cl.get_profile_list().current_profile_name
        prev_c = cl.get_scene_collection_list().current_scene_collection_name
    else:
        prev_p, prev_c = last_obs_preset()
        subprocess.Popen([str(OBS_EXE), "--profile", PRESET, "--collection", PRESET, "--minimize-to-tray",
                          "--disable-shutdown-check", "--disable-missing-files-check"], cwd=str(OBS_EXE.parent))
        cl = obs_client(wait=90)
        time.sleep(3)
    if cl.get_scene_collection_list().current_scene_collection_name != PRESET:
        cl.set_current_scene_collection(PRESET)
        time.sleep(3)
    if cl.get_profile_list().current_profile_name != PRESET:
        cl.set_current_profile(PRESET)
        time.sleep(2)
    return cl, prev_p, prev_c


def obs_restore(cl, prev_p, prev_c):
    try:
        if prev_c and prev_c != PRESET:
            cl.set_current_scene_collection(prev_c)
            time.sleep(2)
        if prev_p and prev_p != PRESET:
            cl.set_current_profile(prev_p)
        log(f"OBS back on {prev_p} / {prev_c}")
    except Exception as e:
        log(f"Could not restore OBS preset: {e}")


def obs_stop(cl):
    path = cl.stop_record().output_path
    time.sleep(3)
    return Path(path)


# ---------- Drive ----------

def drive_item(title, parent_title):
    """Cloud id of a Drive item by name under a folder name, from Drive for desktop's own metadata (read-only copy)."""
    for acct in DRIVEFS.iterdir():
        db = acct / "metadata_sqlite_db"
        if not db.exists():
            continue
        tmp = Path(tempfile.mkdtemp())
        for suffix in ("", "-wal", "-shm"):
            if (acct / ("metadata_sqlite_db" + suffix)).exists():
                shutil.copy(acct / ("metadata_sqlite_db" + suffix), tmp)
        con = sqlite3.connect(tmp / "metadata_sqlite_db")
        try:
            rows = con.execute(
                "select i.id from items i join stable_parents sp on sp.item_stable_id=i.stable_id "
                "join items p on p.stable_id=sp.parent_stable_id "
                "where i.local_title=? and p.local_title=? and i.trashed=0", (title, parent_title)).fetchall()
        finally:
            con.close()
            shutil.rmtree(tmp, ignore_errors=True)
        ids = [r[0] for r in rows if r[0] and not str(r[0]).startswith("local")]
        if ids:
            return ids[0]
    return None


def link_is_public(url):
    try:
        r = requests.get(url, timeout=30, allow_redirects=True)
        return r.status_code == 200 and "accounts.google.com" not in r.url
    except requests.RequestException:
        return False


def to_drive(local, title):
    DRIVE_DIR.mkdir(parents=True, exist_ok=True)
    name = f"{datetime.fromtimestamp(local.stat().st_mtime):%Y-%m-%d} {title}{local.suffix}"
    name = "".join(ch for ch in name if ch not in '<>:"/\\|?*')
    dest = DRIVE_DIR / name
    n = 2
    while dest.exists():
        dest = DRIVE_DIR / f"{Path(name).stem} ({n}){local.suffix}"
        n += 1
    shutil.copy2(local, dest)
    log(f"Copied to Drive folder: {dest.name}")
    return dest


def wait_for_link(dest, hours=8):
    end = time.time() + hours * 3600
    while time.time() < end:
        fid = drive_item(dest.name, DRIVE_DIR.name)
        if fid:
            url = f"https://drive.google.com/file/d/{fid}/view"
            if link_is_public(url):
                return url, True
            # uploaded but the folder isn't shared with "anyone with the link" yet
            return url, False
        time.sleep(60)
    return None, False


def folder_link():
    fid = drive_item(DRIVE_DIR.name, DRIVE_PARENT.name)
    return f"https://drive.google.com/drive/folders/{fid}" if fid else None


# ---------- after a call ----------

def publish(local, title, started=None):
    secs = duration_s(local)
    log(f"Recording {local.name}: {nice_len(secs)}")
    if secs < MIN_POST_MIN * 60:
        dm_samuel(f"📼 The recording of **{title}** is only {nice_len(secs)}, so I didn't post it. "
                  f"It's on the PC: `{local}`")
        brain_log(f"{title}: {nice_len(secs)}, too short, kept locally, not posted")
        return
    dest = to_drive(local, title)
    url, public = wait_for_link(dest)
    if not url:
        dm_samuel(f"📼 **{title}** is in the Drive folder but Drive hasn't finished uploading after 8 hours. "
                  f"Check Drive for desktop is signed in and running.")
        brain_log(f"{title}: {nice_len(secs)}, Drive upload not confirmed")
        return
    if not public:
        dm_samuel(f"📼 **{title}** is on Drive but the recordings folder isn't shared yet, so members can't open it. "
                  f"In Drive, share \"Community Call Recordings\" as Anyone with the link → Viewer, "
                  f"then I'll post it. File: {url}")
        brain_log(f"{title}: {nice_len(secs)}, on Drive, waiting for folder sharing")
        # keep checking for a day, then give up
        end = time.time() + 24 * 3600
        while time.time() < end and not link_is_public(url):
            time.sleep(300)
        if not link_is_public(url):
            return
    when = started or datetime.fromtimestamp(local.stat().st_mtime)
    archive = folder_link()
    text = (f"📼 **{title}** — the recording is up\n"
            f"{when:%A %d %B %Y} · {nice_len(secs)}\n\n"
            f"Watch it here: {url}")
    if archive:
        text += f"\n\nEvery call we've recorded is in one place: {archive}"
    post_announcement(text)
    brain_log(f"{title}: {nice_len(secs)}, posted in #announcements ({dest.name})")


# ---------- the watcher ----------

def run():
    try:
        lock = socket.socket()
        lock.bind(("127.0.0.1", LOCK_PORT))
    except OSError:
        log("Another watcher is already running; exiting.")
        return
    log("Watcher started.")
    s = load_state()
    if s.get("recording"):
        log("Found a recording left open from before a restart; will stop it if the call is over.")
    live_n = idle_n = tick = 0
    warned_absent = False
    shown = None  # the OBS scene we last put up
    while True:
        time.sleep(SHARE_POLL)
        tick += 1
        s = load_state()
        if s.get("recording"):
            # follow his screen share: whole monitor while he shares, the Discord window otherwise
            try:
                vs = samuel_voice()
                if vs is not None:
                    want = "Screen" if vs.get("self_stream") else "Meeting"
                    if want != shown:
                        obs_client(wait=5).set_current_program_scene(want)
                        log(f"Scene: {want}")
                        shown = want
            except Exception as e:
                log(f"Scene follow error: {e}")
        else:
            shown = None
        if tick % (POLL // SHARE_POLL):
            continue
        try:
            live, title, chan = call_live()
            s = load_state()
            if live and not s.get("recording"):
                live_n += 1
                if live_n >= START_AFTER:
                    start_recording(title, chan)
                    warned_absent = False
            elif live and s.get("recording"):
                idle_n = 0
                elapsed = time.time() - s["started_ts"]
                if not warned_absent and elapsed > 120 and samuel_in(s.get("channel")) is False:
                    dm_samuel("🎙️ I'm recording the call, but you're not in it on the PC, so the recording "
                              "may be empty. Join the stage from Discord on the PC.")
                    warned_absent = True
                if elapsed > MAX_HOURS * 3600:
                    dm_samuel(f"⏹️ The call has run {MAX_HOURS} hours, so I stopped the recording.")
                    stop_recording()
            elif not live:
                live_n = 0
                if s.get("recording"):
                    idle_n += 1
                    if idle_n >= STOP_AFTER:
                        stop_recording()
                        idle_n = 0
        except Exception as e:
            log(f"Watcher error: {e}\n{traceback.format_exc()}")


def start_recording(title, chan):
    log(f"Call live: {title}. Starting recording.")
    try:
        cl, prev_p, prev_c = obs_open_on_preset()
        cl.start_record()
        time.sleep(3)
        if not cl.get_record_status().output_active:
            raise RuntimeError("OBS did not start recording")
    except Exception as e:
        log(f"Could not start recording: {e}")
        dm_samuel(f"⚠️ **{title}** is live but I couldn't start the recording ({e}). "
                  "Open OBS, pick the \"Called to Edit Meeting\" profile and scene collection, and press Start Recording.")
        save_state({"recording": False, "failed_title": title})
        time.sleep(300)  # don't retry every 15 s
        return
    keep_awake(True)
    save_state({"recording": True, "title": title, "channel": chan, "started_ts": time.time(),
                "started": datetime.now().isoformat(timespec="seconds"), "prev_profile": prev_p, "prev_collection": prev_c})
    log("Recording.")


def stop_recording():
    s = load_state()
    title = s.get("title", "Community call")
    try:
        cl = obs_client(wait=10)
        path = obs_stop(cl) if cl.get_record_status().output_active else None
        obs_restore(cl, s.get("prev_profile"), s.get("prev_collection"))
    except Exception as e:
        log(f"Could not stop through OBS: {e}")
        path = None
    keep_awake(False)
    save_state({"recording": False, "last_title": title})
    if not path:
        files = sorted(LOCAL_DIR.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
        path = files[-1] if files else None
    if not path or not path.exists():
        dm_samuel(f"⚠️ The call **{title}** ended but I couldn't find its recording. Check OBS.")
        return
    started = datetime.fromisoformat(s["started"]) if s.get("started") else None
    log(f"Stopped. File: {path}")
    threading.Thread(target=_publish_safe, args=(path, title, started), daemon=True).start()


def _publish_safe(path, title, started):
    try:
        publish(path, title, started)
    except Exception as e:
        log(f"Publish failed: {e}\n{traceback.format_exc()}")
        dm_samuel(f"⚠️ I recorded **{title}** but couldn't post it ({e}). The file is at `{path}`.")


# ---------- setup ----------

def setup_obs():
    if obs_running():
        cl = obs_client(wait=5)
        if PRESET in (cl.get_profile_list().current_profile_name,
                      cl.get_scene_collection_list().current_scene_collection_name):
            sys.exit("OBS is on the meeting preset; switch it to another one (or close OBS) first.")
        # OBS reads a profile and collection from disk when it switches to them, so rewriting is safe now
    # profile: copy his 1080p profile, then change what a meeting needs
    src, dst = OBS_DIR / "basic" / "profiles" / BASE_PROFILE, OBS_DIR / "basic" / "profiles" / PRESET_DIR
    if not dst.exists():
        shutil.copytree(src, dst)
    ini = (dst / "basic.ini").read_text(encoding="utf-8-sig").splitlines()
    rec = str(LOCAL_DIR).replace("\\", "\\\\")
    sets = {("General", "Name"): PRESET,
            ("Output", "FilenameFormatting"): "Meeting %CCYY-%MM-%DD %hh-%mm",
            ("AdvOut", "RecFilePath"): rec, ("AdvOut", "RecFormat2"): "hybrid_mp4",
            ("AdvOut", "RecEncoder"): "obs_nvenc_h264_tex", ("AdvOut", "RecTracks"): "3",
            ("AdvOut", "RecType"): "Standard", ("AdvOut", "RecUseRescale"): "false",
            ("AdvOut", "RecSplitFile"): "false",
            ("SimpleOutput", "FilePath"): rec,
            ("Video", "BaseCX"): "1920", ("Video", "BaseCY"): "1080",
            ("Video", "OutputCX"): "1920", ("Video", "OutputCY"): "1080",
            ("Video", "FPSType"): "0", ("Video", "FPSCommon"): "30"}
    out, sec, seen = [], None, set()
    for line in ini:
        if line.startswith("["):
            for (s_, k), v in sets.items():  # keys missing from the previous section
                if s_ == sec and (s_, k) not in seen:
                    out.append(f"{k}={v}")
                    seen.add((s_, k))
            sec = line.strip("[]")
        elif "=" in line and (sec, line.split("=", 1)[0]) in sets:
            k = line.split("=", 1)[0]
            line = f"{k}={sets[(sec, k)]}"
            seen.add((sec, k))
        out.append(line)
    for (s_, k), v in sets.items():
        if s_ == sec and (s_, k) not in seen:
            out.append(f"{k}={v}")
    (dst / "basic.ini").write_text("\n".join(out) + "\n", encoding="utf-8")
    # NVENC H.264, constant quality: plays everywhere, about 1-2 GB an hour for a call
    (dst / "recordEncoder.json").write_text(json.dumps(
        {"rate_control": "CQP", "cqp": 23, "preset2": "p5", "tune": "hq", "multipass": "qres",
         "profile": "high", "keyint_sec": 2, "bf": 2}), encoding="utf-8")
    (dst / "streamEncoder.json").unlink(missing_ok=True)
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)

    # scene collection: "Meeting" (the Discord window) and "Screen" (his whole monitor, used while he
    # screen-shares), both with the same sound: track 1 = everything he hears + his mic, track 2 = Discord + mic
    def src_(name, sid, settings, mixers, volume=1.0):
        return {"prev_ver": 536870914, "name": name, "uuid": str(uuid.uuid4()), "id": sid, "versioned_id": sid,
                "settings": settings, "mixers": mixers, "sync": 0, "flags": 0, "volume": volume, "balance": 0.5,
                "enabled": True, "muted": False, "push-to-mute": False, "push-to-mute-delay": 0,
                "push-to-talk": False, "push-to-talk-delay": 0, "hotkeys": {}, "deinterlace_mode": 0,
                "deinterlace_field_order": 0, "monitoring_type": 0, "private_settings": {}}
    win = "Discord:Chrome_WidgetWin_1:Discord.exe"
    monitor = next(s["settings"]["monitor_id"] for s in json.loads(
        (OBS_DIR / "basic" / "scenes" / "Course_rec.json").read_text(encoding="utf-8"))["sources"]
        if s["id"] == "monitor_capture")  # his one monitor, as his Course rec preset captures it
    discord_win = src_("Discord window", "window_capture", {"window": win, "priority": 2, "method": 2,
                                                            "cursor": False, "client_area": True}, 255)
    screen = src_("Full screen", "monitor_capture", {"monitor_id": monitor, "method": 0, "capture_cursor": True}, 255)
    sound = [
        src_("Desktop sound", "wasapi_output_capture", {"device_id": "default"}, 1),            # track 1
        src_("Samuel mic", "wasapi_input_capture", {"device_id": "default"}, 3),  # Windows default mic, as Discord uses; tracks 1+2
        src_("Discord sound", "wasapi_process_output_capture", {"window": win, "priority": 2}, 2),  # track 2
    ]

    def items_(sources):
        out_ = []
        for i, s in enumerate(sources, 1):
            out_.append({"name": s["name"], "source_uuid": s["uuid"], "visible": True, "locked": i == 1, "rot": 0.0,
                         "align": 5, "bounds_type": 2 if i == 1 else 0, "bounds_align": 0, "bounds_crop": False,
                         "crop_left": 0, "crop_top": 0, "crop_right": 0, "crop_bottom": 0, "id": i,
                         "group_item_backup": False, "pos": {"x": 0.0, "y": 0.0}, "scale": {"x": 1.0, "y": 1.0},
                         "bounds": {"x": 1920.0, "y": 1080.0}, "scale_filter": "disable", "blend_method": "default",
                         "blend_type": "normal", "show_transition": {"duration": 0},
                         "hide_transition": {"duration": 0}, "private_settings": {}})
        return {"items": out_, "id_counter": len(out_), "custom_size": False}
    scenes = [src_("Meeting", "scene", items_([discord_win] + sound), 0),
              src_("Screen", "scene", items_([screen] + sound), 0)]
    coll = {"current_scene": "Meeting", "current_program_scene": "Meeting",
            "scene_order": [{"name": "Meeting"}, {"name": "Screen"}],
            "name": PRESET, "groups": [], "quick_transitions": [], "transitions": [], "saved_projectors": [],
            "current_transition": "Cut", "transition_duration": 300, "preview_locked": False,
            "scaling_enabled": False, "scaling_level": 0, "scaling_off_x": 0.0, "scaling_off_y": 0.0,
            "modules": {}, "sources": scenes + [discord_win, screen] + sound}
    (OBS_DIR / "basic" / "scenes" / f"{PRESET_DIR}.json").write_text(json.dumps(coll, indent=4), encoding="utf-8")

    # OBS WebSocket on, local password kept as OBS set it
    ws = json.loads(WS_CONFIG.read_text(encoding="utf-8"))
    ws["server_enabled"] = True
    ws["auth_required"] = True
    ws["alerts_enabled"] = False
    WS_CONFIG.write_text(json.dumps(ws, indent=4), encoding="utf-8")
    DRIVE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Meeting preset written: profile + scene collection '{PRESET}'. WebSocket on.")
    print(f"Recordings: {LOCAL_DIR} (local) -> {DRIVE_DIR}")


def status():
    live, title, chan = call_live()
    print("Call live:", live, title or "")
    print("Recorder state:", load_state())
    print("OBS running:", obs_running())
    if obs_running():
        cl = obs_client(wait=5)
        print("OBS on:", cl.get_profile_list().current_profile_name, "/",
              cl.get_scene_collection_list().current_scene_collection_name,
              "| recording:", cl.get_record_status().output_active)
    print("Drive folder:", DRIVE_DIR.exists(), folder_link())


def test(seconds):
    cl, prev_p, prev_c = obs_open_on_preset()
    cl.start_record()
    time.sleep(seconds)
    path = obs_stop(cl)
    obs_restore(cl, prev_p, prev_c)
    print("File:", path, f"{path.stat().st_size / 1e6:.1f} MB", nice_len(duration_s(path)), f"({duration_s(path):.0f} s)")
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=index,codec_type,codec_name,width,height,r_frame_rate",
                        "-of", "compact", str(path)], capture_output=True, text=True)
    print(r.stdout)
    for idx in (0, 1):
        r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(path), "-map", f"0:a:{idx}", "-af", "volumedetect",
                            "-f", "null", "-"], capture_output=True, text=True)
        levels = [l.split("]")[-1].strip() for l in r.stderr.splitlines() if "max_volume" in l or "mean_volume" in l]
        print(f"audio track {idx + 1}:", levels)


def install():
    pyw = Path(sys.executable).with_name("pythonw.exe")
    # A Startup-folder shortcut: runs at his logon with no admin rights (a logon task needs admin).
    lnk = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / \
        "Called to Edit meeting recorder.lnk"
    ps = (f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{lnk}');$s.TargetPath='{pyw}';"
          f"$s.Arguments='\"{Path(__file__).resolve()}\" run';$s.WorkingDirectory='{Path(__file__).parent}';"
          f"$s.WindowStyle=7;$s.Save()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    subprocess.Popen([str(pyw), str(Path(__file__).resolve()), "run"], cwd=str(Path(__file__).parent),
                     creationflags=0x00000008 | 0x00000200)  # detached, own process group
    print(f"Installed ({lnk.name} in Startup) and started.")


if __name__ == "__main__":
    a = sys.argv[1:] or ["status"]
    if a[0] == "setup-obs":
        setup_obs()
    elif a[0] == "status":
        status()
    elif a[0] == "test":
        test(int(a[1]) if len(a) > 1 else 20)
    elif a[0] == "run":
        run()
    elif a[0] == "install":
        install()
    elif a[0] == "publish":
        publish(Path(a[1]), a[2] if len(a) > 2 else "Community call")
    else:
        sys.exit(__doc__)
