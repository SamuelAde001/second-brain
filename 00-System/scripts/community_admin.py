"""Called to Edit Community: run the Discord server and the site's member store from the PC.

The bot token and keys sit in %USERPROFILE%\\.brain-secrets\\community.json (Samuel fills it).
This script reads them and never prints them. No agent opens that file (AGENTS.md §6, §10).

  python community_admin.py invite-url      link that adds the bot to the server
  python community_admin.py build           roles, channels, permissions, AutoMod, Community mode (safe to re-run)
  python community_admin.py post-texts      post or update the pinned texts from the Brain note, upload the workbook
  python community_admin.py push-env        put the keys and the server config on the Netlify site
  python community_admin.py nuggets         rebuild the bot's morning-nugget list from the Brain note
  python community_admin.py status          what the server looks like now
  python community_admin.py members         who has paid, until when (no emails or phones printed)
  python community_admin.py team-invite     a one-use, 24-hour invite for a team member
  python community_admin.py team <name>     give someone already in the server a free Team seat
  python community_admin.py say <channel> <text>
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

BRAIN = Path(__file__).resolve().parents[2]
SECRETS = Path(os.environ["USERPROFILE"]) / ".brain-secrets" / "community.json"
SITE_DIR = Path(r"C:\Users\repzy\Desktop\called-to-edit-site")
CONFIG = SITE_DIR / "discord-config.json"  # ids only, nothing secret
TEXTS = BRAIN / "04-Projects" / "called-to-edit-community-discord-texts.md"
WORKBOOK = BRAIN / "_attachments" / "called-to-edit-workbook" / "Called-to-Edit-Workbook-Your-First-60-Days.pdf"
ICON = BRAIN / "_attachments" / "called-to-edit-brand" / "png" / "called-to-edit-avatar-community.png"
SITE_ID = "20664735-e47b-402f-9450-6fab7ce27ebc"
SITE_URL = os.environ.get("CTE_SITE_URL", "https://calledtoeditcommunity.netlify.app")
SERVER_NAME = "Called to Edit"
API = "https://discord.com/api/v10"

# Permission bits
VIEW, SEND, HISTORY, REACT = 1 << 10, 1 << 11, 1 << 16, 1 << 6
MEMBER_PERMS = (VIEW | SEND | HISTORY | REACT | (1 << 38) | (1 << 35) | (1 << 14) | (1 << 15) | (1 << 18)
                | (1 << 20) | (1 << 21) | (1 << 25) | (1 << 32) | (1 << 26) | (1 << 31) | (1 << 9))
TEAM_PERMS = MEMBER_PERMS | (1 << 13) | (1 << 34) | (1 << 17)  # + manage messages, manage threads, mention everyone
NO_POST = SEND | (1 << 38) | (1 << 35)  # send, send in threads, create threads

TEXT, VOICE, CATEGORY, STAGE, FORUM = 0, 2, 4, 13, 15
# (category, [(name, type, mode, topic)]). mode: ro = read-only for members, rw, team, expired
LAYOUT = [
    ("START HERE", [
        ("welcome", TEXT, "ro", "Join messages and welcomes land here, so the chat stays clear."),
        ("rules", TEXT, "ro", "The rules. One minute."),
        ("announcements", TEXT, "ro", "News from Samuel."),
        ("start-here", TEXT, "ro", "How the community works and how to post your check-in."),
        ("workbook", TEXT, "ro", "Your First 60 Days: the workbook."),
        ("daily-nugget", TEXT, "ro", "A nugget from Samuel's teaching, every morning at 7."),
    ]),
    ("COMMUNITY", [
        ("introduce-yourself", TEXT, "rw", "Your name, where you edit from, what you edit on, who you want to edit for."),
        ("general", TEXT, "rw", "Talk with the community."),
        ("wins", TEXT, "rw", "First client, first reply, first finished video. Share it."),
    ]),
    ("THE 60 DAYS", [
        ("daily-check-in", FORUM, "rw", None),
        ("leaderboard", TEXT, "ro", "Streaks and days done, every Sunday at 6pm."),
    ]),
    ("FEEDBACK", [
        ("portfolio-and-profile", TEXT, "rw", "Share your portfolio, bio or profile. Say what you want feedback on."),
        ("outreach", TEXT, "rw", "Your DMs, emails and Looms before you send them."),
        ("niche", TEXT, "rw", "Your one-sentence niche and who you edit for."),
    ]),
    ("HELP", [
        ("questions", TEXT, "rw", "Ask anything about the 60 days or the work."),
        ("davinci-help", TEXT, "rw", "DaVinci Resolve questions. CapCut and phone editing too."),
        ("gear", TEXT, "rw", "Laptops, phones, mics, cameras."),
    ]),
    ("LIVE", [
        ("weekly-call", STAGE, "rw", None),
        ("call-recordings", TEXT, "ro", "Recordings of the live calls."),
    ]),
    ("OFF-TOPIC", [
        ("off-topic", TEXT, "rw", "Anything else. Keep it kind."),
    ]),
    ("TEAM", [
        ("payments-log", TEXT, "team", "Payments, joins, renewals and expiries, posted by the bot."),
        ("mod-log", TEXT, "team", "What AutoMod blocked."),
    ]),
    ("SUBSCRIPTION", [
        ("subscription-expired", TEXT, "expired", "Renew to get back in."),
    ]),
]
CONFIG_KEYS = {  # channel name -> key the site's functions use
    "welcome": "welcome", "rules": "rules", "start-here": "startHere", "workbook": "workbook",
    "introduce-yourself": "introduce", "general": "general", "daily-check-in": "checkin",
    "daily-nugget": "nugget", "leaderboard": "leaderboard", "payments-log": "payments",
    "mod-log": "modLog", "subscription-expired": "expired", "announcements": "announcements",
}
SCAM_WORDS = ["*free nitro*", "*discord.gift*", "*nitro for free*", "*steamcommunity*", "*crypto signal*",
              "*forex signal*", "*investment opportunity*", "*invest with me*", "*double your money*",
              "*binary option*", "*airdrop*", "*send me your pin*", "*send your otp*", "*bit.ly*", "*t.me/*"]


def secrets():
    if not SECRETS.exists():
        sys.exit(f"Missing {SECRETS}. Samuel fills it (see the community launch note).")
    s = json.loads(SECRETS.read_text(encoding="utf-8"))
    missing = [k for k in ("discord_bot_token", "discord_client_id", "discord_client_secret") if not str(s.get(k, "")).strip() or " " in str(s.get(k))]
    if missing:
        sys.exit("Not filled in yet: " + ", ".join(missing))
    return s


def api(method, path, body=None, files=None, ok_missing=False):
    tok = secrets()["discord_bot_token"].strip()
    for _ in range(5):
        kw = {"headers": {"Authorization": "Bot " + tok}}
        if files:
            kw["files"] = files
            kw["data"] = {"payload_json": json.dumps(body or {})}
        elif body is not None:
            kw["json"] = body
        r = requests.request(method, API + path, timeout=60, **kw)
        if r.status_code == 429:
            time.sleep(float(r.json().get("retry_after", 1)) + 0.2)
            continue
        if r.status_code == 404 and ok_missing:
            return None
        if r.status_code >= 400:
            sys.exit(f"Discord said {r.status_code} on {method} {path}: {r.text[:300]}")
        return r.json() if r.content else None
    sys.exit("Discord kept rate-limiting; try again in a minute.")


def load_cfg():
    return json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}


def save_cfg(c):
    CONFIG.write_text(json.dumps(c, indent=2), encoding="utf-8")


def find_guild():
    guilds = api("GET", "/users/@me/guilds")
    named = [g for g in guilds if g["name"].strip().lower() == SERVER_NAME.lower()]
    pick = named or guilds
    if len(pick) != 1:
        sys.exit(f"The bot is in {len(guilds)} servers; add it to the '{SERVER_NAME}' server (invite-url).")
    return pick[0]["id"]


def cmd_setup_secrets():
    """Samuel pastes each key; nothing is echoed or printed. Blank keeps what's there."""
    import getpass
    cur = json.loads(SECRETS.read_text(encoding="utf-8")) if SECRETS.exists() else {}
    cur.setdefault("discord_client_id", "1562931510364082336")
    asks = [("discord_bot_token", "Discord BOT TOKEN (Bot page > Reset Token > Copy)"),
            ("discord_client_secret", "Discord CLIENT SECRET (OAuth2 page > Reset Secret > Copy)"),
            ("flw_secret_key", "Flutterwave SECRET KEY (starts FLWSECK; blank to add later)")]
    print("Paste each one and press Enter. Nothing shows when you paste: that's normal.\n")
    for key, label in asks:
        v = getpass.getpass(label + ": ").strip()
        if v:
            cur[key] = v
    SECRETS.parent.mkdir(exist_ok=True)
    SECRETS.write_text(json.dumps(cur, indent=2), encoding="utf-8")
    print("\nSaved. Filled in: " + ", ".join(k for k, _ in asks if str(cur.get(k, "")).strip()))


