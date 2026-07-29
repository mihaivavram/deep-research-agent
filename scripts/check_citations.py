#!/usr/bin/env python3
"""Verify citation integrity in a research report.

Quality gate 3 in CLAUDE.md ("every major claim has an inline citation") was previously
unverifiable — nothing checked it, so it was graded by eyeballing. This script checks it
mechanically, plus the things eyeballing never catches: dead URLs, and quotes that do not
actually appear at the page they are attributed to.

Structural checks run offline and are fast. Network checks are opt-in.

Usage:
    python3 scripts/check_citations.py results/report.md              # structural only
    python3 scripts/check_citations.py results/report.md --check-urls # + resolve every URL
    python3 scripts/check_citations.py results/report.md --check-quotes  # + verify quotes
    python3 scripts/check_citations.py results/*.md                   # many reports

Exit code 0 if all checks pass, 1 otherwise.
"""

import sys
import os
import re
import glob
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LINK = re.compile(r"\[([^\]\[]*)\]\((https?://[^\s)]+)\)")
BARE_URL = re.compile(r"(?<![\(<\w])(https?://[^\s<>)\]]+)")
CONFIDENCE = re.compile(r"\*\*\[(High|Medium|Low) confidence\]\*\*|\*\*\[Unverified\]\*\*")
# Quoted spans of >=5 words — short quotes are too generic to verify meaningfully.
QUOTE = re.compile(r"[\"“]([^\"”\n]{25,400})[\"”]")
PLACEHOLDER = re.compile(r"example\.com|localhost|127\.0\.0\.1|TODO|FIXME|<url>", re.I)

UA = {"User-Agent": "Mozilla/5.0 (compatible; deep-research-agent citation checker)"}
TIMEOUT = 15


def split_sections(text):
    """Return an ordered list of (level, heading_lower, body_text) for markdown headings.

    Levels are kept so a section can be read together with its deeper subsections —
    reports group Sources by skill under ### headings, and those belong to Sources.
    """
    out, level, name, buf = [], 0, "_preamble", []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            out.append((level, name, "\n".join(buf)))
            level, name, buf = len(m.group(1)), m.group(2).strip().lower(), []
        else:
            buf.append(line)
    out.append((level, name, "\n".join(buf)))
    return out


def find_section(sections, *keywords):
    """Return (heading, body) for the best-matching section, including nested subsections.

    Candidates are ranked so that a real `## Sources` heading beats an incidental
    `### where sources agree` buried inside another section: exact match first, then
    heading-starts-with, then the shallowest level, then document order.
    """
    candidates = []
    for i, (level, name, body) in enumerate(sections):
        for kw in keywords:
            if kw not in name:
                continue
            if name == kw:
                rank = 0
            elif name.startswith(kw):
                rank = 1
            elif re.match(rf"^{re.escape(kw)}\b", name):
                rank = 2
            else:
                rank = 3
            candidates.append((rank, level, i))
            break
    if not candidates:
        return None, ""

    _, level, i = min(candidates)
    _, name, body = sections[i]
    chunks = [body]
    for sub_level, sub_name, sub_body in sections[i + 1:]:
        if sub_level <= level:
            break
        chunks.append(f"{'#' * sub_level} {sub_name}")
        chunks.append(sub_body)
    return name, "\n".join(chunks)


