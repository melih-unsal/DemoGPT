import streamlit as st
from time import sleep
from dotenv import load_dotenv
import os
load_dotenv()
from templates import *
   
    
# Page title
title = '🦜🔗 DemoGPT'

st.set_page_config(page_title=title)
st.title(title)
# Text input

openai_api_key = st.text_input('Enter your OpenAI API Key', placeholder='sk-...',value=os.getenv('OPENAI_API_KEY',''),type="password")
demo_title = st.text_input('Enter your demo title', placeholder='Type your demo title')

st.write("Examples")

cols = st.columns([1,1,1.2,1.2])

pid = None

submitted = False

demo_name = st.sidebar.selectbox("Choose a demo", example2pages.keys())
if openai_api_key:
    example2pages[demo_name](openai_api_key,demo_title)
else:
    st.warning('Please enter your OpenAI API Key', icon="⚠️")