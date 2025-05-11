from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import (
    TextLoader, 
    WebBaseLoader, 
    PyPDFLoader,
    DirectoryLoader,
    JSONLoader
    )
from langchain_community.document_loaders.csv_loader import CSVLoader
from typing import List, Union
import os
import shutil
import logging

from demogpt_agenthub.llms.base import BaseLLM
from demogpt_agenthub.prompts.rag.base import template

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseRAG:
    OPENAI_EMBEDDING_MODELS = [
        "text-embedding-3-small",
        "text-embedding-3-large",
        "text-embedding-ada-002"
    ]
    def __init__(self, llm: BaseLLM, 
                 vectorstore: str, 
                 persistent_path: str, 
                 index_name: str,
                 reset_vectorstore: bool = False,
                 embedding_model_name: str = "sentence-transformers/all-mpnet-base-v2",
                 filter: dict = None,
                 k: int = 4,
                 verbose: bool = False):
        self.name = "RAG"
        self.description = "A tool that can search for information in vector database by using a query."
        self.llm = llm
        self.persistent_path = persistent_path
        self.verbose = verbose
        self.index_name = index_name
        self.search_kwargs={
            'k': k,
            'filter': filter
        }
        self.load_embedding_model(embedding_model_name)
        self.load_vectorstore(vectorstore, reset_vectorstore)
        self.output_parser = StrOutputParser()
        
        prompt = ChatPromptTemplate.from_template(template)

        self.rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | self.output_parser
        )

    def load_embedding_model(self, model_name: str):
        if model_name in self.OPENAI_EMBEDDING_MODELS:
            from langchain_openai import OpenAIEmbeddings
            self.embedding_model = OpenAIEmbeddings(model=model_name)
        else:
            from langchain_huggingface import HuggingFaceEmbeddings
            self.embedding_model = HuggingFaceEmbeddings(model_name=model_name)

    def load_vectorstore(self, vectorstore, reset_vectorstore: bool = False):
        # First, close any existing connection
        if hasattr(self, 'vectorstore') and hasattr(self.vectorstore, '_client'):
            self.vectorstore._client.close()
        
        if reset_vectorstore:
            if os.path.exists(self.persistent_path):
                print(f"Removing existing vectorstore at {self.persistent_path}")
                shutil.rmtree(self.persistent_path)
        if vectorstore == "chroma":
            from langchain_chroma import Chroma
            self.vectorstore = Chroma(embedding_function=self.embedding_model, persist_directory=self.persistent_path)
        elif vectorstore == "pinecone":
            from langchain_pinecone import PineconeVectorStore
            self.vectorstore = PineconeVectorStore(index_name=self.index_name)
        elif vectorstore == "faiss":
            from langchain_community.vectorstores import FAISS
            self.vectorstore = FAISS(self.persistent_path, self.embedding_model)
        else:
            raise ValueError(f"Vectorstore {vectorstore} not supported")
        
        self.retriever = self.vectorstore.as_retriever()
        
    def _add_documents(self, documents: List[Document]):
        self.vectorstore.add_documents(documents)

    def add_texts(self, texts: Union[str, List[str]]):
        if isinstance(texts, str):
            texts = [texts]
        self.vectorstore.add_texts(texts)
    
    def add_files(self, file_paths  : Union[str, List[str]]):
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        docs = []
        for file_path in file_paths:  
            if file_path.endswith(".txt"):
                loader = TextLoader(file_path)
            elif file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file_path.endswith(".json"):
                loader = JSONLoader(file_path)
            elif file_path.endswith(".csv"):
                loader = CSVLoader(file_path)
            elif file_path.startswith("http"):
                loader = WebBaseLoader(file_path)
            else:
                logger.info(f"File {file_path} not supported")
                continue
            try:    
                docs.extend(loader.load())
            except Exception as e:
                logger.error(f"Error loading file {file_path}: {e}")
        self._add_documents(docs)

    def run(self, query: str):
        return self.rag_chain.invoke(query)

if __name__ == "__main__":
    from demogpt_agenthub.llms.openai import OpenAIChatModel
    rag = BaseRAG(llm=OpenAIChatModel(model="gpt-4o-mini"), 
                  vectorstore="chroma", 
                  persistent_path="rag_chroma", 
                  index_name="rag_index",
                  reset_vectorstore=True,
                  embedding_model_name="sentence-transformers/all-mpnet-base-v2",
                  filter={"search_kwargs": {"score_threshold": 0.5}}
                  )
    rag.add_files(["/home/melih/Downloads/results - 2024-11-04T160209.186.pdf"])
    print(rag.query("How many people joined the interview with Age 40 to 49?"))
