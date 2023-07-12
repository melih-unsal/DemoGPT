from prompts import *
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from subprocess import PIPE, run
import tempfile
import os
from tqdm import tqdm
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

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
            self.docsearch = Chroma(persist_directory=persist_directory, embedding_function=embeddings).as_retriever(search_type="mmr")
        else:
            DOC_ROOT = "../documents/langchain_summary/"
            docs = []
            for filename in tqdm(os.listdir(DOC_ROOT)):
                filepath = os.path.join(DOC_ROOT, filename)

                source_path = filepath.replace("langchain_summary","langchain")
                with open(source_path) as sf:
                    metadata = {"source":sf.read()}
                with open(filepath) as f:
                    docs.append(Document(page_content=f.read(), metadata=metadata))
            print("Docs have been created!")
            print("Number of docs:", len(docs))

            text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
            texts = text_splitter.split_documents(docs)

            print("Number of texts:", len(texts))

            #self.docsearch = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory).as_retriever(search_type="mmr")
            self.docsearch = Chroma.from_documents(texts, embeddings).as_retriever(search_type="mmr")

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
        docs = self.docsearch.get_relevant_documents(query)
        for i,doc in enumerate(docs):
            if i >= max_count:
                break
            resulting_text += doc.metadata["source"]
        return resulting_text
    
    def __call__(self,topic,iterations=10):

        code = ""
        error = ""
        feedback=""
        out = ""
        plan=""
        percentage = 0
        for _ in trange(iterations):
            if feedback:
                document = self.getRelatedText(feedback + "\n" + topic)
            else:
                document = self.getRelatedText(topic)
            print ("document:",document)
            
            if code:
                code = self.with_code_chain.run(document=document,topic=topic,code=code,error=error,feedback=feedback)
                """code = self.refine_chain.run(content=code,
                                             critics=error,
                                             document=document,
                                             instruction_hint="Fix the code snippet based on the error provided. Only provide the fixed code snippet between `` and nothing else.")"""
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
        

        
class Summarizer:
    def __init__(self) -> None:
        llm = ChatOpenAI(temperature=0)
        self.chain = load_summarize_chain(llm, chain_type="map_reduce")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 4000,
            chunk_overlap  = 200,
            length_function = len
            )
    def __call__(self,path):
        out_path = path.replace("docs/","docs_summary/")
        if os.path.exists(out_path):
            return 
        with open(path) as f:
            state_of_the_union = f.read()
        texts = self.text_splitter.split_text(state_of_the_union)
        docs = [Document(page_content=t) for t in texts]
        summary = self.chain.run(docs)
        with open(out_path,"w") as f:
            f.write(summary)

class Explainer:
    def __init__(self) -> None:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k",temperature=0)
        template = "Create a concise tutorial to talk about the given document"
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{document}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        self.chain = LLMChain(llm=llm, prompt=chat_prompt)

    def __call__(self,path):
        out_path = path.replace("docs/","docs_explanation/")
        if os.path.exists(out_path):
            return 
        with open(path) as f:
            document = f.read()
        explanation = self.chain.run(document)
        with open(out_path,"w") as f:
            f.write(explanation)
if __name__ == "__main__":
    model = Summarizer()
    path = "../documents/langchain/Vectara Text Generation.txt"
    summary = model(path)
    with open(path.replace("langchain/","langchain_summary/"),"w") as f:
        f.write(summary)        