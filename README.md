# Model Router

**DeepSeek Chat (primary) → Llama 3.1 8B local fallback via Ollama**

Auto-routes queries to the best available LLM backend. DeepSeek is always preferred. Falls back to local Llama 3.1 8B on API failure, timeout, or network outage.

## Installation

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Verify
python3 -c "from src.model_router import health_check; print(health_check())"
```

## Usage

```python
from src.model_router import query, health_check

# Normal query (DeepSeek primary)
response = query("What is the capital of France?")

# Force local inference
response = query("Hello", prefer_local=True)

# Check backend health
status = health_check()
```

## Architecture

```
User Request → Router → DeepSeek Chat (primary)
                        └→ Llama 3.1 8B (fallback on failure)
```

## Requirements

- Python 3.8+
- Ollama (for local fallback)
- 4.9 GB free disk (model download)
- ARM64 or x86_64
