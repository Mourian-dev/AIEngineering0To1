#NVIDIA accessed via openAI provider
from typing import Optional
from src.enums import Provider
from src.provider.openai_provider import OpenAIProvider

class NvidiaProvider(OpenAIProvider):
    def __init__(self, api_key: str, model: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(
            api_key, 
            model or "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning", 
            base_url or "https://integrate.api.nvidia.com/v1"
        )

    def get_provider_name(self) -> str:
        return Provider.NVIDIA.value