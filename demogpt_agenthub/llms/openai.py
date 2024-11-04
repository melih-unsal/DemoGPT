from langchain_openai import OpenAI, ChatOpenAI
from demogpt_agenthub.llms.base import BaseLLM

class OpenAIModel(OpenAI, BaseLLM):
    def run(self, prompt: str) -> str:
        return self.invoke(prompt)

class OpenAIChatModel(ChatOpenAI, BaseLLM):
    def run(self, prompt: str) -> str:
        return self.invoke(prompt).content