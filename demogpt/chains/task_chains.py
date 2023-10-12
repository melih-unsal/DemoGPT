import json
import os
import re
from difflib import SequenceMatcher

from langchain.chains import LLMChain
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
    def uiInputText(cls, task):
        variable = ", ".join(task["output_key"])
        instruction = task["description"]
        code = cls.getChain(
            human_template=prompts.ui_input_text.human_template,
            instruction=instruction,
            variable=variable,
        )
        return utils.refine(code)

    @classmethod
    def uiOutputText(cls, task):
        args = ", ".join(task["input_key"])
        data_type = task["input_data_type"]
        if isinstance(args, list):
            args = ",".join(args)
        instruction = task["description"]
        code = cls.getChain(
            system_template=prompts.ui_output_text.system_template,
            human_template=prompts.ui_output_text.human_template,
            instruction=instruction,
            args=args,
            data_type=data_type,
        )
        return utils.refine(code)

    @classmethod
    def uiInputFile(cls, task):
        variable = ", ".join(task["output_key"])
        instruction = task["description"]
        res = cls.getChain(
            system_template=prompts.ui_input_file.system_template,
            human_template=prompts.ui_input_file.human_template,
            instruction=instruction
        )
        res = res[res.find("{") : res.rfind("}") + 1]
        res = json.loads(res)
        title = res.get("title")
        data_type = res.get("data_type")
        code = f"""
uploaded_file = st.file_uploader("{title}", type={data_type}, key='{variable}')
if uploaded_file is not None:
    # Create a temporary file to store the uploaded content
    extension = uploaded_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{{extension}}') as temp_file:
        temp_file.write(uploaded_file.read())
        {variable} = temp_file.name # it shows the file path
else:
    {variable} = ''
        """
        return code

    @classmethod
    def pathToContent(cls, task, code_snippets):
        instruction = task["description"]
        argument = ", ".join(task["input_key"])
        variable = ", ".join(task["output_key"])

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
        inputs = ", ".join(task["input_key"])
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
        variable = ", ".join(task["output_key"])
        instruction = task["description"]

        code = cls.getChain(
            human_template=prompts.ui_input_chat.human_template,
            instruction=instruction,
            variable=variable,
        )
        return utils.refine(code)

    @classmethod
    def uiOutputChat(cls, task):
        res = ", ".join(task["input_key"])

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
        inputs = ", ".join(task["input_key"])
        instruction = task["description"]

        res = cls.getChain(
            system_template=prompts.chat.system_template,
            human_template=prompts.chat.human_template,
            instruction=instruction,
            inputs=inputs,
        )
        res = res.replace("'''", '"""')
        print("chat:")
        print(res)
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
        print("promptTemplateRefiner:")
        print(res)
        res = res[res.find("{") : res.rfind("}") + 1]
        return json.loads(res)
    
    @classmethod
    def search_chat(cls, task):
        argument = ", ".join(task["input_key"])
        variable = ", ".join(task["output_key"])
        function_name = task["task_name"]
        instruction = task["description"]

        res = cls.getChain(
            system_template=prompts.search.system_template,
            human_template=prompts.search.human_template,
            instruction=instruction,
            inputs=argument,
        )
        
        res = res.replace('"',"'")

        code = f"""
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.tools import DuckDuckGoSearchRun
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.agents.tools import Tool
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler

msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
)

def {function_name}({argument}):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        DuckDuckGoSearchRun(name="Search"),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        )]
    chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=tools)
    executor = AgentExecutor.from_agent_and_tools(
        agent=chat_agent,
        tools=tools,
        memory=memory,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
    )
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
    return executor({argument}, callbacks=[st_cb])["output"]

if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
elif {argument}:
    {variable} = {function_name}({argument})
else:
    {variable} = ''
  
        """
        
        return code

    @classmethod
    def search(cls, task):
        argument = ", ".join(task["input_key"])
        variable = ", ".join(task["output_key"])
        function_name = task["task_name"]
        instruction = task["description"]

        res = cls.getChain(
            system_template=prompts.search.system_template,
            human_template=prompts.search.human_template,
            instruction=instruction,
            inputs=argument,
        )
        
        res = res.replace('"',"'")

        code = f"""
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMMathChain
from langchain.callbacks import StreamlitCallbackHandler

def {function_name}({argument}):
    search_input = "{res}".format({argument}={argument})
    llm = OpenAI(openai_api_key=openai_api_key, temperature=0)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [
        DuckDuckGoSearchRun(name="Search"),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        ),
    ]
    model = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
    return agent.run(search_input, callbacks=[st_cb])
        
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
elif {argument}:
    {variable} = {function_name}({argument})
else:
    {variable} = ''
        """
        return code

    @classmethod
    def docLoad(cls, task, code_snippets):
        
        def get_most_similar_key(input_key, available_keys):
            # This function returns the most similar key from available_keys to the input_key.
            best_match = None
            best_ratio = 0
            for key in available_keys:
                ratio = SequenceMatcher(None, input_key, key).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = key
            return best_match
        
        type2loader = {
            "txt": "TextLoader",
            "docx":"UnstructuredWordDocumentLoader",
            "pdf":"UnstructuredPDFLoader",
            "pptx":"UnstructuredPowerPointLoader",
            "csv":"CSVLoader",
            "xlsx":"UnstructuredExcelLoader",
            "zip":"NotionDirectoryLoader",
            "online_pdf":"OnlinePDFLoader",
            "web":"WebBaseLoader",
            "xlsx":"UnstructuredExcelLoader",
            "youtube":"YoutubeLoader",  
        }
        
        loader2type = {type2loader[dtype]:dtype for dtype in type2loader}
        
        def getLoaderCall(data_type):
            if data_type in loader2type:
                data_type = loader2type[data_type]
            
            loader = type2loader.get(data_type)  # First, try to get the exact match
            if loader is None:
                # If there's no exact match, get the most similar key and retrieve the value
                similar_key = get_most_similar_key(data_type, type2loader.keys())
                loader = type2loader[similar_key]
                
            loader = type2loader[data_type]
            
            if data_type in [
                "txt",
                "online_pdf",
                "docx",
                "csv"
            ]:
                loader_line = f"loader = {loader}({argument})"
            elif data_type == "web":
                loader_line = f"loader = {loader}([{argument}])"
            elif data_type in ["pdf", "pptx"]:
                loader_line = (
                    f'loader = {loader}({argument}, mode="elements", strategy="fast")'
                )
            elif data_type  == "xlsx":
                loader_line = f'loader = {loader}({argument}, mode="elements")'
            elif data_type == "youtube":
                loader_line = (
                    f"loader = {loader}.from_youtube_url({argument}, add_video_info=False)"
                )
            elif data_type == "zip":
                loader_line = f"""if os.path.exists('Notion_DB') and os.path.isdir('Notion_DB'):
            shutil.rmtree('Notion_DB')
        os.system(f"unzip {{{argument}}} -d Notion_DB")
        loader = {loader}("Notion_DB")"""
            else:
                loader_line = f"loader = TextLoader({argument})"
            
            return loader_line
        
        instruction = task["description"]
        argument = task["input_key"][0]
        variable = ", ".join(task["output_key"])
        function_name = task["task_name"]
        
        variable_match = re.search(r"(\w+)\s*=\s*temp_file\.name", code_snippets, re.MULTILINE)
        
        if variable_match:
            variable_name = variable_match.group(1).strip()
        else:
            variable_name = ''
            
        match = re.search(r"st\.file_uploader\(\s*?.*?type=\s*\[(.*?)\]\s*?.*?\)", code_snippets, re.DOTALL)
                
        loader_line = ""

        if variable_name == argument and  match:
            types = match.group(1).replace("'", "").split(", ")
            types = [type.strip() for type in types]
            if len(types) == 1:
                loader_line = getLoaderCall(types[0])
            else:
                loader_line = "\n    ".join([f"if {argument}.endswith('.{data_type}'):\n\t{getLoaderCall(data_type)}" for data_type in types])
        else:
            print("No match found. Using the chain...")
            types = []
            loader = cls.getChain(
                system_template=prompts.doc_load.system_template,
                human_template=prompts.doc_load.human_template,
                instruction=instruction,
                code_snippets=code_snippets
                )
            
            loader_line = getLoaderCall(loader)
            
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
    def stringToDoc(cls, task):
        argument = ", ".join(task["input_key"])
        variable = ", ".join(task["output_key"])
        code = f"""
from langchain.docstore.document import Document
{variable} =  [Document(page_content={argument}, metadata={{'source': 'local'}})]
        """
        return code

    @classmethod
    def docToString(cls, task):
        argument = ", ".join(task["input_key"])
        variable = ", ".join(task["output_key"])
        code = f'{variable} = "".join([doc.page_content for doc in {argument}])'
        return code

    @classmethod
    def summarize(cls, task):
        argument = ", ".join(task["input_key"])
        variable = ", ".join(task["output_key"])
        function_name = task["task_name"]

        code = f"""
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain

def {function_name}(docs):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    with st.spinner('DemoGPT is working on it. It might take 5-10 seconds...'):
        return chain.run(docs)
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
    {variable} = ""
elif {argument}:
    {variable} = summarize(argument)
else:
    variable = ""
"""
        return code

    @classmethod
    def pythonCoder(cls, task, code_snippets):
        instruction = task["description"]
        argument = ", ".join(task["input_key"])
        variable = ", ".join(task["output_key"])
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