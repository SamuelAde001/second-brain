---
type: knowledge
area: finances
status: needs-input
updated: 2026-09-20
source: claude-export
tags: [invoicing, clients]
---

# Invoicing

From the chat `01-Inbox/_imports/processed/shortlist/finances/2026-08-20-creating-an-invoice-with-logo.md`, 2026-08-20. Built for an actual client job for **Mshel**.

## Format and what goes on it

- **Logo** — extracted from the original badge (which sat on a dark circular background) and cleaned into a transparent PNG so it prints correctly on white paper. Reused across the invoice, the builder file, and future letterheads/quotes.
- **Fonts** — Poppins for display (matches the logo's lettering), Carlito for body text, chosen specifically because Carlito renders the ₦ symbol natively without font-fallback issues.
- **Invoice number** — running format **`DSG-2026-001`**, auto-incrementing on later invoices (002, 003…). His original handwritten sheet had no invoice numbers at all; this was added so payments can be referenced later. What "DSG" stands for is not stated anywhere in the source — needs-input.
- **Line items** — description, quantity, unit price, computed row amount.
- **Subtotal, VAT, total.**
- **Amount in words** — spelled out, standard on Nigerian invoices and useful for a client's accounts department.
- **Payment note** — asks the payer to quote the invoice number on transfer.
- **Signature** — see below.

## The first real invoice (worked numbers)

Client: Mshel. Invoice DSG-2026-001, dated 2026-08-20.

- Line 1: 1,000 × NGN 900 = NGN 900,000
- Line 2: 500 × NGN 800 = NGN 400,000
- Subtotal: NGN 1,300,000
- VAT at **7.5%**: NGN 97,500
- **Total: NGN 1,397,500**

(What the two line items were for is not stated in the source — only the quantities and unit prices. Not guessed here.)

## Payment terms — outstanding

Two things were flagged as missing from this invoice and never supplied in the chat:

- **TIN (Tax Identification Number)** — flagged twice as something "Mshel's accounts team will likely ask for" since VAT is being charged. Not added.
- **Payment term** — e.g. "due on receipt" or "net 14". Not on the invoice as of 2026-08-20.

Both are needs-input; logged in `00-System/open-questions.md`.

## The process — two deliverables

1. **A one-off finished PDF/HTML invoice** per job, with the logo and figures baked in — the version actually sent for the Mshel job.
2. **A reusable offline "builder"** — one HTML file, opened by double-clicking in Chrome, no internet or login required. Typing directly into underlined fields (description, qty, price) recalculates everything live:
   - Row amount → subtotal → VAT → total
   - Amount in words rewrites itself
   - "Next invoice no." auto-bumps (verified including rollovers, e.g. 009 → 010) and updates the payment note to match
   - VAT can be set to 0 in the top bar for a non-VAT job
   - **To save:** browser print dialog → Destination "Save as PDF" → under "More settings" tick **Background graphics**, otherwise the navy header bar and totals block print white.
   - The builder file itself does not save state between sessions — it is a blank template every time it's reopened. Fill in, save the PDF, close without saving.

## Signature

A photo of his handwritten signature, background removed (transparent PNG), placed just above the signature line with the tail crossing it, "the way a pen signature naturally would." The builder has a **Signature: on/off** toggle, used to print unsigned copies (e.g. a quotation that shouldn't look like a committed invoice yet).

**Handling caution** (assistant's advice, not a stored rule — worth keeping in mind): a transparent PNG signature is reusable by anyone holding the file. Keep it out of shared Drive folders and off WhatsApp; send invoices as **PDF** rather than the editable builder file, since a PDF flattens the image so it can't be lifted back out.

## needs-input

- TIN.
- A standard payment term to put on every invoice.
- What "DSG" stands for.
- Whether the builder/PDF workflow above is still what he actually uses for invoices sent after 2026-08-20.

Back to [[03-Areas/finances/_index|Finances]]

## Payment terms — confirmed by Samuel, 2026-09-20

Invoicing the agency ([[03-Areas/video-editing/clients/routerise|Routerise]]) is **monthly, not per video**. At month end he invoices for however many videos he delivered that month.

- **70% paid at the end of that month.**
- **30% paid in the middle of the following month.**

Rate: **USD 333.33 per video**, the agency's standard.

This is the split the percentage-based budget system's Receipt Ratio exists to track — see [[budget-system]]. It also means a month's earnings are never fully in hand until mid the next month, which is the single most important fact for any runway or cashflow calculation.

