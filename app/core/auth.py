"""Authentication & Security module for PlainClause.

Manages user sessions, authentication tokens, and pre-configured demo credentials.
"""

from __future__ import annotations

import secrets
from typing import Dict, Any, Optional

# Pre-configured Demo Users for easy demonstration
DEMO_USERS: Dict[str, Dict[str, str]] = {
    "demo@plainclause.com": {
        "username": "demo@plainclause.com",
        "password": "demo123Password!",
        "name": "Alex Taylor (Demo User)",
        "role": "Premium Reviewer",
    },
    "legal.admin": {
        "username": "legal.admin",
        "password": "admin123Password!",
        "name": "Sarah Jenkins (Legal Admin)",
        "role": "Chief Legal Counsel",
    },
    "tenant.reviewer": {
        "username": "tenant.reviewer",
        "password": "password123",
        "name": "Jordan Lee (Tenant)",
        "role": "Standard Reviewer",
    },
}

# Active session tokens storage (in-memory)
ACTIVE_SESSIONS: Dict[str, Dict[str, str]] = {}


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Validate username and password, returning user info and session token if valid."""
    user = DEMO_USERS.get(username.strip().lower())
    if not user:
        # Check by lowercase or username fallback
        for u_key, u_data in DEMO_USERS.items():
            if u_data["username"].lower() == username.strip().lower():
                user = u_data
                break

    if user and user["password"] == password:
        token = secrets.token_hex(16)
        session_info = {
            "token": token,
            "username": user["username"],
            "name": user["name"],
            "role": user["role"],
        }
        ACTIVE_SESSIONS[token] = session_info
        return session_info

    return None


def verify_session(token: str) -> Optional[Dict[str, str]]:
    """Verify an active session token."""
    return ACTIVE_SESSIONS.get(token)


def invalidate_session(token: str) -> bool:
    """Log out a user by removing their session token."""
    if token in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[token]
        return True
    return False
