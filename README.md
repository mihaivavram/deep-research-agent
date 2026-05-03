# Deep Research Agent

A Claude Code research agent that searches many web sources in parallel and 
distills everything into a structured, ranked report (Markdown and PDF). 
Runs on the best and latest Claude model available and logs each run.

## Requirements

- Claude Code
- Python 3.10+ (for PDF export)
- System libraries for WeasyPrint (macOS: `brew install pango glib`; 
  Linux: `apt install libpango-1.0-0 libglib2.0-0`)

### Python setup

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or use an existing Python environment — just make sure the packages 
in `requirements.txt` are installed.

## Usage

Open this folder in Claude Code:

```bash
cd ~/Repositories/Agents/research-agent
```

Then just ask your research question:

```
What are the best mechanical keyboards under $150?
```

The agent automatically selects which sources to search, runs them all in 
parallel, and returns a synthesized report.

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

### Run logs

Every research run is logged to `logs/<report-name>.yaml` with start/end 
timestamps, per-skill status and timing, and any errors. Logs are local 
only (gitignored).

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
- **Key Findings** — the most important takeaways, synthesized across all sources
- **By Source** — what each source distinctly contributed
- **Consensus vs. Debate** — where sources agree, and where they conflict
- **Sources** — all URLs, each tagged with the skill that found it (e.g. `— reddit-search`, `— crunchbase-search`)
- **Reliability Ranking** — sources ranked from most to least reliable, with reasoning
