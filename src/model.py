from utils import generateTxtFromFolder
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool
from langchain.utilities import PythonREPL
import sys
from io import StringIO
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from subprocess import PIPE, run
import tempfile

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from tqdm import trange

from dotenv import load_dotenv
import os
load_dotenv()





class Model:
    def __init__(self):
        #self.documents_root = "../documents/pdf"
        #self.txt_folder = "../documents/txt"
        #generateTxtFromFolder(self.documents_root,self.txt_folder)
        #self.out_paths = [os.path.join(self.txt_folder,path) for path in os.listdir(self.txt_folder)]
        self.llm = ChatOpenAI(temperature=0.0)
        self.python_repl = PythonREPL()
        persist_directory = 'db'

        embeddings = HuggingFaceEmbeddings(model_kwargs = {'device': 'cuda'})

        splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN, chunk_size=4000, chunk_overlap=0
        )
        texts = splitter.create_documents([open(f"../documents/txt/tutorial{i}.txt").read() for i in range(1,3)])

        print("Texts have been created!")
        print("Number of texts:", len(texts))

        if os.path.exists(persist_directory):
            self.docsearch = Chroma(persist_directory=persist_directory, embedding_function=embeddings).as_retriever()
        else:
            self.docsearch = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory, metadatas=[{"source": str(i)} for i in range(len(texts))]).as_retriever()
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    def run_python(self,code):
        with tempfile.NamedTemporaryFile("w") as tmp:
            tmp.write(code)
            tmp.flush()
            result = run("python "+tmp.name, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            return result.stdout, result.stderr
    
    def getRelatedText(self,query, max_count=2):
        print("query:",query)
        resulting_text = ""
        docs = self.docsearch.get_relevant_documents(query)
        for i,doc in enumerate(docs):
            if i >= max_count:
                break
            resulting_text += doc.page_content
        return resulting_text
    
    def getFixMessages(self,code,error):
        return  [
            HumanMessage(content=f"""
            ##### Find the bugs in the below Python code
            
            ### Buggy Python
            {code}

            ### Error
            {error}

            ### Error Reason
            """)
        ]
    
    def getMessages(self,topic, code, error, document, feedback):
        messages = [
            SystemMessage(content=f"""
            You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. You use langchain library. Don't explain the code, just generate the code block itself.
            Keep in mind that 
            OPENAI API KEY is {self.OPENAI_API_KEY}
            So, you can use this kind of code below:
            openai.api_key = '{self.OPENAI_API_KEY}'

            or 

            llm = ChatOpenAI(
                openai_api_key='{self.OPENAI_API_KEY}'
            )

            """)
        ]
        if code:
            messages.append(
                HumanMessage(content=f"""
                             You wrote a python code {code} using langchain library to do the task: {topic}.
                             You got the error {error} 
                             
                             Please refine the code using the following document and feedback
                             
                             document:{document}  

                             feedback:{feedback}
                             
                             If you want to use API Key, please use {self.OPENAI_API_KEY}
                         """)
            )
        else:
            messages.append(
                    HumanMessage(content=f"Write a python code using langchain library whose details are like {document} to generate {topic} function and test it.")
                )

        return messages
    
    def __call__(self,topic,iterations=10):

        code = ""
        error = topic
        feedback=""
        out = ""
        percentage = 0
        for _ in trange(iterations):
            document = self.getRelatedText(error + "\n" + topic)
            
            messages = self.getMessages(topic, code, error, document, feedback)
            code = self.llm(messages).content
            if "```" in code: 
                code = code.split("```")[1]
                if code.startswith("python"):
                    code = code[len("python"):].strip()
            print(code)
            out, error = self.run_python(code)
            if not error:
                break
            fix_messages = self.getFixMessages(code,error)
            feedback = self.llm(fix_messages).content
            percentage += 100//iterations
            print("error:",error)
            yield {
                "code":code,
                "success":False,
                "out":error,
                "feedback":feedback,
                "percentage":min(100,percentage)
            }
        if not error:
            yield {
                "code":code,
                "success":True,
                "out":out,
                "feedback":"",
                "percentage":100
            }
        else:
            yield {
                "code":code,
                "success":False,
                "out":error,
                "feedback":feedback,
                "percentage":100
            }
        

        
