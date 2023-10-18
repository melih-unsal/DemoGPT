import ast
import os
import re
import subprocess
import sys
import tempfile
import threading
from subprocess import PIPE, Popen

from demogpt.chains.task_chains import TaskChains
from demogpt.chains.task_chains_seperate import TaskChainsSeperate
from demogpt.controllers import checkPromptTemplates, refineKeyTypeCompatiblity

def inputs_joiner(var):
    """
    used in generating if statement. Instead of if var1 and var2 and ..., it also checks if it is bool.
    """
    return f"(isinstance({var},bool) or {var})"

def separateCode(source):
    class CodeSeparator(ast.NodeVisitor):
        def __init__(self):
            self.imports = []
            self.functions = []
            self.others = []
            self.current_other = []

        def visit_Import(self, node):
            self.imports.append(ast.unparse(node))  # Convert AST node back to code

        def visit_ImportFrom(self, node):
            self.imports.append(ast.unparse(node))  # Convert AST node back to code

        def visit_FunctionDef(self, node):
            self.functions.append(ast.unparse(node))  # Convert AST node back to code

        def generic_visit(self, node):
            # For the other parts, we need to handle more types of nodes
            if isinstance(node, (ast.Expr, ast.Assign, ast.AugAssign, ast.AnnAssign, ast.For, ast.While, ast.If, ast.With, ast.Try, ast.ClassDef)):
                code = ast.unparse(node)  # Convert AST node back to code
                self.current_other.append(code)
            else:
                # For nodes that are not directly translatable to code, visit their children
                super().generic_visit(node)

        def finalize_others(self):
            # If there are any collected "other" code pieces, join them and add to the "others" list
            if self.current_other:
                self.others.append("\n".join(self.current_other))
                self.current_other = []

    separator = CodeSeparator()
    tree = ast.parse(source)
    separator.visit(tree)
    separator.finalize_others()  # Finalize any remaining "other" code pieces

    return "\n".join(separator.imports), "\n".join(separator.functions), "\n".join(separator.others)


AI_VARIETY_TEMPERATURE = 0.7

def separateCode(code):
    # Regular expression patterns
    imports_pattern = re.compile(r'^(import .*|from .* import .*)$', re.MULTILINE)
    function_pattern = re.compile(r'^(def .+:)\s*$(.*?)(?=^\S|\Z)', re.MULTILINE | re.DOTALL)

    # Extracting parts
    imports = re.findall(imports_pattern, code)
    functions = re.findall(function_pattern, code)

    # Removing the found parts from the original code
    remaining_code = re.sub(imports_pattern, '', code)
    remaining_code = re.sub(function_pattern, '', remaining_code)

    # Cleaning up the remaining code
    remaining_code = '\n'.join([line for line in remaining_code.split('\n') if line.strip()])

    return {
        'imports': '\n'.join(imports),
        'function_defs': '\n'.join([func[0] + func[1] for func in functions]),
        'remaining_code': remaining_code
    }

def catchErrors(code):
    temp_path = ''
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False, suffix='.py') as temp:
            # Write the code to the temporary file
            temp.write(code)
            temp_path = temp.name  # Get the path of the temporary file

        # Run flake8 on the temporary file
        result = subprocess.run(['flake8', '--select=E', '--ignore=E501', temp_path], capture_output=True, text=True)
    except:
        return True
    finally:
        # Clean up the temporary file if it has been created
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
    return result.returncode != 0

def init(title="", app_type={}):
    initial_code = IMPORTS_CODE_SNIPPET + "\n" + PREFIX_CODE_SNIPPET + "\n"
    if title:
        initial_code += f"\nst.title('{title}')\n"
    if app_type.get("is_search",False):
        initial_code += f"\nst_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)\n"
    return initial_code

