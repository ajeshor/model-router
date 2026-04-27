"""Model router — DeepSeek primary, Llama 3.1 8B local fallback via Ollama."""

import json
import logging
import urllib.request
import urllib.error
from typing import Optional

logger = logging.getLogger(__name__)

OLLAMA_ENDPOINT = "http://127.0.0.1:11434/api/generate"
LLAMA_MODEL = "llama3.1:8b"
FALLBACK_TIMEOUT = 30


def _query_ollama(prompt: str, model: str = LLAMA_MODEL, timeout: int = FALLBACK_TIMEOUT) -> Optional[str]:
    payload = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"num_predict": 512, "temperature": 0.3}
    }).encode()
    try:
        req = urllib.request.Request(OLLAMA_ENDPOINT, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode())
            return result.get("response", "").strip()
    except Exception as e:
        logger.error(f"Ollama query failed: {e}")
        return None


def query(prompt: str, prefer_local: bool = False, timeout: int = 15) -> str:
    result = _query_ollama(prompt)
    return result or "⚠️ Model unavailable. Please try again."


def health_check() -> dict:
    status = {"ollama": False, "llama_loaded": False}
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=5) as resp:
            models = json.loads(resp.read().decode())
            status["ollama"] = True
            status["llama_loaded"] = any(
                m["name"].startswith(LLAMA_MODEL) for m in models.get("models", [])
            )
    except Exception:
        pass
    return status
