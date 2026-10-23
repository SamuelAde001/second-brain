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
# Samuel, 2026-10-22: few, essential channels; the community is for growing with others, the
# 60-day challenge is one activity in it.
LAYOUT = [
    ("START HERE", [
        ("start-here", TEXT, "ro", "What this community is, the rules, and how to use it. Read first."),
        ("announcements", TEXT, "ro", "Live calls, challenges and news from Samuel."),
        ("welcome", TEXT, "rw", "New here? Say hi: your name, where you edit from, what you edit, who you want to edit for."),
    ]),
    ("COMMUNITY", [
        ("general", TEXT, "rw", "Talk with the community. The morning nugget from Samuel lands here."),
        ("wins", TEXT, "rw", "Clients, replies, finished videos, milestones. Share them. Sunday's leaderboard lands here too."),
        ("accountability", FORUM, "rw", None),
        ("ask-editors-bot", TEXT, "rw", "Ask Editors Bot anything from Samuel's teachings. Type /ask, or /help for all commands."),
    ]),
    ("GROW", [
        ("feedback", FORUM, "rw", None),
        ("resources", FORUM, "rw", None),
        ("opportunities", TEXT, "rw", "Gigs, client leads, jobs and collabs. Too busy for a job? Pass it on here."),
        ("help", TEXT, "rw", "Stuck? Software, gear, clients, pricing, anything."),
    ]),
    ("LIVE", [
        ("weekly-live", STAGE, "rw", None),
    ]),
    ("TEAM", [
        # Samuel, 2026-10-23: "we need to have a team chat room and a team call room"
        ("team-chat", TEXT, "team", "The team's own chat. Members can't see this."),
        ("team-call", VOICE, "team", None),
        ("payments-log", TEXT, "team", "Payments, joins, renewals and expiries, posted by the bot."),
        ("mod-log", TEXT, "team", "What AutoMod blocked."),
    ]),
    ("SUBSCRIPTION", [
        ("subscription-expired", TEXT, "expired", "Renew to get back in."),
    ]),
]
# Old channel -> new channel, kept so posts and links survive the rename.
RENAMES = {"daily-check-in": "accountability", "questions": "help", "weekly-call": "weekly-live"}
# Channels from the first layout that are gone (Samuel: "any thing not neccessary should be removed").
REMOVED = ["rules", "workbook", "daily-nugget", "introduce-yourself", "leaderboard", "portfolio-and-profile",
           "outreach", "niche", "davinci-help", "gear", "call-recordings", "off-topic"]
FORUM_TAGS = {
    "accountability": [("60-Day Challenge", "🗓️"), ("Weekly goals", "🎯"), ("Daily log", "✍️")],
    "feedback": [("Edit", "🎬"), ("Portfolio", "🗂️"), ("Profile and bio", "🪪"), ("Outreach", "📨"), ("Niche", "🧭"), ("Client work", "💼")],
    "resources": [("Tutorial", "🎓"), ("Editing hack", "⚡"), ("Template or asset", "🧩"), ("Tool", "🛠️"), ("Call replay", "📼")],
}
CONFIG_KEYS = {  # channel name -> keys the site's functions use
    "welcome": ["welcome"], "start-here": ["startHere", "rules"], "announcements": ["announcements"],
    "general": ["general", "nugget"], "wins": ["wins", "leaderboard"], "accountability": ["checkin"],
    "ask-editors-bot": ["askBot"], "feedback": ["feedback"], "resources": ["resources"],
    "opportunities": ["opportunities"], "help": ["help"], "weekly-live": ["live"],
    "payments-log": ["payments"], "mod-log": ["modLog"], "subscription-expired": ["expired"],
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
            "flw_secret_key": "PASTE FLUTTERWAVE SECRET KEY HERE",
            "gemini_api_key": "PASTE GEMINI API KEY HERE"}, indent=2), encoding="utf-8")
    else:  # add any key the file doesn't have yet, keeping what's there
        cur = json.loads(SECRETS.read_text(encoding="utf-8"))
        if "gemini_api_key" not in cur:  # Editors Bot runs on Gemini (Samuel, 2026-10-23)
            cur["gemini_api_key"] = "PASTE GEMINI API KEY HERE"
            SECRETS.write_text(json.dumps(cur, indent=2), encoding="utf-8")
    subprocess.Popen(["notepad.exe", str(SECRETS)])
    print("Opened in Notepad. Replace each PASTE ... HERE (keep the quotes), then Ctrl+S.")


def cmd_invite_url():
    cid = secrets()["discord_client_id"].strip()
    print(f"https://discord.com/oauth2/authorize?client_id={cid}&permissions=8&scope=bot%20applications.commands")


