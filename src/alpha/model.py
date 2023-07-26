import logging
import os

import fire
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from tqdm import tqdm

import utils
from chains.chains import Chains


class Model:
    def __init__(
        self,
        openai_api_key="sk-",
        model_name="gpt-3.5-turbo"
    ):
        Chains.setLlm(model_name, openai_api_key)

    def __call__(
        self,
        instruction="Create a translation system that converts English to French",
        title="my translator",
        iterations=10,
    ):
        system_inputs = Chains.inputs(instruction)
        button_text = Chains.buttonText(instruction)

        yield {
            "stage":"start"
        }

        task_list = Chains.tasks(instruction=instruction,
                                 system_inputs=system_inputs)
        
        yield {
            "stage":"plan"
        }
        
        
        ai_tasks, ai_functions = utils.getAIPieces(task_list)
        streamlit_code = Chains.streamlit(instruction=instruction,
                                          task_list=task_list,
                                          button_text=button_text,
                                          ai_functions=ai_functions)
        
        yield {
            "stage":"draft"
        }

        langchain_functions = utils.getLangchainFunctions(ai_tasks)

        yield {
            "stage":"langchain"
        }

        final_code = Chains.final(instruction=instruction,
                                  streamlit_code=streamlit_code, 
                                  langchain_code=langchain_functions,
                                  imports_code_snippet=utils.IMPORTS_CODE_SNIPPET)
        
        yield {
            "stage":"done",
            "code":final_code
        }
        
