#!/usr/bin/env python3
"""
Builds Samuel's "Money" Google Sheet from the Brain. The sheet is a VIEW:
Samuel reads it, and every input goes through the finance agent into the
Brain. The finance agent owns the sheet's layout and look too (Samuel,
2026-09-22). Each build rewrites every tab from:

    03-Areas/finances/money-ledger.md          what actually moved (row types defined there)
    03-Areas/finances/plans/plan-YYYY-MM.md    each month's plan; frozen (status: done) at its close
    03-Areas/finances/obligations.md           the standing plan, for a month with no plan file yet
    GOALS below                                copied from 03-Areas/finances/finances-goals.md

Tabs, in order:
    Overview     where the money is · goals · money flow · plan vs actual · subscriptions · every month
    <Mon YYYY>   one per month from 2026-09, newest first: money flow, plan vs actual, entries
    Ledger       every ledger row

Styling (Samuel, 2026-09-22): a big title, a coloured band per section, boxed
tables, colour-coded numbers. Headers, rows and numbers only; no sentences.

    python 00-System/scripts/budget_sheet.py preview            # print the tables; touches nothing
    python 00-System/scripts/budget_sheet.py doctor             # key file, robot email, can it open the sheet
    python 00-System/scripts/budget_sheet.py build              # rewrite the sheet from the Brain
    python 00-System/scripts/budget_sheet.py left               # what's left per line this month (spend checks)
    python 00-System/scripts/budget_sheet.py month-plan 2026-10 # start a month's plan from the standing plan
    python 00-System/scripts/budget_sheet.py freeze 2026-09     # at the close: the month's plan never changes again

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

# The first month with its own tab. September 2026 came into the live ledger
# from the archived one on 2026-09-22, at Samuel's request.
LIVE_FROM = "2026-09"

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
    """The standing plan: [(line, payday, amount)] from the obligations table, total rows skipped."""
    out = []
    for r in ml.table_rows(OBLIGATIONS, "Item"):
        item = r.get("Item", "")
        if not item or item.startswith("**") or item.lower().startswith("investment contribution"):
            continue  # totals, and the investment row, which is the Cowrywise pot line below
        out.append((item, r.get("Payday", ""), ml.ngn(r.get("Amount", "")) or 0))
    return out + list(POT_PLAN)


def plan_path(month):
    return os.path.join(PLANS, "plan-%s.md" % month)


def plan_for(month):
    """The month's own plan file if it has one; otherwise the standing plan."""
    p = plan_path(month)
    if os.path.exists(p):
        return [(r["Line"], r["Payday"], ml.ngn(r["Planned NGN"])) for r in ml.table_rows(p, "Line")]
    return live_plan()


def balances():
    as_of, bank, bal, mismatches = ml.position()
    for m in mismatches:
        print("CHECKPOINT MISMATCH: " + m)
    return as_of, bank or 0.0, {p: (v or 0.0) for p, v in bal.items()}


def shown(rows):
    """Rows a person reads: money only. Checkpoint openings and correction notes stay in the Brain."""
    opens = [r["Date"][:10] for r in rows if r["Type"] == "opening"]
    start = min(opens) if opens else None
    return [r for r in rows if r["Type"] != "correction" and not (r["Type"] == "opening" and r["Date"][:10] != start)]


def entries(month):
    return [r for r in shown(ml.ledger()) if month_of(r["Date"]) == month]


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
    # Spending on a line the plan never had shows as its own row, planned 0, so it can't hide in Other.
    for k in sorted(k for k in act if k not in known and k != "Other"):
        rows.append([k, "unplanned", 0, act[k], -act[k]])
    rows.append(["Other", "", "", act.get("Other", 0), ""])
    rows.append(["Total", "", sum(r[2] for r in rows if r[2] != ""), sum(r[3] for r in rows),
                 sum(r[4] for r in rows if r[4] != "")])
    return rows


def bank_at_start(month):
    return ml.position([r for r in ml.ledger() if r["Date"][:10] < month + "-01"])[1] or 0


