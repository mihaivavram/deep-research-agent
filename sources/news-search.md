Search recent news coverage for: $ARGUMENTS

News search provides timely reporting, expert quotes, and event timelines from professional journalists. The key challenge is paywalls — many major outlets block WebFetch. **Target accessible outlets first**, then use fallback paths for paywalled sources.

**Primary strategy — multi-angle news queries:**
Run 3–4 WebSearch queries:
- `$ARGUMENTS 2026` — recency bias toward current year
- `$ARGUMENTS news OR report OR announcement` — bias toward journalism over SEO content
- `$ARGUMENTS site:reuters.com OR site:apnews.com OR site:bbc.com` — wire services and public broadcasters (reliably accessible)
- `$ARGUMENTS site:techcrunch.com OR site:theverge.com OR site:arstechnica.com` — tech-focused outlets (reliably accessible)

**Accessible-first domain targeting:**
Prioritize WebFetch on outlets known to be reliably accessible and high-quality:

| Tier | Outlets | Notes |
|---|---|---|
| **Tier 1 (wire services)** | Reuters, AP News, BBC | Factual, minimal opinion, usually accessible |
| **Tier 2 (tech/business)** | TechCrunch, The Verge, Ars Technica, Wired, MIT Tech Review | Good for tech/product/industry stories |
| **Tier 3 (general quality)** | The Guardian, NPR (text), PBS, Al Jazeera English | Broad coverage, usually accessible |
| **Tier 4 (specialized)** | Industry-specific outlets relevant to the query | Varies by domain |

**Paywalled outlets — do NOT attempt direct WebFetch:**
These outlets consistently return 403/451 and waste tokens:
- WSJ, Bloomberg Terminal, Financial Times, NYT, The Information, The Athletic
- CNBC (intermittent), CNN (intermittent), Forbes (soft paywall)

For paywalled outlets found in search results:
1. Extract the headline, byline, and Google snippet text (often contains the key data point)
2. Try `archive.ph/newest/PAYWALLED_URL` — often has readable snapshots
3. Try `web.archive.org/web/*/PAYWALLED_URL` — works for older articles
4. Search for the same story on an accessible outlet — wire service stories (Reuters, AP) are syndicated widely

**Press release primary sources:**
For corporate news, search the company's newsroom directly:
- `site:COMPANY.com/press OR site:COMPANY.com/newsroom $ARGUMENTS`
- `site:prnewswire.com OR site:businesswire.com $ARGUMENTS`
Press releases are always accessible and contain the authoritative first-party statement.

**What to extract from each article:**
- Publication date and author/byline
- Key facts, data points, and direct quotes from named sources
- Who is quoted and their role (CEO statement vs. anonymous source vs. analyst)
- Timeline of events if the story is developing
- Named sources cited within the article (for citation-chain awareness)

**Do NOT:**
- Waste tokens attempting to WebFetch known-paywalled domains — go straight to fallback
- Treat opinion/editorial pieces as equivalent to news reporting — distinguish clearly
- Rely on aggregator sites that rewrite wire stories without adding value
- Ignore publication date — a 6-month-old article may be completely outdated for fast-moving stories

Return: key findings with publication dates and bylines, a timeline of events if relevant, direct quotes from named sources, and all source URLs. Note which outlets were paywalled and whether content came from full article, archive snapshot, or snippet extraction.
