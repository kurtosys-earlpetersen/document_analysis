"""
Comprehensive accessibility and assistive-technology checks.
Aligned with WCAG 2.1/2.2, PDF/UA, Section 508, EN 301 549, and
the accessibility requirements from the Document Benchmarking Project.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..ingestion.models import ExtractedDocument


@dataclass
class AccessibilityFinding:
    category: str
    check_id: str
    name: str
    passed: bool
    severity: str  # "critical", "major", "minor"
    message: str
    standard: str  # "WCAG 2.1", "PDF/UA", etc.
    wcag_criterion: str = ""
    details: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_heading_presence(doc: ExtractedDocument) -> AccessibilityFinding:
    headings = doc.get_headings()
    return AccessibilityFinding(
        category="Structure",
        check_id="heading_presence",
        name="Document has headings",
        passed=len(headings) >= 1,
        severity="critical",
        message=f"Found {len(headings)} heading(s)" if headings else "No headings — screen readers cannot navigate the document",
        standard="WCAG 2.1",
        wcag_criterion="1.3.1 Info and Relationships",
    )


def check_heading_hierarchy(doc: ExtractedDocument) -> AccessibilityFinding:
    levels = [b.level for b in doc.blocks if b.kind == "heading" and b.level is not None]
    issues: list[str] = []
    if levels:
        prev = 0
        for lvl in levels:
            if lvl > prev + 1:
                issues.append(f"Heading skip: H{prev} → H{lvl}")
            prev = lvl
    return AccessibilityFinding(
        category="Structure",
        check_id="heading_hierarchy",
        name="Heading hierarchy is logical",
        passed=len(issues) == 0,
        severity="major",
        message="Valid heading order" if not issues else "; ".join(issues[:3]),
        standard="WCAG 2.1",
        wcag_criterion="1.3.1 Info and Relationships",
        details=issues,
    )


def check_images_alt_text(doc: ExtractedDocument) -> AccessibilityFinding:
    images = doc.get_images()
    if not images:
        return AccessibilityFinding(
            category="Text Alternatives",
            check_id="images_alt_text",
            name="Images have alt text",
            passed=True,
            severity="critical",
            message="No images detected",
            standard="WCAG 2.1",
            wcag_criterion="1.1.1 Non-text Content",
        )
    missing = [i for i in images if not getattr(i, "alt_text", None) or not str(i.alt_text).strip()]
    return AccessibilityFinding(
        category="Text Alternatives",
        check_id="images_alt_text",
        name="Images have alt text",
        passed=len(missing) == 0,
        severity="critical",
        message=f"All {len(images)} image(s) have alt text" if not missing else f"{len(missing)} of {len(images)} image(s) missing alt text",
        standard="WCAG 2.1",
        wcag_criterion="1.1.1 Non-text Content",
    )


def check_document_structure(doc: ExtractedDocument) -> AccessibilityFinding:
    block_types = set(b.kind for b in doc.blocks)
    has_variety = len(block_types) >= 2 and len(doc.blocks) >= 3
    return AccessibilityFinding(
        category="Structure",
        check_id="document_structure",
        name="Document has semantic structure",
        passed=has_variety,
        severity="major",
        message=f"{len(doc.blocks)} blocks across {len(block_types)} types" if has_variety else "Weak structure — may affect screen readers and navigation",
        standard="PDF/UA",
        wcag_criterion="1.3.1 Info and Relationships",
    )


def check_reading_order(doc: ExtractedDocument) -> AccessibilityFinding:
    # Heuristic: headings should appear before their content blocks
    headings = [i for i, b in enumerate(doc.blocks) if b.kind == "heading"]
    has_logical_order = len(headings) > 0 and headings[0] < len(doc.blocks) // 2
    return AccessibilityFinding(
        category="Structure",
        check_id="reading_order",
        name="Logical reading order",
        passed=has_logical_order or len(doc.blocks) < 3,
        severity="major",
        message="Reading order appears logical" if has_logical_order else "First heading appears late — reading order may be non-sequential",
        standard="PDF/UA",
        wcag_criterion="1.3.2 Meaningful Sequence",
    )


def check_table_structure(doc: ExtractedDocument) -> AccessibilityFinding:
    tables = [b for b in doc.blocks if b.kind == "table"]
    if not tables:
        return AccessibilityFinding(
            category="Structure",
            check_id="table_structure",
            name="Tables have proper structure",
            passed=True,
            severity="major",
            message="No tables detected",
            standard="WCAG 2.1",
            wcag_criterion="1.3.1 Info and Relationships",
        )
    # Check if tables have header-like first row
    issues: list[str] = []
    for i, t in enumerate(tables):
        rows_data = t.metadata.get("rows", 0)
        if rows_data and rows_data < 2:
            issues.append(f"Table {i+1}: single row — may lack header")
    return AccessibilityFinding(
        category="Structure",
        check_id="table_structure",
        name="Tables have proper structure",
        passed=len(issues) == 0,
        severity="major",
        message=f"{len(tables)} table(s) with structure" if not issues else "; ".join(issues),
        standard="WCAG 2.1",
        wcag_criterion="1.3.1 Info and Relationships",
        details=issues,
    )


def check_colour_contrast_signals(doc: ExtractedDocument) -> AccessibilityFinding:
    # Cannot measure actual colours from text extraction,
    # but flag if the document has content (a reminder to check manually).
    return AccessibilityFinding(
        category="Visual",
        check_id="colour_contrast",
        name="Colour contrast (manual check required)",
        passed=True,  # advisory
        severity="major",
        message="Automated contrast check not available for this format — manual verification recommended (4.5:1 normal text, 3:1 large text)",
        standard="WCAG 2.1",
        wcag_criterion="1.4.3 Contrast (Minimum)",
    )


def check_plain_language(doc: ExtractedDocument) -> AccessibilityFinding:
    words = doc.raw_text.split()
    if not words:
        return AccessibilityFinding(
            category="Cognitive",
            check_id="plain_language",
            name="Plain language usage",
            passed=False,
            severity="minor",
            message="No content to assess",
            standard="WCAG 2.1",
            wcag_criterion="3.1.5 Reading Level",
        )
    sentences = re.split(r"[.!?]+", doc.raw_text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    avg_len = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    long_words = sum(1 for w in words if len(w) > 14)
    long_word_pct = long_words / len(words) * 100

    passed = avg_len <= 22 and long_word_pct <= 8
    details: list[str] = []
    if avg_len > 22:
        details.append(f"Average sentence length: {avg_len:.0f} words (target: ≤22)")
    if long_word_pct > 8:
        details.append(f"Complex words: {long_word_pct:.1f}% (target: ≤8%)")

    return AccessibilityFinding(
        category="Cognitive",
        check_id="plain_language",
        name="Plain language usage",
        passed=passed,
        severity="minor",
        message=f"Avg sentence: {avg_len:.0f} words, complex words: {long_word_pct:.1f}%" if words else "No content",
        standard="WCAG 2.1",
        wcag_criterion="3.1.5 Reading Level",
        details=details,
    )


def check_document_language(doc: ExtractedDocument) -> AccessibilityFinding:
    has_lang = bool(doc.language and doc.language.strip())
    return AccessibilityFinding(
        category="Structure",
        check_id="document_language",
        name="Document language defined",
        passed=has_lang or doc.format == "pdf",  # PDF metadata often not extracted
        severity="major",
        message=f"Language: {doc.language}" if has_lang else "Language metadata not detected (check PDF properties)",
        standard="WCAG 2.1",
        wcag_criterion="3.1.1 Language of Page",
    )


def check_link_text(doc: ExtractedDocument) -> AccessibilityFinding:
    text_lower = doc.raw_text.lower()
    bad_links = ["click here", "read more", "here", "link", "more info"]
    found = [lk for lk in bad_links if lk in text_lower]
    return AccessibilityFinding(
        category="Navigation",
        check_id="link_text",
        name="Descriptive link text",
        passed=len(found) == 0,
        severity="minor",
        message="No generic link text found" if not found else f"Generic link text detected: {', '.join(found)}",
        standard="WCAG 2.1",
        wcag_criterion="2.4.4 Link Purpose",
        details=found,
    )


def check_risk_warnings_accessible(doc: ExtractedDocument) -> AccessibilityFinding:
    text_lower = doc.raw_text.lower()
    risk_terms = ["risk warning", "capital at risk", "risk of loss", "past performance"]
    found = [t for t in risk_terms if t in text_lower]
    return AccessibilityFinding(
        category="Financial Services",
        check_id="risk_warnings",
        name="Risk warnings are text-based (not image-only)",
        passed=len(found) > 0,
        severity="critical",
        message=f"Risk warnings found as text: {', '.join(found[:3])}" if found else "No risk warning text detected — may be embedded as image or missing",
        standard="EN 301 549 / FCA",
        wcag_criterion="1.1.1 Non-text Content",
    )


def check_chart_accessibility(doc: ExtractedDocument) -> AccessibilityFinding:
    images = doc.get_images()
    # Financial docs often have charts as images
    if len(images) > 2:
        return AccessibilityFinding(
            category="Financial Services",
            check_id="chart_accessibility",
            name="Charts / graphs have text alternatives",
            passed=False,
            severity="major",
            message=f"Document has {len(images)} images — charts should have data tables or long descriptions as alternatives",
            standard="WCAG 2.1",
            wcag_criterion="1.1.1 Non-text Content",
        )
    return AccessibilityFinding(
        category="Financial Services",
        check_id="chart_accessibility",
        name="Charts / graphs have text alternatives",
        passed=True,
        severity="major",
        message="Few or no chart images detected",
        standard="WCAG 2.1",
        wcag_criterion="1.1.1 Non-text Content",
    )


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_heading_presence,
    check_heading_hierarchy,
    check_images_alt_text,
    check_document_structure,
    check_reading_order,
    check_table_structure,
    check_colour_contrast_signals,
    check_plain_language,
    check_document_language,
    check_link_text,
    check_risk_warnings_accessible,
    check_chart_accessibility,
]


def run_accessibility(doc: ExtractedDocument) -> dict:
    """Run all accessibility and assistive-tech checks."""
    findings: list[AccessibilityFinding] = [check(doc) for check in ALL_CHECKS]

    results = []
    for f in findings:
        results.append({
            "category": f.category,
            "check": f.check_id,
            "name": f.name,
            "passed": f.passed,
            "severity": f.severity,
            "message": f.message,
            "standard": f.standard,
            "wcag_criterion": f.wcag_criterion,
            "details": f.details,
        })

    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    score = round(passed / total * 100, 1) if total else 100.0

    # Severity breakdown
    critical_fails = sum(1 for r in results if not r["passed"] and r["severity"] == "critical")
    major_fails = sum(1 for r in results if not r["passed"] and r["severity"] == "major")
    minor_fails = sum(1 for r in results if not r["passed"] and r["severity"] == "minor")

    return {
        "results": results,
        "passed_count": passed,
        "failed_count": total - passed,
        "total_count": total,
        "accessibility_score": score,
        "critical_failures": critical_fails,
        "major_failures": major_fails,
        "minor_failures": minor_fails,
    }
