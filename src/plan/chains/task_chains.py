import json
import os

import chains.prompts as prompts
import utils

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)


class TaskChains:
    llm = None

    @classmethod
    def setLlm(
        cls, model, openai_api_key=os.getenv("OPENAI_API_KEY", ""), temperature=0
    ):
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
    def uiInputText(cls, task):
        variable = task["output_key"]
        instruction = task["description"]
        code = cls.getChain(
            human_template=prompts.ui_input_text.human_template,
            instruction=instruction,
            variable=variable,
        )
        return utils.refine(code)

    @classmethod
    def uiOutputText(cls, task):
        args = task["input_key"]
        if isinstance(args, list):
            args = ",".join(args)
        instruction = task["description"]
        code = cls.getChain(
            human_template=prompts.ui_output_text.human_template,
            instruction=instruction,
            args=args,
        )
        return utils.refine(code)

    @classmethod
    def uiInputFile(cls, task):
        variable = task["output_key"]
        instruction = task["description"]
        code = cls.getChain(
            human_template=prompts.ui_input_file.human_template,
            instruction=instruction,
            variable=variable,
        )
        return utils.refine(code)

    @classmethod
    def promptChatTemplate(cls, task):
        inputs = task["input_key"]
        instruction = task["description"]

        res = cls.getChain(
            system_template=prompts.prompt_chat_template.system_template,
            human_template=prompts.prompt_chat_template.human_template,
            instruction=instruction,
            inputs=inputs,
        )
        start_index = res.find("{")
        return res[start_index:]
