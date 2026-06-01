from typing import Any, List, Optional

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from demogpt_agenthub.llms.base import BaseLLM


class LiteLLMChatModel(BaseChatModel, BaseLLM):
    """LLM provider that routes through the LiteLLM SDK.

    Supports 100+ providers (Anthropic, Bedrock, Vertex, Azure, Groq, etc.)
    using LiteLLM's unified model naming convention.
    Provider API keys are read from environment variables.
    """

    model: str = "gpt-4o-mini"
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.0

    @property
    def _llm_type(self) -> str:
        return "litellm"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        import litellm

        message_dicts = [
            {"role": _role_from_message(m), "content": m.content}
            for m in messages
        ]

        params = {
            "model": self.model,
            "messages": message_dicts,
            "temperature": self.temperature,
            "drop_params": True,
        }
        if self.api_key:
            params["api_key"] = self.api_key
        if self.api_base:
            params["api_base"] = self.api_base
        if stop:
            params["stop"] = stop

        response = litellm.completion(**params)
        content = response.choices[0].message.content
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    def run(self, prompt: str) -> str:
        return self.invoke(prompt).content


def _role_from_message(msg: BaseMessage) -> str:
    if msg.type == "human":
        return "user"
    elif msg.type == "ai":
        return "assistant"
    elif msg.type == "system":
        return "system"
    return "user"
