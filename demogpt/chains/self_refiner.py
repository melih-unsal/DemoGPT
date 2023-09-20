import os

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (AIMessagePromptTemplate,
                                    ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from termcolor import colored
from tqdm import trange

from . import prompts

PROMPTS = {"final": prompts.final_refiner}


class SelfRefiner:
    def __init__(
        self,
        key="final",
        max_iter=4,
        stop_kw="<SUCCESS>",
        log_intermediate_steps=True,
        model="gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        temperature=0.0,
        openai_api_base=None,
    ):
        assert key in PROMPTS

        self.stop_kw = stop_kw
        self.max_iter = max_iter
        self.log_intermediate_steps = log_intermediate_steps

        self.prompts = {
            "feedback": PROMPTS[key].FEEDBACK_PROMPT,
            "refine": PROMPTS[key].REFINEMENT_PROMPT,
        }
        self.llm = ChatOpenAI(
            model=model,
            openai_api_key=openai_api_key,
            temperature=temperature,
            openai_api_base=openai_api_base,
        )

        self.conversation_history = self.getPromptTemplate("refine")

    def getPromptTemplate(self, key):
        assert key in self.prompts
        prompts = []
        prompts.append(
            SystemMessagePromptTemplate.from_template(self.prompts[key])
        )
        return prompts

    def addToHistory(self, prompt):
        if len(self.conversation_history) % 2 == 0:
            template = HumanMessagePromptTemplate.from_template(prompt)
        else:
            template = AIMessagePromptTemplate.from_template(prompt)

        self.conversation_history.append(template)

    def feedback(self, **kwargs):
        return LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_template(self.prompts["feedback"]),
        ).run(**kwargs)

    def refine(self):
        prompt = ChatPromptTemplate.from_messages(self.conversation_history)
        return LLMChain(llm=self.llm, prompt=prompt).run({})

    def isCompleted(self, res):
        return self.stop_kw in res

    def run(self, instruction, plan, result):
        self.addToHistory("instruction:" + instruction)
        self.addToHistory("plan:" + plan)
        self.addToHistory("code:" + result)
        for _ in trange(self.max_iter):
            feedback = self.feedback(instruction=instruction, result=result)
            self.addToHistory("feedback:" + feedback)
            if self.log_intermediate_steps:
                print(colored("feedback:\n" + feedback, "blue"))
            if self.isCompleted(feedback):
                return result
            if self.log_intermediate_steps:
                print(colored("refined result:\n" + result, "green"))
            result = self.refine().replace("{", "{{").replace("}", "}}")
            self.addToHistory("code:" + result)
        return result


if __name__ == "__main__":
    plan_refiner = SelfRefiner()
    instruction = """create a game where the system creates a story and stops at the exciting point and asks to the user 
    to make a selection then after user makes his selection, system continues to the story depending on the user's selection"""
    with open("~/Desktop/test/test.py") as f:
        result = f.read().replace("{", "{{").replace("}", "}}")
    plan_refiner.run(instruction=instruction, result=result)
