Search YouTube for: $ARGUMENTS

YouTube is the primary platform for long-form expert reviews, tutorials, and visual demonstrations. YouTube watch pages frequently block transcript extraction, so **use multiple extraction paths** rather than relying on direct watch-page fetches.

**Primary strategy — find videos via Google site-search:**
Run 2–3 queries:
- `site:youtube.com $ARGUMENTS` — broad sweep
- `site:youtube.com $ARGUMENTS review OR tutorial OR explained` — bias toward substantive content
- `site:youtube.com $ARGUMENTS 2025 OR 2026` — recency for time-sensitive topics

**Transcript extraction — ordered fallback chain:**
1. **Third-party transcript services (best path):** Extract the video ID from the YouTube URL (the `v=XXXX` parameter or `youtu.be/XXXX`). Then WebFetch one of these:
   - `https://downsub.com/?url=https://www.youtube.com/watch?v=VIDEO_ID`
   - `https://kome.ai/tools/youtube-transcript-generator?url=https://www.youtube.com/watch?v=VIDEO_ID`
   These services render transcripts server-side and are usually fetchable.
2. **YouTube search results page:** WebFetch `https://www.youtube.com/results?search_query=QUERY` — this renders server-side and includes video titles, channel names, view counts, and description snippets. Often enough signal without individual video pages.
3. **Direct watch page extraction:** WebFetch the watch page URL. Even when transcripts are blocked, extract whatever renders: video title, channel name, view count, upload date, description text, and chapter titles (chapters appear as a structured outline of the video's content).
4. **Channel pages:** For known authoritative channels, fetch `youtube.com/@CHANNEL/videos` to see their recent uploads and identify the most relevant video.

**What to extract:**
- Video title, channel name, upload date, view count
- Full transcript text when available (this is the highest-value data)
- Description text (creators often include key links, timestamps, and summaries)
- Chapter titles if present (structured outline of video content)
- Like/comment counts as engagement signals
- Key claims, recommendations, product picks, or methodology from the content

**When YouTube matters most:**
- Product reviews and comparisons (hands-on demonstrations)
- How-to and tutorial content
- Conference talks and expert presentations
- Creator/influencer opinion on trends

**When to deprioritize:**
- Pure text-based research (academic, financial, legal)
- Questions where written sources are more authoritative

**Do NOT:**
- Skip a video just because the transcript is unavailable — title + description + chapter titles often provide the core signal
- Prioritize clickbait titles with high views over lower-view videos from authoritative channels
- Ignore the comments section — top comments often contain corrections, updates, or alternative recommendations

Return: key points from video content, noting video title, channel, view count, publish date, and URL. Flag whether findings came from full transcripts, descriptions only, or title/metadata-level extraction.
