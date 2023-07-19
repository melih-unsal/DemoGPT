import os

from dotenv import load_dotenv
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

template = f"""
    You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. You use langchain library. Don't explain the code, just generate the code block itself.
    Keep in mind that 
    OPENAI API KEY is {OPENAI_API_KEY}
    So, you can use this kind of code below:
    openai.api_key = '{OPENAI_API_KEY}'

    or 

    llm = ChatOpenAI(
        openai_api_key='{OPENAI_API_KEY}'
    )

    """
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template1 = (
    """You wrote a python code {code} using langchain library to do the task: {topic}.
                        You got the error {error} 
                        
                        Please refine the code using the following document and feedback
                        
                        document:{document}  

                        feedback:{feedback}
                        
                        If you want to use API Key, please use """
    + OPENAI_API_KEY
)
human_message_prompt1 = HumanMessagePromptTemplate.from_template(human_template1)
human_template2 = """Write a python code using the plan and document below to generate {topic} function and test it.
plan:
{plan}
---------
document:
{document}
---------
"""
human_message_prompt2 = HumanMessagePromptTemplate.from_template(human_template2)
human_template3 = """
    ##### Find the bugs in the below Python code
    
    ### Buggy Python
    {code}

    ### Error
    {error}

    ### Error Reason
    """
human_message_prompt3 = HumanMessagePromptTemplate.from_template(human_template3)

refine_remplate = """
Examples:
{document}
================================================================
Based on the critics, fix the content provided to you. {instruction_hint}:
content:
{content}
---------
critics:
{critics}
---------
Python Code:
import
"""

refine_message_prompt = HumanMessagePromptTemplate.from_template(refine_remplate)

plan_remplate = """
You have to create a plan to generate LangChain code to generate {topic} function and test it. 
While creating the plan, you have the LangChain document that you can use for.

document:
{document}
---------
"""

plan_message_prompt = HumanMessagePromptTemplate.from_template(plan_remplate)


with_code_chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt1]
)
without_code_chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt2]
)
fix_chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt3])
refine_chat_prompt = ChatPromptTemplate.from_messages([refine_message_prompt])
plan_chat_prompt = ChatPromptTemplate.from_messages([plan_message_prompt])


__all__ = [
    "with_code_chat_prompt",
    "without_code_chat_prompt",
    "fix_chat_prompt",
    "refine_chat_prompt",
    "plan_chat_prompt",
]
