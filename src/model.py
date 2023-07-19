import logging
import os

import fire
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from tqdm import tqdm

import utils
from chains.chains import Chains
from langchain_expert import LangChainExpert


class LangChainCoder:
    def __init__(
        self,
        model_name="gpt-3.5-turbo-16k",
        persist_directory="langchain_code",
        device="cuda",
        distance_metric="cos",
        maximal_marginal_relevance=True,
        k=4,
    ):
        self.root_dir = "/".join(langchain.__file__.split("/")[:-1])
        self.model_name = model_name
        self.persist_directory = persist_directory
        self.device = device
        self.distance_metric = distance_metric
        self.maximal_marginal_relevance = maximal_marginal_relevance
        self.k = k
        self.embeddings = HuggingFaceEmbeddings(model_kwargs={"device": device})
        self.__initModels()

    def __constructDB(self):
        if os.path.exists(self.persist_directory):
            logging.info("DB has been found and fetched")
            self.db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
            )
        else:
            logging.info("DB not found, creation started...")
            docs = []
            for dirpath, _, filenames in tqdm(os.walk("examples/goals/")):
                for file in filenames:
                    if file.endswith(".md"):
                        filepath = os.path.join(dirpath, file)
                        source_path = filepath.replace("goals", "codes/").replace(
                            ".md", ".py"
                        )
                        with open(source_path) as sf:
                            metadata = {"source": sf.read()}
                        with open(filepath) as f:
                            docs.append(
                                Document(page_content=f.read(), metadata=metadata)
                            )
            self.db = Chroma.from_documents(
                docs, self.embeddings, persist_directory=self.persist_directory
            )

    def __constructRetriever(self):
        self.__constructDB()
        self.retriever = self.db.as_retriever()
        self.retriever.search_kwargs["distance_metric"] = self.distance_metric
        self.retriever.search_kwargs[
            "maximal_marginal_relevance"
        ] = self.maximal_marginal_relevance
        self.retriever.search_kwargs["k"] = self.k
        logging.info("Retriever has been succesfully constructed")

    def __initModels(self):
        self.__constructRetriever()
        self.model = ChatOpenAI(model_name=self.model_name, temperature=0)
        self.expert = LangChainExpert()

    def __getSource(self, query):
        resulting_text = ""
        docs = self.retriever.get_relevant_documents(query)
        for doc in docs:
            resulting_text += doc.metadata["source"]
            resulting_text += "\n" + "#" * 40
        return resulting_text

    def __getTasks(self, task):
        instruction_list = Chains.divide(task=task)
        if instruction_list.startswith("["):
            instruction_list = instruction_list[1:]
        if instruction_list.endswith("]"):
            instruction_list = instruction_list[:-1]
        return [insruction.strip() for insruction in instruction_list.split(",")]

    def __mergeTasks(self, task, examples):
        merged_code = Chains.merge(task=task, examples=examples)
        merged_code = utils.refineCode(merged_code)
        return merged_code

    def __getSubResult(self, query, iterations):
        doc = self.__getSource(query)
        draft_code = Chains.draft(document=doc, idea=query)
        for _ in range(iterations):
            _, error, success = utils.runPython(draft_code)
            if not success:
                feedback = self.expert.debug(error)
                draft_code = Chains.debug(
                    draft_code=draft_code, idea=query, feedback=feedback, document=doc
                )
            else:
                return utils.refineCode(draft_code)
        return None

    def __getLangChainCode(self, instruction, iterations):
        tasks = self.__getTasks(instruction)
        print(tasks)
        examples = ""
        for i, task in enumerate(tasks):
            code = self.__getSubResult(task, iterations=iterations)
            if code:
                examples += f"""
                Subtask {i+1} : {task}
                Code {i+1} : {code}
                {'#'*40}

                """
        if len(tasks) == 1:
            return code
        final_code = self.__mergeTasks(instruction, examples)
        return final_code

    def __getStreamlitCode(self, instruction, langchain_code, title):
        merged_code = Chains.streamlit(
            instruction=instruction, langchain_code=langchain_code, title=title
        )
        merged_code = utils.refineCode(merged_code)
        return merged_code

    def code(
        self,
        instruction="Create a translation system that converts English to French",
        title="my translator",
        iterations=10,
    ):
        langchain_code = self.__getLangChainCode(instruction, iterations=iterations)
        return self.__getStreamlitCode(instruction, langchain_code, title)


if __name__ == "__main__":
    coder = LangChainCoder()
    fire.Fire(coder.code)
