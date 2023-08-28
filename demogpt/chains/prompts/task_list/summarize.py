system_template = """
You will summarization code with a strict structure like in the below but 
loader will change depending on the input
###
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
###
"""

human_template = """
Here is the part of the code that you are supposed to continue:
{code_snippets}

Write a summarize function for the argument name and variable below:
Argument Name : {argument}
Variable Name : {variable}
Summarization Code:
"""
