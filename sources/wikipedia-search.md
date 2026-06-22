Search Wikipedia for: $ARGUMENTS

Wikipedia provides structured, well-sourced overviews that are valuable for definitions, entity disambiguation, historical context, and discovering primary sources to follow. It is a starting point, not an endpoint — the real value is often in Wikipedia's references section.

**Primary strategy — Wikipedia API (clean text, no HTML parsing):**
WebFetch `https://en.wikipedia.org/w/api.php?action=query&titles=TOPIC&prop=extracts&explaintext=true&format=json` (URL-encode the topic). Returns clean plaintext of the article without HTML markup.

**Secondary strategy — Google site-search:**
- `site:wikipedia.org $ARGUMENTS` — finds the most relevant article(s) when the exact title is unknown
- `site:wikipedia.org $ARGUMENTS` with different phrasings if the first query misses (Wikipedia titles can be non-obvious)

**For the top 1–3 articles, extract:**
- **Lead section**: the opening paragraphs provide the most concise, well-edited overview available anywhere
- **Key data**: dates, figures, definitions, categorizations, taxonomy
- **"See also" section**: links to related Wikipedia articles that reveal adjacent topics worth exploring
- **"References" section (highest value)**: Wikipedia's references are curated primary sources — academic papers, government reports, news articles. Fetch the 2-3 most relevant references directly for primary-source data that the Wikipedia article summarizes.
- **Infobox data**: if present, contains structured facts (founding date, headquarters, revenue, population, etc.)
- **Categories**: listed at the bottom, useful for understanding how the topic is classified

**When to go deeper:**
- If the Wikipedia article references a specific study, dataset, or government report — fetch that primary source directly via WebFetch. Wikipedia's synthesis is good, but primary sources are better.
- If the article has a "Controversy" or "Criticism" section — extract this for balanced coverage.
- If the article is a stub or very short — note this as a signal that the topic may be too niche or too new for Wikipedia coverage, and rely more on other sources.

**Talk page for contested topics:**
For controversial or rapidly-evolving topics, WebFetch `https://en.wikipedia.org/wiki/Talk:TOPIC` — the Talk page reveals: active disputes about neutrality, recent significant edits, and which claims editors consider unsupported. This is a unique signal for understanding where expert consensus is uncertain.

**What makes Wikipedia uniquely valuable:**
- **Neutral point of view policy**: deliberately attempts balanced coverage
- **Curated references**: the reference list is a research bibliography maintained by hundreds of editors
- **Structured overviews**: infoboxes, categories, and "See also" provide structured data that search engines don't
- **Historical depth**: most articles cover origin, evolution, and current state

**Do NOT:**
- Use Wikipedia as a primary source for contested claims — follow its references to the primary source instead
- Ignore article quality signals: Featured Articles (star icon) and Good Articles (green circle) have passed rigorous review; stubs and unreferenced articles are much less reliable
- Copy Wikipedia's exact phrasing without attribution — paraphrase and cite
- Assume Wikipedia is current for fast-moving topics — check the "last edited" date

Return: key facts, definitions, structured data from infoboxes, notable references worth following, related topics from "See also", and Wikipedia URLs. Flag whether the article is Featured/Good quality or a stub.
