import logging
import os
import signal
import webbrowser
from time import sleep

import streamlit as st
from utils import runStreamlit
from model import DemoGPT

# logging.basicConfig(level = logging.DEBUG,format='%(levelname)s-%(message)s')

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception as e:
    logging.error("dotenv import error but no needed")


def generate_response(txt, title):
    """
    Generate response using the LangChainCoder.

    Args:
        txt (str): The input text.

    Yields:
        dict: A dictionary containing response information.
    """
    for data in agent(txt, title):
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

models = (
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
)

model_name = st.sidebar.selectbox("Model", models)

empty_idea = st.empty()
demo_idea = empty_idea.text_area(
    "Enter your LLM-based demo idea", placeholder="Type your demo idea here", height=100
)

empty_title = st.empty()
demo_title = empty_title.text_input(
    "Give a name for your application", placeholder="Title"
)


def progressBar(percentage, bar=None):
    if bar:
        bar.progress(percentage)
    else:
        return st.progress(percentage)


if "pid" not in st.session_state:
    st.session_state["pid"] = -1


with st.form("a", clear_on_submit=True):
    submitted = st.form_submit_button("Submit")

if submitted:

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API Key!", icon="⚠️")
    else:
        bar = progressBar(0)
        container = st.container()

        agent = DemoGPT(openai_api_key=openai_api_key)
        agent.setModel(model_name)

        if st.session_state["pid"] != -1:
            logging.info(f"Terminating the previous applicaton ...")
            try:
                os.kill(st.session_state["pid"], signal.SIGTERM)
            except Exception as e:
                pass
            st.session_state["pid"] = -1

        code_empty = st.empty()
        for data in generate_response(demo_idea, demo_title):
            done = data["done"]
            message = data["message"]
            stage = data["stage"]
            completed = data["completed"]
            code = data.get("code")

            progressBar(data["percentage"], bar)

            if done:
                container.success(message)
                with st.expander("Code"):
                    st.code(code)
                example_submitted = False
                st.session_state["pid"] = runStreamlit(code, openai_api_key)
                break
            else:
                container.info("🧩 " + message)