ICONS = {
    "start-here": "🧭", "announcements": "📢", "welcome": "👋", "general": "💬", "wins": "🏆",
    "accountability": "✅", "ask-editors-bot": "🤖", "feedback": "🎞️", "resources": "📚",
    "opportunities": "💼", "help": "🆘", "weekly-live": "🎙️", "payments-log": "💳", "mod-log": "🛡️",
    "subscription-expired": "🔒", "team-chat": "🗨️", "team-call": "📞",
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
    for ch in chans:
        if base(ch["name"]) in RENAMES:
            ch.update(api("PATCH", f"/channels/{ch['id']}", {"name": shown(RENAMES[base(ch["name"])])}))
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
            if typ == FORUM and name in FORUM_TAGS and not ch.get("available_tags"):
                ch = api("PATCH", f"/channels/{ch['id']}", {"available_tags": [{"name": n, "emoji_name": e} for n, e in FORUM_TAGS[name]]})
            for key in CONFIG_KEYS.get(name, []):
                ids[key] = ch["id"]
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
    keep = {k for keys in CONFIG_KEYS.values() for k in keys}
    for k in [k for k in ids if k not in keep]:
        ids.pop(k)
    # Channels the layout dropped, then categories left empty (the guild's rules channel already moved).
    layout_cats = {cat for cat, _ in LAYOUT}
    for ch in api("GET", f"/guilds/{g}/channels"):
        if ch["type"] != CATEGORY and base(ch["name"]) in REMOVED:
            api("DELETE", f"/channels/{ch['id']}")
    left = api("GET", f"/guilds/{g}/channels")
    for ch in left:
        if ch["type"] == CATEGORY and ch["name"] not in layout_cats and not any(x.get("parent_id") == ch["id"] for x in left):
            api("DELETE", f"/channels/{ch['id']}")

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
    """Each '## #channel' (or '## #channel 2') section is one pinned bot message there, edited in place
    on re-runs. '## #forum guidelines' is a forum's guidelines; '## #forum post: Title' its pinned post."""
    c = load_cfg()
    if not c.get("guild"):
        sys.exit("Run build first.")
    sec = sections()
    posted = c.setdefault("posted", {})
    by_name = {base(ch["name"]): ch["id"] for ch in api("GET", f"/guilds/{c['guild']}/channels")}

    # The first layout's example check-in post is replaced by the posts below.
    if posted.get("checkin-example"):
        api("DELETE", f"/channels/{posted.pop('checkin-example')}", ok_missing=True)

    for key, body in sec.items():
        if not key.startswith("#"):
            continue
        name, _, rest = key[1:].partition(" ")
        ch = by_name.get(name)
        if not ch:
            print("No channel for", key)
            continue
        content = render(body, c)
        if rest == "guidelines":
            api("PATCH", f"/channels/{ch}", {"topic": content[:4096]})
            print("Guidelines set for", name)
            continue
        if rest.startswith("post:"):
            title = rest[5:].strip()
            tid = posted.get(key)
            if tid and api("PATCH", f"/channels/{tid}/messages/{tid}", {"content": content}, ok_missing=True):
                print("Updated forum post", key)
                continue
            files = None
            if "60-Day" in title and WORKBOOK.exists():
                files = {"files[0]": (WORKBOOK.name, WORKBOOK.read_bytes(), "application/pdf")}
            t = api("POST", f"/channels/{ch}/threads", {"name": title[:100], "message": {"content": content, "allowed_mentions": {"parse": []}}}, files=files)
            api("PATCH", f"/channels/{t['id']}", {"flags": 2})  # pinned at the top of the forum
            posted[key] = t["id"]
            print("Posted forum post", key)
            continue
        mid = posted.get(key) or posted.get(name) if not rest else posted.get(key)
        if mid and api("PATCH", f"/channels/{ch}/messages/{mid}", {"content": content}, ok_missing=True):
            posted[key] = mid
            print("Updated", key)
            continue
        msg = api("POST", f"/channels/{ch}/messages", {"content": content, "allowed_mentions": {"parse": []}})
        api("PUT", f"/channels/{ch}/pins/{msg['id']}")
        posted[key] = msg["id"]
        print("Posted and pinned", key)
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
        "DISCORD_CONFIG": json.dumps({k: c[k] for k in ("guild", "roles", "channels", "call") if k in c}, separators=(",", ":")),
        "DISCORD_PUBLIC_KEY": api("GET", "/applications/@me")["verify_key"],  # not secret; checks Discord's signatures
    }
    if str(s.get("gemini_api_key", "")).strip().startswith("AIza"):
        values["GEMINI_API_KEY"] = s["gemini_api_key"].strip()  # Netlify only
    else:
        print("Anthropic API key not filled in yet: Editors Bot's /ask, /review and /niche wait for it.")
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



