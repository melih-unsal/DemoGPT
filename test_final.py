#Create a system that generates random programming related humors when 'laugh' button is clicked without any user input by AI
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile
from langchain.docstore.document import Document

def generate_humor():
    st.markdown("### Programming Humor")
    st.write("Why do programmers prefer dark mode?")
    st.write("Because light attracts bugs!")

def randomHumorGenerator():
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0.7
    )
    system_template = """You are a programming humor generator. Your task is to generate a random programming-related joke or humorous statement when the 'Laugh' button is clicked."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Click the 'Laugh' button to generate a random programming-related joke or humorous statement."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run({})
    return result # returns string   

st.title('My App')

laugh_button = st.button("Laugh")

if laugh_button:
    generate_humor()

if laugh_button:
    humor = randomHumorGenerator()
    st.markdown("### Generated Humor")
    st.write(humor)