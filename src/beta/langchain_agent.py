import os
import shutil
import subprocess
import sys
import tempfile
from subprocess import PIPE, TimeoutExpired

import fire
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from termcolor import colored
from tqdm import tqdm

from agent_prompts import *
from langchain_expert import LangChainExpert

load_dotenv()

from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)


def decodeResults(results):
    return (res.strip().decode("utf-8") for res in results)


def refineCode(code):
    if "```" in code:
        code = code.split("```")[1]
        if code.startswith("python"):
            code = code[len("python") :].strip()
    return code


def runPython(code, timeout_sec=10):
    code = refineCode(code)
    with tempfile.NamedTemporaryFile("w") as tmp:
        tmp.write(code)
        tmp.flush()
        environmental_variables = {"OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")}
        python_path = shutil.which("python")
        if not python_path:  # shows 'which' returns None
            python_path = sys.executable
        process = subprocess.Popen(
            [python_path, tmp.name],
            env=environmental_variables,
            stdout=PIPE,
            stderr=PIPE,
        )
        try:
            output, err = decodeResults(process.communicate(timeout=timeout_sec))
            success = len(err) == 0
        except TimeoutExpired:
            process.kill()
            success = True
            output = err = ""
        return output, err, success


persist_directory = "goals_db"
embeddings = HuggingFaceEmbeddings(model_kwargs={"device": "cuda"})
if os.path.exists(persist_directory):
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
else:
    docs = []
    for dirpath, dirnames, filenames in tqdm(os.walk("examples/goals/")):
        for file in filenames:
            if file.endswith(".md"):
                filepath = os.path.join(dirpath, file)
                source_path = filepath.replace("goals", "codes/").replace(".md", ".py")
                with open(source_path) as sf:
                    metadata = {"source": sf.read()}
                with open(filepath) as f:
                    docs.append(Document(page_content=f.read(), metadata=metadata))
    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)

retriever = db.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["maximal_marginal_relevance"] = True
retriever.search_kwargs["k"] = 4

llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)

expert = LangChainExpert()


def getSource(query):
    resulting_text = ""
    docs = retriever.get_relevant_documents(query)
    for doc in docs:
        resulting_text += doc.metadata["source"]
        resulting_text += "\n" + "#" * 40
    return resulting_text


def getTasks(task):
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        DIVIDE_TASKS_SYSTEM_TEMPLATE
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        DIVIDE_TASKS_HUMAN_TEMPLATE
    )
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    chain = LLMChain(llm=llm, prompt=chat_prompt)
    instruction_list = chain.run(task=task)
    if instruction_list.startswith("["):
        instruction_list = instruction_list[1:]
    if instruction_list.endswith("]"):
        instruction_list = instruction_list[:-1]
    return [insruction.strip() for insruction in instruction_list.split(",")]


def mergeTasks(task, examples):
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        MERGE_CODES_SYSTEM_TEMPLATE
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        MERGE_CODES_HUMAN_TEMPLATE
    )
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    chain = LLMChain(llm=llm, prompt=chat_prompt)
    merged_code = chain.run(task=task, examples=examples)
    merged_code = refineCode(merged_code)
    return merged_code


def getSubResult(query, iterations):
    doc = getSource(query)

    human_message_prompt = HumanMessagePromptTemplate.from_template(DOC_USE_TEMPLATE)
    chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])
    chain = LLMChain(llm=llm, prompt=chat_prompt)

    draft_code = chain.run(document=doc, idea=query)

    for _ in range(iterations):
        print(colored(draft_code, "yellow"))
        output, error, success = runPython(draft_code)
        print(colored(output, "blue"))
        print(colored(error, "red"))
        if not success:
            question = f"""
            How to solve that error below?

            {error}
            """

            feedback = expert.ask(question)

            print(colored(feedback, "blue"))

            human_message_prompt = HumanMessagePromptTemplate.from_template(
                APP_DEBUGGING_TEMPLATE
            )
            chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])
            chain = LLMChain(llm=llm, prompt=chat_prompt)
            draft_code = chain.run(
                draft_code=draft_code, idea=query, feedback=feedback, document=doc
            )
        else:
            return refineCode(draft_code)
    return None


def getLangChainCode(instruction, iterations):
    tasks = getTasks(instruction)
    print(tasks)
    examples = ""
    for i, task in enumerate(tasks):
        code = getSubResult(task, iterations=iterations)
        if code:
            examples += f"""
            Subtask {i+1} : {task}
            Code {i+1} : {code}
            {'#'*40}

            """
    if len(tasks) == 1:
        return code
    final_code = mergeTasks(instruction, examples)
    return final_code


def getStreamlitCode(instruction, langchain_code, title):
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        STREAMLIT_CODE_SYSTEM_TEMPLATE
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        STREAMLIT_CODE_HUMAN_TEMPLATE
    )
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    chain = LLMChain(llm=llm, prompt=chat_prompt)
    merged_code = chain.run(
        instruction=instruction, langchain_code=langchain_code, title=title
    )
    merged_code = refineCode(merged_code)
    return merged_code


def get(
    instruction="Create a translation system that converts English to French",
    title="my translator",
    iterations=10,
):
    langchain_code = getLangChainCode(instruction, iterations=iterations)
    print(colored(langchain_code, "green"))
    return getStreamlitCode(instruction, langchain_code, title)


def streamlit_test():
    langchain_code = """
    from langchain.llms import OpenAI
    from langchain.chains import ConversationChain
    from langchain.memory import ConversationSummaryBufferMemory

    llm = OpenAI()

    psychologist = ConversationChain(
        llm=llm,
        memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=500),
        verbose=True
    )

    print("Welcome to the Personal Psychologist!")
    print("You can start by telling me about your problems or concerns.")

    while True:
        user_input = input("You: ")
        response = psychologist.predict(input=user_input)
        print("Psychologist:", response)
    """

    instruction = (
        "Create a personal psychologist that can remember the conversation history"
    )
    title = "My Psychologist"

    system_message_prompt = SystemMessagePromptTemplate.from_template(
        STREAMLIT_CODE_SYSTEM_TEMPLATE
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        STREAMLIT_CODE_HUMAN_TEMPLATE
    )
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    chain = LLMChain(llm=llm, prompt=chat_prompt)
    merged_code = chain.run(
        instruction=instruction, langchain_code=langchain_code, title=title
    )
    merged_code = refineCode(merged_code)
    return merged_code


if __name__ == "__main__":
    fire.Fire(get)
