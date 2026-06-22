Search Quora for long-form Q&A and expert explanations on: $ARGUMENTS

Quora is a long-tail Q&A platform whose value is **expert answers from credentialed authors on niche questions**. Quality varies wildly — the best answers come from named experts with domain credentials (former Google engineer, practicing physician, retired NASA scientist), the worst come from anonymous SEO content. Filtering by author credentials is the entire game.

Quora aggressively blocks direct WebFetch (returns 403). **Use archive and snippet paths as primary access methods.**

**Primary search strategy — Google site-search:**
- `site:quora.com $ARGUMENTS` — general
- `site:quora.com "$ARGUMENTS"` — exact phrase
- `site:quora.com $ARGUMENTS "former" OR "ex-" OR "PhD" OR "years of experience"` — bias toward credentialed answers
- For comparison questions: `site:quora.com "$ARGUMENTS" vs OR difference between` — Quora hosts many high-quality explainer comparisons

**Fetching content — ordered fallback chain:**
1. **Wayback Machine (best path for full content):** For each Quora URL found via Google, WebFetch `https://web.archive.org/web/*/QUORA_URL`. Quora's older content is well-archived on Wayback and returns full answers with author credentials.
2. **archive.ph:** Try `https://archive.ph/newest/QUORA_URL` — often has recent snapshots.
3. **Direct WebFetch (attempt but expect failure):** Try fetching the Quora URL directly. Occasionally works, especially for older questions. If it returns 403 or a login wall, move to the next fallback.
4. **Google snippet extraction (always works):** Google snippets from Quora searches typically contain:
   - The question title
   - Author name and credential line (e.g. "John Smith, Former VP Engineering at Google")
   - First 200-400 words of the top answer
   Systematically extract all of these fields from every search result snippet, even when full-page access fails. This is often sufficient for the key insight.

**What to extract (from full pages or snippets):**
- The question itself and any clarifying details
- For each highly-upvoted answer: the **author's stated credentials** (title, company, years of experience, education) — this is the credibility filter
- The answer's upvote count (Quora's signal of quality consensus)
- Specific claims, examples, or data referenced
- Any answer marked as "Most Viewed Writer" or with the author's profile link to a real-world identity
- Disagreements: Quora often has 2–3 answers with different angles on the same question; surface the divergence

**What makes Quora uniquely valuable:**
- **Credentialed long-form answers**: ex-FAANG engineers, doctors, lawyers, professors writing under their real names
- **Niche topics**: Quora often has the only good answer to oddly-specific questions
- **Beginner-friendly explainers**: high-quality "explain like I'm new to this" content from experts
- **Historical context**: answers often go deeper into "why" than Wikipedia or news articles

**Cross-reference source (when Quora is fully blocked):**
For technical topics, search Stack Exchange as an alternative: `site:stackexchange.com OR site:stackoverflow.com $ARGUMENTS` — provides similar Q&A content without the login wall.

**Do NOT:**
- Treat anonymous answers or low-upvote answers as authoritative — Quora's content farm problem is real
- Skip answers with no author credentials visible
- Cite "Quora user said X" without a real author name or credential
- Watch for paid promotional answers (rare but they exist)
- Report "no results" if Google snippets contained relevant credentialed answers — extract and use them

Return: question summary, top credentialed answer summaries with **author credentials always cited**, points of disagreement between answers, upvote signal, and source URLs. Flag whether content came from full-page access, Wayback archive, or snippet-level extraction.
