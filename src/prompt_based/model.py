import logging
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import threading
from subprocess import PIPE
from threading import Timer

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from prompt_based.prompts import *
from pkg_resources import resource_stream


class BaseModel:
    """
    Base class for the LogicModel and StreamlitModel classes.

    Methods:
        - __init__(self, openai_api_key: str):
            Initializes the BaseModel with the provided OpenAI API key.

        - refine_code(self, code: str) -> str:
            Refines the provided code by removing unnecessary parts.
    """

    def __init__(self, openai_api_key):
        """
        Initializes the BaseModel with the provided OpenAI API key.

        Args:
            openai_api_key (str): The OpenAI API key.
        """
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.0)

    def refine_code(self, code):
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
                code = code[len("python") :].strip()
        return code


class LogicModel(BaseModel):
    """
    Represents the logic model for generating Python code.

    Methods:
        - __init__(self, openai_api_key: str):
            Initializes the LogicModel with the provided OpenAI API key.

        - addDocuments(self):
            Adds documents to the logic model for generating Python code.

        - decode_results(self, results) -> Generator[str, None, None]:
            Decodes the results returned by the GPT-3.5-turbo model.

        - run_python(self, code: str) -> Tuple[str, str, bool]:
            Executes the Python code using the subprocess module.

        - __call__(self, topic: str, num_iterations: int = 10) -> Generator[Dict[str, Any], None, None]:
            Executes the logic model to generate Python code based on the given topic.
    """

    def __init__(self, openai_api_key):
        """
        Initializes the LogicModel with the provided OpenAI API key.

        Args:
            openai_api_key (str): The OpenAI API key.
        """
        super().__init__(openai_api_key)
        self.code_chain = LLMChain(llm=self.llm, prompt=code_prompt)
        self.test_chain = LLMChain(llm=self.llm, prompt=test_prompt)
        self.refine_chain = LLMChain(llm=self.llm, prompt=refine_chat_prompt)
        self.fix_chain = LLMChain(llm=self.llm, prompt=fix_chat_prompt)
        self.check_chain = LLMChain(llm=self.llm, prompt=check_chat_prompt)
        self.addDocuments()

    def addDocuments(self):
        """
        Adds documents to the logic model for generating Python code.
        """
        self.document = ""
        for path in ["prompts.txt"]:
            with resource_stream('prompt_based', path) as f:
                self.document += f.read().decode('utf-8')

    def decode_results(self, results):
        """
        Decodes the results returned by the executed python code

        Args:
            results: The results to be decoded.

        Returns:
            Tuple[str, str]: The decoded results.
        """
        return (res.strip().decode("utf-8", errors="ignore") for res in results)

    def run_python(self, code):
        """
        Executes the Python code using the subprocess module.

        Args:
            code (str): The Python code to be executed.

        Returns:
            Tuple[str, str, bool]: The output, error, and success status of the execution.
        """
        tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding='utf-8')
        tmp.write(code)
        tmp.flush()
        environmental_variables = {"OPENAI_API_KEY": self.openai_api_key}
        python_path = shutil.which("python")
        if platform.system() == "Windows":
            env = os.environ.copy()
            env["PYTHONPATH"] = ""
            env["OPENAI_API_KEY"] = self.openai_api_key
            python_path = sys.executable
            process = subprocess.Popen(
                [python_path, tmp.name], env=env, stdout=PIPE, stderr=PIPE
            )
        else:
            process = subprocess.Popen(
                [python_path, tmp.name],
                env=environmental_variables,
                stdout=PIPE,
                stderr=PIPE,
            )
        try:
            tmp.close()
        except PermissionError:
            pass
        output, err = self.decode_results(process.communicate())
        success = len(err) == 0
        return output, err, success

    def __call__(self, topic, num_iterations=10):
        """
        Executes the logic model to generate Python code based on the given topic.

        Args:
            topic (str): The topic or goal of the code generation.
            num_iterations (int, optional): The maximum number of iterations. Defaults to 10.

        Yields:
            Generator[Dict[str, Any], None, None]: A dictionary containing information about each iteration.
        """
        error = ""
        percentage = 0
        feedback = ""
        total_code = ""
        refined_code = ""

        for i in range(num_iterations):
            if error:
                code = self.refine_chain.run(
                    content=code, critics=feedback, document=self.document
                )
            else:
                code = self.code_chain.run(document=self.document, topic=topic)
            code = self.refine_code(code)

            test_code = self.test_chain.run(code=code, topic=topic, feedback=feedback)
            test_code = self.refine_code(test_code)

            total_code = code + "\n" + test_code

            response, error, success = self.run_python(total_code)

            if not success:
                logging.warning(f"Iteration:{i}:{error}")

            if success:
                break

            response = error

            feedback = self.fix_chain.run(code=total_code, error=error)

            percentage += 100 // num_iterations

            yield {
                "code": code,
                "total_code": total_code,
                "success": success,
                "out": response,
                "error": error,
                "feedback": feedback,
                "test_code": test_code,
                "refined_code": refined_code,
                "percentage": min(100, percentage),
            }

        yield {
            "code": code,
            "total_code": total_code,
            "success": success,
            "out": response,
            "error": error,
            "feedback": feedback,
            "test_code": test_code,
            "refined_code": refined_code,
            "percentage": 100,
        }


