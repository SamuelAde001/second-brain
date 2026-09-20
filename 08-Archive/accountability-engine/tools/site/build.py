#!/usr/bin/env python3
"""
Samuelsignals OS — build the site's data layer.

WHY IT WORKS THIS WAY
---------------------
`context/*.md` stays the SOURCE OF TRUTH. This script derives the site from it.

That is the same rule as tools/scorecard/build.py, and it exists for the same
reason: generated output is never hand-written, so it can never drift from the
record. It also means the whole site inherits git's append-only guarantee for
free — you cannot silently soften a 40% day, because the day lives in a committed
markdown file and the site is just a view of it.

Nothing here writes to context/. If a number is wrong on the site, the fix is in
context/, never in site/data/.

    python tools/site/build.py            # build
    python tools/site/build.py --check    # parse and report, write nothing

Stdlib only. Runs here, in a cloud routine, and in CI unchanged.
"""

import hashlib
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CTX = REPO / "context"
OUT = REPO / "site" / "data"

WARNINGS = []   # the SITE is wrong: it does not match context/
GAPS = []       # the RECORD is thin: context/ is behind real life


def warn(msg):
    """The site is out of step with context/. A build or data problem. Fix it here."""
    WARNINGS.append(msg)


def gap(msg):
    """context/ is behind reality — a day not logged, a balance not given.

    Split from warn() on 2026-09-02, because conflating the two made the dashboard
    shout "THIS RECORD IS OUT OF SYNC" about things the site was rendering perfectly.
    A missing money row is not a site failure; it is a reckoning that has not been
    run yet. The two need different words because they need different actions:
    a warning is fixed by building, a gap is closed by logging.
    """
    GAPS.append(msg)


# ---------------------------------------------------------------- primitives

def parse_duration(text):
    """'5.95h' '16.23h' '18m43s' '5h21m35s' '5h21m' '0h' -> float hours, or None.

    The ledger is written by a human at 9pm, so it carries every one of these
    shapes. Be tolerant here rather than losing a day's focus figure to a regex.
    """
    if not text:
        return None
    t = text.strip().lower().replace("~", "")
    if not t or t in {"—", "-", "none", "n/a"}:
        return None

    # 5h21m35s / 5h21m / 18m43s / 45s
    m = re.search(r"(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?", t)
    if m and any(m.groups()) and re.search(r"[hms]", t):
        h = int(m.group(1) or 0)
        mi = int(m.group(2) or 0)
        s = int(m.group(3) or 0)
        # A bare "5.95h" lands here with h=5 and loses the decimal, so only take
        # this branch when there is no decimal point attached to the hours.
        if not re.search(r"\d+\.\d+\s*h", t):
            total = h + mi / 60 + s / 3600
            if total > 0:
                return round(total, 4)

    m = re.search(r"(\d+(?:\.\d+)?)\s*h", t)
    if m:
        return round(float(m.group(1)), 4)

    m = re.search(r"^(\d+(?:\.\d+)?)$", t)
    if m:
        return round(float(m.group(1)), 4)
    return None


def parse_focus_cell(cell):
    """'5.95h / 14.7h = 40%' -> (5.95, 14.7). '0h logged' -> (0.0, None)."""
    if not cell:
        return None, None
    c = cell.strip()
    if c in {"", "—", "-"}:
        return None, None
    parts = c.split("/")
    logged = parse_duration(parts[0]) if parts else None
    committed = parse_duration(parts[1]) if len(parts) > 1 else None
    if logged is None and re.search(r"\b0h\b", c):
        logged = 0.0
    return logged, committed


def parse_habits_cell(cell):
    """'5/5' -> (5,5). '3/5 (social media + M broken...)' -> (3,5)."""
    if not cell:
        return None, None
    m = re.search(r"(\d+)\s*/\s*(\d+)", cell)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def parse_bed_cell(cell):
    """'1:42am (19h day)' -> ('01:42', 19.0). '—' -> (None, None).

    Returns 24h HH:MM plus any sleep-hours figure the row happened to carry.
    """
    if not cell:
        return None, None
    c = cell.strip()
    if c in {"", "—", "-"}:
        return None, None

    bed = None
    m = re.search(r"(\d{1,2}):(\d{2})\s*(am|pm)", c, re.I)
    if m:
        h, mi, ap = int(m.group(1)), int(m.group(2)), m.group(3).lower()
        if ap == "pm" and h != 12:
            h += 12
        if ap == "am" and h == 12:
            h = 0
        bed = f"{h:02d}:{mi:02d}"

    # The parenthetical after a bed time is USUALLY sleep — "1:30am (4h)" — but not
    # always: "1:42am (19h day)" is the length of the WORKING day, and reading it as
    # 19 hours of sleep pushed the site's average to 8h45m on a record whose real
    # nights were 4h, 5.5h and 6.5h. A comforting number, confidently wrong, shown
    # on the one page about the thing everything else stands on. Found 2026-09-02.
    slept = None
    m = re.search(r"\(\s*~?\s*(\d+(?:\.\d+)?)\s*h([^)]*)\)", c)
    if m:
        qualifier = (m.group(2) or "").lower()
        val = float(m.group(1))
        if any(w in qualifier for w in ("day", "span", "awake", "work")):
            slept = None          # a day length, not a night
        elif 0 < val <= 14:
            slept = val
        else:
            warn(f"IMPLAUSIBLE SLEEP VALUE IGNORED: {val}h parsed from bed cell {c!r}")
    return bed, slept


