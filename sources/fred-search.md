Search FRED (Federal Reserve Economic Data) for macroeconomic time series on: $ARGUMENTS

FRED is the authoritative free source for US (and many international) macro data series. Use it any time an investment thesis touches rates, inflation, employment, credit, or money supply — these are the variables that move every asset class.

**Series search:**
Use WebFetch on `https://fred.stlouisfed.org/searchresults/?st=QUERY` (URL-encode) to find relevant series. For specific known series, fetch directly:
- `https://fred.stlouisfed.org/series/CPIAUCSL` — Headline CPI
- `https://fred.stlouisfed.org/series/CPILFESL` — Core CPI
- `https://fred.stlouisfed.org/series/DGS10` — 10-Year Treasury Yield
- `https://fred.stlouisfed.org/series/DGS2` — 2-Year Treasury Yield
- `https://fred.stlouisfed.org/series/T10Y2Y` — 10y-2y spread (recession indicator)
- `https://fred.stlouisfed.org/series/UNRATE` — Unemployment Rate
- `https://fred.stlouisfed.org/series/M2SL` — M2 Money Supply
- `https://fred.stlouisfed.org/series/FEDFUNDS` — Effective Fed Funds Rate
- `https://fred.stlouisfed.org/series/BAMLH0A0HYM2` — High-yield credit spread
- `https://fred.stlouisfed.org/series/DCOILWTICO` — WTI crude
- `https://fred.stlouisfed.org/series/PAYEMS` — Nonfarm payrolls

**What to extract from each series page:**
- Latest observation value and date
- Direction over the last 3, 6, 12 months
- Long-run context: where does the current value sit vs. the 10-year and 30-year history?
- Recession-bar overlay (FRED marks recessions on every chart) — note proximity to historical inversions/spikes
- Release schedule (some series are real-time, others lag 30+ days — note staleness)

**Cross-series reasoning:**
The most useful FRED outputs combine series — e.g. real yields = DGS10 - CPIAUCSL YoY, financial conditions = credit spread + USD index + equity vol. State these explicitly when relevant.

**Fallback:** If FRED is slow, use `site:fred.stlouisfed.org $ARGUMENTS` WebSearch. The St. Louis Fed's FRED API at `https://api.stlouisfed.org/fred/series/observations?series_id=ID` also returns clean JSON if you have an API key.

**Do NOT** quote a single data point without trend context — a 3.2% CPI print only matters relative to expectations and trajectory. Skip series with fewer than 24 months of history.

Return: series found, latest value, trend direction, position vs. long-run history, any cross-series implications, and source FRED URLs.
