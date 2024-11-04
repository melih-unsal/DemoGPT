from langchain_openai import OpenAI, ChatOpenAI
from demogpt_agenthub.llms.base import BaseLLM

class OpenAIModel(OpenAI, BaseLLM):
    ...

class OpenAIChatModel(ChatOpenAI, BaseLLM):
    ...