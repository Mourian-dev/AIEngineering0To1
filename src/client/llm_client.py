from typing import Any, Optional, Dict, List

from src.interface.client import ILLMClient
from src.interface.platform import IPlatformProvider
from src.models import ChatCompletionResponse, CostAnalysis

class LLMClient(ILLMClient):
    def __init__(self, provider: IPlatformProvider) -> None:
        self.provider = provider
        self._total_cost = 0.0
        self._total_request = 0
        self._total_tokens = 0

    def generate(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = None) -> ChatCompletionResponse:
        response: ChatCompletionResponse = self.provider.generate(messages=messages, tools=tools)
        self._total_request += 1
        self._total_cost += response.cost
        self._total_tokens += response.total_tokens
        return response

    def switch_provider(self, provider: IPlatformProvider) -> None:
        self.provider = provider

    def get_total_cost(self):
        return self._total_cost

    def get_cost_analysis(self) -> CostAnalysis:
        return CostAnalysis(
            total_cost=self._total_cost,
            total_requests=self._total_request,
            total_tokens=self._total_tokens
        )
        