# Dynamically selecting from multiple prompts
# This notebook demonstrates how to use the RouterChain paradigm to create a chain that dynamically selects the prompt to use for a given input. Specifically we show how to use the MultiPromptChain to create a question-answering chain that selects the prompt which is most relevant for a given question, and then answers the question using that prompt.

from langchain.chains.router import MultiPromptChain
from langchain.llms import OpenAI

physics_template = """You are a very smart physics professor. \
You are great at answering questions about physics in a concise and easy to understand manner. \
When you don't know the answer to a question you admit that you don't know.

Here is a question:
{input}"""


math_template = """You are a very good mathematician. You are great at answering math questions. \
You are so good because you are able to break down hard problems into their component parts, \
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{input}"""

prompt_infos = [
    {
        "name": "physics",
        "description": "Good for answering questions about physics",
        "prompt_template": physics_template,
    },
    {
        "name": "math",
        "description": "Good for answering math questions",
        "prompt_template": math_template,
    },
]

chain = MultiPromptChain.from_prompts(OpenAI(), prompt_infos, verbose=True)

print(chain.run("What is black body radiation?"))
