# Dynamically selecting from multiple retrievers

# Importing necessary libraries
from langchain.chains.router import MultiRetrievalQAChain
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS

# Loading and splitting documents for the State of the Union retriever
sou_docs = TextLoader("../../state_of_the_union.txt").load_and_split()
sou_retriever = FAISS.from_documents(sou_docs, OpenAIEmbeddings()).as_retriever()

# Loading and splitting documents for the Paul Graham essay retriever
pg_docs = TextLoader("../../paul_graham_essay.txt").load_and_split()
pg_retriever = FAISS.from_documents(pg_docs, OpenAIEmbeddings()).as_retriever()

# Creating a list of personal texts
personal_texts = [
    "I love apple pie",
    "My favorite color is fuchsia",
    "My dream is to become a professional dancer",
    "I broke my arm when I was 12",
    "My parents are from Peru",
]

# Creating a retriever for personal texts
personal_retriever = FAISS.from_texts(personal_texts, OpenAIEmbeddings()).as_retriever()

# Creating a list of retriever information
retriever_infos = [
    {
        "name": "state of the union",
        "description": "Good for answering questions about the 2023 State of the Union address",
        "retriever": sou_retriever,
    },
    {
        "name": "pg essay",
        "description": "Good for answering questions about Paul Graham's essay on his career",
        "retriever": pg_retriever,
    },
    {
        "name": "personal",
        "description": "Good for answering questions about me",
        "retriever": personal_retriever,
    },
]

# Creating a MultiRetrievalQAChain from the retrievers
chain = MultiRetrievalQAChain.from_retrievers(OpenAI(), retriever_infos, verbose=True)

# Running the chain with a specific question
print(chain.run("What did the president say about the economy?"))

# Running the chain with another question
print(chain.run("What is something Paul Graham regrets about his work?"))

# Running the chain with another question
print(chain.run("What is my background?"))

# Running the chain with another question
print(chain.run("What year was the Internet created in?"))