def flow_rows(month):
    """Bank at the start + money in + taken from each pot − spent − into pots = bank at the end.
    Shows where an overspend was paid from, so over-plan never reads as a deficit (Samuel, 2026-09-22)."""
    start = bank_at_start(month)
    rows = [["Bank at the start", start]]
    t = totals(month)
    rows.append(["+ Money in", t["in"]])
    by_pot = {}
    for r in entries(month):
        if r["Type"] == "from-pot" and ml.ngn(r["NGN"]):
            by_pot[r["Category"]] = by_pot.get(r["Category"], 0) + ml.ngn(r["NGN"])
    for pot, amt in by_pot.items():
        rows.append(["+ From " + pot, amt])
    rows.append(["− Spent", t["spent"]])
    rows.append(["− Into pots", t["to"]])
    rows.append(["= Bank at the end", start + t["left"]])
    return rows


def subscription_rows(month):
    """The subscriptions table in obligations.md, with what was paid for each this month."""
    paid = {}
    for r in entries(month):
        if r["Category"] == "Subscriptions" and ml.ngn(r["NGN"]):
            key = r["What"].split()[0].lower()
            paid.setdefault(key, [0, ""])
            paid[key][0] += ml.ngn(r["NGN"])
            paid[key][1] = r["Date"][:10]
    rows = []
    for r in ml.table_rows(OBLIGATIONS, "Subscription"):
        name = r["Subscription"]
        if name.startswith("**"):
            continue
        amount = ml.ngn(r["NGN"]) or 0
        got, when = paid.get(name.split()[0].lower(), [0, ""])
        status = ("Paid " + when[5:]) if got >= amount and got else "Due " + r["Bills on"]
        rows.append([name, amount, r["Bills on"], got, status])
    rows.append(["Total", sum(x[1] for x in rows), "", sum(x[3] for x in rows), ""])
    return rows


def plan_month(today=None):
    return max((today or dt.date.today()).strftime("%Y-%m"), LIVE_FROM)


def months(today=None):
    """Every month that gets a tab: LIVE_FROM up to the plan month, plus any later month
    that already has ledger rows or a plan file."""
    planned = [f[5:12] for f in os.listdir(PLANS)] if os.path.isdir(PLANS) else []
    last = max([plan_month(today)] + [month_of(r["Date"]) for r in ml.ledger() if r["Type"] != "correction"] + planned)
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


# ================================================================ month plans

def month_plan(month, quiet=False):
    """Start a month's plan file from the standing plan. Never overwrites."""
    p = plan_path(month)
    if os.path.exists(p):
        if not quiet:
            print("%s already exists." % os.path.relpath(p, ml.BRAIN))
        return p
    os.makedirs(PLANS, exist_ok=True)
    today = dt.date.today().isoformat()
    lines = ["---", "type: log", "area: finances", "status: active", "updated: " + today, "source: manual",
             "tags: [plan, budget]", "---", "", "# Plan — " + month_label(month), "",
             "%s's budget, started %s from the standing plan in [[obligations]]. The `budget` skill changes it "
             "while the month runs and records each change below. Frozen at the month close (`status: done`)."
             % (month_label(month), today), "",
             "| Line | Payday | Planned NGN |", "|---|---|---|"]
    for line, payday, amount in live_plan():
        lines.append("| %s | %s | %s |" % (line, payday, "—" if amount is None else "{:,.0f}".format(amount)))
    lines += ["", "## Changes", "", "| Date | Line | From | To | Whose call |", "|---|---|---|---|---|", "",
              "Back to [[03-Areas/finances/finances|Finances]]", ""]
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print("started the plan for %s -> %s" % (month, os.path.relpath(p, ml.BRAIN)))
    return p


def freeze(month):
    """At the month close: mark the plan done. From then on it is never edited."""
    p = month_plan(month, quiet=True)
    s = open(p, encoding="utf-8").read()
    if "\nstatus: done\n" in s:
        print("%s is already frozen." % month)
        return
    s = s.replace("\nstatus: active\n", "\nstatus: done\n", 1)
    s = s.replace("\nupdated: ", "\nupdated: %s\nfrozen: " % dt.date.today().isoformat(), 1)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s)
    print("froze the plan for %s" % month)


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
    show("Money flow " + pm, H_FLOW, flow_rows(pm))
    show("Subscriptions " + pm, H_SUBS, subscription_rows(pm))
    show("Plan vs actual " + pm, H_PLAN, plan_vs_actual(pm))
    for m in reversed(months(today)):
        print("=== %s ===" % month_label(m, short=True))
        show("Money flow", H_FLOW, flow_rows(m))
        show("Plan vs actual", H_PLAN, plan_vs_actual(m))
        show("Every entry", H_ENTRY, entry_rows(entries(m)))
    print("=== Ledger ===")
    show("Every entry", H_ENTRY, entry_rows(ml.ledger()))


