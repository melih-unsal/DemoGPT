import streamlit as st

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

st.title("My App")

def melodyGenerator(song_title):
    chat = ChatOpenAI(
        temperature=0.7
    )
    system_template = "You are an AI music composer. Your task is to generate a melody for the song '{song_title}'."
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "Please use AI to generate a melody for the song '{song_title}'."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(song_title=song_title)
    return result # returns string   

def lyricGenerator(song_title):
    chat = ChatOpenAI(
        temperature=0.7
    )
    system_template = "You are an AI songwriter. Your task is to generate lyrics for a song with the title: '{song_title}'."
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "Please generate lyrics for a song titled '{song_title}'."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(song_title=song_title)
    return result # returns string   

song_title = st.text_input("Enter song title")
button = st.button("Submit")

if button and song_title != "":
    melody = melodyGenerator(song_title)
    lyrics = lyricGenerator(song_title)

    def show_text(melody, lyrics):
        if melody != "" and lyrics != "":
            st.markdown("Melody: {}".format(melody))
            st.markdown("Lyrics: {}".format(lyrics))
        else:
            st.markdown("No melody and lyrics generated.")

    show_text(melody, lyrics)
else:
    st.markdown("Please enter a song title and click Submit.")