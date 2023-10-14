import logging
import os
import signal
import tempfile
import webbrowser
from time import sleep

import components
import cv2
import requests
import streamlit as st
from demogpt import DemoGPT
from utils import generateImage, getEmbeddings, getUrl

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = st.secrets.get("LANGCHAIN_API_KEY","")
os.environ["LANGCHAIN_PROJECT"] = st.secrets.get("LANGCHAIN_PROJECT","")

DEPLOY_URL = st.secrets.get("DEPLOY_URL","")
API_URL = st.secrets.get("API_URL","")

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception as e:
    logging.error("dotenv import error but no needed")


def generate_response(txt):
    for data in agent(txt):
        yield data
        
toast_messages = [
    "🌱 Planting the seeds...",
    "🌦️ Watering and waiting...",
    "☀️ Soaking up some sunshine...",
    "🌳 Watching the beans grow...",
    "🍂 Harvesting time...",
    "☕ Grinding the beans...",
    "🚰 Pouring the water...",
    "⏳ Steeping...",
    "🥛 Adding a splash of milk. Just 1 more step left...",
    "✨ Voilà! Your brew is ready. Enjoy your application!"
]
        
def create(code):
    image = generateImage(demo_idea, openai_api_key, openai_api_base)
    index = 0
    embeddings = getEmbeddings(demo_idea, openai_api_key)
    with tempfile.NamedTemporaryFile("w", suffix=".jpg") as tmp:
        cv2.imwrite(tmp.name, image)
        tmp.flush()  # Make sure the data is written to disk
        while True:
            if index < len(toast_messages) - 1:
                index += 1
                
            data={
                "code": code, 
                "prompt":demo_idea, 
                "title":st.session_state.title,
                "embeddings":embeddings
                }

            with open(tmp.name, 'rb') as file:
                res = requests.post(DEPLOY_URL + "create", data=data, files={"image": file})
                try:
                    st.session_state.app_id = res.json()["id"]
                    st.session_state.url = getUrl(st.session_state.app_id) 
                except:
                    yield index
                else:
                    break
    yield index

def sendEmail(email):
    res = requests.post(API_URL + "email", 
                        data={
                            "email": email, 
                            "description":demo_idea,
                            "title":st.session_state.title
                            }
                        )
                     
def edit(code):
    res = requests.post(DEPLOY_URL + "edit", data={
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


st.sidebar.markdown(components.how_to_use)

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

openai_api_base = st.sidebar.text_input(
    "Open AI base URL (Optional)",
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

st.sidebar.markdown(components.about)
st.sidebar.markdown(components.faq)

overview = st.text_area(
    "Explain your LLM-based application idea *",
    placeholder="Type your application idea here",
    height=100,
    help="""## Example prompts
* Character Clone: Want an app that converses like Jeff Bezos? Prompt - "A chat-based application that talks like Jeff Bezos."
* Language Mastery: Need help in learning French? Prompt - "An application that translates English sentences to French and provides pronunciation guidance for learners. 
* Content Generation: Looking to generate content? Prompt - "A system that can write ready to share Medium article from website. The resulting Medium article should be creative and interesting and written in a markdown format."
    """,
)

features = st.text_input(
    "List all specific features desired for your app (comma seperated)",
    placeholder="Document interpretation, question answering, ...",
    help="Please provide a comprehensive list of specific features and functionalities you envision in your application, ensuring each element supports your overall objectives and user needs.(comma seperated)"
    )

if overview and features:
    demo_idea = f"Overview:{overview}\nFeatures:{features}"
elif overview:
    demo_idea = overview
else:
    demo_idea = ""

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
    if not demo_idea:
        st.warning("Please enter your demo idea", icon="⚠️")
        st.stop()
        
    st.session_state.messages = []
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API Key!", icon="⚠️")
    elif demo_idea:
        bar = progressBar(0)
        st.session_state.container = st.container()
        try:
            agent = DemoGPT(openai_api_key=openai_api_key, openai_api_base=openai_api_base)
            agent.setModel(model_name)
        except Exception as e:
            st.warning(e)
        else:
            code_empty = st.empty()
            st.session_state.container = st.container()
            st.session_state.done = False
            st.session_state.app_deployed = False
            st.session_state.app_editted = False
            for data in generate_response(demo_idea):
                done = data.get("done",False)
                failed = data.get("failed", False)
                message = data.get("message","")
                st.session_state["message"] = message
                stage = data.get("stage","stage")
                code = data.get("code","")
                progressBar(data["percentage"], bar)
                
                st.session_state["done"] = done
                st.session_state["failed"] = failed
                st.session_state["message"] = message

                if done or failed:
                    st.session_state.code = code
                    st.session_state.title=data.get("title","")
                    break
                
                st.info(message,icon="🧩") 
                st.session_state.messages.append(message)  
            
elif "messages" in st.session_state:
    for message in st.session_state.messages:
        st.info(message,icon="🧩")                

if st.session_state.done:
    #st.success(st.session_state.message)
    with st.expander("Code",expanded=st.session_state.get("app_deployed",False)):
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
            index = 0
            for i in create(st.session_state.code):
                if i != index:
                    st.info(toast_messages[index])
                index = i
                sleep(30)
            
            for i in range(index+1,len(toast_messages)):
                sleep(30)
                st.info(toast_messages[i])
            st.session_state.app_deployed = True
            webbrowser.open_new_tab(st.session_state.url) 
    if not st.session_state.get("app_editted", False):
        st.success("Your app has been successfully created.", icon="✅")
    else:
        st.success("Your app has been successfully updated.", icon="✅")
    
    link = f"""<a href="{st.session_state.url}" style="font-size: 24px; text-decoration: none; color: green;">🥳 Woohoo! Your app's up and running. <span style="text-decoration: underline;">Click to explore!</span></a>"""
    st.markdown(link, unsafe_allow_html=True)
    
    
if st.session_state.get("failed",False):
    with st.form('fail'):
        st.warning(st.session_state["message"])
        email = st.text_input("Email", placeholder="example@example.com")
        email_submit = st.form_submit_button('Send')
    if email_submit:
        sendEmail(email)
        st.success("🌟 Thank you for entrusting us with your vision! We're on it and will ping you the moment your app is ready to launch. Stay tuned for a stellar update soon!")