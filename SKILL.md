---
name: deep-research-agent
description: Multi-source deep research agent. Runs parallel searches across 37+ sources (web, Reddit, YouTube, arXiv, SEC, FRED, social media, product review sites, and more), synthesizes findings into a structured report with PDF export. Use when user wants to research a topic deeply, investigate a question, or do competitive/market/investment analysis.
---

# Deep Research Agent

Research orchestrator that searches 37+ sources in parallel and synthesizes findings.

## Quick start

Given a query via `$ARGUMENTS`, immediately start all searches — do not ask for confirmation.

## Source selection

1. **Always run**: web, reddit, youtube (unless user specifies otherwise)
2. **Conditionally run**: Read [REFERENCE.md](REFERENCE.md) to determine which additional sources match the query's domain
3. **Source strategies**: For each selected source, read its strategy file from `~/.agents/skills/deep-research-agent/sources/<source-name>.md` and follow the search instructions there using WebSearch and WebFetch directly

## Execution

- Run all source searches **in parallel** — launch all at once
- For each source: follow the strategy in its `.md` file, using WebSearch and WebFetch directly
- Fetch **3–5 full pages per source** minimum — don't rely on search snippets
- Skip sources that return no results or are blocked — continue silently
- For follow-up questions, re-run only relevant sources

## Dynamic source creation

If the user names a source with no existing strategy file in `sources/`, write a new `<source-name>.md` file there following the pattern of existing files (site-scoped search, what to extract, fallback, what NOT to do), then execute it immediately. Announce: `Created new source: <source-name>`

## Output format

Synthesize into a single report:

- **Skills Used** — every source searched, with status (success / skipped / no results)
- **Key Findings** — top takeaways synthesized across all sources
- **By Source** — what each source distinctly contributed
- **Consensus vs. Debate** — where sources agree and where they conflict
- **Sources** — all URLs consulted, grouped by source
- **Reliability Ranking** — sources ranked most to least reliable with brief reason

## Saving the report

1. Create `results/` in the current working directory if it doesn't exist
2. Save as `results/<query-slug>.md` (lowercase, hyphenated, max 50 chars). Include YAML front-matter:
   ```yaml
   ---
   query: "<original question>"
   date: "<YYYY-MM-DD>"
   skills_used: [list, of, sources]
   ---
   ```
3. Attempt PDF generation (skip silently if dependencies are missing):
   ```bash
   python3 ~/.agents/skills/deep-research-agent/scripts/md_to_pdf.py "results/<filename>.md" 2>/dev/null || true
   ```
4. Tell the user: `Report saved to results/<filename>.md`

5. **Email (opt-in only)** — only if the user explicitly asks for email delivery (e.g. "email me the results", "send me the report"):
   ```bash
   python3 ~/.agents/skills/deep-research-agent/scripts/send_email.py "results/<filename>.md"
   ```
   The script reads SMTP credentials (`SMTP_SERVER`, `SMTP_PORT`, `SENDER_EMAIL`, `SENDER_PASSWORD`, `RECIPIENT_EMAIL`) from the project `.env`. It attaches both the `.md` and `.pdf` files. If the email fails, log the error but don't block. If the user does not mention email, skip this step entirely.

## Logging

Capture timestamps with `date -u +%Y-%m-%dT%H:%M:%SZ`. Create `logs/` if needed. Write `logs/<report-name>.yaml` after the report is saved:

```yaml
query: "<question>"
start_time: "<ISO>"
end_time: "<ISO>"
duration_seconds: <N>
report_file: "results/<filename>.md"
steps:
  - skill: <source-name>
    timestamp: "<ISO>"
    status: success|no_results|skipped|error
    sources_fetched: <N>
errors: []
```
