"""Public core API for PlainClause."""

from __future__ import annotations

from app.core.clauses import (
    ALL_CLAUSE_TYPES,
    ATTENTION_THRESHOLD,
    BAND_HIGH,
    BAND_LOW,
    BAND_MODERATE,
    BAND_SEVERE,
    CATALOG,
    UNKNOWN_CLAUSE_TYPE,
    band_for,
    band_rank,
    compiled_patterns,
    get_clause_type,
    clause_type_label,
    group_label,
)
from app.core.personas import (
    MAX_SEVERITY,
    MIN_SEVERITY,
    OTHER_PERSONA_ID,
    PERSONAS,
    PERSONA_IDS,
    clamp_severity,
    get_persona,
    jurisdiction_caution,
    severity_weight,
)

__all__ = [
    "ALL_CLAUSE_TYPES",
    "ATTENTION_THRESHOLD",
    "BAND_HIGH",
    "BAND_LOW",
    "BAND_MODERATE",
    "BAND_SEVERE",
    "CATALOG",
    "UNKNOWN_CLAUSE_TYPE",
    "band_for",
    "band_rank",
    "compiled_patterns",
    "get_clause_type",
    "clause_type_label",
    "group_label",
    "MAX_SEVERITY",
    "MIN_SEVERITY",
    "OTHER_PERSONA_ID",
    "PERSONAS",
    "PERSONA_IDS",
    "clamp_severity",
    "get_persona",
    "jurisdiction_caution",
    "severity_weight",
]
