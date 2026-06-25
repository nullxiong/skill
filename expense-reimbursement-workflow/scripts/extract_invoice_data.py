#!/usr/bin/env python3
import argparse
import json
import re
import zipfile
from pathlib import Path

from pypdf import PdfReader


def pdf_text(path):
    try:
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as exc:
        return f"__PDF_ERROR__ {exc}"


def money_after(pattern, text):
    match = re.search(pattern, text, re.S)
    return float(match.group(1)) if match else None


def parse_ride(path):
    text = pdf_text(path)
    total = money_after(r"合计\s*([0-9.]+)元", text)
    invoice_no = re.search(r"发票号码\s*[:：]\s*(\d{8,30})", text)
    rows = []
    for match in re.finditer(
        r"(?P<idx>\d+)\s+\S+\s+(?P<date>\d{2}-\d{2})\s+(?P<time>\d{2}:\d{2})\s+\S+\s+(?P<city>[\u4e00-\u9fa5]+市)\s+"
        r"(?P<start>.+?)\s+(?P<end>.+?)\s+(?P<km>\d+(?:\.\d+)?)\s+(?P<amount>\d+(?:\.\d+)?)",
        text,
    ):
        rows.append(match.groupdict())
    return {
        "kind": "ride",
        "file": str(path),
        "invoice_no": invoice_no.group(1) if invoice_no else None,
        "total": total,
        "rows": rows,
        "text": text[:2500],
    }


def parse_hotel_statement(path):
    text = pdf_text(path)
    check_in = re.search(r"入住日期\s*：\s*(\d{4}-\d{2}-\d{2})", text)
    check_out = re.search(r"离店日期\s*：\s*(\d{4}-\d{2}-\d{2})", text)
    hotel = (text.strip().splitlines() or [""])[0].strip()
    total = money_after(r"消费合计\s*([0-9.]+)", text) or money_after(r"付款合计\s*([0-9.]+)", text)
    return {
        "kind": "hotel_statement",
        "file": str(path),
        "hotel": hotel,
        "check_in": check_in.group(1) if check_in else None,
        "check_out": check_out.group(1) if check_out else None,
        "total": total,
        "text": text[:2500],
    }


def parse_generic_invoice(path, kind):
    text = pdf_text(path)
    invoice_no = re.search(r"(?:发票号码|发票号)\s*[:：]?\s*(\d{8,30})", text)
    total = (
        money_after(r"价税合计[^\d]*(\d+\.\d+)", text)
        or money_after(r"小写[）)]\s*[¥￥]?\s*(\d+\.\d+)", text)
        or money_after(r"合计[^\d]{0,10}[¥￥]?\s*(\d+\.\d+)", text)
    )
    return {
        "kind": kind,
        "file": str(path),
        "invoice_no": invoice_no.group(1) if invoice_no else None,
        "total": total,
        "text": text[:2500],
    }


def parse_rail_pdf(path):
    text = pdf_text(path)
    amount = (
        money_after(r"票价\s*[:：]?\s*[¥￥]?\s*(\d+\.\d+)", text)
        or money_after(r"退票费\s*[:：]?\s*[¥￥]?\s*(\d+\.\d+)", text)
        or money_after(r"￥\s*\n?\s*(\d+\.\d+)", text)
    )
    travel_date = re.search(r"(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日|\d{4}-\d{2}-\d{2})", text)
    invoice_no = re.search(r"(?:发票号码|电子发票号码|号码)\s*[:：]?\s*(\d{8,30})", text)
    stations = re.findall(r"([\u4e00-\u9fa5]{1,12})\s*站", text)
    return {
        "kind": "rail",
        "file": str(path),
        "invoice_no": invoice_no.group(1) if invoice_no else None,
        "amount": amount,
        "date": travel_date.group(1).replace(" ", "") if travel_date else None,
        "stations": stations,
        "text": text[:3000],
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--invoice-dir", required=True)
    parser.add_argument("--extracted-dir", default="work/extracted_invoices")
    parser.add_argument("--output-json")
    return parser.parse_args()


def main():
    args = parse_args()
    base = Path(args.invoice_dir).expanduser()
    extracted = Path(args.extracted_dir)
    extracted.mkdir(parents=True, exist_ok=True)
    records = []

    for zip_path in sorted((base / "高铁发票").glob("*.zip")):
        with zipfile.ZipFile(zip_path) as zf:
            for member in zf.namelist():
                if member.lower().endswith(".pdf"):
                    target = extracted / f"{zip_path.stem}_{Path(member).name}"
                    if not target.exists():
                        target.write_bytes(zf.read(member))
                    item = parse_rail_pdf(target)
                    item["source_zip"] = str(zip_path)
                    records.append(item)

    for path in sorted((base / "住宿发票").glob("*.pdf")):
        records.append(parse_hotel_statement(path) if "结账单" in path.name else parse_generic_invoice(path, "hotel_invoice"))

    for path in sorted((base / "网约车发票").glob("*.pdf")):
        records.append(parse_ride(path) if "行程" in path.name else parse_generic_invoice(path, "ride_invoice"))

    output = json.dumps(records, ensure_ascii=False, indent=2)
    if args.output_json:
        Path(args.output_json).write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