def cmd_edit_secrets():
    """Writes a fill-in template if the file is missing, then opens it in Notepad for Samuel."""
    if not SECRETS.exists():
        SECRETS.parent.mkdir(exist_ok=True)
        SECRETS.write_text(json.dumps({
            "discord_bot_token": "PASTE BOT TOKEN HERE",
            "discord_client_id": "1562931510364082336",
            "discord_client_secret": "PASTE CLIENT SECRET HERE",
            "flw_secret_key": "PASTE FLUTTERWAVE SECRET KEY HERE"}, indent=2), encoding="utf-8")
    subprocess.Popen(["notepad.exe", str(SECRETS)])
    print("Opened in Notepad. Replace each PASTE ... HERE (keep the quotes), then Ctrl+S.")


def cmd_invite_url():
    cid = secrets()["discord_client_id"].strip()
    print(f"https://discord.com/oauth2/authorize?client_id={cid}&permissions=8&scope=bot%20applications.commands")


ICONS = {
    "welcome": "👋", "rules": "📜", "announcements": "📢", "start-here": "🧭", "workbook": "📘", "daily-nugget": "☀️",
    "introduce-yourself": "🙋", "general": "💬", "wins": "🏆", "daily-check-in": "✍️", "leaderboard": "🔥",
    "portfolio-and-profile": "🎞️", "outreach": "📨", "niche": "🎯", "questions": "❓", "davinci-help": "🎬", "gear": "🎧",
    "weekly-call": "🎙️", "call-recordings": "📼", "off-topic": "🍿", "payments-log": "💳", "mod-log": "🛡️",
    "subscription-expired": "🔒",
}
SEP = "・"


