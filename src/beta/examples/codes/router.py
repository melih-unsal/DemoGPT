# Router
# This notebook demonstrates how to use the RouterChain paradigm to create a chain that dynamically selects the next chain to use for a given input.

# Router chains are made up of two components:
# - The RouterChain itself (responsible for selecting the next chain to call)
# - destination_chains: chains that the router chain can route to

from langchain.chains import ConversationChain
from langchain.chains.llm import LLMChain

# Import necessary modules
from langchain.chains.router import MultiPromptChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Define the physics and math templates
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

# Define the prompt information
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

# Create an instance of the OpenAI language model
llm = OpenAI()

# Create the destination chains dictionary
destination_chains = {}
for p_info in prompt_infos:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
    chain = LLMChain(llm=llm, prompt=prompt)
    destination_chains[name] = chain

# Create the default chain
default_chain = ConversationChain(llm=llm, output_key="text")

# LLMRouterChain
# This chain uses an LLM to determine how to route things.

# Import necessary modules
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE

# Create the destinations string
destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)

# Create the router template and prompt
router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

# Create the router chain
router_chain = LLMRouterChain.from_llm(llm, router_prompt)

# Create the MultiPromptChain
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=default_chain,
    verbose=True,
)

# Run the chain with a physics question
print(chain.run("What is black body radiation?"))

# Run the chain with a math question
print(
    chain.run(
        "What is the first prime number greater than 40 such that one plus the prime number is divisible by 3"
    )
)

# Run the chain with a general question
print(chain.run("What is the name of the type of cloud that rains?"))

# EmbeddingRouterChain
# The EmbeddingRouterChain uses embeddings and similarity to route between destination chains.

# Import necessary modules
from langchain.chains.router.embedding_router import EmbeddingRouterChain
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Chroma

# Define the names and descriptions
names_and_descriptions = [
    ("physics", ["for questions about physics"]),
    ("math", ["for questions about math"]),
]

# Create the router chain
router_chain = EmbeddingRouterChain.from_names_and_descriptions(
    names_and_descriptions, Chroma, CohereEmbeddings(), routing_keys=["input"]
)

# Create the MultiPromptChain
chain = MultiPromptChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=default_chain,
    verbose=True,
)

# Run the chain with a physics question
print(chain.run("What is black body radiation?"))

# Run the chain with a math question
print(
    chain.run(
        "What is the first prime number greater than 40 such that one plus the prime number is divisible by 3"
    )
)
