Search Reddit for: $ARGUMENTS

Reddit is the highest-signal community platform for unfiltered opinions, product reviews, and
real-world experience reports. **reddit.com itself is unreachable in this environment** — the
client refuses it and `WebSearch allowed_domains:[reddit.com]` returns API 400. Use the pullpush
API, which is verified working and returns full post and comment bodies.

## Access ladder

**Verified working (use this first — it is the whole strategy):**
`api.pullpush.io` — the public Pushshift successor. Returns real JSON with full bodies, scores,
subreddits, and timestamps. No auth required.

- **Submissions:** `https://api.pullpush.io/reddit/search/submission/?q=<query>&size=25&sort=desc`
- **Comments:** `https://api.pullpush.io/reddit/search/comment/?q=<query>&score=>10&size=50&sort=desc`

Useful parameters (all verified):
- `subreddit=BuyItForLife` — scope to one subreddit. **Highest-value parameter** — use it.
- `score=>25` — filter to comments the community actually upvoted. Use `>10` minimum, `>25` to
  find consensus, `>100` for strongly-endorsed claims.
- `after=`/`before=` — epoch seconds, for recency windows.
- `sort=desc` with `sort_type=score` — rank by score rather than date.

**Dead paths — do NOT attempt, they cost fetches and always fail:**
- `reddit.com`, `www.reddit.com`, `old.reddit.com` — refused at client level
- Appending `.json` to a reddit URL — refused at client level
- `WebSearch` with `allowed_domains:["reddit.com"]` — returns API 400
- `site:reddit.com` in a normal WebSearch — returns zero Reddit URLs
- `web.archive.org` / `archive.ph` — both refused at client level in this environment
- `r.jina.ai` proxy — 403, blocked by network security
- `frontpagemetrics.com` (404), subredditstats (defunct)

**Fallback if pullpush is down:** Google snippet extraction for Reddit content that appears in
general web results, flagged explicitly as snippet-sourced. Then substitute
`teamblind.com` (verified employees, fetches cleanly) or niche industry forums.

## Query strategy — run at least 3 variants

pullpush relevance matching is **loose**: `q=standing desk` matched comments containing "standing"
in unrelated contexts (standing on a desk, standing upright). Compensate:

1. **Quote multi-word phrases:** `q="standing desk"` rather than `q=standing desk`.
2. **Scope by subreddit** for the topic's home community — this is the strongest precision lever.
   Pick from context: r/BuyItForLife (durability), r/personalfinance, r/investing,
   r/wallstreetbets, r/programming, r/ExperiencedDevs, r/coffee, r/HomeImprovement, r/SaaS,
   r/Entrepreneur.
3. **Search comments, not just submissions.** Comments carry the actual verdicts; submissions
   mostly carry questions. Run at least one `score=>25` comment query.
4. **Discard non-matching results manually** — do not treat every returned row as relevant. The
   API returns loose matches; you must filter.

## What to extract

- Post title, body, subreddit, and score
- High-scoring comments (these represent community consensus, not the OP's guess)
- Upvote count and comment volume as signal-strength indicators
- Minority/contrarian views that still carry positive scores
- Which subreddits are most active on this topic
- Recurring recommendations, complaints, and warnings repeated across threads
- Reconstruct thread URLs as `reddit.com/comments/<link_id without t3_ prefix>` for citation —
  cite them even though you fetched via API, since that is where a reader can verify

## Do NOT

- Spend fetches on any dead path listed above
- Pass `fields=` expecting it to work — it is ignored, full records are always returned
- Treat one high-scoring comment as consensus — look for patterns across threads
- Report "no results" without having tried a quoted phrase, a subreddit scope, AND a comment query
- Silently degrade to snippets while pullpush is available

Return: key perspectives, community consensus, minority views, specific recommendations with
context, comment scores, and reconstructed thread URLs. State whether content came from the
pullpush API (full bodies) or snippet extraction.
