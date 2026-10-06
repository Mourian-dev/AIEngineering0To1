from typing import Any, Dict, Optional, List
from src.enums import Provider
from src.models import ChatCompletionResponse
from src.interface.platform import IPlatformProvider

import ollama

class OllamaProvider(IPlatformProvider):
    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> None:
        self.model = model or "llama3.2"
        self._client = ollama.Client(host=base_url)

    def generate(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> ChatCompletionResponse:
        try:
            raw: ollama.ChatResponse = self._client.chat(
                model = self.model,
                messages = messages,
                tools = tools
            )
        except (ollama.ResponseError, ollama.RequestError, ConnectionError) as exc:
            return ChatCompletionResponse(
                success=False,
                content='',
                model=self.model,
                provider=Provider.OLLAMA,
                tokens_input=0,
                tokens_output=0,
                cost=0.0,
                stop_reason="error",
                error=str(exc)
            )

        return ChatCompletionResponse(
                success=True,
                content=raw.message.content or "",
                model=raw.model or self.model,
                provider=Provider.OLLAMA,
                tokens_input=raw.prompt_eval_count or 0,
                tokens_output=raw.eval_count or 0,
                cost=0.0,
                stop_reason=raw.done_reason or "stop",
            )

    def get_provider_name(self) -> str:
        return Provider.OLLAMA

    def validate_config(self) -> bool:
        try:
            self._client.list()
            return True
        except(ollama.ResponseError, ollama.RequestError, ConnectionError):
            return False

    def get_pricing(self) -> Dict[str, float]:
        return {"input_per_1k": 0.0, "output_per_1k": 0.0}