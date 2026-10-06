from abc import ABC, abstractmethod
from typing import Any, Dict

from src.models import ToolExecutionResult

class ITool(ABC):
    @abstractmethod
    def execute(self, **kwargs: Any) -> ToolExecutionResult:
        ...

    @abstractmethod
    def get_name(self) -> str:
        ...

    @abstractmethod
    def get_description(self) -> str:
        ...

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        ...
