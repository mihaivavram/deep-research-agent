#!/usr/bin/env python3
"""Convert a Markdown file to a styled PDF.

Thin CLI wrapper around report_pdf.render_report().
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report_pdf import DROPPED_EMOJI, render_report  # noqa: E402


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Convert Markdown to PDF")
    parser.add_argument("input", help="Path to the .md file")
    parser.add_argument(
        "-o", "--output", help="Output PDF path (default: same name with .pdf)"
    )
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"Error: {src} not found", file=sys.stderr)
        sys.exit(1)

    dst = Path(args.output) if args.output else src.with_suffix(".pdf")
    render_report(src.read_text(encoding="utf-8"), dst)
    print(dst)

    # The embedded fonts carry no emoji glyphs. Mapped emoji become ASCII markers;
    # anything unmapped is reported here rather than vanishing from the PDF unnoticed.
    if DROPPED_EMOJI:
        glyphs = " ".join(sorted(DROPPED_EMOJI))
        print(
            f"warning: {len(DROPPED_EMOJI)} emoji had no ASCII mapping and were removed "
            f"from the PDF: {glyphs}\n"
            f"         add them to _EMOJI_TEXT in scripts/report_pdf.py, or avoid emoji "
            f"in reports.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
