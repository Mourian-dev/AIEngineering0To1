from typing import Optional, Dict

from src.interface.platform import IPlatformProvider
from src.enums import Provider

class ProviderFactory:
    _providers: Dict[Provider, IPlatformProvider] = {}

    @classmethod
    def create(
        cls,
        provider_type: Provider,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> IPlatformProvider:
        if provider_type not in cls._providers:
            raise ValueError(f"No provider registered for {provider_type}")
        provider_class = cls._providers[provider_type]
        ...