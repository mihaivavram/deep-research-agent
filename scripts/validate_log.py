#!/usr/bin/env python3
"""Validate research run logs against the schema in REFERENCE.md.

The run-log schema exists so that source reliability can be measured across runs and fed
back into source selection. That only works if the logs are complete and use a consistent
skill vocabulary — a log that invents a skill name is invisible to aggregation.

Usage:
    python3 scripts/validate_log.py                    # validate every log in logs/
    python3 scripts/validate_log.py logs/foo.yaml ...  # validate specific files
    python3 scripts/validate_log.py --quiet            # only report failures

Exit code 0 if all logs valid, 1 otherwise.
"""

import sys
import glob
import os
from datetime import datetime

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required. Run: pip install pyyaml (or use the venv from .env)")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_TOP = [
    "query", "query_type", "depth_tier", "start_time", "end_time", "duration_seconds",
    "report_file", "sources_selected", "sources_succeeded", "sources_failed",
    "total_pages_fetched", "pages_fetch_succeeded", "pages_fetch_failed",
    "fetch_success_rate", "triage_threshold", "pages_passed_triage", "pages_dropped_triage",
    "triage_pass_rate", "requery_rounds", "requery_pages_fetched", "quality_score",
    "research_plan",
]

QUERY_TYPES = {"factual", "opinion", "product", "market", "investment", "how_to",
               "troubleshooting", "recommendation"}
DEPTH_TIERS = {"quick", "standard", "deep"}
STATUSES = {"success", "partial", "no_results", "skipped", "error"}
ERROR_TYPES = {"access_blocked", "rate_limited", "timeout", "empty_content", "parse_error",
               "redirect_error", "server_error", "login_required"}
FALLBACKS = {"google_cache", "wayback", "archive_ph", "google_snippets", "platform_api",
             "alternate_publisher", "none"}

# Pipeline steps are not source skills; they have their own required fields.
PIPELINE_STEPS = {
    "source-triage", "gap-detection", "synthesis", "evidence-ledger", "report-written",
    "pdf-generated", "email-sent", "query-analysis",
}

# Steps that may legitimately carry a phase marker instead of being a distinct skill.
VALID_PHASES = {"initial", "requery", "gap_fill"}


def known_skills():
    """Source skill names are exactly the strategy files in sources/."""
    names = set()
    for path in glob.glob(os.path.join(REPO, "sources", "*.md")):
        base = os.path.basename(path)[:-3]
        if base.upper() == base and "-" in base:   # SOURCE-HEALTH
            continue
        names.add(base)
    return names


SOURCE_SKILLS = known_skills()
ALL_SKILLS = SOURCE_SKILLS | PIPELINE_STEPS


