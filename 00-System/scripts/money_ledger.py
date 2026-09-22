#!/usr/bin/env python3
"""
Totals from the money ledger and the delivered-projects record, so no agent
reads either file whole (AGENTS.md rule 10). Stdlib only. Read-only: it never
writes a file.

    python 00-System/scripts/money_ledger.py totals 2026-10   # a month: in, out, pots, categories
    python 00-System/scripts/money_ledger.py pots             # pot balances + derived bank, as of the last row
    python 00-System/scripts/money_ledger.py last 10          # the last N ledger rows
    python 00-System/scripts/money_ledger.py videos 2026-10   # delivered videos in a batch month, USD total

Ledger:    03-Areas/finances/money-ledger.md   (row types are defined there)
Delivered: 03-Areas/video-editing/delivered-projects.md   (owned by the video-editor)

Every figure it prints is derived from rows, and says "as of" the last row's
date. It is never a current balance (finance agent hard limit).
"""

import os
import sys
from collections import OrderedDict, defaultdict

BRAIN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER = os.path.join(BRAIN, "03-Areas", "finances", "money-ledger.md")
DELIVERED = os.path.join(BRAIN, "03-Areas", "video-editing", "delivered-projects.md")

POTS = ["Goal 1", "Buffer", "Cowrywise investment", "Emergency fund", "Goal 2"]
OUT_TYPES = ("major", "bulk", "charges")
TYPES = ("opening", "in", "major", "bulk", "to-pot", "from-pot", "charges", "balance", "correction")


def table_rows(path, first_header):
    """Rows of the first markdown table whose first header cell is `first_header`."""
    if not os.path.exists(path):
        sys.exit("missing: %s" % os.path.relpath(path, BRAIN))
    rows, header, inside = [], None, False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("|"):
                if inside:
                    break
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if header is None:
                if cells and cells[0] == first_header:
                    header, inside = cells, True
                continue
            if set("".join(cells)) <= set("-: "):
                continue
            rows.append(dict(zip(header, cells)))
    if header is None:
        sys.exit("no table starting with '%s' in %s" % (first_header, os.path.relpath(path, BRAIN)))
    return rows


def ngn(cell):
    cell = cell.replace(",", "").replace("NGN", "").strip()
    if cell in ("", "—", "-"):
        return None
    try:
        return float(cell)
    except ValueError:
        return None


def ledger():
    """Every counted row, in date order (file order within a date)."""
    rows = table_rows(LEDGER, "Date")
    bad = [r for r in rows if r.get("Type") not in TYPES]
    for r in bad:
        print("WARNING: unknown row type %r on %s — not counted" % (r.get("Type"), r.get("Date")))
    rows = [r for r in rows if r.get("Type") in TYPES]
    return sorted(rows, key=lambda r: r["Date"][:10])


def position(rows=None):
    """Pot balances and the derived bank, as of the last money row.

    The starting position is the set of `opening` rows with the EARLIEST date.
    A later `opening` row is a checkpoint: it is compared with the running
    figure at the end of its day and never applied (ledger note, 2026-09-22).
    Returns (as_of, bank, balances, checkpoint_mismatches).
    """
    rows = ledger() if rows is None else rows
    opens = [r["Date"][:10] for r in rows if r["Type"] == "opening"]
    start = min(opens) if opens else None
    is_check = lambda r: r["Type"] == "opening" and r["Date"][:10] != start
    rows = sorted(rows, key=lambda r: (r["Date"][:10], is_check(r)))
    bal = OrderedDict((p, None) for p in POTS)
    bank, mismatches = None, []
    for r in rows:
        t, amt, what, cat = r["Type"], ngn(r["NGN"]), r["What"], r["Category"]
        if amt is None:
            continue
        if is_check(r):
            have = bal.get(what) if what in POTS else bank
            if have is None or abs(have - amt) > 0.5:
                mismatches.append("%s checkpoint %s: ledger says %s, rows add up to %s"
                                  % (r["Date"][:10], what, fmt(amt), "nothing" if have is None else fmt(have)))
            continue
        if t in ("opening", "balance"):
            if what in POTS:
                bal[what] = amt
            else:
                bank = amt
        elif t == "in":
            bank = (bank or 0) + amt
        elif t in OUT_TYPES:
            bank = (bank or 0) - amt
        elif t == "to-pot":
            bal[cat] = (bal.get(cat) or 0) + amt
            bank = (bank or 0) - amt
        elif t == "from-pot":
            bal[cat] = (bal.get(cat) or 0) - amt
            bank = (bank or 0) + amt
    money = [r for r in rows if r["Type"] != "correction"]
    as_of = money[-1]["Date"][:10] if money else ""
    return as_of, bank, bal, mismatches


