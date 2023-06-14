from utils import generateTxtFromFolder
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool
from langchain.utilities import PythonREPL
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

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
        prompt1 = PromptTemplate(
            input_variables=["document","topic"],
            template="Write a python code using langchain library whose details are like {document} to generate {topic} "
        )
        self.start_chain = LLMChain(llm=self.llm, prompt=prompt1)
        prompt2 = PromptTemplate(
            input_variables=["document","topic","prev_code","response"],
            template="""
            You wrote a python code {prev_code} using langchain library to do the task: {topic}.
            You got the error {response} 
            
            Please refine the code using the following document
            document:{document}  
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=prompt2)
        self.python_repl = PythonREPL()

        embeddings = OpenAIEmbeddings()

        splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.HTML, chunk_size=4000, chunk_overlap=0
        )
        texts = splitter.create_documents([open(f"../documents/txt/langchain{i}.html").read() for i in range(1,7) if i != 4])

        print("Texts have been created!")
        print("Number of texts:", len(texts))

        self.docsearch = Chroma.from_documents(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))]).as_retriever()
    
    def getIndex(self,txt_path):
        loader = TextLoader(txt_path)
        return VectorstoreIndexCreator().from_loaders([loader])
    
    def getRelatedText(self,query, max_count=2):
        resulting_text = ""
        docs = self.docsearch.get_relevant_documents(query)
        for i,doc in enumerate(docs):
            if i >= max_count:
                break
            resulting_text += doc.page_content
        return resulting_text
    
    def __call__(self,topic,iterations=10):
        code = ""
        response = topic
        for _ in trange(iterations):
            document = self.getRelatedText(response + "\n" + topic)
            messages = [
            SystemMessage(content="""
            You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. You use langchain library. Don't explain the code, just generate the code block itself.
            Keep in mind that 
            OPENAI API KEY is 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
            So, you can use this kind of code below:
            openai.api_key = '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'

            or 

            llm = OpenAI(
                openai_api_key='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'
            )

            """)
            ]
            if not code:
                messages.append(
                    HumanMessage(content=f"Write a python code using langchain library whose details are like {document} to generate {topic}.")
                )
            else:
                messages.append(
                    HumanMessage(content=f"""
                    You wrote a python code {code} using langchain library to do the task: {topic}.
                    You got the error {response} 
            
                    Please refine the code using the following document
                    document:{document}  
                    If you want to use API Key, please use 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
                    """)
                )
            code = self.llm(messages).content

            if "```" in code: 
                code = code.split("```")[1]
                if code.startswith("python"):
                    code = code[len("python"):].strip()
                response = self.python_repl.run(code)
            print("response:",response)
            yield code, response

        
