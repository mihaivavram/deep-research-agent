Search YouTube channel statistics platforms for: $ARGUMENTS

Social Blade and its competitors are the standard third-party source for **channel-level growth data** — subscriber counts, view totals, upload cadence, 30-day deltas, and estimated earnings. Use this source whenever a query needs to benchmark creators, verify claimed subscriber numbers, or measure growth trajectories rather than opinions.

**Primary strategy — WebSearch with `allowed_domains`, not direct fetch:**
Social Blade renders its stat tables client-side and rate-limits aggressively. Use the domain-scoped search trick that works for G2:

- `WebSearch(query: "<channel name> subscribers views", allowed_domains: ["socialblade.com"])`
- `WebSearch(query: "<channel name> YouTube stats subscriber count", allowed_domains: ["viewstats.com"])`
- `WebSearch(query: "<channel name> channel analytics", allowed_domains: ["hypeauditor.com", "thoughtleaders.io", "noxinfluencer.com"])`

Counts frequently come back in the search snippet even when the page itself is unfetchable.

**Fetchable substitutes (try in this order when a number must be exact):**
1. `https://app.thoughtleaders.io/youtube/<slug>` — renders server-side; gives subscribers, avg views, engagement rate, sponsorship history
2. `https://www.youtube.com/@<handle>/about` — first-party, but often footer-only (see youtube-search health notes)
3. `https://outlierkit.com/channel/<slug>` — channel teardowns with growth analysis
4. `https://raresocial.com/youtube-creators/channel/<slug>` — top-performing videos + title pattern analysis
5. Wikipedia, for channels large enough to have an article

**What to extract:**
- Subscriber count **with the date it was measured** (counts age fast — always timestamp them)
- Total views and video count → compute views-per-video (the single most useful comparative metric)
- Upload cadence (videos per week/month)
- 30-day subscriber and view deltas (growth rate, not just size)
- Views-per-subscriber ratio (a reach-quality signal; Paddy Galloway benchmarks against it)
- Top-performing videos and their titles (outlier analysis input)
- Channel start date → derive months-to-milestone trajectories

**Do NOT:**
- Treat third-party estimated earnings as reliable — the ranges are formulaic and ignore sponsorships, which dominate revenue in B2B niches
- Report a subscriber count without a date attached
- Compare raw subscriber counts across channels of different ages — normalize to views-per-video or months-to-100K
- Fetch socialblade.com directly and count on it; budget for the search-snippet path

Return: a benchmark table of channels with subscribers (dated), views-per-video, cadence, and growth rate, flagging which figures are snippet-sourced vs. fetched.
