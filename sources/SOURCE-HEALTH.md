# Source Health Registry

> **GENERATED FILE — do not hand-edit.**
> Measured columns come from `logs/*.yaml`; access-path facts come from
> `sources/source-health.yaml`. Regenerate with `python3 scripts/derive_health.py`.
> To record a newly-discovered access path, edit `sources/source-health.yaml`
> **and** the relevant `sources/<skill>.md` strategy file, then regenerate.

Runs analyzed: 24 · most recent run start: 2026-07-29T20:29:01Z

Status codes: `S` = success · `P` = partial (snippets/fallback only) · `F` = failure

## Measured reliability

| Source | Last 5 attempts | Success rate | Tier |
|---|---|---|---|
| reddit-search | F F F F F | 0/5 (0%) | core |
| youtube-search | S S F F F | 2/5 (40%) | opportunistic |
| crunchbase-search | P P P | 1.5/3 (50%) | optional |
| glassdoor-search | P | 0.5/1 (50%) | optional |
| twitter-search | S S S F F | 3/5 (60%) | optional |
| amazon-reviews | S P P | 2/3 (67%) | optional |
| trends-search | S S F | 2/3 (67%) | optional |
| quora-search | P S S S F | 3.5/5 (70%) | optional |
| g2-search | S S P P | 3/4 (75%) | optional |
| hackernews-search | S S S P P | 4/5 (80%) | optional |
| linkedin-search | S S S P P | 4/5 (80%) | optional |
| producthunt-search | S S P | 2.5/3 (83%) | optional |
| news-search | S S S P S | 4.5/5 (90%) | optional |
| blind-search | S S | 2/2 (100%) | optional |
| deep-fetch | S S | 2/2 (100%) | — |
| github-search | S S S | 3/3 (100%) | optional |
| pdf-export | S S S S S | 5/5 (100%) | — |
| substack-search | S S | 2/2 (100%) | optional |
| threads-search | S | 1/1 (100%) | optional |
| web-fetch-deep-dives | S S | 2/2 (100%) | — |
| web-search | S S S S S | 5/5 (100%) | core |
| web-search-followup | S | 1/1 (100%) | — |
| web-search-lacrm-specific | S | 1/1 (100%) | — |
| appstore-search | — | — | optional |
| arxiv-search | — | — | optional |
| benzinga-search | — | — | optional |
| bogleheads-search | — | — | optional |
| cme-fedwatch-search | — | — | optional |
| finviz-search | — | — | optional |
| fred-search | — | — | optional |
| macrotrends-search | — | — | optional |
| pubmed-search | — | — | optional |
| sec-search | — | — | optional |
| seekingalpha-search | — | — | optional |
| stocktwits-search | — | — | optional |
| valueinvestorsclub-search | — | — | optional |
| wayback-search | — | — | optional |
| wikipedia-search | — | — | optional |
| worldbank-search | — | — | optional |

## Access paths per source

### amazon-reviews
*last verified: 2026-07-27*

**Works:**

- Google snippets carry product name, star rating, review count
- Reddit via pullpush is the strongest substitute for real verbatims
- Manufacturer/non-Amazon retailer pages and RTINGS/Wirecutter often fetch

**Dead — do not budget fetches:**

- amazon.com product and review pages — HTML head only, no body

**Notes:** Watch for variant-merging (reviews from a different model pooled onto one listing) and incentivized reviews. Corroborate strong claims against Reddit before calling consensus.

### appstore-search

**Notes:** Not yet characterized.

### arxiv-search
*last verified: 2026-06-20*

**Works:**

- arXiv API and web search both reliable

### benzinga-search

**Notes:** Not yet characterized.

### blind-search
*last verified: 2026-07-27*

**Works:**

- teamblind.com post URLs fetch cleanly and return full reply threads with employer tags

**Notes:** High value as a Reddit substitute for workplace topics — verified employees, financially disinterested, unusually candid.

### bogleheads-search

**Notes:** Not yet characterized.

### cme-fedwatch-search

**Notes:** Not yet characterized.

### crunchbase-search
*last verified: 2026-07-27*

**Works:**

- Press-release wires (GlobeNewswire, BusinessWire, PRNewswire, AccessWire) — primary path
- SEC EDGAR Form D for private raises — primary source, prefer when it exists
- Snippets for crunchbase.com carry total-raised and founded-year

**Dead — do not budget fetches:**

- crunchbase.com — never fetched successfully in 3 logged runs
- cbinsights.com — surfaces in results, does not fetch
- pitchbook.com — paywalled

**Notes:** Repeat investors across competitors signal category conviction — more useful than round size.

### finviz-search

**Notes:** Not yet characterized.

### fred-search
*last verified: 2026-06-20*

**Works:**

- FRED API reliable

### g2-search
*last verified: 2026-07-27*

**Works:**

- Capterra — the ONLY reliable full fetch. Verbatims carry reviewer name, role, industry, company size, date.
- Get product IDs from a capterra.com/compare/<id1>-<id2>/ URL first
- GetApp fetches but returns ratings only, no verbatim text

