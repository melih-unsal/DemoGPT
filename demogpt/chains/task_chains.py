import json
import os

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

from demogpt import utils
from demogpt.chains import prompts


class TaskChains:
    llm = None

    @classmethod
    def setLlm(
        cls,
        model,
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        temperature=0.0,
        openai_api_base=None,
    ):
        cls.llm = ChatOpenAI(
            model=model,
            openai_api_key=openai_api_key,
            temperature=temperature,
            openai_api_base=openai_api_base,
        )

    @classmethod
    def getChain(cls, system_template="", human_template="", **kwargs):
        prompts = []
        if system_template:
            prompts.append(SystemMessagePromptTemplate.from_template(system_template))
        if human_template:
            prompts.append(HumanMessagePromptTemplate.from_template(human_template))
        chat_prompt = ChatPromptTemplate.from_messages(prompts)
        return LLMChain(llm=cls.llm, prompt=chat_prompt).run(**kwargs)

    @classmethod
    def uiInputText(cls, task, code_snippets):
        variable = task["output_key"]
        instruction = task["description"]
        code = cls.getChain(
            human_template=prompts.ui_input_text.human_template,
            instruction=instruction,
            variable=variable,
        )
        return utils.refine(code)

    @classmethod
    def uiOutputText(cls, task, code_snippets):
        args = task["input_key"]
        data_type = task["input_data_type"]
        if isinstance(args, list):
            args = ",".join(args)
        instruction = task["description"]
        code = cls.getChain(
            human_template=prompts.ui_output_text.human_template,
            instruction=instruction,
            args=args,
            data_type=data_type,
        )
        return utils.refine(code)

    @classmethod
    def uiInputFile(cls, task, code_snippets):
        variable = task["output_key"]
        instruction = task["description"]
        code = cls.getChain(
            system_template=prompts.ui_input_file.system_template,
            human_template=prompts.ui_input_file.human_template,
            instruction=instruction,
            variable=variable,
            code_snippets=code_snippets,
        )
        return utils.refine(code)

    @classmethod
    def pathToContent(cls, task, code_snippets):
        instruction = task["description"]
        argument = task["input_key"]
        variable = task["output_key"]

        code = cls.getChain(
            system_template=prompts.path_to_file.system_template,
            human_template=prompts.path_to_file.human_template,
            instruction=instruction,
            argument=argument,
            variable=variable,
            code_snippets=code_snippets,
        )
        return utils.refine(code)

    @classmethod
    def promptTemplate(cls, task):
        inputs = task["input_key"]
        instruction = task["description"]

        res = cls.getChain(
            system_template=prompts.prompt_template.system_template,
            human_template=prompts.prompt_template.human_template,
            instruction=instruction,
            inputs=inputs,
        )
        res = res[res.find("{") : res.rfind("}") + 1]
        return json.loads(res)

    @classmethod
    def uiInputChat(cls, task):
        variable = task["output_key"]
        instruction = task["description"]

        code = cls.getChain(
            human_template=prompts.ui_input_chat.human_template,
            instruction=instruction,
            variable=variable,
        )
        return utils.refine(code)

    @classmethod
    def uiOutputChat(cls, task):
        res = task["input_key"]

        code = f"""
import time

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in {res}.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    if full_response:
        st.session_state.messages.append({{"role": "assistant", "content": full_response}})        
        """
        return code

    @classmethod
    def chat(cls, task):
        inputs = task["input_key"]
        instruction = task["description"]

        res = cls.getChain(
            system_template=prompts.chat.system_template,
            human_template=prompts.chat.human_template,
            instruction=instruction,
            inputs=inputs,
        )
        res = res.replace("'''", '"""')
        res = res[res.find("{") : res.rfind("}") + 1]
        return json.loads(res, strict=False)

    @classmethod
    def promptTemplateRefiner(cls, templates, inputs, feedback):
        res = cls.getChain(
            system_template=prompts.prompt_chat_refiner.system_template,
            human_template=prompts.prompt_chat_refiner.human_template,
            templates=templates,
            feedback=feedback,
            inputs=inputs,
        )
        res = res[res.find("{") : res.rfind("}") + 1]
        return json.loads(res)

    @classmethod
    def search(cls, task):
        argument = task["input_key"]
        variable = task["output_key"]
        function_name = task["task_name"]
        instruction = task["description"]

        res = cls.getChain(
            system_template=prompts.search.system_template,
            human_template=prompts.search.human_template,
            instruction=instruction,
            inputs=argument,
        )

        code = f"""
from langchain.chat_models import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain.llms import OpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents.tools import Tool
from langchain.chains import LLMMathChain

def {function_name}({argument}):
    search_input = "{res}".format({argument}={argument})
    search = GoogleSerperAPIWrapper()
    llm = OpenAI(temperature=0)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        Tool(
            name = "Search",
            func=search.run,
            description="useful for when you need to answer questions about current events"
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        ),
    ]
    model = ChatOpenAI(temperature=0, model_name="gpt-4")
    planner = load_chat_planner(model)
    executor = load_agent_executor(model, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
    try:
        with st.spinner('DemoGPT is working on it. It might take 1-2 minutes...'):
            return agent.run(search_input)
    except AuthenticationError:
        st.warning('This tool requires GPT-4. Please enter a key that has GPT-4 access', icon="⚠️")
        return ''
        

if {argument}:
    {variable} = {function_name}({argument})
else:
    {variable} = ''
        """
        return code

    @classmethod
    def docLoad(cls, task, code_snippets):
        instruction = task["description"]
        argument = task["input_key"]
        if isinstance(argument, list):
            argument = argument[0]
        variable = task["output_key"]
        function_name = task["task_name"]

        loader = cls.getChain(
            system_template=prompts.doc_load.system_template,
            human_template=prompts.doc_load.human_template,
            instruction=instruction,
            code_snippets=code_snippets,
        )

        if loader in [
            "TextLoader",
            "OnlinePDFLoader",
            "UnstructuredWordDocumentLoader",
        ]:
            loader_line = f"loader = {loader}({argument})"
        elif loader == "WebBaseLoader":
            loader_line = f"loader = {loader}([{argument}])"
        elif loader in ["UnstructuredPDFLoader", "UnstructuredPowerPointLoader"]:
            loader_line = (
                f'loader = {loader}({argument}, mode="elements", strategy="fast")'
            )
        elif loader in ["UnstructuredCSVLoader", "UnstructuredExcelLoader"]:
            loader_line = f'loader = {loader}({argument}, mode="elements")'
        elif loader == "YoutubeLoader":
            loader_line = (
                f"loader = {loader}.from_youtube_url({argument}, add_video_info=False)"
            )
        elif loader == "NotionDirectoryLoader":
            loader_line = f"""if os.path.exists('Notion_DB') and os.path.isdir('Notion_DB'):
        shutil.rmtree('Notion_DB')
    os.system(f"unzip {{{argument}}} -d Notion_DB")
    loader = {loader}("Notion_DB")"""
        else:
            loader_line = f"loader = TextLoader({argument})"

        code = f"""
import shutil
from langchain.document_loaders import *

def {function_name}({argument}):
    {loader_line}
    docs = loader.load()
    return docs
if {argument}:
    {variable} = {function_name}({argument})
else:
    {variable} = ''
        """
        return code

    @classmethod
    def stringToDoc(cls, task, code_snippets):
        argument = task["input_key"]
        variable = task["output_key"]
        code = f"""
from langchain.docstore.document import Document
{variable} =  [Document(page_content={argument}, metadata={{'source': 'local'}})]
        """
        return code

    @classmethod
    def docToString(cls, task, code_snippets):
        argument = task["input_key"]
        variable = task["output_key"]
        code = f'{variable} = "".join([doc.page_content for doc in {argument}])'
        return code

    @classmethod
    def summarize(cls, task, code_snippets):
        argument = task["input_key"]
        variable = task["output_key"]
        function_name = task["task_name"]

        code = f"""
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

def {function_name}(docs):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    with st.spinner('DemoGPT is working on it. It might take 5-10 seconds...'):
        return chain.run(docs)
if {argument}:
    {variable} = summarize(argument)
else:
    variable = ""
"""
        return code

    @classmethod
    def pythonCoder(cls, task, code_snippets):
        instruction = task["description"]
        argument = task["input_key"]
        variable = task["output_key"]
        function_name = task["task_name"]

        code = cls.getChain(
            system_template=prompts.python_coder.system_template,
            human_template=prompts.python_coder.human_template,
            instruction=instruction,
            argument=argument,
            variable=variable,
            function_name=function_name,
            code_snippets=code_snippets,
        )
        return utils.refine(code)
