import argparse
import os
import sys
from typing import NoReturn, List, Dict

from src.client.llm_client import LLMClient
from src.enums import Provider
from src.provider.anthropic_provider import AnthropicProvider
from src.provider.openai_provider import OpenAIProvider
from src.provider.ollama_provider import OllamaProvider
from src.provider.nvidia_provider import NvidiaProvider
from src.provider.factory import ProviderFactory

ProviderFactory.register(Provider.OLLAMA, OllamaProvider)
ProviderFactory.register(Provider.OPENAI, OpenAIProvider)
ProviderFactory.register(Provider.ANTHROPIC, AnthropicProvider)
ProviderFactory.register(Provider.NVIDIA, NvidiaProvider)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ask any question of a real LLM Provider and print the answer, cost and token usage."
    )
    parser.add_argument(
        "--provider",
        required=True,
        choices=["ollama", "anthropic", "openai", "nvidia"]
    )
    parser.add_argument(
        "--question",
        required=True,
        help="The question to ask the model."
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override the provider's default model."
    )
    parser.add_argument(
        "--system",
        default=None,
        help="An optional system prompt."
    )
    return parser

def fail(message: str) -> NoReturn:
    print(message, file=sys.stderr)
    sys.exit(1)

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    provider_type = Provider(args.provider)

    api_key = None
    if provider_type is Provider.OPENAI:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            fail("OPENAI_API_KEY is not set in the environment.")
    elif provider_type is Provider.ANTHROPIC:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            fail("ANTHROPIC_API_KEY is not set in the environment.")
    elif provider_type is Provider.NVIDIA:
        api_key = os.environ.get("NVIDIA_API_KEY")
        if not api_key:
            fail("NVIDIA_API_KEY is not set in th eenvironment")

    create_kwargs: dict[str, str] = {}
    if api_key is not None:
        create_kwargs["api_key"] = api_key
    if args.model is not None:
        create_kwargs["model"] = args.model
    provider = ProviderFactory.create(provider_type, **create_kwargs)

    client:LLMClient = LLMClient(provider=provider)
    messages: List[Dict[str, str]] = []

    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": args.question})

    response = client.generate(messages, tools=None)
    print(response.content)
    print(
        f"\n[provider={response.provider.value} model={response.model} "
        f"tokens_in={response.tokens_input} tokens_out={response.tokens_output} "
        f"cost=${response.cost:.6f} total_cost=${client.get_total_cost():.6f}]"
    )


if __name__ == "__main__":
    main()