**Dead — do not budget fetches:**

- g2.com — 403
- trustradius.com — 403
- trustpilot.com — 403
- gartner.com Peer Insights — unreachable
- softwareadvice.com — 404 on review paths

**Notes:** Guessed Capterra /p/<id>/<Name>/reviews/ paths have 404'd repeatedly. Derive the ID.

### github-search
*last verified: 2026-07-27*

**Works:**

- github.com/search?q=&type=repositories&sort=stars renders server-side
- raw.githubusercontent.com/<o>/<r>/main/README.md — preferred content path

**Dead — do not budget fetches:**

- /blob/ HTML views — frequently return empty bodies

**Notes:** Repo landing pages can be metadata-thin; recover via the raw README.

### glassdoor-search
*last verified: 2026-07-27*

**Works:**

- Google snippets

**Dead — do not budget fetches:**

- glassdoor.com direct — gated

**Notes:** Snippet-level only, as expected. Prefer blind-search for candid employee signal.

### hackernews-search
*last verified: 2026-07-29*

**Works:**

- hn.algolia.com/api/v1/search?query=<q>&tags=story — VERIFIED
- hn.algolia.com/api/v1/items/<id> — full comment tree, no rate limits
- news.ycombinator.com/item?id= pages fetch cleanly

**Notes:** Algolia is QUERY-SYNTAX SENSITIVE — quoted multi-term and OR queries return nbHits=0. Use short unquoted keywords plus numericFilters=points>N. If nbHits=0, drop a term and retry before concluding the topic is absent.

### linkedin-search
*last verified: 2026-07-27*

**Works:**

- Google snippets only — reliably carry group member counts and company follower counts

**Dead — do not budget fetches:**

- linkedin.com URLs including /pulse and /posts — never fetched successfully

**Notes:** Good for audience sizing, useless for content. Substitute trade press; use blind-search for employee views.

### macrotrends-search

**Notes:** Not yet characterized.

### news-search
*last verified: 2026-07-27*

**Works:**

- Fortune, Forbes, Yahoo Finance fetch cleanly
- Insurance Journal, GlobeNewswire, BusinessWire, PRNewswire, Coverager fetch cleanly
- Trade press for any vertical is more reliable than general tech press

**Dead — do not budget fetches:**

- GeekWire — 403
- CNBC — 403

**Notes:** GlobeNewswire/BusinessWire are the reliable path to dated vendor adoption numbers.

### producthunt-search
*last verified: 2026-07-27*

**Works:**

- Snippet-level

**Dead — do not budget fetches:**

- leaderboard pages not fetched in logged runs

### pubmed-search
*last verified: 2026-06-20*

**Works:**

- PubMed pages and E-utilities API reliable

### quora-search
*last verified: 2026-07-27*

**Works:**

- Google snippets

**Dead — do not budget fetches:**

- quora.com direct fetch — 403
- Wayback (formerly suggested) — refused at client

### reddit-search
*last verified: 2026-07-29*

**Works:**

- api.pullpush.io/reddit/search/submission/?q=<q>&size=25&sort=desc — VERIFIED
- api.pullpush.io/reddit/search/comment/?q=<q>&score=>10&size=50 — VERIFIED, returns full comment bodies with score and subreddit
- subreddit= and after=/before= (epoch) parameters both work

**Dead — do not budget fetches:**

- reddit.com / old.reddit.com / .json paths — refused at client
- WebSearch allowed_domains:[reddit.com] — API 400
- site:reddit.com — zero Reddit URLs
- frontpagemetrics.com (404), subredditstats (defunct), r.jina.ai (403)

**Notes:** Was previously marked "fully unavailable — do not budget fetches." That was WRONG and cost 20 runs of community signal. pullpush relevance matching is loose: quote phrases, scope by subreddit, and filter results manually. fields= parameter is ignored.

### sec-search
*last verified: 2026-07-27*

**Works:**

- EDGAR API and filing documents reliable — primary source, highest authority

### seekingalpha-search
*last verified: 2026-06-20*

**Dead — do not budget fetches:**

- Paywalled; public summaries sometimes accessible

### stocktwits-search

**Notes:** Not yet characterized.

### substack-search
*last verified: 2026-07-27*

**Works:**

- Most Substack posts fetch cleanly

### threads-search

**Notes:** Variable accessibility; not yet characterized.

### trends-search
*last verified: 2026-07-27*

**Works:**

- pullpush comment counts per time window — a genuine fetchable demand time-series
- Job-posting volume, funding flow, new-launch counts as demand proxies
- Google Trends screenshots republished inside dated articles

**Dead — do not budget fetches:**

- trends.google.com/trends/explore — JS app, no time-series via WebFetch

**Notes:** NO Google Trends data has ever been obtained. Falls back to vendor market-size reports, which are consistently INFLATED — always name the publishing firm and its incentive.

