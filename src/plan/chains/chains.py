import json
import os

import chains.prompts as prompts
import utils

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)


class Chains:
    @classmethod
    def setLlm(
        cls, model, openai_api_key=os.getenv("OPENAI_API_KEY", ""), temperature=0
    ):
        Chains.llm = ChatOpenAI(
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
    def plan(cls, instruction):
        return cls.getChain(
            system_template=prompts.plan.system_template,
            human_template=prompts.plan.human_template,
            instruction=instruction,
        )

    @classmethod
    def tasks(cls, instruction, plan):
        task_list = cls.getChain(
            system_template=prompts.tasks.system_template,
            human_template=prompts.tasks.human_template,
            instruction=instruction,
            plan=plan,
        )
        return json.loads(task_list)

    @classmethod
    def final(cls, instruction, code_snippets, plan):
        code = cls.getChain(
            system_template=prompts.final.system_template,
            human_template=prompts.final.human_template,
            instruction=instruction,
            code_snippets=code_snippets,
            plan=plan,
        )
        return utils.refine(code)
