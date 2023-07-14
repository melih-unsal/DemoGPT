from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_expert import LangChainExpert
from agent_prompts import *
import sys
import fire
from tqdm import tqdm
import tempfile
import subprocess
import shutil
from termcolor import colored
from subprocess import PIPE
from subprocess import TimeoutExpired
import os
from dotenv import load_dotenv
from chains.chains import Chains
load_dotenv()

def decodeResults(results):
    return (res.strip().decode('utf-8') for res in results)

def refineCode(code):
    if "```" in code: 
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python"):].strip()
    return code

def runPython(code, timeout_sec=10):
    code = refineCode(code)
    with tempfile.NamedTemporaryFile("w") as tmp:
        tmp.write(code)
        tmp.flush()
        environmental_variables = {'OPENAI_API_KEY':os.getenv('OPENAI_API_KEY')}
        python_path = shutil.which("python")
        if not python_path: # shows 'which' returns None
            python_path = sys.executable 
        process = subprocess.Popen([python_path,tmp.name], env=environmental_variables,stdout=PIPE, stderr=PIPE)
        try:
            output, err = decodeResults(process.communicate(timeout=timeout_sec))
            success = len(err) == 0
        except TimeoutExpired:
            process.kill()
            success = True
            output = err = ""
        return output, err, success

persist_directory = "goals_db"
embeddings = HuggingFaceEmbeddings(model_kwargs = {'device': "cuda"})
if os.path.exists(persist_directory):
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)        
else:
    docs = []
    for dirpath, dirnames, filenames in tqdm(os.walk("examples/goals/")):
        for file in filenames:
            if file.endswith(".md"):
                filepath = os.path.join(dirpath, file)
                source_path = filepath.replace("goals","codes/").replace(".md",".py")
                with open(source_path) as sf:
                    metadata = {"source":sf.read()}
                with open(filepath) as f:
                    docs.append(Document(page_content=f.read(), metadata=metadata))
    db = Chroma.from_documents(docs, embeddings,persist_directory=persist_directory)

retriever = db.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["maximal_marginal_relevance"] = True
retriever.search_kwargs["k"] = 4

llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0) 

expert = LangChainExpert()

def getSource(query):
    resulting_text = ""
    docs = retriever.get_relevant_documents(query)
    for doc in docs:
        resulting_text += doc.metadata["source"]
        resulting_text += "\n" + "#"*40
    return resulting_text

def getTasks(task):
    instruction_list =  Chains.divide(task=task)
    if instruction_list.startswith("["):
        instruction_list = instruction_list[1:]
    if instruction_list.endswith("]"):
        instruction_list = instruction_list[:-1]
    return [insruction.strip() for insruction in instruction_list.split(",")]

def mergeTasks(task,examples):
    merged_code = Chains.merge(task=task,examples=examples)
    merged_code = refineCode(merged_code)
    return merged_code

def getSubResult(query,iterations):
    doc = getSource(query)
    draft_code = Chains.draft(document=doc, idea=query)
    for _ in range(iterations):
        print(colored(draft_code,"yellow"))
        output, error,success = runPython(draft_code)
        print(colored(output,"blue"))
        print(colored(error,"red"))
        if not success:
            feedback = expert.debug(error)
            print(colored(feedback,"blue"))
            draft_code =  Chains.debug(draft_code=draft_code, idea=query, feedback=feedback,document=doc)
        else:
            return refineCode(draft_code)
    return None 

def getLangChainCode(instruction,iterations):
    tasks = getTasks(instruction)
    print(tasks)
    examples = ""
    for i,task in enumerate(tasks):
        code = getSubResult(task,iterations=iterations)
        if code:
            examples += f"""
            Subtask {i+1} : {task}
            Code {i+1} : {code}
            {'#'*40}

            """
    if len(tasks) == 1:
        return code
    final_code = mergeTasks(instruction,examples)
    return final_code

def getStreamlitCode(instruction,langchain_code,title):
    merged_code = Chains.streamlit(instruction=instruction,langchain_code=langchain_code,title=title)
    merged_code = refineCode(merged_code)
    return merged_code

def get(instruction="Create a translation system that converts English to French",title="my translator",iterations=10):
    langchain_code = getLangChainCode(instruction,iterations=iterations)
    print(colored(langchain_code,"green"))
    return getStreamlitCode(instruction,langchain_code,title)   

if __name__ == "__main__":
    fire.Fire(get)