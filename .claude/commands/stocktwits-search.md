Search StockTwits for real-time retail sentiment on: $ARGUMENTS

StockTwits is the largest retail-investor microblog feed. Its value is **sentiment intensity and direction**, not analysis quality — use it as a contrarian indicator (extreme bullishness/bearishness on a ticker often precedes mean reversion) and a catalyst-detection layer.

**Ticker stream:**
If $ARGUMENTS is a ticker, fetch `https://stocktwits.com/symbol/TICKER` and extract:
- Sentiment ratio: % bullish vs. % bearish (StockTwits tags every post)
- Message volume: posts per day vs. the symbol's normal baseline (volume spikes signal news/catalysts)
- Watchers count and trend (rising watchers = building retail interest)
- Top recent posts and the engagement on each
- Any unusually high-engagement post that names a specific catalyst (earnings, FDA, court ruling, M&A rumor)

**Trending tickers:**
For "what is retail piling into right now" queries, fetch `https://stocktwits.com/rankings/most-active` or `https://stocktwits.com/rankings/trending`. Cross-reference with WSB / r/investing for confirmation.

**Sentiment search by keyword:**
Use WebSearch with `site:stocktwits.com $ARGUMENTS` to surface non-ticker conversations (e.g., "AI bubble", "rate cuts").

**Fallback:** If StockTwits blocks direct fetches, the mobile site at `m.stocktwits.com/symbol/TICKER` is sometimes more permissive. As a last resort, the public API at `https://api.stocktwits.com/api/2/streams/symbol/TICKER.json` returns sentiment-tagged JSON.

**Do NOT** mistake StockTwits sentiment for fundamentals — high bullishness from anonymous retail accounts is a *contrarian* signal, not a thesis. Skip individual posts with low engagement (under ~5 likes); focus on aggregate ratios and message-volume spikes.

Return: bull/bear sentiment %, message volume signal, watcher trend, named catalysts surfaced, and the StockTwits URL.
