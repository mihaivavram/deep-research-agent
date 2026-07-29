Search Amazon reviews for: $ARGUMENTS

For B2C physical products, review verbatims are primary research. **Amazon product pages return
HTML head only in this environment** — no price, rating, or review body. So Amazon is useful for
identifying the competitive set, and the actual verbatim analysis must come from elsewhere.

## Access ladder

**What works:**
1. **Google snippet extraction for Amazon** — search result snippets reliably carry product name,
   star rating, and review count. Use this to build the candidate product list and the ratings
   table. Flag as snippet-sourced.
2. **Reddit via pullpush** (`/reddit-search`) — **the strongest substitute for real verbatims.**
   `api.pullpush.io/reddit/search/comment/?q="<product>"&score=>10` returns unpaid, unsolicited
   product verdicts with community scores. Prefer this over any affiliate listicle.
3. **Manufacturer and retailer sites other than Amazon** — many DTC and big-box product pages
   (and their review widgets) fetch cleanly. Try the brand's own site, and non-Amazon retailers.
4. **Dedicated review outlets** — Wirecutter, RTINGS, Consumer Reports summaries, and specialist
   sites for the category. These fetch inconsistently but carry methodology, which Amazon reviews
   never do.

**Known limitation:** `amazon.com` product and review pages — head only, no body. Do not budget
multiple fetches hoping one renders.

## Query strategy

1. `site:amazon.com $ARGUMENTS reviews` — snippet harvest for the product set + ratings
2. `"<specific product>" review problems OR complaints OR "stopped working"` — surfaces the
   failure modes that 5-star averages hide
3. pullpush comment query on each shortlisted product name
4. `$ARGUMENTS rtings OR wirecutter OR "consumer reports"` — methodology-backed testing

## What to extract

- Overall star rating and total review count (satisfaction + market-size signal)
- Star distribution shape — **a pile of 3-star reviews usually means "good enough but missing X,"**
  which is the most actionable finding in product research
- Recurring complaints from critical reviews — unmet needs and positioning gaps
- Recent vs. legacy sentiment (a product's reputation often lags a quality change, in both
  directions — note manufacturing/revision changes)
- Verbatim customer language — the phrasing buyers use is directly reusable
- Competitive set from "also viewed"/"bought together" where visible in snippets
- Unanswered Q&A items — friction and feature gaps

## Do NOT

- Present Amazon findings as full-page-sourced when they came from snippets
- Trust the star average alone — review solicitation, incentivized reviews, and variant-merging
  (reviews from a different model pooled onto one listing) all inflate it. **Check whether reviews
  actually describe the product you are researching.**
- Use affiliate-heavy "best of" listicles as sentiment evidence — flag them as commercial content
- Ignore that Amazon review corpora contain paid and fake reviews; corroborate any strong claim
  against Reddit or a methodology-driven outlet before calling it consensus

Return: product names with ratings and review counts, complaint and praise themes, competitor
alternatives, and URLs. State the extraction level per source, and flag any commercial/affiliate
content used.
