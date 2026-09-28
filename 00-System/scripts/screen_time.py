"""Screen time from StayFree, for the PA's night plan.

StayFree's Windows app keeps two local SQLite files:
  usage.db   -> this PC's app sessions (start/end, ms since epoch, UTC)
  config.db  -> a cache of sessions synced from his other devices: the phone
               (platform "android") and the Chrome extension (platform "web").
               It only holds the dates the app last pulled from StayFree's cloud.

Both are copied to a temp folder and read there. The originals are never opened
for writing (AGENTS.md rule 5). Only session rows are read, nothing else in config.

Usage:
  python screen_time.py                  print today's report
  python screen_time.py --date 2026-09-27
  python screen_time.py --write          write 06-Logs/screen-time/<date>.md (and yesterday's, now complete)
  python screen_time.py --write --push   ...then commit and push those files only
  python screen_time.py --refresh ...    if phone data is stale, open StayFree, wait, read again

Rules it applies (07-Agents/personal-life/standing-rules.md):
  social media only while eating -> meal windows below; YouTube counts as social media.
"""
import argparse, datetime as dt, json, os, shutil, sqlite3, subprocess, sys, tempfile, time
from pathlib import Path

BRAIN = Path(__file__).resolve().parents[2]
OUT_DIR = BRAIN / "06-Logs" / "screen-time"
RUN_LOG = BRAIN / "06-Logs" / "automation" / "screen-time-runs.md"
PKG = "37081StayFreeApps.StayFree3_fqhk48m1tsma0"
SRC = Path(os.environ["LOCALAPPDATA"]) / "Packages" / PKG / "LocalCache" / "Roaming" / "StayFree"
APP_ID = PKG + "!stayfree"
WAT = dt.timezone(dt.timedelta(hours=1))

# Allowed social media: while eating. From 02-Me/daily-routine.md (1:00pm meal, 2:00pm nap; ~6:30pm dinner).
MEALS = [((13, 0), (14, 0)), ((18, 30), (19, 30))]
BED, WAKE = 23, 6          # phone away by 11:00pm, wake 6:00am
MORNING = (6, 7)           # the hour before work starts (P4: the day is lost in the morning)
STALE_MIN = 120            # phone data older than this at run time = stale

SOCIAL = {  # label -> test on one appId part (lower case)
    "YouTube":   lambda p: "youtube" in p or p == "youtu.be",
    "Instagram": lambda p: "instagram" in p or p == "threads.net",
    "TikTok":    lambda p: "tiktok" in p or "musically" in p or p.startswith("com.ss.android.ugc"),
    "X":         lambda p: p in ("x.com", "twitter.com") or "twitter" in p,
    "Facebook":  lambda p: "facebook" in p or p in ("fb.com", "m.facebook.com"),
    "Snapchat":  lambda p: "snapchat" in p,
    "Reddit":    lambda p: "reddit" in p,
    "LinkedIn":  lambda p: "linkedin" in p,
}
MESSAGING = {"WhatsApp": lambda p: "whatsapp" in p, "Telegram": lambda p: "telegram" in p}
SKIP = lambda p: "launcher" in p  # the phone's home screen is not an app


def label(app_id, table):
    parts = [p.strip().lower() for p in str(app_id).split(",")]
    for name, test in table.items():
        if any(test(p) for p in parts):
            return name
    return None


def copy_dbs():
    tmp = Path(tempfile.mkdtemp(prefix="stayfree-"))
    for f in ("usage.db", "usage.db-wal", "config.db", "config.db-wal"):
        if (SRC / f).exists():
            shutil.copy2(SRC / f, tmp / f)
    return tmp


def load_sessions():
    """[(platform, appId, start_ms, end_ms)] from the PC db and the sync cache."""
    tmp = copy_dbs()
    out, seen = [], set()
    try:
        c = sqlite3.connect(tmp / "usage.db")
        for sid, app, s, e in c.execute("select id, appId, startedAt, endedAt from sessions where endedAt is not null"):
            seen.add(sid); out.append(("windows", app, s, e))
        c.close()

        def walk(o):
            if isinstance(o, dict):
                if "startedAt" in o and "appId" in o:
                    sid, plat = o.get("id"), o.get("platform")
                    if plat != "windows" and o.get("endedAt") and sid not in seen:
                        seen.add(sid); out.append((plat or "?", o["appId"], o["startedAt"], o["endedAt"]))
                    return
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)

        c = sqlite3.connect(tmp / "config.db")
        for (v,) in c.execute("select value from config where key like '%sessions%'"):
            try: walk(json.loads(v))
            except (TypeError, ValueError): pass
        c.close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out


