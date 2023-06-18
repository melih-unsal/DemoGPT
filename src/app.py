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

progress_text = "Operation in progress. Please wait."
complete_text = {
    "success":"Operation completed",
    "fail":"Operation failed"
    }

st.subheader("Plan")
empty_plan = st.empty()

st.subheader("Code")
empty_code = st.empty()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Feedback")
    empty_feedback = st.empty()
    
with col2:
    st.subheader("Response")
    empty_response = st.empty()

# Form to accept user's text input for summarization
result = []

with st.form('a', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    if submitted:
        #with st.spinner('Calculating...'):
        bar = st.progress(0, text=progress_text)
        for data in generate_response(txt_input):
            response = data["out"]
            feedback = data["feedback"]
            code = data["code"]
            percentage = data["percentage"]
            success = data["success"]
            plan=data["plan"]
            empty_code.code(code, language='python')
            empty_feedback.markdown(feedback)
            empty_plan.markdown(plan)
            if success:
                empty_response.markdown(response)
            else:
                empty_response.exception(response)
            if percentage == 100:
                if success:
                    text = complete_text["success"]
                else:
                    text = complete_text["fail"]
            else:
                text = progress_text
            bar.progress(percentage, text=text)
            if percentage == 100:
                if success:
                    st.balloons()