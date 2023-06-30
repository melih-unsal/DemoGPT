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

pressed = False

if 'current' not in st.session_state:
    st.session_state['current'] = ''
    st.session_state['done'] = None 
elif st.session_state['done']:
    st.session_state['done'].empty()

for col,example in zip(cols,examples):
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