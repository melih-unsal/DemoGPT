# Retrieval QA using OpenAI functions

# OpenAI functions allows for structuring of response output. This is often useful in question answering when you want to not only get the final answer but also supporting evidence, citations, etc.

# In this notebook we show how to use an LLM chain which uses OpenAI functions as part of an overall retrieval pipeline.

from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains import create_qa_with_sources_chain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from typing import List
from pydantic import BaseModel, Field
from langchain.chains.openai_functions import create_qa_with_structure_chain
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage, HumanMessage

# Load documents
loader = TextLoader("../../state_of_the_union.txt", encoding="utf-8")
documents = loader.load()

# Split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Add metadata to each chunk
for i, text in enumerate(texts):
    text.metadata['source'] = f"{i}-pl"

# Create OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Create Chroma vector store from documents
docsearch = Chroma.from_documents(texts, embeddings)

# Create LLM model
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

# Create QA chain
qa_chain = create_qa_with_sources_chain(llm)

# Create document prompt template
doc_prompt = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)

# Create final QA chain with document context
final_qa_chain = StuffDocumentsChain(
    llm_chain=qa_chain, 
    document_variable_name='context',
    document_prompt=doc_prompt,
)

# Create retrieval QA chain
retrieval_qa = RetrievalQA(
    retriever=docsearch.as_retriever(),
    combine_documents_chain=final_qa_chain
)

# Query
query = "What did the president say about russia"

# Run retrieval QA
retrieval_qa.run(query)

# Using Pydantic
# If we want to, we can set the chain to return in Pydantic. Note that if downstream chains consume the output of this chain - including memory - they will generally expect it to be in string format, so you should only use this chain when it is the final chain.

# Create QA chain with Pydantic output
qa_chain_pydantic = create_qa_with_sources_chain(llm, output_parser="pydantic")

# Create final QA chain with document context and Pydantic output
final_qa_chain_pydantic = StuffDocumentsChain(
    llm_chain=qa_chain_pydantic, 
    document_variable_name='context',
    document_prompt=doc_prompt,
)

# Create retrieval QA chain with Pydantic output
retrieval_qa_pydantic = RetrievalQA(
    retriever=docsearch.as_retriever(),
    combine_documents_chain=final_qa_chain_pydantic
)

# Run retrieval QA with Pydantic output
retrieval_qa_pydantic.run(query)

# Using in ConversationalRetrievalChain
# We can also show what it's like to use this in the ConversationalRetrievalChain. Note that because this chain involves memory, we will NOT use the Pydantic return type.

# Create memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create prompt template for condensing question
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.\
Make sure to avoid using any unclear pronouns.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

# Create LLM chain for condensing question
condense_question_chain = LLMChain(
    llm=llm,
    prompt=CONDENSE_QUESTION_PROMPT,
)

# Create ConversationalRetrievalChain
qa = ConversationalRetrievalChain(
    question_generator=condense_question_chain, 
    retriever=docsearch.as_retriever(),
    memory=memory, 
    combine_docs_chain=final_qa_chain
)

# Query
query = "What did the president say about Ketanji Brown Jackson"

# Run ConversationalRetrievalChain
result = qa({"question": query})

result

# Query
query = "what did he say about her predecessor?"

# Run ConversationalRetrievalChain
result = qa({"question": query})

result

# Using your own output schema
# We can change the outputs of our chain by passing in our own schema. The values and descriptions of this schema will inform the function we pass to the OpenAI API, meaning it won't just affect how we parse outputs but will also change the OpenAI output itself. For example we can add a countries_referenced parameter to our schema and describe what we want this parameter to mean, and that'll cause the OpenAI output to include a description of a speaker in the response.

# Create custom response schema
class CustomResponseSchema(BaseModel):
    """An answer to the question being asked, with sources."""

    answer: str = Field(..., description="Answer to the question that was asked")
    countries_referenced: List[str] = Field(..., description="All of the countries mentioned in the sources")
    sources: List[str] = Field(
        ..., description="List of sources used to answer the question"
    )

# Create prompt messages for custom response schema
prompt_messages = [
    SystemMessage(
        content=(
            "You are a world class algorithm to answer "
            "questions in a specific format."
        )
    ),
    HumanMessage(content="Answer question using the following context"),
    HumanMessagePromptTemplate.from_template("{context}"),
    HumanMessagePromptTemplate.from_template("Question: {question}"),
    HumanMessage(content="Tips: Make sure to answer in the correct format. Return all of the countries mentioned in the sources in uppercase characters."),
]

# Create prompt template for chain
chain_prompt = ChatPromptTemplate(messages=prompt_messages)

# Create QA chain with custom response schema
qa_chain_pydantic = create_qa_with_structure_chain(llm, CustomResponseSchema, output_parser="pydantic", prompt=chain_prompt)

# Create final QA chain with document context and custom response schema
final_qa_chain_pydantic = StuffDocumentsChain(
    llm_chain=qa_chain_pydantic,
    document_variable_name='context',
    document_prompt=doc_prompt,
)

# Create retrieval QA chain with custom response schema
retrieval_qa_pydantic = RetrievalQA(
    retriever=docsearch.as_retriever(),
    combine_documents_chain=final_qa_chain_pydantic
)

# Query
query = "What did he say about russia"

# Run retrieval QA with custom response schema
retrieval_qa_pydantic.run(query)