#!/usr/bin/env python3
"""
Builds Samuel's "Money" Google Sheet from the Brain. The sheet is a VIEW:
Samuel reads it, and every input goes through the finance agent into the
Brain. Each build rewrites the sheet completely from:

    03-Areas/finances/money-ledger.md   what actually moved (row types defined there)
    03-Areas/finances/obligations.md    the plan: one line per monthly item, and its payday
    GOALS below                         copied from 03-Areas/finances/finances-goals.md

Two tabs, headers + numbers only, no text in cells (Samuel, 2026-09-22):
    Overview  - where the money is · goals · plan vs actual for the month · months
    Ledger    - every ledger row: date, type, amount, what, category

    python 00-System/scripts/budget_sheet.py preview   # print the tables; touches nothing
    python 00-System/scripts/budget_sheet.py doctor    # key file, robot email, can it open the sheet
    python 00-System/scripts/budget_sheet.py build     # rewrite the sheet from the Brain

Talks to Google's official Sheets API as a service account. The key file lives
OUTSIDE the Brain, at %USERPROFILE%\\.brain-secrets\\budget-sheet-key.json (or the
path in BUDGET_SHEET_KEY). This script reads it; nothing prints it.
Needs: pip install google-auth requests
"""

import datetime as dt
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import money_ledger as ml  # noqa: E402

