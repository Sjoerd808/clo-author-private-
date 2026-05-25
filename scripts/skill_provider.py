#!/usr/bin/env python3
"""
Cross-repo skill provider interface for clo-author.

Stable invocation modes:
  - partial: run one capability
  - bundle: run a grouped set of capabilities
  - full: run all capabilities in sequence
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


CAPABILITIES = {
    "dashboard",
    "literature",
    "strategy-review",
    "code-audit",
    "quality-gate",
    "peer-review",
}

BUNDLES = {
    "discovery": ["literature"],
    "strategy": ["strategy-review"],
    "execution": ["code-audit", "quality-gate"],
    "review": ["peer-review", "dashboard"],
}


def ensure_absolute_dir(path: str, label: str) -> Path:
    p = Path(path)
    if not p.is_absolute():
        raise ValueError(f"{label} must be an absolute path: {path}")
    if not p.exists() or not p.is_dir():
        raise ValueError(f"{label} does not exist or is not a directory: {path}")
    return p.resolve()


def ensure_within_repo(target_repo: Path, candidate: Path) -> Path:
    c = candidate.resolve()
    try:
        c.relative_to(target_repo)
    except ValueError as exc:
        raise ValueError(f"Path escapes target repo: {candidate}") from exc
    return c


def provider_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_contract(contract_path: Path | None) -> Dict[str, object]:
    if contract_path is None:
        return {}
    if not contract_path.exists():
        raise ValueError(f"Contract file not found: {contract_path}")
    return json.loads(contract_path.read_text())


def resolve_input_paths(
    target_repo: Path, contract: Dict[str, object], capability: str, cli_inputs: List[str]
) -> List[Path]:
    if cli_inputs:
        resolved = [ensure_within_repo(target_repo, (target_repo / p) if not Path(p).is_absolute() else Path(p)) for p in cli_inputs]
        return resolved

    inputs_map = contract.get("inputs", {})
    if not isinstance(inputs_map, dict):
        return []

    value = inputs_map.get(capability)
    if value is None:
        return []

    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        raise ValueError(f"Contract inputs for {capability} must be a string or list")

    resolved = []
    for item in value:
        p = Path(item)
        rp = p if p.is_absolute() else target_repo / p
        resolved.append(ensure_within_repo(target_repo, rp))
    return resolved


def default_output_path(target_repo: Path, capability: str) -> Path:
    reviews = target_repo / "quality_reports" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    mapping = {
        "dashboard": reviews / "provider_dashboard.html",
        "literature": reviews / "provider_literature.html",
        "strategy-review": reviews / "provider_strategy_review.html",
        "code-audit": reviews / "provider_code_audit.html",
        "quality-gate": reviews / "provider_quality_gate.html",
        "peer-review": reviews / "provider_peer_review.html",
    }
    return mapping[capability]


def run_cmd(cmd: List[str]) -> None:
    subprocess.run(cmd, check=True)


def run_capability(
    provider_root: Path,
    target_repo: Path,
    capability: str,
    inputs: List[Path],
    dry_run: bool,
) -> str:
    output = ensure_within_repo(target_repo, default_output_path(target_repo, capability))
    dashboard_script = provider_root / "scripts" / "generate_dashboard.py"
    report_script = provider_root / "scripts" / "generate_html_report.py"

    if capability == "dashboard":
        cmd = [
            sys.executable,
            str(dashboard_script),
            "--project-root",
            str(target_repo),
            "--output",
            str(output),
        ]
    else:
        if not inputs:
            raise ValueError(
                f"Capability {capability} requires input markdown file(s). "
                "Provide --input or a contract file mapping."
            )
        cmd = [sys.executable, str(report_script), capability, *[str(i) for i in inputs], "--output", str(output)]

    if dry_run:
        print("DRY-RUN:", " ".join(cmd))
    else:
        run_cmd(cmd)
    return str(output)


def provider_revision(provider_root: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(provider_root), "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        )
        return out.decode().strip()
    except Exception:
        return "unknown"


def canonicalize_target_dirs(target_repo: Path) -> None:
    (target_repo / "quality_reports" / "reviews").mkdir(parents=True, exist_ok=True)
    (target_repo / "paper" / "figures").mkdir(parents=True, exist_ok=True)
    (target_repo / "paper" / "tables").mkdir(parents=True, exist_ok=True)
    (target_repo / "quality_reports" / "provider").mkdir(parents=True, exist_ok=True)


def build_run_list(mode: str, capability: str | None, bundle: str | None) -> List[str]:
    if mode == "partial":
        if capability is None:
            raise ValueError("--capability is required for partial mode")
        if capability not in CAPABILITIES:
            raise ValueError(f"Unknown capability: {capability}")
        return [capability]
    if mode == "bundle":
        if bundle is None:
            raise ValueError("--bundle is required for bundle mode")
        if bundle not in BUNDLES:
            raise ValueError(f"Unknown bundle: {bundle}")
        return BUNDLES[bundle]
    if mode == "full":
        return ["literature", "strategy-review", "code-audit", "quality-gate", "peer-review", "dashboard"]
    raise ValueError(f"Unknown mode: {mode}")


def write_manifest(
    target_repo: Path, provider_root: Path, mode: str, run_list: List[str], outputs: Dict[str, str], contract_path: Path | None
) -> Path:
    manifest_path = target_repo / "quality_reports" / "provider" / "provider_run_manifest.json"
    payload = {
        "provider_root": str(provider_root),
        "provider_revision": provider_revision(provider_root),
        "target_repo": str(target_repo),
        "mode": mode,
        "run_list": run_list,
        "outputs": outputs,
        "contract": str(contract_path) if contract_path else None,
    }
    manifest_path.write_text(json.dumps(payload, indent=2))
    return manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description="clo-author cross-repo skill provider")
    parser.add_argument("--target-repo", required=True, help="Absolute path to consumer repository")
    parser.add_argument("--mode", required=True, choices=["partial", "bundle", "full"], help="Invocation mode")
    parser.add_argument("--capability", choices=sorted(CAPABILITIES), help="Capability for partial mode")
    parser.add_argument("--bundle", choices=sorted(BUNDLES.keys()), help="Bundle name for bundle mode")
    parser.add_argument(
        "--contract",
        help="Absolute path to contract JSON with input mappings",
    )
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        help="Input file path(s) for report capabilities (absolute or relative to target repo)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    args = parser.parse_args()

    try:
        target_repo = ensure_absolute_dir(args.target_repo, "--target-repo")
        contract_path = Path(args.contract).resolve() if args.contract else None
        if contract_path and not contract_path.is_absolute():
            raise ValueError("--contract must be an absolute path")
        contract = load_contract(contract_path)
        provider_root = provider_root_from_script()
        canonicalize_target_dirs(target_repo)
        run_list = build_run_list(args.mode, args.capability, args.bundle)

        outputs: Dict[str, str] = {}
        for cap in run_list:
            cap_inputs = resolve_input_paths(target_repo, contract, cap, args.input if args.mode == "partial" else [])
            outputs[cap] = run_capability(provider_root, target_repo, cap, cap_inputs, args.dry_run)

        if args.dry_run:
            print("Provider dry-run complete. Manifest not written.")
        else:
            manifest = write_manifest(target_repo, provider_root, args.mode, run_list, outputs, contract_path)
            print(f"Provider run complete. Manifest: {manifest}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
