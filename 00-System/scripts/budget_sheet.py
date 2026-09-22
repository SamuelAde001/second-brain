#!/usr/bin/env python3
"""
Builds Samuel's "Money" Google Sheet from the Brain. The sheet is a VIEW:
Samuel reads it, and every input goes through the finance agent into the
Brain. The finance agent owns the sheet's layout and look too (Samuel,
2026-09-22). Each build rewrites every tab from:

    03-Areas/finances/money-ledger.md          what actually moved (row types defined there)
    03-Areas/finances/obligations.md           the live plan: one line per monthly item, and its payday
    03-Areas/finances/plans/plan-YYYY-MM.md    a closed month's plan, frozen at its close
    GOALS below                                copied from 03-Areas/finances/finances-goals.md

Tabs, in order:
    Overview     where the money is · goals · this month · plan vs actual · every month
    <Mon YYYY>   one per month from 2026-10, newest first: totals, plan vs actual, entries
    Ledger       every ledger row

Styling (Samuel, 2026-09-22): a big title, a coloured band per section, boxed
tables, colour-coded numbers. Headers, rows and numbers only; no sentences.

    python 00-System/scripts/budget_sheet.py preview            # print the tables; touches nothing
    python 00-System/scripts/budget_sheet.py doctor             # key file, robot email, can it open the sheet
    python 00-System/scripts/budget_sheet.py build              # rewrite the sheet from the Brain
    python 00-System/scripts/budget_sheet.py snapshot 2026-10   # freeze a month's plan (at its close)

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

FIN = os.path.join(ml.BRAIN, "03-Areas", "finances")
OBLIGATIONS = os.path.join(FIN, "obligations.md")
PLANS = os.path.join(FIN, "plans")

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
OLD_SHEET_TABS = {"Dashboard", "Setup", "Details", "Budget"}  # refuse to touch the old sheet


# ================================================================ the numbers

def month_of(d):
    return d[:7]


def month_label(m, short=False):
    return dt.date(int(m[:4]), int(m[5:7]), 1).strftime("%b %Y" if short else "%B %Y")


def next_month(m):
    y, mo = int(m[:4]), int(m[5:7]) + 1
    return "%04d-%02d" % (y + (mo > 12), mo - 12 if mo > 12 else mo)


def live_plan():
    """[(line, payday, amount)] from the obligations table, bold total rows skipped."""
    out = []
    for r in ml.table_rows(OBLIGATIONS, "Item"):
        item = r.get("Item", "")
        if not item or item.startswith("**") or item.lower().startswith("investment contribution"):
            continue  # totals, and the investment row, which is the Cowrywise pot line below
        out.append((item, r.get("Payday", ""), ml.ngn(r.get("Amount", "")) or 0))
    return out + list(POT_PLAN)


def snapshot_path(month):
    return os.path.join(PLANS, "plan-%s.md" % month)


def plan_for(month):
    """A closed month reads its frozen plan; the running month reads the live one."""
    p = snapshot_path(month)
    if os.path.exists(p):
        return [(r["Line"], r["Payday"], ml.ngn(r["Planned NGN"])) for r in ml.table_rows(p, "Line")]
    return live_plan()


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


def entries(month):
    return [r for r in ml.ledger() if month_of(r["Date"]) == month]


def totals(month):
    t = {"in": 0, "spent": 0, "to": 0, "from": 0}
    for r in entries(month):
        amt = ml.ngn(r["NGN"])
        if amt is None:
            continue
        if r["Type"] == "in":
            t["in"] += amt
        elif r["Type"] in ml.OUT_TYPES:
            t["spent"] += amt
        elif r["Type"] == "to-pot":
            t["to"] += amt
        elif r["Type"] == "from-pot":
            t["from"] += amt
    t["left"] = t["in"] - t["spent"] - t["to"] + t["from"]
    return t


def plan_vs_actual(month):
    act = {}
    for r in entries(month):
        if r["Type"] not in ("major", "bulk", "charges", "to-pot"):
            continue
        amt = ml.ngn(r["NGN"])
        if amt is not None:
            key = r["Category"] or "Other"
            act[key] = act.get(key, 0) + amt
    rows, known = [], set()
    for line, payday, amount in plan_for(month):
        known.add(line)
        a = act.get(line, 0)
        rows.append([line, payday, "" if amount is None else amount, a, "" if amount is None else amount - a])
    rows.append(["Other", "", "", sum(v for k, v in act.items() if k not in known), ""])
    rows.append(["Total", "", sum(r[2] for r in rows if r[2] != ""), sum(r[3] for r in rows),
                 sum(r[4] for r in rows if r[4] != "")])
    return rows


def plan_month(today=None):
    return max((today or dt.date.today()).strftime("%Y-%m"), LIVE_FROM)


def months(today=None):
    """Every month that gets a tab: LIVE_FROM up to the plan month, plus any later ledger month."""
    last = max([plan_month(today)] + [month_of(r["Date"]) for r in ml.ledger()])
    out, m = [], LIVE_FROM
    while m <= last:
        out.append(m)
        m = next_month(m)
    return out


def months_left(today, start, deadline):
    """A goal already running counts from today, in fractions. A goal that
    starts later counts whole calendar months, start to deadline inclusive
    (Goal 2: Jan-Jul 2027 = 7, as in finances-goals.md)."""
    if not deadline:
        return None
    if start and start > today:
        return (deadline.year - start.year) * 12 + deadline.month - start.month + 1
    return max((deadline - today).days, 0) / (365.25 / 12)


def bar(p):
    n = max(0, min(10, round(p * 10)))
    return "█" * n + "░" * (10 - n) + "  {:.0%}".format(p)


def goal_rows(bal, today):
    rows = []
    for name, target, start, deadline, pots in GOALS:
        saved = sum(bal.get(p, 0) for p in pots)
        left = max(target - saved, 0)
        ml_ = months_left(today, start, deadline)
        rows.append([name, target, saved, left, bar(saved / target if target else 0),
                     start.isoformat() if start else "", deadline.isoformat() if deadline else "",
                     round(ml_, 1) if ml_ is not None else "", round(left / ml_) if ml_ else ""])
    return rows


def where_rows(bank, bal):
    rows = [["Bank", bank, "No"]] + [[p, bal.get(p, 0), "Yes" if p in COUNTS_TOWARD_GOAL_1 else "No"]
                                      for p in ("Goal 1", "Emergency fund", "Buffer", "Cowrywise investment")]
    rows.append(["Saved toward Goal 1", sum(bal.get(p, 0) for p in COUNTS_TOWARD_GOAL_1), ""])
    return rows


def entry_rows(rows):
    return [[r["Date"], r["Type"], ml.ngn(r["NGN"]) if ml.ngn(r["NGN"]) is not None else "",
             r["What"], r["Category"] if r["Category"] not in ("—", "-") else ""] for r in rows]


# ================================================================ snapshot

def snapshot(month):
    p = snapshot_path(month)
    if os.path.exists(p):
        sys.exit("%s already exists. A frozen plan is never rewritten; correct it with a dated note under its table."
                 % os.path.relpath(p, ml.BRAIN))
    os.makedirs(PLANS, exist_ok=True)
    today = dt.date.today().isoformat()
    lines = ["---", "type: log", "area: finances", "status: done", "updated: " + today, "source: manual",
             "tags: [plan, budget]", "---", "", "# Plan — " + month_label(month), "",
             "The plan for %s as it stood on %s, frozen by `budget_sheet.py snapshot`. Never rewritten. "
             "The live plan is [[obligations]]." % (month_label(month), today), "",
             "| Line | Payday | Planned NGN |", "|---|---|---|"]
    for line, payday, amount in live_plan():
        lines.append("| %s | %s | %s |" % (line, payday, "—" if amount is None else "{:,.0f}".format(amount)))
    lines += ["", "Back to [[03-Areas/finances/finances|Finances]]", ""]
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print("froze the plan for %s -> %s" % (month, os.path.relpath(p, ml.BRAIN)))


# ================================================================ preview

def fmt_cell(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return "{:,.1f}".format(v) if isinstance(v, float) and v != int(v) else "{:,.0f}".format(v)
    return str(v)


def show(title, header, rows):
    print("-- " + title)
    print(" | ".join(header))
    for r in rows:
        print(" | ".join(fmt_cell(c) for c in r))
    print()


def preview():
    today = dt.date.today()
    as_of, bank, bal = balances()
    pm = plan_month(today)
    print("=== Overview (as of %s, plan month %s) ===" % (as_of, pm))
    show("Where the money is", H_WHERE, where_rows(bank, bal))
    show("Goals", H_GOALS, goal_rows(bal, today))
    t = totals(pm)
    show("This month", H_KPI, [[t["in"], t["spent"], t["to"], t["from"], t["left"]]])
    show("Plan vs actual " + pm, H_PLAN, plan_vs_actual(pm))
    for m in reversed(months(today)):
        t = totals(m)
        print("=== %s ===" % month_label(m, short=True))
        show("The month in numbers", H_KPI, [[t["in"], t["spent"], t["to"], t["from"], t["left"]]])
        show("Plan vs actual", H_PLAN, plan_vs_actual(m))
        show("Every entry", H_ENTRY, entry_rows(entries(m)))
    print("=== Ledger ===")
    show("Every entry", H_ENTRY, entry_rows(ml.ledger()))


# ================================================================ the look

H_WHERE = ["Account / pot", "Balance (NGN)", "Counts toward Goal 1"]
H_GOALS = ["Goal", "Target (NGN)", "Saved (NGN)", "Still to find (NGN)", "Progress", "Starts", "Deadline",
           "Months left", "Needed / month (NGN)"]
H_KPI = ["In (NGN)", "Spent (NGN)", "To pots (NGN)", "From pots (NGN)", "Left over (NGN)"]
H_PLAN = ["Line", "Payday", "Planned (NGN)", "Actual (NGN)", "Left (NGN)"]
H_MONTHS = ["Month", "In (NGN)", "Spent (NGN)", "To pots (NGN)", "From pots (NGN)", "Left over (NGN)"]
H_ENTRY = ["Date", "Type", "Amount (NGN)", "What", "Category"]

INK, MUTED, WHITE, ZEBRA, LINE = "#0F172A", "#64748B", "#FFFFFF", "#F8FAFC", "#E2E8F0"
TITLE, SUBTITLE = "#1E293B", "#334155"
GREEN, RED, BLUE, ORANGE, VIOLET, AMBER = "#15803D", "#B91C1C", "#1D4ED8", "#C2410C", "#6D28D9", "#B45309"
RED_BG = "#FEE2E2"
# (band colour, header tint) per section
MONEY = ("#0F766E", "#CCFBF1")
GOALS_C = ("#6D28D9", "#EDE9FE")
KPI_C = ("#4338CA", "#E0E7FF")
PLAN_C = ("#1D4ED8", "#DBEAFE")
MONTHS_C = ("#B45309", "#FEF3C7")
LEDGER_C = ("#334155", "#E2E8F0")
TAB_COLOUR = {"Overview": TITLE, "Ledger": LEDGER_C[0]}
TYPE_COLOUR = {"in": GREEN, "major": RED, "bulk": RED, "charges": "#9F1239", "to-pot": BLUE,
               "from-pot": ORANGE, "opening": MUTED, "balance": MUTED, "correction": AMBER}
NGN_FMT = "#,##0;[Red]-#,##0"


def rgb(h):
    h = h.lstrip("#")
    return {"red": int(h[0:2], 16) / 255, "green": int(h[2:4], 16) / 255, "blue": int(h[4:6], 16) / 255}


def rng(sid, r0, r1, c0, c1):
    return {"sheetId": sid, "startRowIndex": r0, "endRowIndex": r1, "startColumnIndex": c0, "endColumnIndex": c1}


def cell(v=None, bg=None, fg=None, bold=False, size=10, align=None, num=None, link=None):
    d = {}
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        d["userEnteredValue"] = {"numberValue": v}
    elif v not in (None, ""):
        d["userEnteredValue"] = {"stringValue": str(v)}
    tf = {"bold": bold, "fontSize": size, "foregroundColor": rgb(fg or INK)}
    if link:
        tf["link"] = {"uri": link}
        tf["underline"] = True
    f = {"textFormat": tf, "verticalAlignment": "MIDDLE", "wrapStrategy": "CLIP",
         "padding": {"left": 8, "right": 8, "top": 2, "bottom": 2}}
    if bg:
        f["backgroundColor"] = rgb(bg)
    if align:
        f["horizontalAlignment"] = align
    if num:
        f["numberFormat"] = {"type": "NUMBER", "pattern": num}
    d["userEnteredFormat"] = f
    return d


class Page:
    """One tab: a grid of cells with their formats, plus merges, heights and borders."""

    def __init__(self, sid, widths):
        self.sid, self.widths = sid, widths
        self.grid, self.reqs = [], []

    def row(self, cells, height=None):
        r = len(self.grid)
        self.grid.append(cells)
        if height:
            self.reqs.append({"updateDimensionProperties": {
                "range": {"sheetId": self.sid, "dimension": "ROWS", "startIndex": r, "endIndex": r + 1},
                "properties": {"pixelSize": height}, "fields": "pixelSize"}})
        return r

    def banner(self, text, bg, span, size=22, height=54, fg=WHITE, bold=True):
        r = self.row([cell(text, bg=bg, fg=fg, bold=bold, size=size)] + [cell(bg=bg) for _ in range(span - 1)], height)
        self.reqs.append({"mergeCells": {"range": rng(self.sid, r, r + 1, 0, span), "mergeType": "MERGE_ALL"}})

    def title(self, text, sub, span):
        self.banner(text, TITLE, span)
        self.banner(sub, SUBTITLE, span, size=10, height=26, fg="#CBD5E1", bold=False)
        self.gap()

    def gap(self, h=18):
        self.row([], h)

    def box(self, title, colour, header, rows, style=None, nums=None, total=False, big=False):
        """A section: a coloured band, a tinted header row, zebra rows, a border around it all."""
        main, tint = colour
        span, nums = len(header), nums or {}
        r0 = len(self.grid)
        self.banner(title.upper(), main, span, size=12, height=32)
        aligns = ["RIGHT" if j in nums else ("CENTER" if j and not nums.get(j) and header[j] in ("Payday", "Type", "Counts toward Goal 1", "Starts", "Deadline") else "LEFT")
                  for j in range(span)]
        if big:
            aligns = ["CENTER"] * span
        self.row([cell(h, bg=tint, fg=main, bold=True, align=aligns[j]) for j, h in enumerate(header)], 28)
        if not rows:
            rows = [["—"] + [""] * (span - 1)]
        for i, row in enumerate(rows):
            last = total and i == len(rows) - 1
            bg = tint if last else (ZEBRA if i % 2 else WHITE)
            cells = []
            for j in range(span):
                v = row[j] if j < len(row) else ""
                kw = {"bg": bg, "bold": last or big, "align": aligns[j], "num": nums.get(j),
                      "size": 14 if big else 10}
                if style:
                    kw.update(style(i, j, v, row) or {})
                cells.append(cell(v, **kw))
            self.row(cells, 40 if big else 26)
        solid = {"style": "SOLID_MEDIUM", "color": rgb(main)}
        self.reqs.append({"updateBorders": {"range": rng(self.sid, r0, len(self.grid), 0, span),
                                            "top": solid, "bottom": solid, "left": solid, "right": solid,
                                            "innerHorizontal": {"style": "SOLID", "color": rgb(LINE)}}})
        self.gap()

    def requests(self):
        out = [{"updateCells": {"start": {"sheetId": self.sid, "rowIndex": 0, "columnIndex": 0},
                                "rows": [{"values": r} for r in self.grid],
                                "fields": "userEnteredValue,userEnteredFormat"}}]
        for j, w in enumerate(self.widths):
            out.append({"updateDimensionProperties": {
                "range": {"sheetId": self.sid, "dimension": "COLUMNS", "startIndex": j, "endIndex": j + 1},
                "properties": {"pixelSize": w}, "fields": "pixelSize"}})
        return out + self.reqs


# ---- colour rules per section

def style_where(i, j, v, row):
    if j == 1:
        return {"fg": INK if row[0] == "Bank" else MONEY[0], "bold": True}
    if j == 2 and v:
        return {"fg": GREEN if v == "Yes" else MUTED, "bold": v == "Yes"}


def style_goals(i, j, v, row):
    return {2: {"fg": GREEN}, 3: {"fg": ORANGE}, 4: {"fg": VIOLET, "bold": True},
            8: {"fg": VIOLET, "bold": True}}.get(j)


def style_kpi(i, j, v, row):
    colour = [GREEN, RED, BLUE, ORANGE, GREEN if (isinstance(v, (int, float)) and v >= 0) else RED][j]
    return {"fg": colour, "align": "CENTER"}


def style_plan(i, j, v, row):
    if j == 1 and v:
        return {"fg": BLUE if v == "A" else (VIOLET if v == "B" else MUTED), "bold": True}
    if j == 3 and isinstance(v, (int, float)) and v:
        return {"fg": BLUE, "bold": True}
    if j == 4 and isinstance(v, (int, float)) and v < 0:
        return {"fg": RED, "bg": RED_BG, "bold": True}
    if row[0] == "Other" and j == 0:
        return {"fg": MUTED}


def style_months(i, j, v, row):
    if j == 0:
        return {"fg": AMBER, "bold": True}
    return {1: {"fg": GREEN}, 2: {"fg": RED}, 3: {"fg": BLUE}, 4: {"fg": ORANGE},
            5: {"fg": GREEN if isinstance(v, (int, float)) and v >= 0 else RED, "bold": True}}.get(j)


def style_entry(i, j, v, row):
    if j in (1, 2):
        return {"fg": TYPE_COLOUR.get(row[1], INK), "bold": j == 1}


PLAN_NUMS = {2: NGN_FMT, 3: NGN_FMT, 4: NGN_FMT}
KPI_NUMS = {j: NGN_FMT for j in range(5)}
ENTRY_NUMS = {2: NGN_FMT}


def paint_overview(page, today, gids):
    as_of, bank, bal = balances()
    pm = plan_month(today)
    page.title("MONEY", "As of %s   ·   Plan month %s" % (as_of, month_label(pm)), 9)
    page.box("Where the money is", MONEY, H_WHERE, where_rows(bank, bal), style_where,
             {1: NGN_FMT}, total=True)
    page.box("Goals", GOALS_C, H_GOALS, goal_rows(bal, today), style_goals,
             {1: NGN_FMT, 2: NGN_FMT, 3: NGN_FMT, 7: "0.0", 8: NGN_FMT})
    t = totals(pm)
    page.box("This month — " + month_label(pm), KPI_C, H_KPI,
             [[t["in"], t["spent"], t["to"], t["from"], t["left"]]], style_kpi, KPI_NUMS, big=True)
    page.box("Plan vs actual — " + month_label(pm), PLAN_C, H_PLAN, plan_vs_actual(pm), style_plan,
             PLAN_NUMS, total=True)
    rows = []
    for m in reversed(months(today)):
        t = totals(m)
        rows.append([month_label(m, short=True), t["in"], t["spent"], t["to"], t["from"], t["left"]])
    page.box("Every month", MONTHS_C, H_MONTHS, rows, style_months,
             {j: NGN_FMT for j in range(1, 6)})
    # Each month name links to its tab.
    for k, m in enumerate(reversed(months(today))):
        r = len(page.grid) - 1 - len(rows) + k  # rows sit just above the trailing gap
        page.grid[r][0] = cell(month_label(m, short=True), bg=ZEBRA if k % 2 else WHITE, fg=AMBER, bold=True,
                               link="#gid=%d" % gids[month_label(m, short=True)])


def paint_month(page, m):
    rows = entries(m)
    sub = ("%d entries   ·   last entry %s" % (len(rows), rows[-1]["Date"][:10])) if rows else "No entries yet"
    page.title(month_label(m).upper(), sub, 5)
    t = totals(m)
    page.box("The month in numbers", KPI_C, H_KPI, [[t["in"], t["spent"], t["to"], t["from"], t["left"]]],
             style_kpi, KPI_NUMS, big=True)
    page.box("Plan vs actual", PLAN_C, H_PLAN, plan_vs_actual(m), style_plan, PLAN_NUMS, total=True)
    page.box("Every entry", LEDGER_C, H_ENTRY, entry_rows(rows), style_entry, ENTRY_NUMS)


def paint_ledger(page):
    rows = ml.ledger()
    page.title("LEDGER", "%d entries   ·   oldest first" % len(rows), 5)
    page.box("Every entry", LEDGER_C, H_ENTRY, entry_rows(rows), style_entry, ENTRY_NUMS)


# ================================================================ the API

class Api:
    def __init__(self):
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import AuthorizedSession
        except ImportError:
            sys.exit("Missing library. Run: pip install google-auth requests")
        if not os.path.exists(KEY):
            sys.exit("No key file at %s. Setup: 03-Areas/finances/budget-system.md -> Credentials." % KEY)
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

    def tabs(self):
        meta = self.call("GET", "?fields=sheets.properties(sheetId,title)")
        return {s["properties"]["title"]: s["properties"]["sheetId"] for s in meta["sheets"]}


def doctor():
    print("key file   : %s" % ("found" if os.path.exists(KEY) else "MISSING at " + KEY))
    api = Api()
    print("robot      : %s" % api.email)
    meta = api.call("GET", "?fields=properties.title,sheets.properties.title")
    tabs = [s["properties"]["title"] for s in meta.get("sheets", [])]
    print("verdict    : OK — opened %r, tabs: %s" % (meta["properties"]["title"], ", ".join(tabs)))


def build():
    today = dt.date.today()
    api = Api()
    have = api.tabs()
    if OLD_SHEET_TABS & set(have):
        sys.exit("This looks like the old 'My Claude Budget' sheet (tabs %s). Refusing to rebuild it."
                 % ", ".join(sorted(OLD_SHEET_TABS & set(have))))

    ms = list(reversed(months(today)))  # newest first
    order = ["Overview"] + [month_label(m, short=True) for m in ms] + ["Ledger"]

    # Tabs: add what is missing, drop anything else, put them in order. The finance agent owns this layout.
    add = [{"addSheet": {"properties": {"title": t}}} for t in order if t not in have]
    if add:
        api.call("POST", ":batchUpdate", json={"requests": add})
        have = api.tabs()
    reqs = [{"deleteSheet": {"sheetId": sid}} for t, sid in have.items() if t not in order]
    for i, t in enumerate(order):
        colour = TAB_COLOUR.get(t, MONTHS_C[0])
        reqs.append({"updateSheetProperties": {
            "properties": {"sheetId": have[t], "index": i, "tabColor": rgb(colour),
                           "gridProperties": {"hideGridlines": True, "frozenRowCount": 0}},
            "fields": "index,tabColor,gridProperties.hideGridlines,gridProperties.frozenRowCount"}})
        # Start clean: no merges, no values, no formats, default row heights.
        reqs.append({"unmergeCells": {"range": {"sheetId": have[t]}}})
        reqs.append({"updateCells": {"range": {"sheetId": have[t]}, "fields": "userEnteredValue,userEnteredFormat"}})
        reqs.append({"updateDimensionProperties": {
            "range": {"sheetId": have[t], "dimension": "ROWS", "startIndex": 0, "endIndex": 1000},
            "properties": {"pixelSize": 21}, "fields": "pixelSize"}})
    api.call("POST", ":batchUpdate", json={"requests": reqs})

    paint = []
    ov = Page(have["Overview"], [230, 125, 170, 130, 170, 105, 105, 100, 150])
    paint_overview(ov, today, have)
    paint += ov.requests()
    for m in ms:
        pg = Page(have[month_label(m, short=True)], [230, 110, 130, 200, 200])
        paint_month(pg, m)
        paint += pg.requests()
    lg = Page(have["Ledger"], [110, 110, 130, 260, 200])
    paint_ledger(lg)
    paint += lg.requests()
    api.call("POST", ":batchUpdate", json={"requests": paint})
    print("built: %s" % ", ".join(order))


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
    elif cmd == "snapshot" and len(argv) == 2:
        snapshot(argv[1])
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