def initSeperate(title="", app_type={}):
    prefix = PREFIX_CODE_SNIPPET 
    imports = IMPORTS_CODE_SNIPPET
    if app_type.get("is_search",False):
        prefix += f"\nst_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)\n"
    return {
        "prefix": prefix,
        "imports":imports,
        "code": prefix + "\n" + imports + "\n"
    }

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
    step2task={task["step"]:task for task in tasks}
    input_chat_step = -1
    for task in tasks:
        if task["task_type"] == "ui_input_chat":
            input_chat_step = task["step"]
            break
    
    if input_chat_step == -1:
        return tasks 

    input2tasks={}
    for task in tasks:
        for input_key in task["input_key"]:
            input2tasks[input_key] = input2tasks.get(input_key,[]) + [task]
    
    non_pre_task_steps = set() # these are the ones that cannot be done before chat input
    steps = {i for i in range(1,len(tasks)+1)}
    all_steps = {i for i in range(1,len(tasks)+1)}
    root = step2task[input_chat_step]
    non_pre_task_steps.add(root["step"])
    change = True
    while change:
        change = False
        for step in non_pre_task_steps:
            task1 = step2task[step]
            for input_key in task1["input_key"]:
                tasks1 = input2tasks[input_key]
                for task2 in tasks1:
                    if task2["step"] not in non_pre_task_steps:
                        change = True
                        non_pre_task_steps.add(task2["step"])
                        steps.remove(task["step"])
    post_steps = sorted(list(all_steps-steps))
    steps = sorted(list(steps))     
    pre_tasks = [step2task[step] for step in steps]
    post_tasks = [step2task[step] for step in post_steps]
    new_tasks = pre_tasks + post_tasks
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

