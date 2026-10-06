from typing import Any, Optional, List, Dict

import anthropic
from anthropic.types.message import Message

from src.enums import Provider
from src.interface.platform import IPlatformProvider
from src.models import ChatCompletionResponse


class AnthropicProvider(IPlatformProvider):
    DEFAULT_MAX_TOKENS = 1024

    def __init__(
        self,
        api_key: str,
        model: Optional[str] = None,
    ) -> None:
        self.api_key = api_key
        self.model = model or "claude-haiku-4-5"
        self._client = anthropic.Anthropic(api_key=self.api_key)

    def generate(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> "ChatCompletionResponse":
        system_parts: List[str] = []
        remaining_messages: List[Dict[str, Any]] = []
        for message in messages:
            if message.get("role") == "system":
                system_parts.append(message.get("content", ""))
            else:
                remaining_messages.append(message)

        create_kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.DEFAULT_MAX_TOKENS,
            "messages": remaining_messages,
        }
        if system_parts:
            create_kwargs["system"] = "\n".join(system_parts)
        if tools is not None:
            create_kwargs["tools"] = tools

        try:
            raw: Message = self._client.messages.create(**create_kwargs)
        except anthropic.AnthropicError as exc:
            return ChatCompletionResponse(
                success=False,
                content="",
                model=self.model,
                provider=Provider.ANTHROPIC,
                tokens_input=0,
                tokens_output=0,
                cost=0.0,
                stop_reason="error",
                error=str(exc),
            )

        text = ""
        for block in raw.content:
            if block.type == "text":
                text = block.text
                break

        usage = raw.usage
        tokens_input = usage.input_tokens if usage else 0
        tokens_output = usage.output_tokens if usage else 0
        pricing = self.get_pricing()
        cost = (tokens_input / 1000.0) * pricing["input_per_1k"] + (
            tokens_output / 1000.0
        ) * pricing["output_per_1k"]

        return ChatCompletionResponse(
            success=True,
            content=text,
            model=raw.model or self.model,
            provider=Provider.ANTHROPIC,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            cost=cost,
            stop_reason=raw.stop_reason or "end_turn",
        )

    def get_provider_name(self) -> str:
        return Provider.ANTHROPIC.value

    def validate_config(self) -> bool:
        if not self.api_key:
            return False
        try:
            self._client.models.list()
            return True
        except anthropic.AnthropicError:
            return False

    def get_pricing(self) -> Dict[str, float]:
        # claude-haiku-4-5 published rate, per 1K tokens, as of this writing.
        return {"input_per_1k": 0.001, "output_per_1k": 0.005}