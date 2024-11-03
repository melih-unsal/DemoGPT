from langchain_openai import OpenAI
from langchain_community.chat_models import ChatOpenAI
from demogpt_agenthub.llms.base import BaseLLM

class OpenAIModel(OpenAI, BaseLLM):
    ...

class OpenAIChatModel(ChatOpenAI, BaseLLM):
    ...