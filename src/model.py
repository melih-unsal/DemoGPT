from prompts import *
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
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
        self.llm = ChatOpenAI(temperature=0.0)
        persist_directory = 'db'

        embeddings = HuggingFaceEmbeddings(model_kwargs = {'device': 'cuda'})

        if os.path.exists(persist_directory):
            self.docsearch = Chroma(persist_directory=persist_directory, embedding_function=embeddings)#.as_retriever(search_kwargs={"k": 2})
        else:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=4000, chunk_overlap=0
                )
            texts = splitter.create_documents([open(f"../documents/tree/explanation.txt").read()])
            print("Texts have been created!")
            print("Number of texts:", len(texts))
            self.docsearch = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory, metadatas=[{"source": str(i)} for i in range(len(texts))])#.as_retriever(search_kwargs={"k": 2})
        

        self.with_code_chain = LLMChain(llm=self.llm, prompt=with_code_chat_prompt)
        self.without_code_chain = LLMChain(llm=self.llm, prompt=without_code_chat_prompt)
        self.fix_chain = LLMChain(llm=self.llm,prompt=fix_chat_prompt)
        self.refine_chain = LLMChain(llm=self.llm,prompt=refine_chat_prompt)
        self.plan_chain = LLMChain(llm=self.llm,prompt=plan_chat_prompt)

    def run_python(self,code):
        with tempfile.NamedTemporaryFile("w") as tmp:
            tmp.write(code)
            tmp.flush()
            command = f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY')} python "+tmp.name
            print(command)
            result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            return result.stdout, result.stderr
    
    def getRelatedText(self,query, max_count=2):
        print("query:",query)
        resulting_text = ""
        #docs = self.docsearch.get_relevant_documents(query)
        docs = self.docsearch.similarity_search(query)
        for i,doc in enumerate(docs):
            if i >= max_count:
                break
            resulting_text += doc.page_content
        return resulting_text
    
    def __call__(self,topic,iterations=10):

        code = ""
        error = topic
        feedback=""
        out = ""
        plan=""
        percentage = 0
        for _ in trange(iterations):
            document = self.getRelatedText(error + "\n" + topic)
            
            if code:
                #code = self.with_code_chain.run(document=document,topic=topic,code=code,error=error,feedback=feedback)
                code = self.refine_chain.run(content=code,
                                             critics=error,
                                             document=document,
                                             instruction_hint="Fix the code snippet based on the error provided. Only provide the fixed code snippet between `` and nothing else.")
            else:
                plan = self.plan_chain.run(document=document,topic=topic)
                code = self.without_code_chain.run(document=document,topic=topic,plan=plan)
            if "```" in code: 
                code = code.split("```")[1]
                if code.startswith("python"):
                    code = code[len("python"):].strip()
            print(code)
            out, error = self.run_python(code)
            if not error:
                break
            feedback = self.fix_chain.run(code=code,error=error)
            percentage += 100//iterations
            print("error:",error)
            yield {
                "code":code,
                "success":False,
                "out":error,
                "feedback":feedback,
                "percentage":min(100,percentage),
                "plan":plan,
                "document":document
            }
        if not error:
            yield {
                "code":code,
                "success":True,
                "out":out,
                "feedback":"",
                "percentage":100,
                "plan":plan,
                "document":document
            }
        else:
            yield {
                "code":code,
                "success":False,
                "out":error,
                "feedback":feedback,
                "percentage":100,
                "plan":plan,
                "document":document
            }
        

        
