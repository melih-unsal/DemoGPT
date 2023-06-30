import streamlit as st
from time import sleep
import os
from templates import *
   

# Page title
title = '🦜🔗 DemoGPT'

st.set_page_config(page_title=title)
st.title(title)
st.markdown(
    """
    This's just to showcase the capabilities of DemoGPT.

    For custom applications, please open in [![Open in GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/melih-unsal/DemoGPT)
    """
)
# Text input    

openai_api_key = st.text_input('Enter your OpenAI API Key', placeholder='sk-...',type="password")
demo_title = st.text_input('Enter your demo title', placeholder='Type your demo title')

st.write("Examples")

cols1 = st.columns([1,1,1.2])
cols2 = st.columns([1.6,1.5,1])

pid = None

pressed = False

if 'current' not in st.session_state:
    st.session_state['current'] = ''
    st.session_state['done'] = None 
elif st.session_state['done']:
    st.session_state['done'].empty()

for col,example in zip(cols1,examples1):
    if col.button(example):
        st.session_state['current'] = example
        pressed = True

for col,example in zip(cols2,examples2):
    if col.button(example):
        st.session_state['current'] = example
        pressed = True

st.markdown('----')
if st.session_state['current']:
    with st.container():
        if not openai_api_key:
            st.warning('Please enter your OpenAI API Key', icon="⚠️")
        else:
            if pressed:
                wait()
                st.session_state['done'] = st.success('Done!')
            example2pages[st.session_state['current']](openai_api_key,demo_title)
st.markdown('----')
REPO_URL = "https://github.com/melih-unsal/DemoGPT"
st.markdown(f"project [repo on github]({REPO_URL}) waiting for your :star:")