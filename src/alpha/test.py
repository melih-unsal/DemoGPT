import os
import sys

sys.path.append(os.path.abspath('src/alpha/'))
import json
import unittest

import utils
from chains.chains import Chains
from termcolor import colored


class TestDemoGPT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.instruction = """create a system that can predict horoscope by asking a question to the user."""
        cls.system_inputs = ""
        cls.button_text = ""
        cls.plan = ""
        cls.draft = ""
        cls.task_list = ""
        cls.explanation = ""
        cls.langchain_functions = ""
        cls.streamlit_functions = ""

    @classmethod
    def printRes(self,title,res):
        print(colored(title,'red', 'on_light_blue', ['bold', 'dark']))
        print(colored(res,"light_green"))
        print(colored("#"*100,"blue"))

    def test_helpers(self):
        if not self.system_inputs:
            TestDemoGPT.system_inputs, TestDemoGPT.button_text = Chains.helpers(TestDemoGPT.instruction)
            self.printRes("SYSTEM INPUTS",TestDemoGPT.system_inputs)

    def test_plan(self):
        if not self.plan:
            TestDemoGPT.plan = Chains.plan(TestDemoGPT.instruction)
            self.printRes("PLAN",TestDemoGPT.plan)

    def test_draft(self):
        self.test_plan()
        if not TestDemoGPT.draft:
            TestDemoGPT.draft = Chains.draft(TestDemoGPT.instruction, TestDemoGPT.plan)
            self.printRes("DRAFT",TestDemoGPT.draft)

    def test_tasks(self):
        self.test_helpers()
        if not self.task_list:
            TestDemoGPT.task_list = Chains.tasks(instruction=TestDemoGPT.instruction, system_inputs=TestDemoGPT.system_inputs)
            self.printRes("TASK LIST",json.dumps(self.task_list, indent=4))

    def test_explanation(self):
        if not self.explanation:
            TestDemoGPT.explanation = Chains.explain(instruction=TestDemoGPT.instruction, task_list=TestDemoGPT.task_list)
            self.printRes("EXPLANATION",self.explanation)
    
    def test_langchain(self):
        self.test_tasks()
        if not self.langchain_functions:
            TestDemoGPT.langchain_functions = utils.getLangchainFunctions(TestDemoGPT.task_list)
            self.printRes("LANGCHAIN FUNCTIONS",TestDemoGPT.langchain_functions)
    
    def test_streamlit(self):
        self.test_tasks()
        if not self.streamlit_functions:
            TestDemoGPT.streamlit_functions = utils.getStreamlitFunctions(TestDemoGPT.task_list)
            self.printRes("STREAMLIT FUNCTIONS",TestDemoGPT.streamlit_functions)
        

    def test_final(self):
        self.test_explanation()
        self.test_langchain()
        self.test_streamlit()

        final_code = Chains.final(
            instruction=TestDemoGPT.instruction,
            streamlit_code=TestDemoGPT.streamlit_functions,
            langchain_code=TestDemoGPT.langchain_functions,
            explanation=TestDemoGPT.explanation,
            button_text=TestDemoGPT.button_text,
            imports_code_snippet=utils.IMPORTS_CODE_SNIPPET,
        )

        self.printRes("FINAL CODE",final_code)
    
if __name__ == '__main__':
    unittest.main()