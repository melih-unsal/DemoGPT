import logging
import os

import fire
import langchain
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import HumanMessage
from langchain.text_splitter import (CharacterTextSplitter, Language,
                                     RecursiveCharacterTextSplitter)
from langchain.vectorstores import Chroma
from tqdm import tqdm

load_dotenv()


class LangChainExpert:
    def __init__(
        self,
        model_name="gpt-3.5-turbo-16k",
        persist_directory="langchain_db_python",
        device="cuda",
        distance_metric="cos",
        fetch_k=20,
        maximal_marginal_relevance=True,
        k=20,
    ):
        self.root_dir = "/".join(langchain.__file__.split("/")[:-1])
        self.model_name = model_name
        self.persist_directory = persist_directory
        self.device = device
        self.distance_metric = distance_metric
        self.fetch_k = fetch_k
        self.maximal_marginal_relevance = maximal_marginal_relevance
        self.k = k
        self.embeddings = HuggingFaceEmbeddings(model_kwargs={"device": device})
        self.__initModels()

    def __constructDB(self, split_type="python"):
        if os.path.exists(self.persist_directory):
            logging.info("DB has been found and fetched")
            self.db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
            )
        else:
            logging.info("DB not found, creation started...")
            docs = []
            for dirpath, _, filenames in tqdm(os.walk(self.root_dir)):
                for file in filenames:
                    if file.endswith(".py") and "/.venv/" not in dirpath:
                        try:
                            loader = TextLoader(
                                os.path.join(dirpath, file), encoding="utf-8"
                            )
                            docs.extend(loader.load_and_split())
                        except Exception as e:
                            pass
            if split_type == "python":
                python_splitter = RecursiveCharacterTextSplitter.from_language(
                    language=Language.PYTHON, chunk_size=1000, chunk_overlap=0
                )
                texts = python_splitter.split_documents(docs)
            else:
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                texts = text_splitter.split_documents(docs)
            self.db = Chroma.from_documents(
                texts, self.embeddings, persist_directory=self.persist_directory
            )

    def __constructRetriever(self):
        self.__constructDB()
        self.retriever = self.db.as_retriever()
        self.retriever.search_kwargs["distance_metric"] = self.distance_metric
        self.retriever.search_kwargs["fetch_k"] = self.fetch_k
        self.retriever.search_kwargs[
            "maximal_marginal_relevance"
        ] = self.maximal_marginal_relevance
        self.retriever.search_kwargs["k"] = self.k
        logging.info("Retriever has been succesfully constructed")

    def __initModels(self):
        self.__constructRetriever()
        self.model = ChatOpenAI(model_name=self.model_name, temperature=0)
        self.qa = ConversationalRetrievalChain.from_llm(
            self.model, retriever=self.retriever
        )
        self.qa_chat_history = []
        self.chat_history = []

    def askToModel(self, question, chat_history=False):
        messages = [HumanMessage(content=question)]
        if chat_history:
            messages = self.chat_history + messages
        return self.model(messages).content

    def ask(self, question, add_history=False):
        result = self.qa({"question": question, "chat_history": self.qa_chat_history})
        if add_history:
            self.chat_history.append((question, result["answer"]))
        return result["answer"]

    def debug(self, error):
        question = f"""
            How to solve that error below?

            {error}
            """
        return self.ask(question)


if __name__ == "__main__":
    expert = LangChainExpert()
    fire.Fire(expert.ask)
