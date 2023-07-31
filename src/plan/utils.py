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
    if inputs.startswith("["):
        inputs = inputs[1:-1]
        inputs = [var.strip() for var in inputs.split(",")]
    else:
        inputs = [inputs]
    variable = task["output_key"]
    templates = json.loads(res)
    run_call = "{}"
    if len(inputs) > 0:
        run_call = ", ".join([f"{var}={var}" for var in inputs])

    temperature = 0 if templates.get("variety", "False") == "False" else 0.7

    signature = f"{templates['function_name']}({str(inputs)[2:-2]})"

    code = f"""
    def {signature}:
        chat = ChatOpenAI(
            temperature={temperature}
        )
        system_template = {templates['system_template']}
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = {templates['template']}
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run({run_call})
        return result # returns string      
    {variable} = {signature}                   
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
