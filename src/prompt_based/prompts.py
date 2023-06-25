from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

template1 = f"""
    You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. You use langchain library. You are good at using PromptTemplate to give appropriate prompt to accomplish the task.
      Don't explain the code, just generate the code block itself.
      Most of the time, langchain code includes these useful imports below:
        from langchain import LLMChain
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts.chat import (
            ChatPromptTemplate,
            SystemMessagePromptTemplate,
            HumanMessagePromptTemplate,
        )
    """
system_message_prompt1 = SystemMessagePromptTemplate.from_template(template1)

human_template1 = """Write a python code using the document below which make it possible to do {topic}. 
Create this function and test it.
document:
{document}
---------
Python Code:

### imports

### function generation
    ### system_message_prompt generation
    ### human_message_prompt
    ### LLMChain object creation
    ### run the chain
    ### return the result

### function testing
"""

human_message_prompt1 = HumanMessagePromptTemplate.from_template(human_template1)

code_prompt = ChatPromptTemplate.from_messages([system_message_prompt1, human_message_prompt1])

template2 = """
    You are a helpful code assistant that can teach a junior developer how to code. Your language of choice is Python. You will get a python code and generate python code to test out the function in that python code to accomplish the task.
      Don't explain the code, just generate the code block itself.
      Example:

      Python Code:
        
        template="You are a helpful assistant that translates {input_language} to {output_language}."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template="{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        prompt=PromptTemplate(
            template="You are a helpful assistant that translates {input_language} to {output_language}.",
            input_variables=["input_language", "output_language"]
            )
        

    """

system_message_prompt2 = SystemMessagePromptTemplate.from_template(template2)

human_template2 = """Generate a sample input and test the function inside the python script below which makes it possible to do {topic}. 
Python Code:
{code}
---------
Function Test:
"""

human_message_prompt2 = HumanMessagePromptTemplate.from_template(human_template2)

test_prompt = ChatPromptTemplate.from_messages([system_message_prompt2, human_message_prompt2])


refine_remplate = """
Based on the critics, fix the content provided to you while you can use the document. {instruction_hint}:
content:
{content}
---------
critics:
{critics}
---------
document:
{document}
---------
"""

refine_message_prompt = HumanMessagePromptTemplate.from_template(refine_remplate)

refine_chat_prompt = ChatPromptTemplate.from_messages([refine_message_prompt])


human_template3 = """
    ##### Find the bugs in the below Python code
    
    ### Buggy Python
    {code}

    ### Error
    {error}

    ### Error Reason
    """

human_message_prompt3 = HumanMessagePromptTemplate.from_template(human_template3)

fix_chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt3])



__all__ = ['code_prompt','test_prompt','refine_chat_prompt','fix_chat_prompt']