# ================================================================ the look

H_WHERE = ["Account / pot", "Balance (NGN)", "Counts toward Goal 1"]
H_GOALS = ["Goal", "Target (NGN)", "Saved (NGN)", "Still to find (NGN)", "Progress", "Starts", "Deadline",
           "Months left", "Needed / month (NGN)"]
H_PLAN = ["Line", "Payday", "Planned (NGN)", "Actual (NGN)", "Left (NGN)"]
H_MONTHS = ["Month", "Bank at start (NGN)", "Money in (NGN)", "From pots (NGN)", "Spent (NGN)",
            "Into pots (NGN)", "Bank at end (NGN)"]
H_ENTRY = ["Date", "Type", "Amount (NGN)", "What", "Category"]
H_SUBS = ["Subscription", "Amount (NGN)", "Bills on", "Paid (NGN)", "Status"]
H_FLOW = ["Where it came from, where it went", "NGN"]

INK, MUTED, WHITE, ZEBRA, LINE = "#0F172A", "#64748B", "#FFFFFF", "#F8FAFC", "#E2E8F0"
TITLE, SUBTITLE = "#1E293B", "#334155"
GREEN, RED, BLUE, ORANGE, VIOLET, AMBER = "#15803D", "#B91C1C", "#1D4ED8", "#C2410C", "#6D28D9", "#B45309"
RED_BG = "#FEE2E2"
# (band colour, header tint) per section
MONEY = ("#0F766E", "#CCFBF1")
GOALS_C = ("#6D28D9", "#EDE9FE")
FLOW_C = ("#15803D", "#DCFCE7")
SUBS_C = ("#BE185D", "#FCE7F3")
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
        aligns = ["RIGHT" if j in nums else ("CENTER" if j and not nums.get(j) and header[j] in ("Payday", "Type", "Counts toward Goal 1", "Starts", "Deadline", "Bills on", "Status") else "LEFT")
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


def style_flow(i, j, v, row):
    label = row[0]
    if label.startswith("+ Money"):
        return {"fg": GREEN}
    if label.startswith("+ From"):
        return {"fg": ORANGE, "bold": True}
    if label.startswith("− Spent"):
        return {"fg": RED}
    if label.startswith("− Into"):
        return {"fg": BLUE}
    if label.startswith("="):
        return {"fg": GREEN if isinstance(row[1], (int, float)) and row[1] >= 0 else RED}


def style_subs(i, j, v, row):
    if j == 4 and v:
        return {"fg": GREEN if v.startswith("Paid") else ORANGE, "bold": True, "align": "CENTER"}
    if j == 2:
        return {"align": "CENTER"}
    if j == 3 and isinstance(v, (int, float)) and v:
        return {"fg": GREEN if v >= row[1] else ORANGE}


def style_plan(i, j, v, row):
    if row[1] == "unplanned" and j in (0, 1):
        return {"fg": ORANGE, "bold": j == 1}
    if j == 1 and v:
        return {"fg": BLUE if v == "A" else (VIOLET if v == "B" else ("#4338CA" if v == "A+B" else MUTED)), "bold": True}
    if j == 3 and isinstance(v, (int, float)) and v:
        return {"fg": BLUE, "bold": True}
    if j == 4 and isinstance(v, (int, float)) and v < 0:
        return {"fg": RED, "bg": RED_BG, "bold": True}
    if row[0] == "Other" and j == 0:
        return {"fg": MUTED}


def style_months(i, j, v, row):
    if j == 0:
        return {"fg": AMBER, "bold": True}
    return {2: {"fg": GREEN}, 3: {"fg": ORANGE}, 4: {"fg": RED}, 5: {"fg": BLUE},
            6: {"fg": GREEN if isinstance(v, (int, float)) and v >= 0 else RED, "bold": True}}.get(j)


def style_entry(i, j, v, row):
    if j in (1, 2):
        return {"fg": TYPE_COLOUR.get(row[1], INK), "bold": j == 1}


PLAN_NUMS = {2: NGN_FMT, 3: NGN_FMT, 4: NGN_FMT}
ENTRY_NUMS = {2: NGN_FMT}


def paint_overview(page, today, gids):
    as_of, bank, bal = balances()
    pm = plan_month(today)
    page.title("MONEY", "As of %s   ·   Plan month %s" % (as_of, month_label(pm)), 9)
    page.box("Where the money is", MONEY, H_WHERE, where_rows(bank, bal), style_where,
             {1: NGN_FMT}, total=True)
    page.box("Goals", GOALS_C, H_GOALS, goal_rows(bal, today), style_goals,
             {1: NGN_FMT, 2: NGN_FMT, 3: NGN_FMT, 7: "0.0", 8: NGN_FMT})
    page.box("Money flow — " + month_label(pm), FLOW_C, H_FLOW, flow_rows(pm), style_flow, {1: NGN_FMT}, total=True)
    page.box("Plan vs actual — " + month_label(pm), PLAN_C, H_PLAN, plan_vs_actual(pm), style_plan,
             PLAN_NUMS, total=True)
    page.box("Subscriptions — " + month_label(pm), SUBS_C, H_SUBS, subscription_rows(pm), style_subs,
             {1: NGN_FMT, 3: NGN_FMT}, total=True)
    rows = []
    for m in reversed(months(today)):
        t, start = totals(m), bank_at_start(m)
        rows.append([month_label(m, short=True), start, t["in"], t["from"], t["spent"], t["to"], start + t["left"]])
    page.box("Every month", MONTHS_C, H_MONTHS, rows, style_months,
             {j: NGN_FMT for j in range(1, 7)})
    # Each month name links to its tab.
    for k, m in enumerate(reversed(months(today))):
        r = len(page.grid) - 1 - len(rows) + k  # rows sit just above the trailing gap
        page.grid[r][0] = cell(month_label(m, short=True), bg=ZEBRA if k % 2 else WHITE, fg=AMBER, bold=True,
                               link="#gid=%d" % gids[month_label(m, short=True)])


def paint_month(page, m):
    rows = entries(m)
    sub = ("%d entries   ·   last entry %s" % (len(rows), rows[-1]["Date"][:10])) if rows else "No entries yet"
    page.title(month_label(m).upper(), sub, 5)
    page.box("Money flow", FLOW_C, H_FLOW, flow_rows(m), style_flow, {1: NGN_FMT}, total=True)
    page.box("Plan vs actual", PLAN_C, H_PLAN, plan_vs_actual(m), style_plan, PLAN_NUMS, total=True)
    page.box("Every entry", LEDGER_C, H_ENTRY, entry_rows(rows), style_entry, ENTRY_NUMS)


def paint_ledger(page):
    rows = shown(ml.ledger())
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
    ov = Page(have["Overview"], [230, 125, 170, 130, 170, 105, 135, 100, 150])
    paint_overview(ov, today, have)
    paint += ov.requests()
    for m in ms:
        pg = Page(have[month_label(m, short=True)], [230, 110, 130, 260, 200])
        paint_month(pg, m)
        paint += pg.requests()
    lg = Page(have["Ledger"], [110, 110, 130, 260, 200])
    paint_ledger(lg)
    paint += lg.requests()
    api.call("POST", ":batchUpdate", json={"requests": paint})
    print("built: %s" % ", ".join(order))


def left(today=None):
    """What's left in the running month, line by line, plus the bank. For a spend check."""
    pm = plan_month(today)
    as_of, bank, bal = balances()
    print("%s — as of %s. Bank NGN {:,.0f} (derived from the ledger)".format(bank) % (month_label(pm), as_of))
    open_lines = []
    for line, payday, planned, actual, rest in plan_vs_actual(pm)[:-1]:
        if line == "Other" or planned in ("", 0) and payday != "unplanned" and not actual:
            continue
        if payday == "unplanned":
            print("  UNPLANNED  %-26s spent NGN {:,.0f}".format(actual) % line)
        elif isinstance(rest, (int, float)) and rest != 0:
            open_lines.append(rest)
            flag = "  OVER     " if rest < 0 else "           "
            print("%s%-26s left NGN {:,.0f} of {:,.0f}".format(rest, planned) % (flag, line))
    print("  Buffer NGN {:,.0f}. When it's empty, an urgency is negotiated, not funded (Rule 8).".format(bal.get("Buffer", 0)))


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    cmd = argv[0] if argv else ""
    if cmd == "preview":
        preview()
    elif cmd == "left":
        left()
    elif cmd == "doctor":
        doctor()
    elif cmd == "build":
        build()
    elif cmd == "month-plan" and len(argv) == 2:
        month_plan(argv[1])
    elif cmd == "freeze" and len(argv) == 2:
        freeze(argv[1])
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
