import streamlit as st
import signal
from model import LogicModel, StreamlitModel
import webbrowser
from time import sleep
from dotenv import load_dotenv
import os
load_dotenv()

num_of_iterations = 10

def generate_response(txt):
    for data in agent(txt,num_of_iterations):
        yield data
    
# Page title
title = '🦜🔗 DemoGPT'

st.set_page_config(page_title=title)
st.title(title)
# Text input

openai_api_key = st.text_input('Enter your OpenAI API Key', placeholder='sk-...',value=os.getenv('OPENAI_API_KEY',''),type="password")
demo_title = st.text_input('Enter your demo title', placeholder='Type your demo title')

st.write("Examples")

cols = st.columns([1,1,1.2])

examples = ["Language Translator 📝","Grammer Corrector 🛠","Blog post generator from title 📔"] 

pid = None

submitted = False

for col,example in zip(cols,examples):
    if col.button(example):
        submitted = True
        demo_idea = example[:-1]
        print(demo_idea)


if not openai_api_key:
    st.warning('Please enter your OpenAI API Key', icon="⚠️")
else:
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
            sleep(4)
            webbrowser.open('http://localhost:8502')

        else:
            bar.progress(50, text="Refining Code...")

        if success:
            #st.balloons()
            break