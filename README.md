# Deep Research Agent

A Claude Code research agent that searches up to 17 sources in parallel and 
distills everything into a structured, ranked report. Runs on `claude-opus-4-6` 
for best research quality.

## Requirements

- Claude Code

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
| What's the market narrative? | `web-search`, `news-search`, `hackernews-search` |
| B2C physical product? | `amazon-reviews`, `appstore-search`, `reddit-search` |
| B2B SaaS product? | `g2-search`, `producthunt-search`, `crunchbase-search`, `glassdoor-search` |

---

## Output Format

Every report includes:

- **Skills Used** — every command invoked, plus any that were skipped and why
- **Key Findings** — the most important takeaways, synthesized across all sources
- **By Source** — what each source distinctly contributed
- **Consensus vs. Debate** — where sources agree, and where they conflict
- **Sources** — all URLs, each tagged with the skill that found it (e.g. `— reddit-search`, `— crunchbase-search`)
- **Reliability Ranking** — sources ranked from most to least reliable, with reasoning
