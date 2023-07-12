# Retrieval QA

# Import necessary libraries
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

# Load the text documents
loader = TextLoader("../../state_of_the_union.txt")
documents = loader.load()

# Split the documents into smaller chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create a vector store for document search
docsearch = Chroma.from_documents(texts, embeddings)

# Create a RetrievalQA chain
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

# Define the query
query = "What did the president say about Ketanji Brown Jackson"

# Run the query
qa.run(query)

# Chain Type

# Change the chain type to map_reduce
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="map_reduce", retriever=docsearch.as_retriever())

# Run the query again
qa.run(query)

# Load the chain directly and pass it to RetrievalQA
from langchain.chains.question_answering import load_qa_chain
qa_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
qa = RetrievalQA(combine_documents_chain=qa_chain, retriever=docsearch.as_retriever())

# Run the query again
qa.run(query)

# Custom Prompts

# Create a custom prompt template
from langchain.prompts import PromptTemplate
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer in Italian:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Pass the custom prompt to RetrievalQA
chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(), chain_type_kwargs=chain_type_kwargs)

# Run the query again
qa.run(query)

# Return Source Documents

# Return the source documents used to answer the question
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(), return_source_documents=True)

# Run the query and get the result
result = qa({"query": query})

# Print the result and source documents
print(result["result"])
print(result["source_documents"])

# Use RetrievalQAWithSourceChain to cite sources
docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": f"{i}-pl"} for i in range(len(texts))])

from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI

chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), chain_type="stuff", retriever=docsearch.as_retriever())

chain({"question": "What did the president say about Justice Breyer"}, return_only_outputs=True)