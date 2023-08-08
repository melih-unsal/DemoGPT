import os
import sys

sys.path.append(os.path.abspath('src/plan/'))
import json
import unittest

import utils
from chains.chains import Chains
from chains.task_chains import TaskChains
from termcolor import colored
from test_cases import TEST_CASES, TOOL_EXAMPLES
from tqdm import tqdm


class TestDemoGPT(unittest.TestCase):
    INSTRUCTION = "Create a system that can summarize a content taken from url then create a blog post on the summarization"
    #"Create a system that can solve any math problem"
    TITLE = "My App"

    @classmethod
    def setUpClass(cls):
        cls.f = open("test.log", "w")
        
        # it sets the model name
        model_name = "gpt-3.5-turbo-0301"

        Chains.setLlm(model_name)
        TaskChains.setLlm(model_name)
        
    @classmethod
    def writeToFile(cls,title,res,instruction):
        cls.f.write(title)
        cls.f.write("\n")
        cls.f.write(instruction)
        cls.f.write("\n")
        cls.f.write(res)
        cls.f.write("\n")
        cls.f.flush()

    @classmethod
    def printRes(cls,title,res,instruction):
        print(colored(title,'red', 'on_light_blue', ['bold', 'dark']))
        print(colored(instruction,'green', 'on_light_blue', ['bold', 'dark']))
        print(colored(res,"light_green"))
        print(colored("#"*100,"blue"))
        cls.f.flush()

    def test_plan(self):
        for test_case in tqdm(TEST_CASES):
            instruction = test_case["instruction"]
            plan = Chains.plan(instruction)
            self.writeToFile("PLAN",plan,instruction)

    def test_tasks(self):
        for test_case in tqdm(TEST_CASES):
            instruction = test_case["instruction"]
            plan = test_case["plan"]
            task_list = Chains.tasks(instruction=instruction,plan=plan)
            self.writeToFile("TASK LIST",json.dumps(task_list, indent=4),instruction)

    def test_final(self):
        for test_case in tqdm(TEST_CASES):
            instruction = test_case["instruction"]
            plan = test_case["plan"]
            code_snippets = test_case["code_snippets"]
            final_code = Chains.final(instruction=instruction,
                                      code_snippets=code_snippets,
                                      plan=plan
                                      )
            self.writeToFile("CODE",final_code,instruction)            
    
    def test_task_ui_input_text(self):
        for example in TOOL_EXAMPLES["ui_input_text"]:
            instruction = example["instruction"]
            variable = example["variable"]
            res = TaskChains.uiInputText(instruction=instruction,variable=variable)
            self.writeToFile("UI INPUT TEXT",res,instruction)

    def test_task_ui_output_text(self):
        for example in TOOL_EXAMPLES["ui_input_text"]:
            instruction = example["instruction"]
            args = example["args"]
            res = TaskChains.uiOutputText(instruction=instruction,args=args)
            self.writeToFile("UI OUTPUT TEXT",res,instruction)

    def test_task_prompt_chat_template(self):
        for example in TOOL_EXAMPLES["ui_input_text"]:
            instruction = example["instruction"]
            inputs = example["inputs"]
            res = TaskChains.promptChatTemplate(instruction=instruction,inputs=inputs)
            self.writeToFile("PROMPT CHAT TEMPLATE",res,instruction)

    def test(self):
        title = TestDemoGPT.TITLE

        instruction = TestDemoGPT.INSTRUCTION

        plan = Chains.plan(instruction)

        print(plan)

        self.writeToFile("PLAN",plan,instruction)

        task_list = Chains.tasks(instruction=instruction, plan=plan)
        print("Task list:",task_list)

        self.writeToFile("TASK LIST",json.dumps(task_list, indent=4),instruction)
    
        code_snippets = utils.IMPORTS_CODE_SNIPPET + f"\nst.title({title})\n"

        for task in tqdm(task_list):
            code = utils.getCodeSnippet(task)
            code = "#"+task["description"] + "\n" + code
            code_snippets += code

        self.writeToFile("CODE SNIPPETS",code_snippets,instruction)

        final_code = Chains.final(instruction=instruction,
                                  code_snippets=code_snippets,
                                  plan=plan
                                  )

        self.writeToFile("CODE",final_code,instruction)

    def test_all(self):
        for test_case in tqdm(TEST_CASES):
            instruction = test_case["instruction"]
            TestDemoGPT.test(instruction)
        TestDemoGPT.f.close()
        
    
if __name__ == '__main__':
    TestDemoGPT.INSTRUCTION = os.environ.get('instruction', TestDemoGPT.INSTRUCTION)
    TestDemoGPT.TITLE = os.environ.get('title', TestDemoGPT.TITLE)
    unittest.test()