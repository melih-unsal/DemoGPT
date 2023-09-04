import os
import sys
from time import sleep

from tqdm import trange

from demogpt.chains.chains import Chains
from demogpt.chains.task_chains import TaskChains
from demogpt.utils import getCodeSnippet, init


class DemoGPT:
    def __init__(
        self,
        llm_config,
        max_steps=10,
    ):
        self.model_name = llm_config["model_name"]
        self.openai_api_base = llm_config["api_base_url"]
        self.openai_api_key = llm_config["api_key"]
        self.max_steps = max_steps  # max iteration for refining the model purpose
        Chains.setLlm(
            self.model_name, self.openai_api_key, openai_api_base=self.openai_api_base
        )
        TaskChains.setLlm(
            self.model_name, self.openai_api_key, openai_api_base=self.openai_api_base
        )

    def setModel(self, model_name):
        self.model_name = model_name
        Chains.setLlm(
            self.model_name, self.openai_api_key, openai_api_base=self.openai_api_base
        )
        TaskChains.setLlm(
            self.model_name, self.openai_api_key, openai_api_base=self.openai_api_base
        )

    def __repr__(self) -> str:
        return f"DemoGPT(model_name='{self.model_name}',max_steps={self.max_steps})"

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

        sleep(1)

        yield {
            "stage": "task",
            "completed": True,
            "percentage": 55,
            "done": False,
            "message": "Tasks are being controlled.",
        }

        task_controller_result = Chains.taskController(tasks=task_list)

        for _ in trange(self.max_steps):
            if not task_controller_result["valid"]:
                task_list = Chains.refineTasks(
                    instruction=instruction,
                    tasks=task_list,
                    feedback=task_controller_result["feedback"],
                )
                task_controller_result = Chains.taskController(tasks=task_list)
            else:
                break

        code_snippets = init(title)

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
            code = getCodeSnippet(task, code_snippets, self.max_steps)
            code = "#" + task["description"] + "\n" + code
            code_snippets += code
            yield {
                "stage": "draft",
                "completed": i + 1 == num_of_tasks,
                "percentage": 60 + int(20 * (i + 1) / num_of_tasks),
                "done": False,
                "message": f"{i+1}/{num_of_tasks} tasks have been converted to code",
                "code": code,
            }

        sleep(1)

        yield {
            "stage": "draft",
            "completed": False,
            "percentage": 85,
            "done": False,
            "message": "Code snippets are being combined...",
        }

        draft_code = Chains.draft(
            instruction=instruction, code_snippets=code_snippets, plan=plan
        )

        yield {
            "stage": "draft",
            "completed": True,
            "percentage": 90,
            "done": False,
            "message": "Code snippets combined. Now code is being finalized...",
        }

        final_code = Chains.final(draft_code=draft_code)

        yield {
            "stage": "final",
            "completed": True,
            "percentage": 100,
            "done": True,
            "message": "Final code has been generated. Directing to the demo page...",
            "code": final_code,
        }
