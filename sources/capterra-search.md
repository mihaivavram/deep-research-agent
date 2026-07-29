Search Capterra for: $ARGUMENTS

Capterra (owned by G2 as of ~2026-02, formerly Gartner Digital Markets) hosts verified B2B software reviews with job title, company size, and industry attached, and — uniquely — separate "Pros" and "Cons" free-text fields. The Cons field is the single richest structured B2B pain corpus for vertical-SaaS mining.

## URL patterns (VERIFY — never guess the numeric ID)
- Product reviews: `capterra.com/p/<NUMERIC_ID>/<ProductName>/reviews/`
- Product overview: `capterra.com/p/<NUMERIC_ID>/<ProductName>/`
- Category directory: `capterra.com/<category-slug>-software/`
- **The numeric ID is NOT guessable. ALWAYS run `WebSearch "capterra <product> reviews"` first to get the exact /p/<id>/ URL, THEN fetch it.** Guessed IDs 404 and waste the run (confirmed 2026-07-23).

## Query strategies (run at least 2)
1. `site:capterra.com <product or category>` — surfaces real product + category URLs with review counts in the snippet
2. `capterra <product> reviews` — gets the exact /p/<id>/ slug for a named product
3. For a category map: fetch `capterra.com/<category>-software/` — it lists many products with per-product star rating + review count in one page

## What to extract (unique to Capterra)
- Overall rating + total review count (corpus-volume signal)
- Verbatim CONS field text — the workflow pain, quoted (this is the payload)
- Reviewer job title + company size + industry (segment attribution forums lack)
- "Alternatives" / "Compare to" products listed on the page (competitor discovery)

## Fetch reality
- `capterra.com/p/<id>/<Name>/reviews/` FETCHES CLEAN (confirmed 2026-07-22: Applied Epic 4.2/5, 141 reviews, verbatim Cons pulled). Category pages usually fetch too.
- If a page 403s or is JS-only: fallback chain (Google cache -> archive.ph -> snippet extraction).
- Capterra shows a rolled-up rating; per-star distribution is on the reviews page.

## What NOT to do
- Do NOT construct /p/<id>/ URLs from a remembered or edited ID — search for the real one first.
- Do NOT rely on the overview page for review text — go to the /reviews/ sub-path.
- Do NOT confuse certificate-HOLDER tracking tools (myCOI, TrustLayer — buyer is the business tracking vendors) with agency-side COI ISSUANCE tools when the buyer segment matters.

Return: category URLs, per-product review counts + ratings, verbatim Cons themes, and the exact /p/<id>/ scrape URLs, with access level (full fetch vs snippet) flagged.
