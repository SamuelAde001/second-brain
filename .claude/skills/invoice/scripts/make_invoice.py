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


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def words(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        return ONES[n // 100] + " hundred" + (" " + words(n % 100) if n % 100 else "")
    for size, name in ((10**9, "billion"), (10**6, "million"), (1000, "thousand")):
        if n >= size:
            return words(n // size) + " " + name + (" " + words(n % size) if n % size else "")


CURRENCY_WORDS = {"USD": ("US dollars", "cents"), "NGN": ("naira", "kobo"), "GBP": ("pounds", "pence")}


def amount_in_words(v, cur):
    major, minor = CURRENCY_WORDS.get(cur, (cur, "cents"))
    whole = int(v)
    cents = int((v - whole) * 100)
    s = f"{words(whole)} {major}"
    if cents:
        s += f" and {words(cents)} {minor}"
    return s[0].upper() + s[1:]


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
    subtotal = sum((money(i["amount"]) for i in items), Decimal("0"))

    # Item rows
    rows = []
    for n, it in enumerate(items, 1):
        sub = f'<div class="note">{e(it["detail"])}</div>' if it.get("detail") else ""
        rows.append(f'<tr><td>{e(it["description"])}{sub}</td><td class="amt">{fmt(money(it["amount"]))}</td></tr>')

    # What this invoice bills: the whole subtotal, or a stage of it (70% / 30%)
    summary = []
    stage = job.get("stage")
    if stage:
        if "amount" in stage:
            billed = money(stage["amount"])
        elif stage.get("rest_of"):
            # 30% stage: total minus the rounded 70%, so the two always add up to the total
            billed = subtotal - money(subtotal * Decimal(stage["rest_of"]) / 100)
        else:
            billed = money(subtotal * Decimal(stage["percent"]) / 100)
        summary.append((stage["label"], billed, stage.get("note", "")))
    else:
        billed = subtotal
    due = billed
    for x in job.get("extras", []):
        amt = money(x["amount"])
        due += amt
        summary.append((x["label"], amt, x.get("note", "")))

    sum_rows = "".join(
        f'<tr><td>{e(lbl)}{f"<div class=note>{e(note)}</div>" if note else ""}</td><td class="amt">{fmt(a)}</td></tr>'
        for lbl, a, note in summary)

    bill_to = "<br>".join([f"<strong>{e(client['name'])}</strong>", *(e(x) for x in client.get("address", []))])
    if job.get("attention") or client.get("attention"):
        bill_to += f'<br><span class="grey">Attn: {e(job.get("attention") or client.get("attention"))}</span>'

    pay_rows = "".join(f"<tr><td>{e(k)}</td><td>{e(v)}</td></tr>" for k, v in [
        ("Account name", payee["account_name"]), ("Bank", payee["bank"]),
        ("Account number", payee["account_number"]), ("Routing number (ACH)", payee["routing_number"]),
        ("Account type", payee["account_type"]), ("Bank address", payee["bank_address"])])

    count = len(items)
    period = job.get("period", "")
    subtotal_label = job.get("subtotal_label") or f"Total for {period} ({count} video{'s' if count != 1 else ''})"
    fields = {
        "TITLE": f"Invoice {job['number']} · {biz['brand']}",
        "BRAND_A": e(biz["brand_parts"][0]), "BRAND_B": e(biz["brand_parts"][1]),
        "TAGLINE": e(biz["tagline"]),
        "NUMBER": e(job["number"]),
        "ISSUED": long_date(job["issued"]),
        "DUE": e(job.get("due", biz.get("default_due", "On receipt"))),
        "PERIOD": e(period),
        "REFERENCE": e(job.get("reference", "")),
        "FROM": "<br>".join([f"<strong>{e(biz['owner'])}</strong>", *(e(x) for x in payee["street"]), e(biz["email"])]),
        "BILL_TO": bill_to,
        "CUR": cur,
        "DUE_AMOUNT": fmt(due),
        "DUE_WORDS": e(amount_in_words(due, cur)),
        "ITEMS_HEAD": e(job.get("items_heading", "Video")),
        "ROWS": "".join(rows),
        "SUBTOTAL_LABEL": e(subtotal_label),
        "SUBTOTAL": fmt(subtotal),
        "SUMMARY_ROWS": sum_rows,
        "PAY_ROWS": pay_rows,
        "PAY_NOTE": e(biz["payment_note"]),
        "PAY_REF": e(f"Payment reference: Invoice {job['number']}."),
        "THANKS": e(job.get("thanks", biz["thanks"])),
        "EMAIL": e(biz["email"]),
    }
    out = TEMPLATE.read_text(encoding="utf-8")
    if not fields["REFERENCE"]:
        out = out.split("<!--REF_START-->")[0] + out.split("<!--REF_END-->")[1]
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
