"""Small provider-agnostic LLM client.

This intentionally mirrors the useful API idea from `per-chaos-ad-ordinem`:
OpenAI-compatible providers, Anthropic, Gemini and Ollama share one interface,
and failures degrade to deterministic local behavior.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request

from backend.config import LLMConfig


class LLMError(RuntimeError):
    """Raised when every configured provider fails."""


USER_AGENT = "Mozilla/5.0 (compatible; Lucerna65/0.1; +https://example.local/)"
MAX_RETRIES = 2
MAX_RETRY_WAIT = 12


def _extract_json(text: str):
    value = (text or "").strip()
    value = re.sub(r"^```(?:json)?|```$", "", value, flags=re.I | re.M).strip()
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        pass
    match = re.search(r"(\{.*\}|\[.*\])", value, flags=re.S)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def _retry_after_seconds(exc: urllib.error.HTTPError, body: str) -> float:
    header = exc.headers.get("Retry-After") if exc.headers else None
    if header:
        try:
            return float(header)
        except ValueError:
            pass
    match = re.search(r"try again in ([\d.]+)s", body)
    return float(match.group(1)) + 0.5 if match else 5.0


def _post(url: str, payload: dict, headers: dict, timeout: int) -> dict:
    data = json.dumps(payload).encode("utf-8")
    merged = {"User-Agent": USER_AGENT, "Accept": "application/json", **headers}
    for attempt in range(MAX_RETRIES + 1):
        req = urllib.request.Request(url, data=data, headers=merged, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "ignore")[:500]
            wait = _retry_after_seconds(exc, body)
            if exc.code == 429 and attempt < MAX_RETRIES and wait <= MAX_RETRY_WAIT:
                time.sleep(wait)
                continue
            if exc.code == 429:
                raise LLMError(f"429 rate limit; retry after about {wait:.0f}s") from exc
            raise LLMError(f"{exc.code} {exc.reason}: {body}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise LLMError(f"network: {exc}") from exc
    raise LLMError("persistent provider failure")


class LLMClient:
    def __init__(self, config: LLMConfig):
        self.config = config

    @property
    def enabled(self) -> bool:
        return self.config.enabled

    @property
    def provider(self) -> str:
        return self.config.provider

    def complete(self, system: str, user: str, *, temperature: float = 0.2,
                 max_tokens: int = 1200, want_json: bool = False) -> str:
        if not self.enabled:
            raise LLMError("LLM not configured")
        if self.config.kind == "openai_compatible":
            return self._openai(system, user, temperature, max_tokens, want_json)
        if self.config.kind == "anthropic":
            return self._anthropic(system, user, temperature, max_tokens)
        if self.config.kind == "gemini":
            return self._gemini(system, user, temperature, max_tokens, want_json)
        raise LLMError(f"unknown LLM kind: {self.config.kind}")

    def complete_json(self, system: str, user: str, **kwargs):
        parsed = _extract_json(self.complete(system, user, want_json=True, **kwargs))
        if parsed is None:
            raise LLMError("provider returned non-JSON content")
        return parsed

    def _openai(self, system: str, user: str, temperature: float, max_tokens: int,
                want_json: bool) -> str:
        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if want_json:
            payload["response_format"] = {"type": "json_object"}
        data = _post(url, payload, headers, self.config.timeout)
        try:
            return data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"unexpected response: {str(data)[:300]}") from exc

    def _anthropic(self, system: str, user: str, temperature: float, max_tokens: int) -> str:
        url = f"{self.config.base_url.rstrip('/')}/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
        }
        payload = {
            "model": self.config.model,
            "system": system,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": user}],
        }
        data = _post(url, payload, headers, self.config.timeout)
        try:
            return "".join(part.get("text", "") for part in data["content"])
        except (KeyError, TypeError) as exc:
            raise LLMError(f"unexpected response: {str(data)[:300]}") from exc

    def _gemini(self, system: str, user: str, temperature: float, max_tokens: int,
                want_json: bool) -> str:
        url = f"{self.config.base_url.rstrip('/')}/models/{self.config.model}:generateContent?key={self.config.api_key}"
        generation = {"temperature": temperature, "maxOutputTokens": max_tokens}
        if want_json:
            generation["responseMimeType"] = "application/json"
        payload = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": generation,
        }
        data = _post(url, payload, {"Content-Type": "application/json"}, self.config.timeout)
        try:
            return "".join(part.get("text", "") for part in data["candidates"][0]["content"]["parts"])
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"unexpected response: {str(data)[:300]}") from exc


class LLMChain:
    def __init__(self, configs: list[LLMConfig]):
        self.clients = [LLMClient(config) for config in configs if config.enabled]
        self.last_used = ""
        self.failovers: list[str] = []
        self.cooldown: set[str] = set()

    @property
    def enabled(self) -> bool:
        return bool(self.clients)

    def complete_json(self, system: str, user: str, **kwargs):
        return self._run("complete_json", system, user, **kwargs)

    def complete(self, system: str, user: str, **kwargs):
        return self._run("complete", system, user, **kwargs)

    def _run(self, method: str, system: str, user: str, **kwargs):
        active = [client for client in self.clients if client.provider not in self.cooldown]
        if not active:
            raise LLMError("no LLM provider available")
        last_error: Exception | None = None
        for index, client in enumerate(active):
            try:
                result = getattr(client, method)(system, user, **kwargs)
                self.last_used = client.provider
                return result
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if "429" in str(exc):
                    self.cooldown.add(client.provider)
                if index + 1 < len(active):
                    self.failovers.append(f"{client.provider} failed; trying {active[index + 1].provider}")
        raise LLMError(str(last_error) if last_error else "all providers failed")


def build_llm(cfg) -> LLMChain:
    return LLMChain(cfg.llm_chain)
