import unittest
from demogpt_agenthub.llms.openai import OpenAIModel, OpenAIChatModel

class TestOpenAIModel(unittest.TestCase):
    def setUp(self):
        self.model = OpenAIModel(model="gpt-3.5-turbo-instruct")
        
    def test_correct_response(self):
        result = self.model.run("What is the capital of Turkey?")
        self.assertIn("Ankara", result)

class TestOpenAIChatModel(unittest.TestCase):
    def setUp(self):
        self.model = OpenAIChatModel(model="gpt-4o-mini")
        
    def test_correct_response(self):
        result = self.model.run("What is the capital of Turkey?")
        self.assertIn("Ankara", result)