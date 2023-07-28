import utils
from chains.chains import Chains


class Model:
    def __init__(self, openai_api_key="sk-", model_name="gpt-3.5-turbo"):
        self.model_name = model_name
        self.openai_api_key = openai_api_key
        Chains.setLlm(self.model_name, self.openai_api_key)

    def setModel(self, model_name):
        self.model_name = model_name
        Chains.setLlm(self.model_name, self.openai_api_key)

    def __call__(
        self, instruction="Create a translation system that converts English to French"
    ):
        yield {"stage": "start"}
        system_inputs = Chains.inputs(instruction)
        button_text = Chains.buttonText(instruction)

        task_list = Chains.tasks(instruction=instruction, system_inputs=system_inputs)

        yield {"stage": "plan", "tasks": task_list}

        explanation = Chains.explain(instruction=instruction, task_list=task_list)

        yield {"stage": "explanation"}

        langchain_functions = utils.getLangchainFunctions(task_list)

        yield {"stage": "langchain", "code": langchain_functions}

        streamlit_functions = utils.getStreamlitFunctions(task_list)

        yield {"stage": "streamlit", "code": streamlit_functions}

        final_code = Chains.final(
            instruction=instruction,
            streamlit_code=streamlit_functions,
            langchain_code=langchain_functions,
            explanation=explanation,
            button_text=button_text,
            imports_code_snippet=utils.IMPORTS_CODE_SNIPPET,
        )

        yield {"stage": "done", "code": final_code}
