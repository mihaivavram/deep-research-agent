Search SEC EDGAR for company filings, earnings, and insider transactions on: $ARGUMENTS

EDGAR is the primary, authoritative source for US public company disclosures — anything sourced here is legally vetted and beats secondhand analyst summaries.

**Full-text filing search:**
Use WebFetch on `https://efts.sec.gov/LATEST/search-index?q=%22QUERY%22&forms=10-K,10-Q,8-K` (URL-encode the query) to find recent filings. Run at least 2 form-type variants:
- `forms=10-K,10-Q` for annual/quarterly financials
- `forms=8-K` for material events (acquisitions, executive changes, guidance updates)
- `forms=4` for insider transactions (officer/director buys and sells)
- `forms=DEF+14A` for proxy statements (executive comp, related-party deals)

**Company-specific lookup:**
If $ARGUMENTS is a ticker or company name, fetch `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=TICKER&type=&dateb=&owner=include&count=40` to get the filing index, then fetch individual filings.

**What to extract:**
- From 10-K/10-Q: revenue trend, segment breakdown, gross/operating margins, cash flow from ops, debt levels, stated risk factors (Item 1A is the most underread section)
- From 8-K: the specific item number (Item 2.02 = earnings, Item 5.02 = exec departure, Item 1.01 = material agreement)
- From Form 4: net insider buying/selling, cluster buys (multiple insiders buying = strong signal)
- From DEF 14A: CEO comp vs peer median, perks, related-party transactions

**Fallback:** If EDGAR full-text search times out, use WebSearch with `site:sec.gov $ARGUMENTS` and fetch the resulting filing pages directly.

**Do NOT** rely on summary press releases or third-party filing aggregators — fetch the primary filing. Skip thin filings (S-8, 144) unless specifically asked about insider sales.

Return: filing types found, key financial figures with YoY trend, insider transaction summary, material risk factors, and direct EDGAR URLs for each filing cited.
