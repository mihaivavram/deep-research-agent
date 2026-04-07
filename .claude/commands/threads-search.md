Search Threads (Meta) for casual professional discourse and Instagram-adjacent commentary on: $ARGUMENTS

Threads is Meta's text-based social network, launched July 2023. Audience skews more toward creators, designers, marketers, and Instagram-native professionals than Twitter/X. Smaller corpus, more civil discourse, less breaking-news velocity. Public posts are crawlable without login.

**Primary search strategy:**
Use Google site-search:
- `site:threads.net $ARGUMENTS` — general
- `site:threads.net "$ARGUMENTS"` — exact phrase for quote attribution
- `site:threads.com $ARGUMENTS` — newer URL pattern (Threads added the .com domain)

**WebFetch individual post URLs** for the top 4–6 results:
- Public post URLs follow the pattern `threads.net/@USERNAME/post/SHORTCODE`
- Posts render server-side and are readable without login
- Extract: post text, author handle, follower count (if visible), like/reply count, any reply chain

**What makes Threads distinct from Twitter:**
- **Audience**: heavier in design, marketing, creator-economy, lifestyle commentary
- **Tone**: less combative, more long-form-friendly than X
- **Discoverability**: posts often surface through Instagram cross-promotion, so look for Instagram personalities on the same topic
- **Lower noise**: less spam, fewer bots, fewer hot-take wars — but also less raw signal velocity
- **Use case**: best for "what are creators / designers / brand marketers saying about X" — not for breaking news or hard analysis

**Fallback strategies:**
1. If Threads search returns thin results (Threads is still much smaller than X), pivot to `/twitter-search` for the same query — many Threads creators cross-post
2. Instagram comments on related posts often mirror Threads sentiment — `site:instagram.com $ARGUMENTS` as a tertiary signal
3. Wayback Machine on specific known Threads URLs for older posts

**Do NOT** treat Threads as a primary signal source for finance, breaking news, or hard tech topics — Twitter/X still dominates those. Skip posts with no engagement (Threads' early-stage corpus has many low-signal posts). Don't quote threads that 404 — the platform reorganizes URLs occasionally.

Return: post text or paraphrase, author handle + credibility signal, engagement counts, dated context, and direct threads.net URLs.
