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
        if isinstance(args, list):
            args = ",".join(args)
        instruction = task["description"]
        code = cls.getChain(
            human_template=prompts.ui_output_text.human_template,
            instruction=instruction,
            args=args,
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
    def promptTemplate(cls, task, code_snippets):
        inputs = task["input_key"]
        instruction = task["description"]

        res = cls.getChain(
            system_template=prompts.prompt_template.system_template,
            human_template=prompts.prompt_template.human_template,
            instruction=instruction,
            inputs=inputs,
            code_snippets=code_snippets,
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
            variable=variable
        )
        return utils.refine(code)
    
    @classmethod
    def uiOutputChat(cls, task):
        res = task["input_key"]

        code = f"""
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
            inputs=inputs
        )
        res = res.replace("'''",'"""')
        res = res[res.find("{") : res.rfind("}") + 1]
        return json.loads(res,strict=False)

    @classmethod
    def promptTemplateRefiner(cls, templates, feedback):
        res = cls.getChain(
            system_template=prompts.prompt_chat_refiner.system_template,
            human_template=prompts.prompt_chat_refiner.human_template,
            templates=templates,
            feedback=feedback,
        )
        res = res[res.find("{") : res.rfind("}") + 1]
        return json.loads(res)

    @classmethod
    def docLoad(cls, task, code_snippets):
        instruction = task["description"]
        argument = task["input_key"]
        if isinstance(argument, list):
            argument = argument[0]
        variable = task["output_key"]
        function_name = task["task_name"]

        code = cls.getChain(
            system_template=prompts.doc_load.system_template,
            human_template=prompts.doc_load.human_template,
            instruction=instruction,
            argument=argument,
            variable=variable,
            function_name=function_name,
            code_snippets=code_snippets,
        )
        return utils.refine(code)

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
    return chain.run(docs)
if {argument}:
    {variable} = summarize(argument)
else:
    variable = ""
"""
        return code
