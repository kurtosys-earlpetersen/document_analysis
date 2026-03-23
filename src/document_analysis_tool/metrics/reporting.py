"""Metrics storage and reporting."""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class AnalysisRun:
    document_path: str
    jurisdiction: str
    timestamp: str
    compliance_score: float
    accessibility_score: float
    compliance_passed: int
    compliance_failed: int
    accessibility_passed: int
    accessibility_failed: int
    compliance_details: list[dict]
    accessibility_details: list[dict]
    error: str | None = None


def store_run(output_path: Path, run: AnalysisRun) -> None:
    """Append a run to a JSONL file or write a single JSON file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(run)
    # Use .jsonl to append each run (batch); .json overwrites with single run
    if output_path.suffix.lower() == ".jsonl":
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, default=str) + "\n")
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)


def build_run(
    document_path: Path,
    jurisdiction: str,
    compliance_result: dict,
    accessibility_result: dict,
    error: str | None = None,
) -> AnalysisRun:
    return AnalysisRun(
        document_path=str(document_path),
        jurisdiction=jurisdiction,
        timestamp=datetime.utcnow().isoformat() + "Z",
        compliance_score=compliance_result.get("compliance_score") or 0.0,
        accessibility_score=accessibility_result.get("accessibility_score") or 0.0,
        compliance_passed=compliance_result.get("passed_count") or 0,
        compliance_failed=compliance_result.get("failed_count") or 0,
        accessibility_passed=accessibility_result.get("passed_count") or 0,
        accessibility_failed=accessibility_result.get("failed_count") or 0,
        compliance_details=compliance_result.get("results") or [],
        accessibility_details=accessibility_result.get("results") or [],
        error=error,
    )


def format_summary(run: AnalysisRun) -> str:
    lines = [
        f"Document: {run.document_path}",
        f"Jurisdiction: {run.jurisdiction}",
        f"Compliance: {run.compliance_score:.1f}% ({run.compliance_passed}/{run.compliance_passed + run.compliance_failed} passed)",
        f"Accessibility: {run.accessibility_score:.1f}% ({run.accessibility_passed}/{run.accessibility_passed + run.accessibility_failed} passed)",
    ]
    if run.error:
        lines.append(f"Error: {run.error}")
    return "\n".join(lines)
