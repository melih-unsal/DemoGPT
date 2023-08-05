# Models Overview

This section provides an overview of the models used in DemoGPT. Currently, we are using two main models, `LogicModel` and `StreamlitModel`. These models interact with the OpenAI GPT-3.5-turbo to perform specific tasks and generate LangChain pipelines automatically.


## Introduction

This Python module contains the implementation of three main classes - `BaseModel`, `LogicModel`, and `StreamlitModel`. The classes encapsulate a way to interact with OpenAI and the logic to refine and execute python code using a subprocess, while also managing temporary files. 

## Classes

### BaseModel

The `BaseModel` is a foundational class used to interact with OpenAI.

#### Attributes:

- `openai_api_key`: The API key for OpenAI.
- `llm`: An instance of the `ChatOpenAI` class.

#### Methods:

- `__init__(self,openai_api_key)`: A constructor that initializes the BaseModel with the provided OpenAI API key.
- `refine_code(self,code)`: A method that refines python code removing markdown code block syntax.

### LogicModel

`LogicModel` is a class used to interact with OpenAI to obtain python code and subsequently refine, test, and execute it. 

#### Attributes:

- `code_chain`: An instance of `LLMChain` with the `code_prompt`.
- `test_chain`: An instance of `LLMChain` with the `test_prompt`.
- Other chain attributes for refining, fixing, and checking code.

#### Methods:

- `__init__(self,openai_api_key)`: A constructor that initializes the LogicModel with the provided OpenAI API key.
- `addDocuments(self)`: This method reads text from a specified file and saves it to `self.document`.
- `decode_results(self, results)`: This method decodes the result of the subprocess command.
- `run_python(self,code)`: This method executes python code using a subprocess and decodes the result.
- `__call__(self,topic,num_iterations=10)`: This method uses the various chains to generate, refine, and test python code based on a given topic.

### StreamlitModel

`StreamlitModel` is a class that uses OpenAI to create a Streamlit app, which is then run as a subprocess.

#### Attributes:

- `streamlit_code_chain`: An instance of `LLMChain` with the `streamlit_code_prompt`.

#### Methods:

- `__init__(self,openai_api_key)`: A constructor that initializes the StreamlitModel with the provided OpenAI API key.
- `run_code(self,code)`: This method writes the Streamlit code to a temporary file and runs it as a subprocess.
- `__call__(self,topic, title, code, test_code,progress_func,success_func)`: This method generates the Streamlit code, executes it, and returns the process ID.

