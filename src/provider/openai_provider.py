from typing import Any, Optional, List, Dict

import openai
from openai.types.chat import ChatCompletion

from src.enums import Provider
from src.interface.platform import IPlatformProvider
from src.models import ChatCompletionResponse

class OpenAIProvider(IPlatformProvider):
    def __init__(self, api_key: str, model: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.model = model or "gpt-4o-mini"
        self._client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = None) -> ChatCompletionResponse:
        create_kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages
        }

        if tools is not None:
            create_kwargs["tools"] = tools

        try:
            raw: ChatCompletion = self._client.chat.completions.create(**create_kwargs)
        except openai.OpenAIError as exc:
            return ChatCompletionResponse(
                success=False,
                content='',
                model=self.model,
                provider=Provider.OPENAI,
                tokens_input=0,
                tokens_output=0,
                cost=0.0,
                stop_reason="error",
                error=str(exc)
            )
        tokens_input: int = raw.usage.prompt_tokens or 0
        tokens_output: int = raw.usage.completion_tokens or 0
        cost: float = (tokens_input/10000.0) * self.get_pricing()["input_per_1k"] + ( tokens_output / 1000.0) * self.get_pricing()["output_per_1k"]

        return ChatCompletionResponse(
            success=True,
            content=raw.choices[0].message.content or "",
            model=raw.model or self.model,
            provider=Provider.OPENAI,
            tokens_input=raw.usage.prompt_tokens or 0,
            tokens_output=raw.usage.completion_tokens or 0,
            cost=cost,
            stop_reason=raw.choices[0].finish_reason or "stop"
        )

    def get_provider_name(self) -> str:
        return Provider.OPENAI.value

    def validate_config(self) -> bool:
        if not self.api_key:
            return False
        try:
            self._client.models.list()
            return True
        except openai.OpenAIError:
            return False

    def get_pricing(self) -> dict[str, float]:
        # gpt-4o-mini published rate, per 1K tokens, as of this writing.
        return {"input_per_1k": 0.00015, "output_per_1k": 0.0006}
        

        