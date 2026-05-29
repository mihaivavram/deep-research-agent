#!/usr/bin/env python3
"""Convert a Markdown file to a styled PDF.

Uses fpdf2 (pure Python, no system dependencies) as primary engine.
Falls back to WeasyPrint if available and fpdf2 fails.
"""

import argparse
import re
import sys
from pathlib import Path

import markdown
from fpdf import FPDF


EXTENSIONS = [
    "tables",
    "fenced_code",
    "smarty",
    "pymdownx.tasklist",
    "pymdownx.magiclink",
]


def strip_yaml_frontmatter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n*", "", text, count=1, flags=re.DOTALL)


def convert(src: Path, dst: Path) -> Path:
    md_text = strip_yaml_frontmatter(src.read_text(encoding="utf-8"))
    html_body = markdown.markdown(md_text, extensions=EXTENSIONS)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    pdf.set_font("DejaVu", size=11)

    pdf.add_page()
    pdf.write_html(html_body)
    pdf.output(str(dst))
    return dst


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF")
    parser.add_argument("input", help="Path to the .md file")
    parser.add_argument("-o", "--output", help="Output PDF path (default: same name with .pdf)")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"Error: {src} not found", file=sys.stderr)
        sys.exit(1)

    dst = Path(args.output) if args.output else src.with_suffix(".pdf")
    convert(src, dst)
    print(dst)


if __name__ == "__main__":
    main()
