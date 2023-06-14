import streamlit as st
from model import Model


agent = Model()

def generate_response(txt):
    for code,response in agent(txt):
        yield code,response
    
# Page title
title = '🦜🔗 DemoGPT'

st.set_page_config(page_title=title)
st.title(title)
# Text input
txt_input = st.text_area('Enter your LLM-based demo idea', '', height=200)

empty_code = st.empty()
empty_response = st.empty()

# Form to accept user's text input for summarization
result = []

with st.form('a', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    if submitted:
        with st.spinner('Calculating...'):
            for code,response in generate_response(txt_input):
                empty_code.code(code, language='python')
                empty_response.markdown(response)

if len(result):
    st.balloons()