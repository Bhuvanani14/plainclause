"""Validated request bodies.

Validation is strict on purpose (``extra="forbid"``) so a malformed or
unexpected payload is rejected at the edge rather than reaching the analysis
engines.  Size limits are enforced here as a cheap first line of defence; the
authoritative limit comes from :mod:`app.config`.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

MAX_CONCERNS = 12
MAX_CONCERN_CHARS = 80
MAX_QUESTION_CHARS = 500
MAX_JURISDICTION_CHARS = 80
MIN_DOCUMENT_CHARS = 60

SIDES = ("receiving", "drafting")


class ReviewContext(BaseModel):
    """The user context that makes the advice specific rather than generic."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    persona: str = Field(
        default="other",
        description="Who the reader is, which selects the review checklist.",
    )
    jurisdiction: str = Field(
        default="",
        max_length=MAX_JURISDICTION_CHARS,
        description="Free-text jurisdiction hint, used for notes, never for legal conclusions.",
    )
    side: str = Field(
        default="receiving",
        description="'receiving' if the reader was handed the document, 'drafting' if they wrote it.",
    )
    concerns: list[str] = Field(
        default_factory=list,
        max_length=MAX_CONCERNS,
        description="Specific worries the reader already has, used to bias the review.",
    )

    @field_validator("persona")
    @classmethod
    def _known_persona(cls, value: str) -> str:
        from app.core.personas import PERSONA_IDS

        if value not in PERSONA_IDS:
            raise ValueError(f"unknown persona '{value}'")
        return value

    @field_validator("side")
    @classmethod
    def _known_side(cls, value: str) -> str:
        if value not in SIDES:
            raise ValueError(f"side must be one of {SIDES}")
        return value

    @field_validator("concerns")
    @classmethod
    def _clean_concerns(cls, values: list[str]) -> list[str]:
        cleaned: list[str] = []
        for raw in values:
            text = " ".join(raw.split())
            if text and len(text) <= MAX_CONCERN_CHARS:
                cleaned.append(text)
        return cleaned


class AnalyzeRequest(ReviewContext):
    """Review a pasted document."""

    text: str = Field(min_length=MIN_DOCUMENT_CHARS)
    filename: str = Field(default="pasted-document.txt", max_length=120)
    use_ai: bool = Field(default=True, description="Allow the generative layer to enhance the review.")

    @model_validator(mode="after")
    def _require_content(self) -> AnalyzeRequest:
        if not self.text.strip():
            raise ValueError("document text is empty")
        return self


class CompareRequest(ReviewContext):
    """Compare two versions of a document, or two competing documents."""

    text_a: str = Field(min_length=MIN_DOCUMENT_CHARS)
    text_b: str = Field(min_length=MIN_DOCUMENT_CHARS)
    name_a: str = Field(default="Version A", max_length=120)
    name_b: str = Field(default="Version B", max_length=120)
    use_ai: bool = True


class AskRequest(ReviewContext):
    """Ask a grounded question about a document."""

    text: str = Field(min_length=MIN_DOCUMENT_CHARS)
    question: str = Field(min_length=3, max_length=MAX_QUESTION_CHARS)
    top_k: int = Field(default=5, ge=1, le=12)
    use_ai: bool = True


class RedactionPreviewRequest(BaseModel):
    """Show exactly what would leave the machine before a cloud call."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=20000)


class ChatRequest(BaseModel):
    """Payload for the legal assistant chat agent."""

    message: str = Field(default="", max_length=1000)


class QuizSubmitRequest(BaseModel):
    """Payload for submitting quiz responses."""

    answers: dict[str, int] = Field(default_factory=dict)

