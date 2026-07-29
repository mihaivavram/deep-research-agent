Search the web for: $ARGUMENTS

General web search is the broadest and most reliable source. It serves as the foundation for every research query — catching authoritative content that specialized sources miss.

**Query strategy — run at least 4 WebSearch queries covering different angles:**
1. `$ARGUMENTS` — broad overview to surface the most authoritative results
2. `$ARGUMENTS expert OR guide OR analysis` — bias toward substantive expert content
3. `$ARGUMENTS 2025 OR 2026` — recency filter for time-sensitive topics
4. `$ARGUMENTS pros cons OR comparison OR alternatives` — surface evaluative content and tradeoffs
5. (Optional) `$ARGUMENTS site:news.ycombinator.com` — catch community discussion. **Do not add
   `site:reddit.com`** — it returns zero Reddit URLs in this environment; use `/reddit-search`
   (pullpush API) instead.

**High-yield source classes discovered in past runs — reach for these deliberately:**
- **Trade associations, industry bodies, and professional societies** fetch cleanly and are the best
  path for B2B niche mapping (audiences, venues, named executive contacts).
- **Conference agenda pages** — session titles reveal exactly which job roles own which problem.
- **Independent vendor user groups** — candid practitioner discussion that is not on social media.
- **Press-release wires** (`globenewswire.com`, `businesswire.com`, `prnewswire.com`) — date-stamped
  and reliable for adoption numbers and corporate change.

**WebFetch the top 4–6 most relevant results.** Prioritize in this order:
1. **Official sources**: company websites, government sites (.gov), academic institutions (.edu), official documentation
2. **Established publications**: Reuters, AP, BBC, The Verge, Ars Technica, TechCrunch, Wired, MIT Technology Review
3. **Subject-matter expert blogs and reports**: named authors with visible credentials or domain authority
4. **Well-researched aggregator content**: Wirecutter, Consumer Reports, NerdWallet — these add genuine testing/analysis

**When a page returns 403, 451, or paywall:**
1. **Find an alternate publisher of the same underlying data** — the highest-yield move by a wide
   margin. Wire services and trade press often carry the same figures and do fetch.
2. Try Google cache: WebSearch for `cache:BLOCKED_URL`
3. Extract maximum signal from the Google snippet, flagged as snippet-sourced, and move on

**Do not attempt `web.archive.org` or `archive.ph`** — both are refused at the client level in this
environment. They are not available as fallbacks.

**Known-403 publishers:** GeekWire, CNBC, G2, TrustRadius, Trustpilot. Go straight to an alternate
publisher rather than retrying these.

**What to extract from each page:**
- Publication date and author (for freshness and credibility)
- Key data points, statistics, and specific claims (not just general summaries)
- Named sources cited within the article (for citation-chain awareness)
- Methodology or evidence basis when present

**Do NOT:**
- Rely on search snippets alone — always attempt to fetch the full page
- Trust content farms, AI-generated aggregator pages, or thin SEO listicles (recognize by: no author, no dates, generic language, keyword-stuffed headers)

  **Business, startup-idea, and "best X" queries return a very high density of AI-generated SEO
  content.** On these topics, expect to discard a large share of results and budget for aggressive
  triage. Two content-farm pages agreeing is not corroboration — they are often derived from the
  same source, or from each other.
- Count multiple pages that cite the same underlying source as independent corroboration
- Prioritize .com over .gov/.edu/.org for factual or regulatory questions

Return a synthesized list of findings with source URLs, publication dates, and author/publication names where available.
