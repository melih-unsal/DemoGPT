import unittest
import os
from demogpt_agenthub.rag.base import BaseRAG
from demogpt_agenthub.llms.openai import OpenAIChatModel

class TestRAG(unittest.TestCase):
    def setUp(self):
        self.rag = BaseRAG(
            llm=OpenAIChatModel(model="gpt-4o-mini"),
            vectorstore="chroma", 
            persistent_path="rag_chroma", 
            index_name="rag_index",
            reset_vectorstore=True,
            embedding_model_name="sentence-transformers/all-mpnet-base-v2",
            filter={"search_kwargs": {"score_threshold": 0.5}}
            )
        
        with open("test_rag.txt", "w") as f:
            f.write("John Doe is 40 years old and he is a software engineer.")
            
    def tearDown(self):
        if os.path.exists("test_rag.txt"):
            os.remove("test_rag.txt")
        
    def test_add_files(self):
        self.rag.add_files(["test_rag.txt"])
        question = "How old is John Doe?"
        self.assertIn("40", self.rag.query(question))
        
    def test_add_text(self):
        self.rag.add_texts("John Doe is 28 years old and he is a doctor.")
        question = "How old is John Doe?"
        self.assertIn("28", self.rag.query(question))