Search GitHub for: $ARGUMENTS

GitHub is the primary platform for open-source software, developer tools, and code-level evidence. It uniquely provides: working code, real-world usage patterns, community-reported issues, and strategic signals from project activity.

**Primary strategy — GitHub search page (renders server-side):**
WebFetch `https://github.com/search?q=QUERY&type=repositories&sort=stars` to find top repositories. This returns repository names, descriptions, star counts, and language breakdown.

**Secondary strategy — Google site-search for deeper discovery:**
- `site:github.com $ARGUMENTS` — broad repository and page discovery
- `site:github.com $ARGUMENTS awesome` — find curated "awesome lists" (community-maintained resource collections)
- `site:github.com $ARGUMENTS issues OR discussions "help wanted"` — find real-world problems and community activity
- `site:github.com $ARGUMENTS README.md` — surface well-documented projects

**For the top 3–5 results, fetch and extract:**

1. **README content (highest value):** WebFetch `https://raw.githubusercontent.com/OWNER/REPO/main/README.md` (try `master` if `main` fails). READMEs contain: project purpose, features, installation, usage examples, and comparison to alternatives.

2. **Repository metadata (from the repo page):** WebFetch `https://github.com/OWNER/REPO` and extract:
   - Star count (popularity signal — >1K stars = significant adoption)
   - Fork count (developer engagement)
   - "Used by" count if visible (real-world adoption)
   - Last commit date (is it actively maintained?)
   - Language breakdown
   - License type

3. **Issues and Discussions (real-world pain points):** WebSearch `site:github.com/OWNER/REPO/issues $ARGUMENTS` or fetch the issues page. Look for:
   - Recurring complaints or feature requests (signal for product gaps)
   - Resolved vs. open issue ratio (project health)
   - Response time from maintainers (community responsiveness)
   - "Bug" vs. "enhancement" labels (stability signal)

**What makes GitHub uniquely valuable:**
- **Working code**: proof that something works, not just claims
- **Issue discussions**: unfiltered user reports of real-world problems
- **Activity signals**: commit frequency, contributor count, and release cadence reveal project health
- **Awesome lists**: community-curated resources that surface the best tools in any category
- **Comparative READMEs**: many projects include "Alternatives" or "Comparison" sections

**Do NOT:**
- Equate high star counts with quality — some viral repos are toys; some low-star repos are critical infrastructure
- Ignore archived or unmaintained repos without noting it — "archived" means the maintainer has abandoned it
- Skip the issues tab — it often contains more honest assessments than the README
- Treat GitHub Copilot suggestions or AI-generated code as authoritative source material

Return: project names with star counts and last-commit dates, key README highlights, notable issues or discussions, community health signals, and GitHub URLs. Note whether projects are actively maintained.
