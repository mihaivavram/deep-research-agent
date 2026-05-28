# Source Routing Reference

## Source categories

### Core sources (always run)
- `web-search` — general internet search
- `reddit-search` — Reddit posts and threads
- `youtube-search` — YouTube videos and transcripts

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
