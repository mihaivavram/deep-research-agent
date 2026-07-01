# Deep Research Agent

A Claude Code research agent that searches many web sources in parallel and 
distills everything into a structured, ranked report (Markdown and PDF). 
Runs on the best and latest Claude model available and logs each run.

## Installation

### 1. Clone the repo

```bash
git clone <repo-url> ~/Repositories/Agents/deep-research-agent
cd ~/Repositories/Agents/deep-research-agent
```

### 2. Python setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

PDF generation uses `fpdf2` — pure Python, no system libraries required.

### 3. Configure `.env`

Create a `.env` file in the project root. This file is gitignored.

```bash
# Required — path to the Python virtualenv with fpdf2 installed
VIRTUAL_ENV="/path/to/your/virtualenv"

# Optional — email delivery (Gmail example, uses App Passwords)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=you@gmail.com
SENDER_PASSWORD="xxxx xxxx xxxx xxxx"
RECIPIENT_EMAIL=recipient@example.com

# Optional — display name on sent emails (default: "Deep Research Agent")
SENDER_NAME="Deep Research Agent"
```

**`VIRTUAL_ENV`** is required for PDF export. Point it at the virtualenv 
where you installed `requirements.txt`. The PDF script activates this env 
at runtime.

**Email** is opt-in. If the SMTP variables are set, you can say "email me 
the results" in your query and the agent will send the report as an 
attachment. For Gmail, generate an 
[App Password](https://myaccount.google.com/apppasswords) — your regular 
password won't work with 2FA enabled.

### 4. Install as a global Claude Code skill (optional)

Link the project into Claude Code's skill directories so 
`/deep-research-agent` is available from any project, not just when you 
`cd` into this repo:

```bash
# Step 1 — link into the shared agents directory
ln -s "$(pwd)" ~/.agents/skills/deep-research-agent

# Step 2 — link into Claude Code's skill directory
ln -s ~/.agents/skills/deep-research-agent ~/.claude/skills/deep-research-agent
```

After this, `/deep-research-agent <query>` works from any directory in 
Claude Code. The skill reads its `SKILL.md`, `REFERENCE.md`, source 
strategies, and scripts from the symlinked project — no copies, no drift.

> **Note:** When invoked as a global skill, reports and logs are saved in 
> the *current working directory* (under `results/` and `logs/`), not in 
> the agent's installation directory.

## Usage

Open any project in Claude Code (or just a terminal) and ask your research 
question:

```
What are the best mechanical keyboards under $150?
```

Or invoke it explicitly as a skill:

```
/deep-research-agent What are the best mechanical keyboards under $150?
```

The agent automatically selects which sources to search, runs them all in 
parallel, and returns a synthesized report with Markdown and PDF output. 
If email is configured, add "email me the results" to your query.

> **Tip:** Prefix your query with `ultrathink` for deeper reasoning and 
> synthesis across sources. Best for complex queries where you want richer 
> analysis, not just aggregation.

### Targeting specific sources

Ask naturally or use slash commands directly:

```
What does reddit say about standing desks?
/reddit-search best standing desks under $500

Search arxiv and github for transformer architecture improvements

What's the competitive landscape for AI writing tools?
/g2-search Notion alternatives
/crunchbase-search vertical SaaS for construction
/wayback-search linear.app

Should I buy NVDA at current levels?
/sec-search NVDA latest 10-Q
/macrotrends-search NVDA gross margin history
/fred-search 10-year treasury yield
```

### Searching a source that doesn't have a skill yet

Just ask for it — the agent will write the command file and run it in the 
same session. The skill persists for all future sessions.

```
Search Quora for opinions on standing desks
Check Substack for takes on the creator economy
Look on Yelp for Italian restaurants in Austin
```

The agent will announce: `Created new skill: /quora-search — Quora questions and answers`

---

## How It Works

The agent follows a multi-stage pipeline for each research run:

### 1. Query analysis & decomposition

Before searching, the agent classifies the query (factual, opinion, product, 
market, investment, how-to, troubleshooting, recommendation) and decomposes 
complex queries into 2-4 sub-questions, each mapped to different source 
clusters. Queries are reformulated per source type — colloquial for Reddit, 
formal for SEC filings, technical for arXiv.

### 2. Research plan & depth budgeting

The agent emits a brief research plan before launching sources:

```
Research plan: Product comparison (Standard depth)
- Sub-questions: (1) Which models exist? (2) What do users say? (3) What do experts recommend?
- Sources: web-search, reddit-search, youtube-search, amazon-reviews, news-search [5 sources, ~20 fetches]
- Triage: score ≥ 4/9 to pass, re-query if < 3 pages/sub-question
- reddit-search demoted (2/5 recent success) — compensating with extra web-search query
```

Three depth tiers control how many sources and pages are fetched:

| Tier | When | Sources | Page fetches |
|---|---|---|---|
| Quick | Simple factual lookup | 2-3 | 5-8 |
| Standard | Product comparison, opinion survey, how-to | 4-6 | 15-25 |
| Deep | Market analysis, investment thesis, or user says "deep dive" | 8-15 | 30-50 |

### 3. Parallel source execution

All selected sources run simultaneously. Each source has a strategy file 
(`sources/<name>.md`) with site-specific search tactics, extraction guidance, 
and fallback chains. If a source is blocked or returns empty results, 
the agent falls back through Google cache, Wayback Machine, archive.ph, 
and finally snippet extraction — never reporting "no results" if snippets 
contained relevant content.

### 4. Source triage (per-page quality gate)

After fetching, each page is scored on three axes (0-3 each):

| Axis | What it measures |
|---|---|
| **Relevance** | How directly the page addresses the query or sub-question |
| **Authority** | Source credibility — primary data vs. anonymous blog |
| **Recency** | How current the content is relative to the topic |

Pages scoring below the tier threshold are dropped from synthesis (but still 
listed in the report as triaged out). If too few pages survive for a 
sub-question, the agent re-queries with reformulated terms — up to 2 rounds.

Triage thresholds and scoring parameters are configurable in 
`sources/triage-config.yaml`.

### 5. Gap detection

Before synthesizing, the agent checks for:
- **Source category gaps** — e.g., product query with no user reviews
- **Temporal gaps** — all sources older than 6 months on a time-sensitive topic
- **Perspective gaps** — all sources agree on a debatable topic (missing contrarian view)
- **Contradictions** — unresolved conflicts needing a tiebreaker source

### 6. Synthesis & report

The agent distills everything into a structured report with confidence-scored 
findings, cross-source validation, and a self-assessed quality score.

### 7. Progress reporting

During execution, the agent emits real-time progress:

```
[1/7] web-search: 8 pages fetched ✓
[2/7] reddit-search: blocked, extracted 3 snippets ⚠
[3/7] youtube-search: 4 videos found (descriptions only) ✓
[4/7] amazon-reviews: 5 product pages fetched ✓
[5/7] source-triage: 18/23 pages passed (5 dropped, score < 4) ✓
[6/7] re-query: 1 sub-question below minimum, 3 new pages fetched (2 passed) ⚠
[7/7] gap-detection: 1 follow-up search triggered ✓
```

---

## Available Skills

### Core — always run by default

| Command | What it does |
|---|---|
| `/web-search <query>` | General internet search — reads full articles, not just snippets |
| `/reddit-search <query>` | Reddit threads and top comments across multiple subreddits |
| `/youtube-search <query>` | YouTube videos — transcripts, descriptions, top comments |

### Optional: General research — used automatically when relevant, or on explicit request

| Command | When it's used |
|---|---|
| `/arxiv-search <query>` | Scientific research, ML/AI, physics, math, formal papers |
| `/pubmed-search <query>` | Health, medicine, clinical research, pharmacology |
| `/github-search <query>` | Open-source software, libraries, developer tools |
| `/wikipedia-search <query>` | Foundational context, definitions, entity disambiguation |
| `/news-search <query>` | Current events, breaking news, time-sensitive developments |
| `/hackernews-search <query>` | Developer culture, startups, tech industry |

### Optional: Social & community — used automatically for opinion, professional discourse, or workplace queries

| Command | What it finds |
|---|---|
| `/twitter-search <query>` | Twitter/X — real-time discourse, expert hot-takes, viral threads, breaking signals |
| `/linkedin-search <query>` | LinkedIn — Pulse long-form articles, public posts, profile credentialing, job postings |
| `/threads-search <query>` | Threads (Meta) — creator/designer/marketer commentary |
| `/blind-search <query>` | Blind — verified-employee anonymous comp data, layoffs, RTO, internal culture |
| `/quora-search <query>` | Quora — long-form expert Q&A, niche explainers, credentialed answers |

### Optional: Product & market research — used automatically for product/competitive/market queries

| Command | What it finds |
|---|---|
| `/producthunt-search <query>` | Launch history, upvote counts, early adopter community discussion |
| `/g2-search <query>` | G2, Capterra, Trustpilot — ratings, complaint themes, competitor comparisons |
| `/appstore-search <query>` | App Store + Play Store reviews — user frustrations and praise |
| `/amazon-reviews <query>` | Amazon review analysis — primary research for physical/DTC products |
| `/crunchbase-search <query>` | Funding rounds, investors, headcount, hiring patterns as strategy signal |
| `/trends-search <query>` | Google Trends + Exploding Topics — demand curve and category growth |
| `/glassdoor-search <query>` | Employee reviews + job postings as proxy for strategic priorities |
| `/wayback-search <query>` | Competitor positioning, pricing, and messaging evolution over time |

### Optional: Investing & financial research — used automatically for stock / fund / macro queries

| Command | What it finds |
|---|---|
| `/sec-search <query>` | SEC EDGAR — 10-K, 10-Q, 8-K, Form 4 insider transactions, proxy statements |
| `/finviz-search <query>` | Quote-page snapshot: valuation, profitability, short interest, ownership |
| `/macrotrends-search <query>` | 20+ year historical financials — margin, FCF, ROIC trend lines |
| `/seekingalpha-search <query>` | Long/short investor theses, earnings reactions, contributor track records |
| `/fred-search <query>` | Federal Reserve macro data — CPI, yield curve, M2, payrolls, credit spreads |
| `/stocktwits-search <query>` | Real-time retail sentiment ratios and message-volume catalyst spikes |
| `/benzinga-search <query>` | Analyst rating changes, unusual options flow, breaking corporate news |
| `/bogleheads-search <query>` | Long-term passive investing forum + wiki — fund/ETF and tax placement |
| `/valueinvestorsclub-search <query>` | Vetted deep fundamental write-ups from professional value investors |
| `/substack-search <query>` | Independent analyst newsletters — macro, quant, sector deep work |
| `/cme-fedwatch-search <query>` | Market-implied probabilities for upcoming FOMC rate decisions |
| `/worldbank-search <query>` | Country GDP, inflation, debt, demographics — international/EM angles |

### PDF export

| Command | What it does |
|---|---|
| `/export-pdf <filename>` | Convert a specific report in `results/` to a styled PDF |
| `/export-pdf all` | Convert all reports in `results/` to PDF |

### Dynamic skills — created on demand

If you name any source that doesn't have a skill, the agent writes the command file, runs the search, and saves it for future sessions. The agent grows over time.

---

## Product Research Routing

The agent automatically maps your question type to the right skill subset:

| Research question | Skills prioritized |
|---|---|
| Is this market real / is there demand? | `trends-search`, `reddit-search`, `appstore-search` |
| Who are the players / competitive landscape? | `crunchbase-search`, `producthunt-search`, `g2-search` |
| What do users hate / what's the gap? | `g2-search`, `amazon-reviews`, `reddit-search`, `appstore-search` |
| Where is money and talent flowing? | `crunchbase-search`, `glassdoor-search` |
| How has a competitor evolved / pivoted? | `wayback-search`, `news-search` |
| What's the market narrative? | `web-search`, `news-search`, `hackernews-search`, `twitter-search` |
| What's it actually like to work at this company? | `blind-search`, `glassdoor-search`, `reddit-search` |
| What do experts publicly say about this topic? | `twitter-search`, `linkedin-search`, `quora-search` |
| B2C physical product? | `amazon-reviews`, `appstore-search`, `reddit-search` |
| B2B SaaS product? | `g2-search`, `producthunt-search`, `crunchbase-search`, `glassdoor-search` |

---

## Investing Research Routing

For stock, ETF, fund, sector, or macro questions, the agent maps to the right financial sources:

| Research question | Skills prioritized |
|---|---|
| Is this company financially healthy? | `sec-search`, `macrotrends-search`, `finviz-search` |
| What's the analyst / Wall Street view? | `benzinga-search`, `seekingalpha-search`, `news-search` |
| What's the macro backdrop? | `fred-search`, `cme-fedwatch-search`, `news-search` |
| What's retail sentiment right now? | `stocktwits-search`, `reddit-search` (r/investing, r/wallstreetbets) |
| Long-term passive / ETF research? | `bogleheads-search`, `macrotrends-search`, `finviz-search` |
| Deep value / fundamental thesis? | `valueinvestorsclub-search`, `sec-search`, `seekingalpha-search` |
| International or emerging-market angle? | `worldbank-search`, `fred-search`, `news-search` |
| Independent / contrarian analyst views? | `substack-search`, `seekingalpha-search`, `valueinvestorsclub-search` |
| Recent catalyst / breaking corporate news? | `benzinga-search`, `news-search`, `sec-search` (8-K) |
| What are insiders doing? | `sec-search` (Form 4), `finviz-search` |

---

## Output Format

Every report includes:

- **Skills Used** — every command invoked, plus any that were skipped and why
- **Key Findings** — top takeaways synthesized across all sources, each prefixed with a confidence level (High / Medium / Low / Unverified) based on source count and type
- **By Source** — what each source distinctly contributed
- **Consensus vs. Debate** — where sources agree, and where they conflict
- **Sources** — all URLs, each tagged with the skill that found it (e.g. `— reddit-search`). Pages that failed triage are listed with `[triaged out — score X/9]`
- **Reliability Ranking** — sources ranked most to least reliable, with publication date and bias signals noted
- **Research Quality Score** — self-assessed 1-5 based on coverage, source diversity, claim backing, contradiction resolution, and staleness checks

---

## Quality & Reliability Features

### Adaptive source health

The agent tracks each source's success/failure rate across runs in 
`sources/SOURCE-HEALTH.md`. Sources that have failed 3+ of their last 5 runs 
are automatically demoted — still attempted, but compensated for with 
alternative queries. Sources with perfect recent records get priority 
in synthesis.

### Source triage

After fetching pages but before synthesis, each page is individually scored 
(relevance + authority + recency, 0-9 scale) and weak pages are dropped. 
If too few quality pages survive for a sub-question, the agent re-queries 
with reformulated terms. This prevents synthesizing noise.

Triage is configurable via `sources/triage-config.yaml`:

| Parameter | Default | What it controls |
|---|---|---|
| `thresholds.standard` | 4 | Minimum score (out of 9) for a page to enter synthesis |
| `min_surviving_pages.standard` | 3 | Min pages per sub-question before re-query triggers |
| `max_requery_rounds` | 2 | How many re-query rounds before accepting results |
| `snippet_penalty` | 2 | Score penalty for snippet-only access |
| `healthy_source_bonus` | 1 | Score bonus for sources with 5/5 recent health |

### Confidence scoring

Each key finding is prefixed with a confidence level:

| Level | Criteria |
|---|---|
| **High** | 3+ independent sources including a primary source |
| **Medium** | 2 sources, or 1 primary source |
| **Low** | Single non-primary source, or all derivative of the same original |
| **Unverified** | Snippet-only, no corroboration, or single anonymous source |

### Cross-source validation

During synthesis, the agent traces citation chains (multiple articles citing 
the same study count as one source, not many), flags platform-specific biases, 
and notes freshness for time-sensitive topics.

### Universal fallback chain

When any source is blocked (403, 429, 451, timeout, empty): Google cache, 
Wayback Machine, archive.ph, then snippet extraction. The agent never reports 
"no results" if search snippets contained relevant content.

---

## Run Logs

Every research run is logged to `logs/<report-name>.yaml` with structured, 
machine-parseable fields designed for later LLM review and trend analysis.

### What's logged

- **Run metadata** — query type, depth tier, duration, research plan, quality score
- **Per-skill status** — timestamp, status (`success`/`partial`/`no_results`/`skipped`/`error`), pages fetched, queries run, fallback used and whether it succeeded
- **Triage stats** — pages scored, passed, dropped, threshold used, re-query rounds
- **Gap detection** — gaps found, follow-up searches triggered
- **Per-page errors** — every failed URL is logged individually with structured fields:
  - `error_type` — one of: `access_blocked`, `rate_limited`, `timeout`, `empty_content`, `parse_error`, `redirect_error`, `server_error`, `login_required`
  - `http_status` — actual HTTP response code (or `null` for timeouts)
  - `url` — the specific URL that failed
  - `fallback_used` — which fallback was tried (`google_cache`, `wayback`, `archive_ph`, `google_snippets`, `none`)
  - `fallback_succeeded` — whether the fallback produced usable data
  - `error` — human-readable description

### Reviewing logs for improvements

The structured format makes it straightforward to ask an LLM to review logs 
and surface patterns. Example prompts:

```
Review all YAML files in logs/ and tell me:
- Which sources fail most often, and what error types dominate?
- Which fallback strategies succeed vs. fail?
- Are there sources I should demote or drop?
- What's my average fetch success rate and triage pass rate?
- Any patterns in the types of queries that produce low quality scores?
```

Logs are local only (gitignored).

---

## Configuration Files

| File | Purpose |
|---|---|
| `sources/triage-config.yaml` | Triage scoring weights, thresholds, re-query settings |
| `sources/SOURCE-HEALTH.md` | Per-source success/failure tracking across runs (auto-updated) |
| `sources/<name>.md` | Search strategy for each source (site-scoped queries, extraction guidance, fallbacks) |
| `.env` | `VIRTUAL_ENV` path (required for PDF), SMTP credentials (optional, for email delivery) |

---

## Project Structure

```
.
├── CLAUDE.md                    # Agent instructions (the brain)
├── REFERENCE.md                 # Source routing quick-reference
├── SKILL.md                     # Skill definition for Claude Code
├── README.md                    # This file
├── .env                         # VIRTUAL_ENV path + SMTP credentials (gitignored)
├── requirements.txt             # Python dependencies (fpdf2)
├── sources/
│   ├── triage-config.yaml       # Triage scoring configuration
│   ├── SOURCE-HEALTH.md         # Source reliability tracking
│   ├── web-search.md            # Source strategy files (one per source)
│   ├── reddit-search.md
│   └── ...                      # 34 source strategies total
├── scripts/
│   ├── md_to_pdf.py             # CLI wrapper — Markdown → PDF
│   ├── report_pdf.py            # PDF engine (fpdf2-based, pure Python)
│   └── send_email.py            # Email delivery with SMTP
├── results/                     # Generated reports (gitignored contents)
├── logs/                        # Run logs (gitignored contents)
└── .claude/
    ├── commands/                 # Symlinks to sources/*.md (slash commands)
    ├── settings.json             # Model and permission config
    └── skills/                   # Skill definitions
```

### Global installation layout

When installed as a global skill (see Installation step 4):

```
~/.agents/skills/
└── deep-research-agent -> /path/to/deep-research-agent   # symlink to repo

~/.claude/skills/
└── deep-research-agent -> ~/.agents/skills/deep-research-agent  # chains to above
```
