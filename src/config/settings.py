from __future__ import annotations

import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

@dataclass
class Settings:
    ollama_base_url: str = "http://localhost:11434"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    nvidia_api_key: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ollama_base_url or not self.ollama_base_url.strip():
            raise ValueError(
                "Settings.ollama_base_url must be a non-empty URL. "
                "Check OLLAMA_BASE_URL in your .env file, or omit it to use "
                "the default http://localhost:11434."
            )
        if not (
            self.ollama_base_url.startswith("http://")
            or self.ollama_base_url.startswith("https://")
        ):
            raise ValueError(
                f"Settings.ollama_base_url must start with http:// or https:// "
                f"— got {self.ollama_base_url!r}. Check OLLAMA_BASE_URL in your .env file."
            )
        if self.openai_api_key is not None and not self.openai_api_key.strip():
            raise ValueError(
                "OPENAI_API_KEY is set but empty. Remove the line from .env "
                "entirely if you don't intend to use the OpenAI provider, rather "
                "than leaving it blank."
            )
        if self.anthropic_api_key is not None and not self.anthropic_api_key.strip():
            raise ValueError(
                "ANTHROPIC_API_KEY is set but empty. Remove the line from .env "
                "entirely if you don't intend to use the Anthropic provider, "
                "rather than leaving it blank."
            )
        if self.nvidia_api_key is not None and not self.nvidia_api_key.strip():
            raise ValueError(
                "NVIDI_AAPI_KEY is set but empty. Remove the line from .env "
                "entirely if you don't intend to use the Nvidia provider, "
                "rather than leaving it blank."
            )
        
    @classmethod
    def from_env(cls, dotenv_path: Optional[str] = None) -> Settings:
        # load_dotenv() populates os.environ from a .env file if one is found
        # (cwd by default, or an explicit dotenv_path). It does NOT override
        # a variable that's already set in the real process environment —
        # see the integration_notes facet for exactly why that default matters.
        load_dotenv(dotenv_path)
        return cls(
            ollama_base_url=os.environ.get(
                "OLLAMA_BASE_URL", "http://localhost:11434"
            ),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            nvidia_api_key=os.environ.get("NVIDIA_API_KEY")
        )