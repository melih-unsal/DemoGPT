import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def language_translator(input_language, output_language, text):
    chat = ChatOpenAI(temperature=0)

    template = "You are a helpful assistant that translates {input_language} to {output_language}. Please provide the text to translate."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(input_language=input_language, output_language=output_language, text=text)
    return result

st.title("My Lang App")

input_language = st.text_input("Input Language")
output_language = st.text_input("Output Language")
text = st.text_area("Text")

if st.button("Translate"):
    result = language_translator(input_language, output_language, text)
    st.write(result)
    st.balloons()