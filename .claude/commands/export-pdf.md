Convert a research report to PDF: $ARGUMENTS

## What this does
Converts a Markdown report from the `results/` directory into a styled PDF.

## How to run

1. Identify the target file. If `$ARGUMENTS` names a file directly, use that. If it's a query or topic, find the matching report in `results/`.

2. Run the conversion script by activating the virtual environment from `.env` and running the script:

```bash
source .env && source "$VIRTUAL_ENV/bin/activate" && python3 scripts/md_to_pdf.py "results/<filename>.md"
```

3. The PDF is saved next to the Markdown file in `results/` with the same name and `.pdf` extension.

4. Report to the user:
   - Confirm the PDF was created
   - Give the full path: `results/<filename>.pdf`
   - Mention they can open it with: `open results/<filename>.pdf` (macOS) or their file manager

## If no arguments provided
List all `.md` files in `results/` and ask which one to convert.

## If "all" is specified
Convert every `.md` file in `results/` to PDF.
