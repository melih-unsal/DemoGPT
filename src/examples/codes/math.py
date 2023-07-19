"""
Math chain
This notebook showcases using LLMs and Python REPLs to do complex word math problems.
"""

from langchain import OpenAI, LLMMathChain

llm = OpenAI(temperature=0)
llm_math = LLMMathChain.from_llm(llm, verbose=True)

llm_math.run("What is 13 raised to the .3432 power?")
