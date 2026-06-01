"""Shared factory for creating LLM instances in chain classes."""

import os


def create_llm(model, api_key=None, temperature=0.0, api_base=None, provider=None):
    if provider == "litellm":
        from demogpt_agenthub.llms.litellm import LiteLLMChatModel

        kwargs = {"model": model, "temperature": temperature}
        if api_key:
            kwargs["api_key"] = api_key
        if api_base:
            kwargs["api_base"] = api_base
        return LiteLLMChatModel(**kwargs)
    else:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=model,
            openai_api_key=api_key or os.getenv("OPENAI_API_KEY", ""),
            temperature=temperature,
            openai_api_base=api_base,
        )
