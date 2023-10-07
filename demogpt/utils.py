import json
import os
import platform
import re
import shutil
import sys
import tempfile
import threading
from subprocess import PIPE, Popen

from demogpt.chains.task_chains import TaskChains
from demogpt.controllers import checkPromptTemplates, refineKeyTypeCompatiblity

AI_VARIETY_TEMPERATURE = 0.5

def init(title=""):
    if title:
        return IMPORTS_CODE_SNIPPET + f"\nst.title('{title}')\n"
    return IMPORTS_CODE_SNIPPET

def filterTasks(tasks):
    filtered_tasks = []
    for task in tasks:
        if len(task["input_key"]) == 0 and len(task["output_key"]) == 0:
            ...
        else:
            filtered_tasks.append(task)
    return filtered_tasks

def reorderTasksForChatApp(tasks):
    print("before reordering:")
    print(tasks)
    chat_input_order = chat_output_order = -1
    for i,task in enumerate(tasks):
        if task["task_type"] == "ui_input_chat":
            chat_input_order = i
        if task["task_type"] == "ui_output_chat":
            chat_output_order = i
    
    if chat_input_order == -1 and chat_output_order == -1: # means, chat input output pair does not exist (it should have failed before.)
        return tasks

    if chat_input_order + 1 == chat_output_order: # means there is no task between chat input and chat output
        return tasks
    
    pre_chat_tasks = []
    middle_chat_tasks = []
    post_chat_tasks = []
    
    for i, task in enumerate(tasks):
        if i < chat_input_order:
            pre_chat_tasks.append(task)
        elif chat_input_order < i < chat_output_order:
            if set(tasks[i]["input_key"]) & set(tasks[chat_input_order]["output_key"]):
                middle_chat_tasks.append(task)
            else:
                pre_chat_tasks.append(task)
        elif i >= chat_output_order:
            post_chat_tasks.append(task)
                
    new_tasks =  pre_chat_tasks + [tasks[chat_input_order]] + middle_chat_tasks + post_chat_tasks
    
    print("after reordering:")
    print(new_tasks)
            
    return new_tasks
    
def getFunctionNames(code):
    pattern = r"def (\w+)\(.*\):"
    return re.findall(pattern, code)


def getGenericPromptTemplateCode(task, iters):
    res = ""
    is_valid = False
    task_type = task["task_type"]
    inputs = task["input_key"]
    prompt_func = (
        TaskChains.promptTemplate if task_type == "prompt_template" else TaskChains.chat
    )
    finalizer_func = (
        getPromptChatTemplateCode if task_type == "prompt_template" else getChatCode
    )
    additional_inputs = []
    if task_type == "chat":
        additional_inputs.append("chat_history")
    res = prompt_func(task=task)
    function_name = res.get("function_name")
    variety = res.get("variety")
    index = 0
    while not is_valid:
        templates = {key: res.get(key) for key in res if "template" in key}
        check = checkPromptTemplates(templates, task, additional_inputs)
        is_valid = check["valid"]
        feedback = check["feedback"]
        if not is_valid:
            res = TaskChains.promptTemplateRefiner(res, inputs, feedback)
        else:
            break
        index += 1
        if index == iters:
            break
    res["function_name"] = function_name
    res["variety"] = variety
    return finalizer_func(res, task)


def getCodeSnippet(task, code_snippets, iters=10):
    #task = refineKeyTypeCompatiblity(task)
    task_type = task["task_type"]
    code = ""
    if task_type == "ui_input_text":
        code = TaskChains.uiInputText(task=task)
    elif task_type == "ui_output_text":
        code = TaskChains.uiOutputText(task=task)
    elif task_type in ["prompt_template", "chat"]:
        code = getGenericPromptTemplateCode(task, iters=iters)
    elif task_type == "path_to_content":
        code = TaskChains.pathToContent(task=task, code_snippets=code_snippets)
    elif task_type == "doc_to_string":
        code = TaskChains.docToString(task=task)
    elif task_type == "string_to_doc":
        code = TaskChains.stringToDoc(task=task)
    elif task_type == "ui_input_file":
        code = TaskChains.uiInputFile(task=task)
    elif task_type == "doc_loader":
        code = TaskChains.docLoad(task=task, code_snippets=code_snippets)
    elif task_type == "doc_summarizer":
        code = TaskChains.summarize(task=task)
    elif task_type == "ui_input_chat":
        code = getChatInputCode(TaskChains.uiInputChat(task=task))
    elif task_type == "ui_output_chat":
        code = TaskChains.uiOutputChat(task=task)
    elif task_type == "python":
        code = TaskChains.pythonCoder(task=task, code_snippets=code_snippets)
    elif task_type == "plan_and_execute":
        code = TaskChains.search(task=task)
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


def reformatTasks(tasks):
    def proprocess(io):
        if io == "none":
            io = []
        elif isinstance(io, str):
            if io.startswith("["):
                io = io[1:-1]
            io = [var.strip() for var in io.split(",")]
        return io
    
    tasks = filterTasks(tasks)

    processed_tasks = []
    for task in tasks:
        task_input = proprocess(task["input_key"])
        task_output = proprocess(task["output_key"])
        task["input_key"] = task_input
        task["output_key"] = task_output
        processed_tasks.append(task)

    return processed_tasks


def getChatCode(template, task):
    def getHumanInput(template, inputs):
        rightmost = -1
        human_input = ""
        for input in inputs:
            pattern = f"{{{input}}}"
            index = template.rfind(pattern)
            if index > rightmost:
                human_input = input
                rightmost = index
        return human_input

    inputs = task["input_key"]
    variable = ", ".join(task["output_key"])
    temperature = 0 if template.get("variety", "False") == "False" else AI_VARIETY_TEMPERATURE
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
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = st.session_state.chat_llm_chain.run({run_call})
else:
    {variable} = ""
"""
    input_variables = ["chat_history"] + inputs
    human_input = template["human_input"]
    if human_input not in inputs:
        human_input = getHumanInput(system_template, inputs)
    code = f"""
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

def {signature}:
    prompt = PromptTemplate(
        input_variables={input_variables}, template='''{system_template}'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="{human_input}")
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
    variable = ", ".join(task["output_key"])
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
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = {signature}
else:
    {variable} = ""
"""

    temperature = 0 if templates.get("variety", "False") == "False" else AI_VARIETY_TEMPERATURE

    code = f"""\n
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)

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
import tempfile

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
