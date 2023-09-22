import logging
import os
import signal

import streamlit as st
from utils import  generateImage, getUrl
from demogpt import DemoGPT
import requests
import tempfile
import cv2
import webbrowser
from time import sleep
from streamlit.components.v1 import html

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception as e:
    logging.error("dotenv import error but no needed")


def generate_response(txt, title):
    for data in agent(txt, title):
        yield data
        
SERVER_URL = "https://api.demogpt.io/"
        
def create(code):
    image = generateImage(demo_idea, openai_api_key, openai_api_base)
    with tempfile.NamedTemporaryFile("w", suffix=".jpg") as tmp:
        cv2.imwrite(tmp.name, image)
        tmp.flush()  # Make sure the data is written to disk
        with open(tmp.name, 'rb') as file:
            res = requests.post(SERVER_URL + "create", data={"code": code, "prompt":demo_idea, "title":demo_title}, files={"image": file})
            st.session_state.app_id = res.json()["id"]
            st.session_state.url = getUrl(st.session_state.app_id, demo_title, demo_idea)
            
def edit(code):
    res = requests.post(SERVER_URL + "edit", data={
        "code": code, "app_id":st.session_state.app_id})
    
def initCode():
    if "code" not in st.session_state:
        st.session_state["code"] = "" 
        st.session_state.edit_mode = False
        
initCode()
    
# Page title
title = "🧩 DemoGPT"

st.set_page_config(page_title=title)
st.title(title)

button_style = st.markdown("""
<style>
button[kind="primary"] {
    background-color: rgb(0, 200, 0);
    padding: 14px 40px;
    width: 40%;
    text-align: center;
}
button[kind="primary"]:hover {
    background-color: rgb(0, 230, 0);
}
</style>""", unsafe_allow_html=True)

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
    
if "done" not in st.session_state:
    st.session_state["done"] = False

with st.form("a", clear_on_submit=True):
    submitted = st.form_submit_button("Submit") 

if submitted:
    st.session_state.messages = []
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API Key!", icon="⚠️")
    else:
        bar = progressBar(0)
        st.session_state.container = st.container()
        agent = DemoGPT(openai_api_key=openai_api_key)
        agent.setModel(model_name)
        code_empty = st.empty()
        st.session_state.container = st.container()
        st.session_state.done = False
        st.session_state.app_deployed = False
        st.session_state.app_editted = False
        for data in generate_response(demo_idea, demo_title):
            done = data.get("done",False)
            message = data.get("message","")
            st.session_state["message"] = message
            stage = data.get("stage","stage")
            code = data.get("code","")
            progressBar(data["percentage"], bar)
            
            st.session_state["done"] = True

            if done:
                st.session_state.code = code
                break
            
            st.info(message,icon="🧩") 
            st.session_state.messages.append(message)  
            
elif "messages" in st.session_state:
    for message in st.session_state.messages:
        st.info(message,icon="🧩")                

if st.session_state.done:
    #st.success(st.session_state.message)
    with st.expander("Code",expanded=st.session_state.app_deployed):
        code_empty = st.empty()
        if st.session_state.edit_mode:
            new_code = code_empty.text_area("", st.session_state.code,height=500)
            if st.button("Save & Rerun"):
                st.session_state.code = new_code  # Save the edited code to session state
                st.session_state.edit_mode = False  # Exit edit mode
                code_empty.code(new_code)
                with st.spinner('App is being updated...'):
                    edit(st.session_state.code)
                    st.session_state.app_editted = True
                    sleep(15) # to make the app ready.
                    webbrowser.open_new_tab(st.session_state.url) 
                st.experimental_rerun()
                
        else:
            print("st.session_state.code:",st.session_state.code)
            code_empty.code(st.session_state.code)
            if st.button("Edit"):
                st.session_state.edit_mode = True  # Enter edit mode
                st.experimental_rerun()            
    if not st.session_state.get("app_deployed", False):
        with st.spinner('App is being deployed. It takes 4-5 minutes...'):
            create(st.session_state.code)
            sleep(240) # to make the app ready.
            st.session_state.app_deployed = True
            webbrowser.open_new_tab(st.session_state.url) 
    if not st.session_state.get("app_editted", False):
        st.success("Your app has been successfully created.", icon="✅")
    else:
        st.success("Your app has been successfully updated.", icon="✅")
    
    link = f"""<a href="{st.session_state.url}" style="font-size: 24px; text-decoration: none; color: green;">🥳 Woohoo! Your app's up and running. <span style="text-decoration: underline;">Click to explore!</span></a>"""
    st.markdown(link, unsafe_allow_html=True)