### twitter-search
*last verified: 2026-07-27*

**Works:**

- threadreaderapp, syndicated embeds, snippets from x.com status URLs

**Dead — do not budget fetches:**

- x.com / twitter.com direct — login wall

**Notes:** Snippet-level only in practice.

### valueinvestorsclub-search
*last verified: 2026-06-20*

**Dead — do not budget fetches:**

- Paywalled; public summaries sometimes accessible

### wayback-search
*last verified: 2026-07-29*

**Works:**

- Press-release wires (date-stamped) read chronologically
- Company's own /blog, /changelog, /releases pages
- Dated third-party commentary and Capterra verbatims (which carry dates)

**Dead — do not budget fetches:**

- web.archive.org (all paths incl. CDX API) — refused at client
- archive.ph — refused at client
- timetravel.mementoweb.org — DNS failure

**Notes:** No web archive is reachable. Skill repurposed to reconstruct timelines from dated live sources; reports must say the timeline is a reconstruction and name coverage gaps.

### web-search
*last verified: 2026-07-29*

**Works:**

- General WebSearch; fetch 4-6 top results directly.
- High-yield classes: trade associations, industry bodies, conference agenda pages, independent vendor user groups, press-release wires.

**Dead — do not budget fetches:**

- site:reddit.com — returns zero Reddit URLs

**Notes:** Most reliable source (100% across 24 logged runs) but a monoculture risk. Business, startup-idea and "best X" queries return a very high density of AI-generated SEO content — budget for aggressive triage. Known-403 publishers: GeekWire, CNBC.

### wikipedia-search
*last verified: 2026-06-20*

**Works:**

- REST API and article pages reliable

### worldbank-search
*last verified: 2026-06-20*

**Works:**

- World Bank API reliable

### youtube-search
*last verified: 2026-07-29*

**Works:**

- General WebSearch (unscoped) surfaces video pages with titles/descriptions in snippets
- Direct watch-page fetch sometimes yields title, channel, views, description, chapters
- Best substitute: the creator's own site/blog/podcast page, which fetches cleanly

**Dead — do not budget fetches:**

- youtube.com/results?search_query= — footer nav only
- youtube.com/api/timedtext — empty
- youtubei/v1/player — HTTP 405
- downsub.com — app shell, no transcript
- youtubetotranscript.com — HTTP 403
- Invidious public instances (inv.nadeko.net) — no response
- site:youtube.com — returns SEO listicles, not YouTube pages

**Notes:** TRANSCRIPTS ARE NOT OBTAINABLE. Every documented path tested and failed 2026-07-29. Description-level signal only; do not count toward sub-question coverage.

## Environment-level blocks (not source failures)

Hosts refused by the client itself. No fallback rung can rescue these.

| Host | Status | Impact |
|---|---|---|
| `reddit.com (all subdomains, incl. old.reddit.com and .json paths)` | refused at client level | Reddit HTML is unreachable. Use api.pullpush.io (works). Never mark Reddit unavailable. |
| `web.archive.org (incl. /cdx/ API)` | refused at client level | Wayback is unavailable as fallback tier. Reconstruct timelines from dated live sources. |
| `archive.ph / archive.today` | refused at client level | archive.ph fallback tier unavailable. |
| `timetravel.mementoweb.org` | DNS does not resolve | No memento aggregator available. |
| `r.jina.ai` | 403 blocked by network security | Reader-proxy workaround unavailable. |
| `facebook.com (groups + pages)` | fetches but returns title only | Group member counts and post content never obtainable. Source size claims elsewhere. |
| `insurance-forums.com` | 403 on every path | Thread titles indexed by search; post bodies never retrievable. |

## Working fallback chain in this environment

1. platform API (pullpush, Algolia, EDGAR, FRED, Wikipedia REST)
2. alternate publisher of the same data (GlobeNewswire, BusinessWire, PRNewswire, trade press)
3. Google cache
4. Google snippet extraction (flag as snippet-sourced)

## Cross-cutting lessons

- **b2b-niche-mapping** (added 2026-07-27) — For B2B niche audience/venue mapping the social platforms are all gated, and the highest-yield sources are institutional: trade-association sites, independent vendor user groups, conference agenda pages (session titles reveal which job roles own which problem), and industry-body directories with named executive contacts. Budget fetches there, not at Reddit/Facebook/LinkedIn.
- **api-before-surrender** (added 2026-07-29) — Never record a source as unavailable without trying a platform API. Reddit was written off for ~20 runs while api.pullpush.io worked the whole time. A blocked HTML page is not evidence the data is inaccessible, and a surrender persisted into source health suppresses every future attempt.
- **pdf-emoji-loss** (added 2026-07-29) — scripts/report_pdf.py embeds Arial/DejaVu, which have no emoji coverage, so emoji silently vanish from PDFs. md_to_pdf.py now transliterates emoji to ASCII markers before rendering — keep that mapping updated rather than putting raw emoji in reports.

