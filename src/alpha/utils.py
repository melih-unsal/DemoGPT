import shutil
import tempfile
from subprocess import Popen

from chains.chains import Chains


def refine(code):
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python") :].strip()
    return code


def getAIPieces(task_list):
    ai_tasks = [task for task in task_list if task["model_type"] == "ai"]
    ai_functions = [task["function_name"] for task in ai_tasks]
    return ai_tasks, ai_functions


def getLangchainFunctions(ai_tasks):
    langchain_functions = ""
    for task in ai_tasks:
        function_name = task["function_name"]
        inputs = task["input_key"]
        description = task["description"]
        if isinstance(inputs, str):
            inputs = [inputs]
        langchain_code = Chains.draft(
            inputs=inputs, instruction=description, function_name=function_name
        )
        langchain_functions += langchain_code + "\n\n\n"
    return langchain_functions


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
