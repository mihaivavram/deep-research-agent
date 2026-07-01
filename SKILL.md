---
name: deep-research-agent
description: Multi-source deep research agent. Runs parallel searches across 34+ sources (web, Reddit, YouTube, arXiv, SEC, FRED, social media, product review sites, and more), synthesizes findings into a structured report with PDF export. Use when user wants to research a topic deeply, investigate a question, or do competitive/market/investment analysis.
---

# Deep Research Agent

Research orchestrator that searches 34+ sources in parallel and synthesizes findings.

## Quick start

Given a query via `$ARGUMENTS`, immediately start all searches — do not ask for confirmation.

## Source selection

1. **Always run**: web, reddit, youtube (unless user specifies otherwise)
2. **Conditionally run**: Read [REFERENCE.md](REFERENCE.md) to determine which additional sources match the query's domain
3. **Source strategies**: For each selected source, read its strategy file from `~/.agents/skills/deep-research-agent/sources/<source-name>.md` and follow the search instructions there using WebSearch and WebFetch directly

## Execution pipeline

### 1. Query analysis
Classify the query type (factual, opinion, product, market, investment, how-to, troubleshooting, recommendation). Decompose complex queries into 2-4 sub-questions. Reformulate queries per source type (colloquial for Reddit, formal for SEC, technical for arXiv).

### 2. Research plan
Emit a brief plan (query type, sub-questions, sources selected, depth tier, triage threshold). Do not wait for confirmation — start execution immediately after.

### 3. Depth budgeting

| Tier | When | Sources | Page fetches |
|---|---|---|---|
| Quick | Simple factual lookup | 2-3 | 5-8 |
| Standard | Product comparison, opinion survey, how-to | 4-6 | 15-25 |
| Deep | Market analysis, investment thesis, or user says "deep dive" | 8-15 | 30-50 |

### 4. Adaptive source health
Read `sources/SOURCE-HEALTH.md`. Demote sources with 3+/5 recent failures (compensate with `site:` scoped web-search). Prioritize sources with 5/5 recent success.

### 5. Parallel execution
- Run all source searches **in parallel** — launch all at once
- For each source: follow the strategy in its `.md` file, using WebSearch and WebFetch directly
- Fetch **3–5 full pages per source** minimum — don't rely on search snippets
- On failure: follow universal fallback chain (Google cache → Wayback → archive.ph → snippet extraction)
- For follow-up questions, re-run only relevant sources

### 6. Source triage
After fetching, score each page on relevance (0-3) + authority (0-3) + recency (0-3). Read `sources/triage-config.yaml` for thresholds. Drop pages below the tier threshold. If fewer than minimum pages survive per sub-question, re-query with reformulated terms (max 2 rounds). Triaged-out pages are listed in Sources section with `[triaged out — score X/9]`.

### 7. Gap detection
Check for: missing source categories, temporal staleness, missing contrarian views, unresolved contradictions. Run 1-2 targeted follow-up searches to fill gaps.

### 8. Progress reporting
Emit one-line updates after each stage completes (source fetches, triage stats, gap detection results).

## Dynamic source creation

If the user names a source with no existing strategy file in `sources/`, write a new `<source-name>.md` file there following the pattern of existing files (site-scoped search, what to extract, fallback, what NOT to do), then execute it immediately. Announce: `Created new source: <source-name>`

## Output format

Synthesize into a single report:

- **Skills Used** — every source searched, with status (success / skipped / no results)
- **Key Findings** — top takeaways synthesized across all sources, each prefixed with confidence level (High / Medium / Low / Unverified)
- **By Source** — what each source distinctly contributed
- **Consensus vs. Debate** — where sources agree and where they conflict
- **Sources** — all URLs consulted, grouped by source. Triaged-out pages marked with score
- **Reliability Ranking** — sources ranked most to least reliable with brief reason, publication date, and bias signals
- **Research Quality Score** — self-assessed 1-5 based on coverage, source diversity, claim backing, contradiction resolution, staleness

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

Capture timestamps with `date -u +%Y-%m-%dT%H:%M:%SZ`. Create `logs/` if needed. Write `logs/<report-name>.yaml` after the report is saved.

All fields shown below are REQUIRED — write `0`, `0.0`, `null`, or `"n/a"` if not applicable. Never omit fields.

### Top-level fields

```yaml
query: "<question>"
query_type: "product_comparison"       # factual | opinion | product | market | investment | how_to | troubleshooting | recommendation
depth_tier: "standard"                 # quick | standard | deep
start_time: "<ISO>"
end_time: "<ISO>"
duration_seconds: <N>
report_file: "results/<filename>.md"
sources_selected: <N>
sources_succeeded: <N>                 # status success or partial
sources_failed: <N>                    # status no_results or error
total_pages_fetched: <N>
pages_fetch_succeeded: <N>
pages_fetch_failed: <N>
fetch_success_rate: <float>            # pages_fetch_succeeded / total_pages_fetched
triage_threshold: <N>
pages_passed_triage: <N>
pages_dropped_triage: <N>
triage_pass_rate: <float>
requery_rounds: <N>
requery_pages_fetched: <N>
quality_score: <1-5>
research_plan: "<summary string>"
```

### Step entries

Every step MUST include `skill`, `timestamp`, `status`. Additional fields depend on status:

```yaml
steps:
  - skill: <source-name>
    timestamp: "<ISO>"
    status: success                    # success | partial | no_results | skipped | error
    sources_fetched: <N>               # required for success/partial
    queries_run: <N>                   # required for all source skills
    fallback_used: <type>              # required for partial: google_cache | wayback | archive_ph | google_snippets | none
    fallback_succeeded: <bool>         # required for partial
    reason: "<why>"                    # required for partial | no_results | skipped | error
  - skill: source-triage
    timestamp: "<ISO>"
    status: success
    pages_scored: <N>
    pages_passed: <N>
    pages_dropped: <N>
    triage_threshold: <N>
    requery_rounds: <N>
    requery_pages_fetched: <N>
    requery_pages_passed: <N>
  - skill: gap-detection
    timestamp: "<ISO>"
    status: success
    gaps_found: <N>
    followup_searches: <N>
    reason: "<what gaps were found>"
```

### Error entries

Every error MUST include ALL structured fields — never log free-text only:

```yaml
errors:
  - skill: <source-name>
    timestamp: "<ISO>"
    error_type: access_blocked         # access_blocked | rate_limited | timeout | empty_content | parse_error | redirect_error | server_error | login_required
    http_status: 403                   # actual HTTP status, or null
    url: "<the specific URL that failed>"  # or null for skill-level errors
    fallback_used: google_snippets     # google_cache | wayback | archive_ph | google_snippets | none
    fallback_succeeded: true
    error: "<human-readable description>"
```

Log individual page failures, not just skill-level summaries. If 3 URLs returned 403, log 3 separate error entries with specific URLs.

After writing the log, update `sources/SOURCE-HEALTH.md` with success/failure status from this run.
