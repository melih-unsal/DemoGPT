def wait():
    import streamlit as st
    import time

    progress_texts = ["Generating Code...:pencil:","Creating App...:running:","Rendering the demo page...:tv:"]
    num_of_texts = len(progress_texts)
    progress_texts_iter =  iter(progress_texts)
    my_bar = st.progress(0, "Initializing...")
    with st.spinner('Processing...'):
        start = end = 0
        for i in range(num_of_texts):
            text = next(progress_texts_iter)
            start = end
            end = start + 100 // num_of_texts
            for percent_complete in range(start, end):
                time.sleep(0.03*(num_of_texts-i))
                my_bar.progress(percent_complete + 1, text=text)
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
        with st.spinner("Generating the blog post..."):
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
        with st.spinner("Generating song..."):
            result = generate_song(title)
            st.write(result)
            st.balloons()

def twit_generator(openai_api_key,demo_title="My AutoTwitter"):
    import streamlit as st
    from langchain import LLMChain
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    def twitter(hashtag):
        chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.1)

        template = "You are a helpful assistant that generate twit from {hashtag}. Please provide the hashtag to generate a twit."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "Only generate the corresponding twit for this hashtag {hashtag}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(hashtag=hashtag)
        return result

    st.header(demo_title)
    
    hashtag = st.text_input("Hashtag",placeholder="#")

    if st.button("Generate"):
        result = twitter(hashtag)
        st.write(result)
        st.balloons()

def email_generator(openai_api_key,demo_title="My AutoTwitter"):
    import streamlit as st
    from langchain import LLMChain
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts.chat import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )

    def email(sender_name,receiver_name,purpose,keywords,tone):
        chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.1)

        template = "You are a helpful assistant that generate email to a person according to the given purpose, keywords and tone."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = """Generate email for a person according to the given purpose, keywords and tone.
        Sender Name:{sender_name}
        Receiver Name:{receiver_name}
        Purpose:{purpose}
        Keywords:{keywords}
        Tone:{tone}
        Directly start to type an email
        """
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain = LLMChain(llm=chat, prompt=chat_prompt)
        result = chain.run(sender_name=sender_name, receiver_name=receiver_name, purpose=purpose, keywords=keywords, tone=tone)
        return result

    st.header(demo_title)
    
    sender_name = st.text_input("Name of the sender")
    receiver_name = st.text_input("Receiver of the sender")
    purpose = st.text_input("Purpose of email")
    keywords = st.text_input("Primary keywords",placeholder="comma separated list of keywords")
    tone = st.text_input("Tone of the email")

    if st.button("Generate"):
        with st.spinner("Generating email..."):
            result = email(sender_name,receiver_name,purpose,keywords,tone)
            st.write(result)
            st.balloons()

examples1 = [
    "Language Translator 📝",
    "Grammer Corrector 🛠",
    "Blog post generator from title 📔"
    ]

examples2=[
    "Lyrics generator from song title 🎤",
    "Twit generation from hashtag 🐦",
    'Email generator :email:'
    ] 

examples = examples1 + examples2

pages1 = [language_translator,grammer_corrector,blog_post_generator]
pages2=[lyrics_generator,twit_generator,email_generator]

pages = pages1 + pages2

example2pages={
    example:page
    for example,page in zip(examples,pages)
}


__all__ = ['language_translator','grammer_corrector','blog_post_generator','lyrics_generator','twit_generator',
           'example2pages', 'examples', 'examples1', 'examples2', 'wait']