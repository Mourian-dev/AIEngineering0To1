from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Dict

from src.enums import Provider

@dataclass
class ChatCompletionResponse:
    success: bool
    content: str
    model: str
    provider: Provider
    tokens_input: int
    tokens_output: int
    cost: float
    stop_reason: str
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.tokens_input + self.tokens_output

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "content": self.content,
            "model": self.model,
            "provider": self.provider.value,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "cost": self.cost,
            "stop_reason": self.stop_reason,
            "error": self.error,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

@dataclass
class ToolCallRequest:
    tool_name: str
    args: Dict[str, Any]
    call_id: str

@dataclass
class ToolExecutionResult:
    success: bool
    output: str
    tool_name: str
    call_id: str
    error: Optional[str] = None
    execution_time_ms: float = 0.0

@dataclass
class AgentResponse:
    success: bool
    message: str
    cost: float
    tool_calls_made: int = 0
    error: Optional[str] = None

@dataclass
class CostAnalysis:
    total_cost: float
    total_requests: int
    total_tokens: int

    @property
    def cost_per_request(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_cost / self.total_requests

