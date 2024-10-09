import os

from langchain.agents import AgentType, initialize_agent

class Assistant:
    def __init__(self, tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False):
        self.agent = initialize_agent(tools=tools, llm=llm, agent=agent_type, verbose=verbose)
    
    def ask(self, prompt):
        return self.agent.run(prompt)    

if __name__ == "__main__":
    from demogpt.tools import DuckDuckGoSearchTool
    from demogpt.llms import OpenAIModel
    assistant = Assistant(tools=[DuckDuckGoSearchTool()], llm=OpenAIModel(model_name="gpt-4o-mini"))
    query = "What is the capital of France?"
    print(assistant.ask(query))