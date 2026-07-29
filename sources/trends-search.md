Search for market demand trends on: $ARGUMENTS

Use multiple sources to build a demand curve picture:

**Google Trends — does NOT work here.** `trends.google.com/trends/explore` is a JS application and
returns no time-series data via WebFetch. No Google Trends numbers have ever been obtained in this
environment. Do not budget fetches for it, and **never report a trend direction as if sourced from
Google Trends.**

**What to use instead — demand proxies that actually fetch:**
- **Job-posting volume** for roles tied to the category (rising req counts = real budget movement)
- **Community activity volume** — pullpush comment counts per year for the key term
  (`api.pullpush.io/reddit/search/comment/?q="<term>"&after=<epoch>&before=<epoch>`) is a genuine,
  fetchable demand time-series and the best substitute available
- **Funding flow** over time via press-release wires (`/crunchbase-search`)
- **New product launches** in the category per year (`/producthunt-search`, wires)
- **Google Trends screenshots republished inside articles** — usable if you cite the article and
  its date, not Google Trends directly

**Exploding Topics:**
Use WebSearch for `site:explodingtopics.com $ARGUMENTS` and WebFetch on results to see if the topic is categorized as exploding, peaked, or declining. Also look at related topics they surface.

**Google search volume signals:**
Run WebSearch for `"$ARGUMENTS" trends OR "growing market" OR "market size" OR "industry report"` to find analyst takes and market sizing estimates.

**Keyword and SEO trend coverage:**
Search for `"$ARGUMENTS" "search volume" OR "keyword trends" site:ahrefs.com OR site:semrush.com OR site:moz.com` — these sites often publish free keyword trend data in blog posts.

Synthesize: Is demand growing, plateauing, or declining? When did interest spike? Are there seasonal patterns? What adjacent topics are growing alongside it?

**Bias warning — vendor and analyst market-size reports are consistently inflated.** With Google
Trends unavailable, this skill falls back to market-sizing reports, and those are published by
firms with an incentive to make the category look large (they sell to vendors in it, or sell the
report itself). Whenever you cite a TAM or CAGR figure:
- Name the firm that produced it and note the incentive
- Prefer a range across multiple independent firms over any single number
- Flag it as an estimate, never as measured demand
- Treat a CAGR projection as a marketing claim unless the methodology is disclosed

**Do NOT** report a demand trend as established fact when the only evidence is vendor market-sizing.
Say what the proxy was and how strong it is.

Return trend direction with the specific proxy used for it, key inflection points, related growing
topics, any market size estimates found (each with its publisher and an inflation caveat), and
source URLs.
