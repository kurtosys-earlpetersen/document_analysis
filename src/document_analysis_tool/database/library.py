"""Analysis library: save, retrieve, delete persisted analysis results."""

import json
from .db import get_connection


def save_analysis(
    user_id: int,
    filename: str,
    doc_type: str,
    jurisdiction: str,
    audience: str,
    overall_score: float,
    compliance_pct: float,
    accessibility_pct: float,
    esg_needed: bool,
    esg_coverage: float,
    results_json: dict,
) -> int:
    """Save analysis to DB. Returns the new row id."""
    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO analyses
               (user_id, filename, doc_type, jurisdiction, audience,
                overall_score, compliance_pct, accessibility_pct,
                esg_needed, esg_coverage, results_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id, filename, doc_type, jurisdiction, audience,
                overall_score, compliance_pct, accessibility_pct,
                1 if esg_needed else 0, esg_coverage,
                json.dumps(results_json, default=str),
            ),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_user_analyses(user_id: int) -> list[dict]:
    """Get all analyses for a user, newest first."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM analyses WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_analysis(analysis_id: int, user_id: int) -> bool:
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM analyses WHERE id = ? AND user_id = ?",
            (analysis_id, user_id),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