TEACHINGS = BRAIN / "04-Projects" / "called-to-edit-webinar-teachings.md"


def cmd_knowledge():
    """Editors Bot's knowledge: the webinar teachings, without the production notes (board, recording dates)."""
    text = TEACHINGS.read_text(encoding="utf-8")
    text = text[text.index("\n## 0."):]
    out, skip = [], False
    for line in text.splitlines():
        if line.startswith("**Board") or line.startswith("**Settled") or line.startswith("Recorded "):
            skip = True
            continue
        if skip and (line.startswith("#") or line.startswith("**")):
            skip = False
        if skip or "Brand manager" in line:
            continue
        line = re.sub(r"\[\[[^|\]]*\|([^\]]+)\]\]", r"\1", line)
        line = re.sub(r"\[\[([^\]]+)\]\]", r"\1", line)
        out.append(line)
    body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    dest = SITE_DIR / "netlify" / "lib" / "knowledge.mjs"
    dest.write_text("// Made by community_admin.py knowledge from the Brain's webinar teachings. Don't edit here.\nexport default "
                    + json.dumps(body, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"Knowledge written: {len(body):,} characters.")


S, I = 3, 4  # option types: string, integer
COMMANDS = [
    {"name": "ask", "description": "Ask Editors Bot anything from Samuel's teachings",
     "options": [{"type": S, "name": "question", "description": "Your question", "required": True, "max_length": 1000}]},
    {"name": "review", "description": "Feedback on your bio, portfolio blurb or outreach message",
     "options": [{"type": S, "name": "text", "description": "Paste it here", "required": True, "max_length": 1800}]},
    {"name": "niche", "description": "Say your niche in one sentence",
     "options": [{"type": S, "name": "what", "description": "What you edit, e.g. talking-head Reels", "required": True, "max_length": 300},
                 {"type": S, "name": "who", "description": "Who for, e.g. real estate agents", "required": False, "max_length": 300}]},
    {"name": "nugget", "description": "A nugget from Samuel's teaching"},
    {"name": "streak", "description": "Your accountability streak and days done"},
    {"name": "subscription", "description": "When your access ends, and how to renew"},
    {"name": "call", "description": "When the next weekly live call is"},
    {"name": "help", "description": "Everything Editors Bot can do"},
]


def cmd_bot_setup():
    """Name, slash commands and the Interactions Endpoint (the site must already be deployed with DISCORD_PUBLIC_KEY)."""
    c = load_cfg()
    app = api("GET", "/applications/@me")
    try:
        api("PATCH", "/users/@me", {"username": "Editors Bot"})
    except SystemExit as e:
        print("Username not changed now (Discord limits renames):", str(e)[:120])
    api("PATCH", f"/guilds/{c['guild']}/members/@me", {"nick": "Editors Bot"})
    api("PUT", f"/applications/{app['id']}/guilds/{c['guild']}/commands", COMMANDS)
    api("PATCH", "/applications/@me", {"interactions_endpoint_url": SITE_URL + "/api/interactions",
                                       "description": "The Called to Edit Community's guide. Ask me anything from Samuel's teachings: type /help."})
    print(f"Editors Bot: name set, {len(COMMANDS)} slash commands registered, endpoint {SITE_URL}/api/interactions.")


DAYS = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]


def cmd_call(day_name, hhmm, *label):
    """Weekly live call, e.g.: call wednesday 19:00. Then push-env + deploy."""
    c = load_cfg()
    h, m = (int(x) for x in hhmm.split(":"))
    d = DAYS.index(day_name.lower())
    nice = f"{DAYS[d].capitalize()}s, {((h - 1) % 12) + 1}:{m:02d}{'am' if h < 12 else 'pm'} WAT"
    c["call"] = {"day": d, "hour": h, "minute": m, "text": " ".join(label) or nice}
    save_cfg(c)
    print("Call saved:", c["call"]["text"], "- now push-env and deploy.")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    cmds = {"setup-secrets": cmd_setup_secrets, "edit-secrets": cmd_edit_secrets, "invite-url": cmd_invite_url, "build": cmd_build, "post-texts": cmd_post_texts, "push-env": cmd_push_env,
            "nuggets": cmd_nuggets, "status": cmd_status, "members": cmd_members, "team-invite": cmd_team_invite,
            "knowledge": cmd_knowledge, "bot-setup": cmd_bot_setup}
    if a and a[0] in cmds:
        cmds[a[0]]()
    elif a[:1] == ["team"] and len(a) > 1:
        cmd_team(" ".join(a[1:]))
    elif a[:1] == ["call"] and len(a) > 2:
        cmd_call(*a[1:])
    elif a[:1] == ["say"] and len(a) > 2:
        cmd_say(a[1], " ".join(a[2:]))
    else:
        print(__doc__)