def claim_lines(body):
    """Bullets and confidence-labelled lines that constitute claims.

    A nested sub-bullet elaborating a cited parent is not an independent claim — it
    inherits the parent's citation. Only flag it when no ancestor is cited.
    """
    out = []
    # indent width -> whether the nearest bullet at that depth carried a citation
    cited_at_depth = {}
    # A confidence-labelled paragraph heads a claim group; the flat bullets beneath it
    # elaborate that claim. Track it so the group is judged once, not per line.
    group_cited = None
    for i, line in enumerate(body.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("|"):
            continue
        indent = len(line) - len(line.lstrip())
        is_bullet = bool(re.match(r"^([-*+]|\d+\.)\s+", s))
        is_labelled = bool(CONFIDENCE.search(s))
        if not (is_bullet or is_labelled):
            if indent == 0:
                group_cited = None          # ordinary prose ends the group
            continue
        has_cite = bool(LINK.search(s))

        if is_labelled and not is_bullet:
            group_cited = has_cite
            if not has_cite:
                out.append((i, s))          # report the group head once
            continue

        if is_bullet:
            cited_at_depth = {d: v for d, v in cited_at_depth.items() if d < indent}
            cited_at_depth[indent] = has_cite
        # Inherit a citation from any shallower (ancestor) bullet.
        if any(v for d, v in cited_at_depth.items() if d < indent):
            continue
        # Inherit from the confidence-labelled paragraph heading this group: if that head
        # was cited the bullets are covered; if it was uncited it is already reported.
        if group_cited is not None:
            continue
        out.append((i, s))
    return out


def is_research_report(text):
    """Distinguish a research report from an unrelated markdown file in results/.

    Front matter alone is not sufficient — PDF layout fixtures in results/ copy the front
    matter block too. A real report additionally has one of the mandated report sections or
    a body of citations. Something with none of those is a fixture or scratch file, and
    judging it against the report spec is pure noise.

    Deliberately permissive on the second test (any ONE of the three), so a genuine report
    cannot dodge the checks by dropping a single heading.
    """
    has_section = bool(re.search(r"^#{1,3}\s+(key findings|sources)\b", text, re.M | re.I))
    has_citations = len(LINK.findall(text)) >= 3
    return has_section or has_citations


def check_structure(path, text):
    errs, warns = [], []
    sections = split_sections(text)

    body_links = LINK.findall(text)
    if not body_links:
        errs.append("no markdown citations found anywhere in the report")

    # --- gate 3: every Key Findings claim carries an inline citation ---
    kf_name, kf = find_section(sections, "key finding", "findings")
    if not kf.strip():
        errs.append("no 'Key Findings' section found")
    else:
        uncited = []
        for lineno, line in claim_lines(kf):
            if not LINK.search(line):
                # A bullet may be cited by an indented child bullet directly beneath it.
                uncited.append((lineno, line))
        # Re-check: drop bullets whose following indented lines carry a citation.
        kf_lines = kf.splitlines()
        really_uncited = []
        for lineno, line in uncited:
            cited_by_child = False
            for nxt in kf_lines[lineno:lineno + 4]:
                if nxt.startswith((" ", "\t")) and LINK.search(nxt):
                    cited_by_child = True
                    break
                if nxt.strip() and not nxt.startswith((" ", "\t")):
                    break
            if not cited_by_child:
                really_uncited.append((lineno, line))
        for lineno, line in really_uncited:
            snippet = (line[:90] + "…") if len(line) > 90 else line
            errs.append(f"Key Findings line {lineno} has no inline citation: {snippet}")

    # --- confidence labels present at all ---
    if kf.strip() and not CONFIDENCE.search(kf):
        warns.append("no confidence labels ([High confidence] etc.) in Key Findings")

    # --- Sources section completeness ---
    src_name, src = find_section(sections, "sources")
    if not src.strip():
        warns.append("no 'Sources' section found")
    else:
        cited = {u.rstrip(".,;") for _, u in LINK.findall(text)}
        listed = {u.rstrip(".,;") for _, u in LINK.findall(src)}
        listed |= {u.rstrip(".,;") for u in BARE_URL.findall(src)}
        missing = sorted(cited - listed)
        if missing:
            warns.append(f"{len(missing)} URL(s) cited in the body but absent from Sources: "
                         + ", ".join(missing[:3]) + ("…" if len(missing) > 3 else ""))

    # --- coverage/gaps disclosure ---
    if not find_section(sections, "coverage", "gap")[1].strip():
        warns.append("no 'Coverage & Gaps' section — required when any residual gap exists")

    # --- placeholders and malformed links ---
    for _, url in LINK.findall(text):
        if PLACEHOLDER.search(url):
            errs.append(f"placeholder/non-real URL cited: {url}")
    for title, url in LINK.findall(text):
        if not title.strip():
            warns.append(f"citation with empty link text: {url}")

    return errs, warns


def fetch(url):
    """Return (status, body_text_or_None)."""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read(400_000)
            enc = resp.headers.get_content_charset() or "utf-8"
            return resp.status, raw.decode(enc, errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, None
    except Exception as exc:                     # noqa: BLE001 - network is best-effort
        return f"ERR {type(exc).__name__}", None


def check_urls(text, want_quotes=False):
    errs, warns = [], []
    urls = sorted({u.rstrip(".,;") for _, u in LINK.findall(text)})
    if not urls:
        return errs, warns
    print(f"      resolving {len(urls)} unique URL(s)…")
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(zip(urls, pool.map(fetch, urls)))

    for url, (status, body) in results.items():
        if isinstance(status, int) and 200 <= status < 400:
            continue
        # 403 is usually anti-bot, not a broken citation — warn, don't fail.
        if status in (403, 401, 429):
            warns.append(f"{status} (likely anti-bot, citation may still be valid): {url}")
        else:
            errs.append(f"unreachable citation [{status}]: {url}")

    if want_quotes:
        bodies = {u: b for u, (s, b) in results.items() if b}
        # The report quoting its own query (from YAML front matter) is not a source claim.
        own = re.search(r"^query:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
        own_query = re.sub(r"\s+", " ", own.group(1)).strip().lower() if own else ""
        quotes = [q for q in QUOTE.findall(text)
                  if not (own_query and re.sub(r"\s+", " ", q).strip().lower() in own_query)]
        if not quotes:
            print("      no verifiable quotes (>=25 chars) found")
        checked = 0
        for quote in quotes:
            norm = re.sub(r"\s+", " ", quote).strip().lower()
            if len(norm) < 25:
                continue
            checked += 1
            probe = norm[:120]
            if not any(probe in re.sub(r"\s+", " ", b).lower() for b in bodies.values()):
                warns.append(
                    f"quote not found in any fetched citation (may be paraphrased, "
                    f"paywalled, or fabricated): \"{quote[:70]}…\"")
        if checked:
            print(f"      verified {checked} quote(s)")
    return errs, warns


def main(argv):
    do_urls = "--check-urls" in argv or "--check-quotes" in argv
    do_quotes = "--check-quotes" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        paths = sorted(glob.glob(os.path.join(REPO, "results", "*.md")))
    if not paths:
        print("no reports found")
        return 0

    n_bad = 0
    n_skipped = 0
    for path in paths:
        name = os.path.relpath(path, REPO)
        try:
            text = open(path).read()
        except OSError as exc:
            print(f"FAIL  {name}: {exc}")
            n_bad += 1
            continue

        if not is_research_report(text):
            print(f"skip  {name}  (not a research report — no Key Findings/Sources section "
                  f"and fewer than 3 citations)")
            n_skipped += 1
            continue

        errs, warns = check_structure(path, text)
        if do_urls:
            print(f"      {name}")
            e2, w2 = check_urls(text, do_quotes)
            errs += e2
            warns += w2

        if errs:
            n_bad += 1
            print(f"\nFAIL  {name}  ({len(errs)} error(s), {len(warns)} warning(s))")
            for e in errs:
                print(f"        - {e}")
            for w in warns:
                print(f"      ! {w}")
        else:
            print(f"ok    {name}" + (f"  ({len(warns)} warning(s))" if warns else ""))
            for w in warns:
                print(f"      ! {w}")

    checked = len(paths) - n_skipped
    print(f"\n{checked - n_bad}/{checked} reports passed citation checks"
          + (f" ({n_skipped} non-report file(s) skipped)" if n_skipped else ""))
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
