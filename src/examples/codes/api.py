# API chains
# APIChain enables using LLMs to interact with APIs to retrieve relevant information. Construct the chain by providing a question relevant to the provided API documentation.

# Import necessary modules
from langchain.chains.api.prompt import API_RESPONSE_PROMPT
from langchain.chains import APIChain
from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI

# Create an instance of the OpenAI language model
llm = OpenAI(temperature=0)

# OpenMeteo Example
from langchain.chains.api import open_meteo_docs

# Create an APIChain using the OpenMeteo API documentation
chain_new = APIChain.from_llm_and_api_docs(
    llm, open_meteo_docs.OPEN_METEO_DOCS, verbose=True
)

# Run the APIChain with a specific question
result = chain_new.run(
    "What is the weather like right now in Munich, Germany in degrees Fahrenheit?"
)
print(result)
