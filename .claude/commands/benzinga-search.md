Search Benzinga for breaking news, analyst rating changes, and options flow on: $ARGUMENTS

Benzinga is a fast-feed financial newswire — its three differentiated signals are **analyst rating changes** (upgrades/downgrades with target moves), **unusual options activity**, and **catalyst-driven news** that often hits before mainstream media.

**Analyst ratings:**
Use WebSearch with `site:benzinga.com $ARGUMENTS analyst rating` or `site:benzinga.com $ARGUMENTS upgrade OR downgrade`. Fetch the top results to extract:
- The brokerage firm name and analyst
- Old rating → new rating
- Old price target → new price target (and % change)
- The dated catalyst behind the change
- Whether multiple firms moved the same direction in the same week (consensus shift)

**Unusual options activity:**
Search `site:benzinga.com $ARGUMENTS unusual options` to find pieces flagging large block trades or unusual put/call ratios. Note strike, expiry, premium paid, and whether the trade was bought or sold (sweep = bought aggressively).

**Catalyst news feed:**
Search `site:benzinga.com $ARGUMENTS` for general news. Benzinga tends to publish FDA decisions, earnings beats/misses, and corporate guidance updates within minutes of release. Note the timestamp.

**Pre-market and after-hours movers:**
For "what moved overnight" queries, fetch `https://www.benzinga.com/news/pre-market-outlook` or search `site:benzinga.com pre-market movers DATE`.

**Fallback:** If Benzinga's site blocks the fetch, use Google News search restricted to benzinga.com, or pivot to /news-search for the same catalyst across multiple wires.

**Do NOT** treat "unusual options activity" as a directional signal on its own — the same flow can be hedge or speculation. Cross-reference with stock price action and any concurrent catalyst. Skip "trader idea" posts with no named source.

Return: rating change details, options flow specifics, catalyst news with timestamps, and source Benzinga URLs.
