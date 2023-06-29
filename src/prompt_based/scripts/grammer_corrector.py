import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def correct_grammar(text):
    chat = ChatOpenAI(temperature=0)

    template = "You are a helpful assistant that corrects grammar. Please provide the text you want to correct."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(text=text)
    return result

st.title("My Grammerly")

text = st.text_input("Enter the text you want to correct")
if st.button("Correct Grammar"):
    result = correct_grammar(text)
    st.write(result)
    st.balloons()