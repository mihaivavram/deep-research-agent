#!/usr/bin/env python3
"""Regenerate sources/SOURCE-HEALTH.md from measured logs + curated facts.

Two inputs, deliberately separated:

  logs/*.yaml              -> MEASURED: per-source last-5-run outcomes and success rate
  sources/source-health.yaml -> CURATED: which access paths work, which are dead, gotchas

Previously SOURCE-HEALTH.md was hand-written prose, so its conclusions drifted from what the
logs actually measured (Reddit was described as "fully unavailable" while a working API
existed). Deriving the measured half mechanically keeps the numbers honest; the curated half
still needs a human/agent to write, because "this path works" is knowledge, not a statistic.

Usage:
    python3 scripts/derive_health.py            # rewrite sources/SOURCE-HEALTH.md
    python3 scripts/derive_health.py --check    # exit 1 if the file is stale (no write)
    python3 scripts/derive_health.py --stdout   # print, don't write
"""

import sys
import os
import glob

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required. Run: pip install pyyaml (or use the venv from .env)")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(REPO, "logs")
CURATED = os.path.join(REPO, "sources", "source-health.yaml")
OUTPUT = os.path.join(REPO, "sources", "SOURCE-HEALTH.md")

WINDOW = 5   # how many recent runs to report per source

# status -> (health code, credit toward success rate)
CODE = {
    "success":    ("S", 1.0),
    "partial":    ("P", 0.5),
    "no_results": ("F", 0.0),
    "error":      ("F", 0.0),
}
PIPELINE = {"source-triage", "gap-detection", "synthesis", "evidence-ledger",
            "report-written", "pdf-generated", "email-sent", "query-analysis"}


def load_runs():
    """Return logs sorted oldest->newest by start_time, falling back to mtime."""
    runs = []
    for path in glob.glob(os.path.join(LOGS, "*.yaml")):
        try:
            with open(path) as fh:
                doc = yaml.safe_load(fh)
        except yaml.YAMLError:
            continue
        if not isinstance(doc, dict):
            continue
        key = str(doc.get("start_time") or "") or f"~{os.path.getmtime(path)}"
        runs.append((key, os.path.basename(path), doc))
    runs.sort(key=lambda r: r[0])
    return runs


def measure(runs):
    """source -> list of (code, run_name) for the last WINDOW runs that attempted it."""
    history = {}
    for _, name, doc in runs:
        for step in doc.get("steps") or []:
            if not isinstance(step, dict):
                continue
            skill = step.get("skill")
            if not skill or skill in PIPELINE:
                continue
            # A skipped source was not attempted — it is not evidence of health.
            if step.get("status") == "skipped":
                continue
            # Re-query / gap-fill passes are part of the same run, not separate evidence.
            if step.get("phase") in {"requery", "gap_fill"}:
                continue
            entry = CODE.get(step.get("status"))
            if entry:
                history.setdefault(skill, []).append((entry[0], name))
    return {k: v[-WINDOW:] for k, v in history.items()}


def rate(codes):
    credit = sum(CODE[{"S": "success", "P": "partial", "F": "no_results"}[c]][1]
                 for c in codes)
    return credit, len(codes)


def bullets(items, prefix):
    out = []
    for item in items or []:
        out.append(f"{prefix}{str(item).strip()}")
    return out


def render(curated, measured):
    latest = max((r[0] for r in load_runs()), default="unknown")
    L = []
    A = L.append
    A("# Source Health Registry")
    A("")
    A("> **GENERATED FILE — do not hand-edit.**")
    A("> Measured columns come from `logs/*.yaml`; access-path facts come from")
    A("> `sources/source-health.yaml`. Regenerate with `python3 scripts/derive_health.py`.")
    A("> To record a newly-discovered access path, edit `sources/source-health.yaml`")
    A("> **and** the relevant `sources/<skill>.md` strategy file, then regenerate.")
    A("")
    A(f"Runs analyzed: {len(load_runs())} · most recent run start: {latest}")
    A("")
    A("Status codes: `S` = success · `P` = partial (snippets/fallback only) · `F` = failure")
    A("")

    A("## Measured reliability")
    A("")
    A("| Source | Last 5 attempts | Success rate | Tier |")
    A("|---|---|---|---|")
    src = curated.get("sources") or {}
    # Sort: worst success rate first — the ones needing attention lead.
    def sort_key(name):
        hist = measured.get(name)
        if not hist:
            return (2, name)
        credit, n = rate([c for c, _ in hist])
        return (0, credit / n, name)
    for name in sorted(set(src) | set(measured), key=sort_key):
        hist = measured.get(name) or []
        codes = [c for c, _ in hist]
        tier = (src.get(name) or {}).get("tier", "—")
        if codes:
            credit, n = rate(codes)
            pretty = f"{credit:g}/{n}"
            pct = f" ({100 * credit / n:.0f}%)"
        else:
            pretty, pct = "—", ""
        A(f"| {name} | {' '.join(codes) or '—'} | {pretty}{pct} | {tier} |")
    A("")

    A("## Access paths per source")
    A("")
    for name in sorted(src):
        info = src[name] or {}
        works, dead = info.get("works") or [], info.get("dead") or []
        notes, lv = info.get("notes"), info.get("last_verified")
        if not (works or dead or notes):
            continue
        A(f"### {name}")
        if lv:
            A(f"*last verified: {lv}*")
        A("")
        if works:
            A("**Works:**")
            A("")
            for line in bullets(works, "- "):
                A(line)
            A("")
        if dead:
            A("**Dead — do not budget fetches:**")
            A("")
            for line in bullets(dead, "- "):
                A(line)
            A("")
        if notes:
            A(f"**Notes:** {str(notes).strip()}")
            A("")

    A("## Environment-level blocks (not source failures)")
    A("")
    A("Hosts refused by the client itself. No fallback rung can rescue these.")
    A("")
    A("| Host | Status | Impact |")
    A("|---|---|---|")
    for blk in curated.get("environment_blocks") or []:
        A(f"| `{blk.get('host')}` | {blk.get('status')} | {blk.get('impact', '')} |")
    A("")

    A("## Working fallback chain in this environment")
    A("")
    for i, rung in enumerate(curated.get("working_fallback_chain") or [], 1):
        A(f"{i}. {rung}")
    A("")

    A("## Cross-cutting lessons")
    A("")
    for lesson in curated.get("cross_cutting_lessons") or []:
        A(f"- **{lesson.get('id')}** (added {lesson.get('added', 'n/a')}) — "
          f"{str(lesson.get('lesson', '')).strip()}")
    A("")
    return "\n".join(L) + "\n"


def main(argv):
    with open(CURATED) as fh:
        curated = yaml.safe_load(fh) or {}
    runs = load_runs()
    if not runs:
        print("no logs found — nothing to derive")
        return 0
    text = render(curated, measure(runs))

    if "--stdout" in argv:
        sys.stdout.write(text)
        return 0
    if "--check" in argv:
        existing = open(OUTPUT).read() if os.path.exists(OUTPUT) else ""
        if existing != text:
            print("SOURCE-HEALTH.md is stale — run: python3 scripts/derive_health.py")
            return 1
        print("SOURCE-HEALTH.md is current")
        return 0

    with open(OUTPUT, "w") as fh:
        fh.write(text)
    print(f"wrote {os.path.relpath(OUTPUT, REPO)} "
          f"({len(runs)} runs, {len(measure(runs))} sources with measured history)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
