# Self-checking chain
# This notebook showcases how to use LLMCheckerChain.

from langchain.chains import LLMCheckerChain
from langchain.llms import OpenAI

# Create an instance of the OpenAI language model
llm = OpenAI(temperature=0.7)

# Define the input text
text = "What type of mammal lays the biggest eggs?"

# Create an instance of LLMCheckerChain using the OpenAI language model
checker_chain = LLMCheckerChain.from_llm(llm, verbose=True)

# Run the checker chain on the input text
checker_chain.run(text)

# Output the result
# No mammal lays the biggest eggs. The Elephant Bird, which was a species of giant bird, laid the largest eggs of any bird.
