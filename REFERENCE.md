# Source Routing Reference

## Source categories

### Core sources (always run)
- `web-search` — general internet search. 100% success across 24 runs, but a monoculture risk:
  heavy AI-generated SEO content on business/product topics. Never the only source.
- `reddit-search` — via the `api.pullpush.io` API. Returns full post and comment bodies with scores.
  (`reddit.com` itself is refused at client level; the API is the only working path.)

Then add **at least two more** sources by measured yield from `sources/SOURCE-HEALTH.md`.
A run must end with real content from **3+ distinct source types**.

### Opportunistic (do not count toward coverage)
- `youtube-search` — **transcripts are not obtainable in this environment.** Title, description,
  and metadata only.

### General research sources
Use when the topic clearly maps to the source's domain.

| Source | Use when |
|---|---|
| `arxiv-search` | Scientific research, ML/AI, physics, math, formal papers |
| `pubmed-search` | Health, medicine, clinical research, pharmacology |
| `github-search` | Open-source software, libraries, developer tools, code |
| `wikipedia-search` | Needs foundational context, definitions, or entity disambiguation |
| `news-search` | Current events, breaking news, recent developments |
| `hackernews-search` | Developer culture, startups, tech industry, product launches |

### Social & community sources
Use when the question is about real-people opinion, professional discourse, workplace/comp signal, or expert Q&A.

| Source | Use when |
|---|---|
| `twitter-search` | Real-time discourse, expert hot-takes, breaking news, viral threads |
| `linkedin-search` | Professional perspectives, Pulse articles, hiring signals |
| `threads-search` | Creator/designer/marketer commentary |
| `blind-search` | Verified-employee anonymous workplace data — comp, layoffs, RTO, culture |
| `quora-search` | Long-form expert Q&A, niche explainers, credentialed answers |

### Product & market research sources
Use when the query is about a product, company, market, competitor, or industry.

| Source | Use when |
|---|---|
| `producthunt-search` | SaaS/tech products, competitive landscape, early adopter sentiment |
| `g2-search` | Software products — ratings, review themes, competitor comparisons |
| `appstore-search` | Mobile-first products, apps, consumer software |
| `amazon-reviews` | Physical products, DTC/B2C, hardware |
| `crunchbase-search` | Funding landscape, investor signals, headcount, company history |
| `trends-search` | Market demand validation, category growth curve |
| `glassdoor-search` | Competitor culture signals, hiring patterns as strategic proxy |
| `wayback-search` | How a competitor's messaging, pricing, or ICP has evolved |

### Investing & financial research sources
Use when the query is about a stock, ETF, fund, sector, macro variable, or investing decision.

| Source | Use when |
|---|---|
| `sec-search` | Company filings, earnings, insider transactions — primary EDGAR data |
| `finviz-search` | Stock screener: valuation ratios, short interest, earnings dates |
| `macrotrends-search` | 20+ year historical financials: margins, FCF, ROIC trends |
| `seekingalpha-search` | Investor thesis writing, earnings reactions, dividend analysis |
| `fred-search` | Fed macro data: CPI, yield curve, money supply, unemployment |
| `stocktwits-search` | Real-time retail sentiment on specific tickers |
| `benzinga-search` | Breaking news, analyst upgrades/downgrades, options flow |
| `bogleheads-search` | Long-term passive investing, fund/ETF debates |
| `valueinvestorsclub-search` | Deep fundamental write-ups from professional value investors |
| `substack-search` | Independent analyst newsletters — macro, quant, sector research |
| `cme-fedwatch-search` | Market-implied Fed rate probabilities |
| `worldbank-search` | Country GDP, inflation, trade — international/EM investing |

---

## Routing: which question maps to which sources

### Product research routing

| Research question | Sources to prioritize |
|---|---|
| Is this market real / is there demand? | `trends-search`, `reddit-search`, `appstore-search` |
| Who are the players / competitive landscape? | `crunchbase-search`, `producthunt-search`, `g2-search` |
| What do users actually hate / what's the gap? | `g2-search`, `amazon-reviews`, `reddit-search`, `appstore-search` |
| Where is money and talent flowing? | `crunchbase-search`, `glassdoor-search` |
| How has a competitor evolved / pivoted? | `wayback-search`, `news-search` |
| What is the market narrative? | `web-search`, `news-search`, `hackernews-search`, `twitter-search` |
| What is it like to work at this company? | `blind-search`, `glassdoor-search`, `reddit-search` |
| What do experts publicly say? | `twitter-search`, `linkedin-search`, `quora-search` |
| Is this a B2C physical product? | `amazon-reviews`, `appstore-search`, `reddit-search` |
| Is this a B2B SaaS product? | `g2-search`, `producthunt-search`, `crunchbase-search`, `glassdoor-search` |

