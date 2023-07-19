import logging
import os
import signal
import webbrowser
from time import sleep

import streamlit as st

import utils
from langchain_coder import LangChainCoder

# logging.basicConfig(level = logging.DEBUG,format='%(levelname)s-%(message)s')

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception as e:
    logging.error("dotenv import error but no needed")

num_of_iterations = 10


def generate_response(txt, title):
    """
    Generate response using the LangChainCoder.

    Args:
        txt (str): The input text.

    Yields:
        dict: A dictionary containing response information.
    """
    for data in agent(txt, title, num_of_iterations):
        yield data


# Page title
title = "🧩 DemoGPT"

st.set_page_config(page_title=title)
st.title(title)
# Text input

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)
demo_title = st.text_input("Enter your demo title", placeholder="Type your demo title")
empty_idea = st.empty()
demo_idea = empty_idea.text_area(
    "Enter your LLM-based demo idea", placeholder="Type your demo idea here", height=100
)

st.write("Examples")

cols = st.columns([1, 1, 1.2])

PROGRESS_BAR_INFO = {
    "start": {"text": "Generating Code...", "percentage": 25},
    "langchain": {"text": "Transforming to streamlit code", "percentage": 35},
    "refining": {"text": "Refining Code...", "percentage": 50},
    "streamlit": {"text": "Creating App...", "percentage": 75},
    "failed": {"text": "Failed", "percentage": 100},
}


def progressBar(key, bar=None):
    info = PROGRESS_BAR_INFO[key]
    if bar:
        bar.progress(info["percentage"], text=info["text"])
    else:
        return st.progress(info["percentage"], text=info["text"])


examples = [
    "Language Translator 📝",
    "Grammer Corrector 🛠",
    "Blog post generator from title 📔",
]

if "pid" not in st.session_state:
    st.session_state["pid"] = -1

example_submitted = False

with st.form("a", clear_on_submit=True):
    submitted = st.form_submit_button("Submit")
    for col, example in zip(cols, examples):
        if col.button(example):
            example_submitted = True
            demo_idea = empty_idea.text_area(
                "Enter your LLM-based demo idea", example, height=100
            )
            logging.info(f"Demo Idea:{demo_idea}")

    if submitted or example_submitted:

        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API Key!", icon="⚠️")
        else:
            bar = progressBar("start")

            agent = LangChainCoder(openai_api_key=openai_api_key)

            if st.session_state["pid"] != -1:
                logging.info(f"Terminating the previous applicaton ...")
                os.kill(st.session_state["pid"], signal.SIGTERM)
                st.session_state["pid"] = -1

            code_empty = st.empty()
            for data in generate_response(demo_idea, demo_title):
                code = data["code"]
                success = data["success"]
                task_id = data["task_id"]
                stage = data["stage"]

                if success:
                    progressBar(stage, bar)
                    if stage == "streamlit" and task_id == "final":
                        with st.expander("Code"):
                            st.code(code)
                        example_submitted = False
                        st.session_state["pid"] = utils.runStreamlit(
                            code, openai_api_key
                        )
                        sleep(5)
                        webbrowser.open("http://localhost:8502")
                        break
                else:
                    progressBar("refining")
            else:
                progressBar("failed")
