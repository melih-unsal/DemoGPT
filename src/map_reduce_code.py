from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
import fire
from tqdm import tqdm
import os
from dotenv import load_dotenv
import tiktoken
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from pprint import pprint

load_dotenv()

encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")


def get_code(query="English to Turkish translator"):

    embeddings = HuggingFaceEmbeddings(model_kwargs = {'device': 'cuda'})

    DOC_ROOT = "../documents/langchain_summary/"
    docs = []
    for filename in tqdm(os.listdir(DOC_ROOT)):
        filepath = os.path.join(DOC_ROOT, filename)
        source_path = filepath.replace("langchain_summary","langchain")
        with open(source_path) as sf:
            metadata = {"source":sf.read(),"path":source_path}
        with open(filepath) as f:
            docs.append(Document(page_content=f.read(), metadata=metadata))
    print("Docs have been created!")
    print("Number of docs:", len(docs))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=100)
    texts = text_splitter.split_documents(docs)

    print("Number of texts:", len(texts))

    docsearch = Chroma.from_documents(texts, embeddings)
    #retriever = docsearch.as_retriever(search_type="mmr")

    related_texts = []

    #res = retriever.get_relevant_documents(query)

    res = docsearch.similarity_search(query,k=4)
    related_docs = []
    for doc in res:
        source = doc.metadata["source"]
        path = doc.metadata["path"]
        related_docs.append(Document(page_content=source, metadata={"path":path}))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=100)
    related_texts = text_splitter.split_documents(related_docs)


    print("Number of related texts:", len(related_texts))

    related_docsearch = Chroma.from_documents(related_texts, embeddings)

    retriever = related_docsearch.as_retriever(search_type="similarity", search_kwargs={"k":4})

    res = retriever.get_relevant_documents(query)
    document = ""
    for i,doc in enumerate(res):
        document += doc.page_content + "\n"

    """qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0), chain_type="stuff", retriever=retriever, return_source_documents=True)

    result = qa({"query": query})
    for k,v in result.items():
        print(k,":",v)
        print("#"*100)"""

    prompt_template = """Use the following pieces of langchain related document to generate a python code to accomplish the goal.

    {documentation}

    Goal: {topic}
    Python Code:"""

    prompt = prompt_template.format(documentation=document, topic=query)
    print(prompt)
    messages = [HumanMessage(content=prompt)]

    llm = ChatOpenAI(temperature=0) 
    res = llm(messages)
    print(res.content)



if __name__ == "__main__":
    fire.Fire(get_code)