### Investing research routing

| Research question | Sources to prioritize |
|---|---|
| Is this company financially healthy? | `sec-search`, `macrotrends-search`, `finviz-search` |
| What's the analyst / Wall Street view? | `benzinga-search`, `seekingalpha-search`, `news-search` |
| What's the macro backdrop? | `fred-search`, `cme-fedwatch-search`, `news-search` |
| What's retail sentiment right now? | `stocktwits-search`, `reddit-search` |
| Long-term passive / ETF research? | `bogleheads-search`, `macrotrends-search`, `finviz-search` |
| Deep value / fundamental thesis? | `valueinvestorsclub-search`, `sec-search`, `seekingalpha-search` |
| International or emerging-market angle? | `worldbank-search`, `fred-search`, `news-search` |
| Independent / contrarian analyst views? | `substack-search`, `seekingalpha-search`, `valueinvestorsclub-search` |
| Recent catalyst / breaking corporate news? | `benzinga-search`, `news-search`, `sec-search`, `twitter-search` |
| What are insiders doing? | `sec-search`, `finviz-search` |

---

## Query type classification

The agent classifies each query before selecting sources:

| Type | Description | Typical depth |
|---|---|---|
| Factual lookup | Definitions, dates, entity identification | Quick |
| Opinion survey | "What do people think about X" | Standard |
| Product comparison | "Best X for Y" | Standard |
| Market analysis | Competitive landscape, industry trends | Deep |
| Investment thesis | Stock/ETF/macro analysis | Deep |
| How-to / tutorial | "How do I X" | Standard |
| Troubleshooting | "Why does X happen" | Standard |
| Recommendation | "Suggest X like Y" | Standard |

---

## Quality pipeline stages

Each research run passes through these stages in order:

1. **Query analysis** — classify type, decompose sub-questions, reformulate per source
2. **Source selection** — pick skills based on query type + routing tables above
3. **Adaptive health check** — read `sources/SOURCE-HEALTH.md`, demote unreliable sources
4. **Depth budgeting** — set tier (Quick/Standard/Deep) and page fetch limits
5. **Parallel execution** — run all source skills simultaneously with fallback chains
6. **Source triage** — score each page (relevance + authority + recency), drop weak pages, re-query if needed
7. **Gap detection** — check for category, temporal, perspective, and contradiction gaps
8. **Cross-source validation** — trace citation chains, flag bias signals, check freshness
9. **Synthesis** — write report with confidence-scored findings and quality self-assessment

### Source triage quick reference

Configured in `sources/triage-config.yaml`. Each page scored **0-12** — four axes, 0-3 each:
**relevance, authority, recency, independence**.

| Depth tier | Min score to pass | Min pages per sub-question | Re-query rounds |
|---|---|---|---|
| Quick | 7 | 2 | Up to 3 |
| Standard | 5 | 3 | Up to 3 |
| Deep | 4 | 4 | Up to 3 |

**Modifiers:** snippet-only −2; source with 5/5 health +1; bias penalty (largest applicable only) —
SEO content farm −3, affiliate/sponsored −2, vendor self-interest −2, undisclosed position −1.

**Independence** is the citation-chain guard: derivative copies of one study score 0-1 and collapse
into that single origin when counting sources for confidence. Three articles restating one study are
one piece of evidence.

If a sub-question is still below its minimum after the final re-query round, the report **must**
disclose the gap under Coverage & Gaps.

---

# Run Log Schema

Moved here from CLAUDE.md so it does not consume prompt context on every session.
Enforced mechanically by `scripts/validate_log.py` — run `make logs` to check.


Log every research run to `logs/`. One YAML file per run, named to match the report: `logs/<report-name>.yaml`.

### When to log

1. **Start** — immediately when the research query is received, before launching any skills. Run `date -u +%Y-%m-%dT%H:%M:%SZ` to capture the start timestamp.
2. **Each skill** — after each skill completes (or fails/is skipped), record its entry. Run `date -u +%Y-%m-%dT%H:%M:%SZ` for each timestamp.
3. **End** — after the report is written. Run `date -u +%Y-%m-%dT%H:%M:%SZ` for the end timestamp.
4. **Errors** — log every error with full structured fields (see Required Error Fields below). Never log an error as free-text only.

