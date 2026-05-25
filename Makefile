PYTHON ?= python3
TARGET_REPO ?=
MODE ?=
CAPABILITY ?=
BUNDLE ?=
CONTRACT ?=
INPUT ?=
OUT ?=
FILE ?=
FILES ?=

.PHONY: validate dashboard report-peer-review report-code-audit report-strategy-review report-quality-gate report-literature copilot-pre-edit copilot-post-edit codex-pre-edit codex-post-edit skill-partial skill-bundle skill-full skill-health

validate:
	$(PYTHON) scripts/generate_dashboard.py --help
	$(PYTHON) scripts/generate_html_report.py --help
	$(PYTHON) scripts/skill_provider.py --help

dashboard:
	$(PYTHON) scripts/generate_dashboard.py

report-peer-review:
	@test -n "$(FILES)" || (echo "Set FILES='file1.md file2.md file3.md'" && exit 1)
	$(PYTHON) scripts/generate_html_report.py peer-review $(FILES) $(if $(OUT),--output "$(OUT)")

report-code-audit:
	@test -n "$(FILE)" || (echo "Set FILE=path/to/code_audit.md" && exit 1)
	$(PYTHON) scripts/generate_html_report.py code-audit "$(FILE)" $(if $(OUT),--output "$(OUT)")

report-strategy-review:
	@test -n "$(FILE)" || (echo "Set FILE=path/to/strategy_review.md" && exit 1)
	$(PYTHON) scripts/generate_html_report.py strategy-review "$(FILE)" $(if $(OUT),--output "$(OUT)")

report-quality-gate:
	@test -n "$(FILE)" || (echo "Set FILE=path/to/quality_gate_summary.md" && exit 1)
	$(PYTHON) scripts/generate_html_report.py quality-gate "$(FILE)" $(if $(OUT),--output "$(OUT)")

report-literature:
	@test -n "$(FILE)" || (echo "Set FILE=path/to/annotated_bibliography.md" && exit 1)
	$(PYTHON) scripts/generate_html_report.py literature "$(FILE)" $(if $(OUT),--output "$(OUT)")

copilot-pre-edit:
	@bash .claude/hooks/protect-files.sh
	@$(PYTHON) .claude/hooks/session-guard.py

copilot-post-edit:
	@bash .claude/hooks/post-edit-lint.sh

codex-pre-edit: copilot-pre-edit

codex-post-edit: copilot-post-edit

skill-partial:
	@test -n "$(TARGET_REPO)" || (echo "Set TARGET_REPO=/absolute/path/to/consumer-repo" && exit 1)
	@test -n "$(CAPABILITY)" || (echo "Set CAPABILITY=dashboard|literature|strategy-review|code-audit|quality-gate|peer-review" && exit 1)
	$(PYTHON) scripts/skill_provider.py --target-repo "$(TARGET_REPO)" --mode partial --capability "$(CAPABILITY)" $(if $(CONTRACT),--contract "$(CONTRACT)") $(if $(INPUT),--input "$(INPUT)")

skill-bundle:
	@test -n "$(TARGET_REPO)" || (echo "Set TARGET_REPO=/absolute/path/to/consumer-repo" && exit 1)
	@test -n "$(BUNDLE)" || (echo "Set BUNDLE=discovery|strategy|execution|review" && exit 1)
	$(PYTHON) scripts/skill_provider.py --target-repo "$(TARGET_REPO)" --mode bundle --bundle "$(BUNDLE)" $(if $(CONTRACT),--contract "$(CONTRACT)")

skill-full:
	@test -n "$(TARGET_REPO)" || (echo "Set TARGET_REPO=/absolute/path/to/consumer-repo" && exit 1)
	$(PYTHON) scripts/skill_provider.py --target-repo "$(TARGET_REPO)" --mode full $(if $(CONTRACT),--contract "$(CONTRACT)")

skill-health:
	@test -n "$(TARGET_REPO)" || (echo "Set TARGET_REPO=/absolute/path/to/consumer-repo" && exit 1)
	$(PYTHON) scripts/skill_provider.py --target-repo "$(TARGET_REPO)" --mode partial --capability dashboard --dry-run
