# Deep Research Agent — verification entry points.
#
# The quality gates in CLAUDE.md were previously graded by eyeballing, which is why gate 3
# ("every claim carries a citation") never actually failed. These targets make the checks
# mechanical: one command, not remembered discipline.
#
#   make verify        run every offline check (fast, no network)
#   make verify-full   also resolve citation URLs and verify quotes (slow, network)
#
# Python comes from the virtualenv named in .env (VIRTUAL_ENV), same as the PDF pipeline.

SHELL := /bin/bash
PY := set -a && source .env && set +a && "$$VIRTUAL_ENV/bin/python3"

.PHONY: help verify verify-latest verify-full logs citations citations-full health health-check pdf-smoke clean-pyc

help:
	@echo "make verify-latest — check ONLY the newest report + log (use after a research run)"
	@echo "make verify        — audit everything: all logs, all reports, health freshness, PDF"
	@echo "make verify-full   — verify + resolve every citation URL and verify quotes (network)"
	@echo "make logs          — validate logs/*.yaml against the run-log schema"
	@echo "make citations     — structural citation checks on results/*.md"
	@echo "make citations-full— citation checks incl. URL resolution and quote verification"
	@echo "make health        — regenerate sources/SOURCE-HEALTH.md from logs + curated facts"
	@echo "make health-check  — fail if SOURCE-HEALTH.md is stale"
	@echo "make pdf-smoke     — render a throwaway markdown file to PDF"
	@echo ""
	@echo "Note: 'make verify' audits the full history, which includes reports and logs written"
	@echo "before these checks existed. Use 'verify-latest' as the per-run gate."

# The per-run gate: newest report and newest log only, so a fresh failure is unambiguous.
verify-latest:
	@rc=0; \
	log=$$(ls -t logs/*.yaml 2>/dev/null | head -1); \
	rep=$$(ls -t results/*.md 2>/dev/null | head -1); \
	if [ -n "$$log" ]; then echo "── log: $$log"; $(PY) scripts/validate_log.py "$$log" || rc=1; \
	else echo "no logs found"; fi; \
	echo; \
	if [ -n "$$rep" ]; then echo "── report: $$rep"; $(PY) scripts/check_citations.py "$$rep" || rc=1; \
	else echo "no reports found"; fi; \
	echo; \
	$(MAKE) --no-print-directory health-check || rc=1; \
	echo; \
	if [ $$rc -eq 0 ]; then echo "verify-latest: passed"; else echo "verify-latest: FAILURES above"; fi; \
	exit $$rc

# Offline gate. Runs everything, then fails if any check failed, so one broken check
# does not hide the others.
verify:
	@rc=0; \
	echo "── run logs ─────────────────────────────────────────"; \
	$(MAKE) --no-print-directory logs || rc=1; \
	echo; echo "── citations (structural) ───────────────────────────"; \
	$(MAKE) --no-print-directory citations || rc=1; \
	echo; echo "── source health freshness ──────────────────────────"; \
	$(MAKE) --no-print-directory health-check || rc=1; \
	echo; echo "── pdf pipeline ─────────────────────────────────────"; \
	$(MAKE) --no-print-directory pdf-smoke || rc=1; \
	echo; \
	if [ $$rc -eq 0 ]; then echo "verify: all checks passed"; \
	else echo "verify: FAILURES above"; fi; \
	exit $$rc

verify-full:
	@rc=0; \
	echo "── run logs ─────────────────────────────────────────"; \
	$(MAKE) --no-print-directory logs || rc=1; \
	echo; echo "── citations (incl. network) ────────────────────────"; \
	$(MAKE) --no-print-directory citations-full || rc=1; \
	echo; echo "── source health freshness ──────────────────────────"; \
	$(MAKE) --no-print-directory health-check || rc=1; \
	echo; echo "── pdf pipeline ─────────────────────────────────────"; \
	$(MAKE) --no-print-directory pdf-smoke || rc=1; \
	echo; \
	if [ $$rc -eq 0 ]; then echo "verify-full: all checks passed"; \
	else echo "verify-full: FAILURES above"; fi; \
	exit $$rc

logs:
	@$(PY) scripts/validate_log.py --quiet

citations:
	@$(PY) scripts/check_citations.py

citations-full:
	@$(PY) scripts/check_citations.py --check-quotes

health:
	@$(PY) scripts/derive_health.py

health-check:
	@$(PY) scripts/derive_health.py --check

# Confirms the whole markdown->PDF path works, including the emoji transliteration step.
pdf-smoke:
	@tmp=$$(mktemp -d); \
	printf '# PDF smoke test\n\nStatus: pass ✅ warn ⚠️ target 🎯 play ▶\n\n| Col | Val |\n|---|---|\n| a | 1 |\n' > $$tmp/smoke.md; \
	if $(PY) scripts/md_to_pdf.py "$$tmp/smoke.md" >/dev/null 2>&1 && [ -s "$$tmp/smoke.pdf" ]; then \
		echo "ok    pdf pipeline (emoji + tables rendered, $$(wc -c < $$tmp/smoke.pdf | tr -d ' ') bytes)"; \
		rm -rf $$tmp; \
	else \
		echo "FAIL  pdf pipeline — scripts/md_to_pdf.py did not produce a PDF"; \
		rm -rf $$tmp; exit 1; \
	fi

clean-pyc:
	@rm -rf scripts/__pycache__
