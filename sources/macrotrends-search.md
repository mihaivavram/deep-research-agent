Search Macrotrends for long-term historical financials and ratio trends on: $ARGUMENTS

Macrotrends is uniquely valuable for **20+ year time series** — use it any time you need to understand whether a company's current margin/FCF/ROIC is structural or cyclical, or whether a multiple is high vs. its own history.

**Company financials:**
If $ARGUMENTS is a ticker/company, fetch the relevant Macrotrends pages directly:
- `https://www.macrotrends.net/stocks/charts/TICKER/COMPANY-SLUG/revenue` (and `/gross-profit`, `/operating-income`, `/net-income`, `/free-cash-flow`)
- `https://www.macrotrends.net/stocks/charts/TICKER/COMPANY-SLUG/profit-margins` (and `/operating-margin`, `/roe`, `/roic`)
- `https://www.macrotrends.net/stocks/charts/TICKER/COMPANY-SLUG/pe-ratio` (and `/ps-ratio`, `/price-book`, `/ev-ebitda`)
If you don't know the slug, run a `site:macrotrends.net TICKER` WebSearch first to discover the canonical URL.

**What to extract — focus on shape, not point values:**
- 10-year and 20-year trend direction for revenue, gross margin, operating margin, FCF
- ROIC vs cost of capital over time (is the business actually creating value?)
- Current valuation multiple vs its own 10-year median (cheap vs history is more useful than cheap vs sector)
- Inflection points: when did margins/growth break trend, and what happened that year?

**Macro time series:**
Macrotrends also hosts long-run macro data: `https://www.macrotrends.net/2526/sp-500-historical-annual-returns`, gold/oil prices, CPI, interest rates. Fetch these for cycle context.

**Fallback:** If a specific Macrotrends page 404s, try the parent ticker page `https://www.macrotrends.net/stocks/charts/TICKER/` to navigate to the correct slug. As a last resort, use Stock Analysis (stockanalysis.com) for 10-year history.

**Do NOT** quote single-year numbers without the surrounding trend — the entire value of Macrotrends is the time series. Skip pages with fewer than 5 years of history.

Return: long-run trend descriptions (with start/end values and direction), ratio vs. own-history comparison, inflection-point years, and the Macrotrends URLs for each chart cited.
