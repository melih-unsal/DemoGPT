import json
import os
import platform
import shutil
import sys
import tempfile
import threading
from subprocess import PIPE, Popen

from demogpt.plan.controllers import checkPromptTemplates, refineKeyTypeCompatiblity
from demogpt.plan.chains.task_chains import TaskChains


def init(title=""):
    if title:
        return IMPORTS_CODE_SNIPPET + f"\nst.title({title})\n"
    return IMPORTS_CODE_SNIPPET


def getCodeSnippet(task,code_snippets,iters):
    task = refineKeyTypeCompatiblity(task)
    task_type = task["task_type"]
    code = ""
    if task_type == "ui_input_text":
        code = TaskChains.uiInputText(task=task,code_snippets=code_snippets)
    elif task_type == "ui_output_text":
        code = TaskChains.uiOutputText(task=task,code_snippets=code_snippets)
    elif task_type == "prompt_chat_template":
        res = ""
        is_valid = False
        res = TaskChains.promptChatTemplate(task=task,code_snippets=code_snippets)
        index = 0
        while not is_valid:
            check = checkPromptTemplates(res,task)
            is_valid = check["valid"]
            feedback = check["feedback"]
            if not is_valid:
                res = TaskChains.promptTemplateRefiner(res,feedback)
            else:
                break   
            index += 1
            if index == iters:
                break
        code = getPromptChatTemplateCode(res, task)
    elif task_type == "path_to_content":
        code = TaskChains.pathToContent(task=task,code_snippets=code_snippets)
    elif task_type == "doc_to_string":
        code = TaskChains.docToString(task=task,code_snippets=code_snippets)
    elif task_type == "string_to_doc":
        code = TaskChains.stringToDoc(task=task,code_snippets = code_snippets)
    elif task_type == "ui_input_file":
        code = TaskChains.uiInputFile(task=task,code_snippets=code_snippets)
    elif task_type == "doc_loader":
        code = TaskChains.docLoad(task=task,code_snippets=code_snippets)
    elif task_type == "doc_summarizer":
        code = TaskChains.summarize(task=task,code_snippets=code_snippets)
    return code.strip() + "\n"


def refine(code):
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python") :].strip()
    return code


def getPromptChatTemplateCode(templates, task):
    inputs = task["input_key"]
    variable = task["output_key"]
    run_call = "{}"

    if inputs == "none":
        signature = f"{templates['function_name']}()"
        function_call = f"{variable} = {signature}"
    else:
        if isinstance(inputs, str):
            if inputs.startswith("["):
                inputs = inputs[1:-1]
            inputs = [var.strip() for var in inputs.split(",")]
        if len(inputs) > 0:
            run_call = ", ".join([f"{var}={var}" for var in inputs])
        signature = f"{templates['function_name']}({','.join(inputs)})"
        function_call = f"""
if {' and '.join(inputs)}:
    {variable} = {signature}
else:
    {variable} = ""
"""

    temperature = 0 if templates.get("variety", "False") == "False" else 0.7

    code = f"""\n
def {signature}:
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature={temperature}
    )
    system_template = \"\"\"{templates['system_template']}\"\"\"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = \"\"\"{templates['template']}\"\"\"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run({run_call})
    return result # returns string   

{function_call}               

"""
    return code


def runThread(proc):
    proc.communicate()


def runStreamlit(code, openai_api_key):
    """
    Runs the provided code as a Streamlit application and returns the process ID.

    Args:
        code (str): The code of the Streamlit application.

    Returns:
        int: The process ID of the Streamlit application.
    """
    tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8")
    tmp.write(code)
    tmp.flush()
    environmental_variables = {
        "OPENAI_API_KEY": openai_api_key,
        "STREAMLIT_SERVER_PORT": "8502",
    }
    streamlit_path = shutil.which("streamlit")
    if True or platform.system() == "Windows":
        env = os.environ.copy()
        env["PYTHONPATH"] = ""
        env["OPENAI_API_KEY"] = openai_api_key
        env["STREAMLIT_SERVER_PORT"] = "8502"
        python_path = sys.executable
        process = Popen(
            [python_path, "-m", "streamlit", "run", tmp.name],
            env=env,
            stdout=PIPE,
            stderr=PIPE,
        )
        threading.Thread(target=runThread, args=(process,)).start()
    try:
        tmp.close()
    except PermissionError:
        pass

    return process.pid


IMPORTS_CODE_SNIPPET = """
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile
from langchain.docstore.document import Document
"""
