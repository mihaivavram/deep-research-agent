# Source Health Registry

Last updated: 2026-06-22

This file is read at the start of each research run (for adaptive source selection) and updated at the end (with success/failure status from that run). Track the last 5 runs per source.

Status codes: S = success, P = partial (snippets/fallback only), F = failure (no usable data)

| Source | Last 5 Runs | Success Rate | Notes |
|---|---|---|---|
| web-search | — | — | Baseline: most reliable source |
| reddit-search | — | — | Historically blocked; use cache/JSON/snippet fallbacks |
| youtube-search | — | — | Transcripts often blocked; descriptions/titles usually work |
| twitter-search | — | — | Login wall; use threadreaderapp + syndicated embeds |
| hackernews-search | — | — | Algolia API reliable; direct HN pages rate-limited |
| news-search | — | — | Accessible outlets reliable; paywalled outlets fail |
| arxiv-search | — | — | API and web search both reliable |
| github-search | — | — | Search page and raw READMEs reliable |
| pubmed-search | — | — | PubMed pages and API reliable |
| wikipedia-search | — | — | API and pages reliable |
| linkedin-search | — | — | Heavily gated; snippet-level mostly |
| blind-search | — | — | Gated behind login; snippets only |
| quora-search | — | — | 403 on direct fetch; use Wayback/snippets |
| threads-search | — | — | Variable accessibility |
| producthunt-search | — | — | |
| g2-search | — | — | |
| appstore-search | — | — | |
| amazon-reviews | — | — | |
| crunchbase-search | — | — | |
| trends-search | — | — | |
| glassdoor-search | — | — | |
| wayback-search | — | — | |
| sec-search | — | — | EDGAR API reliable |
| finviz-search | — | — | |
| macrotrends-search | — | — | |
| seekingalpha-search | — | — | Paywalled; public summaries sometimes accessible |
| fred-search | — | — | API reliable |
| stocktwits-search | — | — | |
| benzinga-search | — | — | |
| bogleheads-search | — | — | |
| valueinvestorsclub-search | — | — | Paywalled; public summaries sometimes accessible |
| substack-search | — | — | Most posts accessible |
| cme-fedwatch-search | — | — | |
| worldbank-search | — | — | API reliable |