def ms(t): return int(t.timestamp() * 1000)


def union(iv):
    """Merge overlapping [s, e) intervals; returns merged list."""
    res = []
    for s, e in sorted(iv):
        if res and s <= res[-1][1]: res[-1][1] = max(res[-1][1], e)
        else: res.append([s, e])
    return res


def overlap(iv, lo, hi):
    return sum(max(0, min(e, hi) - max(s, lo)) for s, e in iv) / 60000


def at(day, h, m=0): return dt.datetime.combine(day, dt.time(h, m), WAT)


def report(sessions, day, now):
    d0, d1 = at(day, 0), at(day + dt.timedelta(days=1), 0)
    end = min(d1, now)
    lo, hi = ms(d0), ms(end)
    night = (ms(at(day - dt.timedelta(days=1), BED)), ms(at(day, WAKE)))
    meals = [(ms(at(day, *a)), ms(at(day, *b))) for a, b in MEALS]

    by_label, plat_iv, msg_iv, other = {}, {}, {}, {}
    for plat, app, s, e in sessions:
        if e <= night[0] or s >= hi: continue
        parts = str(app).lower()
        if SKIP(parts): continue
        lab = label(app, SOCIAL)
        if lab: by_label.setdefault(lab, []).append((s, e))
        m = label(app, MESSAGING)
        if m: msg_iv.setdefault(m, []).append((s, e))
        plat_iv.setdefault(plat, []).append((s, e))
        if not lab and not m and plat == "android":
            other.setdefault(app, []).append((s, e))

    def split(iv):
        iv = union(iv)
        total = overlap(iv, lo, hi)
        in_meals = sum(overlap(iv, a, b) for a, b in meals)
        return iv, total, total - in_meals

    rows, all_social = [], []
    for lab, iv in by_label.items():
        iv, total, outside = split(iv)
        all_social += iv
        if total >= 1 or overlap(iv, *night) >= 1:
            rows.append((lab, total, outside, overlap(iv, *night), overlap(iv, ms(at(day, MORNING[0])), ms(at(day, MORNING[1])))))
    rows.sort(key=lambda r: -r[1])
    s_iv, s_total, s_out = split(all_social)
    s_night = overlap(s_iv, *night)
    s_morning = overlap(s_iv, ms(at(day, MORNING[0])), ms(at(day, MORNING[1])))
    yt = next((r for r in rows if r[0] == "YouTube"), None)

    latest = {}
    for plat, _, s, e in sessions:
        latest[plat] = max(latest.get(plat, 0), e)
    phone_last = latest.get("android", 0)
    phone_stale = day == now.date() and (ms(now) - phone_last) / 60000 > STALE_MIN
    has_phone = any(p == "android" for p in plat_iv) and overlap(union(plat_iv.get("android", [])), lo, hi) > 0

    f = lambda m: f"{int(m // 60)}h {int(round(m % 60)):02d}m" if m >= 60 else f"{int(round(m))}m"
    hhmm = lambda x: dt.datetime.fromtimestamp(x / 1000, WAT).strftime("%Y-%m-%d %H:%M") if x else "none"
    upto = "the whole day" if end == d1 else f"00:00–{end.strftime('%H:%M')} (the day wasn't over)"

    L = ["---", "type: log", "area: me", "status: active", f"updated: {now.date()}", "source: local-folder",
         "tags: [screen-time, social-media, stayfree]", "---", "",
         f"# Screen time — {day}", "",
         f"Made by `00-System/scripts/screen_time.py` from StayFree's data on the PC. Covers {upto}.",
         f"Last data seen — phone: {hhmm(phone_last)} · Chrome: {hhmm(latest.get('web', 0))} · PC: {hhmm(latest.get('windows', 0))}.", ""]
    if not has_phone:
        L += ["**No phone data for this day in StayFree's cache.** The phone numbers below are missing, not zero. Ask him for a StayFree screenshot.", ""]
    elif phone_stale:
        L += [f"**Phone data is stale:** nothing newer than {hhmm(phone_last)}. Treat phone numbers as incomplete.", ""]

    meal_txt = " and ".join(f"{a[0]}:{a[1]:02d}–{b[0]}:{b[1]:02d}" for a, b in MEALS)
    L += ["## Social media (his rule: only while eating)", "",
          f"- **Outside meal times: {f(s_out)}** (meal windows {meal_txt})",
          f"- Total today: {f(s_total)}",
          f"- Last night, 11:00pm–6:00am: {f(s_night)}",
          f"- 6:00–7:00am, before work: {f(s_morning)}", ""]
    if rows:
        L += ["| App | Today | Outside meals | Last night | 6–7am |", "|---|---|---|---|---|"]
        L += [f"| {r[0]} | {f(r[1])} | {f(r[2])} | {f(r[3])} | {f(r[4])} |" for r in rows]
        L += [""]
    if yt and yt[2] >= 1:
        L += [f"YouTube counts as social media, but he sometimes uses it for work (Samuel, 2026-09-28). Ask how much of the {f(yt[2])} outside meals was work; his word stands.", ""]

    hours = []
    for h in range(24):
        a, b = ms(at(day, h)), ms(at(day, h) + dt.timedelta(hours=1))
        if b > hi: break
        m = overlap(s_iv, a, b)
        if m >= 1: hours.append(f"{h:02d}:00 {int(round(m))}m")
    if hours:
        L += ["**Social media by hour:** " + " · ".join(hours), ""]

    L += ["## Devices", ""]
    names = {"android": "Phone", "web": "Chrome (sites)", "windows": "PC (apps, Chrome included)"}
    for plat in ("android", "web", "windows"):
        if plat in plat_iv:
            L.append(f"- {names[plat]}: {f(overlap(union(plat_iv[plat]), lo, hi))}")
    for m, iv in msg_iv.items():
        t = overlap(union(iv), lo, hi)
        if t >= 1: L.append(f"- {m} (messaging, not counted as social media): {f(t)}")
    top = sorted(((overlap(union(iv), lo, hi), a) for a, iv in other.items()), reverse=True)[:5]
    top = [f"{a.split(',')[0]} {f(t)}" for t, a in top if t >= 5]
    if top: L.append("- Other phone apps: " + " · ".join(top))
    L += ["", "Back to [[02-Me/daily-routine|daily routine]]", ""]
    return "\n".join(L), phone_stale or not has_phone, s_out


