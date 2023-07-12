from termcolor import colored
from langchain_expert import LangChainExpert
import tempfile
import subprocess
import shutil
from subprocess import PIPE
import os
import sys
import fire
from tqdm import trange
from dotenv import load_dotenv
load_dotenv()

expert = LangChainExpert()

def decode_results(results):
    """
    Decodes the results returned by the executed python code

    Args:
        results: The results to be decoded.

    Returns:
        Tuple[str, str]: The decoded results.
    """
    return (res.strip().decode('utf-8') for res in results)

def refine_code(code):
    """
    Refines the provided code by removing unnecessary parts.

    Args:
        code (str): The code to be refined.

    Returns:
        str: The refined code.
    """
    if "```" in code: 
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python"):].strip()
    return code

def run_python(code):
    """
    Executes the Python code using the subprocess module.

    Args:
        code (str): The Python code to be executed.

    Returns:
        Tuple[str, str, bool]: The output, error, and success status of the execution.
    """
    code = refine_code(code)
    
    print("code:\n",code,sep="")

    with tempfile.NamedTemporaryFile("w") as tmp:
        tmp.write(code)
        tmp.flush()
        environmental_variables = {'OPENAI_API_KEY':os.getenv('OPENAI_API_KEY')}
        python_path = shutil.which("python")
        if not python_path: # shows 'which' returns None
            python_path = sys.executable 
        process = subprocess.Popen([python_path,tmp.name], env=environmental_variables,stdout=PIPE, stderr=PIPE)
        output, err = decode_results(process.communicate())
        success = len(err) == 0
        return output, err, success



def main(instruction = "Create a teacher that can do any calculation and solve any chemistry question"):
    question = f"""Which Langchain classes could be used to implement the below instruction
    Instruction:{instruction}
    """
    answer = expert.ask(question)
    print(colored(answer,"yellow"))
    question = f"""
    What are the langchain classes/functions here 
    {answer}. 
    Don't do explanation, just give the result like in the below:
    
    -
    -
    -
    """
    classes = expert.askToModel(question)
    print(colored(classes,"red"))
    question = f"""Give examples to use the langchain classes/functions below:
    classes/functions:{classes}
    """
    examples = expert.ask(question)
    print(colored(examples,"blue"))
    question = f"""Langchain is a python library to create LLM-based applications.
    Create a python application to accomplish the instruction below based on langchain by inspiring from the langchain code examples.
    
    ### instruction:{instruction}
    ########################################################################
    ### LangChain Examples : {examples}
    ########################################################################
    LangChain Code:
    """
    code = expert.askToModel(question)
    print(colored(code,"green"))
    for _ in trange(10):
        output, error, success = run_python(code)
        if not success:
            print(colored(error,"red"))
            question = f"""
            ##### Find the bugs in the below Python code
            
            ### Buggy Python
            {code}

            ### Error
            {error}

            ### Error Reason
            """
            reason = expert.askToModel(question)
            print(colored(reason,"blue"))

            question = f"""
            ##### Ask a single question to solve the error in the below Python code. Don't ask installation related questions 
            because it is known that everything is setup correctly. 
            
            ### Buggy Python
            {code}

            ### Error
            {error}

            ### Error Reason
            {reason}

            ### Question(how) to understand and refine the code (such as how to use that class/function):
            """
            questions = expert.askToModel(question)
            print(colored(questions,"yellow"))
            answer = expert.ask(questions)
            print(colored(answer,"blue"))

            refine_question = f"""
            Based on the critics, fix the buggy code provided to you while you can use the document. Fix the code snippet based on the error provided. Only provide the fixed code snippet between `` and nothing else.:
            buggy code:
            {code}
            ---------
            critics:
            {reason}
            ---------
            document:
            {answer}
            ---------
            Python Code:
            """
            code = expert.askToModel(refine_question)
            print(colored(code,"green"))
        else:
            print("Congrats!!!!!!")
        



def main1(instruction):
    answers = ""
    for i in range(3):
        if i == 0:
            questions = expert.generateQuestions(instruction=instruction)
        else:
            questions = expert.generateQuestions(instruction=instruction,answer=answers)
        print(colored(questions,"blue"))    
        answers = expert.ask(questions,add_history=False)
        print(colored(str(answers),"yellow"))  

    
    question = f"""
    langchain is a python library to create LLM-based applications.
    You will create a python application to accomplish an instruction based on langchain library.

    ### instruction:{instruction}

    ### langchain code:
    """

    code = expert.askToModel(question, chat_history=True)
    print(colored(code,"green"))



if __name__ == "__main__":
    fire.Fire(main)