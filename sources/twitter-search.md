Search Twitter/X for real-time discourse, expert opinions, and breaking signals on: $ARGUMENTS

Twitter/X is the fastest-moving public discourse platform — uniquely valuable for breaking news, expert hot-takes, viral threads, and real-time sentiment from named industry figures. Since X tightened API access in 2023, the only reliable free path is **Google site-search + WebFetch on public tweet URLs**.

**Primary search strategy — Google site-search:**
Run at least 2 angled queries:
- `site:twitter.com $ARGUMENTS` — covers legacy URLs still indexed
- `site:x.com $ARGUMENTS` — covers post-rebrand URLs
- `site:twitter.com OR site:x.com "$ARGUMENTS" -filter:replies` — main tweets only, skip reply noise
- For threads specifically: `site:twitter.com $ARGUMENTS thread` or add `"1/"` to find numbered threads

**WebFetch individual tweet/profile URLs** for the top 4–6 results:
- Public tweets render server-side and are usually readable
- Look for: tweet text, author handle + verification status, follower count, like/repost/reply counts
- Threads: if the URL is the first tweet, fetch and look for the "Show this thread" continuation
- Profiles: bio, follower count, recent pinned tweet — useful for vetting source credibility

**What makes Twitter uniquely valuable:**
- **Speed**: breaking news, earnings reactions, FDA decisions hit Twitter minutes before news wires
- **Expert access**: domain experts (researchers, founders, analysts) post raw takes here that don't appear elsewhere
- **Aggregation**: viral threads often consolidate dozens of sources into one digestible post
- **Sentiment direction**: high-engagement posts reveal which framing is winning the narrative

**Fallback strategies (in order):**
1. **Nitter mirrors** — try `nitter.net/USERNAME/status/ID` or `nitter.privacydev.net/...` (most public instances are dead, but worth a shot)
2. **Google cache** — `cache:twitter.com/...` URLs sometimes return readable snapshots
3. **Wayback Machine** — `https://web.archive.org/web/*/twitter.com/USERNAME/status/ID` for older tweets
4. **Quote-tweet chains** — searching for the tweet ID in Google often surfaces quote-tweets that contain the original text

**Do NOT** rely on the X frontend directly — it requires login for almost everything beyond a few seed tweets. Skip protected accounts entirely. Skip tweets with under ~50 likes unless from a credentialed account. Never invent quotes or attribute words to a user without a fetched URL backing it.

Return: tweet text or paraphrase, author + credibility signal (followers, verification, role), engagement counts, the dated context, and direct twitter.com / x.com URLs.
