from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.models import ChatCompletionResponse

class IPlatformProvider(ABC):
    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> "ChatCompletionResponse":
        ...

    @abstractmethod
    def get_provider_name(self) -> str:
        ...

    @abstractmethod
    def validate_config(self) -> bool:
        ...

    @abstractmethod
    def get_pricing(self) -> Dict[str, float]:
        ...