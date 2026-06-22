Search Hacker News for: $ARGUMENTS

Hacker News is a high-signal source for developer culture, startup dynamics, tech industry analysis, and practitioner-level technical commentary. The comments are often more valuable than the submitted articles — HN's community includes experienced engineers, founders, VCs, and researchers who provide substantive, opinionated analysis.

**Primary strategy — Algolia API (most reliable, no rate limits):**
WebFetch `https://hn.algolia.com/api/v1/search?query=QUERY&tags=story&hitsPerPage=10` — returns JSON with story titles, URLs, points, comment counts, and story IDs. This is the most reliable path and avoids the 429 rate limits that plague direct `news.ycombinator.com` fetches.

Run multiple Algolia queries for coverage:
- `query=QUERY&tags=story` — all stories mentioning the topic
- `query=QUERY&tags=show_hn` — Show HN posts (projects and launches)
- `query=QUERY&tags=ask_hn` — Ask HN posts (community questions and advice)
- `query=QUERY&numericFilters=created_at_i>UNIX_TIMESTAMP` — time-scoped (use a timestamp from 6 months ago for recency)

**Fetching comments — ordered fallback chain:**
1. **Algolia item API (best path):** For high-comment stories, WebFetch `https://hn.algolia.com/api/v1/items/STORY_ID` — returns the full comment tree as JSON, including author, text, points, and nesting. No rate limits.
2. **Direct HN page:** WebFetch `https://news.ycombinator.com/item?id=STORY_ID` — works sometimes but returns 429 when rate-limited. Only attempt if Algolia item API is insufficient.
3. **Google cached version:** WebSearch for `cache:news.ycombinator.com/item?id=STORY_ID` as fallback if both above fail.

**What to extract:**
- Story title, submitted URL, point count, and comment count
- Top 3-5 comments by points (these represent the community's most valued perspectives)
- Contrarian comments with positive points (HN values well-argued dissent)
- Comments from users with visible expertise (mentions of "I work at X", "I built Y", "10 years in Z")
- Whether the discussion is primarily positive, negative, or divided on the topic
- "Ask HN" threads for the topic — these contain direct experience reports and recommendations

**What makes HN uniquely valuable:**
- **Technical depth**: commenters frequently provide implementation details, architecture critiques, and performance data
- **Practitioner perspectives**: "I've been running this in production for 2 years" type reports
- **Contrarian takes**: HN's culture rewards well-argued disagreement with conventional wisdom
- **Startup/product signal**: Show HN launches + community reaction = early product-market-fit signal

**Do NOT:**
- Fetch `news.ycombinator.com` pages without trying Algolia first — HN rate-limits aggressively (429)
- Treat high-point comments as objective truth — HN has known biases (anti-enterprise, pro-open-source, skeptical of hype)
- Ignore low-point but substantive comments — HN's voting is noisy on controversial topics
- Conflate the linked article's content with HN's discussion — they often diverge significantly

Return: story titles with point/comment counts, key perspectives from top comments with author context, areas of consensus vs. debate, and HN URLs. Note whether comments were fetched via Algolia API or snippet-level.
