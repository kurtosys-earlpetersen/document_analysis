"""Compliance rules engine: load jurisdiction configs and evaluate documents."""

from pathlib import Path
from typing import Any

import yaml

from ..ingestion.models import ExtractedDocument


def load_jurisdiction_config(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_jurisdiction_configs(config_dir: Path) -> dict[str, Path]:
    """Return mapping jurisdiction -> config path."""
    config_dir = Path(config_dir)
    if not config_dir.is_dir():
        return {}
    out = {}
    for f in config_dir.glob("*.yaml"):
        try:
            data = load_jurisdiction_config(f)
            j = data.get("jurisdiction") or data.get("name", f.stem)
            out[str(j).upper()] = f
        except Exception:
            continue
    return out


def run_required_section_rule(text: str, rule: dict) -> tuple[bool, str]:
    keywords = rule.get("keywords") or []
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            return True, f"Found required section keyword: '{kw}'"
    return False, f"Missing required section (keywords: {', '.join(keywords)})"


def run_required_phrase_rule(text: str, rule: dict) -> tuple[bool, str]:
    phrases = rule.get("phrases") or []
    text_lower = text.lower()
    for phrase in phrases:
        if phrase.lower() in text_lower:
            return True, f"Found required phrase: '{phrase[:50]}...'"
    return False, f"Missing required phrase (one of: {len(phrases)} phrases)"


def run_min_length_rule(text: str, rule: dict) -> tuple[bool, str]:
    min_chars = rule.get("min_chars") or 0
    n = len(text.strip())
    if n >= min_chars:
        return True, f"Length {n} >= {min_chars} characters"
    return False, f"Length {n} < {min_chars} characters (min: {min_chars})"


RULE_HANDLERS = {
    "required_section": run_required_section_rule,
    "required_phrase": run_required_phrase_rule,
    "min_length": run_min_length_rule,
}


def evaluate_rule(doc: ExtractedDocument, rule: dict) -> dict[str, Any]:
    text = doc.raw_text
    rule_type = rule.get("type") or "required_section"
    handler = RULE_HANDLERS.get(rule_type)
    if not handler:
        return {
            "rule_id": rule.get("id"),
            "passed": None,
            "message": f"Unknown rule type: {rule_type}",
            "severity": rule.get("severity", "medium"),
        }
    passed, message = handler(text, rule)
    return {
        "rule_id": rule.get("id"),
        "name": rule.get("name"),
        "passed": passed,
        "message": message,
        "severity": rule.get("severity", "medium"),
    }


def run_compliance(doc: ExtractedDocument, jurisdiction: str, config_dir: Path | None = None) -> dict[str, Any]:
    if config_dir is None:
        _root = Path(__file__).resolve().parent.parent.parent.parent
        config_dir = _root / "config" / "jurisdictions"
    configs = find_jurisdiction_configs(config_dir)
    j = jurisdiction.upper().strip()
    if j not in configs:
        return {
            "jurisdiction": jurisdiction,
            "error": f"No config found for jurisdiction: {jurisdiction}",
            "results": [],
            "passed_count": 0,
            "failed_count": 0,
        }
    config = load_jurisdiction_config(configs[j])
    rules = config.get("rules") or []
    results = [evaluate_rule(doc, r) for r in rules]
    passed = sum(1 for r in results if r.get("passed") is True)
    failed = sum(1 for r in results if r.get("passed") is False)
    return {
        "jurisdiction": jurisdiction,
        "config_name": config.get("name"),
        "results": results,
        "passed_count": passed,
        "failed_count": failed,
        "total_count": len(rules),
        "compliance_score": (passed / len(rules) * 100) if rules else 100.0,
    }
