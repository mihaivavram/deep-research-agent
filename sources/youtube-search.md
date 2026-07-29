Search YouTube for: $ARGUMENTS

YouTube hosts long-form expert reviews, tutorials, and demonstrations. **In this environment
YouTube yields metadata and description-level signal only — transcripts are not obtainable.**
Every documented transcript path has been tested and fails. Treat this source as *opportunistic*:
run it for creator/reviewer signal, but do not budget it for depth or count it toward
sub-question coverage.

## Access ladder

**Verified working:**
1. **General WebSearch (no `site:` scoping)** — searching the topic plus `youtube review` surfaces
   video pages with titles, channel names, and description text in the result snippets. This is
   the primary path.
2. **Direct watch-page WebFetch** — inconsistent, but when it renders it yields title, channel,
   view count, upload date, description, and chapter titles. Chapters are valuable: they are a
   structured outline of the video's argument. Attempt for the 2-3 most promising videos only.
3. **Channel video listings** — `youtube.com/@CHANNEL/videos` for a known authoritative channel.
4. **Creator's own site / blog / podcast page** — reviewers with a YouTube channel usually publish
   the same findings in text, which fetches cleanly. **This is often the highest-yield substitute:
   go for the text version of the same creator's analysis.**

**Dead paths — do NOT attempt, all tested and failing:**
- `youtube.com/results?search_query=` — returns footer navigation only
- `youtube.com/api/timedtext` — returns empty
- `youtubei/v1/player` — HTTP 405
- `downsub.com` — app shell, no transcript
- `youtubetotranscript.com` — HTTP 403
- `kome.ai` transcript generator — unverified, assume dead with the rest
- Invidious public instances (e.g. `inv.nadeko.net/api/v1/search`) — no response
- `site:youtube.com` scoped WebSearch — returns SEO listicles, not YouTube pages

## What to extract

- Video title, channel name, upload date, view count
- Description text — creators often include their key picks, links, and summaries
- Chapter titles if present (structured outline of the content)
- Engagement counts as signal-strength indicators
- The creator's text-published version of the same analysis, where one exists

## When YouTube matters / when to skip

**Matters:** hands-on product demonstrations, how-to content, conference talks, creator opinion
on trends — cases where a named reviewer's verdict is itself the evidence.

**Skip entirely:** academic, financial, legal, or any topic where written sources are more
authoritative. Given the transcript blackout, skip whenever the value would depend on what is
*said* in the video rather than what the title and description assert.

## Do NOT

- Spend fetches on any dead path listed above
- Claim a video's argument from its title alone — a title is a claim, not evidence. Attribute at
  the level you actually accessed it.
- Count description-level findings toward the surviving-pages minimum for a sub-question
- Prioritize high-view clickbait over lower-view videos from authoritative channels

Return: key points with video title, channel, view count, publish date, and URL. **Always flag the
extraction level** — description-only, metadata-only, or (rarely) full page. Never imply
transcript-level access.
