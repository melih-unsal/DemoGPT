from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import os
from tqdm import tqdm
import logging
import fire
from dotenv import load_dotenv
load_dotenv()

from termcolor import colored

class LangChainExpert:
    def __init__(self,
                 model_name="gpt-3.5-turbo-16k", 
                 persist_directory = "langchain_db_python",
                 root_dir = "../../langchain",
                 device="cuda",
                 distance_metric="cos",
                 fetch_k=20,
                 maximal_marginal_relevance=True,
                 k=20):
         self.model_name = model_name
         self.persist_directory = persist_directory
         self.root_dir = root_dir
         self.device = device
         self.distance_metric = distance_metric
         self.fetch_k = fetch_k
         self.maximal_marginal_relevance = maximal_marginal_relevance
         self.k = k
         self.embeddings = HuggingFaceEmbeddings(model_kwargs = {'device': device})
         self.__initModels()

    def __constructDB(self,split_type="python"):             
        if os.path.exists(self.persist_directory):
            logging.info('DB has been found and fetched')
            self.db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)        
        else:
            logging.info('DB not found, creation started...')
            docs = []
            for dirpath, dirnames, filenames in tqdm(os.walk(self.root_dir)):
                for file in filenames:
                    if file.endswith(".py") and "/.venv/" not in dirpath:
                        try:
                            loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
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
            self.db = Chroma.from_documents(texts, self.embeddings,persist_directory=self.persist_directory)
    
    def __constructRetriever(self):
        self.__constructDB()
        self.retriever = self.db.as_retriever()
        self.retriever.search_kwargs["distance_metric"] = self.distance_metric
        self.retriever.search_kwargs["fetch_k"] = self.fetch_k
        self.retriever.search_kwargs["maximal_marginal_relevance"] = self.maximal_marginal_relevance
        self.retriever.search_kwargs["k"] = self.k
        logging.info('Retriever has been succesfully constructed')

    def __initModels(self):
        self.__constructRetriever()
        self.model = ChatOpenAI(model_name=self.model_name,temperature=0)
        self.qa = ConversationalRetrievalChain.from_llm(self.model, retriever=self.retriever)
        self.qa_chat_history = []
        self.chat_history = []

    def askToModel(self, question, chat_history=False):
        messages = [HumanMessage(content=question)]
        if chat_history:
            messages = self.chat_history + messages
        return self.model(messages).content
    
    def refineCode(self,code):
        question = f"""
        Refine the below code to run properly and bug free:

        {code}
        """
        refined_code = self.askToModel(question)
        print(refined_code)
        if "```" in refined_code: 
            refined_code = refined_code.split("```")[1]
            if refined_code.startswith("python"):
                refined_code = refined_code[len("python"):].strip()

        return refined_code

    def generateQuestions(self,instruction="",answer=""):
        system_message = SystemMessage(
        content = """
        langchain is a python library to create LLM-based applications.
        You will create a python application to accomplish an instruction based on langchain library.
        You are good at Python but you are bad at langchain and the details of langchain.
        To build the app, ask questions related to langchain and how to use it.
        You have zero knowledge on langchain
        Generate a single question to do the instruction given to you
        Don't generate question about installation, langchain has been already installed.
        Generate a single question.
        Only generate questions to gather implementation related information, don't ask redundant questions.
        """)
        if answer:
            human_message = HumanMessage(content=f"""
                ### instruction:{instruction}

                ### Previous knowledge:{answer}

                ### New questions:
                """)
        else:    
            human_message = HumanMessage(content = f"""
            ### instruction:{instruction}

            ### questions:
            """)
        messages = [system_message] + self.chat_history + [human_message]
        questions = self.model(messages).content

        self.chat_history += [human_message] + [AIMessage(content=str(questions))]

        return questions

    
    def ask(self,question, add_history=False):
        result = self.qa({"question": question, "chat_history": self.qa_chat_history})
        if add_history:
            self.chat_history.append((question, result["answer"]))
        return result['answer']
    
    def solveError(self,code, error, add_history=False):
        question = f"""
        I wrote a langchain code and got an error. How can I solve the error?
        Code : {code}
        ########################################################################
        Error : {error}
        """
        result = self.qa({"question": question, "chat_history": self.qa_chat_history})
        if add_history:
            self.chat_history.append((question, result["answer"]))
        return result['answer']
    
    def explainError(self,error, add_history=False):
        question = f"""
        I wrote a langchain code and got an error. How can I solve the error?
        Error : {error}
        """
        result = self.qa({"question": question, "chat_history": self.qa_chat_history})
        if add_history:
            self.chat_history.append((question, result["answer"]))
        return result['answer']
    
    def giveFeedback(self,code, goal, add_history=False):
        question = f"""
        I wrote a langchain code to accomplish a goal. Could you refine that code?
        ########################################################################
        LangChain Code : {code}
        ########################################################################
        Goal : {goal}
        """
        result = self.qa({"question": question, "chat_history": self.qa_chat_history})
        if add_history:
            self.chat_history.append((question, result["answer"]))
        return result['answer']
    
def code(instruction="Create a teacher that can do any calculation and solve any chemistry question"): 
    expert = LangChainExpert()
    answers = ""
    for i in range(3):
        if i == 0:
            questions = expert.generateQuestions(instruction=instruction)
        else:
            questions = expert.generateQuestions(instruction=instruction,answer=answers)
        print(colored(questions,"blue"))    
        answers = expert.ask(questions,add_history=False)
        print(colored(str(answers),"yellow"))  

    
    question = f"""
    langchain is a python library to create LLM-based applications.
    You will create a python application to accomplish an instruction based on langchain library.

    ### instruction:{instruction}

    ### langchain code:
    """

    code = expert.askToModel(question, chat_history=True)
    print(colored(code,"green"))


if __name__ == "__main__":
    fire.Fire(code)