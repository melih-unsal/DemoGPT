from prompts import *
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from subprocess import PIPE, run
import tempfile

from dotenv import load_dotenv
import os
load_dotenv()

class Model:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.0)
        self.code_chain = LLMChain(llm=self.llm, prompt=code_prompt)
        self.test_chain = LLMChain(llm=self.llm, prompt=test_prompt)
        self.refine_chain = LLMChain(llm=self.llm,prompt=refine_chat_prompt)
        self.fix_chain = LLMChain(llm=self.llm,prompt=fix_chat_prompt)
        self.document = ""
        for path in ["langchain.txt","doc.txt"]:
            with open(path) as f:
                self.document += f.read()

    def run_python(self,code):
        with tempfile.NamedTemporaryFile("w") as tmp:
            tmp.write(code)
            tmp.flush()
            command = f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')} python "+tmp.name
            print(command)
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            return result.stdout, result.stderr
    
    def __call__(self,topic,num_iterations=5):
        error = ""
        percentage = 0
        feedback = ""

        for _ in range(num_iterations):
            if error:
                code = self.refine_chain.run(content=code,
                                             critics=feedback,
                                             document=self.document,
                                             instruction_hint="Fix the code snippet based on the error provided. Only provide the fixed code snippet between `` and nothing else.")
            else:
                code = self.code_chain.run(document=self.document,topic=topic)

            if "```" in code: 
                code = code.split("```")[1]
                if code.startswith("python"):
                    code = code[len("python"):].strip()
            print(code)
            response, error = self.run_python(code)

            success = len(response) > 0
            if success:
                break

            feedback = self.fix_chain.run(code=code,error=error)


            percentage += 100 // num_iterations

            yield {
                "code":code,
                "success":success,
                "out":response,
                "error":error,
                "percentage":min(100,percentage)
                }

        yield {
            "code":code,
            "success":success,
            "out":response,
            "error":error,
            "percentage":100
        }