from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from tqdm import tqdm

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)


def refine_code(code):
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python") :].strip()
    return code


def getCode(doc):
    prompt = f"""
    Transfer the below document to a valid python code by preserving the standard texts as comments

    {doc}
    """
    messages = [HumanMessage(content=prompt)]
    code = llm(messages).content
    return refine_code(code)


def getGoals(doc):
    prompt = f"""
    For which project ideas, the techniques inside the below code could be used?
    Create a list of project idea

    {doc}
    """
    messages = [HumanMessage(content=prompt)]
    code = llm(messages).content
    return refine_code(code)


import os

ROOT = "docs"

# Fill codes folder
for filename in tqdm(os.listdir(ROOT)):
    filepath = os.path.join(ROOT, filename)
    out_filename = filename.replace(".txt", ".py")
    out_path = f"examples/codes/{out_filename}"
    if os.path.exists(out_path):
        continue
    with open(filepath) as f:
        doc = f.read()
    code = getCode(doc)
    with open(out_path, "w") as f:
        f.write(code)

CODE_ROOT = "examples/codes/"
# Fill goals folder
for filename in tqdm(os.listdir(CODE_ROOT)):
    filepath = os.path.join(CODE_ROOT, filename)
    out_filename = filename.replace(".py", ".md")
    out_path = f"examples/goals/{out_filename}"
    if os.path.exists(out_path):
        continue
    with open(filepath) as f:
        code = f.read()
    goals = getGoals(code)
    with open(out_path, "w") as f:
        f.write(goals)
