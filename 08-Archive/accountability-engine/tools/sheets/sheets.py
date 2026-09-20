#!/usr/bin/env python3
"""
engine -> Google Sheets client.

Talks to the Apps Script web app bound to "My Claude Budget" (see Code.gs).
Stdlib only, no pip install, so it runs here and in a cloud routine unchanged.

Config comes from .env at the repo root, or from environment variables of the
same names. .env is gitignored, so a cloud session has no .env — it gets the
same three values from its cloud environment instead (tools/sheets/README.md).

    SHEETS_WEBAPP_URL=https://script.google.com/macros/s/AKfy.../exec
    SHEETS_TOKEN=...
    SHEETS_ID=1BrM8jAJC8Wuqm6WWZnu9jocdeNfxr4rYngapAXTXWMI

Usage
-----
    python tools/sheets/sheets.py ping
    python tools/sheets/sheets.py read Budget            [A1:P40]
    python tools/sheets/sheets.py formulas Budget C5:C20
    python tools/sheets/sheets.py append Expenses '[["2026-08-26","Feeding",8500]]'
    python tools/sheets/sheets.py ops payload.json       # full batch, the one that does real work
    echo '{"ops":[...]}' | python tools/sheets/sheets.py ops -
    python tools/sheets/sheets.py ops payload.json --queue "reckoning 2026-08-27"

    python tools/sheets/sheets.py doctor    # why can't THIS session reach the sheet
    python tools/sheets/sheets.py pending   # what is in the ledger but not the sheet
    python tools/sheets/sheets.py flush     # replay whatever an offline session queued

`ops` is the general form. Everything else is a shortcut onto it.

With `--queue LABEL`, a batch that cannot be delivered is parked in
context/sheet-queue.jsonl instead of being lost, and the next session anywhere
that CAN reach the bridge replays it with `flush`. That is what makes the cloud,
the phone and this desktop equivalent: a session that cannot reach the sheet
defers the write, it never drops it.
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE = os.path.join(REPO, "context", "sheet-queue.jsonl")
QUEUE_DONE = os.path.join(REPO, "context", "sheet-queue.done.jsonl")

# The Apps Script /exec URL 302s to script.googleusercontent.com, so both hosts
# have to be reachable. Neither is on the cloud "Trusted" default allowlist.
DOMAINS = ["script.google.com", "*.googleusercontent.com"]

FIX = """
This session cannot write to the budget sheet. One-time fix, in the browser,
by editing the cloud environment the routines run in. There is no settings page
for it: open claude.ai/code/routines, open a routine, click the pencil, then the
cloud icon under the Instructions box, then the gear on the environment.

  1. Network access: Custom, with "also include default list" ticked.
     Allowed domains:
         script.google.com
         *.googleusercontent.com
     The Trusted default list does NOT include these, so the bridge stays
     blocked from the cloud even when the credentials are right.

  2. Environment variables (.env format). The same three values as the repo's
     own .env — print them with:  python tools/sheets/sheets.py env
         SHEETS_WEBAPP_URL=...
         SHEETS_TOKEN=...
         SHEETS_ID=...

