from prompts import *
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from subprocess import PIPE, run
import tempfile
from termcolor import colored

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
        self.check_chain = LLMChain(llm=self.llm,prompt=check_chat_prompt)
        self.document = ""
        for path in ["examples.txt"]:
            with open(path) as f:
                self.document += f.read()

    def run_python(self,code):
        with tempfile.NamedTemporaryFile("w") as tmp:
            tmp.write(code)
            tmp.flush()
            command = f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')} python "+tmp.name
            print(colored(command,"blue"))
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            return result.stdout, result.stderr
        
    def refine_code(self,code):
        if "```" in code: 
            code = code.split("```")[1]
            if code.startswith("python"):
                code = code[len("python"):].strip()
        return code

    
    def __call__(self,topic,num_iterations=5):
        error = ""
        percentage = 0
        feedback = ""
        total_code=""
        refined_code=""

        for _ in range(num_iterations):
            if error:
                code = self.refine_chain.run(content=code,
                                             critics=feedback,
                                             document=self.document,
                                             instruction_hint="Fix the code snippet based on the error provided. Only provide the fixed code snippet between `` and nothing else.")
            else:
                code = self.code_chain.run(document=self.document,topic=topic)
            code = self.refine_code(code)

            test_code = self.test_chain.run(code=code, topic=topic,feedback=feedback)
            test_code = self.refine_code(test_code)

            total_code = code + "\n" + test_code

            response, error = self.run_python(total_code)

            print("response:",response,type(response))
            print("error:",colored(error,"red"),colored(type(error),"red"))

            success = len(response) > 0
            if success:
                refined_code = self.check_chain.run(topic=topic,code=total_code,response=response)

                

            print("response:",response)
            print("error:",error)

            feedback = self.fix_chain.run(code=total_code,error=error)


            percentage += 100 // num_iterations

            yield {
                "code":code,
                "total_code":total_code,
                "success":success,
                "out":response,
                "error":error,
                "feedback":feedback,
                "test_code":test_code,
                "refined_code":refined_code,
                "percentage":min(100,percentage)
                }

        yield {
            "code":code,
            "total_code":total_code,
            "success":success,
            "out":response,
            "error":error,
            "feedback":feedback,
            "test_code":test_code,
            "refined_code":refined_code,
            "percentage":100
        }