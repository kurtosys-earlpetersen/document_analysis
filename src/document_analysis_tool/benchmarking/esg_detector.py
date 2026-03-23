"""
ESG content detector — determines whether a document needs ESG content
based on sectors, holdings, strategy descriptions and regulatory signals.
"""

from __future__ import annotations

from dataclasses import dataclass, field


ESG_SENSITIVE_SECTORS = [
    "energy", "oil", "gas", "coal", "mining", "utilities", "tobacco",
    "weapons", "defence", "defense", "gambling", "alcohol", "nuclear",
    "chemicals", "petrochemical", "fossil fuel", "extraction",
    "palm oil", "deforestation", "livestock", "agribusiness",
]

ESG_POSITIVE_SECTORS = [
    "renewable", "clean energy", "solar", "wind", "hydrogen",
    "electric vehicle", "green bond", "sustainable", "impact",
    "social housing", "healthcare", "education", "water treatment",
    "circular economy", "biodiversity",
]

ESG_REGULATORY_SIGNALS = [
    "sfdr", "article 6", "article 8", "article 9",
    "taxonomy regulation", "eu taxonomy", "sustainable finance",
    "principal adverse impact", "pai", "tcfd", "issb",
    "climate risk", "net zero", "carbon neutral",
    "paris agreement", "science-based target",
]

ESG_STRATEGY_SIGNALS = [
    "esg integration", "esg", "responsible investment", "sri",
    "socially responsible", "ethical", "stewardship",
    "engagement", "proxy voting", "exclusion", "negative screening",
    "positive screening", "best-in-class", "impact investing",
    "thematic", "green", "sustainable", "climate",
    "environmental", "social", "governance",
    "carbon footprint", "waci", "carbon intensity",
    "scope 1", "scope 2", "scope 3", "emissions",
]

HOLDINGS_ESG_TRIGGERS = [
    "controversial weapons", "cluster munitions", "anti-personnel mines",
    "thermal coal", "arctic drilling", "tar sands", "oil sands",
    "child labour", "human rights", "supply chain",
    "board diversity", "gender pay", "executive compensation",
]


@dataclass
class ESGAssessment:
    needs_esg_content: bool
    confidence: str  # "high", "medium", "low"
    reasons: list[str] = field(default_factory=list)
    sensitive_sectors_found: list[str] = field(default_factory=list)
    positive_sectors_found: list[str] = field(default_factory=list)
    regulatory_signals_found: list[str] = field(default_factory=list)
    strategy_signals_found: list[str] = field(default_factory=list)
    holdings_triggers_found: list[str] = field(default_factory=list)
    has_esg_content: bool = False
    esg_coverage_score: float = 0.0  # 0–100
    missing_esg_elements: list[str] = field(default_factory=list)


REQUIRED_ESG_ELEMENTS = [
    ("ESG policy or integration statement", ["esg policy", "esg integration", "responsible investment policy"]),
    ("SFDR classification", ["sfdr", "article 6", "article 8", "article 9"]),
    ("Carbon or climate metrics", ["carbon", "emissions", "waci", "climate", "carbon footprint"]),
    ("Engagement or stewardship", ["engagement", "stewardship", "proxy voting", "voting"]),
    ("Exclusion or screening criteria", ["exclusion", "screening", "negative screen", "exclude"]),
    ("ESG ratings or scores", ["esg rating", "esg score", "msci esg", "sustainalytics"]),
]


def assess_esg_needs(raw_text: str) -> ESGAssessment:
    text_lower = raw_text.lower()
    reasons: list[str] = []

    sensitive = [s for s in ESG_SENSITIVE_SECTORS if s in text_lower]
    positive = [s for s in ESG_POSITIVE_SECTORS if s in text_lower]
    regulatory = [s for s in ESG_REGULATORY_SIGNALS if s in text_lower]
    strategy = [s for s in ESG_STRATEGY_SIGNALS if s in text_lower]
    holdings = [s for s in HOLDINGS_ESG_TRIGGERS if s in text_lower]

    # Determine if ESG content is needed
    score = 0
    if sensitive:
        score += 30
        reasons.append(f"Document references ESG-sensitive sectors: {', '.join(sensitive[:5])}")
    if positive:
        score += 20
        reasons.append(f"Document references ESG-positive themes: {', '.join(positive[:5])}")
    if regulatory:
        score += 30
        reasons.append(f"Document contains regulatory ESG signals: {', '.join(regulatory[:5])}")
    if strategy:
        score += 20
        reasons.append(f"Document references ESG strategy concepts: {', '.join(strategy[:5])}")
    if holdings:
        score += 15
        reasons.append(f"Document references ESG-relevant holdings factors: {', '.join(holdings[:5])}")

    needs_esg = score >= 20
    if not needs_esg and not reasons:
        reasons.append("No ESG-relevant content detected — document may still benefit from basic ESG disclosure.")

    if score >= 50:
        confidence = "high"
    elif score >= 20:
        confidence = "medium"
    else:
        confidence = "low"

    # Check existing ESG coverage
    has_esg = any(kw in text_lower for kw in ["esg", "sustainable", "sustainability", "responsible investment"])
    missing: list[str] = []
    found_elements = 0
    for element_name, keywords in REQUIRED_ESG_ELEMENTS:
        if any(kw in text_lower for kw in keywords):
            found_elements += 1
        else:
            missing.append(element_name)

    esg_coverage = round(found_elements / len(REQUIRED_ESG_ELEMENTS) * 100, 1) if REQUIRED_ESG_ELEMENTS else 0.0

    return ESGAssessment(
        needs_esg_content=needs_esg,
        confidence=confidence,
        reasons=reasons,
        sensitive_sectors_found=sensitive,
        positive_sectors_found=positive,
        regulatory_signals_found=regulatory,
        strategy_signals_found=strategy,
        holdings_triggers_found=holdings,
        has_esg_content=has_esg,
        esg_coverage_score=esg_coverage,
        missing_esg_elements=missing,
    )
