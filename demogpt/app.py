import logging
import os
import signal
import sys

import streamlit as st

import streamlit.components.v1 as components

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
parent_directory = os.path.dirname(current_directory)
grandparent_directory = os.path.dirname(parent_directory)
sys.path.append(grandparent_directory)

from model import DemoGPT
from utils import runStreamlit


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


def initCode():
    if "code" not in st.session_state:
        st.session_state["code"] = ""
        st.session_state.edit_mode = False


# Page title
title = "🧩 DemoGPT"

st.set_page_config(page_title=title)
    
st.title(title)


initCode()

# Text input

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

openai_api_base = st.sidebar.text_input(
    "Open AI base URL",
    placeholder="https://api.openai.com/v1",
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
    "Enter your LLM-based demo idea",
    placeholder="Type your demo idea here",
    height=100,
    help="""## Example prompts
* Character Clone: Want an app that converses like Jeff Bezos? Prompt - "Create me a chat-based application that talks like Jeff Bezos."
* Language Mastery: Need help in learning French? Prompt - "Create me an application that translates English sentences to French and provides pronunciation guidance for learners. 
* Content Generation: Looking to generate content? Prompt - "Create a system that can write ready to share Medium article from website. The resulting Medium article should be creative and interesting and written in a markdown format."
    """,
)

empty_title = st.empty()
demo_title = empty_title.text_input(
    "Give a name for your application",
    placeholder="Title",
    help="It will be displayed as a title in your app",
)


def progressBar(percentage, bar=None):
    if bar:
        bar.progress(percentage)
    else:
        return st.progress(percentage)


if "pid" not in st.session_state:
    st.session_state["pid"] = -1

if "done" not in st.session_state:
    st.session_state["done"] = False

with st.form("a", clear_on_submit=True):
    submitted = st.form_submit_button("Submit")


def kill():
    if st.session_state["pid"] != -1:
        logging.info(f"Terminating the previous applicaton ...")
        try:
            os.kill(st.session_state["pid"], signal.SIGTERM)
        except Exception as e:
            pass
        st.session_state["pid"] = -1


if submitted:
    st.session_state.messages = []
    if not openai_api_key:
        st.warning("Please enter your OpenAI API Key!", icon="⚠️")
    else:
        bar = progressBar(0)
        st.session_state.container = st.container()
        try:
            agent = DemoGPT(openai_api_key=openai_api_key, openai_api_base=openai_api_base)
            agent.setModel(model_name)
        except Exception as e:
            st.warning(e)
        else:
            kill()
            code_empty = st.empty()
            st.session_state.container = st.container()
            for data in generate_response(demo_idea, demo_title):
                done = data.get("done", False)
                failed = data.get("failed", False)
                message = data.get("message", "")
                st.session_state["message"] = message
                stage = data.get("stage", "stage")
                code = data.get("code", "")
                progressBar(data["percentage"], bar)

                st.session_state["done"] = done
                st.session_state["failed"] = failed
                st.session_state["message"] = message

                if done or failed:
                    st.session_state.code = code
                    break

                st.info(message, icon="🧩")
                st.session_state.messages.append(message)

elif "messages" in st.session_state:
    for message in st.session_state.messages:
        st.info(message, icon="🧩")

if st.session_state.done:
    st.success(st.session_state.message)
    with st.expander("Code", expanded=True):
        code_empty = st.empty()
        if st.session_state.edit_mode:
            new_code = code_empty.text_area("", st.session_state.code, height=500)
            if st.button("Save & Rerun"):
                st.session_state.code = (
                    new_code  # Save the edited code to session state
                )
                st.session_state.edit_mode = False  # Exit edit mode
                code_empty.code(new_code)
                kill()
                st.session_state["pid"] = runStreamlit(
                    new_code, openai_api_key, openai_api_base
                )
                st.experimental_rerun()

        else:
            code_empty.code(st.session_state.code)
            if st.button("Edit"):
                st.session_state.edit_mode = True  # Enter edit mode
                st.experimental_rerun()
    example_submitted = False
    if submitted:
        st.session_state["pid"] = runStreamlit(code, openai_api_key, openai_api_base)

if st.session_state.get("failed", False):
    with st.form("fail"):
        st.warning(st.session_state["message"])
        email = st.text_input("Email", placeholder="example@example.com")
        email_submit = st.form_submit_button("Send")
    if email_submit:
        st.success(
            "🌟 Thank you for entrusting us with your vision! We're on it and will ping you the moment your app is ready to launch. Stay tuned for a stellar update soon!"
        )