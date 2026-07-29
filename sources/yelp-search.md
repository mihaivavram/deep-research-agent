Search Yelp for local business reviews and ratings on: $ARGUMENTS

Yelp is the deepest source for **local service-provider reviews, star ratings, and review volume** — and it is especially useful for distinguishing solo/independent operators from large companies, since listings show whether a business is one person or a franchise. Yelp partially blocks scraping but its listing and "best of" pages are well-indexed in Google, so site-search + snippet extraction carries most of the signal.

**Primary search strategy — Google site-search (run 3-4 queries):**
- `site:yelp.com $ARGUMENTS` — broad sweep
- `site:yelp.com "best" $ARGUMENTS [CITY]` — Yelp's curated "Best of" list pages aggregate top-rated providers with ratings inline
- `site:yelp.com $ARGUMENTS [CITY/NEIGHBORHOOD]` — scope to locality
- `$ARGUMENTS yelp reviews [CITY]` — catch the Yelp list pages that rank providers

**Fetching content — ordered fallback chain:**
1. **Yelp "Best of" list pages (best path):** URLs like `yelp.com/search?find_desc=...&find_loc=...` and `yelp.com/c/[city]/[category]` aggregate many providers with star rating + review count. These often fetch and give a ranked shortlist in one page.
2. **Google snippet extraction:** Individual business snippets show business name, star rating, review count, and neighborhood. Extract from every result.
3. **Wayback Machine:** WebFetch `https://web.archive.org/web/*/YELP_URL` for business pages if the live page is blocked.
4. **Direct WebFetch (attempt):** Try the business page; extract rating, review count, categories, and top review text when it renders.

**What to extract:**
- Business/provider name, overall star rating, and total review count (volume matters — 5 stars on 3 reviews is weak)
- Whether it is a solo operator / "family owned" / independent vs. a large multi-crew company (check the "About" text and review language)
- Recurring themes in reviews: responsiveness, pricing/fairness, quality, licensing/permits, punctuality
- Neighborhood/service-area coverage
- Consistently top-ranked names across multiple Yelp list pages (strongest signal)
- Red flags: patterns of complaints, no-shows, billing disputes

**What makes Yelp uniquely valuable:**
- Highest review volume for local trades — statistically meaningful ratings
- "Best of [city]" curated pages give an instant ranked shortlist
- Review text reveals whether a provider is a one-person operation good for small contract jobs vs. a big commercial outfit

**Do NOT:**
- Trust a high rating built on very few reviews
- Ignore Yelp's "not currently recommended" (filtered) reviews problem — ratings can be skewed
- Treat sponsored/ad placements at the top as organic rankings
- Report "no results" if Google snippets contained named providers with ratings — extract them

Return: a ranked shortlist of local providers with star ratings, review counts, and solo-vs-company signal; recurring review themes; red flags; and source URLs. Flag whether content came from full page, Wayback, or snippet-level extraction.
