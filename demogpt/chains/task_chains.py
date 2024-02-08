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
            openai_api_base=openai_api_base
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
        code = prompts.ui_input_file.code.format(instruction=instruction,
                                                 title=title,
                                                 data_type=data_type,
                                                 variable=variable
                                                 )
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
    def getDetailedDescription(cls, app_idea, instruction):
        return cls.getChain(
            system_template=prompts.detailed_description.system_template,
            human_template=prompts.detailed_description.human_template,
            app_idea=app_idea,
            instruction=instruction
        )

    @classmethod
    def promptTemplate(cls, app_idea, task):
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

        placeholder = cls.getChain(
            human_template=prompts.ui_input_chat.human_template,
            instruction=instruction,
            variable=variable,
        )
        
        code = prompts.ui_input_chat.code.format(variable=variable, placeholder=placeholder)
        
        return code

    @classmethod
    def uiOutputChat(cls, task):
        res = ", ".join(task["input_key"])

        code = prompts.ui_output_chat.code.format(res=res)
        
        return code

    @classmethod
    def chat(cls, app_idea, task):
        inputs = ", ".join(task["input_key"])
        instruction = task["description"]
        
        new_instruction = cls.getDetailedDescription(app_idea=app_idea,instruction=instruction)

        res = cls.getChain(
            system_template=prompts.chat.system_template,
            human_template=prompts.chat.human_template,
            instruction=new_instruction,
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
    def search_chat(cls, task):
        argument = ", ".join(task["input_key"])
        variable = ", ".join(task["output_key"])
        function_name = task["task_name"]
        instruction = task["description"]

        res = cls.getChain(
            system_template=prompts.search_chat.system_template,
            human_template=prompts.search_chat.human_template,
            instruction=instruction,
            inputs=argument,
        )
        
        res = res.replace('"',"'")

        imports = prompts.search_chat.imports
        functions = prompts.search_chat.functions.format(function_name=function_name, argument=argument)
        outputs = prompts.search_chat.outputs.format(function_name=function_name, argument=argument,variable=variable)
        
        code = imports + "\n" + functions + "\n" + outputs + "\n"
        
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

        imports = prompts.search.imports
        functions = prompts.search.functions.format(function_name=function_name, argument=argument,res=res)
        outputs = prompts.search_chat.outputs.format(function_name=function_name, argument=argument,variable=variable)
        code = imports + "\n" + functions + "\n" + outputs + "\n"
        
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
            
        imports = prompts.doc_load.imports
        functions = prompts.doc_load.functions.format(function_name=function_name, argument=argument, loader_line=loader_line)
        outputs = prompts.doc_load.outputs.format(argument=argument, function_name=function_name, variable=variable)
        
        code = imports + "\n" + functions + "\n" + outputs + "\n"
        
        return code

    @classmethod
    def stringToDoc(cls, task):
        argument = ", ".join(task["input_key"])
        variable = ", ".join(task["output_key"])
        imports = prompts.string_to_doc.imports
        outputs = prompts.string_to_doc.outputs.format(variable=variable, argument=argument)
        code = imports + "\n" + outputs + "\n"
        
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

        imports = prompts.summarize.imports
        functions = functions = prompts.summarize.functions.format(function_name=function_name, argument=argument)
        outputs = prompts.string_to_doc.outputs.format(function_name=function_name, variable=variable, argument=argument)
        
        code = imports + "\n" + functions + "\n" + outputs + "\n"
        
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