PYTHON ?= python3

.PHONY: validate dashboard report-peer-review report-code-audit report-strategy-review report-quality-gate report-literature copilot-pre-edit copilot-post-edit

validate:
	$(PYTHON) scripts/generate_dashboard.py --help
	$(PYTHON) scripts/generate_html_report.py --help

dashboard:
	$(PYTHON) scripts/generate_dashboard.py

report-peer-review:
	$(PYTHON) scripts/generate_html_report.py peer-review

report-code-audit:
	$(PYTHON) scripts/generate_html_report.py code-audit

report-strategy-review:
	$(PYTHON) scripts/generate_html_report.py strategy-review

report-quality-gate:
	$(PYTHON) scripts/generate_html_report.py quality-gate

report-literature:
	$(PYTHON) scripts/generate_html_report.py literature

copilot-pre-edit:
	@bash .claude/hooks/protect-files.sh
	@$(PYTHON) .claude/hooks/session-guard.py

copilot-post-edit:
	@bash .claude/hooks/post-edit-lint.sh
