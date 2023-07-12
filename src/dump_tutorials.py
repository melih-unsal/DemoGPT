from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
from langchain.chat_models import ChatOpenAI
import os
from tqdm import tqdm

ROOT = "../documents/langchain/"

OUT_ROOT = ROOT.replace("langchain","langchain_tutorials")

os.makedirs(OUT_ROOT,exist_ok=True)

llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0) 

def getRes(messages):
    res = llm(messages)
    return res.content

prompt_template = """
Create a tutorial for teaching the langchain to a computer engineer student using the document below:
Don't mention about any installation steps because all the libraries have been already installed.
Remove all the installation codes.

{document}
"""

for filename in tqdm(os.listdir(ROOT)):
    out_path = os.path.join(OUT_ROOT,filename)
    if os.path.exists(out_path):
        continue
    filepath = os.path.join(ROOT,filename)
    with open(filepath) as f:
        document = f.read()
    prompt = prompt_template.format(document=document)
    messages = [HumanMessage(content=prompt)]
    res = getRes(messages)
    with open(out_path,"w") as f:
        f.write(res)