# Source Health Registry

Last updated: 2026-07-29 (run: python-md-to-pdf-engines-unix)

This file is read at the start of each research run (for adaptive source selection) and updated at the end (with success/failure status from that run). Track the last 5 runs per source.

Status codes: S = success, P = partial (snippets/fallback only), F = failure (no usable data)

| Source | Last 5 Runs | Success Rate | Notes |
|---|---|---|---|
| web-search | S S S S S | 5/5 | Consistently reliable. This run: WeasyPrint/Pandoc/Typst/PyPI docs and Baeldung all fetched cleanly. Prior: Medium, a16z, SaaStr, IndieHackers, personal blogs, Substack. Blocked: G2, TrustRadius, Trustpilot, insurance-forums, agentforthefuture (all 403). **Association / trade-body / conference-organiser sites fetch cleanly for B2B niche mapping.** **Warning: business/startup-idea queries return a very high density of AI-generated SEO content farms — budget for aggressive triage** |
| reddit-search | F F F F | 0/4 | **BLOCKED AT USER-AGENT LEVEL — CONFIRMED AGAIN.** WebSearch `allowed_domains:[reddit.com]` returns API 400 'not accessible to our user agent'; `site:reddit.com` returns zero Reddit URLs; `old.reddit.com` and `.json` API both refused at client. Third-party mirrors also dead: **frontpagemetrics.com = 404**, subredditstats defunct. Treat as fully unavailable — do not budget fetches, and **state the non-coverage explicitly in the report rather than inferring subreddit names**. Best substitutes: teamblind.com (verified employees), niche industry forums, review-site verbatims w/ reviewer role + company size |
| youtube-search | F F F F | 0/4 | `youtube.com/results` returns footer nav only. `site:youtube.com` returns only SEO listicles. Treat as unavailable. **Substitute that worked this run: fetch podcast host sites and conference agendas directly** — they carry the same practitioner signal plus contact info |
| twitter-search | — | — | Login wall; use threadreaderapp + syndicated embeds. x.com status URLs surface in web-search results as snippets only |
| hackernews-search | P P | 1/2 | Algolia API works but is **query-syntax sensitive** — quoted multi-term and OR queries return nbHits=0. Use short unquoted keyword queries + `numericFilters=points>N`. Item API (`/api/v1/items/ID`) returns full comments reliably. Direct `news.ycombinator.com/item?id=` pages fetch cleanly |
| news-search | S P S | 2.5/3 | Fortune, Forbes, Yahoo Finance fetch cleanly. **GeekWire and CNBC return 403.** Insurance Business, IA Magazine, Law360/MLex all fetch cleanly. Added this run: **Insurance Journal, GlobeNewswire, BusinessWire, Coverager, PRNewswire all fetch cleanly** — GlobeNewswire/BusinessWire are the reliable path to vendor adoption numbers |
| arxiv-search | — | — | API and web search both reliable |
| github-search | S | 1/1 | Search page works. **Prefer `raw.githubusercontent.com/.../README.md` over `/blob/` HTML views** — blob pages often return empty bodies via WebFetch. Repo landing pages can be metadata-thin; recover via raw README |
| pubmed-search | — | — | PubMed pages and API reliable |
| wikipedia-search | — | — | API and pages reliable |
| linkedin-search | P P | 1/2 | Never fetches. Snippets reliably carry **group member counts and company follower counts** (e.g. Insurance Journal group 72,150; Big I 17,443) — useful for sizing, useless for content. Substitute trade press for substance |
| blind-search | S | 1/1 | **Upgraded — teamblind.com post URLs fetch cleanly and return full reply threads with employer tags.** High value as a Reddit substitute: verified employees, financially disinterested, unusually candid |
| quora-search | — | — | 403 on direct fetch; use Wayback/snippets |
| threads-search | — | — | Variable accessibility |
| producthunt-search | P | 0.5/1 | Snippet-level only this run; leaderboard pages not fetched |
| g2-search | P P | 1/2 | **Capterra = the only reliable full fetch** (verbatim quotes w/ reviewer first name, role, industry, company size, date). **SoftwareAdvice returned 404 this run — downgrade it.** G2, TrustRadius, Trustpilot, Gartner Peer Insights = consistent 403/unreachable. **Get Capterra product IDs from a `capterra.com/compare/<id1>-<id2>/` URL first** — guessed `/p/<id>/<Name>/reviews/` paths 404'd twice. GetApp fetches but returns ratings only, no verbatim |
| appstore-search | — | — | |
| amazon-reviews | P | 0.5/1 | Product pages return HTML head only — no price/rating/review body. Usable for product IDs via snippets only |
| crunchbase-search | P P P | 1.5/3 | No direct fetch in three runs; BusinessWire/InsurTech Digital/New Market Pitch/Startup Intros/Morningstar-AccessWire snippets carried funding data. CB Insights pages surface in results but do not fetch |
| trends-search | F | 0/1 | No Google Trends time-series obtainable via search. Falls back to vendor market-size reports, which are consistently inflated — flag bias when used |
| glassdoor-search | P | 0.5/1 | Snippet-level only, as expected |
| wayback-search | F | 0/1 | `web.archive.org` refused at client level — tier-2 of universal fallback chain is UNAVAILABLE in this environment |
| sec-search | — | — | EDGAR API reliable. Skipped this run (all vendors PE-owned/private) |
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

## Environment-level blocks (not source failures)

These hosts are refused by the client itself, so the documented universal fallback chain is partially unavailable:

| Host | Status | Impact |
|---|---|---|
| `reddit.com` / `www.reddit.com` / `old.reddit.com` | Refused (client + search user-agent) | Reddit is fully unreachable by every documented path. Third-party mirrors also dead (`frontpagemetrics.com` 404). Substitute: niche industry forums, review-site verbatim quotes with reviewer role/company size |
| `web.archive.org` | Refused (client) | Fallback chain tier 2 (Wayback) unavailable |
| `archive.ph` | Refused (client) | Fallback chain tier 3 (archive.ph) unavailable |
| `facebook.com` (groups + pages) | Fetches but returns title only | Group member counts, rules and post content are never obtainable. Size claims must be sourced from the org's own site or trade press, and conflicting figures flagged |
| `insurance-forums.com` | 403 on every path | Thread titles are indexed by search; post bodies never retrievable. Size stats obtainable via Feedspot snippets |

**Practical fallback chain in this environment:** Google cache -> Google snippet extraction -> alternate publisher of the same data. Tiers 2 and 3 are dead ends; skip them.

## Cross-cutting lesson (added 2026-07-27)

For **B2B niche audience/venue mapping**, the social platforms are all gated and the highest-yield sources are institutional: trade-association sites, **independent vendor user groups** (appliedclientnetwork.org, netvu.org, hawksoftusergroup.org), **conference agenda pages** (session titles reveal exactly which job roles own which problem), and **industry-body directories with named executive contacts** (networksalliance.com was the single best source of the run). Budget fetches there, not at Reddit/Facebook/LinkedIn.

## PDF export note

`scripts/md_to_pdf.py` uses an Arial subset with **no emoji coverage** (missing at minimum: 🎯 ⭐ ⚠️ ✅ ❌ and ▶ U+25B6). Emoji in a report silently drop from the PDF. **Write reports with ASCII/text markers**, or strip emoji before the PDF step.