### Required top-level fields

Every log file MUST include ALL of these fields. None are optional — if a value is zero or not applicable, write `0`, `0.0`, `null`, or `"n/a"` explicitly.

```yaml
query: "<the user's original question>"
query_type: "product_comparison"       # REQUIRED: factual | opinion | product | market | investment | how_to | troubleshooting | recommendation
depth_tier: "standard"                 # REQUIRED: quick | standard | deep
start_time: "2026-05-03T14:30:00Z"     # REQUIRED
end_time: "2026-05-03T14:32:45Z"       # REQUIRED
duration_seconds: 165                  # REQUIRED: computed from start_time and end_time
report_file: "results/<filename>.md"   # REQUIRED
sources_selected: 6                    # REQUIRED: total source skills launched
sources_succeeded: 4                   # REQUIRED: skills with status success or partial
sources_failed: 2                      # REQUIRED: skills with status no_results or error
total_pages_fetched: 23                # REQUIRED: total pages WebFetch attempted
pages_fetch_succeeded: 19             # REQUIRED: pages that returned usable content
pages_fetch_failed: 4                  # REQUIRED: pages that returned errors (403, 429, timeout, empty)
fetch_success_rate: 0.83               # REQUIRED: pages_fetch_succeeded / total_pages_fetched
triage_threshold: 4                    # REQUIRED: from triage-config.yaml for the depth tier
pages_passed_triage: 18                # REQUIRED: pages that scored above threshold
pages_dropped_triage: 5                # REQUIRED: pages dropped (includes re-query pages that failed triage)
triage_pass_rate: 0.78                 # REQUIRED: pages_passed_triage / (pages_passed_triage + pages_dropped_triage)
requery_rounds: 1                      # REQUIRED: 0 if no re-query was needed
requery_pages_fetched: 3               # REQUIRED: 0 if no re-query
quality_score: 4                       # REQUIRED: 1-5 from Quality Gates
research_plan: "Product comparison (Standard). Sub-questions: (1) Which models exist? (2) What do users say? (3) What do experts recommend?"
```

### Required step fields

Every step entry MUST include `skill`, `timestamp`, and `status`. Additional fields depend on the step type.

#### Source skill steps (web-search, reddit-search, etc.)

```yaml
steps:
  # SUCCESS — all required fields present
  - skill: web-search
    timestamp: "2026-05-03T14:30:02Z"
    status: success                    # REQUIRED: success | partial | no_results | skipped | error
    sources_fetched: 8                 # REQUIRED for success/partial: how many pages returned usable content
    queries_run: 3                     # REQUIRED: how many WebSearch queries were executed

  # PARTIAL — source returned some data but with failures
  - skill: reddit-search
    timestamp: "2026-05-03T14:30:03Z"
    status: partial
    sources_fetched: 0
    queries_run: 3
    fallback_used: google_snippets     # REQUIRED for partial: google_cache | wayback | archive_ph | google_snippets | none
    fallback_succeeded: true           # REQUIRED for partial: did the fallback produce usable data?
    reason: "direct fetch blocked (403); extracted 3 snippets via Google"  # REQUIRED for partial/no_results/error

  # NO_RESULTS — source was attempted but returned nothing usable
  - skill: twitter-search
    timestamp: "2026-05-03T14:30:03Z"
    status: no_results
    sources_fetched: 0
    queries_run: 2
    fallback_used: google_snippets
    fallback_succeeded: false
    reason: "X/Twitter gated behind login; site-search returned non-Twitter results; snippet extraction found 0 relevant snippets"

  # SKIPPED — source was not attempted
  - skill: arxiv-search
    timestamp: "2026-05-03T14:30:03Z"
    status: skipped
    reason: "not relevant to query type (product comparison)"

  # ERROR — source encountered an unexpected failure
  - skill: hackernews-search
    timestamp: "2026-05-03T14:30:04Z"
    status: error
    sources_fetched: 0
    queries_run: 1
    reason: "Algolia API returned 500 Internal Server Error on all queries"
```

#### Pipeline steps (triage, gap-detection, synthesis, report, pdf, email)