Routines run in the same environment, so this fixes the scheduled brief, midday
and reckoning too. A session already running keeps the values it started with —
start a new one. Full detail: tools/sheets/README.md.
"""


def load_env():
    cfg = {}
    path = os.path.join(REPO, ".env")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("SHEETS_WEBAPP_URL", "SHEETS_TOKEN", "SHEETS_ID"):
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    return cfg


class BridgeError(Exception):
    """The batch did not land in the sheet. `kind` says why, in one word."""

    def __init__(self, kind, msg):
        Exception.__init__(self, msg)
        self.kind = kind


# The last row of each tab the Budget tab's SUMIF windows actually reach.
# A row past this is ON the tab and INVISIBLE to every total. Keep in step with
# the ranges written by tools/sheets/build_budget.py.
READABLE_TO = {"Income": 124, "Expenses": 404, "Transfers": 404}


def _anchor_appends(ops):
    """Point every bare `append` at the last row that has a DATE in column A.

    Apps Script's getLastRow() counts formatting and footer text, so on Income
    and Expenses it returns 124 and 404 — far below the real data. An append
    that trusts it lands outside the SUMIF windows the Budget tab reads: the
    row is on the tab, every total ignores it, and nothing says a word.

    Found 2026-09-02 and fixed the same day — but only on the `append` CLI
    verb, while the reckoning mirrors money through `ops`. It landed four
    Payday A rows at 405-408 that same night. The anchoring belongs HERE, at
    the one chokepoint every path goes through: `ops`, `append`, and `flush`.
    """
    todo = [o for o in ops if o.get("action") == "append" and "after" not in (o.get("args") or {})]
    if not todo:
        return

    tabs = []
    for o in todo:
        tab = (o.get("args") or {}).get("tab")
        if tab and tab not in tabs:
            tabs.append(tab)

    reads = _send_raw(
        [{"action": "read", "args": {"tab": t, "range": "A1:A1000"}} for t in tabs]
    )
    last = {}
    for tab, block in zip(tabs, reads):
        rows = block.get("values") or []
        n = 0
        for i, row in enumerate(rows):
            if row and str(row[0]).strip():
                n = i + 1
        last[tab] = n

    # Several appends to one tab in a single batch must stack, not collide.
    for o in todo:
        args = o["args"]
        tab = args.get("tab")
        if last.get(tab):
            args["after"] = last[tab]
            last[tab] += len(args.get("values") or [])


def _warn_out_of_range(ops, results):
    """Say it out loud when a batch lands where no total can see it."""
    for op, res in zip(ops, results or []):
        if op.get("action") != "append" or not isinstance(res, dict):
            continue
        tab = (op.get("args") or {}).get("tab")
        landed = res.get("appendedAtRow")
        cap = READABLE_TO.get(tab)
        rows = len(((op.get("args") or {}).get("values")) or [])
        if cap and landed and landed + rows - 1 > cap:
            sys.stderr.write(
                "\nWARNING: %s rows landed at %d-%d but the Budget tab only reads that tab\n"
                "to row %d. They are ON the tab and INVISIBLE to every total. Widen the\n"
                "ranges in tools/sheets/build_budget.py and re-run it before trusting any\n"
                "figure on the sheet.\n" % (tab, landed, landed + rows - 1, cap)
            )


def send(ops):
    """POST a batch. Raises BridgeError on any failure — never exits.

    Appends are anchored to real data first, so no caller can land a row
    outside the ranges the Budget tab sums.
    """
    _anchor_appends(ops)
    results = _send_raw(ops)
    _warn_out_of_range(ops, results)
    return results


def _send_raw(ops):
    """The bare POST. Never call this directly — go through send()."""
    ops = list(ops)
    cfg = load_env()
    url = cfg.get("SHEETS_WEBAPP_URL")
    token = cfg.get("SHEETS_TOKEN")
    if not url or not token:
        raise BridgeError(
            "config", "SHEETS_WEBAPP_URL / SHEETS_TOKEN missing from this session."
        )

    body = json.dumps({"token": token, "ops": ops}).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise BridgeError(
            "http",
            "HTTP %s from the web app: %s"
            % (e.code, e.read().decode("utf-8", "replace")[:2000]),
        )
    except urllib.error.URLError as e:
        raise BridgeError("network", "could not reach the web app: %s" % e.reason)

    try:
        out = json.loads(raw)
    except ValueError:
        raise BridgeError(
            "response",
            "the web app did not return JSON. First 800 chars: "
            + raw[:800]
            + " -- usually this means the deployment is not set to "
            '"Execute as: Me" + "Who has access: Anyone".',
        )

    if not out.get("ok"):
        raise BridgeError("rejected", "web app error: %s" % out.get("error"))
    return out["results"]


def post(ops):
    """send(), but exits with the message. For the interactive commands."""
    try:
        return send(ops)
    except BridgeError as e:
        msg = str(e)
        if e.kind in ("config", "network"):
            msg += FIX
        die(msg)


def die(msg):
    sys.stderr.write("sheets.py: " + msg + "\n")
    sys.exit(1)


def show(results):
    print(json.dumps(results, indent=2, ensure_ascii=False))


def grid(values):
    """Print a read result as a readable grid."""
    if not values:
        print("(empty)")
        return
    for i, row in enumerate(values, start=1):
        cells = [str(c) for c in row]
        while cells and cells[-1] == "":
            cells.pop()
        if cells:
            print("%4d | %s" % (i, " | ".join(cells)))


# ------------------------------------------------------------------ the queue
#
# A session that cannot reach the bridge parks its batch here instead of losing
# it. The ledger is still written first and is still the source of truth; the
# queue exists only so the mirror catches itself up from wherever it next can.


def queue_batch(ops, label):
    stamp = datetime.datetime.now()
    entry = {
        "id": stamp.strftime("%Y%m%dT%H%M%S"),
        "queued_at": stamp.isoformat(timespec="seconds"),
        "label": label,
        "ops": ops,
    }
    with open(QUEUE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def read_queue():
    if not os.path.exists(QUEUE):
        return []
    entries = []
    with open(QUEUE, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def write_queue(entries):
    if not entries:
        if os.path.exists(QUEUE):
            os.remove(QUEUE)
        return
    with open(QUEUE, "w", encoding="utf-8") as fh:
        for e in entries:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")


def archive(entry):
    """Delivered batches move to the .done file. Nothing is ever just deleted."""
    entry = dict(entry)
    entry["flushed_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    with open(QUEUE_DONE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def flush():
    """Replay every parked batch, oldest first. Stop at the first failure."""
    queued = read_queue()
    if not queued:
        print("nothing queued — the sheet is up to date.")
        return 0

    for i, entry in enumerate(queued):
        try:
            send(entry["ops"])
        except BridgeError as e:
            write_queue(queued[i:])
            print("flushed %d of %d, then stopped." % (i, len(queued)))
            msg = str(e)
            if e.kind in ("config", "network"):
                msg += FIX
            die(msg)
        archive(entry)
        print("flushed  %s  %s" % (entry["id"], entry.get("label") or "(no label)"))

    write_queue([])
    print("")
    print("%d queued batch(es) mirrored into the sheet. Queue empty." % len(queued))
    print("Commit context/sheet-queue*.jsonl before this session ends.")
    return 0


def pending():
    queued = read_queue()
    if not queued:
        print("nothing queued — the sheet is up to date.")
        return 0
    print("%d batch(es) in the ledger but NOT yet in the sheet:" % len(queued))
    print("")
    for e in queued:
        print(
            "  %s  %s  (%d ops)"
            % (e["queued_at"], e.get("label") or "(no label)", len(e["ops"]))
        )
    print("")
    print("Run: python tools/sheets/sheets.py flush")
    return 1


def doctor():
    """Say, in order, which link in the chain is broken and what to do about it."""
    cfg = load_env()
    dotenv = os.path.exists(os.path.join(REPO, ".env"))
    from_env = [k for k in ("SHEETS_WEBAPP_URL", "SHEETS_TOKEN") if os.environ.get(k)]
    remote = os.environ.get("CLAUDE_CODE_REMOTE") == "1"

    print("where      : %s" % ("cloud session" if remote else "local checkout"))
    print(
        ".env file  : %s"
        % ("found" if dotenv else "absent — expected in the cloud, it is gitignored")
    )
    print("env vars   : %s" % (", ".join(from_env) if from_env else "none set"))

    if not cfg.get("SHEETS_WEBAPP_URL") or not cfg.get("SHEETS_TOKEN"):
        print("verdict    : NO CREDENTIALS — the bridge has no URL or token to use.")
        sys.stdout.write(FIX)
        return 1

    try:
        info = send([{"action": "ping", "args": {}}])[0]
    except BridgeError as e:
        verdicts = {
            "network": "BLOCKED — credentials are set, but the network refused the connection.",
            "http": "HTTP ERROR — the web app answered with an error status.",
            "rejected": "REJECTED — reached the web app, but it refused the request. Wrong token?",
            "response": "BAD RESPONSE — reached something, but not the web app.",
        }
        print("verdict    : %s" % verdicts.get(e.kind, "FAILED."))
        print("detail     : %s" % str(e).splitlines()[0][:300])
        if e.kind == "network":
            sys.stdout.write(FIX)
        return 1

    print("verdict    : OK — reached %r, %d tabs." % (info["name"], len(info["tabs"])))
    queued = read_queue()
    if queued:
        print(
            "queued     : %d batch(es) waiting. Run: python tools/sheets/sheets.py flush"
            % len(queued)
        )
    else:
        print("queued     : nothing pending.")
    return 0


def main(argv):
    # Windows consoles default to cp1252, which cannot encode the naira sign.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if not argv:
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]

    if cmd == "ping":
        show(post([{"action": "ping", "args": {}}]))

    elif cmd == "read":
        args = {"tab": rest[0]}
        if len(rest) > 1:
            args["range"] = rest[1]
        grid(post([{"action": "read", "args": args}])[0]["values"])

    elif cmd == "formulas":
        args = {"tab": rest[0]}
        if len(rest) > 1:
            args["range"] = rest[1]
        grid(post([{"action": "readFormulas", "args": args}])[0]["formulas"])

    elif cmd == "append":
        # The anchoring and the out-of-range warning live in send(), so every
        # path gets them — this verb, `ops`, and `flush` alike. See
        # _anchor_appends() for why that matters and what it cost to learn.
        tab, values = rest[0], json.loads(rest[1])
        if not values or not values[0]:
            die("append needs at least one non-empty row.")
        show(post([{"action": "append", "args": {"tab": tab, "values": values}}]))

    elif cmd == "write":
        show(post([{"action": "write", "args": {"tab": rest[0], "cell": rest[1], "values": json.loads(rest[2])}}]))

    elif cmd == "script":
        # Print Code.gs with the real token substituted in, for pasting into the
        # Apps Script editor. The committed Code.gs keeps a placeholder so the
        # token never enters git history.
        cfg = load_env()
        if not cfg.get("SHEETS_TOKEN"):
            die("SHEETS_TOKEN missing from .env")
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Code.gs")
        with open(src, encoding="utf-8") as fh:
            body = fh.read()
        if "__SHEETS_TOKEN__" not in body:
            die("Code.gs has no __SHEETS_TOKEN__ placeholder — refusing to print it")
        sys.stdout.write(body.replace("__SHEETS_TOKEN__", cfg["SHEETS_TOKEN"]))

    elif cmd == "env":
        # The three lines to paste into the cloud environment's variables box.
        # Secrets on stdout, deliberately — redirect it to a file and open that.
        # Never into a chat, an issue or a screenshot.
        cfg = load_env()
        for k in ("SHEETS_WEBAPP_URL", "SHEETS_TOKEN", "SHEETS_ID"):
            if not cfg.get(k):
                die("%s missing from .env" % k)
            print("%s=%s" % (k, cfg[k]))

    elif cmd == "ops":
        label = ""
        if "--queue" in rest:
            i = rest.index("--queue")
            label = rest[i + 1] if len(rest) > i + 1 else "(unlabelled)"
            rest = rest[:i] + rest[i + 2:]
        src = sys.stdin.read() if rest[0] == "-" else open(rest[0], encoding="utf-8").read()
        payload = json.loads(src)
        ops = payload["ops"] if isinstance(payload, dict) else payload
        if not label:
            show(post(ops))
        else:
            try:
                show(send(ops))
            except BridgeError as e:
                entry = queue_batch(ops, label)
                sys.stderr.write("sheets.py: %s\n" % e)
                print("")
                print("NOT written to the sheet. Queued as %s (%s)." % (entry["id"], label))
                print("The ledger still stands as the source of truth. The next")
                print("session anywhere that can reach the bridge picks it up with:")
                print("    python tools/sheets/sheets.py flush")
                print("Commit context/sheet-queue.jsonl before this session ends.")
                if e.kind in ("config", "network"):
                    sys.stdout.write(FIX)

    elif cmd == "doctor":
        return doctor()

    elif cmd == "flush":
        return flush()

    elif cmd == "pending":
        return pending()

    else:
        die("unknown command: %s" % cmd)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
