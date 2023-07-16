import streamlit as st
import signal
from langchain_coder import LangChainCoder
import utils
import webbrowser
from time import sleep
import os
import logging 

logging.basicConfig(level = logging.DEBUG,format='%(levelname)s-%(message)s')

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    logging.error("dotenv import error but no needed")

num_of_iterations = 10

def generate_response(txt):
    """
    Generate response using the LangChainCoder.

    Args:
        txt (str): The input text.

    Yields:
        dict: A dictionary containing response information.
    """
    for data in agent(txt,num_of_iterations):
        yield data
    
# Page title
title = '🧩 DemoGPT'

st.set_page_config(page_title=title)
st.title(title)
# Text input

openai_api_key = st.sidebar.text_input('OpenAI API Key', placeholder='sk-...',value=os.getenv('OPENAI_API_KEY',''), type="password")
demo_title = st.text_input('Enter your demo title', placeholder='Type your demo title')
empty_idea = st.empty()
demo_idea = empty_idea.text_area('Enter your LLM-based demo idea', placeholder = 'Type your demo idea here', height=100)

st.write("Examples")

cols = st.columns([1,1,1.2])

PROGRESS_BAR_TEXTS = {
    "start":"Generating Code...",
    "creating":"Creating App...",
    "refining":"Refining Code...",
    "failed":"Failed"
}

examples = ["Language Translator 📝","Grammer Corrector 🛠","Blog post generator from title 📔"] 

if 'pid' not in st.session_state:
    st.session_state['pid'] = -1

example_submitted = False

with st.form('a', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    for col,example in zip(cols,examples):
        if col.button(example):
            example_submitted = True
            demo_idea = empty_idea.text_area('Enter your LLM-based demo idea', example, height=100)
            logging.info(f"Demo Idea:{demo_idea}")

    if submitted or example_submitted:

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API Key!', icon="⚠️")
        else:
            agent = LangChainCoder(openai_api_key=openai_api_key)

            if st.session_state['pid'] != -1:
                logging.info(f"Terminating the previous applicaton ...")
                os.kill(st.session_state['pid'], signal.SIGTERM)
                st.session_state['pid'] = -1
            
            bar = st.progress(25, PROGRESS_BAR_TEXTS["start"])
            for data in generate_response(demo_idea):
                code = data["code"]
                success = data["success"]
                task_id = data["task_id"]
                stage = data["stage"]

                with st.expander("Code"):
                    st.code(code)

                if success:
                    if stage == "streamlit":
                        bar.progress(75, text=PROGRESS_BAR_TEXTS["creating"])
                        example_submitted = False
                        st.session_state['pid'] = utils.runStreamlit(code,openai_api_key)
                        sleep(5)
                        webbrowser.open('http://localhost:8502')
                    else:
                        bar.progress(75, text="Transforming to streamlit code")


                else:
                    bar.progress(50, text=PROGRESS_BAR_TEXTS["refining"])

                if success:
                    break
            else:
                bar.progress(100, text=PROGRESS_BAR_TEXTS["failed"])