```yaml
  - skill: source-triage
    timestamp: "2026-05-03T14:31:25Z"
    status: success
    pages_scored: 23
    pages_passed: 18
    pages_dropped: 5
    triage_threshold: 4
    requery_rounds: 1
    requery_pages_fetched: 3
    requery_pages_passed: 2

  - skill: gap-detection
    timestamp: "2026-05-03T14:31:30Z"
    status: success                    # success | skipped (for Quick tier)
    gaps_found: 2                      # REQUIRED: number of gaps identified
    followup_searches: 2              # REQUIRED: number of follow-up searches triggered
    reason: "missing user reviews (source category gap); no contrarian perspective found (perspective gap)"

  - skill: synthesis
    timestamp: "2026-05-03T14:31:50Z"
    status: success

  - skill: report-written
    timestamp: "2026-05-03T14:32:45Z"
    status: success

  - skill: pdf-generated
    timestamp: "2026-05-03T14:32:48Z"
    status: success                    # success | error | skipped

  - skill: email-sent
    timestamp: "2026-05-03T14:32:50Z"
    status: success                    # success | error | skipped (if not requested)
```

### Required error fields

Every entry in the `errors` list MUST include ALL of these structured fields. Do NOT log errors as free-text only — the structured fields enable automated analysis.

```yaml
errors:
  # Page-level fetch error (a specific URL failed)
  - skill: reddit-search              # REQUIRED: which skill produced this URL
    timestamp: "2026-05-03T14:30:05Z" # REQUIRED: when the error occurred
    error_type: access_blocked        # REQUIRED: access_blocked | rate_limited | timeout | empty_content | parse_error | redirect_error | server_error | login_required
    http_status: 403                  # REQUIRED: actual HTTP status code, or null if no HTTP response (timeout, DNS failure)
    url: "https://old.reddit.com/r/BuyItForLife/comments/abc123"  # REQUIRED: the specific URL that failed
    fallback_used: google_snippets    # REQUIRED: google_cache | wayback | archive_ph | google_snippets | none
    fallback_succeeded: true          # REQUIRED: did the fallback produce usable content?
    error: "reddit.com returned 403 Forbidden; fell back to Google snippets, extracted 3 relevant snippets"  # REQUIRED: human-readable description for context

  # Skill-level error (the entire skill failed, not a single URL)
  - skill: email-sent
    timestamp: "2026-05-03T14:32:52Z"
    error_type: server_error
    http_status: null
    url: null
    fallback_used: none
    fallback_succeeded: false
    error: "SMTP credentials not configured in .env — SENDER_EMAIL and SENDER_PASSWORD are empty"
```

### Error type definitions

Use these exact values for `error_type` — do not invent new ones or use free-text:

| error_type | When to use | Typical http_status |
|---|---|---|
| `access_blocked` | Server returned 403 or 451, or content is behind a paywall/login wall that blocks scraping | 403, 451 |
| `rate_limited` | Server returned 429 or equivalent throttling response | 429 |
| `timeout` | Request timed out or connection was dropped | null |
| `empty_content` | Page loaded but contained no usable content (only nav, JS shell, or boilerplate) | 200 |
| `parse_error` | Page content was returned but could not be meaningfully extracted (malformed HTML, unexpected format) | 200 |
| `redirect_error` | URL redirected to an unrelated page or domain | 301, 302 |
| `server_error` | Server returned 5xx or an unexpected server-side failure | 500, 502, 503 |
| `login_required` | Content exists but requires authentication to access (distinct from access_blocked — the page tells you to log in rather than just blocking) | 200, 401 |

### Rules
- Timestamps must come from `date -u +%Y-%m-%dT%H:%M:%SZ` (not estimated).
- Write the log file **after** the report is saved — collect entries in memory during the run, then write once at the end.
- `duration_seconds` is computed from `start_time` and `end_time`.
- `fetch_success_rate` is `pages_fetch_succeeded / total_pages_fetched`.
- Do not log the report content — just metadata.
- **Every error MUST have all structured fields** (`error_type`, `http_status`, `url`, `fallback_used`, `fallback_succeeded`, `error`). Never omit fields or log a truncated error entry with only `skill` and `timestamp`. If a field is not applicable, write `null` — do not omit it.
- **Every step MUST have all required fields** for its status type. A `partial` step must include `fallback_used`, `fallback_succeeded`, and `reason`. A `no_results` step must include `reason`. Never write a step entry with only `skill` and `timestamp`.
- **Log individual page failures**, not just skill-level summaries. If 3 out of 5 fetched URLs returned 403, log 3 separate error entries with the specific URLs — not one entry saying "some pages blocked."
- After writing the log, **update `sources/SOURCE-HEALTH.md`** with the success/failure status of each source from this run (see Adaptive Source Selection).