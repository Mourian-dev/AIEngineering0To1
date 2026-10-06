from enum import Enum
from typing import List

class Provider(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    NVIDIA = "nvidia"

    @classmethod
    def get_all(cls) -> List[Provider]:
        return List[cls]

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

    def is_user_message(self) -> bool:
        return self is MessageRole.USER

    def is_assistant_message(self) -> bool:
        return self is MessageRole.ASSISTANT

class ToolType(str, Enum):
    CALCULATOR = "calculator"
    WEB_SEARCH = "web_search"
    FILE_READ = "file_read"
    CODE_ANALYSIS = "code_analysis"
    CODE_EXECUTION = "code_execution"
    CUSTOM = "custom"