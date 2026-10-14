"""Make a SamuelVisuals invoice PDF from a job file.

  python make_invoice.py setup                 create the private payee file (blank bank numbers) if missing
  python make_invoice.py check                 say which payee fields are still empty (names only, never values)
  python make_invoice.py build <job.json>      write the PDF to the client's invoice folder (business.json)
  python make_invoice.py build <job.json> --preview
                                               masked bank numbers + a PNG, for an AI to check the layout

Bank details live outside the Brain, in %USERPROFILE%\\.brain-secrets\\invoice-payee.json
(AGENTS.md section 6). Samuel fills that file himself. This script reads it; no AI opens it,
and nothing here ever prints a value from it.
"""
import html
import json
import re
import shutil
import subprocess
import time
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
BUSINESS = SKILL / "assets" / "business.json"
TEMPLATE = SKILL / "assets" / "invoice.html"
PAYEE = Path.home() / ".brain-secrets" / "invoice-payee.json"
PREVIEWS = Path.home() / "Documents" / "Invoices" / "previews"
BROWSERS = [Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")]

PAYEE_TEMPLATE = {
    "_note": "Fill account_number and routing_number. Read only by make_invoice.py. Never copy this file into the Brain.",
    "street": ["House 27/8, Bwari Area Council", "Abuja 901101, Nigeria"],
    "account_name": "SAMUEL SHOLA ADEBAYO",
    "bank": "Lead Bank",
    "account_number": "",
    "routing_number": "",
    "account_type": "Personal Checking",
    "bank_address": "9450 Southwest Gemini Drive, Beaverton, OR 97008, USA",
}
SECRET = ("account_number", "routing_number")

CENT = Decimal("0.01")


def money(v):
    return Decimal(str(v)).quantize(CENT, ROUND_HALF_UP)


def fmt(v):
    return f"{v:,.2f}"


def long_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def load_payee(preview):
    if not PAYEE.exists():
        if not preview:
            sys.exit("No payee file. Run: python make_invoice.py setup, then fill it.")
        p = dict(PAYEE_TEMPLATE)
    else:
        p = json.loads(PAYEE.read_text(encoding="utf-8"))
    missing = [k for k in PAYEE_TEMPLATE if k != "_note" and not p.get(k)]
    if missing and not preview:
        sys.exit("Payee file has empty fields: " + ", ".join(missing))
    if preview:
        for k in SECRET:
            p[k] = "•••• •••• ••••"
    return p


def e(s):
    return html.escape(str(s))


def render(job, biz, payee):
    cur = job.get("currency", "USD")
    client = biz["clients"][job["client"]]
    items = job["items"]
    rates = [money(i["amount"]) for i in items]
    subtotal = sum(rates, Decimal("0"))

    # What this invoice bills: the whole total, or a stage of it (70% / 30%)
    stage = job.get("stage")
    if stage:
        pct = Decimal(str(stage["percent"]))
        if "amount" in stage:
            billed = money(stage["amount"])
        elif stage.get("rest_of"):
            # 30% stage: total minus the rounded 70%, so the two always add up to the total
            billed = subtotal - money(subtotal * Decimal(str(stage["rest_of"])) / 100)
        else:
            billed = money(subtotal * pct / 100)
    else:
        billed = subtotal

    # Videos at their rate, the month's total, then the stage being billed and any extras
    heading = job.get("items_heading") or f"{job.get('period', '')} videos".strip()
    rows = [f'<tr><th>{e(heading)}</th><th class="amt">Amount</th></tr>']
    rows += [f'<tr><td>{e(it["description"])}</td><td class="amt">{fmt(rates[i])}</td></tr>'
             for i, it in enumerate(items)]
    rows.append(f'<tr class="total"><td>Total</td><td class="amt">{fmt(subtotal)}</td></tr>')
    if stage:
        rows.append(f'<tr class="extra"><td>{e(stage["label"])}</td><td class="amt">{fmt(billed)}</td></tr>')
    due = billed
    for x in job.get("extras", []):
        amt = money(x["amount"])
        due += amt
        rows.append(f'<tr class="extra"><td>{e(x["label"])}</td><td class="amt">{fmt(amt)}</td></tr>')

    who = [f"<strong>{e(biz['owner'])}</strong>"] + [e(x) for x in payee["street"]] + [e(biz["email"])]
    bill = [f"<strong>{e(client['name'])}</strong>"] + [e(x) for x in client.get("address", [])]
    if client.get("email"):
        bill.append(e(client["email"]))

    pay_rows = "".join(f"<tr><td>{e(k)}</td><td>{e(v)}</td></tr>" for k, v in [
        ("Account name", payee["account_name"]), ("Bank", payee["bank"]),
        ("Account number", payee["account_number"]), ("Routing number", payee["routing_number"]),
        ("Account type", payee["account_type"]), ("Bank address", payee["bank_address"])])

    fields = {
        "TITLE": f"Invoice {job['number']} · {biz['brand']}",
        "BRAND_A": e(biz["brand_parts"][0]), "BRAND_B": e(biz["brand_parts"][1]),
        "NUMBER": e(job["number"]),
        "ISSUED": long_date(job["issued"]),
        "DUE": e(job.get("due", biz.get("default_due", "On receipt"))),
        "FROM": "<br>".join(who),
        "BILL_TO": "<br>".join(bill),
        "ROWS": "".join(rows),
        "CUR": cur,
        "DUE_AMOUNT": fmt(due),
        "PAY_ROWS": pay_rows,
        "PAY_NOTE": e(biz["payment_note"]),
    }
    out = TEMPLATE.read_text(encoding="utf-8")
    for k, v in fields.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out, due


def browser():
    for b in BROWSERS:
        if b.exists():
            return b
    sys.exit("No Edge or Chrome found to print the PDF.")


def build(job_path, preview):
    job = json.loads(Path(job_path).read_text(encoding="utf-8"))
    biz = json.loads(BUSINESS.read_text(encoding="utf-8"))
    payee = load_payee(preview)
    page, due = render(job, biz, payee)
    client = biz["clients"][job["client"]]["short"]
    if preview:
        out_dir = PREVIEWS
        stem = f"{biz['file_prefix']}-Invoice-{int(job['number']):03d}-{client}-{job['issued']}"
        html_dir = out_dir
    else:
        # His naming since 2025: "Samuelvisuals <Month> mid invoice" (the 30%), "... end invoice" (the 70%)
        out_dir = Path(biz["clients"][job["client"]]["invoice_folder"])
        month = date.fromisoformat(job["issued"]).strftime("%B")
        kind = {30: " mid", 70: " end"}.get((job.get("stage") or {}).get("percent"), "")
        stem = job.get("file_name") or f"Samuelvisuals {month}{kind} invoice"
        if (out_dir / f"{stem}.pdf").exists():
            sys.exit(f"Already exists, not overwritten: {out_dir / (stem + '.pdf')}")
        # Not tempfile.mkdtemp(): its owner-only folder is unreadable to Edge's sandbox.
        # The full page holds bank numbers, so this folder is deleted after the build.
        html_dir = PREVIEWS.parent / "work"
        html_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Edge drops paths with spaces, so it prints under a plain name and Python moves and renames the PDF
    work = stem if preview else "invoice"
    html_file = html_dir / f"{work}.html"
    html_file.write_text(page, encoding="utf-8")
    printed = html_dir / f"{work}.pdf"
    b = str(browser())
    common = [b, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars"]
    run = subprocess.run(common + ["--no-pdf-header-footer", f"--print-to-pdf={printed}", html_file.as_uri()],
                         capture_output=True, text=True, timeout=120)
    # Edge can return before the file lands: wait until it exists and its size stops changing
    size = -1
    for _ in range(60):
        if printed.exists() and printed.stat().st_size == size and size > 0:
            break
        size = printed.stat().st_size if printed.exists() else -1
        time.sleep(0.5)
    else:
        sys.exit(f"The browser didn't write the PDF.\n{run.stderr[-800:]}")
    pdf = out_dir / f"{stem}.pdf"
    if printed != pdf:
        shutil.move(printed, pdf)
    if preview:
        png = out_dir / f"{stem}.png"
        subprocess.run(common + ["--window-size=794,1123", "--force-device-scale-factor=1.5",
                                 f"--screenshot={png}", html_file.as_uri()],
                       check=True, capture_output=True, timeout=120)
        print(f"preview png: {png}")
    else:
        shutil.rmtree(html_dir, ignore_errors=True)  # the full HTML holds bank numbers; keep only the PDF
    print(f"pdf: {pdf}")
    print(f"amount due: {job.get('currency', 'USD')} {fmt(due)}")
    pages = len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))
    if pages != 1:
        print(f"WARNING: {pages} pages. The invoice must fit one A4 page; tighten the layout or shorten the lines.")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "setup":
        if PAYEE.exists():
            print(f"exists, not touched: {PAYEE}")
        else:
            PAYEE.parent.mkdir(parents=True, exist_ok=True)
            PAYEE.write_text(json.dumps(PAYEE_TEMPLATE, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"created: {PAYEE}\nSamuel fills in: account_number, routing_number")
    elif cmd == "check":
        if not PAYEE.exists():
            print("missing: run setup")
            return
        p = json.loads(PAYEE.read_text(encoding="utf-8"))
        empty = [k for k in PAYEE_TEMPLATE if k != "_note" and not p.get(k)]
        print("empty: " + ", ".join(empty) if empty else "all payee fields filled")
    elif cmd == "build" and len(sys.argv) >= 3:
        build(sys.argv[2], "--preview" in sys.argv)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
