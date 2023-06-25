import streamlit as st
from model import Model

num_of_iterations = 10

agent = Model()

def generate_response(txt):
    for data in agent(txt,num_of_iterations):
        yield data
    
# Page title
title = '🦜🔗 DemoGPT'

st.set_page_config(page_title=title)
st.title(title)
# Text input
txt_input = st.text_area('Enter your LLM-based demo idea', '', height=200)


with st.form('a', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')

    st.subheader("Code")
    empty_code = st.empty()

    st.subheader("Response")
    empty_response = st.empty()

    st.subheader("Error")
    empty_error = st.empty()

    if submitted:
        bar = st.progress(0, text="Processing...")
        for data in generate_response(txt_input):
            response = data["out"]
            error = data["error"]
            code = data["code"]
            success = data["success"]
            percentage = data["percentage"]

            empty_code.code(code, language='python')
            empty_response.markdown(response)
            empty_error.exception(error)

            bar.progress(percentage, text="Processing...")

            if success:
                st.balloons()
                break