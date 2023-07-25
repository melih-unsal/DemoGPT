import logging
import os

import fire
import langchain
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from termcolor import colored
from tqdm import tqdm

import utils
from chains.chains import Chains
from langchain_expert import LangChainExpert


class LangChainCoder:
    def __init__(
        self,
        openai_api_key="sk-",
        model_name="gpt-3.5-turbo-16k",
        data_root = "src/data_beta/",
        persist_directory="langchain_code",
        device="cuda",
        distance_metric="cos",
        maximal_marginal_relevance=True,
        k=2,
    ):
        self.root_dir = "/".join(langchain.__file__.split("/")[:-1])
        Chains.setLlm(model_name, openai_api_key)
        self.persist_directory = os.path.join(data_root,persist_directory)
        self.goals_directory = os.path.join(data_root,"examples/goals/")
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
            for dirpath, _, filenames in tqdm(os.walk(self.goals_directory)):
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

    def __getSubResult(self, query, doc, index, iterations):
        draft_code = Chains.draft(document=doc, idea=query)
        for res in self.__solveBugs(draft_code, query, doc, index + 1, iterations):
            yield res
            success = res["success"]
            if success:
                break
        yield res

    def __solveBugs(self, draft_code, query, doc, index, iterations):
        for i in range(iterations):
            _, error, success = utils.runPython(draft_code)
            if not success:
                feedback = self.expert.debug(error)
                print(colored(feedback, "red"))
                draft_code = Chains.debug(
                    draft_code=draft_code, idea=query, feedback=feedback, document=doc
                )
                draft_code = utils.refineCode(draft_code)
                yield {
                    "task_id": index,
                    "progress": f"{i+1}/{iterations}",
                    "success": False,
                    "code": draft_code,
                    "stage": "langchain",
                }
            else:
                draft_code = utils.refineCode(draft_code)
                yield {
                    "task_id": index,
                    "progress": f"{i+1}/{iterations}",
                    "success": True,
                    "code": draft_code,
                    "stage": "langchain",
                }

                break
        else:
            yield {
                "task_id": index + 1,
                "progress": f"{iterations}/{iterations}",
                "success": False,
                "code": draft_code,
                "stage": "langchain",
            }

    def __getLangChainCode(self, instruction, iterations):
        tasks = self.__getTasks(instruction)
        print(colored(tasks,"yellow"))
        print(colored("Tasks have been generated", "green"))
        examples = ""
        for i, task in enumerate(tasks):
            doc = self.__getSource(task)
            for res in self.__getSubResult(task, doc, i, iterations=iterations):
                text = f"Task[{res['task_id']}/{len(tasks)}]\nProgress: {res['progress']}\nSuccess: {res['success']}\n"
                print(task)
                print(colored(res["code"],"blue"))
                if res["success"]:
                    print(colored(text, "green"))
                else:
                    print(colored(text, "yellow"))
                if res["success"]:
                    code = res["code"]
                    examples += f"""
                    Subtask {i+1} : {task}
                    Code {i+1} : {code}
                    {'#'*40}

                    """
                    break
                yield res

        if len(tasks) == 1:
            yield res
        else:
            final_code = self.__mergeTasks(instruction, examples)
            doc = self.__getSource(instruction)
            for res in self.__solveBugs(
                final_code, instruction, doc, "merge", iterations
            ):
                success = res["success"]
                text = f"Task[{res['task_id']}/{len(tasks)}]\nProgress: {res['progress']}\nSuccess: {res['success']}\n"
                if success:
                    print(colored(text, "green"))
                else:
                    print(colored(text, "yellow"))
                if success:
                    final_code = res["code"]
                    break
                yield res
            print(colored("Tasks have been merged", "green"))

    def __getStreamlitCode(self, instruction, langchain_code, title):
        merged_code = Chains.streamlit(
            instruction=instruction, langchain_code=langchain_code, title=title
        )
        merged_code = utils.refineCode(merged_code)
        return {
            "code": merged_code,
            "stage": "streamlit",
            "success": True,
            "task_id": "draft",
        }

    def __getFinalCode(self, instruction, code):
        feedback = Chains.feedback(code=code)
        code = Chains.refine(instruction=instruction, code=code, feedback=feedback)
        return utils.refineCode(code)

    def __getFinalCode1(self, instruction, code):
        code = Chains.refine1(code=code)
        return utils.refineCode(code)

    def __call__(
        self,
        instruction="Create a translation system that converts English to French",
        title="my translator",
        iterations=10,
    ):
        for res in self.__getLangChainCode(instruction, iterations=iterations):
            yield res
        langchain_code = res["code"]
        res = self.__getStreamlitCode(instruction, langchain_code, title)
        yield res
        streamlit_code = res["code"]
        print(colored(streamlit_code, "light_green"))
        final_code = self.__getFinalCode1(instruction, streamlit_code)

        yield {
            "code": final_code,
            "success": True,
            "task_id": "final",
            "stage": "streamlit",
        }


if __name__ == "__main__":
    coder = LangChainCoder()
    fire.Fire(coder.code)
