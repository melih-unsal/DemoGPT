import streamlit as st
import os
import signal
from model import LogicModel, StreamlitModel
import webbrowser
from time import sleep

num_of_iterations = 10

agent = LogicModel()

streamlit_agent = StreamlitModel()

def generate_response(txt):
    for data in agent(txt,num_of_iterations):
        yield data
    
# Page title
title = '🦜🔗 DemoGPT'

st.set_page_config(page_title=title)
st.title(title)
# Text input
demo_title = st.text_input('Enter your demo title', 'Awesome App')
demo_idea = st.text_area('Enter your LLM-based demo idea', placeholder = 'Type your demo idea here', height=100)

cols = st.columns(3)


examples = ["Language Translator 📝","Grammer Corrector 🛠","Blog post generator from title 📔"] 

pid = None

example_submitted = False

with st.form('a', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    st.write("Examples")
    for col,example in zip(cols,examples):
        if col.button(example):
            example_submitted = True
            demo_idea = example
            print(demo_idea)

    if submitted or example_submitted:

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
                sleep(4)
                webbrowser.open('http://localhost:8502')
            else:
                bar.progress(50, text="Refining Code...")

            if success:
                st.balloons()
                break