"""Tests for the PlainClause FastAPI web service."""

import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


# ---------------------------------------------------------------------------
# Health & root
# ---------------------------------------------------------------------------
class TestHealthEndpoints:
    def test_root_returns_200(self):
        r = client.get("/")
        assert r.status_code == 200
        assert "PlainClause" in r.text
        assert "Document Analysis" in r.text

    def test_health_returns_ok(self):
        r = client.get("/api/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# Personas
# ---------------------------------------------------------------------------
class TestPersonas:
    def test_list_personas(self):
        r = client.get("/api/personas")
        assert r.status_code == 200
        personas = r.json()["personas"]
        assert len(personas) >= 7
        ids = [p["id"] for p in personas]
        assert "tenant" in ids
        assert "employee" in ids
        assert "other" in ids

    def test_persona_has_required_fields(self):
        r = client.get("/api/personas")
        p = r.json()["personas"][0]
        for key in ("id", "label", "blurb", "questions", "documents_to_gather"):
            assert key in p, f"missing field: {key}"


# ---------------------------------------------------------------------------
# Analyze (text)
# ---------------------------------------------------------------------------
SAMPLE_LEASE = (
    "RESIDENTIAL LEASE AGREEMENT\\n"
    "This Lease Agreement is made between Landlord and Tenant.\\n"
    "The lease shall automatically renew for successive one-year terms "
    "unless either party provides written notice.\\n"
    "Tenant shall pay monthly rent of $1,500.00, payable in advance on "
    "the first day of each month. Rent shall be considered late if not "
    "received by the fifth day, at which time a late fee of $50 shall be assessed.\\n"
    "Tenant shall deposit with Landlord the sum of $1,500.00 as security deposit.\\n"
    "Landlord shall have the right to enter the premises upon twenty-four hours notice.\\n"
    "This Agreement shall be governed by the laws of the State of California."
)


class TestAnalyze:
    def test_analyze_sample_lease(self):
        r = client.post(
            "/api/analyze",
            data={"text": SAMPLE_LEASE, "persona": "tenant"},
        )
        assert r.status_code == 200
        body = r.json()
        assert body["persona"] == "Tenant or flatmate"
        assert body["total_clauses_found"] >= 1
        assert "risk_level" in body

    def test_analyze_default_persona(self):
        r = client.post("/api/analyze", data={"text": SAMPLE_LEASE})
        assert r.status_code == 200
        assert r.json()["persona_id"] == "other"

    def test_analyze_bad_persona_rejected(self):
        r = client.post(
            "/api/analyze",
            data={"text": SAMPLE_LEASE, "persona": "alien"},
        )
        assert r.status_code == 422

    def test_analyze_short_text_rejected(self):
        r = client.post("/api/analyze", data={"text": "Hi"})
        assert r.status_code == 422


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------
class TestUpload:
    def test_upload_txt_file(self):
        content = SAMPLE_LEASE.encode("utf-8")
        r = client.post(
            "/api/analyze/upload",
            files={"file": ("lease.txt", content, "text/plain")},
            data={"persona": "tenant"},
        )
        assert r.status_code == 200
        assert r.json()["total_clauses_found"] >= 1


# ---------------------------------------------------------------------------
# Samples
# ---------------------------------------------------------------------------
class TestSamples:
    @pytest.mark.parametrize(
        "persona_id",
        ["tenant", "employee", "freelancer", "consumer", "founder", "buyer", "other"],
    )
    def test_get_sample_document(self, persona_id):
        r = client.get(f"/api/samples/{persona_id}")
        assert r.status_code == 200
        data = r.json()
        assert data["persona_id"] == persona_id
        assert len(data["text"]) > 100

