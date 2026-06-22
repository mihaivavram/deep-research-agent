Search Twitter/X for real-time discourse, expert opinions, and breaking signals on: $ARGUMENTS

Twitter/X is the fastest-moving public discourse platform — uniquely valuable for breaking news, expert hot-takes, viral threads, and real-time sentiment from named industry figures. Since X tightened API access in 2023, direct tweet fetching is unreliable. **Use syndicated content and thread-reading services as primary paths.**

**Primary strategy 1 — Thread-reading services (best for threads):**
- `site:threadreaderapp.com $ARGUMENTS` — Thread Reader App unrolls Twitter threads into clean, fetchable web pages. This is the most reliable path for thread content.
- WebFetch the top 2-3 Thread Reader results for full thread text.

**Primary strategy 2 — Syndicated tweet embeds:**
Many tweets are embedded in news articles, blog posts, and newsletters. Search for:
- `"twitter.com" OR "x.com" $ARGUMENTS` — finds pages that embed or quote tweets
- `"x.com/*/status" $ARGUMENTS` — targets pages referencing specific tweet URLs
- The embedding page often contains the full tweet text rendered as a quote.

**Primary strategy 3 — Google site-search:**
- `site:twitter.com $ARGUMENTS` — covers legacy URLs still indexed
- `site:x.com $ARGUMENTS` — covers post-rebrand URLs
- `site:twitter.com OR site:x.com "$ARGUMENTS" -filter:replies` — main tweets only, skip reply noise
- For threads: `site:twitter.com $ARGUMENTS thread` or add `"1/"` to find numbered threads

**WebFetch individual tweet/profile URLs** for the top 4–6 results:
- Public tweets sometimes render server-side and are readable
- Look for: tweet text, author handle + verification status, follower count, like/repost/reply counts
- Threads: if the URL is the first tweet, look for the "Show this thread" continuation
- Profiles: bio, follower count, recent pinned tweet — useful for vetting source credibility

**What makes Twitter uniquely valuable:**
- **Speed**: breaking news, earnings reactions, FDA decisions hit Twitter minutes before news wires
- **Expert access**: domain experts (researchers, founders, analysts) post raw takes here that don't appear elsewhere
- **Aggregation**: viral threads often consolidate dozens of sources into one digestible post
- **Sentiment direction**: high-engagement posts reveal which framing is winning the narrative

**Fallback strategies (in order):**
1. **archive.ph** — `https://archive.ph/newest/TWEET_URL` often has readable snapshots
2. **Wayback Machine** — `https://web.archive.org/web/*/twitter.com/USERNAME/status/ID` for older tweets
3. **Google cache** — `cache:twitter.com/...` URLs sometimes return readable snapshots
4. **Quote-tweet chains** — searching for the tweet ID in Google often surfaces quote-tweets that contain the original text
5. **Google snippet extraction** — when all fetch paths fail, extract tweet text from Google search snippets and flag as "snippet-level only"

**Do NOT:**
- Rely on the X frontend directly — it requires login for almost everything
- Skip protected accounts entirely
- Skip tweets with under ~50 likes unless from a credentialed account
- Invent quotes or attribute words to a user without a fetched URL backing it
- Report "no results" — if Google snippets or syndicated embeds contained tweet content, report what you found with appropriate sourcing caveats

Return: tweet text or paraphrase, author + credibility signal (followers, verification, role), engagement counts, the dated context, and direct URLs. Note whether content came from Thread Reader, syndicated embeds, direct fetch, or snippet extraction.