def md_table_rows(text):
    """Yield lists of cell strings for every pipe row that isn't a separator."""
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if re.match(r"^\|[\s\-:|]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        yield cells


DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


# ------------------------------------------------------------------- parsers

def parse_ledger():
    """context/ledger.md -> one dict per DATE. Later rows win (the 26 Aug interim
    row is superseded by that evening's final row)."""
    path = CTX / "ledger.md"
    if not path.exists():
        warn("ledger.md missing")
        return []
    rows = {}
    order = []
    for cells in md_table_rows(path.read_text(encoding="utf-8")):
        if not cells or not DATE_RE.match(cells[0]):
            continue
        d = DATE_RE.match(cells[0]).group(1)
        interim = "interim" in cells[0].lower()
        g = lambda i: cells[i] if len(cells) > i else ""
        logged, committed_h = parse_focus_cell(g(3))
        hit, hset = parse_habits_cell(g(4))
        bed, slept = parse_bed_cell(g(5))
        verdict = (g(6) or "").strip().upper()
        if verdict.startswith("IN PROGRESS"):
            verdict = "OPEN"
        if not verdict:
            verdict = "OPEN"

        row = {
            "date": d,
            "committed": g(1),
            "shipped": g(2),
            "focus_logged": logged,
            "focus_committed": committed_h,
            "habits_hit": hit,
            "habits_set": hset,
            "bed": bed,
            "slept": slept,
            "verdict": verdict,
            "interim": interim,
        }
        if d in rows and interim:
            continue  # never let an interim overwrite a final row
        if d not in rows:
            order.append(d)
        rows[d] = row
    return [rows[d] for d in order]


def parse_money_ledger():
    path = CTX / "money-ledger.md"
    if not path.exists():
        warn("money-ledger.md missing")
        return []
    out = []
    for cells in md_table_rows(path.read_text(encoding="utf-8")):
        if not cells or not DATE_RE.match(cells[0]):
            continue
        g = lambda i: cells[i] if len(cells) > i else ""

        def money(s):
            s = (s or "").replace(",", "").replace("₦", "").strip()
            m = re.search(r"(-?\d+(?:\.\d+)?)", s)
            return float(m.group(1)) if m else None

        out.append({
            "date": DATE_RE.match(cells[0]).group(1),
            "label": cells[0],
            "balance": money(g(1)),
            "in": money(g(2)),
            "out_text": g(3),
            "savings_moved": money(g(4)) or 0,
            "note": g(5),
        })
    return out


def parse_habits():
    """The habit table in context/habits.md, plus any running fast/detox block."""
    path = CTX / "habits.md"
    if not path.exists():
        warn("habits.md missing")
        return {"habits": [], "blocks": []}
    text = path.read_text(encoding="utf-8")
    habits = []
    for cells in md_table_rows(text):
        if len(cells) < 4:
            continue
        name, cadence, check, hid = cells[0], cells[1], cells[2], cells[3]
        if name.lower() in {"habit", ""} or "---" in name:
            continue
        if not re.match(r"^[0-9a-f]{16,}$", hid.strip()):
            continue
        habits.append({
            "name": name,
            "cadence": cadence,
            "check": check,
            "ticktick_id": hid.strip(),
        })

    blocks = []
    for m in re.finditer(r"##\s+The\s+(.+?)\s+\((\d{1,2})[–-](\d{1,2})\s+(\w+)\s+(\d{4})\)", text):
        blocks.append({"name": m.group(1), "from_day": int(m.group(2)),
                       "to_day": int(m.group(3)), "month": m.group(4), "year": int(m.group(5))})
    return {"habits": habits, "blocks": blocks}


def parse_patterns():
    path = CTX / "patterns.md"
    if not path.exists():
        warn("patterns.md missing")
        return []
    text = path.read_text(encoding="utf-8")
    out = []
    chunks = re.split(r"\n##\s+", text)
    for chunk in chunks[1:]:
        head, _, body = chunk.partition("\n")
        m = re.match(r"(P\d+)\s*[—-]\s*(.+)", head.strip())
        if not m:
            continue
        pid, name = m.group(1), m.group(2).strip()
        status = "candidate" if "candidate" in name.lower() else "active"
        name = re.sub(r"\s*\(candidate.*?\)", "", name, flags=re.I).strip()
        body = body.strip()
        ev = ""
        me = re.search(r"Evidence:(.*)", body, re.S)
        if me:
            ev = " ".join(me.group(1).split())
            body = body[: me.start()].strip()
        out.append({
            "id": pid,
            "name": name,
            "status": status,
            "mechanism": " ".join(body.split()),
            "evidence": ev,
        })
    return out


def parse_ledger_notes():
    """ledger-notes/*.md -> {date: narrative}."""
    notes = {}
    d = CTX / "ledger-notes"
    if not d.exists():
        return notes
    for f in sorted(d.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        for chunk in re.split(r"\n##\s+", text)[1:]:
            head, _, body = chunk.partition("\n")
            m = DATE_RE.match(head.strip())
            if not m:
                continue
            key = m.group(1)
            body = body.strip().rstrip("-").strip()
            # A FINAL row supersedes the interim one written earlier that day.
            if key in notes and "FINAL" not in head:
                continue
            notes[key] = body
    return notes


TODAY = date.today().isoformat()

BUDGET_MONTHS = ["2026-08", "2026-09", "2026-10", "2026-11", "2026-12",
                 "2027-01", "2027-02", "2027-03", "2027-04", "2027-05",
                 "2027-06", "2027-07"]


def parse_spend():
    """context/spend.jsonl — the structured twin of the ledger's spend prose.

    The ledger's Out column is a sentence, so nothing could add it up and every
    category on the Budget page read N0. Same facts, same words, one JSON object
    per line, and the same rows that go to the sheet's Expenses tab.
    """
    path = CTX / "spend.jsonl"
    if not path.exists():
        return []
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            warn("spend.jsonl line %d is not valid JSON" % n)
            continue
        if "_comment" in row:
            continue
        if not (row.get("date") and row.get("category") and row.get("amount") is not None):
            warn("spend.jsonl line %d needs date, category and amount" % n)
            continue
        if not DATE_RE.match(row["date"]):
            warn("spend.jsonl line %d has a bad date: %s" % (n, row["date"]))
            continue
        out.append(row)
    return out


def parse_budget_plan(income=None, paydays=None):
    path = REPO / "tools" / "sheets" / "plan.json"
    if not path.exists():
        warn("tools/sheets/plan.json missing")
        return {}
    plan = json.loads(path.read_text(encoding="utf-8"))
    items = []
    for r in plan.get("recurring", []):
        cat, item, amt, tier, payday, due, active, note = (r + [""] * 8)[:8]
        items.append({"category": cat, "item": item, "amount": amt, "tier": tier,
                      "payday": payday, "due": due,
                      "active": str(active).lower().startswith("y"),
                      "month": None, "note": note})
    for month, rows in (plan.get("one_offs") or {}).items():
        for r in rows:
            cat, item, amt, tier, payday, due, active, note = (r + [""] * 8)[:8]
            items.append({"category": cat, "item": item, "amount": amt, "tier": tier,
                          "payday": payday, "due": due,
                          "active": str(active).lower().startswith("y"),
                          "month": month, "note": note})
    savings = plan.get("savings", [])
    spend = parse_spend()

    # Which categories the plan knows about. A spend row outside this set is a
    # real signal, not a typo to swallow: it is money leaving under a name the
    # budget never planned for.
    known = {i["category"] for i in items if i["active"]}
    known |= {"Savings — " + v["pot"] for v in savings}

    # A ledger day that reports money out but has no spend.jsonl rows is the
    # failure that made this file necessary in the first place: on 2026-09-02
    # the reckoning wrote N750,250 of transfers to the ledger and the sheet,
    # and the Budget page went on saying N0 paid because nothing wrote here.
    # It is a RECORD GAP, not a build error - the fix is to log the rows, never
    # to change the page.
    _spend_days = {r["date"] for r in spend}
    for _row in parse_money_ledger():
        _out = (_row.get("out_text") or "").strip().lower()
        if not _out or _out.startswith("nothing out") or _out.startswith("unreported"):
            continue
        if _row["date"] < (plan.get("plan_start") or "") + "-01":
            continue
        if _row["date"] not in _spend_days:
            gap("SPEND NOT ITEMISED: %s reports money out in money-ledger.md but has no "
                "rows in spend.jsonl, so the Budget page counts it as unpaid" % _row["date"])
    for r in spend:
        if r["category"] not in known:
            warn("spend.jsonl: category %r is not in plan.json" % r["category"])

    # THE MONTH MUST BALANCE. Derived here, never typed: income minus bills
    # minus that month's one-offs minus every pot. A month that does not end at
    # zero is not planned, it is estimated — and the leftover is money with no
    # name on it, which is exactly what evaporated June-August.
    bills = sum(i["amount"] for i in items if i["active"] and not i["month"])
    one_by_month = {}
    for i in items:
        if i["active"] and i["month"]:
            one_by_month[i["month"]] = one_by_month.get(i["month"], 0) + i["amount"]
    # NET, not gross. A flat charge is taken per payment and there are two
    # payments a month, so a month's cash is the batch less 2 x the charge.
    # Confirmed to the cent on 2026-09-02: $711.66 invoiced, $706.66 received.
    # This was gross until then, which overstated every month by ~17,000.
    gross = 0
    if income:
        usd = (2 * income["rate_primary_usd"] + 2 * income["rate_secondary_usd"]
               - 2 * income.get("charge_usd", 0))
        gross = round(usd * income["usd_ngn"])
    plan_start = plan.get("plan_start") or BUDGET_MONTHS[0]
    balance = []
    for m in BUDGET_MONTHS:
        if m < plan_start:
            continue
        pots = sum(v["schedule"].get(m, 0) for v in savings)
        one = one_by_month.get(m, 0)
        balance.append({
            "month": m,
            "income": gross,
            "bills": bills,
            "one_offs": one,
            "pots": pots,
            "pot_split": {v["pot"]: v["schedule"][m] for v in savings if m in v["schedule"]},
            "left": gross - bills - one - pots,
        })
    # ---------------------------------------------------------- actuals ----
    # Everything below is DERIVED. Nothing is typed, so it moves the moment a
    # spend row is logged, a plan line changes or a payday amount is corrected.
    paydays = paydays or []

    # A payday belongs to the month it FUNDS, not the month it lands in.
    # Payday A is the 70% arriving at the end of the previous month, so
    # 30 Sep funds October. Matching on the date put ~N962,000 of October's
    # money into September's expected income. The labels already carry the
    # month they fund ("Payday A - October"), so read that instead.
    MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]

    def funds_month(pd):
        # Read the month straight after "Payday A - ". Scanning the whole label
        # for any month name matches the wrong one: "Payday A - September
        # (August 70%)" names two months, and the batch's month is not the
        # month it funds.
        mo = re.match(r"\s*Payday\s+[AB]\s*[—–-]\s*([A-Za-z]+)", pd.get("label") or "")
        if mo and mo.group(1) in MONTH_NAMES:
            want = MONTH_NAMES.index(mo.group(1)) + 1
            for m in BUDGET_MONTHS:
                if int(m[5:7]) == want:
                    return m
        return (pd.get("date") or "")[:7]

    def money_in(month):
        got = still = 0
        for pd in paydays:
            if funds_month(pd) != month:
                continue
            amt = pd.get("amount") or 0
            if pd.get("confirmed") and (pd.get("date") or "") <= TODAY:
                got += amt
            else:
                still += amt
        return got, still

    months_out = {}
    for m in BUDGET_MONTHS:
        if m < plan_start:
            continue
        rows = [r for r in spend if r["date"].startswith(m)]
        paid_by_cat = {}
        for r in rows:
            paid_by_cat[r["category"]] = paid_by_cat.get(r["category"], 0) + r["amount"]

        # Plan for this month, per category, split by payday.
        plan_by_cat = {}
        for i in items:
            if not i["active"] or (i["month"] and i["month"] != m):
                continue
            e = plan_by_cat.setdefault(i["category"], {"A": 0, "B": 0})
            e[i["payday"] if i["payday"] in ("A", "B") else "B"] += i["amount"]
        for v in savings:
            amt = v["schedule"].get(m, 0)
            if not amt:
                continue
            e = plan_by_cat.setdefault("Savings — " + v["pot"], {"A": 0, "B": 0})
            e[v.get("payday") if v.get("payday") in ("A", "B") else "B"] += amt

        # Attribute what was PAID against the plan, filling Payday A's share
        # first and spilling into B. Not by the date it was spent: a category
        # planned on B that gets paid on the 3rd must still reduce B's
        # still-to-pay, or the cushion figure lies.
        cats = []
        for cat in sorted(set(list(plan_by_cat) + list(paid_by_cat))):
            pl = plan_by_cat.get(cat, {"A": 0, "B": 0})
            paid = paid_by_cat.get(cat, 0)
            pa = min(paid, pl["A"])
            pb = min(paid - pa, pl["B"])
            over = paid - pa - pb
            cats.append({
                "category": cat, "planned": pl["A"] + pl["B"],
                "planned_a": pl["A"], "planned_b": pl["B"],
                "paid": paid, "paid_a": pa, "paid_b": pb, "unplanned": over,
                "left": pl["A"] + pl["B"] - paid,
                "is_pot": cat.startswith("Savings — "),
            })

        got, still = money_in(m)
        agg = lambda k: sum(c[k] for c in cats)
        budget_a, budget_b = agg("planned_a"), agg("planned_b")
        paid_a, paid_b = agg("paid_a"), agg("paid_b")
        months_out[m] = {
            "month": m,
            "categories": cats,
            "income_expected": got + still,
            "income_received": got,
            "income_to_come": still,
            "budget_a": budget_a, "budget_b": budget_b,
            "budget_total": budget_a + budget_b,
            "paid_a": paid_a, "paid_b": paid_b,
            "paid_total": agg("paid"),
            "unplanned": agg("unplanned"),
            "left_a": budget_a - paid_a, "left_b": budget_b - paid_b,
            "left_total": (budget_a + budget_b) - (paid_a + paid_b),
            "cushion_a": None, "cushion_b": None,
            "spend_rows": [r for r in rows],
        }
        for pd in paydays:
            if funds_month(pd) != m:
                continue
            L = pd.get("label") or ""
            if L.startswith("Payday A") and months_out[m]["cushion_a"] is None:
                months_out[m]["cushion_a"] = (pd.get("amount") or 0) - budget_a
            if L.startswith("Payday B") and months_out[m]["cushion_b"] is None:
                months_out[m]["cushion_b"] = (pd.get("amount") or 0) - budget_b

    return {
        "plan_start": plan.get("plan_start"),
        "tracking_start": plan.get("tracking_start"),
        "today": TODAY,
        "months": months_out,
        "spend": spend,
        "items": items,
        "savings": savings,
        "balance": balance,
        "bills_total": bills,
        "lean_ladder": plan.get("lean_month_ladder", []),
    }


# --------------------------------------------------------------------- score

def behaviour_score(row, cfg):
    """The formula Samuel approved 2026-08-28. Returns (score, components).

    Missing data RESCALES rather than scoring zero — a day with no sleep figure
    is not a day he slept badly, it is a day nobody asked.
    """
    w = cfg["weights"]
    comp = {}
    avail = 0
    earned = 0.0

    v = (row.get("verdict") or "").upper()
    if v in cfg["verdict_points"]:
        pts = cfg["verdict_points"][v]
        comp["verdict"] = {"points": pts, "of": w["verdict"]}
        avail += w["verdict"]
        earned += pts

    fl, fc = row.get("focus_logged"), row.get("focus_committed")
    if fl is not None and fc:
        raw = min(fl / fc, 1.0) * w["focus"]
        # >12h is not a good day, it is an invoice. body.md Rule 5.
        pts = min(raw, cfg["focus_over_12h_cap"]) if fl > 12 else raw
        comp["focus"] = {"points": round(pts, 1), "of": w["focus"],
                         "ratio": round(fl / fc, 3), "capped": fl > 12}
        avail += w["focus"]
        earned += pts

    hh, hs = row.get("habits_hit"), row.get("habits_set")
    if hh is not None and hs:
        pts = hh / hs * w["habits"]
        comp["habits"] = {"points": round(pts, 1), "of": w["habits"]}
        avail += w["habits"]
        earned += pts

    bed = row.get("bed")
    if bed:
        h, mi = (int(x) for x in bed.split(":"))
        mins = h * 60 + mi
        if mins < 720:      # after midnight -> push past the previous evening
            mins += 1440
        pts = 20 if mins <= 22 * 60 + 30 else (10 if mins <= 23 * 60 + 30 else 0)
        comp["sleep"] = {"points": pts, "of": w["sleep"], "bed": bed}
        avail += w["sleep"]
        earned += pts

    if avail == 0:
        return None, comp

    base = earned / avail * 100
    pen = 0
    d = datetime.strptime(row["date"], "%Y-%m-%d").date()
    if d.weekday() == 2 and not row.get("content_shipped"):
        pen += cfg["penalties"]["no_wednesday_video"]
        comp["penalty_wednesday"] = -cfg["penalties"]["no_wednesday_video"]
    if row.get("money_due") and not row.get("money_moved"):
        pen += cfg["penalties"]["planned_money_did_not_move"]
        comp["penalty_money"] = -cfg["penalties"]["planned_money_did_not_move"]

    return max(round(base) - pen, 0), comp


# --------------------------------------------------------------------- build

def iso_week_start(d):
    return (d - timedelta(days=d.weekday())).isoformat()


def main():
    check_only = "--check" in sys.argv

    site = json.loads((CTX / "site.json").read_text(encoding="utf-8"))
    ledger = parse_ledger()
    notes = parse_ledger_notes()
    money = parse_money_ledger()
    habits = parse_habits()
    patterns = parse_patterns()
    budget = parse_budget_plan(site["income"], site["paydays"])

    # score + attach narrative
    for row in ledger:
        # Wednesday cadence has not started, so no Wednesday before it can be
        # penalised for a video that was never due.
        cadence = site["content"]["cadence_start"]
        row["content_due"] = row["date"] >= cadence
        row["content_shipped"] = False
        if not row["content_due"]:
            row["content_shipped"] = True  # suppresses the penalty, honestly
        row["money_due"] = False
        row["money_moved"] = False
        score, comp = behaviour_score(row, site["score"])
        row["score"] = score
        row["score_components"] = comp
        row["notes"] = notes.get(row["date"], "")
        row["week"] = iso_week_start(datetime.strptime(row["date"], "%Y-%m-%d").date())
        if row["focus_logged"] is not None and row["focus_committed"]:
            row["focus_pct"] = round(row["focus_logged"] / row["focus_committed"] * 100)
        else:
            row["focus_pct"] = None

    # weeks
    weeks = {}
    for row in ledger:
        wk = weeks.setdefault(row["week"], {
            "week": row["week"], "shipped": 0, "partial": 0, "missed": 0,
            "open": 0, "focus": 0.0, "scores": [], "days": 0,
        })
        wk["days"] += 1
        v = row["verdict"]
        wk["shipped" if v == "SHIPPED" else
           "partial" if v == "PARTIAL" else
           "missed" if v == "MISSED" else "open"] += 1
        if row["focus_logged"]:
            wk["focus"] += row["focus_logged"]
        if row["score"] is not None:
            wk["scores"].append(row["score"])
    for wk in weeks.values():
        wk["focus"] = round(wk["focus"], 2)
        wk["avg_score"] = round(sum(wk["scores"]) / len(wk["scores"])) if wk["scores"] else None
        del wk["scores"]

    closed = [r for r in ledger if r["verdict"] in {"SHIPPED", "PARTIAL", "MISSED"}]
    today = ledger[-1] if ledger else None

    bundle = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "profile": site["profile"],
        "score_config": site["score"],
        "sections": site["sections"],
        "ledger": ledger,
        "weeks": sorted(weeks.values(), key=lambda w: w["week"]),
        "money_ledger": money,
        "pots": site["pots"],
        "goals": site["goals"],
        "income": site["income"],
        "paydays": site["paydays"],
        "countdowns": site["countdowns"],
        "shopping": site.get("shopping") or {},
        "spirit": site.get("spirit", {}),
        "notes": site.get("notes", {}),
        "work": site.get("work", {}),
        "content": site["content"],
        "course": site["course"],
        "body": site["body"],
        "rules": site.get("rules", {}),
        "habits": habits,
        "habit_log": site.get("habit_log", {}),
        "patterns": patterns,
        # Raw markdown, shipped as-is and rendered client-side. This is what makes
        # "context/ is the source of truth" literally true rather than aspirational:
        # the prose on the site IS the file, not a retyped copy of it that drifts.
        "docs": {name: (CTX / f"{name}.md").read_text(encoding="utf-8")
                 for name in ("mission", "stakes", "spirit", "body", "people",
                              "audience", "money", "habits", "patterns", "ticktick")
                 if (CTX / f"{name}.md").exists()},
        "budget": budget,
        "summary": {
            "days_recorded": len(ledger),
            "days_closed": len(closed),
            "shipped": sum(1 for r in closed if r["verdict"] == "SHIPPED"),
            "partial": sum(1 for r in closed if r["verdict"] == "PARTIAL"),
            "missed": sum(1 for r in closed if r["verdict"] == "MISSED"),
            "total_focus": round(sum(r["focus_logged"] or 0 for r in ledger), 2),
            "last_score": next((r["score"] for r in reversed(closed)), None),
            "avg_score": (round(sum(r["score"] for r in closed if r["score"] is not None)
                                / max(1, len([r for r in closed if r["score"] is not None])))
                          if closed else None),
            "today": today["date"] if today else None,
            "nights_floor_hit": sum(
                1 for r in ledger if r["bed"] and
                (lambda m: m <= 22 * 60 + 30)(
                    (int(r["bed"][:2]) * 60 + int(r["bed"][3:])) + (1440 if int(r["bed"][:2]) * 60 + int(r["bed"][3:]) < 720 else 0))
            ),
            "nights_recorded": sum(1 for r in ledger if r["bed"]),
        },
        "warnings": WARNINGS,
        "gaps": GAPS,
    }

    # ------------------------------------------------------------------ STALENESS
    # Added 2026-09-02, his standing rule: "At all times the site must be in sync
    # with everything... If something doesn't show well, or isn't showing the
    # current stats, it must always be updated."
    #
    # A site that is merely OLD looks identical to a site that is CORRECT, which is
    # how the fasting anchors and three dead countdowns survived on the live pages
    # for days after the rules behind them were dropped. These checks make staleness
    # loud. They warn; they never block a build, because a stale record shown with a
    # warning still beats no record at all.
    _today = date.today().isoformat()

    if ledger:
        _last = ledger[-1]["date"]
        _gap = (date.fromisoformat(_today) - date.fromisoformat(_last)).days
        if _gap >= 1:
            gap(f"LEDGER IS {_gap} DAY(S) BEHIND: last row {_last}, today {_today}. "
                 "A day with no row is a gap, and gaps get named at the weekly review.")

    _as_of = (site.get("pots") or {}).get("as_of")
    if _as_of and ledger and _as_of < ledger[-1]["date"]:
        gap(f"POTS ARE STALE: balances as of {_as_of}, ledger runs to {ledger[-1]['date']}. "
             "The money figures on every page are older than the day being shown.")

    if money:
        _lastm = money[-1].get("date")
        if _lastm and _lastm < _today:
            _mg = (date.fromisoformat(_today) - date.fromisoformat(_lastm)).days
            if _mg >= 1:
                gap(f"MONEY LEDGER IS {_mg} DAY(S) BEHIND: last row {_lastm}.")

    # ---------------------------------------------- HARDCODED DATES IN THE UI
    # His rule, 2026-09-02: "Nothing should be hard coded, let it be easily
    # updatable once the data is updated... the frontend reads from the data."
    #
    # Prose may legitimately cite a past date ("the 19-hour day on 25 Aug").
    # A STATUS CARD may not — that is the part of the page that claims to say what
    # is true right now, and a stale one reads as current. So this only inspects
    # statCard(...) lines. The work page carried "Client #2 due — Sun 30 Aug" for
    # three days after it shipped; that is the failure this catches.
    _MONTHS = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,
               "aug":8,"sep":9,"sept":9,"oct":10,"nov":11,"dec":12}
    _pagedir = REPO / "site" / "assets" / "js" / "pages"
    _stale_ui = []
    if _pagedir.exists():
        for _f in sorted(_pagedir.glob("*.js")):
            for _ln, _line in enumerate(_f.read_text(encoding="utf-8").splitlines(), 1):
                if "statCard(" not in _line:
                    continue
                for _m in re.finditer(r"\b(\d{1,2})\s+([A-Z][a-z]{2,4})\b", _line):
                    _mon = _MONTHS.get(_m.group(2).lower())
                    if not _mon:
                        continue
                    try:
                        _d = date(date.today().year, _mon, int(_m.group(1)))
                    except ValueError:
                        continue
                    if _d < date.today():
                        _stale_ui.append(f"{_f.name}:{_ln} \"{_m.group(0)}\"")
    if _stale_ui:
        warn("HARDCODED PAST DATES IN STATUS CARDS: " + "; ".join(_stale_ui)
             + ". A status card must read from context/site.json, not from a literal "
               "in the page script — it goes stale silently and still looks current.")

    # Every notesFor(page, id) in a page script must resolve to an entry in
    # site.json -> notes. A missing one renders a visible marker on the page, but
    # this catches it before it ships.
    _notes = site.get("notes") or {}
    _missing_notes = []
    if _pagedir.exists():
        for _f in sorted(_pagedir.glob("*.js")):
            for _m in re.finditer(r"notesFor\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]", _f.read_text(encoding="utf-8")):
                if _m.group(2) not in (_notes.get(_m.group(1)) or {}):
                    _missing_notes.append(f"{_m.group(1)}/{_m.group(2)}")
    # And the reverse: notes sitting in site.json that no page asks for. That is what
    # a half-reverted migration looks like -- the data survived, the call site did not.
    _used = set()
    if _pagedir.exists():
        for _f in sorted(_pagedir.glob("*.js")):
            for _m in re.finditer(r"notesFor\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]", _f.read_text(encoding="utf-8")):
                _used.add((_m.group(1), _m.group(2)))
    _orphans = [f"{_p}/{_i}" for _p, _items in _notes.items() for _i in _items
                if (_p, _i) not in _used]
    if _orphans:
        warn("NOTES IN site.json THAT NO PAGE RENDERS: " + ", ".join(sorted(_orphans))
             + ". Either the page lost its notesFor() call, or the note is dead and should go.")

    if _missing_notes:
        warn("PAGE ASKS FOR NOTES THAT DO NOT EXIST: " + ", ".join(sorted(set(_missing_notes)))
             + ". Add them under notes in context/site.json.")

    _job = (site.get("work") or {}).get("current_job") or {}
    if _job.get("due") and _job["due"] < _today:
        warn(f"THE JOB ON THE WORK PAGE IS OVER ITS DEADLINE: {_job.get('name')} was due "
             f"{_job['due']}, today is {_today}. Either it shipped and the record does not say "
             "so, or it is late. Update work.current_job in context/site.json.")
    if _job and all(d.get("state") == "done" for d in _job.get("days", [])):
        warn(f"{_job.get('name')} shows every day done but is still the CURRENT job. "
             "Move it to work.history in context/site.json.")

    _past = [c for c in site.get("countdowns", []) if c.get("date", "9999") < _today]
    if _past:
        warn("COUNTDOWNS IN THE PAST, still on the site: "
             + "; ".join(f"{c['date']} {c['label']}" for c in _past)
             + ". Retire or re-date them in context/site.json.")

    _hl = site.get("habit_log") or {}
    if _hl:
        _lasth = max(_hl)
        if _lasth < _today:
            _hg = (date.fromisoformat(_today) - date.fromisoformat(_lasth)).days
            if _hg >= 1:
                gap(f"HABIT LOG IS {_hg} DAY(S) BEHIND: last entry {_lasth}.")
        # DELETED 2026-09-02: a check that warned when habit_log named habits that
        # are no longer tracked. It fired every single build and always will — the
        # log is a HISTORICAL record and history does not change when a habit is
        # archived. Warning that the past contains the past is noise, and noise is
        # how a banner stops being read. If a check cannot ever go green by doing
        # the right thing, it is not a check.


    if check_only:
        print(json.dumps({k: bundle[k] for k in ("summary", "warnings")}, indent=2))
        for r in ledger:
            print(f"  {r['date']}  {r['verdict']:<8} score={r['score']}  "
                  f"focus={r['focus_logged']}/{r['focus_committed']}  "
                  f"habits={r['habits_hit']}/{r['habits_set']}  bed={r['bed']}")
        return

    OUT.mkdir(parents=True, exist_ok=True)
    # A wall-clock stamp cannot answer "is the live site showing this record?"
    # This machine writes WAT and the CI runner writes UTC, so two builds of
    # the identical record carry different clocks and any comparison of them
    # reports a false STALE forever. Hash the record instead, clock removed.
    # Same hash = same record, no matter which machine built it or when.
    bundle["content_hash"] = hashlib.sha256(
        json.dumps({k: v for k, v in bundle.items() if k != "generated"},
                   sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:16]

    payload = json.dumps(bundle, indent=2, ensure_ascii=False)
    (OUT / "os.json").write_text(payload + "\n", encoding="utf-8")

    # Also emit the same data as a plain script. fetch() on a local file is
    # blocked by CORS, so without this the site only works behind a server —
    # and the first thing Samuel will do is double-click index.html.
    (OUT / "os.js").write_text(
        "/* GENERATED by tools/site/build.py — do not edit. */\n"
        "window.OS = " + payload + ";\n", encoding="utf-8")

    # Cache-bust the data script. Opened over file:// (and behind Pages), the
    # browser will happily serve yesterday's os.js from cache and the record
    # silently reads a day late — the one failure mode that makes the site a
    # liar rather than merely stale. Stamping the build time onto the src makes
    # a rebuild a new URL, so a reload cannot miss it.
    stamp = bundle["generated"].replace("-", "").replace(":", "").replace("T", "")
    # Stamp EVERY local script, not just the data file. Until 2026-09-02 only
    # data/os.js carried ?v=, so app.js, charts.js and pages/*.js were cached
    # forever by the browser and the CDN. Numbers updated; the code that RENDERS
    # them did not. A dead "While fasting" card and an out-of-sync banner that
    # never appeared both survived that way. If the record changed, every file
    # that draws it is re-fetched.
    pattern = re.compile(r'(src="(?:\.\./)?(?:data/os|assets/js/[A-Za-z0-9_/-]+)\.js)(?:\?v=[^"]*)?(")')
    # And the stylesheet, for exactly the same reason. Added 2026-09-02 after a
    # new rule shipped and the browser kept serving a cached app.css: the bars
    # were in the DOM with zero height, so the page rendered blank columns and
    # looked like a code bug. JS was stamped, CSS was not, and a half-stamped
    # site is the worst of both — the numbers update and the thing that draws
    # them does not.
    css_pattern = re.compile(
        r'(href="(?:\.\./)?assets/css/[A-Za-z0-9_/-]+\.css)(?:\?v=[^"]*)?(")')
    shells = [REPO / "site" / "index.html", *sorted((REPO / "site" / "pages").glob("*.html"))]
    stamped = 0
    for shell in shells:
        html = shell.read_text(encoding="utf-8")
        new = pattern.sub(r'\g<1>?v=' + stamp + r'\g<2>', html)
        new = css_pattern.sub(r'\g<1>?v=' + stamp + r'\g<2>', new)
        if new != html:
            shell.write_text(new, encoding="utf-8")
            stamped += 1
    print(f"stamped  : {stamped}/{len(shells)} shells with ?v={stamp}")

    size = (OUT / "os.json").stat().st_size
    print(f"wrote    : site/data/os.json + os.js  ({size/1024:.1f} KB)")
    print(f"days     : {bundle['summary']['days_recorded']} recorded, "
          f"{bundle['summary']['days_closed']} closed")
    print(f"scores   : last {bundle['summary']['last_score']}, "
          f"avg {bundle['summary']['avg_score']}")
    if WARNINGS:
        print("SITE OUT OF SYNC (fix here):")
        for w in WARNINGS:
            print(f"  - {w}")
    if GAPS:
        print("RECORD GAPS (close these by logging, not by building):")
        for g in GAPS:
            print(f"  - {g}")
    if not WARNINGS and not GAPS:
        print("in sync    : site matches context/, and context/ is current")


if __name__ == "__main__":
    main()
