#Create a system that can generate blog post related to a website then summarize it
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile

st.title('My App')

# Get website URL from the user
url = st.text_input("Enter website URL")

# Load the website as a Document from the given URL
def load_website(url):
    from langchain.document_loaders import WebBaseLoader
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs

# Convert the Document to string content
content = ""
if url:
    website = load_website(url)
    content = "".join([doc.page_content for doc in website])

# Generate a blog post related to the string content
def blogPostGenerator(content):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0.7
    )
    system_template = """You are an assistant designed to write a blog post related to the given content: '{content}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please compose a blog post based on the following content: '{content}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(content=content)
    return result # returns string   

blog_post = ""
if content:
    blog_post = blogPostGenerator(content)

# Display the generated blog post to the user
st.markdown(blog_post)

# Summarize the blog post
def summarize_blog_post(docs):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.run(docs)

summary = ""
if blog_post:
    summary = summarize_blog_post(blog_post)

# Display the summarized blog post to the user
st.markdown(summary)

# Add a button to start the process
if st.button("Generate Blog Post and Summary"):
    if url:
        website = load_website(url)
        content = "".join([doc.page_content for doc in website])
        if content:
            blog_post = blogPostGenerator(content)
            if blog_post:
                summary = summarize_blog_post(blog_post)
                st.markdown(blog_post)
                st.markdown(summary)