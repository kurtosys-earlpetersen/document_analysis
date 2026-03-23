"""
Benchmarking scoring engine — 5-pillar comparison framework + 6-dimension
evaluation aligned with the Document Benchmarking Project.

5 Pillars: Completeness, Consistency, Compliance, Quality, Data Integrity
6 Dimensions: Clarity, Transparency, Design, Accessibility, Compliance, Usability

Maturity scale: 1 = Basic, 2 = Developing, 3 = Competitive, 4 = Advanced, 5 = Best-in-Class
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass, field
from typing import Any

from ..ingestion.models import ExtractedDocument


MATURITY_LABELS = {5: "Best-in-Class", 4: "Advanced", 3: "Competitive", 2: "Developing", 1: "Basic"}


@dataclass
class DimensionScore:
    dimension: str
    score: float
    max_score: float = 5.0
    details: list[dict[str, Any]] = field(default_factory=list)

    @property
    def label(self) -> str:
        for threshold in sorted(MATURITY_LABELS.keys(), reverse=True):
            if self.score >= threshold - 0.5:
                return MATURITY_LABELS[threshold]
        return "Basic"

    @property
    def colour(self) -> str:
        if self.score >= 4.5:
            return "#10b981"
        if self.score >= 3.5:
            return "#22c55e"
        if self.score >= 2.5:
            return "#eab308"
        if self.score >= 1.5:
            return "#f97316"
        return "#ef4444"


@dataclass
class PillarScore:
    pillar: str
    score: float
    max_score: float = 100.0
    details: list[dict[str, Any]] = field(default_factory=list)

    @property
    def label(self) -> str:
        if self.score >= 90:
            return "Best-in-Class"
        if self.score >= 75:
            return "Advanced"
        if self.score >= 50:
            return "Competitive"
        if self.score >= 25:
            return "Developing"
        return "Basic"


@dataclass
class BenchmarkResult:
    dimensions: dict[str, DimensionScore] = field(default_factory=dict)
    pillars: dict[str, PillarScore] = field(default_factory=dict)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    overall_dimension_score: float = 0.0
    overall_pillar_score: float = 0.0

    @property
    def overall_score(self) -> float:
        if not self.dimensions:
            return 0.0
        return round(statistics.mean(d.score for d in self.dimensions.values()), 1)


# ---------------------------------------------------------------------------
# Dimension scorers
# ---------------------------------------------------------------------------

def _avg_sentence_length(text: str) -> float:
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 3]
    if not sentences:
        return 0.0
    return statistics.mean(len(s.split()) for s in sentences)


def _long_word_ratio(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    return sum(1 for w in words if len(w) > 12) / len(words)


def score_clarity(doc: ExtractedDocument) -> DimensionScore:
    details: list[dict] = []
    components: list[float] = []

    avg_sent = _avg_sentence_length(doc.raw_text)
    s = 5.0 if avg_sent <= 15 else 4.0 if avg_sent <= 20 else 3.0 if avg_sent <= 25 else 2.0 if avg_sent <= 35 else 1.0
    details.append({"metric": "Avg sentence length", "value": f"{avg_sent:.0f} words", "sub_score": s})
    components.append(s)

    lwr = _long_word_ratio(doc.raw_text)
    s = 5.0 if lwr <= 0.03 else 4.0 if lwr <= 0.06 else 3.0 if lwr <= 0.10 else 2.0 if lwr <= 0.15 else 1.0
    details.append({"metric": "Complex word ratio", "value": f"{lwr*100:.1f}%", "sub_score": s})
    components.append(s)

    word_count = len(doc.raw_text.split())
    s = 5.0 if word_count >= 300 else 4.0 if word_count >= 150 else 3.0 if word_count >= 50 else 2.0
    details.append({"metric": "Word count", "value": f"{word_count:,}", "sub_score": s})
    components.append(s)

    return DimensionScore(dimension="Clarity", score=round(statistics.mean(components), 1), details=details)


DISCLOSURE_KEYWORDS = [
    "risk", "disclaimer", "warning", "past performance", "guarantee",
    "loss", "capital at risk", "tax", "charges", "fees", "costs",
    "regulatory", "complaint", "compensation", "prospectus",
    "risk warning", "no guarantee",
]


def score_transparency(doc: ExtractedDocument) -> DimensionScore:
    text_lower = doc.raw_text.lower()
    found = [kw for kw in DISCLOSURE_KEYWORDS if kw in text_lower]
    ratio = len(found) / len(DISCLOSURE_KEYWORDS)
    s = 5.0 if ratio >= 0.7 else 4.0 if ratio >= 0.5 else 3.0 if ratio >= 0.35 else 2.0 if ratio >= 0.2 else 1.0
    return DimensionScore(
        dimension="Transparency",
        score=s,
        details=[
            {"metric": "Disclosure keywords", "value": f"{len(found)}/{len(DISCLOSURE_KEYWORDS)}", "sub_score": s},
            {"metric": "Keywords found", "value": ", ".join(found[:8])},
        ],
    )


def score_design(doc: ExtractedDocument) -> DimensionScore:
    details: list[dict] = []
    components: list[float] = []

    headings = doc.get_headings()
    s = 5.0 if len(headings) >= 8 else 4.0 if len(headings) >= 5 else 3.0 if len(headings) >= 3 else 2.0 if headings else 1.0
    details.append({"metric": "Heading count", "value": str(len(headings)), "sub_score": s})
    components.append(s)

    block_types = set(b.kind for b in doc.blocks)
    s = 5.0 if len(block_types) >= 4 else 4.0 if len(block_types) >= 3 else 3.0 if len(block_types) >= 2 else 2.0
    details.append({"metric": "Block variety", "value": ", ".join(sorted(block_types)), "sub_score": s})
    components.append(s)

    levels = sorted(set(h.level for h in headings if h.level is not None))
    s = 5.0 if len(levels) >= 3 else 4.0 if len(levels) >= 2 else 3.0 if levels else 1.0
    details.append({"metric": "Heading depth", "value": str(levels), "sub_score": s})
    components.append(s)

    return DimensionScore(dimension="Design", score=round(statistics.mean(components), 1), details=details)


def score_accessibility(doc: ExtractedDocument, accessibility_result: dict) -> DimensionScore:
    pct = accessibility_result.get("accessibility_score") or 0.0
    crit = accessibility_result.get("critical_failures", 0)
    s = 5.0 if pct >= 90 and crit == 0 else 4.0 if pct >= 75 else 3.0 if pct >= 50 else 2.0 if pct >= 25 else 1.0
    return DimensionScore(
        dimension="Accessibility",
        score=s,
        details=[
            {"metric": "Score", "value": f"{pct:.0f}%", "sub_score": s},
            {"metric": "Critical failures", "value": str(crit)},
            {"metric": "Total checks", "value": str(accessibility_result.get("total_count", 0))},
        ],
    )


def score_compliance(doc: ExtractedDocument, compliance_result: dict) -> DimensionScore:
    pct = compliance_result.get("compliance_score") or 0.0
    s = 5.0 if pct >= 90 else 4.0 if pct >= 75 else 3.0 if pct >= 50 else 2.0 if pct >= 25 else 1.0
    return DimensionScore(
        dimension="Compliance",
        score=s,
        details=[
            {"metric": "Score", "value": f"{pct:.0f}%", "sub_score": s},
            {"metric": "Rules passed", "value": str(compliance_result.get("passed_count", 0))},
            {"metric": "Rules failed", "value": str(compliance_result.get("failed_count", 0))},
        ],
    )


def score_usability(doc: ExtractedDocument) -> DimensionScore:
    details: list[dict] = []
    components: list[float] = []

    headings = doc.get_headings()
    s = 5.0 if len(headings) >= 5 else 4.0 if len(headings) >= 3 else 3.0 if headings else 1.0
    details.append({"metric": "Navigation headings", "value": str(len(headings)), "sub_score": s})
    components.append(s)

    blocks = len(doc.blocks)
    s = 5.0 if blocks >= 25 else 4.0 if blocks >= 15 else 3.0 if blocks >= 8 else 2.0 if blocks >= 3 else 1.0
    details.append({"metric": "Content blocks", "value": str(blocks), "sub_score": s})
    components.append(s)

    tables = sum(1 for b in doc.blocks if b.kind == "table")
    s = 5.0 if tables >= 3 else 4.0 if tables >= 2 else 3.5 if tables >= 1 else 3.0
    details.append({"metric": "Tables", "value": str(tables), "sub_score": s})
    components.append(s)

    return DimensionScore(dimension="Usability", score=round(statistics.mean(components), 1), details=details)


# ---------------------------------------------------------------------------
# 5-Pillar scorers
# ---------------------------------------------------------------------------

def score_completeness(doc: ExtractedDocument, taxonomy_results: list) -> PillarScore:
    if not taxonomy_results:
        return PillarScore(pillar="Completeness", score=0.0)
    present = sum(1 for t in taxonomy_results if t.present)
    pct = round(present / len(taxonomy_results) * 100, 1)
    return PillarScore(
        pillar="Completeness",
        score=pct,
        details=[{"metric": "Categories present", "value": f"{present}/{len(taxonomy_results)}"}],
    )


def score_consistency(doc: ExtractedDocument) -> PillarScore:
    # Heuristic checks for internal consistency
    components: list[float] = []
    details: list[dict] = []

    # Check if dates appear consistent
    text = doc.raw_text
    date_patterns = re.findall(r"\b\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}\b", text)
    date_patterns += re.findall(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}\b", text, re.I)
    if date_patterns:
        components.append(80.0)
        details.append({"metric": "Date references found", "value": str(len(date_patterns))})
    else:
        components.append(40.0)
        details.append({"metric": "Date references", "value": "None found"})

    # Check naming consistency (headings use similar style)
    headings = doc.get_headings()
    if len(headings) >= 2:
        caps = sum(1 for h in headings if h.text == h.text.upper())
        mixed = sum(1 for h in headings if h.text != h.text.upper() and h.text != h.text.title())
        if caps == len(headings) or mixed == 0:
            components.append(90.0)
        else:
            components.append(60.0)
        details.append({"metric": "Heading style consistency", "value": f"{len(headings)} headings analysed"})
    else:
        components.append(50.0)

    score = round(statistics.mean(components), 1) if components else 50.0
    return PillarScore(pillar="Consistency", score=score, details=details)


def score_data_integrity(doc: ExtractedDocument) -> PillarScore:
    text_lower = doc.raw_text.lower()
    details: list[dict] = []
    components: list[float] = []

    # As-of date
    has_as_of = any(phrase in text_lower for phrase in ["as of", "as at", "data date", "reporting date"])
    components.append(100.0 if has_as_of else 20.0)
    details.append({"metric": "As-of date present", "value": "Yes" if has_as_of else "No"})

    # Source references
    has_source = any(phrase in text_lower for phrase in ["source:", "data source", "calculated by", "provided by"])
    components.append(100.0 if has_source else 30.0)
    details.append({"metric": "Data source reference", "value": "Yes" if has_source else "No"})

    score = round(statistics.mean(components), 1)
    return PillarScore(pillar="Data Integrity", score=score, details=details)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def compute_benchmarking_scores(
    doc: ExtractedDocument,
    compliance_result: dict,
    accessibility_result: dict,
    taxonomy_results: list | None = None,
) -> BenchmarkResult:
    dims = {
        "clarity": score_clarity(doc),
        "transparency": score_transparency(doc),
        "design": score_design(doc),
        "accessibility": score_accessibility(doc, accessibility_result),
        "compliance": score_compliance(doc, compliance_result),
        "usability": score_usability(doc),
    }

    # Pillars
    pillars = {
        "completeness": score_completeness(doc, taxonomy_results or []),
        "consistency": score_consistency(doc),
        "compliance_pillar": PillarScore(
            pillar="Compliance",
            score=compliance_result.get("compliance_score") or 0.0,
            details=[{"metric": "From compliance engine", "value": f"{compliance_result.get('compliance_score', 0):.0f}%"}],
        ),
        "quality": PillarScore(
            pillar="Quality",
            score=round(statistics.mean([dims["clarity"].score, dims["design"].score, dims["usability"].score]) / 5 * 100, 1),
        ),
        "data_integrity": score_data_integrity(doc),
    }

    overall_dim = round(statistics.mean(d.score for d in dims.values()), 1)
    overall_pillar = round(statistics.mean(p.score for p in pillars.values()), 1)

    strengths = [f"{d.dimension} — {d.label} ({d.score:.1f}/5)" for d in dims.values() if d.score >= 4.0]
    weaknesses = [f"{d.dimension} — {d.label} ({d.score:.1f}/5)" for d in dims.values() if d.score <= 2.5]

    recommendations: list[str] = []
    if dims["clarity"].score < 3.5:
        recommendations.append("Simplify language — shorten sentences, reduce jargon, use plain English.")
    if dims["transparency"].score < 3.5:
        recommendations.append("Improve disclosure coverage — add risk warnings, fee breakdowns, complaint procedures.")
    if dims["design"].score < 3.5:
        recommendations.append("Strengthen visual hierarchy — add headings, use varied content blocks (tables, lists).")
    if dims["accessibility"].score < 3.5:
        recommendations.append("Implement accessibility tagging — heading structure, alt text, reading order, PDF/UA compliance.")
    if dims["compliance"].score < 3.5:
        recommendations.append("Review regulatory requirements — ensure all mandatory sections and disclaimers are present.")
    if dims["usability"].score < 3.5:
        recommendations.append("Enhance navigation — add more headings, structured tables, and clear information hierarchy.")
    if pillars["data_integrity"].score < 50:
        recommendations.append("Add data provenance — include as-of dates, data sources, and calculation methodologies.")
    if not recommendations:
        recommendations.append("Document meets or exceeds benchmarking standards across all dimensions.")

    return BenchmarkResult(
        dimensions=dims,
        pillars=pillars,
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations,
        overall_dimension_score=overall_dim,
        overall_pillar_score=overall_pillar,
    )
