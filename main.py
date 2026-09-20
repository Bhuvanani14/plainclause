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
from fastapi.responses import HTMLResponse, JSONResponse

# ---------------------------------------------------------------------------
# HTML Application Dashboard Template
# ---------------------------------------------------------------------------
INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PlainClause — AI Legal Document Analyzer</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0f172a;
      --panel: #1e293b;
      --border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --accent: #06b6d4;
      --danger: #ef4444;
      --warning: #f59e0b;
      --success: #10b981;
      --radius: 12px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
    body { background-color: var(--bg); color: var(--text); line-height: 1.6; min-height: 100vh; padding: 20px; }
    header { max-width: 1200px; margin: 0 auto 30px; display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid var(--border); }
    .logo-container { display: flex; align-items: center; gap: 12px; }
    .logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, var(--primary), var(--accent)); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 20px; color: white; }
    .logo-title { font-size: 24px; font-weight: 800; background: linear-gradient(135deg, #fff, var(--text-muted)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .nav-links a { color: var(--accent); text-decoration: none; font-size: 14px; font-weight: 600; padding: 8px 16px; border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 20px; transition: all 0.2s; }
    .nav-links a:hover { background: rgba(6, 182, 212, 0.1); }
    .container { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
    @media (max-width: 960px) { .container { grid-template-columns: 1fr; } }
    .card { background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); }
    .card-title { font-size: 18px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; }
    .form-group { margin-bottom: 20px; }
    label { display: block; font-size: 14px; font-weight: 600; color: var(--text-muted); margin-bottom: 8px; }
    select, textarea, input[type="file"] { width: 100%; background: #0f172a; border: 1px solid var(--border); border-radius: 8px; padding: 12px; color: var(--text); font-size: 14px; transition: border-color 0.2s; }
    select:focus, textarea:focus { border-color: var(--primary); outline: none; }
    textarea { height: 220px; resize: vertical; font-family: 'JetBrains Mono', monospace; font-size: 13px; }
    .btn-group { display: flex; gap: 12px; }
    .btn { padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 15px; cursor: pointer; border: none; transition: all 0.2s; display: inline-flex; align-items: center; justify-content: center; gap: 8px; }
    .btn-primary { background: var(--primary); color: white; flex: 2; }
    .btn-primary:hover { background: var(--primary-hover); transform: translateY(-1px); }
    .btn-secondary { background: #334155; color: var(--text); flex: 1; }
    .btn-secondary:hover { background: #475569; }
    
    /* Analysis Results Styling */
    .metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px; }
    .metric-box { background: #0f172a; border-radius: 8px; padding: 14px; text-align: center; border: 1px solid var(--border); }
    .metric-val { font-size: 22px; font-weight: 800; color: var(--accent); }
    .metric-lbl { font-size: 12px; color: var(--text-muted); font-weight: 500; }
    
    .badge-risk { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 700; text-transform: uppercase; }
    .risk-High { background: rgba(239, 68, 68, 0.2); color: var(--danger); border: 1px solid var(--danger); }
    .risk-Moderate { background: rgba(245, 158, 11, 0.2); color: var(--warning); border: 1px solid var(--warning); }
    .risk-Low { background: rgba(16, 185, 129, 0.2); color: var(--success); border: 1px solid var(--success); }

    .clause-item { background: #0f172a; border-left: 4px solid var(--border); border-radius: 6px; padding: 16px; margin-bottom: 14px; border-top: 1px solid rgba(255,255,255,0.05); }
    .clause-item.sev-high { border-left-color: var(--danger); }
    .clause-item.sev-med { border-left-color: var(--warning); }
    .clause-item.sev-low { border-left-color: var(--success); }
    
    .clause-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .clause-title { font-weight: 700; font-size: 15px; color: #fff; }
    .clause-line { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-muted); background: #1e293b; padding: 2px 6px; border-radius: 4px; }
    .clause-why { font-size: 13px; color: var(--text-muted); margin-bottom: 8px; }
    .clause-tip { background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 6px; padding: 10px; font-size: 13px; color: #c7d2fe; margin-top: 8px; }
    
    .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
    .empty-icon { font-size: 48px; margin-bottom: 12px; }
    
    .loading-spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: white; animation: spin 0.8s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <header>
    <div class="logo-container">
      <div class="logo-icon">P</div>
      <div>
        <div class="logo-title">PlainClause</div>
        <div style="font-size: 12px; color: var(--text-muted)">AI-Powered Legal Document Risk Analyzer</div>
      </div>
    </div>
    <div class="nav-links">
      <a href="/docs" target="_blank">⚡ API Documentation</a>
    </div>
  </header>

  <main class="container">
    <!-- Input Section -->
    <section class="card">
      <div class="card-title">
        <span>📄 Document Analysis</span>
      </div>
      
      <form id="analyzeForm">
        <div class="form-group">
          <label for="persona">Review Persona (Who is reviewing?)</label>
          <select id="persona" name="persona">
            <option value="tenant">Tenant or flatmate (Lease & Renting)</option>
            <option value="employee">Employee or job applicant (Employment Contract)</option>
            <option value="freelancer">Freelancer or small supplier (Client MSA & SOW)</option>
            <option value="consumer">Consumer or app user (Terms of Service)</option>
            <option value="founder">Founder or business partner (Shareholder / JV)</option>
            <option value="buyer">Buyer or borrower (Loan & Purchase)</option>
            <option value="other">General Reader (All-purpose review)</option>
          </select>
        </div>

        <div class="form-group">
          <label for="docText">Paste Document Text</label>
          <textarea id="docText" name="text" placeholder="Paste your lease, contract, or agreement text here..."></textarea>
        </div>

        <div class="form-group">
          <label for="docFile">Or Upload File (.pdf or .txt)</label>
          <input type="file" id="docFile" accept=".pdf,.txt">
        </div>

        <div class="btn-group">
          <button type="submit" class="btn btn-primary" id="submitBtn">
            <span>Analyze Document</span>
          </button>
          <button type="button" class="btn btn-secondary" id="sampleBtn">
            <span>Load Sample</span>
          </button>
        </div>
      </form>
    </section>

    <!-- Results Section -->
    <section class="card">
      <div class="card-title">
        <span>📊 Analysis Results</span>
        <span id="riskBadge"></span>
      </div>

      <div id="resultsContent">
        <div class="empty-state">
          <div class="empty-icon">⚖️</div>
          <h3>No Document Analyzed Yet</h3>
          <p>Paste a document or click <strong>"Load Sample"</strong> then <strong>"Analyze Document"</strong> to generate a clause-by-clause risk report.</p>
        </div>
      </div>
    </section>
  </main>

  <script>
    const sampleLease = `RESIDENTIAL LEASE AGREEMENT

1. SECURITY DEPOSIT: Tenant agrees to pay a security deposit of $3,000. Landlord reserves the right to retain the entire deposit if tenant terminates the lease early for any reason without exception.
2. RENT INCREASE: Landlord may increase the monthly rent at any time upon 7 days written notice without limitation on the percentage increase.
3. ENTRY RIGHTS: Landlord and agents may enter the premises at any time without prior notice for inspections, repairs, or showings.
4. SUBLETTING: Subletting, assignment, or hosting guests for more than 2 consecutive nights is strictly prohibited and subject to immediate eviction.
5. MAINTENANCE OBLIGATION: Tenant is solely responsible for all maintenance, repairs, and structural plumbing or roof fixes exceeding $50.
6. LATE FEE: A late fee of $150 plus 10% daily interest will apply to any rent paid after the 1st of the month.`;

    document.getElementById('sampleBtn').addEventListener('click', async () => {
      const persona = document.getElementById('persona').value;
      try {
        const res = await fetch(`/api/samples/${persona}`);
        const data = await res.json();
        if (data.text) {
          document.getElementById('docText').value = data.text;
        }
      } catch (e) {
        console.error('Failed to load sample', e);
      }
    });

    document.getElementById('persona').addEventListener('change', async (e) => {
      const persona = e.target.value;
      if (!document.getElementById('docText').value.trim()) {
        try {
          const res = await fetch(`/api/samples/${persona}`);
          const data = await res.json();
          if (data.text) {
            document.getElementById('docText').value = data.text;
          }
        } catch (err) {}
      }
    });

    document.getElementById('analyzeForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = document.getElementById('submitBtn');
      const resultsDiv = document.getElementById('resultsContent');
      const riskBadge = document.getElementById('riskBadge');
      
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span class="loading-spinner"></span> Analyzing...`;

      try {
        const formData = new FormData();
        const persona = document.getElementById('persona').value;
        const fileInput = document.getElementById('docFile');
        const textInput = document.getElementById('docText').value;

        let endpoint = '/api/analyze';

        if (fileInput.files.length > 0) {
          endpoint = '/api/analyze/upload';
          formData.append('file', fileInput.files[0]);
          formData.append('persona', persona);
        } else {
          if (!textInput.trim() || textInput.trim().length < 30) {
            alert('Please paste a document with at least 30 characters.');
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Analyze Document';
            return;
          }
          formData.append('text', textInput);
          formData.append('persona', persona);
        }

        const res = await fetch(endpoint, { method: 'POST', body: formData });
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || 'Analysis failed');
        }

        // Render Results
        riskBadge.className = `badge-risk risk-${data.risk_level}`;
        riskBadge.innerText = `${data.risk_level} Risk`;

        const highCount = data.clauses.filter(c => c.weighted_severity >= 7).length;

        let clausesHtml = data.clauses.map(c => {
          const sevClass = c.weighted_severity >= 7 ? 'sev-high' : (c.weighted_severity >= 4 ? 'sev-med' : 'sev-low');
          return `
            <div class="clause-item ${sevClass}">
              <div class="clause-header">
                <span class="clause-title">${c.clause_label}</span>
                <span class="clause-line">Line ${c.line_number} • Severity ${c.weighted_severity}/10</span>
              </div>
              <div style="font-size: 13px; color: #cbd5e1; margin-bottom: 6px;"><em>"${c.line_text}"</em></div>
              <div class="clause-why"><strong>Why it matters:</strong> ${c.why_it_matters}</div>
              ${c.negotiation_tip ? `<div class="clause-tip">💡 <strong>Negotiation Tip:</strong> ${c.negotiation_tip}</div>` : ''}
            </div>
          `;
        }).join('');

        let questionsHtml = (data.questions_to_ask || []).map(q => `<li>${q}</li>`).join('');

        resultsDiv.innerHTML = `
          <div class="metrics-grid">
            <div class="metric-box">
              <div class="metric-val">${data.total_clauses_found}</div>
              <div class="metric-lbl">Clauses Detected</div>
            </div>
            <div class="metric-box">
              <div class="metric-val">${data.average_severity}</div>
              <div class="metric-lbl">Avg Severity</div>
            </div>
            <div class="metric-box">
              <div class="metric-val" style="color: var(--danger)">${highCount}</div>
              <div class="metric-lbl">High Risk Items</div>
            </div>
          </div>

          <div style="margin-bottom: 20px;">
            <h4 style="font-size: 14px; margin-bottom: 8px; color: var(--accent);">Key Questions to Ask:</h4>
            <ul style="padding-left: 20px; font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">
              ${questionsHtml}
            </ul>
          </div>

          <h4 style="font-size: 15px; margin-bottom: 12px; border-bottom: 1px solid var(--border); padding-bottom: 8px;">
            Detected Clause Breakdown
          </h4>
          <div>${clausesHtml || '<p style="color: var(--text-muted)">No high-risk clauses matching pattern rules were detected.</p>'}</div>
        `;

      } catch (err) {
        alert('Error: ' + err.message);
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Analyze Document';
      }
    });
  </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root():
    """Web application dashboard."""
    return HTMLResponse(content=INDEX_HTML)


@app.get("/api/samples/{persona_id}")
async def get_sample(persona_id: str):
    """Serve sample review documents for each persona option."""
    file_map = {
        "tenant": "samples/sample_tenant_lease.txt",
        "employee": "samples/sample_employee_contract.txt",
        "freelancer": "samples/sample_freelancer_msa.txt",
        "consumer": "samples/sample_consumer_tos.txt",
        "founder": "samples/sample_founder_partnership.txt",
        "buyer": "samples/sample_buyer_loan.txt",
        "other": "samples/sample_general_contract.txt",
    }
    rel_path = file_map.get(persona_id, "samples/sample_general_contract.txt")
    full_path = os.path.join(_PROJECT_ROOT, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return {"persona_id": persona_id, "filename": os.path.basename(rel_path), "text": f.read()}
    raise HTTPException(status_code=404, detail="Sample file not found")




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
