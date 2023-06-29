import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def generate_song(title):
    chat = ChatOpenAI(temperature=0)

    template = "You are a helpful assistant that generates a song from the title: {title}. Please provide some lyrics."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(title=title, text="")
    return result

st.title("Lyrics Maker")

title = st.text_input("Enter the song title:")
if st.button("Generate Song"):
    result = generate_song(title)
    st.write(result)
    st.balloons()