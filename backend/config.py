"""Runtime configuration for LUCERNA 65.

The application runs in an ephemeral demo mode by default. LLM access is
optional and follows the provider pattern used in the source project
`per-chaos-ad-ordinem`: explicit environment variables first, autodetection
second, deterministic local fallback always available.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

_DOTENV_LOADED = False
ROOT = Path(__file__).resolve().parent.parent


def _dotenv_candidates() -> list[Path]:
    """Local config first, then the source project's env as a development bridge.

    Secrets are never hardcoded in LUCERNA 65. In production, Vercel environment
    variables take precedence; locally this lets the prototype reuse the API
    setup already prepared for `per-chaos-ad-ordinem`.
    """
    candidates = [ROOT / ".env"]
    explicit = os.environ.get("PER_CHAOS_ENV_PATH", "").strip()
    if explicit:
        candidates.append(Path(explicit))
    load_source_env = os.environ.get("LUCERNA_LOAD_PER_CHAOS_ENV", "1").strip().lower()
    if load_source_env not in {"0", "false", "no"}:
        candidates.append(ROOT.parent.parent / "per-chaos-ad-ordinem" / ".env")
    return candidates


def _load_dotenv() -> None:
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return
    _DOTENV_LOADED = True
    for path in _dotenv_candidates():
        if not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value and not os.environ.get(key):
                os.environ[key] = value


def env(*names: str, default: str = "") -> str:
    _load_dotenv()
    for name in names:
        value = os.environ.get(name)
        if value:
            return value.strip()
    return default


OPENAI_COMPATIBLE_BASES = {
    "openai": "https://api.openai.com/v1",
    "groq": "https://api.groq.com/openai/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "together": "https://api.together.xyz/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "mistral": "https://api.mistral.ai/v1",
    "ollama": "http://localhost:11434/v1",
}

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "groq": "llama-3.3-70b-versatile",
    "openrouter": "meta-llama/llama-3.3-70b-instruct",
    "together": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "deepseek": "deepseek-chat",
    "mistral": "mistral-small-latest",
    "ollama": "llama3.1",
    "anthropic": "claude-3-5-haiku-latest",
    "gemini": "gemini-2.0-flash",
}


@dataclass
class LLMConfig:
    provider: str = ""
    kind: str = ""
    model: str = ""
    api_key: str = ""
    base_url: str = ""
    timeout: int = 30

    @property
    def enabled(self) -> bool:
        return bool(self.kind) and (bool(self.api_key) or self.provider == "ollama")


@dataclass
class AppConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
    llm_fallbacks: list[LLMConfig] = field(default_factory=list)
    app_env: str = "development"
    data_mode: str = "ephemeral"
    default_locale: str = "ca"
    allowed_origins: list[str] = field(default_factory=lambda: ["*"])
    max_free_text_chars: int = 6000
    public_demo: bool = True

    @property
    def llm_chain(self) -> list[LLMConfig]:
        return [item for item in [self.llm, *self.llm_fallbacks] if item.enabled]

    @property
    def llm_enabled(self) -> bool:
        return bool(self.llm_chain)

    def capabilities(self) -> dict:
        providers = [item.provider for item in self.llm_chain]
        mode = "assistit amb IA" if self.llm_enabled else "determinista local"
        return {
            "name": "LUCERNA 65",
            "mode": mode,
            "llm": {
                "enabled": self.llm_enabled,
                "providers": providers,
                "primaryProvider": providers[0] if providers else "",
                "fallbackProviders": providers[1:],
                "models": [
                    {"provider": item.provider, "model": item.model}
                    for item in self.llm_chain
                ],
                "purpose": (
                    "Extracció prudent de fets observables a partir de text lliure; "
                    "no decideix indicadors, nivell d'atenció ni informe."
                ),
            },
            "dataMode": self.data_mode,
            "storesSensitiveData": False,
            "treeVersion": "2026.1-mvp",
            "reportLocale": ["ca", "es", "en"],
        }


_AUTODETECT = [
    ("gemini", ("GEMINI_API_KEY", "GOOGLE_GENAI_API_KEY")),
    ("groq", ("GROQ_API_KEY",)),
    ("openrouter", ("OPENROUTER_API_KEY",)),
    ("together", ("TOGETHER_API_KEY",)),
    ("deepseek", ("DEEPSEEK_API_KEY",)),
    ("mistral", ("MISTRAL_API_KEY",)),
    ("openai", ("OPENAI_API_KEY",)),
    ("anthropic", ("ANTHROPIC_API_KEY",)),
]


def _build_llm(provider: str, api_key: str, *, model: str = "", base_url: str = "") -> LLMConfig:
    provider = provider.lower().strip()
    if provider == "anthropic":
        kind = "anthropic"
        base_url = base_url or "https://api.anthropic.com/v1"
    elif provider == "gemini":
        kind = "gemini"
        base_url = base_url or "https://generativelanguage.googleapis.com/v1beta"
    else:
        kind = "openai_compatible"
        base_url = base_url or OPENAI_COMPATIBLE_BASES.get(provider, "")
    return LLMConfig(
        provider=provider,
        kind=kind,
        model=model or DEFAULT_MODELS.get(provider, ""),
        api_key=api_key,
        base_url=base_url,
        timeout=int(env("LLM_TIMEOUT", default="30") or "30"),
    )


def _resolve_llm() -> LLMConfig:
    provider = env("LLM_PROVIDER").lower()
    api_key = env("LLM_API_KEY")
    if not provider:
        for candidate, keys in _AUTODETECT:
            key = env(*keys)
            if key:
                provider, api_key = candidate, key
                break
    if not provider:
        return LLMConfig()
    if provider != "ollama" and not api_key:
        api_key = env(f"{provider.upper()}_API_KEY")
    return _build_llm(
        provider,
        api_key,
        model=env("LLM_MODEL"),
        base_url=env("LLM_BASE_URL"),
    )


def _resolve_fallbacks(primary: LLMConfig) -> list[LLMConfig]:
    fallbacks = []
    for provider, keys in _AUTODETECT:
        if provider == primary.provider:
            continue
        key = env(*keys)
        if key:
            fallbacks.append(_build_llm(provider, key))
    return fallbacks


def load_config() -> AppConfig:
    primary = _resolve_llm()
    origins = [item.strip() for item in env("ALLOWED_ORIGINS", default="*").split(",") if item.strip()]
    return AppConfig(
        llm=primary,
        llm_fallbacks=_resolve_fallbacks(primary),
        app_env=env("APP_ENV", default="development").lower(),
        data_mode=env("DATA_MODE", default="ephemeral").lower(),
        default_locale=env("REPORT_LOCALE", default="ca").lower(),
        allowed_origins=origins or ["*"],
        max_free_text_chars=int(env("MAX_FREE_TEXT_CHARS", default="6000") or "6000"),
        public_demo=env("PUBLIC_DEMO", default="1").lower() not in {"0", "false", "no"},
    )
