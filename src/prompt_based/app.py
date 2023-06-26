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

    st.subheader("Total Code")
    empty_total_code = st.empty()

    st.subheader("Code")
    empty_code = st.empty()

    st.subheader("Refined Code")
    empty_refined_code = st.empty()

    st.subheader("Test Code")
    empty_test_code = st.empty()

    st.subheader("Response")
    empty_response = st.empty()

    st.subheader("Feedback")
    empty_feedback = st.empty()

    st.subheader("Error")
    empty_error = st.empty()

    if submitted:
        bar = st.progress(0, text="Processing...")
        for data in generate_response(txt_input):
            response = data["out"]
            error = data["error"]
            code = data["code"]
            total_code = data["total_code"]
            test_code = data["test_code"]
            refined_code = data["refined_code"]
            success = data["success"]
            percentage = data["percentage"]
            feedback = data["feedback"]

            empty_code.code(code, language='python')
            empty_total_code.code(total_code, language='python')
            empty_test_code.code(test_code, language='python')
            empty_refined_code.code(refined_code, language='python')
            empty_response.markdown(response)
            if not success:
                empty_error.exception(error)
            else:
                empty_error.success(response)

            empty_feedback.markdown(feedback)

            if success:
                bar.progress(percentage, text="Successfully completed")
            else:
                bar.progress(percentage, text="Processing...")

            if success:
                st.balloons()
                break