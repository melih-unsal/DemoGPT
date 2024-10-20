from langchain_community.utilities import StackExchangeAPIWrapper
from demogpt_agenthub.tools import BaseTool

class StackOverFlowTool(BaseTool):
    def __init__(self):
        self.tool = StackExchangeAPIWrapper()
        super().__init__()
        
    def run(self, query):
        return self.tool.run(query)
    
if __name__ == "__main__":
    query = "How to create a list in python"
    tool = StackOverFlowTool()
    print(tool.run(query))