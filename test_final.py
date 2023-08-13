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

st.title("My PDF QA")

# Initialize state variables
pdf_path = st.session_state.get('pdf_path', None)
pdf_doc = None
pdf_string = ""
question = ""
answer = ""

# Load the PDF file as a Document
def load_pdf(pdf_path):
    from langchain.document_loaders import UnstructuredPDFLoader
    loader = UnstructuredPDFLoader(pdf_path, mode="elements", strategy="fast")
    docs = loader.load()
    return docs

# Convert the Document to a string
def convert_to_string(pdf_doc):
    return "".join([doc.page_content for doc in pdf_doc])

# Generate an answer to the question based on the content of the PDF
def pdfReader(pdf_string, question):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0
    )
    system_template = """You are an AI assistant that can extract information from a PDF document and answer questions based on its content. The PDF document contains the following text: '{pdf_string}'."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Based on the content of the PDF, please provide an answer to the following question: '{question}'. The PDF document contains the following text: '{pdf_string}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(pdf_string=pdf_string, question=question)
    return result # returns string   

# Get the PDF file from the user
uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        pdf_path = temp_file.name
        st.session_state['pdf_path'] = pdf_path

# Load the PDF file as a Document
if pdf_path:
    pdf_doc = load_pdf(pdf_path)

# Convert the Document to a string
if pdf_doc:
    pdf_string = convert_to_string(pdf_doc)

# Get the question from the user
question = st.text_input("Enter your question")

# Call the function if all user inputs are taken and the button is pressed
if st.button("Submit") and pdf_string and question:
    answer = pdfReader(pdf_string, question)

# Display the answer to the user
st.markdown(f"The answer to your question is: {answer}")