"""
Taxonomy detection — master component dictionary aligned with the
Document Benchmarking Project and normalized component groups.
"""

from __future__ import annotations

from dataclasses import dataclass, field


TAXONOMY: dict[str, dict] = {
    "identity_metadata": {
        "label": "Identity & Product Metadata",
        "icon": "🏷️",
        "keywords": [
            "isin", "sedol", "ticker", "domicile", "base currency",
            "launch date", "aum", "fund size", "share class", "product name",
            "management company", "depositary", "trustee", "administrator",
            "transfer agent", "auditor", "custodian", "vehicle type",
            "ucits", "etf",
        ],
    },
    "investor_proposition": {
        "label": "Investor Proposition",
        "icon": "🎯",
        "keywords": [
            "value proposition", "target investor", "suitability",
            "investment horizon", "key benefits", "key risks",
            "risk tolerance", "who is this product for",
        ],
    },
    "objective_strategy": {
        "label": "Objective, Strategy & Process",
        "icon": "📐",
        "keywords": [
            "investment objective", "investment strategy", "investment universe",
            "alpha source", "portfolio construction", "risk management",
            "liquidity", "use of derivatives", "leverage",
            "benchmark", "strategy overview",
        ],
    },
    "team_governance": {
        "label": "Team & Governance",
        "icon": "👥",
        "keywords": [
            "portfolio manager", "fund manager", "team", "investment committee",
            "governance", "ownership structure", "succession",
        ],
    },
    "performance_analytics": {
        "label": "Performance & Analytics",
        "icon": "📈",
        "keywords": [
            "performance", "return", "ytd", "year to date", "cumulative",
            "annualised", "annualized", "calendar year", "benchmark comparison",
            "attribution", "sharpe", "information ratio", "drawdown",
            "risk adjusted", "turnover", "peer comparison",
        ],
    },
    "portfolio_exposure": {
        "label": "Portfolio & Exposure",
        "icon": "📊",
        "keywords": [
            "top holdings", "holdings", "sector allocation", "geographic allocation",
            "asset allocation", "duration", "yield to maturity", "credit quality",
            "style box", "valuation", "p/e", "cash position",
            "derivatives exposure",
        ],
    },
    "costs_terms": {
        "label": "Costs, Terms & Dealing",
        "icon": "💰",
        "keywords": [
            "management fee", "ongoing charges", "ocf", "ter",
            "total expense ratio", "performance fee", "entry fee", "exit fee",
            "transaction cost", "minimum investment", "dealing frequency",
            "settlement", "liquidity terms", "share class",
        ],
    },
    "esg_impact": {
        "label": "ESG, Impact & Stewardship",
        "icon": "🌿",
        "keywords": [
            "esg", "environmental", "social", "governance", "sustainability",
            "sfdr", "article 8", "article 9", "carbon", "waci", "emissions",
            "engagement", "proxy voting", "stewardship", "impact",
            "principal adverse impact", "pai",
        ],
    },
    "disclosures_legal": {
        "label": "Disclosures & Legal",
        "icon": "⚖️",
        "keywords": [
            "disclaimer", "disclosure", "past performance", "risk warning",
            "guarantee", "prospectus", "regulatory", "gips",
            "data source", "conflict of interest", "complaint",
            "marketing restriction", "country restriction",
        ],
    },
    "operational_dd": {
        "label": "Operational Due Diligence",
        "icon": "🔒",
        "keywords": [
            "valuation policy", "trade execution", "business continuity",
            "cyber security", "compliance monitoring", "service provider",
            "regulatory license",
        ],
    },
}


@dataclass
class TaxonomyCategory:
    id: str
    label: str
    icon: str
    present: bool
    matched_keywords: list[str] = field(default_factory=list)
    total_keywords: int = 0
    coverage_pct: float = 0.0

    @property
    def status_icon(self) -> str:
        if self.coverage_pct >= 50:
            return "🟢"
        if self.coverage_pct >= 20:
            return "🟡"
        if self.present:
            return "🟠"
        return "🔴"


def detect_taxonomy_coverage(raw_text: str) -> list[TaxonomyCategory]:
    text_lower = raw_text.lower()
    results: list[TaxonomyCategory] = []
    for cat_id, cat in TAXONOMY.items():
        keywords = cat["keywords"]
        matched = [kw for kw in keywords if kw.lower() in text_lower]
        pct = round(len(matched) / len(keywords) * 100, 1) if keywords else 0.0
        results.append(TaxonomyCategory(
            id=cat_id,
            label=cat["label"],
            icon=cat.get("icon", "📄"),
            present=len(matched) > 0,
            matched_keywords=matched,
            total_keywords=len(keywords),
            coverage_pct=pct,
        ))
    return results
