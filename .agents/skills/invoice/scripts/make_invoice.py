"""Make a SamuelVisuals invoice PDF from a job file.

  python make_invoice.py setup                 create the private payee file (blank bank numbers) if missing
  python make_invoice.py check                 say which payee fields are still empty (names only, never values)
  python make_invoice.py build <job.json>      write the PDF to Documents\\Invoices
  python make_invoice.py build <job.json> --preview
                                               masked bank numbers + a PNG, for an AI to check the layout

Bank details live outside the Brain, in %USERPROFILE%\\.brain-secrets\\invoice-payee.json
(AGENTS.md section 6). Samuel fills that file himself. This script reads it; no AI opens it,
and nothing here ever prints a value from it.
"""
import html
import json
import re
import subprocess
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
BUSINESS = SKILL / "assets" / "business.json"
TEMPLATE = SKILL / "assets" / "invoice.html"
PAYEE = Path.home() / ".brain-secrets" / "invoice-payee.json"
OUT = Path.home() / "Documents" / "Invoices"
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
        shares = [money(r * pct / 100) for r in rates]
        shares[-1] += billed - sum(shares)  # the rows add up to the billed total
    else:
        billed = subtotal

    heading = job.get("items_heading") or f"{job.get('period', '')} videos".strip()
    head = f'<tr><th>{e(heading)}</th><th class="amt">Rate</th>'
    head += f'<th class="amt">{e(stage["percent"])}%</th></tr>' if stage else "</tr>"
    rows = []
    for i, it in enumerate(items):
        cells = f'<td>{e(it["description"])}</td><td class="amt">{fmt(rates[i])}</td>'
        if stage:
            cells += f'<td class="amt">{fmt(shares[i])}</td>'
        rows.append(f"<tr>{cells}</tr>")
    total = f'<tr class="total"><td>Total</td><td class="amt">{fmt(subtotal)}</td>'
    total += f'<td class="amt">{fmt(billed)}</td></tr>' if stage else "</tr>"
    rows.append(total)
    due = billed
    for x in job.get("extras", []):
        amt = money(x["amount"])
        due += amt
        gap = "<td></td>" if stage else ""
        rows.append(f'<tr class="extra"><td>{e(x["label"])}</td>{gap}<td class="amt">{fmt(amt)}</td></tr>')

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
        "HEAD": head,
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
    stem = f"{biz['file_prefix']}-Invoice-{int(job['number']):03d}-{client}-{job['issued']}"
    out_dir = OUT / "previews" if preview else OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    html_file = out_dir / f"{stem}.html"
    html_file.write_text(page, encoding="utf-8")
    pdf = out_dir / f"{stem}.pdf"
    b = str(browser())
    common = [b, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars"]
    subprocess.run(common + ["--no-pdf-header-footer", f"--print-to-pdf={pdf}", html_file.as_uri()],
                   check=True, capture_output=True, timeout=120)
    if preview:
        png = out_dir / f"{stem}.png"
        subprocess.run(common + ["--window-size=794,1123", "--force-device-scale-factor=1.5",
                                 f"--screenshot={png}", html_file.as_uri()],
                       check=True, capture_output=True, timeout=120)
        print(f"preview png: {png}")
    else:
        html_file.unlink()  # the full HTML holds bank numbers; keep only the PDF
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
