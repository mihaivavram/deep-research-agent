Search the Wayback Machine for competitor history and positioning evolution on: $ARGUMENTS

Use this skill to understand how a company or product has changed its messaging, pricing, and positioning over time.

**Step 1 — Find the target URL:**
If a specific domain isn't provided, use WebSearch to identify the primary website for the company or product.

**Step 2 — Browse the archive:**
Use WebFetch on `https://web.archive.org/web/*/DOMAIN` (replace DOMAIN with the target URL, e.g. `competitor.com`) to see available snapshots by year.

**Step 3 — Fetch key snapshots:**
Pull snapshots at meaningful intervals — typically 1 year apart, plus the earliest available. Focus on high-signal pages:
- Homepage (messaging and headline positioning)
- Pricing page (tier structure, price points, what's included)
- Features/product page (what they were building)
- About/company page (team size, mission framing)

Use WebFetch on `https://web.archive.org/web/YYYYMMDD000000*/DOMAIN/PAGE` to get a snapshot from a specific year.

**What to look for:**
- How has the headline value proposition changed? (Pivots often show here first)
- When did pricing change — up, down, or restructured?
- What features were added or removed from the feature list?
- Did the target customer change? (ICP shifts show in copy)

Return a timeline of key changes with dates, the evolution of positioning/pricing, and Wayback Machine URLs for each snapshot.
