Search Reddit for: $ARGUMENTS

Reddit is the highest-signal community platform for unfiltered opinions, product reviews, and real-world experience reports. Reddit aggressively blocks direct WebFetch from most crawlers, so **do not rely on fetching reddit.com or old.reddit.com directly** — use the fallback chain below.

**Primary strategy — Google site-search with domain-specific subreddits:**
Run 2–3 queries scoped to relevant subreddits:
- `site:reddit.com $ARGUMENTS` — broad sweep
- `site:reddit.com/r/SUBREDDIT $ARGUMENTS` — scoped to the most relevant subreddit for this topic (e.g. r/BuyItForLife for product durability, r/personalfinance for money questions, r/programming for dev tools, r/investing or r/wallstreetbets for stocks, r/coffee for coffee, r/HomeImprovement for home topics)
- `site:reddit.com $ARGUMENTS 2025 OR 2026` — recency bias

**Fetching content — ordered fallback chain:**
1. **Google cached versions (best path):** For each Reddit URL found in search results, try `webcache.googleusercontent.com/search?q=cache:REDDIT_URL` via WebFetch. Google's cache often contains the full thread including top comments.
2. **Reddit JSON API:** Append `.json` to any reddit thread URL (e.g. `reddit.com/r/SUBREDDIT/comments/ID/SLUG.json`) and WebFetch that. Returns structured JSON with post body, all comments, scores. This sometimes works when HTML pages are blocked.
3. **Archive services:** Try `web.archive.org/web/*/REDDIT_URL` for Wayback Machine snapshots of popular threads.
4. **Google snippet extraction (last resort):** If all fetch paths fail, extract content systematically from Google search result snippets — they often contain the post title, first 1-2 sentences of the body, and top comment previews. Flag these explicitly as "snippet-sourced" in your output.

**What to extract:**
- Post title, body text, and subreddit
- Top 3-5 comments by score (these represent community consensus)
- Upvote count and comment volume (engagement = signal quality)
- Minority/contrarian views that have positive scores (not just the top comment)
- Which subreddits are most active on this topic
- Recurring recommendations, complaints, or warnings across threads

**Do NOT:**
- Attempt fetching `old.reddit.com` directly — it is consistently blocked
- Treat a single heavily-upvoted comment as consensus — look for patterns across multiple threads
- Ignore threads with <10 upvotes unless the topic is very niche
- Report "no results" if Google snippets contained relevant content — always extract what you can

Return: key perspectives, community consensus, minority views, specific product/tool recommendations with context, and source URLs. Always note whether content came from full-thread access or snippet-level extraction.