def getGenericPromptTemplateCodeSeperate(task, iters):
    res = ""
    is_valid = False
    task_type = task["task_type"]
    inputs = task["input_key"]
    prompt_func = (
        TaskChains.promptTemplate if task_type == "prompt_template" else TaskChains.chat
    )
    finalizer_func = (
        getPromptChatTemplateCodeSeperate if task_type == "prompt_template" else getChatCodeSeperate
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

def getCodeSnippetSeperate(task, code_snippets, iters=10):
    #task = refineKeyTypeCompatiblity(task)
    task_type = task["task_type"]
    if task_type == "ui_input_text":
        res = TaskChainsSeperate.uiInputText(task=task, code_snippets=code_snippets)
    elif task_type == "ui_output_text":
        res = TaskChainsSeperate.uiOutputText(task=task)
    elif task_type in ["prompt_template", "chat"]:
        res = getGenericPromptTemplateCodeSeperate(task, iters=iters)
    elif task_type == "path_to_content":
        res = TaskChainsSeperate.pathToContent(task=task, code_snippets=code_snippets)
    elif task_type == "doc_to_string":
        res = TaskChainsSeperate.docToString(task=task)
    elif task_type == "string_to_doc":
        res = TaskChainsSeperate.stringToDoc(task=task)
    elif task_type == "ui_input_file":
        res = TaskChainsSeperate.uiInputFile(task=task)
    elif task_type == "doc_loader":
        res = TaskChainsSeperate.docLoad(task=task, code_snippets=code_snippets)
    elif task_type == "doc_summarizer":
        res = TaskChainsSeperate.summarize(task=task)
    elif task_type == "ui_input_chat":
        res = TaskChains.uiInputChat(task=task)
    elif task_type == "ui_output_chat":
        res = TaskChainsSeperate.uiOutputChat(task=task)
    elif task_type == "python":
        res = TaskChainsSeperate.pythonCoder(task=task, code_snippets=code_snippets)
    elif task_type == "plan_and_execute":
        res = TaskChainsSeperate.search(task=task)
    elif task_type == "search_chat":
        res = TaskChainsSeperate.search_chat(task=task)
    return res


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
        code = TaskChains.uiInputChat(task=task)
    elif task_type == "ui_output_chat":
        code = TaskChains.uiOutputChat(task=task)
    elif task_type == "python":
        code = TaskChains.pythonCoder(task=task, code_snippets=code_snippets)
    elif task_type == "plan_and_execute":
        code = TaskChains.search(task=task)
    elif task_type == "search_chat":
        code = TaskChains.search_chat(task=task)
    return code.strip() + "\n"


def refine(code):
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python") :].strip()
    return code


def reformatTasks(tasks):
    def preprocess(io):
        if io == "none":
            io = []
        elif isinstance(io, str):
            if io.startswith("["):
                io = io[1:-1]
            io = [var.strip() for var in io.split(",")]
        return io
    
    processed_tasks = []
    for task in tasks:
        input_key = preprocess(task["input_key"])
        output_key = preprocess(task["output_key"])
        input_data_type = preprocess(task["input_data_type"])
        task["input_key"] = input_key
        task["output_key"] = output_key
        task["input_data_type"] = input_data_type
        processed_tasks.append(task)
        
    processed_tasks = filterTasks(processed_tasks)

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
elif {" and ".join(list(map(inputs_joiner,inputs)))}:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = {signature}
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
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

msgs = StreamlitChatMessageHistory()

def {signature}:
    prompt = PromptTemplate(
        input_variables={input_variables}, template='''{system_template}'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="{human_input}", chat_memory=msgs, return_messages=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature={temperature})
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory
        )
    
    return chat_llm_chain.run({run_call})
    
{function_call} 

    """

    return code


def getChatCodeSeperate(template, task):
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
        if len(inputs) > 0:
            function_call = f"""
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
elif {" and ".join(list(map(inputs_joiner,inputs)))}:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = {signature}
else:
    {variable} = ""
            """
        else:
            function_call = f"""
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
else:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = {signature}
            """
    input_variables = ["chat_history"] + inputs
    human_input = template["human_input"]
    if human_input not in inputs:
        human_input = getHumanInput(system_template, inputs)
    imports = f"""
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

    """
    inputs = """
msgs = StreamlitChatMessageHistory()
    """

    functions = f"""
def {signature}:
    prompt = PromptTemplate(
        input_variables={input_variables}, template='''{system_template}'''
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="{human_input}", chat_memory=msgs, return_messages=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature={temperature})
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory
        )
    
    return chat_llm_chain.run({run_call})
    """

    return {
        "imports":imports,
        "functions":functions,
        "inputs":inputs,
        "outputs":function_call,
        "code":imports + "\n" + functions + "\n" + inputs + "\n" + function_call + "\n"
    }


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
        if len(inputs) > 0:
            function_call = f"""
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
elif {" and ".join(list(map(inputs_joiner,inputs)))}:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = {signature}
else:
    {variable} = ""
            """
        else:
            function_call = f"""
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
else:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = {signature}
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


def getPromptChatTemplateCodeSeperate(templates, task):
    inputs = task["input_key"]
    variable = ", ".join(task["output_key"])
    run_call = "{}"

    if inputs == "none":
        signature = f"{templates['function_name']}()"
        function_call = f"""
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
else:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = {signature}
        """
    else:
        if isinstance(inputs, str):
            if inputs.startswith("["):
                inputs = inputs[1:-1]
            inputs = [var.strip() for var in inputs.split(",")]
        if len(inputs) > 0:
            run_call = ", ".join([f"{var}={var}" for var in inputs])
        signature = f"{templates['function_name']}({','.join(inputs)})"
        if len(inputs) > 0:
            function_call = f"""
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
elif {" and ".join(list(map(inputs_joiner,inputs)))}:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = {signature}
else:
    {variable} = ""
            """
        else:
            function_call = f"""
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
else:
    with st.spinner('DemoGPT is working on it. It takes less than 10 seconds...'):
        {variable} = {signature}
            """

    temperature = 0 if templates.get("variety", "False") == "False" else AI_VARIETY_TEMPERATURE

    imports = f"""\n
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate)
    """
    
    functions = f"""

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

"""
    return {
        "imports":imports,
        "functions":functions,
        "inputs":"",
        "outputs":function_call,
        "code":imports + "\n" + functions + "\n" + function_call + "\n"
    }


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
    env = os.environ.copy()
    env["PYTHONPATH"] = ""
    env["OPENAI_API_KEY"] = openai_api_key
    #env["STREAMLIT_SERVER_PORT"] = "8502"
    #env["OPENAI_API_BASE"] = openai_api_base
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
"""
PREFIX_CODE_SNIPPET = """
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
