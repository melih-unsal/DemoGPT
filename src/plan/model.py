import json
from time import sleep

import utils
from chains.chains import Chains
from chains.task_chains import TaskChains
from tqdm import tqdm


class Model:
    def __init__(self, openai_api_key="sk-", model_name="gpt-3.5-turbo"):
        self.model_name = model_name
        self.openai_api_key = openai_api_key
        Chains.setLlm(self.model_name, self.openai_api_key)
        TaskChains.setLlm(self.model_name, self.openai_api_key)

    def setModel(self, model_name):
        self.model_name = model_name
        Chains.setLlm(self.model_name, self.openai_api_key)
        TaskChains.setLlm(self.model_name, self.openai_api_key)

    def __call__(
        self,
        instruction="Create a translation system that converts English to French",
        title="",
    ):
        yield {
            "stage": "plan",
            "completed": False,
            "percentage": 0,
            "done": False,
            "message": "Plan creation has started...",
        }

        plan = Chains.plan(instruction)

        yield {
            "stage": "plan",
            "completed": True,
            "percentage": 20,
            "done": False,
            "message": "Plan has been generated.",
        }

        sleep(1)

        yield {
            "stage": "task",
            "completed": False,
            "percentage": 30,
            "done": False,
            "message": "Task generation has started...",
        }

        task_list = Chains.tasks(instruction=instruction, plan=plan)

        yield {
            "stage": "task",
            "completed": True,
            "percentage": 50,
            "done": False,
            "message": "Tasks have been generated.",
            "tasks": task_list,
        }

        code_snippets = utils.init(title)

        sleep(1)

        yield {
            "stage": "draft",
            "completed": False,
            "percentage": 60,
            "done": False,
            "message": "Converting tasks to code snippets...",
        }

        num_of_tasks = len(task_list)

        for i, task in enumerate(task_list):
            code = utils.getCodeSnippet(task,code_snippets)
            code_snippets += code
            yield {
                "stage": "draft",
                "completed": i + 1 == num_of_tasks,
                "percentage": 60 + int(20 * (i + 1) / num_of_tasks),
                "done": False,
                "message": f"{i+1}/{num_of_tasks} tasks have been converted to code",
                "code": code_snippets,
            }

        sleep(1)

        yield {
            "stage": "final",
            "completed": False,
            "percentage": 90,
            "done": False,
            "message": "Final code generation has started...",
        }

        final_code = Chains.final(
            instruction=instruction, code_snippets=code_snippets, plan=plan
        )

        yield {
            "stage": "final",
            "completed": True,
            "percentage": 100,
            "done": True,
            "message": "Final code has been generated. Directing to the demo page...",
            "code": final_code,
        }
