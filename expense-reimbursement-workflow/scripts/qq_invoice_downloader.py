#!/usr/bin/env python3
import argparse
import email
import imaplib
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from email.header import decode_header
from email.utils import parsedate_to_datetime
from pathlib import Path


HOST = "imap.qq.com"
PORT = 993

MAIL_KEYWORDS = [
    "高铁", "火车", "铁路", "12306", "中国铁路", "电子客票", "行程信息提示",
    "发票", "电子发票", "滴滴", "DIDI", "曹操", "T3", "高德", "美团打车",
    "网约车", "出行", "行程单", "行程明细", "用车明细",
    "酒店", "住宿", "宾馆", "旅店", "华住", "携程", "美团酒店", "同程", "去哪儿",
]

ATTACHMENT_KEYWORDS = [
    "发票", "invoice", "电子发票", "高铁", "铁路", "12306",
    "行程单", "行程明细", "用车明细", "出行服务", "trip",
    "酒店", "住宿", "宾馆", "结账单",
]


def decode_mime(value):
    if not value:
        return ""
    parts = []
    for text, charset in decode_header(value):
        if isinstance(text, bytes):
            for encoding in (charset, "utf-8", "gb18030", "latin1"):
                if not encoding:
                    continue
                try:
                    parts.append(text.decode(encoding, errors="replace"))
                    break
                except LookupError:
                    continue
        else:
            parts.append(text)
    return "".join(parts)