def shown(name):
    """What Discord shows: icon, dot, name (Samuel, 2026-10-22: icons on every channel)."""
    return f"{ICONS[name]}{SEP}{name}" if name in ICONS else name


def base(name):
    """A channel's plain name, without its icon, so lookups don't depend on the icon."""
    return name.split(SEP, 1)[-1]


def ow(role_id, allow=0, deny=0):
    return {"id": role_id, "type": 0, "allow": str(allow), "deny": str(deny)}


def overwrites(mode, everyone, roles):
    m, t, e = roles["member"], roles["team"], roles["expired"]
    if mode == "ro":
        return [ow(everyone, deny=VIEW), ow(m, VIEW | HISTORY | REACT, NO_POST), ow(t, VIEW | SEND | HISTORY), ow(e, deny=VIEW)]
    if mode == "team":
        return [ow(everyone, deny=VIEW), ow(m, deny=VIEW), ow(e, deny=VIEW), ow(t, VIEW | SEND | HISTORY)]
    if mode == "expired":
        return [ow(everyone, deny=VIEW), ow(m, deny=VIEW), ow(t, deny=VIEW), ow(e, VIEW | HISTORY, NO_POST | REACT)]
    return [ow(everyone, deny=VIEW), ow(e, deny=VIEW)]  # rw: Member and Team see it through their role


