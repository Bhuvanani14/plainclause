"""PlainClause – FastAPI web service.

Exposes the clause-detection engine as a JSON API so that a frontend, mobile
app, or integration can analyse documents without running the CLI.
"""

from __future__ import annotations

import io
import os
import re
import sys
from dataclasses import asdict
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so `app.core.*` imports resolve
# regardless of how uvicorn is launched.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from app.core.clauses import get_clause_type, compiled_patterns  # noqa: E402
from app.core.personas import (  # noqa: E402
    PERSONA_IDS,
    PERSONAS,
    get_persona,
)
from app.config import get_settings  # noqa: E402

# ---------------------------------------------------------------------------
# Optional: PDF text extraction (graceful degradation if pypdf missing)
# ---------------------------------------------------------------------------
try:
    from pypdf import PdfReader

    _HAS_PYPDF = True
except ImportError:
    _HAS_PYPDF = False

# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "PlainClause makes legal documents readable, comparable and actionable. "
        "Upload or paste a document to receive a clause-by-clause risk analysis."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Analyser (re-uses the core engine)
# ---------------------------------------------------------------------------
class PlainClauseAnalyzer:
    """Stateless document analyser backed by the compiled pattern catalogue."""

    def __init__(self) -> None:
        self.patterns = compiled_patterns()

    def analyze_document(self, text: str, persona_id: str = "other") -> dict:
        persona = get_persona(persona_id)
        lines = text.split("\n")

        detected_clauses: list[dict] = []
        total_severity = 0

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            for clause_id, pattern_group in self.patterns:
                for pattern in pattern_group:
                    if pattern.search(line):
                        clause_type = get_clause_type(clause_id)

                        weighted = clause_type.base_severity + persona.severity_weights.get(
                            clause_id, 0
                        )
                        weighted = max(0, min(10, weighted))

                        detected_clauses.append(
                            {
                                "line_number": i,
                                "line_text": line,
                                "clause_id": clause_id,
                                "clause_label": clause_type.label,
                                "group": clause_type.group,
                                "base_severity": clause_type.base_severity,
                                "weighted_severity": weighted,
                                "summary": clause_type.summary,
                                "why_it_matters": clause_type.why_it_matters,
                                "watch_for": list(clause_type.watch_for),
                                "negotiation_tip": clause_type.negotiation_tip,
                            }
                        )

                        total_severity += weighted
                        break  # one match per line per clause type

        avg = total_severity / len(detected_clauses) if detected_clauses else 0
        risk_level = "High" if avg >= 7 else ("Moderate" if avg >= 4 else "Low")

        high = [c for c in detected_clauses if c["weighted_severity"] >= 7]
        med = [c for c in detected_clauses if 4 <= c["weighted_severity"] < 7]
        low = [c for c in detected_clauses if c["weighted_severity"] < 4]

        summary_parts = [
            f"Analysis for {persona.label}:",
            f"- Found {len(detected_clauses)} relevant clause(s)",
            f"- {len(high)} high-risk items (≥7 severity)",
            f"- {len(med)} medium-risk items (4-6 severity)",
            f"- {len(low)} low-risk items (<4 severity)",
        ]
        if high:
            summary_parts.append("\nHigh-risk items requiring attention:")
            for c in high[:5]:
                summary_parts.append(
                    f"  • {c['clause_label']} (line {c['line_number']})"
                )

        return {
            "persona": persona.label,
            "persona_id": persona_id,
            "total_clauses_found": len(detected_clauses),
            "average_severity": round(avg, 2),
            "risk_level": risk_level,
            "clauses": detected_clauses,
            "summary": "\n".join(summary_parts),
            "questions_to_ask": list(persona.questions),
            "documents_to_gather": list(persona.documents_to_gather),
        }


_analyzer = PlainClauseAnalyzer()


# ---------------------------------------------------------------------------
# Helper: extract text from an uploaded file
# ---------------------------------------------------------------------------
def _extract_text(filename: str, content: bytes) -> str:
    """Return plain text from a file upload (PDF or text)."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        if not _HAS_PYPDF:
            raise HTTPException(
                status_code=400,
                detail="PDF support is not available – please paste text instead.",
            )
        reader = PdfReader(io.BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages).strip()
        if not text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF. The file may be image-based.",
            )
        return text
    # Assume plain text
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
async def root():
    """Welcome / health-check endpoint."""
    return {
        "app": settings.app_name,
        "version": settings.version,
        "status": "running",
        "message": (
            "PlainClause API is live. "
            "POST /api/analyze with {text, persona} to analyse a document."
        ),
    }


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": settings.version}


@app.get("/api/personas")
async def list_personas():
    """Return every available persona with its metadata."""
    result = []
    for pid in PERSONA_IDS:
        p = PERSONAS[pid]
        result.append(
            {
                "id": p.id,
                "label": p.label,
                "blurb": p.blurb,
                "questions": list(p.questions),
                "documents_to_gather": list(p.documents_to_gather),
            }
        )
    return {"personas": result}


@app.post("/api/analyze")
async def analyze_text(
    text: str = Form(...),
    persona: str = Form("other"),
    filename: str = Form("pasted-document.txt"),
):
    """Analyse pasted document text."""
    if persona not in PERSONA_IDS:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown persona '{persona}'. Choose from: {list(PERSONA_IDS)}",
        )
    text = text.strip()
    if len(text) < 30:
        raise HTTPException(
            status_code=422,
            detail="Document text is too short for meaningful analysis (min 30 chars).",
        )
    return _analyzer.analyze_document(text, persona)


@app.post("/api/analyze/upload")
async def analyze_upload(
    file: UploadFile = File(...),
    persona: str = Form("other"),
):
    """Analyse an uploaded document (PDF or plain-text file)."""
    if persona not in PERSONA_IDS:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown persona '{persona}'. Choose from: {list(PERSONA_IDS)}",
        )
    content = await file.read()
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large (max {settings.max_upload_bytes // 1024 // 1024} MB).",
        )
    doc_text = _extract_text(file.filename or "upload.txt", content)
    if len(doc_text.strip()) < 30:
        raise HTTPException(
            status_code=422,
            detail="Extracted text is too short for meaningful analysis.",
        )
    return _analyzer.analyze_document(doc_text, persona)


# ---------------------------------------------------------------------------
# Standalone launcher
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
