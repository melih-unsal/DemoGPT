# LLMChain Python Code

# Import necessary modules
from langchain import PromptTemplate, OpenAI, LLMChain

# Define the prompt template
prompt_template = "What is a good name for a company that makes {product}?"

# Create an instance of the OpenAI language model
llm = OpenAI(temperature=0)

# Create an instance of LLMChain
llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))

# Call the LLMChain with an input
output = llm_chain("colorful socks")
print(output)

# Additional ways of running LLM Chain

# Apply the chain logic to a list of inputs
input_list = [{"product": "socks"}, {"product": "computer"}, {"product": "shoes"}]
output_list = llm_chain.apply(input_list)
print(output_list)

# Generate LLMResult instead of string
result = llm_chain.generate(input_list)
print(result)

# Predict using keyword arguments
output_single = llm_chain.predict(product="colorful socks")
print(output_single)

# Multiple inputs example
template = """Tell me a {adjective} joke about {subject}."""
prompt = PromptTemplate(template=template, input_variables=["adjective", "subject"])
llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0))
output_multiple = llm_chain.predict(adjective="sad", subject="ducks")
print(output_multiple)

# Parsing the outputs
from langchain.output_parsers import CommaSeparatedListOutputParser

output_parser = CommaSeparatedListOutputParser()
template = """List all the colors in a rainbow"""
prompt = PromptTemplate(
    template=template, input_variables=[], output_parser=output_parser
)
llm_chain = LLMChain(prompt=prompt, llm=llm)
output_parsed = llm_chain.predict()
print(output_parsed)

# Initialize from string
template = """Tell me a {adjective} joke about {subject}."""
llm_chain = LLMChain.from_string(llm=llm, template=template)
output_initialized = llm_chain.predict(adjective="sad", subject="ducks")
print(output_initialized)