def cmd_build():
    c = load_cfg()
    g = c.get("guild") or find_guild()
    c["guild"] = g
    guild = api("GET", f"/guilds/{g}")

    # Roles. @everyone sees nothing: a paid Member, a Team seat or an Expired role decides what you see.
    existing = {r["name"]: r for r in api("GET", f"/guilds/{g}/roles")}
    want = {"Team": (TEAM_PERMS, 0xFCDD9E, True), "Member": (MEMBER_PERMS, 0xB9C3D6, False), "Expired": (0, 0x4A5670, False)}
    roles = {}
    for name, (perms, color, hoist) in want.items():
        body = {"name": name, "permissions": str(perms), "color": color, "hoist": hoist, "mentionable": False}
        r = existing.get(name)
        r = api("PATCH", f"/guilds/{g}/roles/{r['id']}", body) if r else api("POST", f"/guilds/{g}/roles", body)
        roles[name.lower()] = r["id"]
    api("PATCH", f"/guilds/{g}/roles/{g}", {"permissions": str(1 << 26)})  # @everyone: change nickname only
    c["roles"] = roles

    # Categories and channels, matched by name so a re-run updates instead of duplicating.
    chans = api("GET", f"/guilds/{g}/channels")
    by = {(base(ch["name"]), ch["type"]): ch for ch in chans}
    ids = c.setdefault("channels", {})
    for pos, (cat, items) in enumerate(LAYOUT):
        ckey = (cat.lower(), CATEGORY)
        cat_obj = by.get(ckey) or by.get((cat, CATEGORY))
        body = {"name": cat, "type": CATEGORY, "position": pos}
        cat_obj = api("PATCH", f"/channels/{cat_obj['id']}", {"name": cat, "position": pos}) if cat_obj else api("POST", f"/guilds/{g}/channels", body)
        for i, (name, typ, mode, topic) in enumerate(items):
            body = {"name": shown(name), "parent_id": cat_obj["id"], "position": i, "permission_overwrites": overwrites(mode, g, roles)}
            if topic and typ == TEXT:
                body["topic"] = topic
            if typ == FORUM:
                body.update({"default_auto_archive_duration": 10080, "default_reaction_emoji": {"emoji_name": "🔥"},
                             "default_sort_order": 0, "default_forum_layout": 1})
            ch = by.get((name, typ))
            if ch:
                ch = api("PATCH", f"/channels/{ch['id']}", body)
            else:
                if typ in (FORUM, STAGE) and "COMMUNITY" not in guild.get("features", []):
                    continue  # made after Community mode is on (second pass below)
                ch = api("POST", f"/guilds/{g}/channels", {**body, "type": typ})
            by[(name, typ)] = ch
            if name in CONFIG_KEYS:
                ids[CONFIG_KEYS[name]] = ch["id"]
    save_cfg(c)

    # Community mode (needed for the forum and the stage channel). Join messages go to #welcome.
    patch = {"verification_level": 1, "explicit_content_filter": 2, "default_message_notifications": 1,
             "rules_channel_id": ids["rules"], "public_updates_channel_id": ids["modLog"], "system_channel_id": ids["welcome"],
             "features": sorted(set(guild.get("features", [])) | {"COMMUNITY"})}
    if not guild.get("icon") and ICON.exists():
        import base64
        patch["icon"] = "data:image/png;base64," + base64.b64encode(ICON.read_bytes()).decode()
    api("PATCH", f"/guilds/{g}", patch)
    me = api("GET", "/users/@me")
    if not me.get("avatar") and ICON.exists():  # the bot wears the community logo in DMs
        import base64
        api("PATCH", "/users/@me", {"avatar": "data:image/png;base64," + base64.b64encode(ICON.read_bytes()).decode()})
    if "COMMUNITY" not in guild.get("features", []):
        print("Community mode on; making the forum and stage channels.")
        return cmd_build()

    # AutoMod, alerts to #mod-log. The Team role is exempt.
    alert = {"type": 2, "metadata": {"channel_id": ids["modLog"]}}
    block = lambda msg: {"type": 1, "metadata": {"custom_message": msg}}
    rules = [
        {"name": "Kindness", "trigger_type": 4, "trigger_metadata": {"presets": [1, 2, 3]},
         "actions": [block("That message was blocked. Keep it kind: see #rules."), alert]},
        {"name": "Scams", "trigger_type": 1, "trigger_metadata": {"keyword_filter": SCAM_WORDS},
         "actions": [block("Blocked: that looks like a scam or a sales pitch (rule 3 and 4)."), alert]},
        {"name": "Spam", "trigger_type": 3, "trigger_metadata": {}, "actions": [block("Blocked as spam."), alert]},
        {"name": "Mention spam", "trigger_type": 5, "trigger_metadata": {"mention_total_limit": 5, "mention_raid_protection_enabled": True},
         "actions": [block("Too many mentions in one message."), alert, {"type": 3, "metadata": {"duration_seconds": 600}}]},
    ]
    have = {r["name"]: r for r in api("GET", f"/guilds/{g}/auto-moderation/rules")}
    for r in rules:
        body = {**r, "event_type": 1, "enabled": True, "exempt_roles": [roles["team"]]}
        if r["name"] in have:
            body.pop("trigger_type")
            api("PATCH", f"/guilds/{g}/auto-moderation/rules/{have[r['name']]['id']}", body)
        else:
            api("POST", f"/guilds/{g}/auto-moderation/rules", body)
    # Discord's starter "Text Channels" / "Voice Channels" categories and voice "General", left empty by the move above.
    for ch in api("GET", f"/guilds/{g}/channels"):
        if ch["type"] == VOICE and ch["name"] == "General":
            api("DELETE", f"/channels/{ch['id']}")
    left = api("GET", f"/guilds/{g}/channels")
    for ch in left:
        if ch["type"] == CATEGORY and ch["name"].lower() in ("text channels", "voice channels") and not any(x.get("parent_id") == ch["id"] for x in left):
            api("DELETE", f"/channels/{ch['id']}")
    save_cfg(c)
    print(f"Built: {len(ids)} channels tracked, roles {', '.join(roles)}, AutoMod {len(rules)} rules, Community mode on.")


