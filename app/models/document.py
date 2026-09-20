"""Core document domain objects.

These are plain, frozen dataclasses on purpose: the analysis engines are pure
functions over immutable data, which makes them easy to unit test and safe to
run concurrently.  Character offsets are preserved everywhere so that every
claim the app makes can be traced back to the exact text it came from.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Final

CITATION_HINT: Final = (
    "Clause labels are the visible markers a reader would use to cite a provision, "
    "for example '4.2', 'Section 7', 'Article III' or 'Clause 12'."
)


@dataclass(frozen=True, slots=True)
class Clause:
    """A single citable unit of a legal document."""

    index: int
    text: str
    start: int
    end: int
    label: str = ""
    heading: str = ""

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    @property
    def citation(self) -> str:
        """Human-readable pointer used in the UI and in AI prompts."""
        if self.label and self.heading:
            return f"{self.label} ({self.heading})"
        if self.label:
            return self.label
        if self.heading:
            return self.heading
        return f"Clause {self.index + 1}"

    @property
    def preview(self) -> str:
        text = self.text.strip()
        return text if len(text) <= 140 else text[:137].rstrip() + "…"


@dataclass(frozen=True, slots=True)
class Entity:
    """A concrete value extracted from the document text."""

    kind: str  # "amount" | "duration" | "date" | "percentage" | "party"
    value: str  # exactly as it appears in the source
    normalised: str  # comparable form, e.g. "30 days", "5000 USD"
    clause_index: int


@dataclass(frozen=True, slots=True)
class ParsedDocument:
    """The result of ingesting and segmenting one document."""

    source_name: str
    text: str
    clauses: tuple[Clause, ...] = ()
    entities: tuple[Entity, ...] = ()
    kind: str = "unknown"  # guessed archetype: lease, nda, employment, ...
    truncated: bool = False
    warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def document_id(self) -> str:
        digest = hashlib.sha256(self.text.encode("utf-8", "ignore")).hexdigest()
        return digest[:16]

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    def clause_at(self, index: int) -> Clause | None:
        if 0 <= index < len(self.clauses):
            return self.clauses[index]
        return None

    def entities_of(self, kind: str) -> tuple[Entity, ...]:
        return tuple(entity for entity in self.entities if entity.kind == kind)
