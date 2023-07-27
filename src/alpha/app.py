import logging
import os
import signal
import webbrowser
from time import sleep

import streamlit as st
import utils
from model import Model

# logging.basicConfig(level = logging.DEBUG,format='%(levelname)s-%(message)s')

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception as e:
    logging.error("dotenv import error but no needed")


def generate_response(txt):
    """
    Generate response using the LangChainCoder.

    Args:
        txt (str): The input text.

    Yields:
        dict: A dictionary containing response information.
    """
    for data in agent(txt):
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

model_name = st.sidebar.selectbox(
    'Model',
    ('gpt-3.5-turbo', 'gpt-4'))

empty_idea = st.empty()
demo_idea = empty_idea.text_area(
    "Enter your LLM-based demo idea", placeholder="Type your demo idea here", height=100
)

st.write("Examples")

cols = st.columns([1, 1, 1.2])

PROGRESS_BAR_INFO = {
    "start": {"text": "Plan generation started...", "percentage": 25},
    "plan": {"text": "Global plan has been generated", "percentage": 35},
    "draft": {"text": "Draft code has been generated...", "percentage": 50},
    "langchain": {"text": "Langchain code has been generated.", "percentage": 75},
    "done": {"text": "App created, directed to the demo page", "percentage": 100},
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

            agent = Model(openai_api_key=openai_api_key)
            agent.setModel(model_name)

            if st.session_state["pid"] != -1:
                logging.info(f"Terminating the previous applicaton ...")
                os.kill(st.session_state["pid"], signal.SIGTERM)
                st.session_state["pid"] = -1

            code_empty = st.empty()
            for data in generate_response(demo_idea):
                stage = data["stage"]
                code = data.get("code")

                progressBar(stage, bar)

                if code:
                    with st.expander("Code"):
                        st.code(code)
                    example_submitted = False
                    st.session_state["pid"] = utils.runStreamlit(code, openai_api_key)
                    sleep(5)
                    webbrowser.open("http://localhost:8502")
                    break
