---
name: expense-reimbursement-workflow
description: Automate recurring Chinese travel reimbursement preparation from mailbox invoices to a completed Excel workbook. Use when Codex needs to fetch QQ Mail invoice attachments via IMAP, save high-speed rail, hotel, and ride-hailing invoices locally, deduplicate Didi attachments with per-email suffixes, parse local invoice PDFs/ZIPs, summarize trip legs and costs, and fill a travel reimbursement Excel template without modifying the original template.
---

# Expense Reimbursement Workflow

## Overview

Use this skill for the pre-submission reimbursement workflow: collect invoices from email, archive them locally, extract travel facts, organize trip legs, and generate a filled reimbursement Excel workbook from a template. Do not submit web reimbursement forms unless the user explicitly asks for browser automation in the current turn.

## Safety Rules

- Do not store mailbox passwords or IMAP authorization codes in the skill.
- Prefer a local temporary env file such as `work/.qq_mail_env`; never copy it into the skill.
- Treat the original Excel template as read-only. Always save a timestamped copy.
- For Didi/ride-hailing mail, add a per-email suffix when downloading attachments because multiple messages may reuse the same subject and attachment names.
- Ask the user for the reimbursement date range before searching mail unless they already gave one.

## Standard Inputs

Ask for or infer these paths:

- Reimbursement root directory, for example `/Users/.../work/.../08-报销`
- Invoice output directory, usually `<reimbursement-root>/发票`
- Excel template path, usually `<reimbursement-root>/差旅报销 -模版.xlsx`
- Date range for mailbox search

QQ Mail credentials are read from environment variables:

```bash
QQ_EMAIL=...
QQ_IMAP_AUTH_CODE=...
```

For PDF and Excel scripts, first resolve the Codex workspace dependencies and run scripts with the returned bundled Python. The scripts need `pypdf` and `openpyxl`, which may not exist in system Python.

## Workflow

1. Confirm the time range and local reimbursement directory.
2. If using QQ Mail, verify credentials are available through environment variables or a user-created temporary env file.
3. Download invoice attachments with `scripts/qq_invoice_downloader.py`.
4. For same-day Didi/ride-hailing messages, rerun with `--mode ride-invoice --message-suffix` to avoid skipping same-named attachments from different emails.
5. Parse the invoice directory with `scripts/extract_invoice_data.py`.
6. Group invoice records into trip legs:
   - Use rail invoices for train dates, routes, and fares.
   - Use hotel statements for stay dates and lodging totals.
   - Use ride-hailing trip sheets for local transportation dates and amounts.
   - Use electronic invoices for invoice numbers and amount confirmation.
7. Prepare a `trips.json` file for the Excel writer.
8. Fill the Excel copy with `scripts/fill_reimbursement_excel.py`.
9. Verify key rows in the generated workbook: origin, destination, dates, days, train, taxi, hotel, subsidy, invoice number, and formula cells.
10. Report the generated workbook path and any assumptions requiring human review.

## Download Invoices

Use bundled or system Python with no secrets in arguments when possible:

```bash
set -a
source work/.qq_mail_env
set +a
python scripts/qq_invoice_downloader.py \
  --output-dir "/path/to/报销/发票" \
  --since 2026-05-01 \
  --before 2026-06-02
```

For Didi/ride-hailing mail where same filenames may repeat:

```bash
python scripts/qq_invoice_downloader.py \
  --output-dir "/path/to/报销/发票" \
  --since 2026-06-01 \
  --before 2026-06-02 \
  --mode ride-invoice \
  --message-suffix
```

## Parse Local Invoices

```bash
python scripts/extract_invoice_data.py \
  --invoice-dir "/path/to/报销/发票" \
  --extracted-dir "work/extracted_invoices" \
  --output-json "work/invoice_records.json"
```

Review parsed output before filling Excel. PDF extraction may miss route order or amounts in unusual rail layouts, so compare against source text when values look wrong.

## Trip JSON Shape

Create a JSON file like:

```json
[
  {
    "start": "南京",
    "destination": "徐州",
    "days": 2,
    "date_range": "2026/5/14-2026/5/15",
    "train": 354.0,
    "taxi": 107.8,
    "hotel": 307.12,
    "subsidy": 150.0,
    "invoice_no": "263...,261...",
    "reason": "徐州出差"
  }
]
```

The standard subsidy is `75 * days` unless the user says otherwise.

## Fill Excel Template

```bash
python scripts/fill_reimbursement_excel.py \
  --template "/path/to/差旅报销 -模版.xlsx" \
  --trips-json "work/trips.json" \
  --output-dir "/path/to/报销"
```

The writer targets the `销售费用报销表` sheet and assumes the template has four travel blocks starting at rows `16, 22, 28, 34`. If a template differs, inspect it first and adjust `--block-start-rows`.

Do not manually fill subtotal or cumulative amount cells; keep Excel formulas.

## Reference

Read `references/reimbursement_workflow.md` for a concrete example and conventions from the original workflow.
