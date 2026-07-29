Search for funding and company intelligence on: $ARGUMENTS

Goal: funding totals, investors, headcount, and strategic direction. **Crunchbase itself has never
fetched successfully in this environment** (0 direct fetches across 3 logged runs) — all usable
funding data has come from press-release wires and trade press. Structure the run accordingly.

## Access ladder

**Verified working — go here first:**
1. **Press-release wires** — `globenewswire.com`, `businesswire.com`, `prnewswire.com`,
   `accesswire`/Morningstar. All fetch cleanly and are date-stamped. **This is the reliable path to
   funding amounts, round names, investor lists, and vendor adoption numbers.** Search
   `<company> funding site:globenewswire.com` and `<company> Series site:businesswire.com`.
2. **Trade press for the vertical** — fetches far more reliably than general tech press, and covers
   rounds that TechCrunch ignores.
3. **TechCrunch / VentureBeat / Fortune / Forbes** — Fortune and Forbes fetch cleanly.
   Note **GeekWire and CNBC return 403.**
4. **SEC EDGAR** (`/sec-search`) — for any company that has filed, Form D covers private raises and
   is primary-source. Prefer this over any secondary funding report when it exists.
5. **Google snippet extraction** for Crunchbase and CB Insights. Their pages surface in results and
   carry funding totals in the snippet even though the page will not fetch. Flag as snippet-sourced.

**Dead / unreliable — do not budget full fetches:**
- `crunchbase.com` — never fetched successfully; snippets only
- `cbinsights.com` — surfaces in results, does not fetch
- `pitchbook.com` — paywalled

## Query strategy

1. `<company> funding round site:globenewswire.com OR site:businesswire.com`
2. `site:crunchbase.com $ARGUMENTS` — for the snippet only (total raised, founded year)
3. `"$ARGUMENTS" raised Series A OR Series B OR seed` — unscoped, catches trade press
4. `site:linkedin.com/jobs $ARGUMENTS` — hiring as a strategy signal. LinkedIn will not fetch, but
   **snippets reliably carry company follower counts and role titles** — heavy ML hiring reveals
   product direction before any press release.

## What to extract

- Total funding raised; each round's series, amount, and date
- Named investors — **repeat investors across competitors signal category conviction**, which is
  more informative than any single round size
- Founding year and headcount range (and direction of change)
- Acquisitions and acqui-hires
- Hiring themes as a leading indicator of strategy

## Do NOT

- Spend fetches on crunchbase.com, cbinsights.com, or pitchbook.com
- Report a funding figure from a single secondary source without flagging it single-source —
  reported round sizes are frequently rounded up or restated
- Treat a company's own press release as neutral on valuation or "market leader" claims
- Confuse total raised with valuation, or announced with closed

Return: companies found, funding totals and rounds with dates, named investors, headcount and
hiring signals, strategic inferences, and source URLs. Mark which figures are primary
(SEC/press release) vs. snippet-sourced.
