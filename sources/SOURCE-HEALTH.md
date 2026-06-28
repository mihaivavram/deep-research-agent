# Source Health Registry

Last updated: 2026-06-28

This file is read at the start of each research run (for adaptive source selection) and updated at the end (with success/failure status from that run). Track the last 5 runs per source.

Status codes: S = success, P = partial (snippets/fallback only), F = failure (no usable data)

| Source | Last 5 Runs | Success Rate | Notes |
|---|---|---|---|
| web-search | S | 5/5 | Baseline: most reliable source |
| reddit-search | P | 0/1 | site:reddit.com returned no links; reddit.com fetch refused by tool — synthesis-only |
| youtube-search | S | 1/1 | Channel/creator lists via search; transcripts not needed |
| twitter-search | F | 0/1 | site:x.com returns analyst articles not tweets; login wall |
| hackernews-search | S | 1/1 | Algolia search + item API both reliable |
| news-search | — | — | Accessible outlets reliable; paywalled outlets fail |
| arxiv-search | — | — | API and web search both reliable |
| github-search | S | 1/1 | raw.githubusercontent READMEs reliable (awesome-lists, market-maps) |
| pubmed-search | — | — | PubMed pages and API reliable |
| wikipedia-search | — | — | API and pages reliable |
| linkedin-search | P | 0/1 | Heavily gated; Pulse newsletters via snippets; used Menlo/Microsoft direct instead |
| blind-search | — | — | Gated behind login; snippets only |
| quora-search | — | — | 403 on direct fetch; use Wayback/snippets |
| threads-search | — | — | Variable accessibility |
| producthunt-search | P | 0/1 | Category/product pages JS-heavy; search snippets carried the signal |
| g2-search | S | 1/1 | learn.g2.com buyer guides fetch cleanly |
| appstore-search | — | — | |
| amazon-reviews | — | — | |
| crunchbase-search | — | — | |
| trends-search | S | 1/1 | Demand/market-size via web synthesis (trends.google direct not needed) |
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
| substack-search | S | 1/1 | Most posts accessible (The AI Economy fetched fully) |
| cme-fedwatch-search | — | — | |
| worldbank-search | — | — | API reliable |
