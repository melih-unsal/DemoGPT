import os
import shutil
import sys
import tempfile
from subprocess import PIPE, Popen, TimeoutExpired

from dotenv import load_dotenv

load_dotenv()


def decodeResults(results):
    return (res.strip().decode("utf-8") for res in results)


def refineCode(code):
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python") :].strip()
    return code


def runPython(code, timeout_sec=10):
    code = refineCode(code)
    with tempfile.NamedTemporaryFile("w") as tmp:
        tmp.write(code)
        tmp.flush()
        environmental_variables = {"OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")}
        python_path = shutil.which("python")
        if not python_path:  # shows 'which' returns None
            python_path = sys.executable
        process = Popen(
            [python_path, tmp.name],
            env=environmental_variables,
            stdout=PIPE,
            stderr=PIPE,
        )
        try:
            output, err = decodeResults(process.communicate(timeout=timeout_sec))
            success = len(err) == 0
        except TimeoutExpired:
            process.kill()
            success = True
            output = err = ""
        return output, err, success


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
