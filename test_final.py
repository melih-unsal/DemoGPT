#Create a system that gets pdf and question from user then answer the question by using the pdf.
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *


def load_pdf(pdf_path):
    loader = UnstructuredPDFLoader(pdf_path, mode="elements", strategy="fast")
    docs = loader.load()
    return docs


def pdfReader(pdf_doc, question):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0
    )
    system_template = "You are an AI assistant designed to extract information from a PDF document and answer questions based on it."
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "Please find the answer to the following question from the PDF document: '{question}' in the given PDF document: '{pdf_doc}'."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(pdf_doc=pdf_doc, question=question)
    return result # returns string


st.title('My App')

pdf_path = None
uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    pdf_path = "temp.pdf"
    st.session_state['pdf_path'] = pdf_path

if 'pdf_path' in st.session_state:
    pdf_path = st.session_state['pdf_path']

if pdf_path:
    pdf_doc = load_pdf(pdf_path)
else:
    pdf_doc = None

question = st.text_input("Ask your question:")

if st.button("Submit"):
    if pdf_doc and question:
        answer = pdfReader(pdf_doc, question)
    else:
        answer = ""

    if answer != "":
        st.markdown(f"**Answer:** {answer}")
    else:
        st.markdown("Please upload a PDF file and ask a question to generate an answer.")