def refresh():
    subprocess.run(["explorer.exe", f"shell:AppsFolder\\{APP_ID}"], check=False)
    time.sleep(90)


def git(*a):
    return subprocess.run(["git", "-C", str(BRAIN), *a], capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date"); ap.add_argument("--write", action="store_true")
    ap.add_argument("--push", action="store_true"); ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    now = dt.datetime.now(WAT)
    day = dt.date.fromisoformat(a.date) if a.date else now.date()

    sessions = load_sessions()
    text, stale, _ = report(sessions, day, now)
    refreshed = False
    if stale and a.refresh and day == now.date():
        refresh(); refreshed = True
        now = dt.datetime.now(WAT)
        sessions = load_sessions()
        text, stale, _ = report(sessions, day, now)

    if not a.write:
        sys.stdout.reconfigure(encoding="utf-8"); print(text); return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for d in (day - dt.timedelta(days=1), day):
        t = text if d == day else report(sessions, d, now)[0]
        p = OUT_DIR / f"{d}.md"
        p.write_text(t, encoding="utf-8", newline="\n"); written.append(p)

    line = f"- {now:%Y-%m-%d %H:%M} — wrote {', '.join(p.name for p in written)}; phone data {'STALE/MISSING' if stale else 'fresh'}{'; refresh tried' if refreshed else ''}"
    if not RUN_LOG.exists():
        RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
        RUN_LOG.write_text("---\ntype: log\narea: me\nstatus: active\nupdated: 2026-09-28\nsource: manual\ntags: [automation, screen-time]\n---\n\n"
                           "# Screen time — run log\n\nOne line per run of `00-System/scripts/screen_time.py`. Append-only.\n\n"
                           "Back to [[02-Me/daily-routine|daily routine]]\n\n", encoding="utf-8", newline="\n")

    if a.push:
        paths = [str(p.relative_to(BRAIN)) for p in written] + [str(RUN_LOG.relative_to(BRAIN))]
        with RUN_LOG.open("a", encoding="utf-8", newline="\n") as fh: fh.write(line + "\n")
        git("add", "--", *paths)
        c = git("commit", "-m", f"[automation] screen-time: {day}", "--", *paths)
        pull = git("pull", "--no-rebase", "--no-edit", "origin", "main")
        if pull.returncode != 0:
            git("merge", "--abort")
            print("pull failed:", pull.stderr.strip()); sys.exit(1)
        push = git("push", "origin", "main")
        print(c.stdout.strip().splitlines()[0] if c.stdout else "nothing to commit", "|", "pushed" if push.returncode == 0 else push.stderr.strip())
    else:
        with RUN_LOG.open("a", encoding="utf-8", newline="\n") as fh: fh.write(line + "\n")
        print(line)


if __name__ == "__main__":
    main()