# The "Money" sheet. Its ID is not secret; only the key file is.
SHEET_ID = os.environ.get("BUDGET_SHEET_ID") or "1fqdIK2ty48eMJ2-6fH4ovPg0QY-MMhqTDWrnpyiKG5U"
KEY = os.environ.get("BUDGET_SHEET_KEY") or os.path.join(
    os.path.expanduser("~"), ".brain-secrets", "budget-sheet-key.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
API = "https://sheets.googleapis.com/v4/spreadsheets/"

OBLIGATIONS = os.path.join(ml.BRAIN, "03-Areas", "finances", "obligations.md")

# The live ledger's first full month. September 2026 is split with the archived
# engine ledger, so its plan-vs-actual lives in the September close, not here.
LIVE_FROM = "2026-10"

# From finances-goals.md (Samuel, confirmed 2026-09-20). Change there first.
GOALS = [
    # name, target NGN, starts, deadline, pots that count as saved
    ("Goal 1 — house", 1_000_000, None, dt.date(2026, 12, 31), ("Goal 1", "Emergency fund")),
    ("Goal 2 — marriage", 3_000_000, dt.date(2027, 1, 1), dt.date(2027, 7, 31), ("Goal 2",)),
    ("Emergency fund", 300_000, dt.date(2027, 1, 1), None, ("Emergency fund",)),
    ("Buffer", 200_000, None, None, ("Buffer",)),
]
# Pot lines in the plan, and the rule that fixes their amount.
POT_PLAN = [
    ("Cowrywise investment", "A", 100_000),  # Rule 7
    ("Goal 1", "B", None),                   # set each month in the budget
    ("Buffer", "B", 50_000),                 # Rule 8
]
COUNTS_TOWARD_GOAL_1 = ("Goal 1", "Emergency fund")
TABS = ("Overview", "Ledger")
OLD_SHEET_TABS = {"Dashboard", "Setup", "Details", "Budget"}  # refuse to touch the old sheet


# ---------------------------------------------------------------- the numbers

def month_of(d):
    return d[:7]


def plan_lines():
    """[(line, payday, amount)] from the obligations table, bold total rows skipped."""
    rows = ml.table_rows(OBLIGATIONS, "Item")
    out = []
    for r in rows:
        item = r.get("Item", "")
        if not item or item.startswith("**"):
            continue
        if item.lower().startswith("investment contribution"):
            continue  # it is the Cowrywise pot line below
        out.append((item, r.get("Payday", ""), ml.ngn(r.get("Amount", "")) or 0))
    for pot, payday, amount in POT_PLAN:
        out.append((pot, payday, amount))
    return out


def balances():
    """Pot balances and the derived bank, as of the last ledger row (same maths as money_ledger.pots)."""
    rows = ml.ledger()
    bal = {p: 0.0 for p in ml.POTS}
    bank = 0.0
    for r in rows:
        t, amt, what, cat = r["Type"], ml.ngn(r["NGN"]), r["What"], r["Category"]
        if amt is None:
            continue
        if t in ("opening", "balance"):
            if what in ml.POTS:
                bal[what] = amt
            else:
                bank = amt
        elif t == "in":
            bank += amt
        elif t in ml.OUT_TYPES:
            bank -= amt
        elif t == "to-pot":
            bal[cat] = bal.get(cat, 0) + amt
            bank -= amt
        elif t == "from-pot":
            bal[cat] = bal.get(cat, 0) - amt
            bank += amt
    as_of = rows[-1]["Date"][:10] if rows else ""
    return as_of, bank, bal


def actuals(month):
    """NGN moved per plan line in a month. Unknown categories fall into Other."""
    out = {}
    for r in ml.ledger():
        if month_of(r["Date"]) != month or r["Type"] not in ("major", "bulk", "charges", "to-pot"):
            continue
        amt = ml.ngn(r["NGN"])
        if amt is None:
            continue
        key = r["Category"] or "Other"
        out[key] = out.get(key, 0) + amt
    return out


def months_rows():
    by = {}
    for r in ml.ledger():
        m = month_of(r["Date"])
        if m < LIVE_FROM or r["Type"] in ("opening", "balance", "correction"):
            continue
        amt = ml.ngn(r["NGN"])
        if amt is None:
            continue
        row = by.setdefault(m, {"in": 0, "spent": 0, "to": 0, "from": 0})
        if r["Type"] == "in":
            row["in"] += amt
        elif r["Type"] in ml.OUT_TYPES:
            row["spent"] += amt
        elif r["Type"] == "to-pot":
            row["to"] += amt
        elif r["Type"] == "from-pot":
            row["from"] += amt
    return [[m, v["in"], v["spent"], v["to"], v["from"], v["in"] - v["spent"] - v["to"] + v["from"]]
            for m, v in sorted(by.items())]


def months_left(today, start, deadline):
    """A goal already running counts from today, in fractions. A goal that
    starts later counts whole calendar months, start to deadline inclusive
    (Goal 2: Jan-Jul 2027 = 7, as in finances-goals.md)."""
    if not deadline:
        return None
    if start and start > today:
        return (deadline.year - start.year) * 12 + deadline.month - start.month + 1
    return max((deadline - today).days, 0) / (365.25 / 12)


def overview(today=None):
    """The Overview tab as blocks: (header_row, [rows]). Numbers stay numbers."""
    today = today or dt.date.today()
    as_of, bank, bal = balances()
    plan_month = max(today.strftime("%Y-%m"), LIVE_FROM)

    where = [["Bank", bank, "No"]] + [
        [p, bal.get(p, 0), "Yes" if p in COUNTS_TOWARD_GOAL_1 else "No"]
        for p in ("Goal 1", "Emergency fund", "Buffer", "Cowrywise investment")]
    where.append(["Saved toward Goal 1", sum(bal.get(p, 0) for p in COUNTS_TOWARD_GOAL_1), ""])

    goals = []
    for name, target, start, deadline, pots in GOALS:
        saved = sum(bal.get(p, 0) for p in pots)
        left = max(target - saved, 0)
        ml_ = months_left(today, start, deadline)
        per_month = round(left / ml_) if ml_ else ""
        goals.append([name, target, saved, left,
                      start.isoformat() if start else "",
                      deadline.isoformat() if deadline else "",
                      round(ml_, 1) if ml_ is not None else "", per_month])

    act = actuals(plan_month)
    plan = []
    known = set()
    for line, payday, amount in plan_lines():
        known.add(line)
        a = act.get(line, 0)
        plan.append([line, payday, amount if amount is not None else "", a,
                     (amount - a) if amount is not None else ""])
    other = sum(v for k, v in act.items() if k not in known)
    plan.append(["Other", "", "", other, ""])
    plan.append(["Total", "", sum(r[2] for r in plan if r[2] != ""), sum(r[3] for r in plan),
                 sum(r[4] for r in plan if r[4] != "")])

    return as_of, plan_month, [
        (["As of", "Plan month"], [[as_of, plan_month]]),
        (["Where the money is", "Balance (NGN)", "Counts toward Goal 1"], where),
        (["Goal", "Target (NGN)", "Saved (NGN)", "Still to find (NGN)", "Starts", "Deadline",
          "Months left", "Needed per month (NGN)"], goals),
        (["Plan " + plan_month, "Payday", "Planned (NGN)", "Actual (NGN)", "Left (NGN)"], plan),
        (["Month", "In (NGN)", "Spent (NGN)", "To pots (NGN)", "From pots (NGN)", "Left over (NGN)"],
         months_rows()),
    ]


def ledger_tab():
    header = ["Date", "Type", "Amount (NGN)", "What", "Category"]
    rows = [[r["Date"], r["Type"], ml.ngn(r["NGN"]) if ml.ngn(r["NGN"]) is not None else "",
             r["What"], r["Category"] if r["Category"] not in ("—", "-") else ""]
            for r in ml.ledger()]
    return header, rows


# ---------------------------------------------------------------- preview

def fmt_cell(v):
    if isinstance(v, float) or isinstance(v, int):
        return "{:,.1f}".format(v) if isinstance(v, float) and v != int(v) else "{:,.0f}".format(v)
    return str(v)


def preview():
    as_of, plan_month, blocks = overview()
    print("=== Overview ===")
    for header, rows in blocks:
        print(" | ".join(header))
        for r in rows:
            print(" | ".join(fmt_cell(c) for c in r))
        print()
    print("=== Ledger ===")
    header, rows = ledger_tab()
    print(" | ".join(header))
    for r in rows:
        print(" | ".join(fmt_cell(c) for c in r))


# ---------------------------------------------------------------- the API

class Api:
    def __init__(self):
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import AuthorizedSession
        except ImportError:
            sys.exit("Missing library. Run: pip install google-auth requests")
        if not os.path.exists(KEY):
            sys.exit("No key file at %s. Setup: 03-Areas/finances/budget-system.md -> Credentials." % KEY)
        if not SHEET_ID:
            sys.exit("BUDGET_SHEET_ID is not set. Setup: 03-Areas/finances/budget-system.md -> Credentials.")
        creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
        self.email = creds.service_account_email
        self.s = AuthorizedSession(creds)

    def call(self, method, path, **kw):
        for wait in (2, 5, 10, None):
            r = self.s.request(method, API + SHEET_ID + path, timeout=60, **kw)
            if r.status_code < 400:
                return r.json() if r.content else {}
            if wait is None or r.status_code not in (429, 500, 502, 503, 504):
                raise SystemExit("Sheets API %s: %s" % (r.status_code, r.text[:500]))
            time.sleep(wait)


def doctor():
    print("key file   : %s" % ("found" if os.path.exists(KEY) else "MISSING at " + KEY))
    print("sheet id   : %s" % ("set" if SHEET_ID else "NOT SET"))
    api = Api()
    print("robot      : %s" % api.email)
    meta = api.call("GET", "?fields=properties.title,sheets.properties.title")
    tabs = [s["properties"]["title"] for s in meta.get("sheets", [])]
    print("verdict    : OK — opened %r, tabs: %s" % (meta["properties"]["title"], ", ".join(tabs)))


def rgb(h):
    h = h.lstrip("#")
    return {"red": int(h[0:2], 16) / 255, "green": int(h[2:4], 16) / 255, "blue": int(h[4:6], 16) / 255}


HEADER_FMT = {"textFormat": {"bold": True}, "backgroundColor": rgb("#E8EAED")}


def build():
    api = Api()
    meta = api.call("GET", "?fields=sheets.properties")
    have = {s["properties"]["title"]: s["properties"]["sheetId"] for s in meta["sheets"]}
    if OLD_SHEET_TABS & set(have):
        sys.exit("This looks like the old 'My Claude Budget' sheet (tabs %s). Refusing to rebuild it."
                 % ", ".join(sorted(OLD_SHEET_TABS & set(have))))

    # Tabs: add what is missing, then drop anything else. The robot owns this sheet's layout.
    reqs = [{"addSheet": {"properties": {"title": t}}} for t in TABS if t not in have]
    if reqs:
        api.call("POST", ":batchUpdate", json={"requests": reqs})
        meta = api.call("GET", "?fields=sheets.properties")
        have = {s["properties"]["title"]: s["properties"]["sheetId"] for s in meta["sheets"]}
    extra = [sid for t, sid in have.items() if t not in TABS]
    reqs = [{"deleteSheet": {"sheetId": sid}} for sid in extra]
    for i, t in enumerate(TABS):
        reqs.append({"updateSheetProperties": {"properties": {"sheetId": have[t], "index": i},
                                               "fields": "index"}})
    # Wipe values and formatting, so every build starts clean.
    for t in TABS:
        reqs.append({"updateCells": {"range": {"sheetId": have[t]}, "fields": "userEnteredValue,userEnteredFormat"}})
    api.call("POST", ":batchUpdate", json={"requests": reqs})

    as_of, plan_month, blocks = overview()
    values, fmt = [], []
    row = 0
    ov = have["Overview"]
    for header, rows in blocks:
        values.append(header)
        fmt.append({"repeatCell": {"range": {"sheetId": ov, "startRowIndex": row, "endRowIndex": row + 1,
                                             "startColumnIndex": 0, "endColumnIndex": len(header)},
                                   "cell": {"userEnteredFormat": HEADER_FMT},
                                   "fields": "userEnteredFormat(textFormat,backgroundColor)"}})
        for r in rows:
            values.append(r)
        if header[0] in ("Where the money is",) or header[0].startswith("Plan "):
            last = row + len(rows)  # bold the total row
            fmt.append({"repeatCell": {"range": {"sheetId": ov, "startRowIndex": last, "endRowIndex": last + 1},
                                       "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
                                       "fields": "userEnteredFormat.textFormat.bold"}})
        values.append([])
        row += len(rows) + 2

    lh, lrows = ledger_tab()
    le = have["Ledger"]
    api.call("POST", "/values:batchUpdate", json={
        "valueInputOption": "RAW",
        "data": [{"range": "Overview!A1", "values": values},
                 {"range": "Ledger!A1", "values": [lh] + lrows}]})

    num = {"numberFormat": {"type": "NUMBER", "pattern": "#,##0;[Red]-#,##0"}}  # red when negative, never blocks
    fmt += [
        {"repeatCell": {"range": {"sheetId": ov, "startColumnIndex": 1, "endColumnIndex": 8},
                        "cell": {"userEnteredFormat": num}, "fields": "userEnteredFormat.numberFormat"}},
        {"repeatCell": {"range": {"sheetId": le, "startColumnIndex": 2, "endColumnIndex": 3},
                        "cell": {"userEnteredFormat": num}, "fields": "userEnteredFormat.numberFormat"}},
        {"repeatCell": {"range": {"sheetId": le, "startRowIndex": 0, "endRowIndex": 1},
                        "cell": {"userEnteredFormat": HEADER_FMT},
                        "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
        {"updateSheetProperties": {"properties": {"sheetId": le, "gridProperties": {"frozenRowCount": 1}},
                                   "fields": "gridProperties.frozenRowCount"}},
    ]
    # Months left keeps one decimal.
    goal_row = next(i for i, v in enumerate(values) if v and v[0] == "Goal")
    fmt.append({"repeatCell": {"range": {"sheetId": ov, "startRowIndex": goal_row + 1,
                                         "endRowIndex": goal_row + 1 + len(GOALS),
                                         "startColumnIndex": 6, "endColumnIndex": 7},
                               "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "0.0"}}},
                               "fields": "userEnteredFormat.numberFormat"}})
    for sid in (ov, le):
        fmt.append({"autoResizeDimensions": {"dimensions": {"sheetId": sid, "dimension": "COLUMNS",
                                                            "startIndex": 0, "endIndex": 8}}})
    api.call("POST", ":batchUpdate", json={"requests": fmt})
    print("built: Overview (as of %s, plan %s) and Ledger (%d rows)" % (as_of, plan_month, len(lrows)))


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    cmd = argv[0] if argv else ""
    if cmd == "preview":
        preview()
    elif cmd == "doctor":
        doctor()
    elif cmd == "build":
        build()
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
