"""The clause type record shared by every catalogue module.

Severity is a 0-10 estimate of how much attention a clause deserves *by
default*; persona weights in :mod:`app.core.personas` then adjust it for a
particular reader.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

GROUP_MONEY: Final = "money"
GROUP_CONTROL: Final = "control"
GROUP_EXIT: Final = "exit"
GROUP_PEOPLE: Final = "people"
GROUP_DATA: Final = "data"
GROUP_LEGAL: Final = "legal"
GROUP_SCOPE: Final = "scope"
GROUP_RIGHTS: Final = "rights"


@dataclass(frozen=True, slots=True)
class ClauseType:
    """One recognisable kind of legal provision."""

    id: str
    label: str
    group: str
    summary: str
    base_severity: int
    patterns: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    why_it_matters: str = ""
    watch_for: tuple[str, ...] = field(default_factory=tuple)
    negotiation_tip: str = ""
    expected_in: tuple[str, ...] = ()
