# Prompts Module Documentation

The `prompts.py` file serves as a crucial component of the DemoGPT project. It contains structured prompts for directing OpenAI's GPT-3.5-turbo model in the process of code generation, testing, refinement, bug fixing, and Streamlit application generation. These are implemented through a series of `ChatPromptTemplate` instances.

## Prompt Templates

- **`code_prompt`**: Generates Python code to meet a certain goal. The model is instructed to produce Python code similar to the codes in a supplied document.

- **`test_prompt`**: Produces a function call for testing a previously generated Python function. It prompts the model to create sample input and call the function inside the given Python script.

- **`refine_chat_prompt`**: Improves a content piece based on the provided critics, utilizing a reference document. The model is asked to refine a code snippet considering the error provided.

- **`fix_chat_prompt`**: Identifies and fixes bugs in a Python code snippet based on the provided error message.

- **`check_chat_prompt`**: Verifies if a Python code snippet is functioning as expected by examining the output. If the model decides that the output is inappropriate, it refines the code; otherwise, it returns the original code.

- **`streamlit_code_prompt`**: Generates Streamlit application code from a given goal, logic code, and test code. The model is tasked with creating Streamlit code that achieves the same objective as the test code.

## Understanding Prompt Templates

Each prompt template is assembled from system and/or human message prompts. These prompts originate from template strings that characterize the model's role and define the task it needs to complete. 

The `ChatPromptTemplate.from_messages()` function compiles these message prompts into a comprehensive chat prompt that instructs the model to produce the required output. This method accepts an array of system and human message prompts, with the sequence they appear in the array determining the conversation flow with the model.

## Usage 

These prompt templates are utilized throughout the DemoGPT project to guide the GPT-3.5-turbo model in generating, testing, refining, and fixing Python code, as well as creating Streamlit applications. They form the basic building blocks of the project's interaction with the language model.
