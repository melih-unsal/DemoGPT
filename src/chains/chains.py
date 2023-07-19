from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

from chains.prompts import *


class Chains:
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)

    @classmethod
    def setLlm(cls, model, openai_api_key, temperature=0):
        cls.llm = ChatOpenAI(
            model=model, openai_api_key=openai_api_key, temperature=temperature
        )

    @classmethod
    def getChain(cls, system_template="", human_template="", **kwargs):
        prompts = []
        if system_template:
            prompts.append(SystemMessagePromptTemplate.from_template(system_template))
        if human_template:
            prompts.append(HumanMessagePromptTemplate.from_template(human_template))
        chat_prompt = ChatPromptTemplate.from_messages(prompts)
        return LLMChain(llm=cls.llm, prompt=chat_prompt).run(**kwargs)

    @classmethod
    def divide(cls, **kwargs):
        return cls.getChain(
            system_template=DIVIDE_TASKS_SYSTEM_TEMPLATE,
            human_template=DIVIDE_TASKS_HUMAN_TEMPLATE,
            **kwargs
        )

    @classmethod
    def merge(cls, **kwargs):
        return cls.getChain(
            system_template=MERGE_CODES_SYSTEM_TEMPLATE,
            human_template=MERGE_CODES_HUMAN_TEMPLATE,
            **kwargs
        )

    @classmethod
    def debug(cls, **kwargs):
        return cls.getChain(human_template=APP_DEBUGGING_TEMPLATE, **kwargs)

    @classmethod
    def draft(cls, **kwargs):
        return cls.getChain(human_template=DOC_USE_TEMPLATE, **kwargs)

    @classmethod
    def streamlit(cls, **kwargs):
        return cls.getChain(
            system_template=STREAMLIT_CODE_SYSTEM_TEMPLATE,
            human_template=STREAMLIT_CODE_HUMAN_TEMPLATE,
            **kwargs
        )

    @classmethod
    def feedback(cls, **kwargs):
        return cls.getChain(human_template=CODE_FEEDBACK_HUMAN_TEMPLATE, **kwargs)

    @classmethod
    def refine(cls, **kwargs):
        return cls.getChain(
            system_template=CODE_REFINE_SYSTEM_TEMPLATE,
            human_template=CODE_REFINE_HUMAN_TEMPLATE,
            **kwargs
        )

    @classmethod
    def refine1(cls, **kwargs):
        return cls.getChain(human_template=CODE_REFINE1_HUMAN_TEMPLATE, **kwargs)
