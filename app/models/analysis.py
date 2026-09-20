"""Domain objects produced by the analysis engines.

Everything here is immutable and JSON-serialisable via
``dataclasses.asdict``, so the API layer never has to know how a result was
computed — it just hands the dataclass to the serialiser.
"""

from __future__ import annotations

from dataclasses import dataclass, field

BAND_LOW = "low"
BAND_MODERATE = "moderate"
BAND_HIGH = "high"
BAND_SEVERE = "severe"

FAVOUR_COUNTERPARTY = "counterparty"
FAVOUR_YOU = "you"
FAVOUR_BALANCED = "balanced"
FAVOUR_UNCLEAR = "unclear"


@dataclass(frozen=True, slots=True)
class Readability:
    """A real, computed readability profile of the document text."""

    words: int
    sentences: int
    syllables: int
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    average_sentence_length: float
    long_sentence_ratio: float
    reading_minutes: float
    band: str


@dataclass(frozen=True, slots=True)
class RiskAssessment:
    """Why one clause is (or is not) worth the reader's attention."""

    severity: int  # 0-10
    band: str
    why_it_matters: str
    watch_for: tuple[str, ...] = ()
    negotiation_tip: str = ""
    evidence: tuple[str, ...] = ()
    favour: str = FAVOUR_UNCLEAR


@dataclass(frozen=True, slots=True)
class ClauseAnalysis:
    """Everything the app knows about a single clause."""

    index: int
    citation: str
    heading: str
    text: str
    clause_type: str
    type_label: str
    confidence: float
    plain_language: str
    obligations: tuple[str, ...] = ()
    risk: RiskAssessment | None = None

    @property
    def severity(self) -> int:
        return self.risk.severity if self.risk else 0

    @property
    def band(self) -> str:
        return self.risk.band if self.risk else BAND_LOW


@dataclass(frozen=True, slots=True)
class RiskSummaryItem:
    """Small projection of a risky clause, used by the risk board."""

    clause_index: int
    citation: str
    type_label: str
    severity: int
    band: str
    headline: str
    favour: str


@dataclass(frozen=True, slots=True)
class GapFinding:
    """A provision that is missing, plus what to ask for instead."""

    identifier: str
    label: str
    importance: str  # "essential" | "recommended"
    why_it_matters: str
    ask_for: str


@dataclass(frozen=True, slots=True)
class DocumentProfile:
    """What kind of document this appears to be, and why we think so."""

    archetype: str
    archetype_label: str
    confidence: float
    signals: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class KeyFact:
    """A concrete, quotable fact the reader should verify."""

    kind: str
    value: str
    normalised: str
    citation: str


@dataclass(frozen=True, slots=True)
class ActionItem:
    """One prioritised thing the reader can actually do next."""

    priority: int
    title: str
    detail: str
    citation: str = ""


@dataclass(frozen=True, slots=True)
class NegotiationPoint:
    """A ready-to-use ask, phrased the way a person would say it."""

    citation: str
    headline: str
    say_this: str


@dataclass(frozen=True, slots=True)
class LawyerBrief:
    """A one-page handover for a qualified professional."""

    summary: str
    key_facts: tuple[KeyFact, ...] = ()
    top_risks: tuple[RiskSummaryItem, ...] = ()
    questions: tuple[str, ...] = ()
    documents_to_gather: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AnalysisReport:
    """The complete review of one document."""

    document_id: str
    source_name: str
    persona: str
    jurisdiction: str
    word_count: int
    clause_count: int
    readability: Readability
    profile: DocumentProfile
    clauses: tuple[ClauseAnalysis, ...] = ()
    risks: tuple[RiskSummaryItem, ...] = ()
    gaps: tuple[GapFinding, ...] = ()
    key_facts: tuple[KeyFact, ...] = ()
    actions: tuple[ActionItem, ...] = ()
    negotiation: tuple[NegotiationPoint, ...] = ()
    brief: LawyerBrief | None = None
    overall_risk: int = 0
    overall_band: str = BAND_LOW
    engine: str = "deterministic"
    truncated: bool = False
    warnings: tuple[str, ...] = field(default_factory=tuple)
