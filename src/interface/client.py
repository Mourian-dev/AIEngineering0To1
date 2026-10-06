from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any

from src.models import ChatCompletionResponse, CostAnalysis
from src.interface.platform import IPlatformProvider

class ILLMClient(ABC):
    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> ChatCompletionResponse:
        ...

    @abstractmethod
    def switch_provider(self, provider: IPlatformProvider) -> None:
        ...

    @abstractmethod
    def get_total_cost(self) -> float:
        ...

    @abstractmethod
    def get_cost_analysis(self) -> CostAnalysis:
        ...

    