class StreamlitModel(BaseModel):
    """
    Represents the Streamlit model for generating Streamlit applications.

    Methods:
        - __init__(self, openai_api_key: str):
            Initializes the StreamlitModel with the provided OpenAI API key.

        - run_code(self, code: str) -> int:
            Runs the provided code as a Streamlit application and returns the process ID.

        - __call__(self, topic: str, title: str, code: str, test_code: str, progress_func: Callable[[int, str]], success_func: Callable[[], None]) -> int:
            Executes the Streamlit model to generate a Streamlit application.
    """

    def __init__(self, openai_api_key):
        """
        Initializes the StreamlitModel with the provided OpenAI API key.

        Args:
            openai_api_key (str): The OpenAI API key.
        """
        super().__init__(openai_api_key)
        self.streamlit_code_chain = LLMChain(llm=self.llm, prompt=streamlit_code_prompt)

    def runThread(self, proc):
        proc.communicate()

    def run_code(self, code):
        """
        Runs the provided code as a Streamlit application and returns the process ID.

        Args:
            code (str): The code of the Streamlit application.

        Returns:
            int: The process ID of the Streamlit application.
        """
        tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,encoding='utf-8')
        tmp.write(code)
        tmp.flush()
        environmental_variables = {
            "OPENAI_API_KEY": self.openai_api_key,
            "STREAMLIT_SERVER_PORT": "8502",
        }
        streamlit_path = shutil.which("streamlit")
        if platform.system() == "Windows":
            env = os.environ.copy()
            env["PYTHONPATH"] = ""
            env["OPENAI_API_KEY"] = self.openai_api_key
            env["STREAMLIT_SERVER_PORT"] = "8502"
            python_path = sys.executable
            process = subprocess.Popen(
                [python_path, "-m", "streamlit", "run", tmp.name],
                env=env,
                stdout=PIPE,
                stderr=PIPE,
            )
            threading.Thread(target=self.runThread, args=(process,)).start()
        else:
            process = subprocess.Popen(
                [streamlit_path, "run", tmp.name],
                env=environmental_variables,
                stdout=PIPE,
                stderr=PIPE,
            )
        try:
            tmp.close()
        except PermissionError:
            pass

        return process.pid

    def __call__(self, topic, title, code, test_code, progress_func, success_func):
        """
        Executes the Streamlit model to generate a Streamlit application.

        Args:
            topic (str): The topic or goal of the application.
            title (str): The title of the Streamlit application.
            code (str): The logic code of the application.
            test_code (str): The test code of the application.
            progress_func (Callable[[int, str]]): A function to update the progress of the application generation.
            success_func (Callable[[], None]): A function to indicate the success of the application generation.

        Returns:
            int: The process ID of the Streamlit application.
        """
        streamlit_code = self.streamlit_code_chain.run(
            topic=topic, title=title, logic_code=code, test_code=test_code
        )
        refined_code = self.refine_code(streamlit_code)
        progress_func(100, "Redirecting to the demo page...")
        success_func()
        return self.run_code(refined_code), refined_code
