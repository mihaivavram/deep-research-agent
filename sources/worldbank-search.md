Search the World Bank for country-level economic, trade, and development data on: $ARGUMENTS

The World Bank is the authoritative free source for international macro data — GDP, inflation, trade balances, government debt, demographics, ease-of-doing-business, and country-by-country indicators. Use it any time an investment thesis touches a non-US country, an emerging market, or a cross-border trade dynamic.

**Indicator search:**
Use WebFetch on `https://data.worldbank.org/indicator?tab=all` to find indicator codes, or search directly: `https://data.worldbank.org/?q=QUERY`. Common high-value indicators:
- `NY.GDP.MKTP.CD` — GDP (current US$)
- `NY.GDP.MKTP.KD.ZG` — GDP growth (annual %)
- `FP.CPI.TOTL.ZG` — Inflation (CPI, annual %)
- `GC.DOD.TOTL.GD.ZS` — Central government debt as % of GDP
- `BN.CAB.XOKA.GD.ZS` — Current account balance as % of GDP
- `SP.POP.TOTL` — Population
- `SP.POP.65UP.TO.ZS` — Population aged 65+ (demographic decline signal)
- `NE.EXP.GNFS.ZS` — Exports as % of GDP (trade openness)
- `IC.BUS.EASE.XQ` — Ease of doing business rank

**Country dashboards:**
For a single country query, fetch `https://data.worldbank.org/country/COUNTRY-CODE` (e.g. `/country/IN` for India). These pages give a snapshot of all major indicators with 60+ years of history.

**API access:**
For programmatic queries, the JSON API is `https://api.worldbank.org/v2/country/COUNTRY/indicator/INDICATOR?format=json&date=YEAR1:YEAR2`.

**What to extract:**
- 5-year and 10-year trend for each cited indicator
- Comparison vs. regional peers and vs. global median (the World Bank pages often show this directly)
- Inflection points and what global event coincided (commodity boom, COVID, war, sanctions)
- For investment-thesis contexts, explicitly translate the macro figure into asset implications (e.g. "current account deficit widening + reserves falling → currency vulnerability → unhedged local-bond positions risky")

**Fallback:** If the World Bank site is slow, the IMF World Economic Outlook database at `https://www.imf.org/en/Publications/WEO` covers similar ground and is sometimes more current. Trading Economics also republishes World Bank series in a more skimmable format.

**Do NOT** quote a single year's number without trend context. Skip indicators with frequent revisions (some are restated 18 months later) — note the data vintage. Avoid using World Bank data for very recent (last 6 months) trends — there's a publication lag.

Return: indicator values with trend, peer comparison where relevant, inflection points, investment implications, data vintage, and the World Bank URLs.
