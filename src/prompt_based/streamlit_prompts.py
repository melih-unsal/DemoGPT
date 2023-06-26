from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

template = """
    You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. 
    You will get a GOAL.
    You will get a logic code and test code.
    Logic code includes the logic part
    Test code includes the test part which tests the logic code
    Your tasks is generating a stremlit code which does the same thing that the test code does to accomplish the GOAL.
    """
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template = """Write a streamlit code by looking at the logic code and test code to accomplish the GOAL with the given title. Also add st.balloons() to the code

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

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

streamlit_code_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

__all__ = ['streamlit_code_prompt']