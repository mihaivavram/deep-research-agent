Search Finviz for stock screener data, valuation, and short interest on: $ARGUMENTS

Finviz consolidates fundamentals, technicals, ownership, and news on a single quote page — use it for fast snapshot data that would otherwise require five separate sources.

**Single-ticker quote page:**
If $ARGUMENTS is a ticker, fetch `https://finviz.com/quote.ashx?t=TICKER` and extract:
- Valuation: P/E, Forward P/E, PEG, P/S, P/B, P/FCF, EV/EBITDA
- Profitability: ROA, ROE, ROIC, gross/operating/profit margin
- Growth: EPS growth (this/next year, past 5y, next 5y), sales growth
- Short interest: Short Float %, Short Ratio (days to cover), Short Interest
- Ownership: Insider Own %, Inst Own %, Insider Trans (3mo), Inst Trans
- Earnings date and analyst recommendation (1=Strong Buy, 5=Strong Sell)
- Performance: Perf Week/Month/Quarter/Half/Year/YTD vs SMA20/50/200

**Screener queries:**
For thematic searches (e.g. "small-cap profitable software companies"), use the screener URL pattern `https://finviz.com/screener.ashx?v=111&f=FILTERS` — example filters: `cap_small,fa_pe_u15,fa_roe_o15,sec_technology`. Fetch and extract the result table.

**News integration:**
The bottom of every quote page has aggregated news headlines with sources. These are useful for quickly identifying recent catalysts.

**Fallback:** If Finviz blocks the fetch (occasional rate limits), retry with a `site:finviz.com TICKER` WebSearch and pull cached snippets, or move to Yahoo Finance / Stock Analysis as backup quote sources.

**Do NOT** treat the analyst "Recommendation" number as a thesis — it's a lagging consensus average. Use it only as a sentiment data point, not a buy signal. Skip the "Insider Trading" table if there are fewer than 3 transactions in the last 6 months (too noisy).

Return: valuation snapshot, profitability/growth metrics, short interest signal, insider/institutional ownership trend, recent catalysts, and the Finviz quote URL.
