#!/usr/bin/env python3
"""Send a research report via Gmail SMTP with Markdown and PDF attachments."""

import email.encoders
import email.mime.base
import email.mime.multipart
import email.mime.text
import os
import smtplib
import sys
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


def load_env(env_path: Path) -> None:
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"'))


def attach_file(msg: MIMEMultipart, file_path: Path) -> None:
    data = file_path.read_bytes()
    part = MIMEBase("application", "octet-stream")
    part.set_payload(data)
    email.encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{file_path.name}"')
    msg.attach(part)


def send_report(md_path: str, pdf_path: str | None = None) -> None:
    project_root = Path(__file__).resolve().parent.parent
    load_env(project_root / ".env")

    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    sender_name = os.environ.get("SENDER_NAME", "Deep Research Agent")
    recipient_email = os.environ.get("RECIPIENT_EMAIL")

    if not all([sender_email, sender_password, recipient_email]):
        print("Error: Missing required env vars (SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL)", file=sys.stderr)
        sys.exit(1)

    md_file = Path(md_path)
    if not md_file.exists():
        print(f"Error: {md_file} not found", file=sys.stderr)
        sys.exit(1)

    report_name = md_file.stem.replace("-", " ").title()

    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = recipient_email
    msg["Subject"] = f"Research Report: {report_name}"

    md_content = md_file.read_text(encoding="utf-8")
    preview = md_content[:500].replace("\n", "<br>")

    has_pdf = False
    if pdf_path:
        pdf_file = Path(pdf_path)
        has_pdf = pdf_file.exists()
    else:
        pdf_file = md_file.with_suffix(".pdf")
        has_pdf = pdf_file.exists()

    html_body = (
        f"<h2>Research Report: {report_name}</h2>"
        f"<p>Your research report is attached as Markdown"
        f"{' and PDF' if has_pdf else ''}.</p>"
        f"<hr><h3>Preview</h3><p style='font-size:13px;color:#555;'>{preview}...</p>"
    )
    msg.attach(MIMEText(html_body, "html"))
    attach_file(msg, md_file)
    if has_pdf:
        attach_file(msg, pdf_file)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print(f"Email sent to {recipient_email}")


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <report.md> [report.pdf]", file=sys.stderr)
        sys.exit(1)

    md_path = sys.argv[1]
    pdf_path = sys.argv[2] if len(sys.argv) > 2 else None
    send_report(md_path, pdf_path)


if __name__ == "__main__":
    main()