def approx(a, b, tol=0.02):
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def validate(path):
    """Return (errors, warnings) for one log file."""
    errs, warns = [], []
    try:
        with open(path) as fh:
            doc = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        return [f"unparseable YAML: {exc}"], []
    if not isinstance(doc, dict):
        return ["log is not a YAML mapping"], []

    # --- required top-level fields ---
    for key in REQUIRED_TOP:
        if key not in doc:
            errs.append(f"missing required field: {key}")

    # --- enums ---
    if doc.get("query_type") not in QUERY_TYPES and "query_type" in doc:
        errs.append(f"query_type '{doc['query_type']}' not in {sorted(QUERY_TYPES)}")
    if doc.get("depth_tier") not in DEPTH_TIERS and "depth_tier" in doc:
        errs.append(f"depth_tier '{doc['depth_tier']}' not in {sorted(DEPTH_TIERS)}")
    qs = doc.get("quality_score")
    if qs is not None and not (isinstance(qs, int) and 1 <= qs <= 5):
        errs.append(f"quality_score must be an integer 1-5, got {qs!r}")

    # --- computed-field consistency (catches copy-paste and arithmetic drift) ---
    start, end = doc.get("start_time"), doc.get("end_time")
    if start and end:
        try:
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            delta = (datetime.strptime(str(end), fmt) - datetime.strptime(str(start), fmt))
            actual = int(delta.total_seconds())
            if actual < 0:
                errs.append(f"end_time is before start_time ({start} -> {end})")
            elif "duration_seconds" in doc and doc["duration_seconds"] != actual:
                errs.append(
                    f"duration_seconds {doc['duration_seconds']} != end-start ({actual}s)")
        except ValueError:
            errs.append("start_time/end_time must match %Y-%m-%dT%H:%M:%SZ "
                        "(use: date -u +%Y-%m-%dT%H:%M:%SZ)")

    tot, ok = doc.get("total_pages_fetched"), doc.get("pages_fetch_succeeded")
    bad = doc.get("pages_fetch_failed")
    if all(isinstance(v, int) for v in (tot, ok, bad)):
        if ok + bad != tot:
            errs.append(f"pages_fetch_succeeded({ok}) + failed({bad}) != total({tot})")
        if tot and not approx(doc.get("fetch_success_rate"), ok / tot):
            errs.append(f"fetch_success_rate {doc.get('fetch_success_rate')} != "
                        f"{ok}/{tot} = {ok / tot:.2f}")

    passed, dropped = doc.get("pages_passed_triage"), doc.get("pages_dropped_triage")
    if isinstance(passed, int) and isinstance(dropped, int) and (passed + dropped):
        expect = passed / (passed + dropped)
        if not approx(doc.get("triage_pass_rate"), expect):
            errs.append(f"triage_pass_rate {doc.get('triage_pass_rate')} != "
                        f"{passed}/{passed + dropped} = {expect:.2f}")

    sel, succ, fail = (doc.get("sources_selected"), doc.get("sources_succeeded"),
                       doc.get("sources_failed"))
    if all(isinstance(v, int) for v in (sel, succ, fail)) and succ + fail > sel:
        errs.append(f"sources_succeeded({succ}) + failed({fail}) exceeds selected({sel})")

    # --- steps ---
    steps = doc.get("steps")
    if not steps:
        errs.append("no steps recorded")
    for i, step in enumerate(steps or []):
        tag = f"step[{i}]"
        if not isinstance(step, dict):
            errs.append(f"{tag}: not a mapping")
            continue
        skill = step.get("skill")
        tag = f"step[{i}] {skill or '<no skill>'}"
        if not skill:
            errs.append(f"{tag}: missing 'skill'")
        elif skill not in ALL_SKILLS:
            errs.append(
                f"{tag}: unknown skill name — must be a file in sources/ or a pipeline step. "
                f"For follow-up work use the real skill name plus 'phase: requery|gap_fill'")
        if not step.get("timestamp"):
            errs.append(f"{tag}: missing 'timestamp'")
        phase = step.get("phase")
        if phase is not None and phase not in VALID_PHASES:
            errs.append(f"{tag}: phase '{phase}' not in {sorted(VALID_PHASES)}")

        status = step.get("status")
        if status not in STATUSES:
            errs.append(f"{tag}: status '{status}' not in {sorted(STATUSES)}")
            continue

        if skill in PIPELINE_STEPS:
            required = {
                "source-triage": ["pages_scored", "pages_passed", "pages_dropped",
                                  "triage_threshold"],
                "gap-detection": ["gaps_found", "followup_searches"],
                "evidence-ledger": ["claims_extracted"],
            }.get(skill, [])
            if status == "success":
                for field in required:
                    if field not in step:
                        errs.append(f"{tag}: missing '{field}' (required for {skill})")
            if status in {"error", "skipped", "no_results"} and not step.get("reason"):
                errs.append(f"{tag}: status '{status}' requires 'reason'")
            continue

        # source skills
        if status == "skipped":
            if not step.get("reason"):
                errs.append(f"{tag}: skipped requires 'reason'")
            continue
        for field in ("sources_fetched", "queries_run"):
            if field not in step:
                errs.append(f"{tag}: missing '{field}'")
        if status in {"partial", "no_results", "error"} and not step.get("reason"):
            errs.append(f"{tag}: status '{status}' requires 'reason'")
        if status in {"partial", "no_results"}:
            for field in ("fallback_used", "fallback_succeeded"):
                if field not in step:
                    errs.append(f"{tag}: missing '{field}' (required for {status})")
            fb = step.get("fallback_used")
            if fb is not None and fb not in FALLBACKS:
                errs.append(f"{tag}: fallback_used '{fb}' not in {sorted(FALLBACKS)}")
            # The Phase 1 lesson: never give up on a source without trying its API.
            if status == "no_results" and fb in {"google_snippets", "none"}:
                warns.append(f"{tag}: gave up via '{fb}' — was a platform API tried? "
                             f"(pullpush for Reddit, Algolia for HN)")

    # --- errors list ---
    for i, err in enumerate(doc.get("errors") or []):
        tag = f"errors[{i}]"
        if not isinstance(err, dict):
            errs.append(f"{tag}: not a mapping")
            continue
        for field in ("skill", "timestamp", "error_type", "http_status", "url",
                      "fallback_used", "fallback_succeeded", "error"):
            if field not in err:
                errs.append(f"{tag}: missing '{field}' (all 8 fields required, use null "
                            f"if not applicable)")
        et = err.get("error_type")
        if et is not None and et not in ERROR_TYPES:
            errs.append(f"{tag}: error_type '{et}' not in {sorted(ERROR_TYPES)}")
        fb = err.get("fallback_used")
        if fb is not None and fb not in FALLBACKS:
            errs.append(f"{tag}: fallback_used '{fb}' not in {sorted(FALLBACKS)}")

    # --- cross-check: reported failures should have error entries ---
    n_errors = len(doc.get("errors") or [])
    if isinstance(bad, int) and bad > 0 and n_errors == 0:
        errs.append(f"pages_fetch_failed={bad} but 'errors' list is empty — log individual "
                    f"page failures, not just the count")
    if isinstance(bad, int) and bad > n_errors > 0:
        warns.append(f"pages_fetch_failed={bad} but only {n_errors} error entries — "
                     f"each failed URL should get its own entry")

    return errs, warns


def main(argv):
    quiet = "--quiet" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        paths = sorted(glob.glob(os.path.join(REPO, "logs", "*.yaml")))
    if not paths:
        print("no logs found")
        return 0

    n_bad = 0
    total_warns = 0
    for path in paths:
        errs, warns = validate(path)
        total_warns += len(warns)
        name = os.path.relpath(path, REPO)
        if errs:
            n_bad += 1
            print(f"\nFAIL  {name}  ({len(errs)} error(s))")
            for e in errs:
                print(f"        - {e}")
            for w in warns:
                print(f"      ! {w}")
        elif not quiet:
            print(f"ok    {name}" + (f"  ({len(warns)} warning(s))" if warns else ""))
            for w in warns:
                print(f"      ! {w}")

    print(f"\n{len(paths) - n_bad}/{len(paths)} logs valid"
          f"{f', {total_warns} warning(s)' if total_warns else ''}")
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
