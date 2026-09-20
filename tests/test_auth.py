"""Tests for Authentication & Security endpoints."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.auth import authenticate_user, verify_session, invalidate_session

client = TestClient(app)


class TestAuthEngine:
    def test_authenticate_demo_user_success(self):
        session = authenticate_user("demo@plainclause.com", "demo123Password!")
        assert session is not None
        assert session["username"] == "demo@plainclause.com"
        assert session["role"] == "Premium Reviewer"
        assert "token" in session

    def test_authenticate_admin_user_success(self):
        session = authenticate_user("legal.admin", "admin123Password!")
        assert session is not None
        assert session["role"] == "Chief Legal Counsel"

    def test_authenticate_bad_credentials_fails(self):
        session = authenticate_user("demo@plainclause.com", "wrongpassword")
        assert session is None

    def test_login_api_endpoint_success(self):
        r = client.post(
            "/api/login",
            json={"username": "demo@plainclause.com", "password": "demo123Password!"},
        )
        assert r.status_code == 200
        data = r.json()
        assert data["success"] is True
        assert data["session"]["username"] == "demo@plainclause.com"

        token = data["session"]["token"]

        # Verify auth/me
        r_me = client.get(f"/api/auth/me?token={token}")
        assert r_me.status_code == 200
        assert r_me.json()["user"]["username"] == "demo@plainclause.com"

    def test_login_api_endpoint_failure(self):
        r = client.post(
            "/api/login",
            json={"username": "wrong", "password": "wrong"},
        )
        assert r.status_code == 401
