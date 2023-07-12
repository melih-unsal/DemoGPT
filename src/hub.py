from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
import fire
from tqdm import tqdm
import os
from dotenv import load_dotenv
import tiktoken
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from pprint import pprint

load_dotenv()

persist_directory = "hub"

embeddings = HuggingFaceEmbeddings(model_kwargs = {'device': 'cuda'})

def getLoadCommand(path):
    search_word = "langchain-hub"
    folder = path.replace(path.split('/')[-1],"")
    files = os.listdir(folder)
    for f in files:
        path = os.path.join(folder,f)
        if os.path.isfile(path):
            if path.endswith(".md"):
                continue
            index = path.index(search_word) + len(search_word)+1
            url = "lc://"+path[index:]
            command = f"""
            # To use load_prompt, you can use like in the below:
            prompt = load_prompt('{url}')
            """
            return command
    return ""
        
            


if os.path.exists(persist_directory):
    docsearch = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
else:
    import glob
    files = glob.glob('../../langchain-hub/prompts/**/README.md', recursive=True)
    docs = []
    for file in tqdm(files):
        if "/agents" in file:
            continue
        if "langchain-hub/README.md" in file:
            continue
        with open(file, 'r') as f:
            document = f.read()
        command = getLoadCommand(file)
        if command:
            document += "\n" + command
        metadata = {"source":document,"path":file}
        print(command)
        docs.append(Document(page_content=document, metadata=metadata))
    docsearch = Chroma.from_documents(docs, embeddings)#,persist_directory=persist_directory)
retriever = docsearch.as_retriever(search_type="mmr",search_kwargs={"k":1})

additional_info = """

    Chain objects have a run method to run input on it.
    Example:

    # question is coming from input variables
    res = math_chain.run(question="I have 3 apples and 4 bananas. If I give you 1 apple and 1 banana, how many fruits that I would have?")
    print(res) # it will print the result of the chain

"""

with open("../../langchain-hub/README.md") as f:
    initial_document = f.read() + additional_info


llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0) 

def getRes(messages):
    res = llm(messages)
    return res.content

def get(query):
    res = retriever.get_relevant_documents(query)
    document = ""
    for i,doc in enumerate(res):
        document = doc.page_content
    
    #print(document)

    prompt_template = """Write a langchain hub code to accomplish the goal.

    document:{document}
    ################################################################
    Goal: {goal}
    ################################################################
    Langchain hub code:"""
    prompt = prompt_template.format(goal=query, document=initial_document + "\n\n" + document)
    messages = [HumanMessage(content=prompt)]
    return getRes(messages)
    
    prompt_template = """Use the following langchain documentation to generate a Streamlit application to accomplish the goal.

    document:{document}
    ################################################################
    Goal: {goal}
    ################################################################
    Streamlit Code:"""
    prompt = prompt_template.format(goal=query, document=document)
    """messages = [HumanMessage(content=prompt)]
    return getRes(messages)"""

if __name__ == "__main__":
    fire.Fire(get)