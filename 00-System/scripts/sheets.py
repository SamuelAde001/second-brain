#!/usr/bin/env python3
"""
engine -> Google Sheets client.

Talks to the Apps Script web app bound to "My Claude Budget" (see Code.gs).
Stdlib only, no pip install, so it runs here and in a cloud routine unchanged.

Ported into the Brain 2026-09-22 from the Accountability Engine
(08-Archive/accountability-engine/tools/sheets/). What changed: credentials are
never read from a file in the Brain. They come from environment variables, and
on Windows from the user's own variables in the registry (the HKCU Environment key),
which Samuel sets once himself (03-Areas/finances/budget-system.md). The secret
never enters the Brain, git or a chat. There is no `env` command any more, and
`script` copies to the clipboard instead of printing.

    SHEETS_WEBAPP_URL=https://script.google.com/macros/s/AKfy.../exec
    SHEETS_TOKEN=...
    SHEETS_ID=1BrM8jAJC8Wuqm6WWZnu9jocdeNfxr4rYngapAXTXWMI

Usage
-----
    python 00-System/scripts/sheets.py ping
    python 00-System/scripts/sheets.py read Budget            [A1:P40]
    python 00-System/scripts/sheets.py formulas Budget C5:C20
    python 00-System/scripts/sheets.py append Expenses '[["2026-08-26","Feeding",8500]]'
    python 00-System/scripts/sheets.py ops payload.json       # full batch, the one that does real work
    echo '{"ops":[...]}' | python 00-System/scripts/sheets.py ops -
    python 00-System/scripts/sheets.py ops payload.json --queue "reckoning 2026-08-27"

    python 00-System/scripts/sheets.py doctor    # why can't THIS session reach the sheet
    python 00-System/scripts/sheets.py pending   # what is in the ledger but not the sheet
    python 00-System/scripts/sheets.py flush     # replay whatever an offline session queued
    python 00-System/scripts/sheets.py script    # Apps Script source, token filled in, to the clipboard

`ops` is the general form. Everything else is a shortcut onto it.

With `--queue LABEL`, a batch that cannot be delivered is parked in
06-Logs/automation/sheet-queue.jsonl instead of being lost, and the next session anywhere
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
QUEUE = os.path.join(REPO, "06-Logs", "automation", "sheet-queue.jsonl")
QUEUE_DONE = os.path.join(REPO, "06-Logs", "automation", "sheet-queue.done.jsonl")

# The Apps Script /exec URL 302s to script.googleusercontent.com, so both hosts
# have to be reachable. Neither is on the cloud "Trusted" default allowlist.
DOMAINS = ["script.google.com", "*.googleusercontent.com"]

FIX = """
This session cannot reach the budget sheet. Check, in order:
  1. Credentials: SHEETS_WEBAPP_URL and SHEETS_TOKEN must be set as Windows user
     variables. Samuel sets them himself with the one-line command in
     03-Areas/finances/budget-system.md -> "Credentials". Never paste them in chat.
  2. Network: the POST goes to script.google.com and redirects to
     *.googleusercontent.com. Both must be reachable.
  3. Token: if the web app rejects the request, the token in the Apps Script and
     the user variable differ. Change both, then Deploy -> Manage deployments ->
     New version.
Until it works, send batches with --queue so nothing is lost.
"""


KEYS = ("SHEETS_WEBAPP_URL", "SHEETS_TOKEN", "SHEETS_ID")


def _user_vars():
    """Windows user variables, read live from the registry, so a value Samuel
    sets after this app started is still seen without a restart."""
    out = {}
    try:
        import winreg
    except ImportError:
        return out
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            for k in KEYS:
                try:
                    out[k] = str(winreg.QueryValueEx(key, k)[0]).strip()
                except OSError:
                    pass
    except OSError:
        pass
    return out


def load_env():
    cfg = _user_vars()
    for k in KEYS:
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
# the ranges written by 08-Archive/accountability-engine/tools/sheets/build_budget.py.
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
                "ranges in 08-Archive/accountability-engine/tools/sheets/build_budget.py and re-run it before trusting any\n"
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
    print("Commit 06-Logs/automation/sheet-queue*.jsonl before this session ends.")
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
    print("Run: python 00-System/scripts/sheets.py flush")
    return 1


def doctor():
    """Say, in order, which link in the chain is broken and what to do about it."""
    cfg = load_env()
    reg = [k for k in ("SHEETS_WEBAPP_URL", "SHEETS_TOKEN") if _user_vars().get(k)]
    from_env = [k for k in ("SHEETS_WEBAPP_URL", "SHEETS_TOKEN") if os.environ.get(k)]

    print("user vars  : %s" % (", ".join(reg) if reg else "none set"))
    print("process env: %s" % (", ".join(from_env) if from_env else "none set"))

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
            "queued     : %d batch(es) waiting. Run: python 00-System/scripts/sheets.py flush"
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
        # Apps Script source with the real token substituted in, for pasting into
        # the Apps Script editor. Straight to the clipboard, never to stdout, so
        # the token never lands in a transcript. The committed file keeps a
        # placeholder so the token never enters git history.
        cfg = load_env()
        if not cfg.get("SHEETS_TOKEN"):
            die("SHEETS_TOKEN is not set as a user variable.")
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheets-apps-script.gs")
        with open(src, encoding="utf-8") as fh:
            body = fh.read()
        if "__SHEETS_TOKEN__" not in body:
            die("sheets-apps-script.gs has no __SHEETS_TOKEN__ placeholder — refusing to use it")
        import subprocess
        subprocess.run("clip", input=body.replace("__SHEETS_TOKEN__", cfg["SHEETS_TOKEN"]).encode("utf-16"), check=True)
        print("Apps Script source copied to the clipboard. Paste it in the editor, then clear the clipboard.")

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
                print("    python 00-System/scripts/sheets.py flush")
                print("Commit 06-Logs/automation/sheet-queue.jsonl before this session ends.")
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
