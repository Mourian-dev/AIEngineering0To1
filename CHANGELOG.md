## [v0.1.0] - Chapter 1: Your First Real LLM Call

### Added
- `OllamaProvider` (`src/provider/ollama_provider.py`) — implements `IPlatformProvider`
  against Ollama's native `/api/chat` endpoint. No API key; `validate_config()`
  checks server reachability via `GET {base_url}/api/tags` instead.
- `OpenAIProvider` (`src/provider/openai_provider.py`) — implements `IPlatformProvider`
  against OpenAI's Chat Completions API (`POST /v1/chat/completions`).
- `NvidiaProvider` (`src/provider/nvidia_provider.py`) — extends `OpenAIProvider`
  against OpenAI's Chat Completions API (`POST /v1/chat/completions`).
- `AnthropicProvider` (`src/provider/anthropic_provider.py`) — implements
  `IPlatformProvider` against Anthropic's Messages API (`POST /v1/messages`).
  `generate()` extracts any `role: "system"` entry out of the incoming `messages`
  list and sends it as a separate top-level `system=` parameter, since Anthropic
  rejects a `system`-roled entry inside `messages` itself.
- `LLMClient` (`src/client/llm_client.py`) — implements `ILLMClient`. Wraps a single
  `IPlatformProvider` instance; accumulates total cost and total request count
  across calls, independent of which provider answered any individual call.
- `ask.py` — a CLI entry point. Accepts `--provider {ollama,openai,anthropic}`,
  `--question` (required), `--model` (optional override), `--system` (optional).
  Reads `OPENAI_API_KEY`/`ANTHROPIC_API_KEY` via raw, inline `os.environ.get(...)`
  calls directly inside `main()` — no configuration layer, no `.env` support.

### Changed
- (none — this is the first real implementation of the `v0.0.1` contract; there is
  no pre-existing concrete class in the system for this chapter to have changed
  the shape of)

### Deprecated
- (none this version — see note below on `ask.py`'s configuration approach, which
  is intentionally *not* marked deprecated yet)

### Removed
- (none this version)