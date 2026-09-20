"""Runtime configuration for PlainClause.

Every knob is read from the process environment once, behind a cached factory.
The rest of the codebase depends on an immutable settings object rather than
reaching into ``os.environ``, which keeps configuration testable and keeps
secrets out of application code.

No third-party dependency is used here on purpose: the service must be able to
boot in a bare review environment.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Final

DEFAULT_MAX_DOCUMENT_CHARS: Final = 400_000
DEFAULT_MAX_UPLOAD_BYTES: Final = 5 * 1024 * 1024
DEFAULT_RATE_LIMIT_REQUESTS: Final = 90
DEFAULT_RATE_LIMIT_WINDOW_SECONDS: Final = 60
DEFAULT_REQUEST_TIMEOUT_SECONDS: Final = 45.0

PROVIDER_NONE: Final = "none"
SUPPORTED_PROVIDERS: Final = ("gemini", "openai", "anthropic", "openrouter", "ollama")

_KEY_ENV_VARS: Final[dict[str, tuple[str, ...]]] = {
    "gemini": ("PLAINCLAUSE_GEMINI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"),
    "openai": ("PLAINCLAUSE_OPENAI_API_KEY", "OPENAI_API_KEY"),
    "anthropic": ("PLAINCLAUSE_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY"),
    "openrouter": ("PLAINCLAUSE_OPENROUTER_API_KEY", "OPENROUTER_API_KEY"),
}

DEFAULT_MODELS: Final[dict[str, str]] = {
    "gemini": "gemini-2.0-flash",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "openrouter": "google/gemini-2.0-flash-001",
    "ollama": "llama3.2",
}


def _env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int, *, minimum: int = 1) -> int:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        parsed = int(raw.strip())
    except ValueError:
        return default
    return parsed if parsed >= minimum else default


def _env_float(name: str, default: float, *, minimum: float = 1.0) -> float:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        parsed = float(raw.strip())
    except ValueError:
        return default
    return parsed if parsed >= minimum else default


def _first_env(names: tuple[str, ...]) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value and value.strip():
            return value.strip()
    return None


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable, process-wide configuration."""

    app_name: str
    version: str
    provider_override: str | None
    api_keys: dict[str, str] = field(default_factory=dict)
    models: dict[str, str] = field(default_factory=dict)
    ollama_base_url: str = "http://localhost:11434"
    allow_cloud_provider: bool = True
    redact_before_cloud: bool = True
    max_document_chars: int = DEFAULT_MAX_DOCUMENT_CHARS
    max_upload_bytes: int = DEFAULT_MAX_UPLOAD_BYTES
    rate_limit_requests: int = DEFAULT_RATE_LIMIT_REQUESTS
    rate_limit_window_seconds: int = DEFAULT_RATE_LIMIT_WINDOW_SECONDS
    request_timeout_seconds: float = DEFAULT_REQUEST_TIMEOUT_SECONDS
    trust_proxy_headers: bool = False

    @property
    def active_provider(self) -> str:
        """Provider the service will use, or ``none`` for the offline engine."""
        requested = self.provider_override
        if requested == "ollama":
            return "ollama"
        if requested in SUPPORTED_PROVIDERS and self.allow_cloud_provider:
            return requested if self.api_keys.get(requested) else PROVIDER_NONE
        if not self.allow_cloud_provider:
            return PROVIDER_NONE
        for name in SUPPORTED_PROVIDERS:
            if name != "ollama" and self.api_keys.get(name):
                return name
        return PROVIDER_NONE

    @property
    def offline_mode(self) -> bool:
        return self.active_provider == PROVIDER_NONE

    @property
    def cloud_provider_active(self) -> bool:
        return self.active_provider not in (PROVIDER_NONE, "ollama")

    def model_for(self, provider: str) -> str:
        return self.models.get(provider) or DEFAULT_MODELS.get(provider, "")


def build_settings() -> Settings:
    """Read configuration from the environment. Exposed for tests."""
    api_keys: dict[str, str] = {}
    for provider, names in _KEY_ENV_VARS.items():
        value = _first_env(names)
        if value:
            api_keys[provider] = value

    models: dict[str, str] = {}
    for provider, default in DEFAULT_MODELS.items():
        models[provider] = _first_env((f"PLAINCLAUSE_{provider.upper()}_MODEL",)) or default

    override = _first_env(("PLAINCLAUSE_PROVIDER",))
    if override is not None:
        override = override.strip().lower()
        if override not in SUPPORTED_PROVIDERS and override != PROVIDER_NONE:
            override = None

    return Settings(
        app_name="PlainClause",
        version="1.0.0",
        provider_override=override,
        api_keys=api_keys,
        models=models,
        ollama_base_url=_first_env(("PLAINCLAUSE_OLLAMA_BASE_URL",)) or "http://localhost:11434",
        allow_cloud_provider=_env_flag("PLAINCLAUSE_ALLOW_CLOUD", True),
        redact_before_cloud=_env_flag("PLAINCLAUSE_REDACT_BEFORE_CLOUD", True),
        max_document_chars=_env_int("PLAINCLAUSE_MAX_DOCUMENT_CHARS", DEFAULT_MAX_DOCUMENT_CHARS),
        max_upload_bytes=_env_int("PLAINCLAUSE_MAX_UPLOAD_BYTES", DEFAULT_MAX_UPLOAD_BYTES),
        rate_limit_requests=_env_int("PLAINCLAUSE_RATE_LIMIT_REQUESTS", DEFAULT_RATE_LIMIT_REQUESTS),
        rate_limit_window_seconds=_env_int(
            "PLAINCLAUSE_RATE_LIMIT_WINDOW_SECONDS", DEFAULT_RATE_LIMIT_WINDOW_SECONDS
        ),
        request_timeout_seconds=_env_float(
            "PLAINCLAUSE_REQUEST_TIMEOUT_SECONDS", DEFAULT_REQUEST_TIMEOUT_SECONDS
        ),
        trust_proxy_headers=_env_flag("PLAINCLAUSE_TRUST_PROXY", False),
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Process-wide settings singleton."""
    return build_settings()
