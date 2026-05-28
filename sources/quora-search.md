Search Quora for long-form Q&A and expert explanations on: $ARGUMENTS

Quora is a long-tail Q&A platform whose value is **expert answers from credentialed authors on niche questions**. Quality varies wildly — the best answers come from named experts with domain credentials (former Google engineer, practicing physician, retired NASA scientist), the worst come from anonymous SEO content. Filtering by author credentials is the entire game.

**Primary search strategy:**
Use Google site-search:
- `site:quora.com $ARGUMENTS` — general
- `site:quora.com "$ARGUMENTS"` — exact phrase
- `site:quora.com $ARGUMENTS "former" OR "ex-" OR "PhD" OR "years of experience"` — bias toward credentialed answers
- For comparison questions: `site:quora.com "$ARGUMENTS" vs OR difference between` — Quora hosts many high-quality explainer comparisons

**WebFetch the top 4–6 question pages** and extract:
- The question itself and any clarifying details
- For each highly-upvoted answer: the **author's stated credentials** (title, company, years of experience, education) — this is the credibility filter
- The answer's upvote count (Quora's signal of quality consensus)
- Specific claims, examples, or data referenced
- Any answer marked as "Most Viewed Writer" or with the author's profile link to a real-world identity
- Disagreements: Quora often has 2–3 answers with different angles on the same question; surface the divergence

**What makes Quora uniquely valuable:**
- **Credentialed long-form answers**: ex-FAANG engineers, doctors, lawyers, professors writing under their real names
- **Niche topics**: Quora often has the only good answer to oddly-specific questions ("Why does this medication interact with grapefruit?", "What was the actual reason Google killed Reader?")
- **Beginner-friendly explainers**: high-quality "explain like I'm new to this" content from experts
- **Historical context**: answers often go deeper into "why" than Wikipedia or news articles

**Fallback strategies:**
1. Quora has a soft paywall on some content — try opening the page in an incognito-style request (often returns full content)
2. If Quora returns "log in to read more", **Google snippets typically contain the first 200–400 words of the top answer** — paraphrase from the snippet and link the original
3. For technical topics, cross-reference with Stack Exchange (`site:stackexchange.com` or `site:stackoverflow.com`) — Quora and SE often answer the same questions with different framings
4. Wayback Machine for old Quora answers that may have been removed

**Do NOT** treat anonymous answers or low-upvote answers as authoritative — Quora's content farm problem is real. Skip answers with no author credentials visible. Never cite "Quora user said X" without a real author name or credential. Watch for paid promotional answers (rare but they exist).

Return: question summary, top credentialed answer summaries with **author credentials always cited**, points of disagreement between answers, upvote signal, and source Quora URLs.
