---
name: invoice
description: "Make Samuel's SamuelVisuals invoice as a one-page PDF: the videos he delivered, the stage being billed (70% at month end, 30% balance mid next month, or the full amount), any bonus, and his USD bank details pulled from a private file outside the Brain. Use whenever he says 'make the invoice', 'invoice Route Rise', 'send invoice' is on today's list, it's the 29th (70%) or mid-month (30%), or he asks to change how the invoice looks. Not for logging money that landed (use payday) or the month-end numbers (use month-close)."
effort: medium
type: skill
area: finances
status: active
updated: 2026-10-14
source: interview
tags: [skill, finances, invoicing]
---

# Invoice

Built 2026-10-14. Samuel: *"I want us to work on it and make it look better with the right details and eventually create a skill that would be creating invoices in pdfs when I need it"*. Act as the **Money man**: read `07-Agents/finance/profile.md` and `07-Agents/finance/memory.md` first. Format and rules behind it: [[03-Areas/finances/invoicing|Invoicing]].

**Samuel sends the invoice himself.** This skill makes the PDF and records it. It never emails or messages anyone.

## The files

- `scripts/make_invoice.py`: renders the PDF through Edge (or Chrome) in headless mode. No installs.
- `assets/invoice.html`: the A4 layout. `assets/business.json`: brand, his name, email, payment note, clients.
- **Bank details**: `%USERPROFILE%\.brain-secrets\invoice-payee.json`, outside the Brain (AGENTS.md §6). **Samuel fills it; no AI opens, prints or copies it.** Only the script reads it. `python make_invoice.py check` names any empty field without showing values.
- Job files (no secrets, kept in the Brain): `03-Areas/finances/invoices/invoice-NNN-<client>-<YYYY-MM-DD>.json`.
- PDFs: `C:\Users\repzy\Documents\Invoices\` (they hold the bank numbers, so they never go in the Brain). Masked previews: `...\Invoices\previews\`.

## Steps

1. **What's being billed.** Month and stage:
   - **29th of the month: the 70%.** The invoice still goes out on the 29th even if Route Rise pays late ([[03-Areas/video-editing/clients/routerise|Route Rise]]).
   - **Mid next month: the 30% balance** of that month, on a new invoice number that references the 70% one.
   - Anything else: the full amount.
2. **Which videos.** `python 00-System/scripts/money_ledger.py videos YYYY-MM`, then confirm the titles with him in one line. **If he has moved on to a new Route Rise video, the one before it is delivered** (Samuel, 2026-10-14: he never starts a new one before delivering the last). If the record is short, say so in one line; the Editor adds the row ([[03-Areas/video-editing/delivered-projects|delivered projects]]). Rate: USD 333.33 unless he says otherwise. Never guess a title or an amount.
3. **Number.** The next number after the last row in the register in [[03-Areas/finances/invoicing|Invoicing]]. Every invoice gets its own number (Samuel, 2026-10-14).
4. **Write the job file.** Copy the latest one in `03-Areas/finances/invoices/` and change it. Fields:
   - `number`, `issued` (ISO date), `due` (default **On receipt**, Samuel 2026-10-14), `client` (a key in `business.json`, which holds the client's address and email), `currency`, `period` ("September 2026", heads the video table).
   - `items`: one per video, `{"description": "<title>", "amount": "333.33"}`.
   - `stage`, for a split. It adds a 70% or 30% column with each video's share, like Route Rise's own template. The 70% is `{"label": "70% of the <Month> total", "percent": 70}`. The 30% is `{"label": "30% balance of the <Month> total", "percent": 30, "rest_of": 70}`: total minus the rounded 70%, so the two always add up to the total. An explicit `"amount"` overrides both; use it only when Samuel gives the figure. The last row absorbs any cent of rounding so the column adds up.
   - `extras`: bonuses or other charges, `{"label": "Bonus", "amount": "25.00"}`.
5. **Preview.** `python 00-System/skills/invoice/scripts/make_invoice.py build <job.json> --preview`. Look at the PNG: one page, nothing wrapping badly, numbers right. Bank numbers show as dots here.
6. **Final.** `python .../make_invoice.py check`. If a field is empty, tell him to open the payee file in Notepad and fill it, then stop until he says done. Then `build <job.json>` without `--preview`. Don't open the final PDF (it holds the bank numbers); send it to him with its path.
7. **Record.** Add a row to the register in [[03-Areas/finances/invoicing|Invoicing]] (number, date, client, period, stage, amount). Log one line in `07-Agents/finance/log.md`. Commit and push.

## Changing the look

Edit `assets/invoice.html` (layout and colours) or `assets/business.json` (wording, payment note, clients), rebuild the #14 preview and look at it. The invoice must stay one A4 page. Samuel, 2026-10-14, after seeing Route Rise's own template: *"Make it bold and more legible, and add colors to where colors are needed ... Unneccesary wordings should be removed ... Make mine big and bold too, just still in a good style"*. So: big bold type, green table header and amount-due bar, no extra lines of text. And plain, from earlier the same day: Samuel, 2026-10-14, *"Don't let the design look like AI, let it look easy to understand and clean, not too complex looking"*. No tinted panels, badges or spaced-out capital labels. A new client is a new key under `clients`.
