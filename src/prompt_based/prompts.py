from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

template1 = """
    You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. You use langchain library. You are good at using PromptTemplate to give appropriate prompt to accomplish the task.
    Put an appropriate prompt to enable the model to do {topic}
    Use the arguments which will be passed to the prompt template to run the chain when you define the function.
    """
system_message_prompt1 = SystemMessagePromptTemplate.from_template(template1)

human_template1 = """Write a python code similar to the codes in the document below which makes the following goal possible. Only use the arguments which will be used in in the prompt template for creating a chain.
Useful Document:
{document}
================================================================    
Goal:{topic} 
---------
Python Code:
"""

human_message_prompt1 = HumanMessagePromptTemplate.from_template(human_template1)

code_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt1, human_message_prompt1]
)

template2 = """
    You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. You will get a python code and add function test.
      Don't explain the code, just generate the code block itself.      
      Don't use any assert function!
    """

system_message_prompt2 = SystemMessagePromptTemplate.from_template(template2)

human_template2 = """Generate a sample input and call the function inside the python script below which makes it possible to do {topic}.
Only call the function with the appropriate arguments not use any standard library and don't generate any function but directly call the needed function.
While generating the function, take into an account for the critics {feedback}

Example:

Goal: Implement language translation
---------
Python Code:
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def generate_translation(input_language, output_language, text):
    chat = ChatOpenAI(temperature=0)

    template = "You are a helpful assistant that translates {{input_language}} to {{output_language}}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{{text}}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(input_language=input_language, output_language=output_language, text=text)
    return result # it will return string
---------
Function Test:
input_language = "English"
output_language = "Turkish"
text = "How are you today?"
result = generate_translation(input_language, output_language, text)
print(result)

Goal : {topic}
---------
Python Code:
{code}
---------
Function Test:
"""

human_message_prompt2 = HumanMessagePromptTemplate.from_template(human_template2)

test_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt2, human_message_prompt2]
)


refine_remplate = """
Based on the critics, fix the content provided to you while you can use the document. Fix the code snippet based on the error provided. Only provide the fixed code snippet between `` and nothing else.:
content:
{content}
---------
critics:
{critics}
---------
document:
{document}
---------
Python Code:
"""

refine_message_prompt = HumanMessagePromptTemplate.from_template(refine_remplate)

refine_chat_prompt = ChatPromptTemplate.from_messages([refine_message_prompt])

fix_template = """
    ##### Find the bugs in the below Python code
    
    ### Buggy Python
    {code}

    ### Error
    {error}

    ### Error Reason
    """

fix_message_prompt = HumanMessagePromptTemplate.from_template(fix_template)

fix_chat_prompt = ChatPromptTemplate.from_messages([fix_message_prompt])


check_template = """
    ##### Check if the below Python code is working for the needed goal by checking the received output.
    If you think it is not appropriate, refine the code, otherwise return the original code.

    ### Goal:{topic}
    
    ### Python Code:
    {code}

    ### Receieved Output:
    {response}

    ### Refined Code:
    """

check_message_prompt = HumanMessagePromptTemplate.from_template(check_template)

check_chat_prompt = ChatPromptTemplate.from_messages([check_message_prompt])

streamlit_code_template = """
    You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. 
    You will get a GOAL.
    You will get a logic code and test code.
    Logic code includes the logic part
    Test code includes the test part which tests the logic code
    Your tasks is generating a stremlit code which does the same thing that the test code does to accomplish the GOAL.
    """
streamlit_code_system_message_prompt = SystemMessagePromptTemplate.from_template(
    streamlit_code_template
)

streamlit_code_human_template = """Write a streamlit code by looking at the logic code and test code to accomplish the GOAL with the given title. Also when the result is ready add st.balloons() to the code 

GOAL: {topic}
--------- 
Logic Code:
{logic_code} 
---------
Test Code:
{test_code} 
---------
Streamlit Application Title: {title}
Add st.title({title}) to the app
---------
Stremlit Code:
"""

streamlit_code_human_message_prompt = HumanMessagePromptTemplate.from_template(
    streamlit_code_human_template
)

streamlit_code_prompt = ChatPromptTemplate.from_messages(
    [streamlit_code_system_message_prompt, streamlit_code_human_message_prompt]
)

__all__ = [
    "code_prompt",
    "test_prompt",
    "refine_chat_prompt",
    "fix_chat_prompt",
    "check_chat_prompt",
    "streamlit_code_prompt",
]
