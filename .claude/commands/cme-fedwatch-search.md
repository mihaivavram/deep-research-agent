Search CME FedWatch for market-implied Fed rate probabilities on: $ARGUMENTS

CME FedWatch is the canonical source for **what the futures market is pricing in** for upcoming FOMC meetings. It is the cleanest single signal of consensus rate expectations and is referenced by every Fed-watching trader.

**Primary source:**
Fetch `https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html` to get the live probability table. The page shows, for each upcoming FOMC meeting:
- The current target rate range (e.g. 5.25%–5.50%)
- The probability assigned to each possible outcome at that meeting (cut 50bps, cut 25bps, hold, hike 25bps)
- The implied terminal rate (where futures see the cycle ending)

**What to extract:**
- For the **next FOMC meeting**: the highest-probability outcome and its %, plus the second-most-likely outcome (consensus vs. dispersion)
- For meetings **3, 6, 12 months out**: the cumulative implied move from current
- The implied **terminal rate** and when it's reached
- Any sharp recent change in probabilities (the page often shows day-over-day deltas) — these usually map to a specific data release or Fed-speak

**Cross-reference for context:**
- Use /fred-search to pull DGS2 (2-year yield, which encodes the same expectations) and FEDFUNDS to confirm the current effective rate
- For rate-sensitive sectors (banks, REITs, growth stocks), state explicitly how the implied path would affect the thesis being researched

**Secondary sources if CME page is slow:**
- WebSearch `CME FedWatch DATE` or `Fed funds futures probability DATE` — financial press (Reuters, Bloomberg, WSJ) republishes the same data
- The Atlanta Fed's Market Probability Tracker is an alternative formal source

**Do NOT** present rate probabilities without dating them — these change daily, sometimes hourly. Always note the snapshot date. Skip if the user is asking about a specific meeting more than 12 months out (probabilities become noise).

Return: next-meeting probability distribution, 6/12-month cumulative implied move, terminal rate estimate, snapshot date, and the FedWatch URL.
