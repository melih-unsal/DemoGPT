from prompts import *
from streamlit_prompts import *
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from subprocess import PIPE, run
import tempfile
from termcolor import colored
import subprocess
from subprocess import DEVNULL, STDOUT

from dotenv import load_dotenv
import os
load_dotenv()

class LogicModel:
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

    
    def __call__(self,topic,num_iterations=10):
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
                break

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
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.0)
        self.streamlit_code_chain = LLMChain(llm=self.llm, prompt=streamlit_code_prompt)

    def run_code(self,code):
        with tempfile.NamedTemporaryFile("w",suffix=".py") as tmp:
            tmp.write(code)
            tmp.flush()
            command = f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')} streamlit run "+tmp.name
            environmental_variables = {'OPENAI_API_KEY':os.getenv('OPENAI_API_KEY'),"STREAMLIT_SERVER_PORT":"8502"}
            #p = subprocess.Popen(["/home/melih/anaconda3/envs/synthdata/bin/streamlit","run",tmp.name],stdout=DEVNULL,stderr=STDOUT, close_fds=True, env=environmental_variables)
            process = subprocess.Popen(["/home/melih/anaconda3/envs/synthdata/bin/streamlit","run",tmp.name], env=environmental_variables)
            pid = process.pid
            print("pid:",colored(pid,"red"))
            return pid
        
    def run_code_v2(self,code):
        filepath = "~/code.py"
        filepath = os.path.expanduser(filepath)
        with open(filepath,"w") as tmp:
            tmp.write(code)
            tmp.flush()
        command = f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')} streamlit run "+filepath
        environmental_variables = {'OPENAI_API_KEY':os.getenv('OPENAI_API_KEY'),"STREAMLIT_SERVER_PORT":"8502"}
        #p = subprocess.Popen(["/home/melih/anaconda3/envs/synthdata/bin/streamlit","run",tmp.name],stdout=DEVNULL,stderr=STDOUT, close_fds=True, env=environmental_variables)
        process = subprocess.Popen(["/home/melih/anaconda3/envs/synthdata/bin/streamlit","run",filepath], env=environmental_variables)
        pid = process.pid
        print("pid:",colored(pid,"red"))
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
        return self.run_code_v2(refined_code)
        