def sections():
    text = TEXTS.read_text(encoding="utf-8")
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def render(body, c):
    names = {}
    for ch in api("GET", f"/guilds/{c['guild']}/channels"):
        names[base(ch["name"])] = ch["id"]
    body = body.replace("{SITE}", SITE_URL)
    return re.sub(r"(?<![\w<&])#([a-z0-9-]+)", lambda m: f"<#{names[m.group(1)]}>" if m.group(1) in names else m.group(0), body)


def cmd_post_texts():
    c = load_cfg()
    if not c.get("guild"):
        sys.exit("Run build first.")
    sec = sections()
    ids = c["channels"]
    posted = c.setdefault("posted", {})
    by_name = {base(ch["name"]): ch["id"] for ch in api("GET", f"/guilds/{c['guild']}/channels")}
    for key, body in sec.items():
        if not key.startswith("#") or " " in key:
            continue
        name = key[1:]
        ch = by_name.get(name)
        if not ch:
            print("No channel for", key)
            continue
        content = render(body, c)
        mid = posted.get(name)
        files = None
        if name == "workbook" and not mid and WORKBOOK.exists():
            files = {"files[0]": (WORKBOOK.name, WORKBOOK.read_bytes(), "application/pdf")}
        if mid and api("PATCH", f"/channels/{ch}/messages/{mid}", {"content": content}, ok_missing=True):
            print("Updated", key)
            continue
        msg = api("POST", f"/channels/{ch}/messages", {"content": content, "allowed_mentions": {"parse": []}}, files=files)
        api("PUT", f"/channels/{ch}/pins/{msg['id']}")
        posted[name] = msg["id"]
        print("Posted and pinned", key)

    # The forum: guidelines, plus a pinned example post.
    forum = ids.get("checkin")
    if forum and "#daily-check-in guidelines" in sec:
        api("PATCH", f"/channels/{forum}", {"topic": render(sec["#daily-check-in guidelines"], c)[:4096]})
    if forum and "#daily-check-in example post" in sec:
        body = render(sec["#daily-check-in example post"], c)
        tid = posted.get("checkin-example")
        if tid and api("PATCH", f"/channels/{tid}/messages/{tid}", {"content": body}, ok_missing=True):
            print("Updated the example check-in")
        else:
            t = api("POST", f"/channels/{forum}/threads", {"name": "📌 How to check in (example)", "message": {"content": body}})
            api("PATCH", f"/channels/{t['id']}", {"flags": 2})  # pinned in the forum
            posted["checkin-example"] = t["id"]
            print("Posted the example check-in")
    save_cfg(c)


NETLIFY_JS = Path(os.environ["APPDATA"]) / "npm" / "node_modules" / "netlify-cli" / "bin" / "run.js"


