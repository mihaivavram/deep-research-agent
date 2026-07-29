Search GummySearch (Reddit community intelligence) for: $ARGUMENTS

**Why this source exists:** reddit.com has been hard-blocked in this environment since 2026-07 (403 on `www.reddit.com`, `old.reddit.com`, `/about.json`, `/subreddits/search.json`, redlib mirrors, and the `r.jina.ai` reader proxy). GummySearch indexes ~130,000 active subreddits and its **public `/r/<subreddit>/` pages fetch clean without auth**. It is now the primary Reddit substitute for community/pain-point research.

## Strategy 1 — Direct subreddit profile fetch (the workhorse)

`curl -s "https://gummysearch.com/r/<SUBREDDIT>/"` — **case-sensitive**, must match Reddit's canonical casing (`r/msp` works, `r/MSP` does not; `r/PropertyManagement` works, `r/propertymanagement` does not). When a name returns nothing, retry with alternate casing and common variants before concluding the sub doesn't exist.

Strip tags and extract:
- **Member count** — first `[0-9.,]+[km]? members` match
- **Yearly growth** — `Yearly [+-] Nk members (N.N%)` — the single best "is this pain spreading" signal
- **Categorized post samples** — GummySearch clusters recent posts into `Pain &amp; Anger`, `Solution Requests`, `Advice Requests`, `Money Talk`, `Ideas`. Grep for `<CATEGORY> : &quot;` and take the following ~80 chars.
- **Popular Topics** — ranked topic list with post counts (e.g. r/msp: *"Looking For" 39 posts, "Struggling" 8, "Hate" 3, "Looking For A Tool" 3*)
- **Similar Subreddits** — sidebar list with member counts; free subreddit discovery, use it to expand a vertical's community map

**`Solution Requests` is the highest-value bucket for B2B idea validation** — it is literally people asking to be sold something. `Money Talk` reveals the buyer's unit economics, which sets your price ceiling.

## Strategy 2 — Batch sweep

For any ranking/landscape query, script a loop over 40–150 candidate subreddit names with `sleep 0.3` between requests (no rate limiting observed at that pace) and write TSV. Run it backgrounded while other sources execute — a 150-sub sweep takes ~4 minutes and produces the entire community map in one pass.

## What to extract that is unique to this source
Member counts **and trailing-year growth** together — Reddit's own UI shows only the former. Growth separates heating communities (r/legaltech +171.8%, r/InsuranceAgent +78.4%) from stagnant ones (r/AskHR +2.0%) and is the closest thing to a demand curve for a vertical's pain.

## Verification rules (do not skip)
- **Confirm subreddit identity before trusting it.** Real traps caught in production: `r/PrivatePractice` is a *Grey's Anatomy* fan sub, not clinicians; `r/ContractorUK` is UK IT contractors (IR35), not builders. Read the Pain/Topic samples — if they don't match the vertical, drop the sub.
- **Flag dead subs.** `r/freight` = 832 members, `r/govtech` = 629. Anything under ~5k is watch-only, not mineable.
- A `0 members` / no-match response means unresolvable — log it, don't silently omit it.

## Fallback
If gummysearch.com is unavailable: (1) `subredditstats.com/api/subreddit?name=<sub>` returns clean JSON but the data is stale (last crawl ~2023) — usable for existence checks only, never for current counts; (2) scoped `WebSearch "r/<sub> members"` for snippet-level counts; (3) trade associations and their newsletters, which for micro-verticals (funeral, self-storage, home inspection) are a *better* channel than Reddit anyway.

## What NOT to do
- Do not attempt `reddit.com` directly first — it is a settled failure, budget nothing for it.
- Do not report GummySearch post samples as if you read the Reddit threads. They are GummySearch's clustering, one layer removed — say so and score confidence accordingly.
- Do not treat absence of a subreddit as absence of a market. Reddit skews US/English/young/tech-forward; the least Reddit-visible verticals are frequently the least competitive ones.

## Return
A table of subreddit → members → yearly growth → best Pain/Solution-Request/Money-Talk sample, plus a flagged list of unresolvable or misidentified subs.
