import streamlit as st
import signal
from model import LogicModel, StreamlitModel
import webbrowser
from time import sleep
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    print("dotenv import error but no needed")

num_of_iterations = 10

def generate_response(txt):
    for data in agent(txt,num_of_iterations):
        yield data
    
# Page title
title = '🦜🔗 DemoGPT'

st.set_page_config(page_title=title)
st.title(title)
# Text input

openai_api_key = st.sidebar.text_input('OpenAI API Key', placeholder='sk-...',value=os.getenv('OPENAI_API_KEY',''), type="password")
demo_title = st.text_input('Enter your demo title', placeholder='Type your demo title')
empty_idea = st.empty()
demo_idea = empty_idea.text_area('Enter your LLM-based demo idea', placeholder = 'Type your demo idea here', height=100)


st.write("Examples")


cols = st.columns([1,1,1.2])



examples = ["Language Translator 📝","Grammer Corrector 🛠","Blog post generator from title 📔"] 

pid = None

example_submitted = False

with st.form('a', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    for col,example in zip(cols,examples):
        if col.button(example):
            example_submitted = True
            demo_idea = empty_idea.text_area('Enter your LLM-based demo idea', example, height=100)
            print(demo_idea)

    if submitted or example_submitted:

        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API Key!', icon="⚠️")
        else:
            agent = LogicModel(openai_api_key=openai_api_key)
            streamlit_agent = StreamlitModel(openai_api_key=openai_api_key)

            if pid:
                print("Terminating...")
                os.kill(pid, signal.SIGTERM)
                pid = None
            
            bar = st.progress(25, "Generating Code...")
            for data in generate_response(demo_idea):
                response = data["out"]
                error = data["error"]
                code = data["code"]
                test_code = data["test_code"]
                success = data["success"]
                percentage = data["percentage"]

                if success:
                    bar.progress(75, text="Creating App...")
                    example_submitted = False
                    pid = streamlit_agent(demo_idea,demo_title,code,test_code,bar.progress,st.balloons)
                    sleep(5)
                    webbrowser.open('http://localhost:8502')

                else:
                    bar.progress(50, text="Refining Code...")

                if success:
                    #st.balloons()
                    break