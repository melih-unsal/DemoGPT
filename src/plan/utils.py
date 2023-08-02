import shutil
import tempfile
from subprocess import Popen
import json
from chains.chains import Chains


def refine(code):
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python") :].strip()
    return code

def getPromptChatTemplateCode(res,task):
    inputs = task["input_key"]
    templates = json.loads(res)
    variable = task["output_key"]
    button_text = templates["button_text"]
    button = f"st.button('{button_text}')"
    run_call = "{}"


    if inputs == "none":
        signature = f"{templates['function_name']}()"
        function_call = f"{variable} = {signature}"
    else:
        if isinstance(inputs, str):
            if inputs.startswith("["):
                inputs = inputs[1:-1]
                inputs = [var.strip() for var in inputs.split(",")]
            else:
                inputs = [inputs]
        if len(inputs) > 0:
            run_call = ", ".join([f"{var}={var}" for var in inputs])
        signature = f"{templates['function_name']}({','.join(inputs)})"
        if False:
            function_call = f"""
if {' and '.join(inputs+[button])}:
    {variable} = {signature}
else:
    {variable} = ""
        """
        
    function_call = f"{variable} = {signature}"
    temperature = 0 if templates.get("variety", "False") == "False" else 0.7

    print("inputs:",inputs)


    code = f"""\n
def {signature}:
    chat = ChatOpenAI(
        temperature={temperature}
    )
    system_template = "{templates['system_template']}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "{templates['template']}"
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

def runStreamlit(code, openai_api_key):
    """
    Runs the provided code as a Streamlit application and returns the process ID.

    Args:
        code (str): The code of the Streamlit application.

    Returns:
        int: The process ID of the Streamlit application.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp.flush()
        environmental_variables = {
            "OPENAI_API_KEY": openai_api_key,
            "STREAMLIT_SERVER_PORT": "8502",
        }
        streamlit_path = shutil.which("streamlit")
        process = Popen([streamlit_path, "run", tmp.name], env=environmental_variables)
        return process.pid


IMPORTS_CODE_SNIPPET = """
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

"""
