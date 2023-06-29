def wait():
    import streamlit as st
    import time

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    with st.spinner('Wait for it...'):
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()
   
def language_translator(openai_api_key,demo_title="My Lang App"):
    import streamlit as st
    from langchain import LLMChain
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    def language_translator(input_language, output_language, text):
        chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)

        template = "You are a helpful assistant that translates {input_language} to {output_language}. Please provide the text to translate."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(input_language=input_language, output_language=output_language, text=text)
        return result

    st.header(demo_title)
    
    input_language = st.text_input("Input Language")
    output_language = st.text_input("Output Language")
    text = st.text_area("Text")

    if st.button("Translate"):
        result = language_translator(input_language, output_language, text)
        st.write(result)
        st.balloons()

def blog_post_generator(openai_api_key,demo_title="My Blogger"):
    import streamlit as st
    from langchain import LLMChain
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    def generate_blog_post(title):
        print("Generating blog post")
        chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)

        template = "You are a helpful assistant that generates a blog post from the title: {title}. Please provide some content."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(title=title, text="")
        return result

    st.header(demo_title)

    title = st.text_input("Enter the title of your blog post")
    if st.button("Generate Blog Post"):
        print("Generate")
        result = generate_blog_post(title)
        st.write(result)
        st.balloons()

def grammer_corrector(openai_api_key,demo_title="My Grammerly"):
    import streamlit as st
    from langchain import LLMChain
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    def correct_grammar(text):
        chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)

        template = "You are a helpful assistant that corrects grammar. Please provide the text you want to correct."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(text=text)
        return result

    st.header(demo_title)

    text = st.text_input("Enter the text you want to correct")
    if st.button("Correct Grammar"):
        result = correct_grammar(text)
        st.write(result)
        st.balloons()

def lyrics_generator(openai_api_key,demo_title="Lyrics Maker"):
    import streamlit as st
    from langchain import LLMChain
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    def generate_song(title):
        chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)

        template = "You are a helpful assistant that generates a song from the title: {title}. Please provide some lyrics."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(title=title, text="")
        return result

    st.header(demo_title)

    title = st.text_input("Enter the song title:")
    if st.button("Generate Song"):
        result = generate_song(title)
        st.write(result)
        st.balloons()


examples = ["Language Translator 📝","Grammer Corrector 🛠","Blog post generator from title 📔","Lyrics generator from song title 🎤"] 

pages = [language_translator,grammer_corrector,blog_post_generator,lyrics_generator]

example2pages={
    example:page
    for example,page in zip(examples,pages)
}

__all__ = ['language_translator','grammer_corrector','blog_post_generator','lyrics_generator','example2pages','examples','wait']