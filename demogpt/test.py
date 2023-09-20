import os
import sys

sys.path.append(os.path.abspath("demogpt/"))
import json
import unittest

from tqdm import tqdm

from . import utils
from .chains.chains import Chains
from .chains.task_chains import TaskChains
from .test_cases import CODE_SNIPPETS, INSTRUCTIONS, TEST_CASES, TOOL_EXAMPLES


class TestDemoGPT(unittest.TestCase):
    TEST_INDEX = 5
    INSTRUCTION = INSTRUCTIONS[TEST_INDEX]
    REFINE_ITERATIONS = 10
    # "Create a system that can summarize a content taken from url then create a blog post on the summarization"
    # "Create a system that can solve any math problem"
    TITLE = "My App"

    @classmethod
    def setUpClass(cls):
        cls.f = open(f"test_{TestDemoGPT.TEST_INDEX}.log", "w")

        # it sets the model name
        model_name = "gpt-3.5-turbo-0613"

        Chains.setLlm(model_name)
        TaskChains.setLlm(model_name)

    @classmethod
    def writeToFile(cls, title, res, instruction):
        cls.f.write(title)
        cls.f.write("\n")
        cls.f.write(instruction)
        cls.f.write("\n")
        cls.f.write(res)
        cls.f.write("\n")
        cls.f.flush()

    @classmethod
    def writeFinalToFile(cls, res, instruction):
        with open(f"test_final_{TestDemoGPT.TEST_INDEX}.py", "w") as f:
            f.write("#" + instruction + "\n")
            f.write(res)
            f.flush()

    def test_plan(self):
        for test_case in tqdm(TEST_CASES):
            instruction = test_case["instruction"]
            instruction = (
                "Create a system that can summarize a website from the given URL."
            )
            plan = Chains.plan(instruction)
            self.writeToFile("PLAN", plan, instruction)
            break

    def test_tasks(self):
        for test_case in tqdm(TEST_CASES):
            instruction = test_case["instruction"]
            plan = test_case["plan"]
            task_list = Chains.tasks(instruction=instruction, plan=plan)
            self.writeToFile("TASK LIST", json.dumps(task_list, indent=4), instruction)

    def test_feedback(self):
        for test_id in range(4, 5):
            instruction = INSTRUCTIONS[test_id]
            with open(f"test_final_{test_id}.py") as f:
                code = f.read()
            feedback = Chains.feedback(instruction=instruction, code=code)
            self.writeToFile("FEEDBACK", feedback, instruction)

    def test_refine(self):
        for test_id in range(4, 5):
            instruction = INSTRUCTIONS[test_id]
            with open(f"test_final_{test_id}.py") as f:
                code = f.read()
            feedback = Chains.feedback(instruction=instruction, code=code)
            refined_code = Chains.refine(
                instruction=instruction, code=code, feedback=feedback
            )
            self.writeToFile("REFINED CODE", refined_code, instruction)

    def test_final(self):
        for test_case in tqdm(CODE_SNIPPETS):
            instruction = test_case["instruction"]
            code_snippets = test_case["code_snippets"]
            code_snippets = utils.IMPORTS_CODE_SNIPPET + code_snippets
            final_code = Chains.final(draft_code=code_snippets)
            self.writeToFile("FINAL CODE", final_code, instruction)

    def test_task_ui_input_text(self):
        for example in TOOL_EXAMPLES["ui_input_text"]:
            instruction = example["instruction"]
            variable = example["variable"]
            res = TaskChains.uiInputText(instruction=instruction, variable=variable)
            self.writeToFile("UI INPUT TEXT", res, instruction)

    def test_task_ui_output_text(self):
        for example in TOOL_EXAMPLES["ui_input_text"]:
            instruction = example["instruction"]
            args = example["args"]
            res = TaskChains.uiOutputText(instruction=instruction, args=args)
            self.writeToFile("UI OUTPUT TEXT", res, instruction)

    def test_task_prompt_template(self):
        for example in TOOL_EXAMPLES["ui_input_text"]:
            instruction = example["instruction"]
            inputs = example["inputs"]
            res = TaskChains.promptChatTemplate(instruction=instruction, inputs=inputs)
            self.writeToFile("PROMPT CHAT TEMPLATE", res, instruction)

    def test(self):
        title = TestDemoGPT.TITLE

        instruction = TestDemoGPT.INSTRUCTION

        plan = Chains.plan(instruction)

        self.writeToFile("PLAN", plan, instruction)

        task_list = Chains.tasks(instruction=instruction, plan=plan)

        self.writeToFile("TASK LIST", json.dumps(task_list, indent=4), instruction)

        task_controller_result = Chains.taskController(tasks=task_list)

        self.writeToFile(
            "TASK CONTROLLER RESULT",
            json.dumps(task_controller_result, indent=4),
            instruction,
        )
        for _ in range(TestDemoGPT.REFINE_ITERATIONS):
            if not task_controller_result["valid"]:
                task_list = Chains.refineTasks(
                    instruction=instruction,
                    tasks=task_list,
                    feedback=task_controller_result["feedback"],
                )
                self.writeToFile(
                    "REFINED TASK LIST", json.dumps(task_list, indent=4), instruction
                )
                task_controller_result = Chains.taskController(tasks=task_list)
            else:
                break

            self.writeToFile(
                "FEEDBACK", task_controller_result["feedback"], instruction
            )

        code_snippets = utils.init(title)

        self.writeToFile("CODE SNIPPETS", "", instruction)

        for task in tqdm(task_list):
            code = utils.getCodeSnippet(task, code_snippets)
            code = "#" + task["description"] + "\n" + code
            code_snippets += code
            self.writeToFile("", code, "")

        """draft_code = Chains.draft(instruction=instruction,
                                  code_snippets=code_snippets,
                                  plan=plan
                                  )
        
        self.writeToFile("COMBINED CODE",code_snippets,instruction)
        """

        final_code = Chains.final(draft_code=code_snippets)

        self.writeFinalToFile(final_code, instruction)

    def test_all(self):
        for test_case in tqdm(TEST_CASES):
            instruction = test_case["instruction"]
            TestDemoGPT.test(instruction)
        TestDemoGPT.f.close()


if __name__ == "__main__":
    TestDemoGPT.INSTRUCTION = os.environ.get("instruction", TestDemoGPT.INSTRUCTION)
    TestDemoGPT.TITLE = os.environ.get("title", TestDemoGPT.TITLE)
    unittest.test()
