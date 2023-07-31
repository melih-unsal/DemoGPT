from tqdm import tqdm
import utils
from chains.chains import Chains
from chains.task_chains import TaskChains


class Model:
    def __init__(self, openai_api_key="sk-", model_name="gpt-3.5-turbo"):
        self.model_name = model_name
        self.openai_api_key = openai_api_key
        Chains.setLlm(self.model_name, self.openai_api_key)

    def setModel(self, model_name):
        self.model_name = model_name
        Chains.setLlm(self.model_name, self.openai_api_key)

    def __call__(
        self, instruction="Create a translation system that converts English to French"
    ):
        yield {"stage": "plan"}

        plan = Chains.plan(instruction)

        yield {"stage": "task_generation"}

        task_list = Chains.tasks(instruction=instruction, plan=plan)

        code_snippets = []

        for task in tqdm(task_list):
            task_instruction = task["description"]
            if task["task_name"] == "ui_input_text":
                code = TaskChains.uiInputText(instruction=task_instruction)
                code_snippets.append(
                    {
                        "description": task_instruction,
                        "code":code
                    }
                )
            elif task["task_name"] == "ui_output_text":
                args = task["input_key"]
                code = TaskChains.uiOutputText(instruction=task_instruction,args=args)
                code_snippets.append(
                    {
                        "description": task_instruction,
                        "code":code
                    }
                )
            elif task["task_name"] == "prompt_chat_template":
                inputs = task["input_key"]
                res = TaskChains.promptChatTemplate(instruction=task_instruction, inputs=inputs)
                code = utils.getPromptChatTemplateCode(res,inputs)
                code_snippets.append(
                    {
                        "description": task_instruction,
                        "code":code
                    }
                )




    