def netlify(*args, secret_value=False):
    # node + run.js directly, no shell, so JSON and keys pass through unmangled
    r = subprocess.run(["node", str(NETLIFY_JS), *args], cwd=SITE_DIR, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        sys.exit("netlify " + (args[0] if secret_value else " ".join(args)) + " failed: " + (r.stderr or r.stdout)[-300:])
    return r.stdout


def cmd_push_env():
    s = secrets()
    c = load_cfg()
    values = {
        "DISCORD_BOT_TOKEN": s["discord_bot_token"].strip(),
        "DISCORD_CLIENT_SECRET": s["discord_client_secret"].strip(),
        "DISCORD_CLIENT_ID": s["discord_client_id"].strip(),
        "DISCORD_CONFIG": json.dumps({k: c[k] for k in ("guild", "roles", "channels") if k in c}, separators=(",", ":")),
    }
    if str(s.get("flw_secret_key", "")).strip().startswith("FLWSECK"):
        values["FLW_SECRET_KEY"] = s["flw_secret_key"].strip()
    else:
        print("Flutterwave secret key not filled in yet: skipped.")
    # Python here can't launch the Netlify CLI, so the values go into a one-off file that
    # `netlify env:import` reads from bash (output silenced), then the file is removed.
    out = SITE_DIR / ".env.push"
    out.write_text("".join(f"{k}={v}\n" for k, v in values.items()), encoding="utf-8")
    print("Wrote", ", ".join(values), "to .env.push. Now, in the site folder:")
    print("  netlify env:import .env.push >/dev/null && rm .env.push && sh deploy.sh 'keys'")


def cmd_nuggets():
    lines = [l[2:].strip() for l in sections().get("Morning nuggets", "").splitlines() if l.startswith("- ")]
    out = SITE_DIR / "netlify" / "lib" / "nuggets.mjs"
    out.write_text("// Made by community_admin.py nuggets from the Brain note. Don't edit here.\nexport default "
                   + json.dumps(lines, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print(f"{len(lines)} nuggets written.")


def cmd_status():
    c = load_cfg()
    g = c.get("guild") or find_guild()
    guild = api("GET", f"/guilds/{g}?with_counts=true")
    print(f"{guild['name']}: {guild.get('approximate_member_count')} members, features: {', '.join(guild.get('features', [])) or 'none'}")
    chans = api("GET", f"/guilds/{g}/channels")
    cats = {ch["id"]: ch["name"] for ch in chans if ch["type"] == CATEGORY}
    for ch in sorted(chans, key=lambda x: (x["type"] == CATEGORY, x.get("position", 0))):
        if ch["type"] != CATEGORY:
            print(f"  {cats.get(ch.get('parent_id'), '-'):12} #{ch['name']}")


def cmd_members():
    raw = netlify("blobs:list", "community", "--prefix", "m:", "--json")
    keys = [b["key"] for b in json.loads(raw).get("blobs", [])]
    print(f"{len(keys)} members")
    for k in keys:
        m = json.loads(netlify("blobs:get", "community", k))
        print(f"  {m.get('name', '?')[:24]:24} {m.get('status', '?'):8} to {str(m.get('expiresAt', ''))[:10]}  "
              f"{m.get('method', '')}{' auto' if m.get('autoRenew') and m.get('cardToken') else ''}  discord: {m.get('discordName', '-')}")


def cmd_team_invite():
    c = load_cfg()
    inv = api("POST", f"/channels/{c['channels']['welcome']}/invites", {"max_age": 86400, "max_uses": 1, "unique": True})
    print(f"https://discord.gg/{inv['code']}  (one use, 24 hours). After they join: python community_admin.py team <their name>")


def cmd_team(name):
    c = load_cfg()
    found = api("GET", f"/guilds/{c['guild']}/members/search?query={requests.utils.quote(name)}&limit=5")
    if len(found) != 1:
        sys.exit(f"{len(found)} matches for '{name}': " + ", ".join(f['user']['username'] for f in found))
    uid = found[0]["user"]["id"]
    api("PUT", f"/guilds/{c['guild']}/members/{uid}/roles/{c['roles']['team']}")
    print(f"Team seat given to @{found[0]['user']['username']}.")


def cmd_say(channel, text):
    c = load_cfg()
    by_name = {base(ch["name"]): ch["id"] for ch in api("GET", f"/guilds/{c['guild']}/channels")}
    if channel.lstrip("#") not in by_name:
        sys.exit("No channel " + channel)
    api("POST", f"/channels/{by_name[channel.lstrip('#')]}/messages", {"content": render(text, c), "allowed_mentions": {"parse": []}})
    print("Posted.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    cmds = {"setup-secrets": cmd_setup_secrets, "edit-secrets": cmd_edit_secrets, "invite-url": cmd_invite_url, "build": cmd_build, "post-texts": cmd_post_texts, "push-env": cmd_push_env,
            "nuggets": cmd_nuggets, "status": cmd_status, "members": cmd_members, "team-invite": cmd_team_invite}
    if a and a[0] in cmds:
        cmds[a[0]]()
    elif a[:1] == ["team"] and len(a) > 1:
        cmd_team(" ".join(a[1:]))
    elif a[:1] == ["say"] and len(a) > 2:
        cmd_say(a[1], " ".join(a[2:]))
    else:
        print(__doc__)
