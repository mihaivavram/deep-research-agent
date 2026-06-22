Search arXiv for academic papers on: $ARGUMENTS

arXiv is the primary preprint server for scientific research — uniquely valuable for ML/AI, physics, mathematics, computer science, and quantitative fields. Papers here represent cutting-edge research, often months before journal publication.

**Primary strategy — arXiv API (structured results):**
WebFetch `https://export.arxiv.org/api/query?search_query=all:QUERY&sortBy=lastUpdatedDate&sortOrder=descending&max_results=10` (URL-encode the query terms, use `+` for spaces). This returns structured XML with titles, authors, abstracts, categories, and submission dates.

**Secondary strategy — arXiv web search:**
WebFetch `https://arxiv.org/search/?searchtype=all&query=QUERY&order=-announced_date_first` for the web search interface. Provides titles, authors, and abstract previews.

**Tertiary strategy — Google Scholar site-search:**
WebSearch `site:arxiv.org $ARGUMENTS` — Google often surfaces the most-cited arXiv papers first, providing an implicit quality ranking that arXiv's own search lacks.

**For the top 3–5 results, fetch the abstract page** (`https://arxiv.org/abs/PAPER_ID`) and extract:
- Paper title and full author list
- Abstract (the most information-dense summary available)
- Submission date and latest revision date
- arXiv category (e.g., cs.AI, cs.LG, stat.ML)
- Methodology type: empirical study, theoretical proof, survey/review, benchmark, position paper
- Key results: specific numbers (accuracy, performance gains, sample sizes) — not just qualitative claims
- Stated limitations and future work directions

**Citation count proxy (optional but valuable):**
For key papers, WebFetch `https://api.semanticscholar.org/graph/v1/paper/arXiv:PAPER_ID?fields=citationCount,influentialCitationCount,year` to get citation counts. High citations + recent date = high-impact work.

**What makes arXiv uniquely valuable:**
- **Speed**: research appears here months before journal publication
- **Depth**: full methodologies and results, not journalist summaries
- **Open access**: everything is freely fetchable
- **Review papers**: survey/review papers (search `survey OR review OR overview $ARGUMENTS`) synthesize an entire subfield

**Do NOT:**
- Treat citation count alone as quality — recent breakthrough papers have low citations initially
- Ignore the "Limitations" or "Future Work" sections — these often contain the most honest assessment
- Conflate preprints with peer-reviewed publications — note that arXiv papers may not be peer-reviewed
- Skip review/survey papers — they are often the most useful single source for understanding a field

Return: paper titles, authors, key findings with specific results/numbers, methodology type, limitations, citation counts when available, and arXiv URLs. Note the submission date and whether the paper is a preprint or has been published in a venue.
