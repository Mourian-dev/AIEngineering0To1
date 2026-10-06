from typing import Optional, Dict, List, Any

from src.interface.platform import IPlatformProvider
from src.enums import Provider

class ProviderFactory:
    _providers: Dict[Provider, IPlatformProvider] = {}

    @classmethod
    def register(cls, provider_type: Provider, provider_class: type[IPlatformProvider]) -> None:
        cls._providers[provider_type] = provider_class

    @classmethod
    def create(cls, provider_type: Provider, api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None) -> IPlatformProvider:
        if provider_type not in cls._providers:
            raise ValueError(f"No provider registered for {provider_type}")
        provider_class = cls._providers[provider_type]

        kwargs: Dict[str, Any] = {}
        if api_key is not None:
            kwargs["api_key"] = api_key or None
        if base_url is not None:
            kwargs["base_url"] = base_url or None
        return provider_class(model = model, **kwargs)