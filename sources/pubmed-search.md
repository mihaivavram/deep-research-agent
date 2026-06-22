Search PubMed for medical or scientific research on: $ARGUMENTS

PubMed is the authoritative database for biomedical and life sciences literature — uniquely valuable for health, medicine, pharmacology, clinical research, and biology. Unlike general web sources, PubMed entries are peer-reviewed and indexed with structured metadata.

**Primary strategy — PubMed search page:**
WebFetch `https://pubmed.ncbi.nlm.nih.gov/?term=QUERY&sort=date` (URL-encode the query). This returns a results page with titles, authors, journals, and publication dates.

**Secondary strategy — targeted searches by study quality:**
Run 2–3 queries biased toward the highest-evidence study types:
- `$ARGUMENTS meta-analysis OR systematic review site:pubmed.ncbi.nlm.nih.gov` — these synthesize entire bodies of research
- `$ARGUMENTS randomized controlled trial site:pubmed.ncbi.nlm.nih.gov` — gold-standard experimental evidence
- `$ARGUMENTS clinical trial site:pubmed.ncbi.nlm.nih.gov` — human trial data

**For the top 3–5 results, fetch the abstract page** (`https://pubmed.ncbi.nlm.nih.gov/PMID/`) and extract:
- Full title and complete author list
- Journal name and publication date (impact factor proxy)
- **Study design**: meta-analysis, RCT, cohort study, case-control, case report, review, in-vitro
- **Sample size**: how many participants/subjects (larger = more reliable)
- **Key findings**: specific numbers — effect sizes, p-values, confidence intervals, NNT, hazard ratios
- **Conclusions**: the authors' own summary of what the data means
- **Limitations**: stated limitations and potential biases (always present in good papers)
- **Funding sources and conflicts of interest**: industry-funded studies warrant skepticism on positive findings

**Full-text access for open-access papers:**
If the abstract references a PMC (PubMed Central) ID, the full text is freely available at `https://www.ncbi.nlm.nih.gov/pmc/articles/PMCID/`. Fetch this for high-priority papers to get methodology details, full results tables, and discussion sections.

**Evidence hierarchy (rank findings accordingly):**
1. Systematic reviews and meta-analyses (highest evidence)
2. Randomized controlled trials (RCTs)
3. Cohort studies (prospective > retrospective)
4. Case-control studies
5. Case series and case reports
6. Expert opinion and narrative reviews (lowest evidence)

**What makes PubMed uniquely valuable:**
- **Peer-reviewed**: every entry has passed editorial and peer review
- **Structured abstracts**: background, methods, results, conclusions — consistently formatted
- **MeSH indexing**: precise medical terminology linking related research
- **Clinical relevance**: translates bench science to patient outcomes

**Do NOT:**
- Treat a single study as definitive — look for replication and meta-analyses
- Ignore sample size — a study with n=12 is exploratory, not conclusive
- Skip the "Limitations" section — authors are required to disclose weaknesses
- Conflate in-vitro (lab) results with clinical (human) outcomes
- Ignore funding sources — industry-sponsored trials have documented publication bias toward positive results
- Cite retracted papers — check for retraction notices at the top of the abstract page

Return: study titles, journal names, study designs, sample sizes, key findings with specific statistics, limitations, evidence level, and PubMed URLs. Rank findings by evidence hierarchy, not by recency alone.
