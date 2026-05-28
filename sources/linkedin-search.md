Search LinkedIn for professional discourse, long-form articles, and hiring signals on: $ARGUMENTS

LinkedIn is heavily gated — most feed content requires login. But four public surfaces are useful and indexable: **Pulse articles, public posts, profiles, and job postings**. Use Google site-search to reach them.

**Pulse long-form articles (highest signal):**
- `site:linkedin.com/pulse $ARGUMENTS` — finds long-form articles by professionals, often 1,000+ words
- These are the closest LinkedIn equivalent to Substack — domain experts publishing under their real name and reputation
- WebFetch the article URL directly; Pulse articles render fully server-side

**Public posts (founders, executives, thought leaders):**
- `site:linkedin.com/posts $ARGUMENTS` — finds individual post URLs
- WebFetch on `linkedin.com/posts/USERNAME_POST-SLUG` URLs; many are publicly viewable without login
- High-engagement posts from named executives are useful sentiment / strategy signals

**Profiles (people lookups):**
- `site:linkedin.com/in $ARGUMENTS` — finds individual profiles
- Google snippets typically show: name, current title, company, location, top experience
- The full profile is gated but the snippet is often enough for quick credentialing
- For company employees: `site:linkedin.com/in "Company Name" "$ARGUMENTS"` — find people at a specific company in a specific role

**Job postings (strategic intent signal):**
- `site:linkedin.com/jobs $ARGUMENTS` — surfaces individual job posting pages
- Job posts reveal strategic priorities before press releases (heavy ML hiring → AI feature roadmap, EMEA AE roles → geographic expansion)
- WebFetch the posting page; the description, seniority, and team are visible without login

**Company pages:**
- `site:linkedin.com/company COMPANY-NAME` — for the company overview, headcount range, recent posts
- The "Insights" tab is gated but the public posts and headcount are visible

**Fallback strategies:**
1. If LinkedIn returns a login wall on direct fetch, **rely on Google snippets only** — they often contain enough text to extract the key claim
2. For profile-style queries, cross-reference with `/crunchbase-search` (founder bios) and `/glassdoor-search` (company-side context)
3. Authors who post on LinkedIn Pulse often cross-post to Twitter or Substack — search those platforms for the same person to get unfiltered versions

**Do NOT** attempt to scrape behind login or interpret the gated "Activity" section. Skip profiles that return only a 1-line snippet — there's not enough signal. Never quote a LinkedIn post you couldn't actually fetch — Google snippets are okay to paraphrase but flag them as snippet-only.

Return: Pulse article summaries with author credentials, public-post key claims with engagement signal, profile credentialing data (title/company/tenure), job posting strategic implications, and source LinkedIn URLs. Flag clearly which findings came from full fetches vs. snippets only.
