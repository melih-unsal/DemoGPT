from prompts import *
from streamlit_prompts import *
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from subprocess import PIPE
import tempfile
from termcolor import colored
import subprocess
import shutil
import sys

from dotenv import load_dotenv
import os
load_dotenv()

class LogicModel:
    def __init__(self,openai_api_key):
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.0)
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
            environmental_variables = {'OPENAI_API_KEY':self.openai_api_key}
            python_path = shutil.which("python")
            if not python_path: # shows 'which' returns None
                python_path = sys.executable 
            process = subprocess.Popen([python_path,tmp.name], env=environmental_variables,stdout=PIPE, stderr=PIPE)
            output, err = process.communicate()
            return output.strip().decode('utf-8'), err.strip().decode('utf-8')
        
    def refine_code(self,code):
        if "```" in code: 
            code = code.split("```")[1]
            if code.startswith("python"):
                code = code[len("python"):].strip()
        return code

    
    def __call__(self,topic,num_iterations=10):
        error = ""
        percentage = 0
        feedback = ""
        total_code=""
        refined_code=""

        for i in range(num_iterations):
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

            if len(error) > 0:
                print("Iteration:",i,"error:",colored(error,"red"),colored(type(error),"red"))

            success = len(response) > 0    

            if success:
                break

            response = error

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


class StreamlitModel:
    def __init__(self,openai_api_key):
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.0)
        self.streamlit_code_chain = LLMChain(llm=self.llm, prompt=streamlit_code_prompt)
 
    def run_code(self,code):
        filepath = "~/code.py"
        filepath = os.path.expanduser(filepath)
        with open(filepath,"w") as tmp:
            tmp.write(code)
            tmp.flush()
        environmental_variables = {'OPENAI_API_KEY':self.openai_api_key,"STREAMLIT_SERVER_PORT":"8502"}
        streamlit_path = shutil.which("streamlit")
        process = subprocess.Popen([streamlit_path,"run",filepath], env=environmental_variables)
        pid = process.pid
        return pid

    def refine_code(self,code):
        if "```" in code: 
            code = code.split("```")[1]
            if code.startswith("python"):
                code = code[len("python"):].strip()
        return code
    
    def __call__(self,topic, title, code, test_code,progress_func,baloon_func):
        streamlit_code = self.streamlit_code_chain.run(topic=topic, title=title, logic_code=code, test_code=test_code)
        refined_code = self.refine_code(streamlit_code)
        progress_func(100,"Redirecting to the demo page...")
        baloon_func()
        return self.run_code(refined_code)
        