def fmt(x):
    return "NGN {:,.0f}".format(x)


def totals(month):
    rows = [r for r in ledger() if r["Date"][:7] == month]
    if not rows:
        print("No ledger rows for %s." % month)
        return
    by_type = defaultdict(float)
    to_pot, from_pot, by_cat = defaultdict(float), defaultdict(float), defaultdict(float)
    corrections = []
    for r in rows:
        amt = ngn(r["NGN"])
        if r["Type"] == "correction":
            corrections.append(r)
            continue
        if amt is None or r["Type"] in ("opening", "balance"):
            continue
        by_type[r["Type"]] += amt
        if r["Type"] == "to-pot":
            to_pot[r["Category"]] += amt
        elif r["Type"] == "from-pot":
            from_pot[r["Category"]] += amt
        elif r["Type"] in OUT_TYPES:
            by_cat[r["Category"] or "—"] += amt
    spent = sum(by_type[t] for t in OUT_TYPES)
    print("%s — from %d ledger rows, last dated %s" % (month, len(rows), rows[-1]["Date"]))
    print("  In               %s" % fmt(by_type["in"]))
    print("  Out (spent)      %s   = major %s + bulk %s + charges %s"
          % (fmt(spent), fmt(by_type["major"]), fmt(by_type["bulk"]), fmt(by_type["charges"])))
    print("  Moved to pots    %s" % fmt(by_type["to-pot"]))
    for p, a in to_pot.items():
        print("      %-22s %s" % (p, fmt(a)))
    if from_pot:
        print("  TAKEN FROM POTS  %s" % fmt(by_type["from-pot"]))
        for p, a in from_pot.items():
            print("      %-22s %s" % (p, fmt(a)))
    print("  In − out − pots + withdrawals = %s"
          % fmt(by_type["in"] - spent - by_type["to-pot"] + by_type["from-pot"]))
    if by_cat:
        print("  Spent by category:")
        for c, a in sorted(by_cat.items(), key=lambda kv: -kv[1]):
            print("      %-22s %s" % (c, fmt(a)))
    if corrections:
        print("  %d correction note(s) this month (a money fix is a minus row of the same type):" % len(corrections))
        for r in corrections:
            print("      %s  %s" % (r["Date"], r["What"]))


def pots():
    as_of, bank, bal, mismatches = position()
    print("As of the last ledger row, %s. Derived from rows — not a current balance." % as_of)
    for p, a in bal.items():
        print("  %-22s %s" % (p, "not started" if a is None else fmt(a)))
    print("  %-22s %s" % ("Bank (derived)", "unknown" if bank is None else fmt(bank)))
    print("  Saved toward Goal 1 counts Goal 1 + Emergency fund only. The investment and the Buffer never count (Rule 7).")
    for m in mismatches:
        print("  CHECKPOINT MISMATCH: " + m)


def last(n):
    rows = ledger()[-n:]
    for r in rows:
        print("| %s | %s | %s | %s | %s | %s |" % (r["Date"], r["Type"], r["NGN"], r["What"], r["Category"], r["Note"]))


def videos(month):
    rows = [r for r in table_rows(DELIVERED, "#") if r.get("Batch") == month]
    usd = [ngn(r.get("Rate USD", "")) for r in rows]
    unknown = sum(1 for u in usd if u is None)
    print("%s batch — %d video(s) delivered, USD %s gross%s"
          % (month, len(rows), "{:,.2f}".format(sum(u for u in usd if u)),
             ", %d with no rate recorded" % unknown if unknown else ""))
    for r in rows:
        print("  %s  %s  (%s, USD %s)" % (r.get("Delivered"), r.get("Project"), r.get("End client"), r.get("Rate USD")))
    print("  Gross only. Paid 70% at month end, 30% mid next month; charges and the Cleva rate are not known until it lands.")


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if not argv:
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "totals" and len(argv) == 2:
        totals(argv[1])
    elif cmd == "pots":
        pots()
    elif cmd == "last":
        last(int(argv[1]) if len(argv) > 1 else 10)
    elif cmd == "videos" and len(argv) == 2:
        videos(argv[1])
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
