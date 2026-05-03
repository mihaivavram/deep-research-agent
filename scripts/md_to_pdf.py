#!/usr/bin/env python3
"""Convert a Markdown file to a styled PDF."""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def _ensure_brew_lib_path() -> None:
    """Add Homebrew lib path so WeasyPrint can find Pango/GLib on macOS."""
    if sys.platform != "darwin":
        return
    fallback = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    try:
        prefix = subprocess.check_output(["brew", "--prefix"], text=True).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        prefix = "/opt/homebrew" if os.path.isdir("/opt/homebrew") else "/usr/local"
    lib_dir = f"{prefix}/lib"
    if lib_dir not in fallback:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = f"{lib_dir}:{fallback}".rstrip(":")


_ensure_brew_lib_path()

import markdown  # noqa: E402
from weasyprint import HTML  # noqa: E402

CSS = """
@page {
    size: A4;
    margin: 2cm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
}
h1 { font-size: 22pt; margin-top: 0; border-bottom: 2px solid #e1e4e8; padding-bottom: 8px; }
h2 { font-size: 16pt; margin-top: 24px; border-bottom: 1px solid #e1e4e8; padding-bottom: 6px; }
h3 { font-size: 13pt; margin-top: 20px; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 10pt; }
th, td { border: 1px solid #d0d7de; padding: 8px 12px; text-align: left; }
th { background-color: #f6f8fa; font-weight: 600; }
tr:nth-child(even) { background-color: #f9fafb; }
code { background: #f0f2f4; padding: 2px 6px; border-radius: 3px; font-size: 10pt; }
pre { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; font-size: 9.5pt; }
pre code { background: none; padding: 0; }
a { color: #0969da; text-decoration: none; }
blockquote { border-left: 4px solid #d0d7de; margin: 16px 0; padding: 8px 16px; color: #57606a; }
ul, ol { padding-left: 24px; }
li { margin-bottom: 4px; }
strong { font-weight: 600; }
hr { border: none; border-top: 1px solid #d0d7de; margin: 24px 0; }
"""

EXTENSIONS = [
    "tables",
    "fenced_code",
    "codehilite",
    "toc",
    "smarty",
    "pymdownx.tasklist",
    "pymdownx.magiclink",
]


def strip_yaml_frontmatter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n*", "", text, count=1, flags=re.DOTALL)


def convert(src: Path, dst: Path) -> Path:
    md_text = strip_yaml_frontmatter(src.read_text(encoding="utf-8"))
    html_body = markdown.markdown(md_text, extensions=EXTENSIONS)
    html_doc = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html_body}</body></html>"
    HTML(string=html_doc).write_pdf(str(dst))
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
