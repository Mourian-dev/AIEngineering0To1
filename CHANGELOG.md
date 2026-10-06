## [v0.2.0] - Chapter 1B: Configuration and Secrets Management

### Added
- `Settings` dataclass (`src/config/settings.py`) — fields `ollama_base_url: str`,
  `openai_api_key: Optional[str]`, `anthropic_api_key: Optional[str]`.
- `Settings.__post_init__` — validates that `ollama_base_url` is non-empty and
  URL-shaped, and that any *present* API key is non-blank. Does not require
  `openai_api_key` or `anthropic_api_key` to be present — see the
  `architecture_contract` facet for why that's a deliberate, not accidental,
  omission.
- `Settings.from_env(dotenv_path: Optional[str] = None) -> Settings` classmethod
  — the one place in the entire codebase that calls `os.environ.get(...)` for
  these three values, and the one place that calls `python-dotenv`'s
  `load_dotenv()`.
- `.env.example` (committed to version control) documenting every variable
  `Settings.from_env()` reads, with placeholder values.
- `.env` (real local file, **not** committed — see `.gitignore`, covered in
  the `verification` facet).
- `python-dotenv` added to `requirements.txt`.

### Changed
- `ask.py`'s `main()`: removed `import os`; added
  `import Settings from src.config.settings`; added one line,
  `settings = Settings.from_env()`, immediately after argument parsing.
- `ask.py`'s three provider-construction branches (`Provider.OLLAMA`,
  `Provider.OPENAI`, `Provider.ANTHROPIC`) now read `settings.ollama_base_url`,
  `settings.openai_api_key`, `settings.anthropic_api_key` respectively, in
  place of a hardcoded literal (`"http://localhost:11434"`) and two inline
  `os.environ.get(...)` calls.
  **Non-breaking, and here's why that claim is checkable rather than assumed:**
  `ProviderFactory.create(provider_type, api_key=None, model=None, base_url=None)`
  is called at each of these three sites with the exact same keyword arguments,
  in the exact same positions, as in Chapter 1 — only the *expression* supplying
  each argument's value changed (`settings.openai_api_key` instead of a local
  variable assigned from `os.environ.get(...)`). `src/provider/factory.py` has
  zero lines changed in this version; run `git diff` against it yourself and
  confirm the file is untouched.
- The missing-credential error message's wording changed (still a
  `RuntimeError`, still raised from the same two `elif` branches) to point at
  `.env` / `.env.example` as the sanctioned place to supply the key, rather
  than only naming the environment variable.

### Deprecated
- Nothing. The inline `os.environ.get(...)` pattern from Chapter 1 is not
  marked deprecated-and-still-running with an expiry — it is deleted outright,
  in the same diff that introduces `Settings`. This is different from how
  Refactor Checkpoint 1 (`v0.6.0`) handles its own deprecation of inline
  message-translation logic, which genuinely needed a real expiry window
  (removing it immediately would have meant rewriting three provider classes
  in the same commit that introduces the new formatter interface — a much
  larger, riskier single change). Here, the old mechanism and the new
  mechanism are both one-line reads; there is no migration cost that justifies
  leaving a dead code path running alongside its replacement, so none is left.

### Removed
- The two inline `os.environ.get("OPENAI_API_KEY")` /
  `os.environ.get("ANTHROPIC_API_KEY")` calls, and the hardcoded
  `"http://localhost:11434"` literal, previously written directly inside
  `ask.py`'s `main()`.