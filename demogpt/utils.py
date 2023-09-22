import json
import os
import platform
import shutil
import sys
import tempfile
import threading
from subprocess import PIPE, Popen
import re

from demogpt.chains.task_chains import TaskChains
from demogpt.controllers import checkPromptTemplates, refineKeyTypeCompatiblity


def init(title=""):
    if title:
        return IMPORTS_CODE_SNIPPET + f"\nst.title('{title}')\n"
    return IMPORTS_CODE_SNIPPET

def getFunctionNames(code):
    pattern = r"def (\w+)\(.*\):"
    return re.findall(pattern, code)


def getCodeSnippet(task, code_snippets, iters=10):
    task = refineKeyTypeCompatiblity(task)
    task_type = task["task_type"]
    code = ""
    if task_type == "ui_input_text":
        code = TaskChains.uiInputText(task=task, code_snippets=code_snippets)
    elif task_type == "ui_output_text":
        code = TaskChains.uiOutputText(task=task, code_snippets=code_snippets)
    elif task_type == "prompt_template":
        res = ""
        is_valid = False
        res = TaskChains.promptTemplate(task=task, code_snippets=code_snippets)
        function_name = res.get("function_name")
        variety = res.get("variety")
        index = 0
        while not is_valid:
            check = checkPromptTemplates(res, task)
            is_valid = check["valid"]
            feedback = check["feedback"]
            if not is_valid:
                res = TaskChains.promptTemplateRefiner(res, feedback)
            else:
                break
            index += 1
            if index == iters:
                break
        res["function_name"] = function_name
        res["variety"] = variety
        code = getPromptChatTemplateCode(res, task)
    elif task_type == "path_to_content":
        code = TaskChains.pathToContent(task=task, code_snippets=code_snippets)
    elif task_type == "doc_to_string":
        code = TaskChains.docToString(task=task, code_snippets=code_snippets)
    elif task_type == "string_to_doc":
        code = TaskChains.stringToDoc(task=task, code_snippets=code_snippets)
    elif task_type == "ui_input_file":
        code = TaskChains.uiInputFile(task=task, code_snippets=code_snippets)
    elif task_type == "doc_loader":
        code = TaskChains.docLoad(task=task, code_snippets=code_snippets)
    elif task_type == "doc_summarizer":
        code = TaskChains.summarize(task=task, code_snippets=code_snippets)
    elif task_type == "chat":
        template = TaskChains.chat(task=task)
        code = getChatCode(template=template, task=task)
    elif task_type == "ui_input_chat":
        code = getChatInputCode(TaskChains.uiInputChat(task=task))
    elif task_type == "ui_output_chat":
        code = TaskChains.uiOutputChat(task=task)
    return code.strip() + "\n"

def getChatInputCode(code):
    prefix = """
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])\n
"""
    return prefix + code

def refine(code):
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python") :].strip()
    return code

def getChatCode(template, task):
    inputs = task["input_key"]
    variable = task["output_key"]
    temperature = 0 if template.get("variety", "False") == "False" else 0.7
    system_template = template["system_template"]
    run_call = "{}"

    if inputs == "none":
        signature = f"{template['function_name']}()"
        function_call = f"{variable} = {signature}"
        inputs = []
    else:
        if isinstance(inputs, str):
            if inputs.startswith("["):
                inputs = inputs[1:-1]
            inputs = [var.strip() for var in inputs.split(",")]
        if len(inputs) > 0:
            run_call = ", ".join([f"{var}={var}" for var in inputs])
        signature = f"{template['function_name']}({','.join(inputs)})"
        function_call = f"""
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
elif {' and '.join(inputs)}:
    if 'chat_llm_chain' not in st.session_state:
        st.session_state.chat_llm_chain = {signature}
    {variable} = st.session_state.chat_llm_chain.run({run_call})
else:
    {variable} = ""
"""
    input_variables = ["chat_history"] + inputs
    code = f"""

def {signature}:
    prompt = PromptTemplate(
        input_variables={input_variables}, template='''{system_template}'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="{inputs[0]}")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature={temperature})
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    return chat_llm_chain
    
{function_call} 

    """
    
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
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
elif {' and '.join(inputs)}:
    {variable} = {signature}
else:
    {variable} = ""
"""

    temperature = 0 if templates.get("variety", "False") == "False" else 0.7

    code = f"""\n
def {signature}:
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
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


def runStreamlit(code, openai_api_key, openai_api_base=None):
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
        "OPENAI_API_BASE": openai_api_base,
    }
    streamlit_path = shutil.which("streamlit")
    if True or platform.system() == "Windows":
        env = os.environ.copy()
        env["PYTHONPATH"] = ""
        env["OPENAI_API_KEY"] = openai_api_key
        env["STREAMLIT_SERVER_PORT"] = "8502"
        if openai_api_base:
            env["OPENAI_API_BASE"] = openai_api_base
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
import os
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
import time
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
"""
