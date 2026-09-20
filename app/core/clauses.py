"""The assembled clause catalogue.

The single source of truth for what PlainClause can recognise. It merges the
per-group definition modules, compiles the detection patterns once at import
time, and exposes the small lookup helpers the rest of the code needs.
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Final, Mapping

from app.core.clause_defs import (
    GROUP_CONTROL,
    GROUP_DATA,
    GROUP_EXIT,
    GROUP_LEGAL,
    GROUP_MONEY,
    GROUP_PEOPLE,
    GROUP_RIGHTS,
    GROUP_SCOPE,
    ClauseType,
)
from app.core.clause_defs_consumer import OPERATIONAL_CLAUSES
from app.core.clause_defs_control import CONTROL_CLAUSES
from app.core.clause_defs_employment import EMPLOYMENT_CLAUSES
from app.core.clause_defs_legal import LEGAL_CLAUSES
from app.core.clause_defs_mechanics import MECHANICS_CLAUSES
from app.core.clause_defs_money import MONEY_CLAUSES
from app.core.clause_defs_occupancy import OCCUPANCY_CLAUSES
from app.core.clause_defs_rights import RIGHTS_CLAUSES
from app.core.clause_defs_tenancy import TENANCY_CLAUSES

BAND_LOW: Final = "low"
BAND_MODERATE: Final = "moderate"
BAND_HIGH: Final = "high"
BAND_SEVERE: Final = "severe"

#: Severity at or above which a clause is treated as needing attention.
ATTENTION_THRESHOLD: Final = 5

GROUP_ORDER: Final[tuple[str, ...]] = (
    GROUP_MONEY,
    GROUP_EXIT,
    GROUP_CONTROL,
    GROUP_RIGHTS,
    GROUP_PEOPLE,
    GROUP_DATA,
    GROUP_SCOPE,
    GROUP_LEGAL,
)

GROUP_LABELS: Final[Mapping[str, str]] = {
    GROUP_MONEY: "Money",
    GROUP_EXIT: "Ending the agreement",
    GROUP_CONTROL: "Control and change",
    GROUP_RIGHTS: "Rights and restrictions",
    GROUP_PEOPLE: "Housing and work",
    GROUP_DATA: "Data and privacy",
    GROUP_SCOPE: "Scope and delivery",
    GROUP_LEGAL: "Disputes and warranties",
}

ALL_CLAUSE_TYPES: Final[tuple[ClauseType, ...]] = (
    MONEY_CLAUSES
    + CONTROL_CLAUSES
    + RIGHTS_CLAUSES
    + TENANCY_CLAUSES
    + OCCUPANCY_CLAUSES
    + EMPLOYMENT_CLAUSES
    + MECHANICS_CLAUSES
    + LEGAL_CLAUSES
    + OPERATIONAL_CLAUSES
)

CATALOG: Final[Mapping[str, ClauseType]] = {item.id: item for item in ALL_CLAUSE_TYPES}

UNKNOWN_CLAUSE_TYPE: Final = ClauseType(
    id="other",
    label="General provision",
    group=GROUP_SCOPE,
    summary="Text that does not match a known clause category.",
    base_severity=1,
    why_it_matters=(
        "PlainClause did not recognise a specific category here, which is normal for "
        "definitions, notices and administrative wording."
    ),
    expected_in=("general",),
)


def _identifier_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in ALL_CLAUSE_TYPES:
        counts[item.id] = counts.get(item.id, 0) + 1
    return counts


# Import-time sanity check: a duplicated identifier would silently shadow an
# earlier clause type and quietly weaken every review.
_DUPLICATES = sorted(
    identifier for identifier, count in _identifier_counts().items() if count > 1
)
if _DUPLICATES:  # pragma: no cover - guards a developer mistake
    raise RuntimeError(f"duplicate clause type identifiers: {_DUPLICATES}")


def get_clause_type(clause_type_id: str) -> ClauseType:
    """Look up a clause type, falling back to the neutral 'other' record."""
    return CATALOG.get(clause_type_id, UNKNOWN_CLAUSE_TYPE)


def clause_type_label(clause_type_id: str) -> str:
    return get_clause_type(clause_type_id).label


def group_label(group: str) -> str:
    return GROUP_LABELS.get(group, "Other provisions")


def band_for(severity: int) -> str:
    """Translate a 0-10 severity score into the band shown in the interface."""
    if severity >= 8:
        return BAND_SEVERE
    if severity >= 6:
        return BAND_HIGH
    if severity >= 3:
        return BAND_MODERATE
    return BAND_LOW


def band_rank(band: str) -> int:
    """Ordering helper so 'severe' sorts above 'low'."""
    order = {BAND_LOW: 0, BAND_MODERATE: 1, BAND_HIGH: 2, BAND_SEVERE: 3}
    return order.get(band, 0)


@lru_cache(maxsize=1)
def compiled_patterns() -> tuple[tuple[str, tuple[re.Pattern[str], ...]], ...]:
    """Pre-compiled detection patterns, grouped by clause type.

    Compiled once and cached because a review classifies every clause in a
    document, and recompiling several hundred expressions per clause would
    dominate the request runtime.
    """
    compiled: list[tuple[str, tuple[re.Pattern[str], ...]]] = []
    for clause_type in ALL_CLAUSE_TYPES:
        expressions = tuple(
            re.compile(pattern, re.IGNORECASE) for pattern in clause_type.patterns
        )
        compiled.append((clause_type.id, expressions))
    return tuple(compiled)