def safe_filename(name):
    name = decode_mime(name).strip() or "attachment"
    name = re.sub(r"[\\/:*?\"<>|\r\n\t]+", "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:180]


def unique_path(path):
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    for i in range(2, 1000):
        candidate = path.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Too many duplicate filenames for {path.name}")


def message_text_for_matching(msg):
    subject = decode_mime(msg.get("Subject"))
    sender = decode_mime(msg.get("From"))
    snippets = [subject, sender]
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        disposition = (part.get("Content-Disposition") or "").lower()
        if "attachment" in disposition:
            filename = part.get_filename()
            if filename:
                snippets.append(decode_mime(filename))
            continue
        ctype = part.get_content_type()
        if ctype not in ("text/plain", "text/html"):
            continue
        try:
            payload = part.get_payload(decode=True)
            if payload:
                charset = part.get_content_charset() or "utf-8"
                snippets.append(payload.decode(charset, errors="replace")[:3000])
        except Exception:
            pass
    return "\n".join(snippets)


def classify_attachment(filename, context):
    haystack = f"{filename}\n{context}".lower()
    if any(k.lower() in haystack for k in ["行程单", "行程明细", "用车明细", "出行服务", "trip"]):
        return "网约车行程单"
    if any(k.lower() in haystack for k in ["滴滴", "didi", "曹操", "t3", "高德", "美团打车", "网约车"]):
        return "网约车发票"
    if any(k.lower() in haystack for k in ["酒店", "住宿", "宾馆", "旅店", "华住", "携程", "美团酒店", "同程", "去哪儿", "结账单"]):
        return "住宿发票"
    if any(k.lower() in haystack for k in ["高铁", "火车", "铁路", "12306", "电子客票"]):
        return "高铁发票"
    if any(k.lower() in haystack for k in ["发票", "invoice"]):
        return "发票"
    return ""


def parse_args():
    parser = argparse.ArgumentParser(description="Download QQ Mail invoice attachments via IMAP.")
    parser.add_argument("--email", default=os.environ.get("QQ_EMAIL"), help="QQ email address")
    parser.add_argument("--auth-code", default=os.environ.get("QQ_IMAP_AUTH_CODE"), help="QQ IMAP auth code")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--since", required=True, help="YYYY-MM-DD")
    parser.add_argument("--before", required=True, help="YYYY-MM-DD, exclusive")
    parser.add_argument("--all-folders", action="store_true", help="scan all folders instead of INBOX only")
    parser.add_argument("--mode", choices=["all", "ride-invoice"], default="all")
    parser.add_argument("--message-suffix", action="store_true", help="add a per-email suffix to attachment filenames")
    return parser.parse_args()


def imap_date(date_text):
    return datetime.strptime(date_text, "%Y-%m-%d").strftime("%d-%b-%Y")


def chunks(items, size):
    for index in range(0, len(items), size):
        yield items[index:index + size]


def search_keyword(client, since, before, keyword):
    charset = "UTF-8" if any(ord(ch) > 127 for ch in keyword) else None
    try:
        status, data = client.search(charset, "SINCE", since, "BEFORE", before, "TEXT", keyword)
        if status == "OK" and data and data[0]:
            return set(data[0].split())
    except Exception:
        pass
    try:
        status, data = client.search(charset, "SINCE", since, "BEFORE", before, "SUBJECT", keyword)
        if status == "OK" and data and data[0]:
            return set(data[0].split())
    except Exception:
        pass
    return set()


def main():
    args = parse_args()
    if not args.email or not args.auth_code:
        print("缺少 QQ 邮箱或 IMAP 授权码。请设置 QQ_EMAIL 和 QQ_IMAP_AUTH_CODE 环境变量后重试。", file=sys.stderr)
        return 2

    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    since = imap_date(args.since)
    before = imap_date(args.before)
    search_keywords = MAIL_KEYWORDS
    if args.mode == "ride-invoice":
        search_keywords = [
            "滴滴", "DIDI", "曹操", "T3", "高德", "美团打车",
            "网约车", "打车", "用车", "出行", "发票", "电子发票",
        ]
    downloaded = []
    seen = set()

    with imaplib.IMAP4_SSL(HOST, PORT) as client:
        client.login(args.email, args.auth_code)
        folders = ["INBOX"]
        if args.all_folders:
            status, folders_data = client.list()
            if status != "OK":
                raise RuntimeError("无法读取邮箱文件夹列表")

            folders = []
            for raw in folders_data:
                line = raw.decode(errors="replace")
                match = re.search(r' "/" "?(.*?)"?$', line)
                if match:
                    folder = match.group(1)
                    if not any(skip in folder.lower() for skip in ["sent", "trash", "deleted", "junk", "spam"]):
                        folders.append(folder)
            if "INBOX" not in folders:
                folders.insert(0, "INBOX")

        for folder in folders:
            try:
                status, _ = client.select(f'"{folder}"', readonly=True)
                if status != "OK":
                    continue
                matched_nums = set()
                for keyword in search_keywords:
                    hits = search_keyword(client, since, before, keyword)
                    if hits:
                        print(f"{folder} 关键词“{keyword}”命中 {len(hits)} 封", flush=True)
                    matched_nums.update(hits)

                matched_nums = sorted(matched_nums, key=lambda item: int(item))
                print(f"{folder} 命中候选邮件合计: {len(matched_nums)} 封", flush=True)
                for message_index, num in enumerate(matched_nums, start=1):
                    status, msg_data = client.fetch(num, "(RFC822)")
                    if status != "OK":
                        continue
                    raw_msg = next((part[1] for part in msg_data if isinstance(part, tuple)), None)
                    if not raw_msg:
                        continue
                    msg = email.message_from_bytes(raw_msg)
                    context = message_text_for_matching(msg)

                    msg_date = msg.get("Date") or ""
                    try:
                        date_prefix = parsedate_to_datetime(msg_date).strftime("%Y%m%d")
                    except Exception:
                        date_prefix = "unknown-date"
                    subject = safe_filename(decode_mime(msg.get("Subject")))[:60]
                    subject_suffix = f"{subject}_邮件{message_index:02d}" if args.message_suffix else subject

                    for part in msg.walk():
                        disposition = (part.get("Content-Disposition") or "").lower()
                        filename = part.get_filename()
                        if "attachment" not in disposition and not filename:
                            continue
                        filename = safe_filename(filename or "attachment")
                        label = classify_attachment(filename, context)
                        if args.mode == "ride-invoice" and label not in ("网约车发票", "网约车行程单"):
                            continue
                        if args.mode == "ride-invoice" and label == "网约车行程单":
                            label = "网约车发票"
                        if not label:
                            if not any(k.lower() in filename.lower() for k in ATTACHMENT_KEYWORDS):
                                continue
                            label = "相关附件"
                        payload = part.get_payload(decode=True)
                        if not payload:
                            continue
                        digest_key = (folder, msg.get("Message-ID"), filename, len(payload))
                        if digest_key in seen:
                            continue
                        seen.add(digest_key)
                        category_dir = output_dir / label
                        category_dir.mkdir(parents=True, exist_ok=True)
                        target = category_dir / f"{date_prefix}_{subject_suffix}_{filename}"
                        if target.exists():
                            print(f"已存在，跳过：{target}", flush=True)
                            continue
                        target = unique_path(target)
                        target.write_bytes(payload)
                        downloaded.append({
                            "folder": folder,
                            "subject": decode_mime(msg.get("Subject")),
                            "category": label,
                            "file": str(target),
                        })
            finally:
                try:
                    client.close()
                except Exception:
                    pass

    print(f"下载完成：{len(downloaded)} 个附件")
    for item in downloaded:
        print(f"[{item['category']}] {item['file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
