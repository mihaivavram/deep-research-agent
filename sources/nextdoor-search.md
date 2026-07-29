Search Nextdoor for hyperlocal neighbor recommendations on: $ARGUMENTS

Nextdoor is the highest-signal source for **hyperlocal, neighbor-to-neighbor recommendations of individual service providers** — handymen, electricians, plumbers, and other tradespeople who work as sole operators rather than big companies. Its unique value is real residents naming specific people they hired, tied to a named neighborhood. Nextdoor is heavily gated behind a login wall, so direct WebFetch usually fails — rely on site-search + snippet/archive paths.

**Primary search strategy — Google site-search (run 3-4 queries):**
- `site:nextdoor.com $ARGUMENTS` — broad sweep
- `site:nextdoor.com $ARGUMENTS recommendation OR recommend OR "anyone know"` — bias toward referral threads
- `site:nextdoor.com [CITY/NEIGHBORHOOD] $ARGUMENTS` — scope to the specific locality in the query
- `$ARGUMENTS nextdoor recommendations reddit` — catch discussion about how people use Nextdoor for this

**Fetching content — ordered fallback chain:**
1. **Google snippet extraction (primary path):** Nextdoor "recommendations" and "business" pages surface in Google with the provider name, star rating, number of neighborhood recommendations, and locality right in the snippet. Extract these systematically from every result — this is often the core signal without needing the full page.
2. **Wayback Machine:** WebFetch `https://web.archive.org/web/*/NEXTDOOR_URL` for public business/recommendation pages that were crawled.
3. **Direct WebFetch (attempt, expect login wall):** Try the public `nextdoor.com/pages/` business URL. Public business profile pages sometimes render rating + recommendation counts before the wall.

**What to extract:**
- Specific provider/person names that neighbors recommend (the whole point — capture individuals, not just companies)
- Number of neighborhood recommendations / "faves" and any star rating (Nextdoor's trust signal)
- The neighborhood/locality attached to the recommendation
- Whether the recommended provider is a solo operator/independent vs. an established company
- Recurring names that appear across multiple neighborhoods (strongest signal)
- Warnings/negative experiences neighbors flag

**What makes Nextdoor uniquely valuable:**
- Recommendations are geo-verified to real residents of a named neighborhood — the closest thing to a trusted word-of-mouth referral online
- Skews toward independent/small operators and "a guy I know" referrals rather than big franchises
- Captures the informal local market that never advertises

**Do NOT:**
- Rely on direct fetch — the login wall blocks most pages; lead with snippets
- Report a single recommendation as consensus — prioritize providers recommended across multiple threads/neighborhoods
- Treat Nextdoor business listings that are paid ads as organic neighbor recommendations
- Report "no results" if Google snippets named recommended providers — always extract those names

Return: specific recommended provider names with recommendation counts and neighborhoods, recurring cross-neighborhood picks, any warnings, and source URLs. Always flag whether content came from full page, Wayback, or snippet-level extraction.
