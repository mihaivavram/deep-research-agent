Search software review sites for: $ARGUMENTS

Software review sites carry verbatim buyer complaints — the highest-value signal for positioning
gaps. **Most of them are hard-blocked.** Capterra is the only one that reliably returns full review
text, so this skill is really "search Capterra, and use snippets for the rest."

## Access ladder

**Verified working:**
1. **Capterra — the only reliable full fetch.** Returns verbatim quotes with reviewer first name,
   role, industry, company size, and date. That metadata is what makes the quotes usable as
   evidence rather than anecdote.
   - **Get the product ID correctly first.** Guessed `/p/<id>/<Name>/reviews/` paths have 404'd
     repeatedly. Instead fetch a `capterra.com/compare/<id1>-<id2>/` URL — comparison pages expose
     the real numeric product IDs, which you then use to build a working reviews URL.
   - Find compare URLs via WebSearch: `capterra compare <product A> <product B>`.
2. **GetApp** — fetches, but returns ratings only, no verbatim text. Use for the numbers.
3. **Google snippet extraction** for G2/TrustRadius/Trustpilot content. Snippets frequently carry
   the star rating, review count, and the first line of a top review. Flag as snippet-sourced.

**Dead paths — do NOT budget fetches:**
- `g2.com` — consistent 403
- `trustradius.com` — consistent 403
- `trustpilot.com` — consistent 403
- `gartner.com` Peer Insights — unreachable
- `softwareadvice.com` — 404 on review paths (downgraded after failing)

## Query strategy

1. `site:capterra.com $ARGUMENTS reviews` — find the product's Capterra presence
2. `capterra compare $ARGUMENTS alternatives` — surface `/compare/` URLs that expose product IDs
3. `site:g2.com $ARGUMENTS` — expect no fetch; harvest the snippet for rating + review count
4. `$ARGUMENTS reviews "company size" OR "verified reviewer"` — unscoped, catches syndicated
   review content on sites that *do* fetch

## What to extract

- Overall rating and review count (scale signal — a 4.8 from 12 reviews is not a 4.8 from 900)
- Star distribution — the *shape* of satisfaction; % of 1-star matters more than the mean
- Most common praise themes (what the product genuinely does well)
- **Most common complaint themes — the highest-value output.** These are the positioning gaps.
- Reviewer role, industry, and company size attached to each verbatim, so findings can be
  segmented by buyer type
- Competitor alternatives named inside reviews (real consideration sets, not analyst groupings)
- Comparison-page feature matrices for competitive positioning

## Do NOT

- Spend fetches on G2, TrustRadius, Trustpilot, or Gartner — go straight to snippets for those
- Guess Capterra `/p/<id>/` URLs — derive the ID from a `/compare/` page first
- Present a verbatim quote without its reviewer role/company-size context
- Treat vendor-supplied case studies or review-site "sponsored" placements as organic sentiment —
  review sites monetize placement; flag any result that appears promoted
- Average ratings across sites with different review-solicitation practices

Return: ratings with review counts, complaint and praise themes, buyer segments, competitive
mentions, and source URLs. State for each site whether you got full review text or snippets only.
