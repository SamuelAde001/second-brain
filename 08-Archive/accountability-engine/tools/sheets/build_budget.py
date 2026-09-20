#!/usr/bin/env python3
"""
Builds the Details tab and rebuilds the Budget tab from tools/sheets/plan.json.

Re-runnable. Clears and rewrites both tabs, so plan.json is the source of truth
for structure. Day-to-day edits (a sub changes price, a category moves payday)
are made in plan.json and this is re-run — or made directly with `sheets.py ops`
for one-line changes.

    python tools/sheets/build_budget.py

Design rules it enforces, straight out of context/money.md:
  - Nothing is typed on Budget. Column B reads Details; month columns read
    Expenses; the savings block reads Transfers. A line cannot claim money moved
    when no row exists. That was the whole bug in the old sheets (Rule 6).
  - Details is the ONLY place a plan number is typed.
  - Cancelled items go Active=No, never deleted.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

# ---------------------------------------------------------------- palette ----

INK      = "#1f2937"   # section bars
HEAD     = "#374151"   # table headers
PAPER    = "#f3f4f6"   # total rows
MUTED    = "#6b7280"   # subtitles
GREEN    = "#065f46"   # savings
BLUE     = "#1e40af"   # paydays
RED      = "#b91c1c"   # warnings
AMBER    = "#92400e"   # lean month
PRE      = "#e5e7eb"   # months before the plan existed
WHITE    = "#ffffff"

NGN = '"₦"#,##0;[Red]-"₦"#,##0'

MONTHS = ["2026-08", "2026-09", "2026-10", "2026-11", "2026-12",
          "2027-01", "2027-02", "2027-03", "2027-04", "2027-05",
          "2027-06", "2027-07"]
MONTH_LABELS = ["Aug 26", "Sep 26", "Oct 26", "Nov 26", "Dec 26",
                "Jan 27", "Feb 27", "Mar 27", "Apr 27", "May 27",
                "Jun 27", "Jul 27"]

CATEGORIES = [
    "Building project", "Parents", "Girlfriend", "Community admin",
    "Subscriptions", "Feeding", "Transport", "Health",
    "Chores / household", "Creator visits", "Giving", "Data / airtime",
    "Personal / misc", "Bank charges", "Other",
]

# Ranges of the log tabs, as they already exist in the workbook.
EXP  = ('Expenses!$E$5:$E$404', 'Expenses!$C$5:$C$404', 'Expenses!$B$5:$B$404')
INC  = ('Income!$I$5:$I$124', 'Income!$B$5:$B$124')
TRF  = ('Transfers!$E$5:$E$404', 'Transfers!$C$5:$C$404', 'Transfers!$D$5:$D$404')


def col(n):
    """1 -> A"""
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def load_plan():
    with open(os.path.join(HERE, "plan.json"), encoding="utf-8") as fh:
        return json.load(fh)


def planned_months(plan):
    """The month keys the Plan column actually describes.

    The baseline was set on 2026-08-26 FOR September, so August was never
    planned. Comparing August actuals to it would invent an overspend.
    """
    start = plan.get("plan_start", MONTHS[0])
    return [m for m in MONTHS if m >= start]


# ---------------------------------------------------------------- details ----

def build_details(plan):
    rec = plan["recurring"]
    one = plan["one_offs"]["2026-09"]

    ops = [
        {"action": "ensureSheet", "args": {"tab": "Details", "index": 6, "tabColor": "#065f46"}},
        {"action": "clear", "args": {"tab": "Details"}},
    ]

    rows = [
        ["DETAILS — what every budget category is actually made of"] + [""] * 7,
        ["The ONLY place a plan number is typed. The Budget tab reads this with SUMIFS, "
         "so a category total can always be broken down into the things that make it up."] + [""] * 7,
        ["Cancelling something = set Active to No. Never delete the row. "
         "A subscription that reappears in three months is a pattern, and a deleted row hides it."] + [""] * 7,
        [""] * 8,
        ["Category", "Item", "₦ / month", "Tier", "Payday", "Due day", "Active", "Note"],
    ]
    rows += [list(r) for r in rec]

    first, last = 6, 5 + len(rec)
    total_row = last + 1
    rows.append(["RECURRING TOTAL", "", "", "", "", "", "", "Active items only."])

    # one-offs
    oh = total_row + 2                      # ONE-OFFS title row
    rows.append([""] * 8)
    rows.append(["ONE-OFFS — dated, not recurring"] + [""] * 7)
    rows.append(["These do NOT feed the recurring plan. They are listed on Budget in the month "
                 "they hit, and they show up in actuals automatically because they get logged on Expenses."] + [""] * 7)
    rows.append(["Month", "Category", "Item", "₦", "Payday", "Note", "", ""])
    for o in one:
        # plan.json one-off rows are [cat, item, amt, tier, payday, due, active, note]
        rows.append(["2026-09", o[0], o[1], o[2], o[4], o[7], "", ""])
    one_first = oh + 3
    one_last = one_first + len(one) - 1
    rows.append(["", "", "SEPTEMBER ONE-OFF TOTAL", "", "", "", "", ""])
    one_total = one_last + 1

    ops.append({"action": "write", "args": {"tab": "Details", "cell": "A1", "values": rows}})

    ops += [
        {"action": "setFormulas", "args": {"tab": "Details", "cell": "C%d" % total_row, "formulas": [[
            '=SUMIFS($C$%d:$C$%d,$G$%d:$G$%d,"Yes")' % (first, last, first, last)]]}},
        {"action": "setFormulas", "args": {"tab": "Details", "cell": "D%d" % one_total, "formulas": [[
            '=SUM($D$%d:$D$%d)' % (one_first, one_last)]]}},

        # structure
        {"action": "freeze", "args": {"tab": "Details", "rows": 5}},
        {"action": "setColumnWidth", "args": {"tab": "Details", "column": 1, "width": 150}},
        {"action": "setColumnWidth", "args": {"tab": "Details", "column": 2, "width": 260}},
        {"action": "setColumnWidth", "args": {"tab": "Details", "column": 3, "width": 100}},
        {"action": "setColumnWidth", "args": {"tab": "Details", "column": 4, "width": 105}},
        {"action": "setColumnWidth", "args": {"tab": "Details", "column": 5, "width": 70}},
        {"action": "setColumnWidth", "args": {"tab": "Details", "column": 6, "width": 75}},
        {"action": "setColumnWidth", "args": {"tab": "Details", "column": 7, "width": 65}},
        {"action": "setColumnWidth", "args": {"tab": "Details", "column": 8, "width": 520}},

        # title
        {"action": "format", "args": {"tab": "Details", "range": "A1:H1", "merge": True,
                                      "background": INK, "fontColor": WHITE, "bold": True, "fontSize": 13}},
        {"action": "format", "args": {"tab": "Details", "range": "A2:H2", "merge": True,
                                      "fontColor": MUTED, "italic": True, "wrap": True}},
        {"action": "format", "args": {"tab": "Details", "range": "A3:H3", "merge": True,
                                      "fontColor": RED, "italic": True, "wrap": True}},
        {"action": "format", "args": {"tab": "Details", "range": "A5:H5",
                                      "background": HEAD, "fontColor": WHITE, "bold": True}},
        {"action": "format", "args": {"tab": "Details", "range": "C%d:C%d" % (first, total_row),
                                      "numberFormat": NGN}},
        {"action": "format", "args": {"tab": "Details", "range": "A%d:H%d" % (total_row, total_row),
                                      "background": PAPER, "bold": True}},
        {"action": "format", "args": {"tab": "Details", "range": "H%d:H%d" % (first, last),
                                      "fontColor": MUTED, "fontSize": 9, "wrap": True}},
        {"action": "format", "args": {"tab": "Details", "range": "D%d:G%d" % (first, last),
                                      "horizontalAlignment": "center"}},

        # one-offs block
        {"action": "format", "args": {"tab": "Details", "range": "A%d:H%d" % (oh, oh), "merge": True,
                                      "background": AMBER, "fontColor": WHITE, "bold": True}},
        {"action": "format", "args": {"tab": "Details", "range": "A%d:H%d" % (oh + 1, oh + 1),
                                      "merge": True, "fontColor": MUTED, "italic": True, "wrap": True}},
        {"action": "format", "args": {"tab": "Details", "range": "A%d:F%d" % (oh + 2, oh + 2),
                                      "background": HEAD, "fontColor": WHITE, "bold": True}},
        {"action": "format", "args": {"tab": "Details", "range": "D%d:D%d" % (one_first, one_total),
                                      "numberFormat": NGN}},
        {"action": "format", "args": {"tab": "Details", "range": "A%d:F%d" % (one_total, one_total),
                                      "background": PAPER, "bold": True}},
        {"action": "format", "args": {"tab": "Details", "range": "F%d:F%d" % (one_first, one_last),
                                      "fontColor": MUTED, "fontSize": 9, "wrap": True}},

        # inactive rows greyed
        {"action": "validation", "args": {"tab": "Details", "range": "G%d:G%d" % (first, last),
                                          "list": ["Yes", "No"]}},
        {"action": "validation", "args": {"tab": "Details", "range": "E%d:E%d" % (first, last),
                                          "list": ["A", "B"]}},
        {"action": "validation", "args": {"tab": "Details", "range": "D%d:D%d" % (first, last),
                                          "list": ["Fixed", "Committed", "Discretionary"]}},
    ]

    # grey out any inactive item
    for i, r in enumerate(rec):
        if r[6] != "Yes":
            rn = first + i
            ops.append({"action": "format", "args": {"tab": "Details", "range": "A%d:H%d" % (rn, rn),
                                                     "fontColor": "#9ca3af", "italic": True}})

    return ops, (first, last)


# ----------------------------------------------------------------- budget ----

def build_budget(plan, details_range):
    d_first, d_last = details_range
    ops = [{"action": "freeze", "args": {"tab": "Budget", "rows": 0, "columns": 0}},
           {"action": "clear", "args": {"tab": "Budget"}}]

    LASTCOL = "S"
    WIDTH = 19
    rows = []

    def blank():
        rows.append([""] * 18)

    plan_start  = plan.get("plan_start", MONTHS[0])
    track_start = plan.get("tracking_start", "")
    covered     = planned_months(plan)
    n_covered   = len(covered)
    first_plan_col = MONTHS.index(plan_start)          # 0-based into MONTHS
    plan_label  = MONTH_LABELS[first_plan_col]

    # --- header -------------------------------------------------------------
    rows.append(["BUDGET — the plan, and what it costs to keep it"] + [""] * 17)
    rows.append(["Nothing on this sheet is typed by hand. Plan reads Details. The month columns read "
                 "Expenses. The savings block reads Transfers. A line here cannot claim money moved "
                 "when no row exists — money.md Rule 6."] + [""] * 17)
    blank()

    # --- where you stand today ----------------------------------------------
    # The bank figure lived only on Dashboard, so this tab could show a ₦1,000
    # spend against a ₦951,700 plan and never say what was actually in the
    # account. The breakdown is spelled out so the number can be checked by eye.
    CASH_TITLE = len(rows) + 1
    rows.append(["WHERE YOU STAND TODAY — what is actually in the account"] + [""] * 17)
    rows.append(["In the bank right now", "", "Everything you can actually spend today. "
                 "This is the same figure as the top of Dashboard."] + [""] * 15)
    rows.append(["Made up of:", "", ""] + [""] * 15)
    rows.append(["   Opening balance — %s" % track_start, "",
                 "The figure you gave when this engine was built. Everything you earned or spent "
                 "BEFORE that date is already inside it."] + [""] * 15)
    rows.append(["   + money in since then", "", "Every row on the Income tab."] + [""] * 15)
    rows.append(["   − money out since then", "", "Every row on the Expenses tab."] + [""] * 15)
    rows.append(["   − net moved into pots", "", "Money that left the bank for Goal 1, the Buffer "
                 "or Cowrywise. To pot minus From pot, off the Transfers tab."] + [""] * 15)
    CASH_BANK = CASH_TITLE + 1
    CASH_OPEN, CASH_IN, CASH_OUT, CASH_POT = (CASH_TITLE + 3, CASH_TITLE + 4,
                                              CASH_TITLE + 5, CASH_TITLE + 6)
    rows.append(["Tracking started %s. June, July and August's earnings are already inside the "
                 "opening balance, so they are NOT on the Income tab — which is why the %s column "
                 "below is nearly empty and its income reads zero. Nothing is missing. Putting them "
                 "on Income as well would count them twice and break the bank figure above. "
                 "The first month this sheet measures end to end is %s."
                 % (track_start, MONTH_LABELS[0], plan_label)] + [""] * 17)
    CASH_NOTE = CASH_POT + 1
    blank()

    # --- monthly plan -------------------------------------------------------
    PLAN_TITLE = CASH_NOTE + 2
    rows.append(["THE MONTHLY PLAN — recurring baseline, from %s onward" % plan_label] + [""] * 17)
    # Months before the plan existed are marked, greyed, and excluded from vs-plan.
    month_heads = [l if MONTHS[i] >= plan_start else l + "  ‡"
                   for i, l in enumerate(MONTH_LABELS)]
    NL = chr(10)
    rows.append(["Category", "Plan / month" + NL + "(from %s)" % plan_label, "Tier", "Payday"]
                + month_heads
                + ["Total actual" + NL + "(all 12)",
                   "vs plan" + NL + "(%d planned months)" % n_covered])
    PLAN_HEAD = PLAN_TITLE + 1
    PLAN_FIRST = PLAN_TITLE + 2
    for c in CATEGORIES:
        rows.append([c] + [""] * 17)
    PLAN_LAST = PLAN_FIRST + len(CATEGORIES) - 1
    rows.append(["TOTAL SPENT"] + [""] * 17)
    rows.append(["INCOME THAT MONTH"] + [""] * 17)
    rows.append(["SURPLUS  (in − out)"] + [""] * 17)
    TOTAL, INCOME, SURPLUS = PLAN_LAST + 1, PLAN_LAST + 2, PLAN_LAST + 3
    rows.append(["‡  %s had no plan — the baseline was set on %s FOR %s, and tracking only "
                 "started that day. Its column is greyed, its income is zero because June–August "
                 "sits in the opening balance, and it is left out of “vs plan” so an unplanned "
                 "month can never read as an overspend. “Total actual” on the right still counts "
                 "every month, including it."
                 % (MONTH_LABELS[0], track_start, plan_label)] + [""] * 17)
    PLAN_NOTE = SURPLUS + 1
    blank()

    # --- one-offs -----------------------------------------------------------
    ONE_TITLE = PLAN_NOTE + 2
    rows.append(["ONE-OFFS — dated, not recurring. Listed here so a month knows what is coming."] + [""] * 17)
    rows.append(["Month", "Category", "Item", "₦", "Payday", "Note"] + [""] * 12)
    ONE_FIRST = ONE_TITLE + 2
    for o in plan["one_offs"]["2026-09"]:
        rows.append(["2026-09", o[0], o[1], o[2], o[4], o[7]] + [""] * 12)
    ONE_LAST = ONE_FIRST + len(plan["one_offs"]["2026-09"]) - 1
    rows.append(["", "", "SEPTEMBER ONE-OFF TOTAL", "", "", ""] + [""] * 12)
    ONE_TOTAL = ONE_LAST + 1
    blank()

    # --- savings ------------------------------------------------------------
    # Per-month, not a flat average. A flat number asked September for money it
    # does not have, because September carries the one-offs. Read from plan.json
    # so the pots have exactly one source, like every other number on this tab.
    SAV_TITLE = ONE_TOTAL + 2
    rows.append([u"SAVINGS PLAN — the pots, where they live, and whether the money actually moved"] + [""] * 17)
    rows.append([u"Planned per month, NOT a flat average — September is lower because its one-offs come "
                 u"first. “Moved to date” is not a plan: it reads the Transfers tab, To pot minus "
                 u"From pot. If it says zero, no money moved, whatever the intention was."] + [""] * 17)
    rows.append([u"Pot", u"Where it lives", u"Payday", u"Target"] + MONTH_LABELS
                + [u"Moved to date", u"Still to find"])
    SAV_HEAD = SAV_TITLE + 2
    SAV_FIRST = SAV_HEAD + 1
    savings = plan["savings"]
    # Pots running between now and December vs pots that do not start until
    # January. They must never be summed into one "this month" figure.
    running = [v for v in savings if any(m < "2027-01" for m in v["schedule"])]
    later = [v for v in savings if v not in running]
    ordered = running + later
    for sv in ordered:
        rows.append([sv["pot"], sv["account"], sv["payday"], sv["target"]]
                    + [sv["schedule"].get(m, "") for m in MONTHS]
                    + ["", "", sv["note"]])
    SAV_LAST = SAV_FIRST + len(ordered) - 1
    SAV_NOW_LAST = SAV_FIRST + len(running) - 1
    rows.append([u"MOVING NOW  (Sep – Dec 2026)"] + [""] * 17)
    rows.append([u"FROM JAN 2027"] + [""] * 17)
    SAV_TOTAL = SAV_LAST + 1
    SAV_LATER = SAV_LAST + 2
    rows.append([u"A pot with no account is a pot that cannot be funded on payday. "
                 u"The Buffer lives in the savings account already called “Emergency” "
                 u"(Samuel, 2026-08-28) — which from Jan 2027 would also hold the actual emergency "
                 u"fund. Two pots, one account, one balance that means nothing. Decide before then."] + [""] * 17)
    SAV_NOTE = SAV_LATER + 1
    blank()

    # --- the month must balance ---------------------------------------------
    # The whole point of this block: income minus bills minus one-offs minus
    # every pot must be ZERO. A leftover is money with no name on it, and money
    # with no name on it is how the June-August savings evaporated.
    BAL_TITLE = SAV_NOTE + 2
    rows.append([u"THE MONTH MUST BALANCE — every naira has a job, and the bottom line is ZERO"] + [""] * 17)
    rows.append([u"Expected income minus the bills above, minus that month's one-offs, minus every pot. "
                 u"If the last row is not zero, the month is not planned — it is estimated. Anything "
                 u"left over has no name on it, and money with no name is what evaporated June–August."] + [""] * 17)
    rows.append(["", u"Per month", "", ""] + MONTH_LABELS + ["", ""])
    BAL_HEAD = BAL_TITLE + 2
    bal_rows = [
        u"Expected income",
        u"− Bills (the plan above)",
        u"− One-offs that month",
        u"− Into the pots",
        u"LEFT OVER  (must be ₦0)",
    ]
    for label in bal_rows:
        rows.append([label] + [""] * 17)
    BAL_IN, BAL_BILLS, BAL_ONE, BAL_POTS, BAL_LEFT = (BAL_HEAD + 1, BAL_HEAD + 2, BAL_HEAD + 3,
                                                      BAL_HEAD + 4, BAL_HEAD + 5)
    rows.append([u"Sep – Dec 2026 balance to exactly zero. FROM JANUARY THEY DO NOT: Cowrywise stops "
                 u"(freeing ₦100,000/month) but Goal 2 needs ₦428,571 and the emergency fund "
                 u"₦50,000, so the month is short ₦42,530 at the August mix. That gap is the "
                 u"course's job — and it is far smaller than the ₦152,000–₦186,000 "
                 u"money.md used to claim, which was a Sep–Dec surplus figure wrongly applied to a "
                 u"period in which Cowrywise has already stopped."] + [""] * 17)
    BAL_NOTE = BAL_LEFT + 1
    blank()

    # --- paydays ------------------------------------------------------------
    PAY_TITLE = BAL_NOTE + 2
    rows.append(["THE TWO PAYDAYS — one batch, split across two dates"] + [""] * 17)
    rows.append(["", "Payday A — 70%", "Payday B — 30%", "", "", "", ""] + [""] * 11)
    rows.append(["When it lands", "End of the PREVIOUS month",
                 "Around the 14th", "", "", "", ""] + [""] * 11)
    rows.append(["What it funds", "The 1st – 14th", "The 15th – month end", "", "", "", ""] + [""] * 11)
    rows.append(["Expected in", "", "", "", "", "", ""] + [""] * 11)
    rows.append(["Committed (from Details)", "", "", "", "", "", ""] + [""] * 11)
    rows.append(["Free after commitments", "", "", "", "", "", ""] + [""] * 11)
    PAY_HEAD = PAY_TITLE + 1
    PAY_LANDS, PAY_FUNDS, PAY_IN, PAY_OUT, PAY_FREE = (PAY_HEAD + 1, PAY_HEAD + 2,
                                                       PAY_HEAD + 3, PAY_HEAD + 4, PAY_HEAD + 5)
    rows.append(["The 30% is ALWAYS the previous month's remaining batch, never a new one. "
                 "Every “mid-month payment” is last month's money."] + [""] * 17)
    PAY_NOTE = PAY_FREE + 1
    blank()

    # --- lean ladder --------------------------------------------------------
    LEAN_TITLE = PAY_NOTE + 2
    rows.append(["LEAN MONTH LADDER — decided now, so it is not negotiated at 11pm on a short month"] + [""] * 17)
    ladder = [
        "Income lands short. Cut in THIS order. Do not improvise.",
        "1.  Personal / misc  —  ₦10,000",
        "2.  Creator visits  —  ₦25,000",
        "3.  Household down to ₦20,000  —  ₦20,000",
        "4.  The BUFFER absorbs the rest. That is what it is for.",
        "5.  ONLY THEN a conversation. Savings are never the valve (Rule 1). "
        "Cowrywise never pauses (Rule 7). The gym is not a budget line to raid.",
        "A 2-video month is ₦909,991. Steps 1–3 free only ₦55,000 of a ₦228,569 gap. "
        "Without a buffer there is no legal way to balance that month — which is exactly why the buffer exists.",
    ]
    for l in ladder:
        rows.append([l] + [""] * 17)
    LEAN_LAST = LEAN_TITLE + len(ladder)
    blank()

    # --- payday calendar ----------------------------------------------------
    CAL_TITLE = LEAN_LAST + 2
    rows.append(["PAYDAY CALENDAR — they do not pay at weekends"] + [""] * 17)
    rows.append(["Nominal", "Falls on", "Actually lands", "Slip", "Why it matters"] + [""] * 13)
    CAL_HEAD = CAL_TITLE + 1
    cal = [
        ("Aug 70%", "Mon 31 Aug 2026", "Mon 31 Aug", "—", "Funds the first half of September."),
        ("Sep 30%", "Mon 14 Sep 2026", "Mon 14 Sep", "—", "Funds the second half of September."),
        ("Sep 70%", "Wed 30 Sep 2026", "Wed 30 Sep", "—", ""),
        ("Oct 30%", "Wed 14 Oct 2026", "Wed 14 Oct", "—", ""),
        ("Oct 70%", "Sat 31 Oct 2026", "Mon 2 Nov", "+2 days",
         "TIGHTEST POINT OF THE YEAR. November's front half is funded on the 2nd, and Google bills the "
         "2nd, CapCut the 4th. This is a buffer month."),
        ("Nov 30%", "Sat 14 Nov 2026", "Mon 16 Nov", "+2 days", "Second slip in a row."),
        ("Nov 70%", "Mon 30 Nov 2026", "Mon 30 Nov", "—", ""),
        ("Dec 30%", "Mon 14 Dec 2026", "Mon 14 Dec", "—", ""),
        ("Dec 70%", "Thu 31 Dec 2026", "Thu 31 Dec", "—", "Goal 1 deadline is this day."),
    ]
    for c in cal:
        rows.append(list(c) + [""] * 13)
    CAL_LAST = CAL_HEAD + len(cal)

    rows = [r + [""] * (WIDTH - len(r)) for r in rows]
    assert all(len(r) == WIDTH for r in rows)
    ops.append({"action": "write", "args": {"tab": "Budget", "cell": "A1", "values": rows}})

    # ---------------------------------------------------------- formulas ----
    f = []

    gross = "(2*Setup!$B$18+2*Setup!$B$19)*Setup!$B$17"

    # plan column B  <- Details
    for r in range(PLAN_FIRST, PLAN_LAST + 1):
        f.append(("B%d" % r, '=SUMIFS(Details!$C$%d:$C$%d,Details!$A$%d:$A$%d,$A%d,'
                             'Details!$G$%d:$G$%d,"Yes")'
                  % (d_first, d_last, d_first, d_last, r, d_first, d_last)))
        # tier / payday, read off Details too (blank when the category spans both)
        f.append(("C%d" % r, '=IFERROR(IF(COUNTIF(Details!$A$%d:$A$%d,$A%d)=0,"",'
                             'IF(COUNTIFS(Details!$A$%d:$A$%d,$A%d,Details!$D$%d:$D$%d,'
                             'INDEX(Details!$D$%d:$D$%d,MATCH($A%d,Details!$A$%d:$A$%d,0)))'
                             '=COUNTIF(Details!$A$%d:$A$%d,$A%d),'
                             'INDEX(Details!$D$%d:$D$%d,MATCH($A%d,Details!$A$%d:$A$%d,0)),"mixed")),"")'
                  % (d_first, d_last, r,
                     d_first, d_last, r, d_first, d_last,
                     d_first, d_last, r, d_first, d_last,
                     d_first, d_last, r,
                     d_first, d_last, r, d_first, d_last)))
        f.append(("D%d" % r, '=IFERROR(IF(COUNTIF(Details!$A$%d:$A$%d,$A%d)=0,"",'
                             'IF(COUNTIFS(Details!$A$%d:$A$%d,$A%d,Details!$E$%d:$E$%d,"A")'
                             '=COUNTIF(Details!$A$%d:$A$%d,$A%d),"A",'
                             'IF(COUNTIFS(Details!$A$%d:$A$%d,$A%d,Details!$E$%d:$E$%d,"B")'
                             '=COUNTIF(Details!$A$%d:$A$%d,$A%d),"B","split"))),"")'
                  % (d_first, d_last, r,
                     d_first, d_last, r, d_first, d_last,
                     d_first, d_last, r,
                     d_first, d_last, r, d_first, d_last,
                     d_first, d_last, r)))
        # month actuals  <- Expenses
        for i, m in enumerate(MONTHS):
            f.append(("%s%d" % (col(5 + i), r),
                      '=SUMIFS(%s,%s,$A%d,%s,"%s")' % (EXP[0], EXP[1], r, EXP[2], m)))
        f.append(("Q%d" % r, "=SUM($E%d:$P%d)" % (r, r)))
        # vs plan spans ONLY the planned months. Including an unplanned month
        # here would book its spending as an overspend against a plan that did
        # not exist yet.
        f.append(("R%d" % r, "=SUM($%s%d:$P%d)-($B%d*%d)"
                  % (col(5 + first_plan_col), r, r, r, n_covered)))

    # totals
    f.append(("B%d" % TOTAL, "=SUM(B%d:B%d)" % (PLAN_FIRST, PLAN_LAST)))
    for i in range(12):
        c = col(5 + i)
        f.append(("%s%d" % (c, TOTAL), "=SUM(%s%d:%s%d)" % (c, PLAN_FIRST, c, PLAN_LAST)))
        f.append(("%s%d" % (c, INCOME),
                  '=SUMIFS(%s,%s,"%s")' % (INC[0], INC[1], MONTHS[i])))
        f.append(("%s%d" % (c, SURPLUS), "=%s%d-%s%d" % (c, INCOME, c, TOTAL)))
    f.append(("Q%d" % TOTAL, "=SUM($E%d:$P%d)" % (TOTAL, TOTAL)))
    f.append(("R%d" % TOTAL, "=SUM($%s%d:$P%d)-($B%d*%d)"
              % (col(5 + first_plan_col), TOTAL, TOTAL, TOTAL, n_covered)))
    f.append(("Q%d" % INCOME, "=SUM($E%d:$P%d)" % (INCOME, INCOME)))
    f.append(("Q%d" % SURPLUS, "=SUM($E%d:$P%d)" % (SURPLUS, SURPLUS)))

    # one-offs total
    f.append(("D%d" % ONE_TOTAL, "=SUM(D%d:D%d)" % (ONE_FIRST, ONE_LAST)))

    # savings: moved to date (Q) / still to find (R). The month columns are the
    # typed plan — the ONLY typed numbers on this tab besides Details, and they
    # are here because a pot schedule cannot be derived from anything.
    for r in range(SAV_FIRST, SAV_LAST + 1):
        f.append(("Q%d" % r,
                  '=SUMIFS(%s,%s,$A%d,%s,"To pot")-SUMIFS(%s,%s,$A%d,%s,"From pot")'
                  % (TRF[0], TRF[1], r, TRF[2], TRF[0], TRF[1], r, TRF[2])))
        f.append(("R%d" % r, "=MAX(0,$D%d-$Q%d)" % (r, r)))
    for _row, _lo, _hi in ((SAV_TOTAL, SAV_FIRST, SAV_NOW_LAST),
                           (SAV_LATER, SAV_NOW_LAST + 1, SAV_LAST)):
        for _i in range(12):
            _c = col(5 + _i)
            f.append(("%s%d" % (_c, _row), "=SUM(%s%d:%s%d)" % (_c, _lo, _c, _hi)))
        f.append(("D%d" % _row, "=SUM(D%d:D%d)" % (_lo, _hi)))
        f.append(("Q%d" % _row, "=SUM(Q%d:Q%d)" % (_lo, _hi)))
        f.append(("R%d" % _row, "=SUM(R%d:R%d)" % (_lo, _hi)))

    # the month must balance — every planned column ends at zero, or the month
    # is not planned, it is estimated.
    one_off_months = {}
    for _m, _rws in (plan.get("one_offs") or {}).items():
        one_off_months[_m] = sum(o[2] for o in _rws if str(o[6]).lower().startswith("y"))
    for _i, _m in enumerate(MONTHS):
        _c = col(5 + _i)
        if _m < plan_start:
            for _r in (BAL_IN, BAL_BILLS, BAL_ONE, BAL_POTS, BAL_LEFT):
                f.append(("%s%d" % (_c, _r), '=""'))
            continue
        # ROUND: the rate math lands on ...740.90, and a block whose whole
        # point is "this reads zero" cannot end at -0.1 of a naira.
        f.append(("%s%d" % (_c, BAL_IN), "=ROUND(%s,0)" % gross))
        f.append(("%s%d" % (_c, BAL_BILLS), "=-$B$%d" % TOTAL))
        f.append(("%s%d" % (_c, BAL_ONE), "=-%d" % one_off_months.get(_m, 0)))
        f.append(("%s%d" % (_c, BAL_POTS), "=-(%s%d+%s%d)" % (_c, SAV_TOTAL, _c, SAV_LATER)))
        f.append(("%s%d" % (_c, BAL_LEFT), "=SUM(%s%d:%s%d)" % (_c, BAL_IN, _c, BAL_POTS)))
    # column B repeats the first planned month, so the block reads as "per month"
    for _r in (BAL_IN, BAL_BILLS, BAL_ONE, BAL_POTS, BAL_LEFT):
        f.append(("B%d" % _r, "=%s%d" % (col(5 + first_plan_col), _r)))

    # cash position — the same arithmetic Dashboard uses, shown in its parts
    f.append(("B%d" % CASH_OPEN, "=Setup!$B$5"))
    f.append(("B%d" % CASH_IN,   "=SUM(%s)" % INC[0]))
    f.append(("B%d" % CASH_OUT,  "=SUM(%s)" % EXP[0]))
    f.append(("B%d" % CASH_POT,
              '=SUMIFS(%s,%s,"To pot")-SUMIFS(%s,%s,"From pot")'
              % (TRF[0], TRF[2], TRF[0], TRF[2])))
    f.append(("B%d" % CASH_BANK, "=B%d+B%d-B%d-B%d"
              % (CASH_OPEN, CASH_IN, CASH_OUT, CASH_POT)))

    # paydays
    f.append(("B%d" % PAY_IN, "=%s*0.7" % gross))
    f.append(("C%d" % PAY_IN, "=%s*0.3" % gross))
    f.append(("B%d" % PAY_OUT,
              '=SUMIFS(Details!$C$%d:$C$%d,Details!$E$%d:$E$%d,"A",Details!$G$%d:$G$%d,"Yes")+Setup!$B$20'
              % (d_first, d_last, d_first, d_last, d_first, d_last)))
    f.append(("C%d" % PAY_OUT,
              '=SUMIFS(Details!$C$%d:$C$%d,Details!$E$%d:$E$%d,"B",Details!$G$%d:$G$%d,"Yes")'
              % (d_first, d_last, d_first, d_last, d_first, d_last)))
    f.append(("B%d" % PAY_FREE, "=B%d-B%d" % (PAY_IN, PAY_OUT)))
    f.append(("C%d" % PAY_FREE, "=C%d-C%d" % (PAY_IN, PAY_OUT)))

    for cell, formula in f:
        ops.append({"action": "setFormulas", "args": {"tab": "Budget", "cell": cell,
                                                      "formulas": [[formula]]}})

    # ----------------------------------------------------------- format ----
    def fmt(rng, **kw):
        a = {"tab": "Budget", "range": rng}
        a.update(kw)
        ops.append({"action": "format", "args": a})

    for c, w in [(1, 190), (2, 115), (3, 105), (4, 70), (17, 115), (18, 120), (19, 300)]:
        ops.append({"action": "setColumnWidth", "args": {"tab": "Budget", "column": c, "width": w}})
    for i in range(12):
        ops.append({"action": "setColumnWidth", "args": {"tab": "Budget", "column": 5 + i, "width": 88}})

    fmt("A1:%s1" % LASTCOL, merge=True, background=INK, fontColor=WHITE, bold=True, fontSize=13)
    fmt("A2:%s2" % LASTCOL, merge=True, fontColor=MUTED, italic=True, wrap=True)

    fmt("A%d:%s%d" % (CASH_TITLE, LASTCOL, CASH_TITLE), merge=True, background=GREEN,
        fontColor=WHITE, bold=True)
    fmt("A%d:B%d" % (CASH_BANK, CASH_BANK), background=PAPER, bold=True, fontSize=12)
    fmt("B%d:B%d" % (CASH_BANK, CASH_POT), numberFormat=NGN)
    fmt("B%d:B%d" % (CASH_BANK, CASH_BANK), fontColor=GREEN)
    fmt("A%d:A%d" % (CASH_TITLE + 2, CASH_TITLE + 2), italic=True, fontColor=MUTED)
    fmt("A%d:A%d" % (CASH_OPEN, CASH_POT), fontColor=MUTED)
    for _r in (CASH_BANK, CASH_OPEN, CASH_IN, CASH_OUT, CASH_POT):
        fmt("C%d:%s%d" % (_r, LASTCOL, _r), merge=True, fontColor=MUTED, fontSize=9, wrap=True)
    fmt("A%d:%s%d" % (CASH_NOTE, LASTCOL, CASH_NOTE), merge=True, fontColor=RED,
        italic=True, wrap=True)
    fmt("A%d:%s%d" % (PLAN_TITLE, LASTCOL, PLAN_TITLE), merge=True, background=INK,
        fontColor=WHITE, bold=True)
    fmt("A%d:%s%d" % (PLAN_HEAD, LASTCOL, PLAN_HEAD), background=HEAD, fontColor=WHITE, bold=True,
        horizontalAlignment="center", wrap=True)
    fmt("A%d:A%d" % (PLAN_FIRST, PLAN_LAST), horizontalAlignment="left")
    fmt("B%d:B%d" % (PLAN_FIRST, TOTAL), numberFormat=NGN)
    fmt("E%d:%s%d" % (PLAN_FIRST, LASTCOL, SURPLUS), numberFormat=NGN)
    fmt("C%d:D%d" % (PLAN_FIRST, PLAN_LAST), horizontalAlignment="center")
    fmt("A%d:%s%d" % (TOTAL, LASTCOL, SURPLUS), background=PAPER, bold=True)
    fmt("A%d:%s%d" % (SURPLUS, LASTCOL, SURPLUS), fontColor=GREEN)

    # months that predate the plan: greyed, and called out underneath
    if first_plan_col > 0:
        fmt("%s%d:%s%d" % (col(5), PLAN_FIRST, col(4 + first_plan_col), SURPLUS),
            background=PRE, fontColor=MUTED)
    fmt("A%d:%s%d" % (PLAN_NOTE, LASTCOL, PLAN_NOTE), merge=True, fontColor=MUTED,
        italic=True, wrap=True)

    fmt("A%d:%s%d" % (ONE_TITLE, LASTCOL, ONE_TITLE), merge=True, background=AMBER,
        fontColor=WHITE, bold=True)
    fmt("A%d:F%d" % (ONE_TITLE + 1, ONE_TITLE + 1), background=HEAD, fontColor=WHITE, bold=True)
    fmt("D%d:D%d" % (ONE_FIRST, ONE_TOTAL), numberFormat=NGN)
    fmt("A%d:F%d" % (ONE_TOTAL, ONE_TOTAL), background=PAPER, bold=True)
    fmt("F%d:F%d" % (ONE_FIRST, ONE_LAST), fontColor=MUTED, fontSize=9, wrap=True)

    fmt("A%d:%s%d" % (SAV_TITLE, LASTCOL, SAV_TITLE), merge=True, background=GREEN,
        fontColor=WHITE, bold=True)
    fmt("A%d:%s%d" % (SAV_TITLE + 1, LASTCOL, SAV_TITLE + 1), merge=True, fontColor=MUTED,
        italic=True, wrap=True)
    fmt("A%d:%s%d" % (SAV_HEAD, LASTCOL, SAV_HEAD), background=HEAD, fontColor=WHITE,
        bold=True, wrap=True, horizontalAlignment="center")
    fmt("A%d:A%d" % (SAV_HEAD, SAV_LATER), horizontalAlignment="left")
    fmt("D%d:R%d" % (SAV_FIRST, SAV_LATER), numberFormat=NGN)
    fmt("B%d:C%d" % (SAV_FIRST, SAV_LAST), horizontalAlignment="center")
    fmt("A%d:%s%d" % (SAV_TOTAL, LASTCOL, SAV_TOTAL), background=PAPER, bold=True)
    fmt("A%d:%s%d" % (SAV_LATER, LASTCOL, SAV_LATER), background=PAPER, bold=True)
    fmt("A%d:A%d" % (SAV_LATER, SAV_LATER), fontColor=RED)
    fmt("S%d:S%d" % (SAV_FIRST, SAV_LAST), fontColor=MUTED, fontSize=9, wrap=True)
    fmt("A%d:%s%d" % (SAV_NOTE, LASTCOL, SAV_NOTE), merge=True, fontColor=RED, italic=True, wrap=True)
    # a pot with no home is the one thing on this block that stops a payday
    for _i, _sv in enumerate(ordered):
        if _sv["account"] == "NOT SET":
            fmt("B%d:B%d" % (SAV_FIRST + _i, SAV_FIRST + _i), background="#fee2e2",
                fontColor=RED, bold=True)

    # --- the month must balance --------------------------------------------
    fmt("A%d:%s%d" % (BAL_TITLE, LASTCOL, BAL_TITLE), merge=True, background=GREEN,
        fontColor=WHITE, bold=True)
    fmt("A%d:%s%d" % (BAL_TITLE + 1, LASTCOL, BAL_TITLE + 1), merge=True, fontColor=MUTED,
        italic=True, wrap=True)
    fmt("A%d:%s%d" % (BAL_HEAD, LASTCOL, BAL_HEAD), background=HEAD, fontColor=WHITE,
        bold=True, horizontalAlignment="center")
    fmt("A%d:A%d" % (BAL_HEAD, BAL_LEFT), horizontalAlignment="left")
    fmt("B%d:R%d" % (BAL_IN, BAL_LEFT), numberFormat=NGN)
    fmt("A%d:%s%d" % (BAL_LEFT, LASTCOL, BAL_LEFT), background=PAPER, bold=True, fontSize=12)
    fmt("A%d:%s%d" % (BAL_NOTE, LASTCOL, BAL_NOTE), merge=True, fontColor=RED,
        italic=True, wrap=True)
    ops.append({"action": "setColumnWidth", "args": {"tab": "Budget", "column": 7, "width": 88}})
    ops.append({"action": "setColumnWidth", "args": {"tab": "Budget", "column": 8, "width": 88}})

    fmt("A%d:%s%d" % (PAY_TITLE, LASTCOL, PAY_TITLE), merge=True, background=BLUE,
        fontColor=WHITE, bold=True)
    fmt("A%d:C%d" % (PAY_HEAD, PAY_HEAD), background=HEAD, fontColor=WHITE, bold=True)
    fmt("A%d:A%d" % (PAY_LANDS, PAY_FREE), bold=True)
    fmt("B%d:C%d" % (PAY_IN, PAY_FREE), numberFormat=NGN)
    fmt("A%d:C%d" % (PAY_FREE, PAY_FREE), background=PAPER, bold=True, fontColor=GREEN)
    fmt("A%d:%s%d" % (PAY_NOTE, LASTCOL, PAY_NOTE), merge=True, fontColor=MUTED,
        italic=True, wrap=True)

    fmt("A%d:%s%d" % (LEAN_TITLE, LASTCOL, LEAN_TITLE), merge=True, background=AMBER,
        fontColor=WHITE, bold=True)
    for i in range(1, len(ladder) + 1):
        r = LEAN_TITLE + i
        fmt("A%d:%s%d" % (r, LASTCOL, r), merge=True, wrap=True)
    fmt("A%d:%s%d" % (LEAN_LAST, LASTCOL, LEAN_LAST), fontColor=RED, italic=True)

    fmt("A%d:%s%d" % (CAL_TITLE, LASTCOL, CAL_TITLE), merge=True, background=BLUE,
        fontColor=WHITE, bold=True)
    fmt("A%d:E%d" % (CAL_HEAD, CAL_HEAD), background=HEAD, fontColor=WHITE, bold=True)
    fmt("E%d:E%d" % (CAL_HEAD + 1, CAL_LAST), fontColor=MUTED, fontSize=9, wrap=True)
    # the two slip rows in red
    fmt("A%d:E%d" % (CAL_HEAD + 5, CAL_HEAD + 6), fontColor=RED, bold=True)

    ops.append({"action": "freeze", "args": {"tab": "Budget", "rows": 2}})
    return ops, TOTAL


def build_dashboard(budget_total_row):
    """Repoint Dashboard at the rebuilt Budget tab and at the real pot names.

    Two live bugs this fixes, both silent:

      - "Obligations floor / month" read Budget!$B$18. After the Budget tab was
        rebuilt, B18 stopped being the plan total and became Personal / misc.
        The Dashboard was reporting a ₦10,000 monthly floor against a real one
        of ₦951,700, so "income needed to hit the goal" was understated by about
        ₦940,000.

      - The pot rows summed Transfers where the pot was "Savings", "Emergency"
        or "Investment". The pots were renamed to "Goal 1 — house", "Emergency
        fund" and "Cowrywise investment", and those are the names the Transfers
        dropdown now writes. The old SUMIFS could never match again, so the
        Dashboard would have shown ₦0 saved however much money actually moved —
        exactly the class of lie money.md Rule 6 exists to stop.

    Rewrites rows 5-10 in place rather than inserting, so re-running this script
    can never grow the tab. Everything from row 11 down keeps its position; only
    the references that pointed at the old SAVED row are repointed.
    """
    def pot(name, opening=None):
        """Opening balance (Setup) plus everything Transfers has moved since.

        The opening term matters: Cowrywise already held ₦305,000 on the day
        tracking started, and no Transfers row will ever account for it.
        """
        base = "%s+" % opening if opening else ""
        return ('=%sSUMIFS(%s,%s,"%s",%s,"To pot")-SUMIFS(%s,%s,"%s",%s,"From pot")'
                % (base, TRF[0], TRF[1], name, TRF[2], TRF[0], TRF[1], name, TRF[2]))

    bank = ('=Setup!$B$5+SUM(%s)-SUM(%s)'
            '-SUMIFS(%s,%s,"To pot")+SUMIFS(%s,%s,"From pot")'
            % (INC[0], EXP[0], TRF[0], TRF[2], TRF[0], TRF[2]))

    labels = [
        ["Bank — liquid"],
        ["Goal 1 — house"],
        ["Emergency fund"],
        ["Cowrywise investment"],
        ["Buffer"],
        ["SAVED TOWARD THE GOAL"],
    ]
    notes = [
        ["Everything you can actually spend. Opening balance, plus Income, minus Expenses, "
         "minus what moved into the pots."],
        ["Counts toward the ₦1,000,000."],
        ["Counts toward the goal. Starts Jan 2027, after Goal 1 closes."],
        ["RING-FENCED. Does NOT count toward either goal — Rule 7."],
        ["The in-month cushion urgencies come out of. Deliberately NOT counted below: "
         "it is money meant to be spent, not saved."],
        ["Goal 1 + Emergency fund. The investment and the buffer are both excluded, on purpose."],
    ]

    ops = [
        {"action": "write", "args": {"tab": "Dashboard", "cell": "A5", "values": labels}},
        {"action": "write", "args": {"tab": "Dashboard", "cell": "D5", "values": notes}},
        {"action": "setFormulas", "args": {"tab": "Dashboard", "cell": "B5", "formulas": [
            [bank],
            [pot("Goal 1 — house",        "Setup!$B$6")],
            [pot("Emergency fund",        "Setup!$B$7")],
            [pot("Cowrywise investment",  "Setup!$B$8")],
            [pot("Buffer")],                      # new pot, no opening balance
            ["=$B$6+$B$7"],
        ]}},

        # rows 11+ kept their positions; the old SAVED row was 9, it is now 10
        {"action": "setFormulas", "args": {"tab": "Dashboard", "cell": "B13",
            "formulas": [["=$B$10"]]}},
        {"action": "setFormulas", "args": {"tab": "Dashboard", "cell": "B14",
            "formulas": [["=MAX(0,Setup!$B$11-$B$10)"]]}},
        {"action": "setFormulas", "args": {"tab": "Dashboard", "cell": "B16",
            "formulas": [['=IF(Setup!$B$12<=TODAY(),0,MAX(0,Setup!$B$11-$B$10)'
                          '/MAX(1,(Setup!$B$12-TODAY())/30.4))']]}},
        {"action": "setFormulas", "args": {"tab": "Dashboard", "cell": "B21",
            "formulas": [['=IF(Setup!$B$14<=TODAY(),0,(Setup!$B$11+Setup!$B$13-$B$10)'
                          '/MAX(1,(Setup!$B$14-TODAY())/30.4))']]}},

        # the reality check, pointed at the real plan total
        {"action": "setFormulas", "args": {"tab": "Dashboard", "cell": "B26",
            "formulas": [["=Budget!$B$%d" % budget_total_row]]}},
        {"action": "write", "args": {"tab": "Dashboard", "cell": "D26", "values": [[
            "TOTAL SPENT, Plan column on Budget (row %d). The whole recurring baseline."
            % budget_total_row]]}},

        {"action": "format", "args": {"tab": "Dashboard", "range": "B5:B10",
                                      "numberFormat": NGN}},
        {"action": "format", "args": {"tab": "Dashboard", "range": "A10:D10",
                                      "background": PAPER, "bold": True}},
        {"action": "format", "args": {"tab": "Dashboard", "range": "D5:D10",
                                      "fontColor": MUTED, "fontSize": 9, "wrap": True}},

        # Setup's label for the same pot, so the two tabs agree
        {"action": "write", "args": {"tab": "Setup", "cell": "A6",
                                     "values": [["Goal 1 — house"]]}},
        {"action": "write", "args": {"tab": "Setup", "cell": "C6", "values": [[
            "Does not exist yet. Build it OUTSIDE the investment. This is the ₦1M pot."]]}},
    ]
    return ops


def build_setup():
    """Refresh the category and pot lists so the dropdowns match reality."""
    cats = [[c] for c in CATEGORIES]
    pots = [["Goal 1 — house"], ["Cowrywise investment"], ["Buffer"],
            ["Goal 2 — marriage"], ["Emergency fund"]]
    return [
        {"action": "clear", "args": {"tab": "Setup", "range": "I2:I20", "contentsOnly": True}},
        {"action": "clear", "args": {"tab": "Setup", "range": "K2:K20", "contentsOnly": True}},
        {"action": "write", "args": {"tab": "Setup", "cell": "I2", "values": cats}},
        {"action": "write", "args": {"tab": "Setup", "cell": "K2", "values": pots}},
        # Rule 3, amended for the two-payday reality
        {"action": "write", "args": {"tab": "Setup", "cell": "A25", "values": [[
            "3. Savings move ON A PAYDAY, the day the money lands — never at month end. "
            "Cowrywise on Payday A. Goal 1 and the Buffer on Payday B (Samuel's call 2026-08-26: "
            "Payday A is always full). EXCEPTION: if Payday A leaves more than ₦50,000 free "
            "after its commitments, that excess moves the same day. Six figures sitting loose for "
            "14 days is how ₦595,250 disappeared."]]}},
        {"action": "format", "args": {"tab": "Setup", "range": "A25", "wrap": True}},
        # dropdowns on the log tabs
        {"action": "validation", "args": {"tab": "Expenses", "range": "C5:C404",
                                          "list": CATEGORIES}},
        {"action": "validation", "args": {"tab": "Transfers", "range": "C5:C404",
                                          "list": [p[0] for p in pots]}},
    ]


def main():
    plan = load_plan()
    ops = []
    d_ops, d_range = build_details(plan)
    ops += d_ops
    b_ops, budget_total_row = build_budget(plan, d_range)
    ops += b_ops
    ops += build_setup()
    ops += build_dashboard(budget_total_row)

    payload = os.path.join(HERE, "_build_ops.json")
    with open(payload, "w", encoding="utf-8") as fh:
        json.dump({"ops": ops}, fh, ensure_ascii=False)

    print("%d operations queued" % len(ops))
    r = subprocess.run([sys.executable, os.path.join(HERE, "sheets.py"), "ops", payload],
                       cwd=REPO)
    os.remove(payload)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
