Reconstruct positioning and pricing history for: $ARGUMENTS

The goal of this skill is a **timeline**: how a company's messaging, pricing, ICP, and feature set
changed over time. The Wayback Machine is the natural tool for that and **it is unavailable in this
environment** — so this skill reconstructs the timeline from dated live sources instead.

## Access ladder

**Dead — do NOT attempt, all refused at client level:**
- `web.archive.org/web/*/DOMAIN` — refused
- `web.archive.org/cdx/search/cdx` (CDX API) — refused
- `archive.ph` / `archive.today` — refused
- `timetravel.mementoweb.org` — DNS does not resolve

There is **no working web-archive path**. Do not spend fetches discovering this again.

**Verified working substitutes — dated live sources:**
1. **Press-release wires** — `globenewswire.com`, `businesswire.com`, `prnewswire.com` all fetch
   cleanly and are **date-stamped**, which is exactly what a timeline needs. Search
   `<company> site:globenewswire.com` and read chronologically. These are the reliable path to
   dated product launches, funding, repositioning, and adoption numbers.
2. **Trade press with visible publication dates** — for any vertical, the trade outlets fetch far
   more reliably than general tech press. Sort findings by publish date to build the sequence.
3. **Dated third-party commentary** — blog posts, newsletters, and review-site verbatims that
   quote the company's pricing or claims *at a point in time*. A 2023 review quoting "$49/mo" is
   evidence about 2023 pricing. **Capterra verbatims carry dates** and are usable this way.
4. **The company's own changelog / blog / release notes** — often the single best artifact.
   Try `/blog`, `/changelog`, `/releases`, `/whats-new`, `/pricing`. Changelogs are chronological
   by construction.
5. **The live pages as the timeline's endpoint** — fetch current homepage/pricing to anchor "now,"
   then work backward with the dated sources above.

## Method

1. Identify the target domain via WebSearch if not supplied.
2. Anchor the present: fetch the current homepage and pricing page.
3. Gather dated evidence from the wires and trade press, oldest to newest.
4. Build the timeline, attaching a date and a source URL to every claim.
5. **State the gaps.** A reconstructed timeline has holes. Name the periods you have no evidence
   for rather than interpolating across them.

## What to look for

- How the headline value proposition changed — pivots surface here first
- When pricing changed: up, down, or restructured (per-seat → usage-based is a strategy change)
- Features added or, more tellingly, quietly removed
- ICP shifts — "for teams" → "for enterprises" is a go-to-market change
- Renames, repositioning, and category-switching

## Do NOT

- Attempt any archive host — they are all refused, and it wastes the fetch budget
- Present a reconstructed timeline as archive-verified. Say it is reconstructed from dated
  secondary sources, and mark each entry with its evidence date.
- Infer a change happened at a date merely because that is when you found an article about it —
  distinguish "the change occurred" from "the change was reported"
- Interpolate across evidence gaps

Return: a dated timeline of positioning/pricing/feature changes, each entry with its source URL and
evidence date; an explicit list of periods with no coverage; and a note that this is a
reconstruction, since no web archive was reachable.
